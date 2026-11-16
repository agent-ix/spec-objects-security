"""Regulated-data categories on `data_classification`.

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
from conftest import (
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


def _decl(**extra) -> dict:
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


def _extract(
    quire_engine,
    semantic_block,
    semantic_module,
    name: str,
    text: str | None = None,
    *,
    kind: str = "data_classification",
    bundle: dict | None = None,
) -> dict:
    """Extract any record with the manifest's body extraction and mappings.

    Frontmatter-owned projection and the section diagnostics only run when the
    archetype's `bodyExtraction` and the module `mappings` are supplied. The
    default keeps the regulated-category callers concise; other record kinds
    pass their type and optional bundle index explicitly.
    """
    text = text if text is not None else (FIXTURES / name).read_text()
    docs = {}
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        doc = json.loads(path.read_text())
        docs[doc["$id"]] = doc
    schema_name = object_type(kind)["data_schema"]["schema"].split("/")[-1]
    schema_name = schema_name.removesuffix(".json")
    return quire_engine.extract_semantic(
        {
            "markdown": text,
            "module": {**semantic_module, "mappings": semantic_block["mappings"]},
            "path": name,
            "sourceIdentity": (
                f"ix://agent-ix/spec-objects-security/{frontmatter(text)['id']}"
            ),
            "bundle": bundle
            or {
                "package": "agent-ix/spec-objects-security",
                "objects": [],
                "enumerations": [],
                "imports": {},
            },
            "objectType": kind,
            "dataSchema": _schema(schema_name),
            "schemaDocuments": docs,
            "bodyExtraction": object_type(kind)["body_extraction"],
        }
    )


def _record(out: dict) -> dict:
    return out.get("record") or {}


def _owned_diagnostics(out: dict) -> list:
    return [
        d
        for d in out["diagnostics"]
        if d["code"] == "semantic.feature-not-extractable"
        and d.get("reason") == "frontmatter-owned"
    ]


@pytest.mark.trace("TC-206", "FR-023-AC-5")
def test_the_vocabulary_is_exactly_health_personal_financial():
    schema = _schema("RegulatedDataCategory")
    assert schema["enum"] == MEMBERS
    assert "unknown" not in schema["enum"]


@pytest.mark.trace("TC-206", "FR-023-AC-5")
def test_frontmatter_category_enum_is_self_contained_for_quires_validator():
    frontmatter_schema = _schema("DataClassificationFrontmatter")
    categories = frontmatter_schema["properties"]["regulated_categories"]
    assert categories["items"]["enum"] == MEMBERS
    assert "$ref" not in categories["items"]


@pytest.mark.trace("TC-207", "FR-023-AC-1", "NFR-004-AC-1", "NFR-004-M-1")
def test_the_property_is_an_optional_non_empty_unique_list_without_default():
    schema = _schema("DataClassification")
    prop = schema["properties"]["regulatedCategories"]
    assert prop["type"] == "array"
    assert prop["items"]["$ref"].endswith("/RegulatedDataCategory.json")
    assert prop["minItems"] == 1
    assert prop["uniqueItems"] is True
    assert "default" not in prop
    assert "default" not in schema["properties"]["level"]
    assert "regulatedCategories" not in schema.get("required", [])


@pytest.mark.trace("TC-208", "FR-023-AC-6")
@pytest.mark.parametrize("value", [["health", "personal"], ["financial"], ["health"]])
def test_valid_lists_validate_and_neither_axis_implies_the_other(
    schema_registry, value
):
    assert not _errors(schema_registry, _decl(regulatedCategories=value))
    assert not _errors(
        schema_registry, _decl(regulatedCategories=value, level="restricted")
    )


@pytest.mark.trace("TC-209", "FR-023-AC-2", "FR-023-AC-3")
@pytest.mark.parametrize(
    "value",
    [["medical"], [], ["health", "health"], "health", ["unknown"]],
    ids=["unknown-member", "empty", "duplicate", "scalar", "unknown-token"],
)
def test_invalid_lists_are_refused(schema_registry, value):
    assert _errors(schema_registry, _decl(regulatedCategories=value))


@pytest.mark.trace("TC-210", "FR-023-AC-4")
def test_an_absent_field_validates_with_no_default(schema_registry):
    assert not _errors(schema_registry, _decl())


@pytest.mark.trace("TC-211", "FR-023-AC-7", "NFR-004-AC-1")
def test_each_axis_has_one_source_locator_and_no_assert():
    declared = locators(object_type("data_classification"))
    assert declared["regulatedCategories"] == {
        "from": "frontmatter_field",
        "path": ["regulated_categories"],
        "required": False,
    }
    # `level` is authored only as the `## Properties` table row.
    assert declared["properties"] == {
        "from": "section_body",
        "after_heading": "Properties",
        "required": False,
    }
    assert "level" not in declared
    for key in ("regulatedCategories", "level"):
        assert "assert" not in declared.get(key, {})
    for key, locator in declared.items():
        if key != "regulatedCategories":
            assert "regulated_categories" not in json.dumps(locator), key
        assert "default" not in locator, key


@pytest.mark.trace("TC-212", "FR-023-AC-8")
def test_the_skeleton_shows_the_field_and_validates(quire_engine):
    text = (PACKAGE_ROOT / "skeletons" / "data_classification.md").read_text()
    assert frontmatter(text)["regulated_categories"] == ["health", "personal"]
    result = quire_engine.validate_document(
        "data_classification", str(PACKAGE_ROOT), text
    )
    assert result["is_valid"], result["errors"]


@pytest.mark.trace(
    "TC-213", "FR-023-AC-1", "FR-023-AC-6", "NFR-004-AC-3", "NFR-004-M-2"
)
@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("valid-health-personal.md", ["health", "personal"]),
        ("valid-financial-only.md", ["financial"]),
        ("valid-health-without-personal.md", ["health"]),
        ("valid-level-and-health.md", ["health"]),
    ],
)
def test_valid_fixtures_validate_and_extract_the_list_in_order(
    quire_engine, semantic_block, semantic_module, name, expected
):
    assert _validate(quire_engine, name)["is_valid"]
    out = _extract(quire_engine, semantic_block, semantic_module, name)
    assert _record(out)["regulatedCategories"] == expected
    assert "level" not in _record(out)
    assert "level" in [f["name"] for f in out["fields"]]
    assert not [d for d in out["diagnostics"] if d["severity"] == "error"]


@pytest.mark.trace(
    "TC-214", "FR-023-AC-4", "NFR-004-AC-2", "NFR-004-AC-3", "NFR-004-M-2"
)
@pytest.mark.parametrize("name", ["absent.md", "absent-health-named-fields.md"])
def test_an_absent_field_extracts_no_key_and_no_default(
    quire_engine, semantic_block, semantic_module, name
):
    assert _validate(quire_engine, name)["is_valid"]
    out = _extract(quire_engine, semantic_block, semantic_module, name)
    assert "regulatedCategories" not in _record(out)
    assert not _owned_diagnostics(out)


@pytest.mark.trace("TC-214", "NFR-004-AC-3")
def test_a_classification_without_level_extracts_no_level_key(
    quire_engine, semantic_block, semantic_module
):
    text = (
        (FIXTURES / "absent.md")
        .read_text()
        .replace("| level | String | 1..1 | minLength: 1 |\n", "")
    )
    assert "| level |" not in text
    out = _extract(quire_engine, semantic_block, semantic_module, "no-level.md", text)
    assert "level" not in _record(out)
    assert "level" not in [f["name"] for f in out["fields"]]


@pytest.mark.trace("TC-215", "FR-023-AC-2", "FR-023-AC-3")
@pytest.mark.parametrize(
    ("name", "needles"),
    [
        ("unknown-member.md", ("regulatedCategories[0]", '"medical"')),
        ("empty-list.md", ("regulatedCategories", "less than 1 item")),
        ("duplicate-member.md", ("regulatedCategories", "non-unique")),
        ("scalar.md", ("regulatedCategories", 'not of type "array"')),
    ],
)
def test_invalid_fixtures_fail_with_a_message_that_names_the_cause(
    quire_engine, name, needles
):
    result = _validate(quire_engine, name)
    assert not result["is_valid"], name
    errors = [e for e in result["errors"] if "semantic.record-invalid" in e["message"]]
    assert errors, result["errors"]
    for needle in needles:
        assert needle in errors[0]["message"], (needle, errors[0]["message"])
    assert errors[0]["line"] == 6


@pytest.mark.trace("TC-216", "FR-023-AC-9")
def test_a_section_without_frontmatter_is_an_error_and_yields_no_key(
    quire_engine, semantic_block, semantic_module
):
    assert not _validate(quire_engine, "section-only.md")["is_valid"]
    out = _extract(quire_engine, semantic_block, semantic_module, "section-only.md")
    owned = _owned_diagnostics(out)
    assert [d["severity"] for d in owned] == ["error"], out["diagnostics"]
    assert "regulatedCategories" not in _record(out)


@pytest.mark.trace("TC-217", "FR-023-AC-10")
def test_a_section_beside_frontmatter_warns_and_keeps_only_the_frontmatter(
    quire_engine, semantic_block, semantic_module
):
    name = "section-and-frontmatter.md"
    assert _validate(quire_engine, name)["is_valid"]
    out = _extract(quire_engine, semantic_block, semantic_module, name)
    owned = _owned_diagnostics(out)
    assert [d["severity"] for d in owned] == ["warning"], out["diagnostics"]
    assert _record(out)["regulatedCategories"] == ["health"]
