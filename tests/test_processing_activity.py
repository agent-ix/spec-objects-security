"""Person-authored processing-activity contract (FR-028)."""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest
import yaml

from conftest import (
    MANIFEST_PATH,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    engine_tool,
    PACKAGE_ROOT,
    validation_module_args,
)


@pytest.mark.trace(
    "FR-028-AC-1",
    "FR-028-AC-2",
    "FR-028-AC-3",
    "FR-028-AC-4",
    "FR-028-AC-8",
)
def test_role_specific_frontmatter_has_no_defaults_or_derived_fields(schema_registry):
    validator = schema_registry("ProcessingActivityFrontmatter")
    controller = {
        "role": "controller",
        "controller": "Controller; privacy@example.invalid",
        "purposes": ["provide support"],
        "data_subject_categories": ["customers"],
        "retention": "support period",
        "home_regions": ["US", "eu"],
    }
    processor = {
        "role": "processor",
        "processor": "Processor; privacy@example.invalid",
        "controller": ["Controller; privacy@example.invalid"],
        "home_regions": ["eea"],
    }
    assert validator.is_valid(controller)
    assert validator.is_valid(processor)
    assert not validator.is_valid({**controller, "retention": ""})
    assert not validator.is_valid(
        {key: value for key, value in controller.items() if key != "purposes"}
    )
    assert not validator.is_valid({**processor, "processor": ""})
    assert not validator.is_valid({**processor, "controller": []})
    assert not validator.is_valid({**controller, "role": "unknown"})
    assert not validator.is_valid({**controller, "home_regions": []})
    assert not validator.is_valid({**controller, "home_regions": ["usa"]})
    assert '"default"' not in json.dumps(validator.schema)
    assert not {"purposes", "data_subject_categories", "retention"} & set(processor)


@pytest.mark.trace("FR-028-AC-7")
def test_frontmatter_schemas_have_no_module_sibling_refs():
    for name in (
        "ProcessingActivityFrontmatter",
        "DataClassificationFrontmatter",
    ):
        text = (SCHEMAS_DIR / f"{name}.json").read_text()
        assert "\"$ref\"" not in text, name


@pytest.mark.trace("FR-028-AC-5", "FR-028-AC-6", "FR-028-AC-7")
def test_manifest_exports_processing_activity_and_declares_coverage():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert "processing_activity" in manifest["semantic"]["exports"]
    declared = next(
        o for o in manifest["object_types"] if o["name"] == "processing_activity"
    )
    assert declared["frontmatter_schema_ref"] == "schemas/ProcessingActivityFrontmatter.json"
    assert declared["data_schema"]["schema"] == "schemas/ProcessingActivity.json"
    assert declared["allowed_links"]["covers"] == ["connection", "data_sink", "part"]
    req = manifest["traceability"]["required_relations"]
    assert any(
        item["from"] == "processing_activity"
        and item["edges"] == ["covers"]
        and item["to"] == ["connection", "data_sink", "part"]
        for item in req
    )


def test_skeleton_has_required_fields_and_covers_edge():
    text = (SKELETONS_DIR / "processing_activity.md").read_text()
    assert "role: controller" in text
    assert "role: processor" in text
    assert "type: covers" in text
    assert "home_regions:" in text


@pytest.mark.trace("FR-028-AC-5", "FR-028-AC-6", "FR-028-AC-7")
def test_skeleton_validates_with_its_covered_connection(tmp_path):
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    shutil.copy(
        SKELETONS_DIR / "processing_activity.md", bundle / "activity.md"
    )
    (bundle / "connection.md").write_text(
        "---\n"
        "id: CONN-001\n"
        "title: connection\n"
        "type: connection\n"
        "object: connection\n"
        "---\n"
        "# Connection\n"
    )
    result = subprocess.run(
        [
            engine_tool("quire"),
            "validate",
            "--okf",
            *validation_module_args(PACKAGE_ROOT),
            str(bundle),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
