"""Addressable anomaly records remain separate from nested SOUP anomalies."""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest
import yaml

from tests.conftest import (
    MANIFEST_PATH,
    PACKAGE_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    engine_tool,
    field,
    frontmatter,
    object_type,
    validation_module_args,
)

ANOMALY_SKELETON = SKELETONS_DIR / "anomaly.md"
VULNERABILITY_SKELETON = SKELETONS_DIR / "vulnerability.md"


def statement_field(*, target="String", min_length=1):
    decl = field("statement", target)
    decl["constraints"] = [
        {
            "kind": "MinLengthConstraint",
            "value": {"keyword": "minLength", "value": min_length},
        }
    ]
    return decl


def anomaly_record(
    *, identity=True, statement=True, target="String", min_length=1, constrained=True
):
    fields = []
    if identity:
        fields.append(field("anomaly_id", "UUID", identity=True))
    if statement:
        value = statement_field(target=target, min_length=min_length)
        if not constrained:
            del value["constraints"]
        fields.append(value)
    return {"fields": fields}


def validate(root, *flags):
    return subprocess.run(
        [
            engine_tool("quire"),
            "validate",
            "--okf",
            *flags,
            *validation_module_args(PACKAGE_ROOT, include_iso=True),
            str(root),
        ],
        capture_output=True,
        text=True,
    )


def linked_vulnerability(root, target, target_type):
    text = VULNERABILITY_SKELETON.read_text()
    rel = "relationships:\n" f"  - target: {target}\n" "    type: references\n"
    text = text.replace("severity: high\n", f"severity: high\n{rel}", 1)
    (root / "vulnerability.md").write_text(text)
    if target_type == "anomaly":
        shutil.copy(ANOMALY_SKELETON, root / "anomaly.md")
    else:
        shutil.copy(SKELETONS_DIR / f"{target_type}.md", root / f"{target_type}.md")


@pytest.mark.trace("FR-032-AC-7", "FR-004-AC-17")
def test_module_exports_anomaly_record_and_ships_its_skeleton(quire_engine):
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert "anomaly" in manifest["semantic"]["exports"]
    anomaly_type = next(
        item for item in manifest["object_types"] if item["name"] == "anomaly"
    )
    assert anomaly_type["data_schema"]["schema"] == "schemas/AnomalyRecord.json"
    assert (SCHEMAS_DIR / "AnomalyRecord.json").is_file()
    result = quire_engine.validate_document(
        "anomaly", str(PACKAGE_ROOT), ANOMALY_SKELETON.read_text()
    )
    assert result["is_valid"], result["errors"]
    assert frontmatter(ANOMALY_SKELETON.read_text())["object"] == "anomaly"


@pytest.mark.trace("FR-032-AC-8", "FR-004-AC-17")
def test_anomaly_record_requires_identity_and_nonempty_string_statement(
    schema_registry,
):
    validator = schema_registry("AnomalyRecord")
    assert validator.is_valid(anomaly_record())
    assert validator.is_valid(
        {
            **anomaly_record(),
            "source_ref": "ix://agent-ix/quoin/FIND-001",
            "origin": "field",
        }
    )
    assert not validator.is_valid(anomaly_record(identity=False))
    assert not validator.is_valid(anomaly_record(statement=False))
    assert not validator.is_valid(anomaly_record(target="Integer"))
    assert not validator.is_valid(anomaly_record(constrained=False))
    assert not validator.is_valid(anomaly_record(min_length=0))


@pytest.mark.trace("FR-032-AC-5", "FR-032-AC-9")
def test_vulnerability_reference_targets_include_anomaly_but_refuse_threat(tmp_path):
    vulnerability = object_type("vulnerability")
    assert "soup_record" in vulnerability["allowed_links"]["affects"]
    assert vulnerability["allowed_links"]["references"] == [
        "vulnerability",
        "anomaly",
    ]
    anomaly_id = frontmatter(ANOMALY_SKELETON.read_text())["id"]
    linked_vulnerability(tmp_path, anomaly_id, "anomaly")
    valid = validate(tmp_path)
    assert valid.returncode == 0, valid.stderr
    assert "disallowed-edge-target" not in valid.stderr, valid.stderr

    threat_id = frontmatter((SKELETONS_DIR / "threat.md").read_text())["id"]
    linked_vulnerability(tmp_path, threat_id, "threat")
    invalid = validate(tmp_path)
    failures = [
        line
        for line in invalid.stderr.splitlines()
        if line.endswith("[disallowed-edge-target]")
    ]
    assert len(failures) == 1, invalid.stderr
    assert "target type 'threat'" in failures[0]


@pytest.mark.trace("FR-032-AC-10")
def test_nested_soup_anomaly_keeps_its_independent_shape(schema_registry):
    validator = schema_registry("SoupRecord")
    soup_schema = json.loads((SCHEMAS_DIR / "SoupRecord.json").read_text())
    nested_schema = json.loads((SCHEMAS_DIR / "Anomaly.json").read_text())
    assert soup_schema["properties"]["known_anomalies"]["items"]["$ref"].endswith(
        "/Anomaly.json"
    )
    assert nested_schema["required"] == ["statement"]
    assert "fields" not in nested_schema["properties"]
    base = {
        "fields": [field("component_id", "UUID", identity=True), field("purl")],
        "purl": "pkg:cargo/example-http-client@1.4.2",
        "known_anomalies": [{"statement": "The component truncates long tokens."}],
    }
    assert validator.is_valid(base)
    bad = {
        **base,
        "known_anomalies": [
            {"statement": "The component truncates long tokens.", "identity": True}
        ],
    }
    assert not validator.is_valid(bad)
