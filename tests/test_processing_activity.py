"""Person-authored processing-activity contract (FR-028)."""

from __future__ import annotations

import json
import subprocess

import pytest
import yaml
from conftest import (
    MANIFEST_PATH,
    PACKAGE_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    engine_tool,
    validation_module_args,
)
from test_regulated_categories import _extract, _record


def run_bundle(tmp_path, activity: str, targets: dict[str, str]):
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "activity.md").write_text(activity)
    for name, text in targets.items():
        (bundle / name).write_text(text)
    return subprocess.run(
        [
            engine_tool("quire"),
            "validate",
            "--okf",
            *validation_module_args(PACKAGE_ROOT, include_iso=True),
            str(bundle),
        ],
        capture_output=True,
        text=True,
    )


def target_doc(kind: str, ident: str) -> str:
    return (
        "---\n"
        f"id: {ident}\n"
        f"title: {ident}\n"
        f"type: {kind}\n"
        f"object: {kind}\n"
        "---\n"
        f"# {ident}\n"
    )


@pytest.mark.trace("TC-248", "FR-028-AC-1", "TC-254", "FR-028-AC-7")
def test_controller_skeleton_with_scoped_connection_validates(tmp_path):
    skeleton = (SKELETONS_DIR / "processing_activity.md").read_text()
    result = run_bundle(
        tmp_path,
        skeleton,
        {"connection.md": target_doc("connection", "CONN-001")},
    )
    assert result.returncode == 0, result.stdout + result.stderr


def frontmatter_doc(**changes) -> str:
    values = {
        "id": "PA-001",
        "title": '"Customer support processing"',
        "type": "processing_activity",
        "object": "processing_activity",
        "role": "controller",
        "controller": '"Controller; privacy@example.invalid"',
        "purposes": '["provide support"]',
        "data_subject_categories": '["customers"]',
        "retention": '"support period"',
        "home_regions": "[eu]",
        "relationships": "\n  - target: CONN-001\n    type: scopes",
    }
    values.update(changes)
    fields = "".join(f"{key}: {value}\n" for key, value in values.items())
    return f"---\n{fields}---\n# Processing activity\n"


@pytest.mark.trace("TC-248", "FR-028-AC-1")
def test_controller_activity_record_requires_scalar_identity_and_context(
    schema_registry,
):
    record = {
        "role": "controller",
        "controller": "Controller; privacy@example.invalid",
        "purposes": ["provide support"],
        "data_subject_categories": ["customers"],
        "retention": "support period",
        "home_regions": ["eu"],
    }
    validator = schema_registry("ProcessingActivity")
    assert validator.is_valid(record)
    assert not validator.is_valid({**record, "controller": [record["controller"]]})


@pytest.mark.trace("TC-249", "FR-028-AC-2")
def test_processor_activity_accepts_nonempty_controller_list_without_controller_context(
    schema_registry,
):
    record = {
        "role": "processor",
        "processor": "Processor; privacy@example.invalid",
        "controller": ["Controller; privacy@example.invalid"],
        "home_regions": ["eea"],
    }
    assert schema_registry("ProcessingActivityFrontmatter").is_valid(record)
    assert schema_registry("ProcessingActivity").is_valid(record)
    assert not {"purposes", "data_subject_categories", "retention"} & set(record)


@pytest.mark.trace("TC-250", "FR-028-AC-3")
def test_missing_role_specific_fields_fail_with_field_named_schema_errors(
    schema_registry,
):
    validator = schema_registry("ProcessingActivityFrontmatter")
    controller = {
        "role": "controller",
        "controller": "Controller; privacy@example.invalid",
        "data_subject_categories": ["customers"],
        "home_regions": ["US"],
    }
    errors = list(validator.iter_errors(controller))
    assert any("purposes" in error.message for error in errors), errors
    processor = {
        "role": "processor",
        "controller": [],
        "home_regions": ["US"],
    }
    errors = list(validator.iter_errors(processor))
    assert any("processor" in error.message for error in errors), errors
    assert any(error.json_path.startswith("$.controller") for error in errors), errors


@pytest.mark.trace("TC-251", "FR-028-AC-4")
def test_unknown_role_and_invalid_home_regions_fail_naming_the_field(schema_registry):
    validator = schema_registry("ProcessingActivityFrontmatter")
    valid = {
        "role": "controller",
        "controller": "Controller; privacy@example.invalid",
        "purposes": ["provide support"],
        "data_subject_categories": ["customers"],
        "retention": "support period",
        "home_regions": ["US"],
    }
    for key, value in (
        ("role", "unknown"),
        ("home_regions", []),
        ("home_regions", ["usa"]),
    ):
        errors = list(validator.iter_errors({**valid, key: value}))
        assert errors, (key, value)
        assert any(
            key in error.message or key in error.json_path for error in errors
        ), errors


