"""Auto-generated test: manifest loads + object_types are well-formed."""

from __future__ import annotations

import json
import pathlib

import pytest
import yaml
from jsonschema import Draft202012Validator
from spec_artifacts_iso import module_manifest_schema

PKG_ROOT = pathlib.Path(__file__).resolve().parent.parent / "spec_objects_security"
MANIFEST_PATH = PKG_ROOT / "manifest.yaml"
_PINNED_SCHEMA_PATH = (
    pathlib.Path(__file__).resolve().parent
    / "fixtures"
    / "module-manifest.cr-012.schema.json"
)


@pytest.mark.trace("TC-002", "FR-001-AC-1")
def test_manifest_loads() -> None:
    """TC-002: FR-001-AC-1."""
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert manifest["manifest_version"] == "1.0.0"
    assert manifest["name"] == "spec-objects-security"
    assert manifest["version"]
    assert isinstance(manifest.get("object_types", []), list)


def _object_types():
    return yaml.safe_load(MANIFEST_PATH.read_text()).get("object_types", [])


@pytest.mark.trace("TC-003", "FR-001-AC-1")
@pytest.mark.parametrize("ot", _object_types(), ids=lambda ot: ot["name"])
def test_object_type_has_name_and_data_schema(ot: dict) -> None:
    """TC-003: FR-001-AC-1."""
    assert isinstance(ot["name"], str) and len(ot["name"]) > 0
    assert "data_schema" in ot
    assert isinstance(ot["data_schema"], dict)
    assert set(ot["data_schema"]) == {"schema", "digest"}


@pytest.mark.trace("TC-004", "FR-001-AC-1")
def test_no_duplicate_object_type_names() -> None:
    """TC-004: FR-001-AC-1."""
    names = [ot["name"] for ot in _object_types()]
    assert len(names) == len(set(names)), f"duplicate names: {names}"


@pytest.mark.trace("TC-005", "FR-001-AC-1")
def test_manifest_validates_against_fr035_schema() -> None:
    """TC-005: The manifest validates against the FR-035 module-manifest schema.

    Until this test, **nothing validated this module.** 23 object types, 23
    skeletons, a 15-term lexicon and a nav block were checked by
    `manifest_version == "1.0.0"`, the module name, and a per-type
    `name`/`data_schema` presence check.

    **No skip and no escape hatch.** Both were deleted upstream for cause: a
    `pytest.skip` when the schema could not be found reported this gate green
    while it ran nothing (spec-artifacts-iso#15).

    The schema is normally imported from `spec-artifacts-iso` package data so
    there is one source. No released `spec-artifacts-iso` yet carries the
    CR-012 revision that admits the `semantic` block and the reference-form
    `data_schema` (`agent-ix/spec-artifacts-iso#36`), so the gate runs against
    a pinned copy of that revision instead. The pin is not a relaxation: the
    test below proves the pinned copy differs from the released one only at the
    CR-012 pointers, and every other rule still runs.
    """
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    errors = list(Draft202012Validator(_pinned_schema()).iter_errors(manifest))
    assert not errors, [
        f"{'.'.join(str(p) for p in e.absolute_path)}: {e.message}" for e in errors
    ]


# Every JSON pointer at which the pinned CR-012 schema is allowed to differ
# from the newest released one. Anything else is drift in the pin itself.
_ADMITTED_PIN_DELTA = {
    "#/description",
    "#/properties/semantic",
    "#/$defs/ObjectTypeEntry/properties/data_schema/type",
    "#/$defs/ObjectTypeEntry/properties/data_schema/oneOf",
    "#/$defs/ObjectTypeEntry/properties/data_schema/description",
    "#/$defs/ArtifactTypeEntry/properties/data_schema/type",
    "#/$defs/ArtifactTypeEntry/properties/data_schema/oneOf",
    "#/$defs/ArtifactTypeEntry/properties/data_schema/description",
    "#/$defs/TraceabilityModel/properties/source_exclude/description",
    "#/$defs/TraceabilityModel/properties/source_exclude/items/allOf",
}


def _pinned_schema() -> dict:
    return json.loads(_PINNED_SCHEMA_PATH.read_text())


