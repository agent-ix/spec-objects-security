"""The optional risk-control option type on a control (FR-029)."""

from __future__ import annotations

import pytest
import yaml

from tests.conftest import CLAUSE, PACKAGE_ROOT, field
from tests.test_regulated_categories import _schema

OPTIONS = ["design", "protective", "information"]


def _record(**extra) -> dict:
    return {"clauses": [CLAUSE], "fields": [field("effectiveness")], **extra}


@pytest.mark.trace("FR-029-AC-1")
def test_the_option_enum_is_closed_and_the_key_is_optional_without_default(
    schema_registry,
):
    assert _schema("ControlOptionType")["enum"] == OPTIONS
    control = _schema("Control")
    assert control["properties"]["option_type"]["$ref"].endswith(
        "/ControlOptionType.json"
    )
    frontmatter = _schema("ControlFrontmatter")
    assert frontmatter["properties"]["option_type"]["enum"] == OPTIONS
    for schema in (control, frontmatter):
        assert "default" not in schema["properties"]["option_type"]
        assert "option_type" not in schema.get("required", [])


@pytest.mark.trace("FR-029-AC-2")
def test_a_control_record_admits_each_option_and_refuses_anything_else(
    schema_registry,
):
    record_schema = schema_registry("Control")
    assert record_schema.is_valid(_record())
    for value in OPTIONS:
        assert record_schema.is_valid(_record(option_type=value)), value
    for invalid in ("unknown", "", ["design"], None, 1):
        assert not record_schema.is_valid(_record(option_type=invalid)), invalid
    frontmatter = schema_registry("ControlFrontmatter")
    assert frontmatter.is_valid({"id": "CTRL-1", "option_type": "protective"})
    assert not frontmatter.is_valid({"id": "CTRL-1", "option_type": "shield"})


def _control_entry() -> dict:
    manifest = yaml.safe_load((PACKAGE_ROOT / "manifest.yaml").read_text())
    return next(t for t in manifest["object_types"] if t["name"] == "control")


@pytest.mark.trace("FR-029-AC-3")
def test_the_control_entry_extracts_option_type_from_frontmatter():
    locator = _control_entry()["body_extraction"]["yield_pattern"]["match"][
        "option_type"
    ]
    assert locator == {
        "from": "frontmatter_field",
        "path": ["option_type"],
        "required": False,
    }


@pytest.mark.trace("FR-029-AC-4")
def test_no_rule_or_relation_names_option_type():
    manifest = yaml.safe_load((PACKAGE_ROOT / "manifest.yaml").read_text())
    # The extraction locator is the one place the key is named; every other
    # section (edge_types, allowed_links, grammar_severity, lint_rules,
    # traceability, ...) must not mention it.
    for object_type in manifest.get("object_types", []):
        object_type.pop("body_extraction", None)
    assert "option_type" not in yaml.safe_dump(manifest)