@pytest.mark.trace("TC-252", "FR-028-AC-5")
def test_missing_scopes_edge_emits_located_advisory_warning(tmp_path):
    skeleton = (SKELETONS_DIR / "processing_activity.md").read_text()
    skeleton = skeleton.replace(
        "relationships:\n  - target: CONN-001\n    type: scopes\n", ""
    )
    result = run_bundle(
        tmp_path,
        skeleton,
        {"connection.md": target_doc("connection", "CONN-001")},
    )
    assert result.returncode == 0, result.stdout + result.stderr
    output = result.stdout + result.stderr
    assert "activity.md" in output
    assert "processing-activity-scopes-nothing" in output
    assert "has no 'scopes' edge" in output


@pytest.mark.trace("TC-253", "FR-028-AC-6")
@pytest.mark.parametrize(
    ("target", "kind", "expected"),
    [("QUEUE-001", "queue", "disallowed"), ("MISSING-1", None, "dangling")],
)
def test_invalid_scopes_target_reports_wrong_kind_or_dangling(
    tmp_path, target, kind, expected
):
    skeleton = (
        (SKELETONS_DIR / "processing_activity.md")
        .read_text()
        .replace("CONN-001", target)
    )
    targets = {"target.md": target_doc(kind, target)} if kind else {}
    result = run_bundle(tmp_path, skeleton, targets)
    output = result.stdout + result.stderr
    assert expected in output.lower(), output


@pytest.mark.trace("TC-254", "FR-028-AC-7")
def test_manifest_exports_schema_and_skeleton_for_processing_activity():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert "processing_activity" in manifest["semantic"]["exports"]
    declared = next(
        o for o in manifest["object_types"] if o["name"] == "processing_activity"
    )
    assert declared["frontmatter_schema_ref"] == (
        "schemas/ProcessingActivityFrontmatter.json"
    )
    assert declared["data_schema"]["schema"] == "schemas/ProcessingActivity.json"
    assert declared["allowed_links"]["scopes"] == ["connection", "data_sink", "part"]
    required = manifest["traceability"]["required_relations"]
    assert any(
        item["from"] == "processing_activity"
        and item["edges"] == ["scopes"]
        and item["to"] == ["connection", "data_sink", "part"]
        for item in required
    )
    assert (SCHEMAS_DIR / "ProcessingActivity.json").is_file()
    assert (SCHEMAS_DIR / "ProcessingActivityFrontmatter.json").is_file()
    assert (SKELETONS_DIR / "processing_activity.md").is_file()
    for name in ("ProcessingActivityFrontmatter", "DataClassificationFrontmatter"):
        schema = json.loads((SCHEMAS_DIR / f"{name}.json").read_text())
        assert '"$ref"' not in json.dumps(schema), name
    result = subprocess.run(
        ["node", "scripts/generate-schemas.mjs", "--check"],
        cwd=PACKAGE_ROOT.parent,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.trace("TC-255", "FR-028-AC-8")
def test_omitted_optional_processor_fields_are_absent_from_extracted_record(
    quire_engine, semantic_block, semantic_module, bundle_index
):
    markdown = frontmatter_doc(
        role="processor",
        controller='["Controller; privacy@example.invalid"]',
        processor='"Processor; privacy@example.invalid"',
        purposes=None,
        data_subject_categories=None,
        retention=None,
        joint_controllers=None,
        representative=None,
        dpo_contact=None,
    )
    markdown = "\n".join(
        line for line in markdown.splitlines() if not line.endswith(": None")
    )
    output = _extract(
        quire_engine,
        semantic_block,
        semantic_module,
        "processing-activity.md",
        text=markdown,
        kind="processing_activity",
        bundle=bundle_index,
    )
    record = _record(output)
    assert record.get("role") == "processor"
    assert record.get("controller") == ["Controller; privacy@example.invalid"]
    assert record.get("processor") == "Processor; privacy@example.invalid"
    for key in (
        "purposes",
        "data_subject_categories",
        "retention",
        "joint_controllers",
        "representative",
        "dpo_contact",
    ):
        assert key not in record, (key, record)
