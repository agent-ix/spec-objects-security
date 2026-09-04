"""The `semantic` block, the reference-form `data_schema`, and the frozen
locator and edge vocabulary."""

from __future__ import annotations

import pathlib
import shutil
import tempfile

import pytest
import yaml

from tests.conftest import (
    BASELINE_DIR,
    MODEL_OF,
    OBJECT_TYPES,
    PACKAGE_ROOT,
    REPO_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    frontmatter,
    load_manifest,
    locators,
    object_type,
    object_types,
    sha256_of,
)

ADMITTED_KEYS = {
    "contract_version",
    "semantic_core",
    "package",
    "exports",
    "imports",
    "targets",
    "mappings",
    "compatibility_posture",
    "legacy_forms",
}

BASELINE_MANIFEST = yaml.safe_load((BASELINE_DIR / "manifest.yaml").read_text())


def baseline_object_type(name: str) -> dict:
    return next(ot for ot in BASELINE_MANIFEST["object_types"] if ot["name"] == name)


@pytest.mark.trace("TC-040", "FR-003-AC-1", "FR-003-CON-1")
def test_the_semantic_block_is_exactly_the_nine_admitted_keys(semantic_block):
    assert set(semantic_block) == ADMITTED_KEYS
    assert len(ADMITTED_KEYS) == 9
    assert semantic_block["contract_version"] == "1.0.0"
    assert semantic_block["semantic_core"] == "0.1.0"
    assert semantic_block["package"] == "agent-ix/spec-objects-security"
    assert semantic_block["imports"] == {}
    assert semantic_block["targets"] == ["json-schema", "markdown"]
    assert semantic_block["mappings"] == ["typed-table", "sysml-fence", "ocl-clause"]
    assert semantic_block["compatibility_posture"] == "additive"
    assert semantic_block["legacy_forms"] == "warning"
    assert semantic_block["exports"] == list(OBJECT_TYPES)
    assert len(semantic_block["exports"]) == 23


@pytest.mark.trace("TC-041", "FR-003-AC-2")
def test_every_data_schema_is_the_reference_form_hashing_to_its_digest():
    for ot in object_types():
        schema = ot["data_schema"]
        assert set(schema) == {"schema", "digest"}, ot["name"]
        assert schema["schema"] == f"schemas/{MODEL_OF[ot['name']]}.json"
        path = PACKAGE_ROOT / schema["schema"]
        assert path.is_file(), ot["name"]
        assert sha256_of(path) == schema["digest"], ot["name"]
        assert "type" not in schema, f"{ot['name']} still carries an inline schema"


@pytest.mark.trace("TC-042", "FR-003-AC-3")
def test_every_baseline_locator_is_unchanged():
    for name in OBJECT_TYPES:
        before = locators(baseline_object_type(name))
        after = locators(object_type(name))
        for key, definition in before.items():
            assert key in after, f"{name}: locator {key} disappeared"
            assert after[key] == definition, f"{name}: locator {key} changed"


@pytest.mark.trace("TC-043", "FR-003-AC-3", "FR-003-CON-2")
def test_every_added_locator_is_optional():
    added = 0
    for name in OBJECT_TYPES:
        before = locators(baseline_object_type(name))
        after = locators(object_type(name))
        for key, definition in after.items():
            if key in before:
                continue
            added += 1
            assert definition["required"] is False, f"{name}: {key} is required"
    assert added == 25, added


@pytest.mark.trace("TC-047", "FR-003-AC-7", "FR-003-CON-3")
def test_the_edge_vocabulary_and_traceability_are_frozen():
    """The sibling `agent-ix/spec-objects-safety` declares its bidirectional
    hazard coverage against these fields; changing one here is a
    cross-repository contract change, not a module edit."""
    current = load_manifest()
    assert current["traceability"] == BASELINE_MANIFEST["traceability"]
    for name in OBJECT_TYPES:
        before = baseline_object_type(name)
        after = object_type(name)
        assert after.get("allowed_links") == before.get("allowed_links"), name
        assert after.get("roles") == before.get("roles"), name


