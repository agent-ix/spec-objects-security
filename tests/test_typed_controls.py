"""Controls map to clause references; a scope_exclusion states a boundary.

FR-014 (clause-reference mappings, effectiveness), FR-015 (no standard text in a
mapping) and FR-016 (the `scope_exclusion` object type). Schema evidence uses
hand-built records; document evidence goes through the real engine.
"""

from __future__ import annotations

import json
import re

import pytest
import yaml

from tests.conftest import (
    MANIFEST_PATH,
    PACKAGE_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    locators,
    object_type,
)

BUNDLE = "agent-ix/spec-objects-security"
SET = "example.invalid/std@1"


def control_skeleton() -> str:
    return (SKELETONS_DIR / "control.md").read_text()


def exclusion_skeleton() -> str:
    return (SKELETONS_DIR / "scope_exclusion.md").read_text()


def validate(quire, kind: str, text: str, **kw) -> dict:
    return quire.validate_document(kind, str(PACKAGE_ROOT), text, **kw)


def messages(result: dict) -> list[str]:
    return [e["message"] for e in result["errors"]]


def schema(model: str) -> dict:
    return json.loads((SCHEMAS_DIR / f"{model}.json").read_text())


@pytest.fixture
def mapping(schema_registry):
    return schema_registry("ControlMapping")


@pytest.fixture
def exclusion(schema_registry):
    return schema_registry("ScopeExclusion")


def excl(**over):
    base = {
        "set": SET,
        "clause": "EX-1",
        "responsible": "ix://agent-ix/spec-objects-security/COMP-001",
        "rationale": "The platform owns it.",
    }
    return {**base, **over}


@pytest.mark.trace("TC-187", "FR-014-AC-1")
def test_mapping_requires_set_and_clause_and_refuses_the_old_keys(mapping):
    assert set(schema("ControlMapping")["required"]) == {"set", "clause"}
    assert mapping.is_valid({"set": SET, "clause": "EX-1"})
    for old in ("framework", "control_id", "doc"):
        assert not mapping.is_valid({"set": SET, "clause": "EX-1", old: "x"}), old
    assert not mapping.is_valid({"set": SET})
    assert not mapping.is_valid({"clause": "EX-1"})


@pytest.mark.trace("TC-188", "FR-014-AC-2")
def test_set_key_and_clause_id_shapes(mapping):
    ok = lambda s, c="EX-1": mapping.is_valid({"set": s, "clause": c})  # noqa: E731
    assert ok("example.invalid/std@1")
    for bad in (
        "example.invalid/std@",
        "example.invalid/@1",
        "/std@1",
        "std@1",
        "a/b/c@1",
        "a/b@1@2",
    ):
        assert not ok(bad), bad
    assert not ok(f"{'a' * 65}/b@1")
    assert ok(f"{'a' * 64}/b@1")
    assert not ok("a/b@" + "1" * 65)
    assert ok("a/b@" + "1" * 64)
    assert not ok(SET, "")
    assert not ok(SET, "c" * 65)
    assert ok(SET, "c" * 64)


@pytest.mark.trace("TC-189", "FR-014-AC-3")
def test_authored_control_mappings_and_effectiveness_are_validated(quire_engine):
    text = control_skeleton().replace("`not_assessed`", "`effective`")
    good = validate(quire_engine, "control", text)
    assert good["is_valid"], good["errors"]
    bad_set = validate(
        quire_engine,
        "control",
        text.replace("example.invalid/std@1 | EX-1", "std@1 | EX-1"),
    )
    assert any(
        "semantic.record-invalid" in m and "mappings" in m for m in messages(bad_set)
    ), bad_set["errors"]
    bogus = validate(quire_engine, "control", text.replace("`effective`", "`bogus`"))
    assert any(
        "semantic.record-invalid" in m and "effectiveness" in m for m in messages(bogus)
    ), bogus["errors"]


@pytest.mark.trace("TC-190", "FR-014-AC-4")
def test_control_skeleton_has_a_mappings_table_and_not_assessed_effectiveness(
    quire_engine,
):
    text = control_skeleton()
    result = validate(quire_engine, "control", text)
    assert result["is_valid"], result["errors"]
    section = re.search(r"^## Mappings\n(.*?)^## ", text, re.M | re.S).group(1)
    lines = [ln for ln in section.splitlines() if ln.strip()]
    assert lines[0].replace(" ", "") == "|Set|Clause|"
    assert all(ln.startswith("|") for ln in lines), lines
    assert len(lines) >= 3
    assert re.search(r"^## Effectiveness\n\n`not_assessed`\n", text, re.M)


@pytest.mark.trace("TC-191", "FR-014-AC-5")
def test_a_control_with_no_mappings_or_effectiveness_section_validates(quire_engine):
    text = control_skeleton()
    text = re.sub(r"^## Mappings\n.*?(?=^## Properties)", "", text, flags=re.M | re.S)
    assert "## Mappings" not in text.split("-->", 1)[1]
    assert "## Effectiveness" not in text.split("-->", 1)[1]
    result = validate(quire_engine, "control", text)
    assert result["is_valid"], result["errors"]


@pytest.mark.trace("TC-192", "FR-014-AC-7")
def test_control_manifest_mappings_and_effectiveness_locators_are_optional():
    match = locators(object_type("control"))
    assert match["mappings"]["required"] is False
    assert match["mappings"]["after_heading"] == "Mappings"
    assert match["effectiveness"]["required"] is False
    assert match["effectiveness"]["from"] == "section_body"
    assert match["effectiveness"]["after_heading"] == "Effectiveness"


