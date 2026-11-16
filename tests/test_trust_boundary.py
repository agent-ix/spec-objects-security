"""Required frontmatter value for the TrustBoundary record (FR-024)."""

from __future__ import annotations

import json

import pytest

from tests.conftest import (
    PACKAGE_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    frontmatter,
    object_type,
)

SKELETON = SKELETONS_DIR / "trust_boundary.md"


def _extract(quire_engine, semantic_block, semantic_module, bundle_index, text: str):
    docs = {}
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        schema = json.loads(path.read_text())
        docs[schema["$id"]] = schema
    return quire_engine.extract_semantic(
        {
            "markdown": text,
            "module": {**semantic_module, "mappings": semantic_block["mappings"]},
            "path": "trust_boundary.md",
            "sourceIdentity": (
                f"ix://agent-ix/spec-objects-security/{frontmatter(text)['id']}"
            ),
            "bundle": bundle_index,
            "objectType": "trust_boundary",
            "dataSchema": json.loads((SCHEMAS_DIR / "TrustBoundary.json").read_text()),
            "schemaDocuments": docs,
            "bodyExtraction": object_type("trust_boundary")["body_extraction"],
        }
    )


@pytest.mark.trace("TC-221", "FR-024-AC-1", "FR-024-AC-2", "FR-024-AC-3")
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


@pytest.mark.trace("TC-222", "FR-024-AC-4", "FR-024-AC-7")
def test_frontmatter_trust_level_is_extracted_and_not_derived_from_properties(
    quire_engine, semantic_block, semantic_module, bundle_index
):
    text = SKELETON.read_text()
    extracted = _extract(quire_engine, semantic_block, semantic_module, bundle_index, text)
    assert extracted["record"]["trust_level"] == "untrusted"

    missing = text.replace("trust_level: untrusted\n", "")
    absent = _extract(quire_engine, semantic_block, semantic_module, bundle_index, missing)
    assert "trust_level" not in absent["record"]
    result = quire_engine.validate_document("trust_boundary", str(PACKAGE_ROOT), missing)
    assert not result["is_valid"]
    assert any("trust_level" in str(error) for error in result["errors"])


@pytest.mark.trace("TC-223", "FR-024-AC-6")
def test_trust_boundary_skeleton_states_and_validates_frontmatter_trust_level(
    quire_engine,
):
    text = SKELETON.read_text()
    assert frontmatter(text)["trust_level"] == "untrusted"
    result = quire_engine.validate_document("trust_boundary", str(PACKAGE_ROOT), text)
    assert result["is_valid"], result["errors"]