def _differences(released, pinned, path="#"):
    if type(released) is not type(pinned):
        return [path]
    if isinstance(released, dict):
        out = []
        for key in sorted(set(released) | set(pinned)):
            if key not in released or key not in pinned:
                out.append(f"{path}/{key}")
            else:
                out += _differences(released[key], pinned[key], f"{path}/{key}")
        return out
    return [] if released == pinned else [path]


@pytest.mark.trace("TC-005", "FR-001-AC-1")
def test_the_pinned_schema_differs_from_the_release_only_where_admitted() -> None:
    """The pin is the gate, so the pin itself is gated.

    `agent-ix/spec-artifacts-iso#36` asks that no consumer weaken or skip its
    FR-035 gate while waiting for a release, and that a pinned revision copy
    prove it differs from the released schema only at the CR-012 pointers.
    This is that proof. When #36 ships, this test fails with an empty delta and
    the pin is deleted.
    """
    released = module_manifest_schema()
    delta = set(_differences(released, _pinned_schema()))
    assert delta, (
        "the released spec-artifacts-iso now equals the pin: "
        "agent-ix/spec-artifacts-iso#36 has shipped. Delete "
        f"{_PINNED_SCHEMA_PATH.name} and read the schema from the package."
    )
    assert delta <= _ADMITTED_PIN_DELTA, delta - _ADMITTED_PIN_DELTA


@pytest.mark.trace("TC-006", "FR-001-AC-1")
def test_lexicon_entries_are_whole() -> None:
    """TC-006: Every lexicon entry is exactly `{definition: <non-empty string>}`.

    The regression this pins: `secret` and `audit` were written as YAML flow
    mappings whose definitions contained an unquoted comma —

        secret: {definition: a confidential value (key, password) kept out of code}

    — so YAML read the comma as an entry separator. `secret.definition` became
    "a confidential value (key" and a junk key `password) kept out of code`
    appeared beside it with a null value. The file looked right to a reader and
    was wrong to every consumer.

    Asserted structurally rather than by re-checking those two terms, because
    the defect is a property of the flow-mapping form and the next one will be
    on a different term. This is the standing disposition of
    agent-ix/spec-objects-security#6: the two truncated definitions were
    restored by quoting the scalars, and this structural assertion is what
    stops the next flow mapping from doing it again.
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


@pytest.mark.trace("TC-007", "FR-001-AC-1")
def test_threat_and_risk_coverage_is_declared_not_coded() -> None:
    """TC-007: agent-ix/spec-objects-security#5: upward coverage is manifest data.

    Assumptions: quire-rs FR-058 (v0.31.0) reads
    ``traceability.required_relations``; the engine holds no archetype name,
    no verb and no direction.

    Criteria:
      * ``threat`` and ``risk`` each carry an obligation to be mitigated;
      * each has its OWN ``trace:<check>`` key so it is independently tunable
        (quire-rs FR-057) — a repository can promote uncontrolled threats to
        ``error`` while risk treatment is still being backfilled;
      * ``direction`` is ``incoming``: a control says what it mitigates, and a
        threat listing its own controls would duplicate the fact;
      * every ``from`` names an object type this module declares, and every
        verb is one the module already permits — the relation must not invent
        vocabulary (quire-rs CR-075 would report it as matching nothing).
    """
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    model = manifest["traceability"]
    by_name = {r["name"]: r for r in model["required_relations"]}

    assert set(by_name) == {"threat-has-control", "risk-has-treatment"}
    assert by_name["threat-has-control"]["from"] == "threat"
    assert by_name["risk-has-treatment"]["from"] == "risk"

    checks = {r["check"] for r in by_name.values()}
    assert checks == {"uncontrolled-threat", "untreated-risk"}
    assert len(checks) == len(by_name), "each relation is independently tunable"

    declared = {o["name"] for o in manifest["object_types"]}
    permitted = {
        verb
        for o in manifest["object_types"]
        for verb in (o.get("allowed_links") or {})
    }
    for relation in by_name.values():
        assert relation["direction"] == "incoming"
        assert relation["from"] in declared, relation["from"]
        for verb in relation["edges"]:
            assert verb in permitted, f"{verb} is not a verb this module permits"

    assert model["acyclic_edges"] == ["arises_from"]