@pytest.mark.trace("TC-193", "FR-014-AC-6")
def test_manifest_mappings_names_record_sections():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert "record-sections" in manifest["semantic"]["mappings"]


@pytest.mark.trace("TC-194", "FR-015-AC-1")
def test_a_third_mapping_key_fails_for_each_of_title_text_note(mapping):
    for key in ("title", "text", "note"):
        assert not mapping.is_valid({"set": SET, "clause": "EX-1", key: "x"}), key


@pytest.mark.trace("TC-195", "FR-015-AC-2")
def test_a_third_mapping_column_is_a_column_unknown_refusal(quire_engine):
    text = control_skeleton().replace(
        "| Set | Clause |\n|---|---|\n| example.invalid/std@1 | EX-1 |\n"
        "| example.invalid/std@1 | EX-2 |",
        "| Set | Clause | Title |\n|---|---|---|\n| example.invalid/std@1 | EX-1 | t |",
    )
    result = validate(quire_engine, "control", text)
    assert not result["is_valid"]
    line = text.splitlines().index("| Set | Clause | Title |") + 1
    hit = [
        e
        for e in result["errors"]
        if "semantic.invalid-model-cell" in e["message"] and e["line"] == line
    ]
    assert hit and "header `Title` matches no property" in hit[0]["message"], result[
        "errors"
    ]


@pytest.mark.trace("TC-196", "FR-015-AC-3")
def test_control_mapping_schema_lists_exactly_set_and_clause():
    assert set(schema("ControlMapping")["properties"]) == {"set", "clause"}


@pytest.mark.trace("TC-197", "FR-016-AC-1")
def test_scope_exclusion_schema_is_sealed_and_exported():
    doc = schema("ScopeExclusion")
    assert set(doc["required"]) == {"set", "clause", "responsible", "rationale"}
    assert set(doc["properties"]) == set(doc["required"])
    assert doc["unevaluatedProperties"] == {"not": {}}
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert "scope_exclusion" in manifest["semantic"]["exports"]


@pytest.mark.trace("TC-198", "FR-016-AC-2")
def test_exclusion_without_responsible_or_rationale_fails(exclusion, quire_engine):
    assert exclusion.is_valid(excl())
    assert not exclusion.is_valid(
        {k: v for k, v in excl().items() if k != "responsible"}
    )
    assert not exclusion.is_valid(excl(responsible="not an id"))
    assert not exclusion.is_valid(excl(rationale=""))
    text = exclusion_skeleton().replace("## Responsible\n\n`COMP-001`\n\n", "")
    result = validate(quire_engine, "scope_exclusion", text)
    assert any(
        "semantic.record-invalid" in m and "responsible" in m for m in messages(result)
    ), result["errors"]


@pytest.mark.trace("TC-199", "FR-016-AC-3")
def test_exclusion_admits_no_decision_status_or_approval(exclusion):
    for key in ("decision", "status", "approved_by"):
        assert not exclusion.is_valid(excl(**{key: "x"})), key


@pytest.mark.trace("TC-200", "FR-016-AC-4")
def test_exclusion_skeleton_validates_and_each_section_is_required(quire_engine):
    text = exclusion_skeleton()
    result = validate(quire_engine, "scope_exclusion", text)
    assert result["is_valid"], result["errors"]
    assert not [m for m in messages(result) if "semantic.record-invalid" in m]
    for token in ("TODO", "TBD", "{{", "placeholder"):
        assert token.lower() not in text.lower()
    for heading in ("Set", "Clause", "Responsible", "Rationale"):
        cut = re.sub(rf"^## {heading}\n\n`[^`]*`\n\n?", "", text, flags=re.M)
        assert f"## {heading}\n" not in cut.split("-->", 1)[1]
        broken = validate(quire_engine, "scope_exclusion", cut, bundle_package=BUNDLE)
        assert any(
            "semantic.record-invalid" in m and heading.lower() in m.lower()
            for m in messages(broken)
        ), (heading, broken["errors"])


@pytest.mark.trace("TC-201", "FR-016-AC-7")
def test_responsible_is_a_bare_bundle_id_not_a_cross_repository_identity(
    quire_engine,
):
    ok = validate(
        quire_engine, "scope_exclusion", exclusion_skeleton(), bundle_package=BUNDLE
    )
    assert ok["is_valid"], ok["errors"]
    foreign = exclusion_skeleton().replace(
        "`COMP-001`", "`ix://agent-ix/example-platform/COMP-001`"
    )
    bad = validate(quire_engine, "scope_exclusion", foreign, bundle_package=BUNDLE)
    assert not bad["is_valid"]
    assert any("not a bundle artifact id" in m for m in messages(bad)), bad["errors"]


@pytest.mark.trace("TC-202", "FR-016-AC-5")
def test_the_empty_exclusion_record_fails(exclusion):
    assert not exclusion.is_valid({})


@pytest.mark.trace("TC-203", "FR-016-AC-6")
def test_exclusion_manifest_entry_requires_four_section_body_locators():
    match = locators(object_type("scope_exclusion"))
    for key, heading in (
        ("set", "Set"),
        ("clause", "Clause"),
        ("responsible", "Responsible"),
        ("rationale", "Rationale"),
    ):
        assert match[key] == {
            "from": "section_body",
            "after_heading": heading,
            "required": True,
        }
