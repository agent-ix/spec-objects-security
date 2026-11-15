"""Regulated-data categories on `data_classification` (FR-023, NFR-004).

Two layers are tested apart. The schema tests need no engine: they validate
hand-built records against the emitted `DataClassification.json`. The engine
tests run the real Quire over `tests/fixtures/regulated-categories/`; they
need an engine that projects the frontmatter `regulated_categories` to the
record key `regulatedCategories` and owns that key against section forms.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from tests.conftest import (
    PACKAGE_ROOT,
    SCHEMAS_DIR,
    field,
    frontmatter,
    locators,
    object_type,
)

FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures" / "regulated-categories"
MEMBERS = ["health", "personal", "financial"]


def _schema(name: str) -> dict:
    return json.loads((SCHEMAS_DIR / f"{name}.json").read_text())


def _record(**extra) -> dict:
    return {
        "fields": [
            field("classification_id", "UUID", identity=True),
            field("level"),
        ],
        **extra,
    }


def _errors(validator_for, record: dict) -> list:
    return list(validator_for("DataClassification").iter_errors(record))


def _validate(quire_engine, name: str) -> dict:
    return quire_engine.validate_document(
        "data_classification", str(PACKAGE_ROOT), (FIXTURES / name).read_text()
    )


def _extract(quire_engine, semantic_module, name: str) -> dict:
    text = (FIXTURES / name).read_text()
    docs = {}
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        doc = json.loads(path.read_text())
        docs[doc["$id"]] = doc
    return quire_engine.extract_semantic(
        {
            "markdown": text,
            "module": semantic_module,
            "path": name,
            "sourceIdentity": (
                f"ix://agent-ix/spec-objects-security/{frontmatter(text)['id']}"
            ),
            "bundle": {
                "package": "agent-ix/spec-objects-security",
                "objects": [],
                "enumerations": [],
                "imports": {},
            },
            "objectType": "data_classification",
            "dataSchema": _schema("DataClassification"),
            "schemaDocuments": docs,
        }
    )


@pytest.mark.trace("TC-RC-01", "FR-023-AC-5")
def test_the_vocabulary_is_exactly_health_personal_financial():
    schema = _schema("RegulatedDataCategory")
    assert schema["enum"] == MEMBERS
    assert "unknown" not in schema["enum"]


@pytest.mark.trace("TC-RC-02", "FR-023-AC-1", "NFR-004-AC-1")
def test_the_property_is_an_optional_non_empty_unique_list_without_default():
    schema = _schema("DataClassification")
    prop = schema["properties"]["regulatedCategories"]
    assert prop["type"] == "array"
    assert prop["items"]["$ref"].endswith("/RegulatedDataCategory.json")
    assert prop["minItems"] == 1
    assert prop["uniqueItems"] is True
    assert "default" not in prop
    assert "regulatedCategories" not in schema.get("required", [])


@pytest.mark.trace("TC-RC-03", "FR-023-AC-6")
@pytest.mark.parametrize("value", [["health", "personal"], ["financial"], ["health"]])
def test_valid_lists_validate_and_neither_axis_implies_the_other(
    schema_registry, value
):
    assert not _errors(schema_registry, _record(regulatedCategories=value))
    assert not _errors(
        schema_registry, _record(regulatedCategories=value, level="restricted")
    )


@pytest.mark.trace("TC-RC-04", "FR-023-AC-2", "FR-023-AC-3")
@pytest.mark.parametrize(
    "value",
    [["medical"], [], ["health", "health"], "health", ["unknown"]],
    ids=["unknown-member", "empty", "duplicate", "scalar", "unknown-token"],
)
def test_invalid_lists_are_refused(schema_registry, value):
    assert _errors(schema_registry, _record(regulatedCategories=value))


@pytest.mark.trace("TC-RC-05", "FR-023-AC-4")
def test_an_absent_field_validates_with_no_default(schema_registry):
    assert not _errors(schema_registry, _record())


@pytest.mark.trace("TC-RC-06", "FR-023-AC-7", "NFR-004-AC-1")
def test_the_locator_is_an_optional_frontmatter_list_and_the_only_source():
    declared = locators(object_type("data_classification"))
    assert declared["regulatedCategories"] == {
        "from": "frontmatter_field",
        "path": ["regulated_categories"],
        "required": False,
    }
    assert "assert" not in declared["regulatedCategories"]
    others = {k: v for k, v in declared.items() if k != "regulatedCategories"}
    assert all("regulated_categories" not in json.dumps(v) for v in others.values())


@pytest.mark.trace("TC-RC-07", "FR-023-AC-8")
def test_the_skeleton_shows_the_field_and_validates(quire_engine):
    text = (PACKAGE_ROOT / "skeletons" / "data_classification.md").read_text()
    assert frontmatter(text)["regulated_categories"] == ["health", "personal"]
    result = quire_engine.validate_document(
        "data_classification", str(PACKAGE_ROOT), text
    )
    assert result["is_valid"], result["errors"]


@pytest.mark.trace("TC-RC-08", "FR-023-AC-1", "FR-023-AC-6")
@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("valid-health-personal.md", ["health", "personal"]),
        ("valid-financial-only.md", ["financial"]),
        ("valid-health-without-personal.md", ["health"]),
    ],
)
def test_valid_fixtures_validate_and_extract_the_list_in_order(
    quire_engine, semantic_module, name, expected
):
    assert _validate(quire_engine, name)["is_valid"]
    record = _extract(quire_engine, semantic_module, name)["record"]
    assert record["regulatedCategories"] == expected


@pytest.mark.trace("TC-RC-09", "FR-023-AC-4", "NFR-004-AC-2", "NFR-004-AC-3")
@pytest.mark.parametrize("name", ["absent.md", "absent-health-named-fields.md"])
def test_an_absent_field_extracts_no_key_and_no_default(
    quire_engine, semantic_module, name
):
    assert _validate(quire_engine, name)["is_valid"]
    record = _extract(quire_engine, semantic_module, name)["record"]
    assert "regulatedCategories" not in record


@pytest.mark.trace("TC-RC-10", "FR-023-AC-2", "FR-023-AC-3")
@pytest.mark.parametrize(
    ("name", "needle"),
    [
        ("unknown-member.md", "medical"),
        ("empty-list.md", "regulated"),
        ("duplicate-member.md", "regulated"),
        ("scalar.md", "regulated"),
    ],
)
def test_invalid_fixtures_fail_naming_the_key(quire_engine, name, needle):
    result = _validate(quire_engine, name)
    assert not result["is_valid"], name
    messages = " ".join(e["message"] for e in result["errors"])
    assert "regulatedCategories" in messages or "regulated_categories" in messages
    assert needle in messages


@pytest.mark.trace("TC-RC-11", "FR-023-AC-9")
def test_a_section_without_frontmatter_is_an_error_and_yields_no_key(
    quire_engine, semantic_module
):
    result = _validate(quire_engine, "section-only.md")
    assert not result["is_valid"]
    assert any(
        "semantic.feature-not-extractable" in e["message"]
        and "frontmatter-owned" in e["message"]
        for e in result["errors"]
    ), result["errors"]
    record = _extract(quire_engine, semantic_module, "section-only.md")["record"]
    assert "regulatedCategories" not in (record or {})


@pytest.mark.trace("TC-RC-12", "FR-023-AC-10")
def test_a_section_beside_frontmatter_warns_and_keeps_only_the_frontmatter(
    quire_engine, semantic_module
):
    result = _validate(quire_engine, "section-and-frontmatter.md")
    assert result["is_valid"], result["errors"]
    assert any(
        "frontmatter-owned" in w["message"] for w in result.get("warnings", [])
    ), result
    record = _extract(quire_engine, semantic_module, "section-and-frontmatter.md")[
        "record"
    ]
    assert record["regulatedCategories"] == ["health"]
