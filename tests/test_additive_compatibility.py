"""The previous population still validates under the new manifest version.

The population is named: the twenty-three skeletons as they stood at manifest
version 0.1.0, frozen under `tests/fixtures/baseline-0.1.0/`. That freeze is
this requirement's evidence and is compared against the live manifest, so a
locator or edge-vocabulary change cannot pass unnoticed.
"""

from __future__ import annotations

import pytest
import yaml

from tests.conftest import (
    BASELINE_DIR,
    OBJECT_TYPES,
    PACKAGE_ROOT,
    frontmatter,
    load_manifest,
    locators,
    object_type,
)

BASELINE_MANIFEST = yaml.safe_load((BASELINE_DIR / "manifest.yaml").read_text())
BASELINE_SKELETONS = sorted((BASELINE_DIR / "skeletons").glob("*.md"))


def baseline_object_type(name: str) -> dict:
    return next(ot for ot in BASELINE_MANIFEST["object_types"] if ot["name"] == name)


def test_the_frozen_baseline_is_the_previous_module_version():
    """The baseline is a deliverable, not an incidental copy: without it every
    NFR-001 criterion compares the manifest against itself."""
    assert BASELINE_MANIFEST["version"] == "0.1.0"
    assert len(BASELINE_SKELETONS) == 23
    assert {ot["name"] for ot in BASELINE_MANIFEST["object_types"]} == set(OBJECT_TYPES)
    assert load_manifest()["version"] == "0.2.0"


@pytest.mark.trace("TC-100", "NFR-001-AC-1")
def test_zero_baseline_locators_changed():
    changed = []
    for name in OBJECT_TYPES:
        before = locators(baseline_object_type(name))
        after = locators(object_type(name))
        for key, definition in before.items():
            if after.get(key) != definition:
                changed.append((name, key))
    assert changed == [], changed


@pytest.mark.trace("TC-101", "NFR-001-AC-2")
def test_zero_traceability_or_edge_vocabulary_bytes_changed():
    current = load_manifest()
    assert current["traceability"] == BASELINE_MANIFEST["traceability"]
    assert current["lexicon"] == BASELINE_MANIFEST["lexicon"]
    for name in OBJECT_TYPES:
        before = baseline_object_type(name)
        after = object_type(name)
        assert after.get("allowed_links") == before.get("allowed_links"), name
        assert after.get("roles") == before.get("roles"), name


@pytest.mark.trace("TC-102", "NFR-001-AC-3")
def test_every_baseline_skeleton_validates_under_the_new_manifest(quire_engine):
    for path in BASELINE_SKELETONS:
        text = path.read_text()
        result = quire_engine.validate_document(
            frontmatter(text)["type"], str(PACKAGE_ROOT), text
        )
        assert result["is_valid"], (path.name, result["errors"])


@pytest.mark.trace("TC-103", "NFR-001-AC-4")
def test_no_baseline_skeleton_yields_a_record_invalid_finding(quire_engine):
    """It holds because no 0.1.0 skeleton declares frontmatter `object:`, so
    Quire runs headings-only validation and never assembles a typed record.
    That is asserted here rather than assumed."""
    for path in BASELINE_SKELETONS:
        text = path.read_text()
        assert "object:" not in frontmatter(text), path.name
        result = quire_engine.validate_document(
            frontmatter(text)["type"], str(PACKAGE_ROOT), text
        )
        assert not [
            e for e in result["errors"] if "semantic.record-invalid" in e["message"]
        ], (path.name, result["errors"])


@pytest.mark.xfail(strict=True, reason="agent-ix/quire-rs#391")
def test_a_legacy_form_declaring_object_is_not_an_error(quire_engine):
    """The engine defect NFR-001 carries rather than works around: once a
    legacy-form artifact declares `object:`, quire 0.46.0 assembles its record
    as `{}` and validates it unconditionally, so it fails
    `semantic.record-invalid` at error severity even under
    `legacy_forms: warning`. Strict xfail, so the day the engine changes this
    row turns red and is noticed."""
    path = BASELINE_DIR / "skeletons" / "asset.md"
    text = path.read_text().replace("type: asset\n", "type: asset\nobject: asset\n", 1)
    result = quire_engine.validate_document("asset", str(PACKAGE_ROOT), text)
    assert not [
        e for e in result["errors"] if "semantic.record-invalid" in e["message"]
    ], result["errors"]
