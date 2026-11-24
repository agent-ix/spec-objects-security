"""Required frontmatter value for the TrustBoundary record (FR-024)."""

from __future__ import annotations

import json

import pytest

from tests.conftest import (
    PACKAGE_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    frontmatter,
    load_manifest,
)
from tests.test_regulated_categories import _extract

SKELETON = SKELETONS_DIR / "trust_boundary.md"


@pytest.mark.trace("FR-024-AC-8")
def test_trust_boundary_frontmatter_schema_declares_the_engine_vocabulary():
    manifest = load_manifest()
    trust_boundary = next(
        item for item in manifest["object_types"] if item["name"] == "trust_boundary"
    )
    assert trust_boundary["frontmatter_schema_ref"] == (
        "schemas/TrustBoundaryFrontmatter.json"
    )

    schema = json.loads((SCHEMAS_DIR / "TrustBoundaryFrontmatter.json").read_text())
    assert schema["type"] == "object"
    assert "additionalProperties" not in schema
    assert schema["required"] == ["trust_level"]
    assert schema["properties"]["trust_level"]["enum"] == [
        "untrusted",
        "semi_trusted",
        "trusted",
        "unknown",
    ]


@pytest.mark.trace("FR-024-AC-1", "FR-024-AC-2", "FR-024-AC-3")
def test_trust_boundary_requires_a_valid_frontmatter_trust_level(quire_engine):
    text = SKELETON.read_text()
    valid = quire_engine.validate_document("trust_boundary", str(PACKAGE_ROOT), text)
    assert valid["is_valid"], valid["errors"]

    missing = text.replace("trust_level: untrusted\n", "")
    missing_result = quire_engine.validate_document(
        "trust_boundary", str(PACKAGE_ROOT), missing
    )
    assert not missing_result["is_valid"]
    assert any("trust_level" in str(error) for error in missing_result["errors"])

    invalid = text.replace("trust_level: untrusted", "trust_level: partly")
    invalid_result = quire_engine.validate_document(
        "trust_boundary", str(PACKAGE_ROOT), invalid
    )
    assert not invalid_result["is_valid"]
    assert any("partly" in str(error) for error in invalid_result["errors"])


@pytest.mark.trace("FR-024-AC-4", "FR-024-AC-7")
def test_frontmatter_trust_level_is_extracted_and_not_derived_from_properties(
    quire_engine, semantic_block, semantic_module, bundle_index
):
    text = SKELETON.read_text()
    extracted = _extract(
        quire_engine,
        semantic_block,
        semantic_module,
        "trust_boundary.md",
        text,
        kind="trust_boundary",
        bundle=bundle_index,
    )
    assert extracted["record"]["trust_level"] == "untrusted"

    missing = text.replace("trust_level: untrusted\n", "")
    absent = _extract(
        quire_engine,
        semantic_block,
        semantic_module,
        "trust_boundary.md",
        missing,
        kind="trust_boundary",
        bundle=bundle_index,
    )
    assert "trust_level" not in (absent.get("record") or {})
    result = quire_engine.validate_document(
        "trust_boundary", str(PACKAGE_ROOT), missing
    )
    assert not result["is_valid"]
    assert any("trust_level" in str(error) for error in result["errors"])


@pytest.mark.trace("FR-024-AC-6")
def test_trust_boundary_skeleton_states_and_validates_frontmatter_trust_level(
    quire_engine,
):
    text = SKELETON.read_text()
    assert frontmatter(text)["trust_level"] == "untrusted"
    result = quire_engine.validate_document("trust_boundary", str(PACKAGE_ROOT), text)
    assert result["is_valid"], result["errors"]
