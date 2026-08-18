"""Auto-generated test: manifest loads + object_types are well-formed."""

from __future__ import annotations

import pathlib

import pytest
import yaml
from jsonschema import Draft202012Validator
from spec_artifacts_iso import module_manifest_schema

PKG_ROOT = pathlib.Path(__file__).resolve().parent.parent / "spec_objects_security"
MANIFEST_PATH = PKG_ROOT / "manifest.yaml"


def test_manifest_loads() -> None:
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert manifest["manifest_version"] == "1.0.0"
    assert manifest["name"] == "spec-objects-security"
    assert manifest["version"]
    assert isinstance(manifest.get("object_types", []), list)


def _object_types():
    return yaml.safe_load(MANIFEST_PATH.read_text()).get("object_types", [])


@pytest.mark.parametrize("ot", _object_types(), ids=lambda ot: ot["name"])
def test_object_type_has_name_and_data_schema(ot: dict) -> None:
    assert isinstance(ot["name"], str) and len(ot["name"]) > 0
    assert "data_schema" in ot
    assert isinstance(ot["data_schema"], dict)


def test_no_duplicate_object_type_names() -> None:
    names = [ot["name"] for ot in _object_types()]
    assert len(names) == len(set(names)), f"duplicate names: {names}"


def test_manifest_validates_against_fr035_schema() -> None:
    """The manifest validates against the FR-035 module-manifest schema.

    Until this test, **nothing validated this module.** 23 object types, 23
    skeletons, a 15-term lexicon and a nav block — 464 lines of module data —
    were checked by `manifest_version == "1.0.0"`, the module name, and a
    per-type `name`/`data_schema` presence check. A new key shipped
    unvalidated, and two lexicon definitions were silently truncated by
    unquoted commas inside YAML flow mappings for who knows how long.

    **No skip and no escape hatch.** Both were deleted upstream for cause: a
    `pytest.skip` when the schema could not be found reported this gate green
    while it ran nothing (spec-artifacts-iso#15). The schema is package data on
    `spec-artifacts-iso`, imported rather than copied, so there is one source
    and no branch on which this can quietly not run.
    """
    schema = module_manifest_schema()
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    errors = list(Draft202012Validator(schema).iter_errors(manifest))
    assert not errors, [
        f"{'.'.join(str(p) for p in e.absolute_path)}: {e.message}" for e in errors
    ]


def test_lexicon_entries_are_whole() -> None:
    """Every lexicon entry is exactly `{definition: <non-empty string>}`.

    The regression this pins: `secret` and `audit` were written as YAML flow
    mappings whose definitions contained an unquoted comma —

        secret: {definition: a confidential value (key, password) kept out of code}

    — so YAML read the comma as an entry separator. `secret.definition` became
    "a confidential value (key" and a junk key `password) kept out of code`
    appeared beside it with a null value. The file looked right to a reader and
    was wrong to every consumer.

    Asserted structurally rather than by re-checking those two terms, because
    the defect is a property of the flow-mapping form and the next one will be
    on a different term (agent-ix/spec-objects-security#6).
    """
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    lexicon = manifest.get("lexicon") or {}
    assert lexicon, "the module declares a lexicon"

    malformed = {
        term: entry
        for term, entry in lexicon.items()
        if not isinstance(entry, dict)
        or set(entry) != {"definition"}
        or not str(entry.get("definition", "")).strip()
    }
    assert not malformed, (
        "lexicon entries must be exactly {definition: <text>} — an entry with "
        "extra keys is an unquoted comma inside a flow mapping, which silently "
        f"truncates the definition: {malformed}"
    )
