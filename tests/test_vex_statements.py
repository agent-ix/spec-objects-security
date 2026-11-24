"""Optional authored VEX statements on SOUP records (FR-022)."""

from __future__ import annotations

import json

import pytest

from tests.conftest import SCHEMAS_DIR, field

STATUSES = ("affected", "not_affected", "under_investigation", "fixed")
JUSTIFICATIONS = (
    "component_not_present",
    "vulnerable_code_not_present",
    "vulnerable_code_not_in_execute_path",
    "vulnerable_code_cannot_be_controlled_by_adversary",
    "inline_mitigations_already_exist",
)
DATE = "2026-11-24"


def record(**extra):
    return {
        "fields": [field("component_id", "UUID", identity=True), field("purl")],
        "purl": "pkg:cargo/example-http-client@1.4.2",
        **extra,
    }


def statement(**extra):
    return {
        "advisory": "CVE-2026-12345",
        "status": "under_investigation",
        "assessed_by": "Ada Example",
        "assessed_at": DATE,
        **extra,
    }


def schema():
    return json.loads((SCHEMAS_DIR / "SoupRecord.json").read_text())


def keywords(node, found=None):
    found = set() if found is None else found
    if isinstance(node, dict):
        found.update(node)
        for value in node.values():
            keywords(value, found)
    elif isinstance(node, list):
        for value in node:
            keywords(value, found)
    return found


def errors(validator, value):
    return list(validator.iter_errors(value))


def names_field(validator, value, field_name):
    return any(
        field_name in error.path or field_name in error.message
        for error in errors(validator, value)
    )


@pytest.mark.trace("FR-022-AC-1", "FR-022-AC-8", "FR-022-AC-9")
def test_vex_statements_are_optional_and_have_no_defaults(schema_registry):
    validator = schema_registry("SoupRecord")
    assert validator.is_valid(record())
    assert validator.is_valid(record(vex_statements=[]))
    assert "vex_statements" not in record()
    assert "vex_statements" not in schema()["required"]
    assert "default" not in keywords(schema())
    assert schema()["properties"]["vex_statements"]["type"] == "array"
    assert schema()["properties"]["vex_statements"]["items"]["$ref"].endswith(
        "/VexStatement.json"
    )
    assert "decision" not in schema()["properties"]
    statement_schema = json.loads((SCHEMAS_DIR / "VexStatement.json").read_text())
    assert "default" not in keywords(statement_schema)
    assert not validator.is_valid(record(unlisted_record_key="must be refused"))


@pytest.mark.trace("FR-022-AC-2")
def test_vex_status_vocabulary_is_closed(schema_registry):
    validator = schema_registry("SoupRecord")
    status_schema = json.loads((SCHEMAS_DIR / "VexStatus.json").read_text())
    assert status_schema["enum"] == list(STATUSES)
    for status in STATUSES:
        item = statement(status=status)
        if status == "affected":
            item["action_statement"] = "Patch the affected dependency."
        if status == "not_affected":
            item["justification"] = "component_not_present"
        assert validator.is_valid(record(vex_statements=[item])), status
    bad = statement(status="not_exploitable")
    assert names_field(validator, record(vex_statements=[bad]), "status")


@pytest.mark.trace("FR-022-AC-3")
def test_not_affected_requires_one_closed_justification_vocabulary(schema_registry):
    validator = schema_registry("SoupRecord")
    justification_schema = json.loads(
        (SCHEMAS_DIR / "VexJustification.json").read_text()
    )
    assert justification_schema["enum"] == list(JUSTIFICATIONS)
    for justification in JUSTIFICATIONS:
        item = statement(status="not_affected", justification=justification)
        assert validator.is_valid(record(vex_statements=[item])), justification
    missing = statement(status="not_affected")
    assert names_field(validator, record(vex_statements=[missing]), "justification")
    invalid = statement(status="not_affected", justification="not_reachable")
    assert names_field(validator, record(vex_statements=[invalid]), "justification")


@pytest.mark.trace("FR-022-AC-4")
def test_affected_requires_a_nonblank_action_statement(schema_registry):
    validator = schema_registry("SoupRecord")
    assert validator.is_valid(
        record(
            vex_statements=[
                statement(status="affected", action_statement="Release a fix.")
            ]
        )
    )
    for item in (
        statement(status="affected"),
        statement(status="affected", action_statement=" "),
    ):
        assert names_field(validator, record(vex_statements=[item]), "action_statement")


@pytest.mark.trace("FR-022-AC-5")
def test_vex_assessor_and_date_are_required_and_validated(schema_registry):
    validator = schema_registry("SoupRecord")
    assert validator.is_valid(record(vex_statements=[statement()]))
    for key, value in (
        ("assessed_by", ""),
        ("assessed_by", " "),
        ("assessed_at", ""),
        ("assessed_at", "2027-02-29"),
        ("assessed_at", "2027-04-31"),
    ):
        item = statement(**{key: value})
        assert names_field(validator, record(vex_statements=[item]), key), (key, value)
    for key in ("assessed_by", "assessed_at"):
        item = statement()
        del item[key]
        assert names_field(validator, record(vex_statements=[item]), key), key


@pytest.mark.trace("FR-022-AC-6")
def test_same_advisory_with_different_assessment_dates_validates(schema_registry):
    validator = schema_registry("SoupRecord")
    first = statement(status="under_investigation")
    second = statement(
        status="fixed", advisory=first["advisory"], assessed_at="2026-11-25"
    )
    assert validator.is_valid(record(vex_statements=[first, second]))
    distinct = statement(status="fixed", advisory="CVE-2026-54321")
    assert validator.is_valid(record(vex_statements=[first, distinct]))


@pytest.mark.trace("FR-022-AC-7")
def test_evidence_refs_are_semantic_ids(schema_registry):
    validator = schema_registry("SoupRecord")
    valid = statement(evidence_refs=["ix://agent-ix/spec-objects-security/VULN-001"])
    assert validator.is_valid(record(vex_statements=[valid]))
    invalid = statement(evidence_refs=["VULN-001"])
    assert names_field(validator, record(vex_statements=[invalid]), "evidence_refs")