@pytest.mark.trace("TC-044", "FR-003-AC-4")
def test_the_registry_lists_every_archetype_and_no_skeleton_fails_to_load(
    quire_engine,
):
    # `load_from` takes *search paths* that contain modules, not a module
    # directory: handed the module itself it finds nothing and lists nothing.
    registry = quire_engine.Registry.load_from([str(REPO_ROOT)])
    listed = set(registry.archetype_names())
    for name in OBJECT_TYPES:
        assert name in listed, name
    for path in sorted(SKELETONS_DIR.glob("*.md")):
        text = path.read_text()
        result = quire_engine.validate_document(
            frontmatter(text)["type"], str(PACKAGE_ROOT), text
        )
        failures = [
            e
            for e in result["errors"]
            if "semantic." in e["message"] and "load" in e["message"]
        ]
        assert not failures, (path.name, failures)


@pytest.mark.trace("TC-045", "FR-003-AC-6")
def test_an_unknown_key_and_an_altered_digest_are_refused(quire_engine):
    """The refusal is verified. The *naming* half of FR-003-AC-6 — a diagnostic
    that names the offending key or path — is an expected failure while
    agent-ix/quire-rs#221 and agent-ix/quire-rs#394 are open, and is asserted
    as `xfail(strict=True)` below so the day the engine names them, the row
    turns red and is noticed."""
    with tempfile.TemporaryDirectory() as tmp:
        module = _copy_module(tmp, "unknown-key")
        data = yaml.safe_load((module / "manifest.yaml").read_text())
        data["semantic"]["foo"] = "bar"
        (module / "manifest.yaml").write_text(yaml.safe_dump(data, sort_keys=False))
        registry = quire_engine.Registry.load_from([str(module.parent)])
        assert not set(registry.archetype_names()) & set(OBJECT_TYPES)
    with tempfile.TemporaryDirectory() as tmp:
        module = _copy_module(tmp, "bad-digest")
        data = yaml.safe_load((module / "manifest.yaml").read_text())
        for ot in data["object_types"]:
            if ot["name"] == "threat":
                ot["data_schema"]["digest"] = "sha256:" + "0" * 64
        (module / "manifest.yaml").write_text(yaml.safe_dump(data, sort_keys=False))
        registry = quire_engine.Registry.load_from([str(module.parent)])
        assert "threat" not in set(registry.archetype_names())


@pytest.mark.xfail(strict=True, reason="agent-ix/quire-rs#221, agent-ix/quire-rs#394")
@pytest.mark.trace("TC-045", "FR-003-AC-6")
def test_the_refusal_names_the_offending_key_or_path(quire_engine, capsys):
    with tempfile.TemporaryDirectory() as tmp:
        module = _copy_module(tmp, "unknown-key")
        data = yaml.safe_load((module / "manifest.yaml").read_text())
        data["semantic"]["foo"] = "bar"
        (module / "manifest.yaml").write_text(yaml.safe_dump(data, sort_keys=False))
        quire_engine.Registry.load_from([str(module.parent)])
        assert "foo" in capsys.readouterr().err


def _copy_module(tmp, name):
    module = pathlib.Path(tmp) / name
    shutil.copytree(PACKAGE_ROOT, module)
    return module


@pytest.mark.trace("TC-111", "StR-001-VC-3")
def test_two_records_of_different_types_are_distinguishable_by_schema_alone(
    schema_registry,
):
    """StR-001-VC-3 as an executable demonstration: a fixture reader given only
    the shipped schemas can tell a secret from a risk."""
    from tests.conftest import field

    secret = {"fields": [field("secret_id", "UUID", identity=True)]}
    risk = {
        "fields": [
            field("risk_id", "UUID", identity=True),
            field("likelihood"),
            field("impact"),
        ]
    }
    assert schema_registry("Secret").is_valid(secret)
    assert not schema_registry("Risk").is_valid(secret)
    assert schema_registry("Risk").is_valid(risk)
    for name in OBJECT_TYPES:
        assert (SCHEMAS_DIR / f"{MODEL_OF[name]}.json").is_file(), name
