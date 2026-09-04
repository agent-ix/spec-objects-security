"""One role-distinct declaration schema per security object type.

Every record here is **hand-built**. The keys these criteria exercise beyond
`fields`, `clauses` and `operations` are not populated by the extractor of the
pinned wheel (`agent-ix/quoin#335` owns the mapping), so this file is schema
evidence and never extraction evidence. The extraction path is exercised in
`test_skeletons_semantic.py`.
"""

from __future__ import annotations

import json

import pytest

from tests.conftest import (
    CLAUSE,
    MODEL_OF,
    OBJECT_TYPES,
    OPERATION,
    SCHEMAS_DIR,
    field,
)

MODELS = [MODEL_OF[name] for name in OBJECT_TYPES]


def schema(model: str) -> dict:
    return json.loads((SCHEMAS_DIR / f"{model}.json").read_text())


def signature(model: str) -> tuple:
    """The rule set that makes one type differ from another: its required keys,
    the keys it admits at all, and every item rule over those keys."""
    doc = schema(model)
    required = tuple(sorted(doc.get("required", [])))
    admitted = tuple(sorted(doc.get("properties", {})))
    rules = []
    for key, value in sorted(doc.get("properties", {}).items()):
        for keyword in ("minItems", "contains", "items"):
            if keyword in value:
                rules.append((key, keyword, json.dumps(value[keyword], sort_keys=True)))
    for branch in doc.get("allOf", []):
        rules.append(("allOf", "branch", json.dumps(branch, sort_keys=True)))
    return (required, admitted, tuple(sorted(rules)))


@pytest.mark.trace("TC-050", "FR-004-AC-1")
def test_every_schema_differs_from_every_other():
    seen: dict[tuple, str] = {}
    for model in MODELS:
        doc = schema(model)
        assert set(doc) > {"$schema", "$id", "type"}, model
        assert doc.get("required"), f"{model} requires nothing"
        key = signature(model)
        assert key not in seen, f"{model} is indistinguishable from {seen.get(key)}"
        seen[key] = model
    assert len(seen) == 23


@pytest.mark.trace("TC-051", "FR-004-AC-2")
def test_asset_requires_an_identity_field(schema_registry):
    validator = schema_registry("Asset")
    ok = {"fields": [field("asset_id", "UUID", identity=True)]}
    assert validator.is_valid(ok)
    assert not validator.is_valid({"fields": [field("asset_id", "UUID")]})
    assert not validator.is_valid({})
    assert not validator.is_valid({"fields": []})


@pytest.mark.trace("TC-052", "FR-004-AC-3")
def test_role_permission_and_scope_refuse_the_keys_their_roles_exclude(
    schema_registry,
):
    identity = [field("id", "UUID", identity=True)]
    assert schema_registry("Role").is_valid({"fields": identity})
    assert not schema_registry("Role").is_valid(
        {"fields": identity, "operations": [OPERATION]}
    )
    for model in ("Permission", "Scope"):
        assert schema_registry(model).is_valid({"fields": identity})
        assert not schema_registry(model).is_valid(
            {"fields": identity, "relations": []}
        )
        assert not schema_registry(model).is_valid(
            {"fields": identity, "operations": [OPERATION]}
        )


@pytest.mark.trace("TC-053", "FR-004-AC-4")
def test_threat_requires_a_stride_row_and_a_closed_stride_value(schema_registry):
    validator = schema_registry("Threat")
    identity = field("threat_id", "UUID", identity=True)
    stride = field("stride_category")
    assert validator.is_valid({"fields": [identity, stride]})
    assert not validator.is_valid({"fields": [identity]})
    assert validator.is_valid(
        {"fields": [identity, stride], "stride_category": "spoofing"}
    )
    assert not validator.is_valid(
        {"fields": [identity, stride], "stride_category": "catastrophic"}
    )


@pytest.mark.trace("TC-054", "FR-004-AC-5")
def test_the_assessment_types_require_the_rows_that_score_them(schema_registry):
    identity = field("id", "UUID", identity=True)
    vuln = schema_registry("Vulnerability")
    assert vuln.is_valid({"fields": [identity, field("severity")]})
    assert not vuln.is_valid({"fields": [identity]})
    risk = schema_registry("Risk")
    both = [identity, field("likelihood"), field("impact")]
    assert risk.is_valid({"fields": both})
    assert not risk.is_valid({"fields": [identity, field("likelihood")]})
    assert not risk.is_valid({"fields": [identity, field("impact")]})
    finding = schema_registry("AuditFinding")
    assert finding.is_valid({"fields": [identity, field("status")]})
    assert not finding.is_valid({"fields": [identity]})


@pytest.mark.trace("TC-055", "FR-004-AC-6")
def test_control_states_its_effectiveness_and_constrains_something(schema_registry):
    validator = schema_registry("Control")
    ok = {"clauses": [CLAUSE], "fields": [field("effectiveness")]}
    assert validator.is_valid(ok)
    assert not validator.is_valid({"fields": [field("effectiveness")]})
    assert not validator.is_valid({"clauses": [], "fields": [field("effectiveness")]})
    assert not validator.is_valid({"clauses": [CLAUSE], "fields": [field("owner")]})
    assert not validator.is_valid({**ok, "relations": []})


@pytest.mark.trace("TC-056", "FR-004-AC-7")
def test_every_governing_type_needs_a_clause_and_refuses_operations(schema_registry):
    for model in ("Policy", "PasswordPolicy", "CorsPolicy", "SessionConfig"):
        validator = schema_registry(model)
        assert validator.is_valid({"clauses": [CLAUSE]}), model
        assert not validator.is_valid({"clauses": []}), model
        assert not validator.is_valid({}), model
        assert not validator.is_valid(
            {"clauses": [CLAUSE], "operations": [OPERATION]}
        ), model


@pytest.mark.trace("TC-057", "FR-004-AC-8")
def test_auth_flow_is_its_exchanges(schema_registry):
    validator = schema_registry("AuthFlow")
    assert validator.is_valid({"operations": [OPERATION]})
    assert not validator.is_valid({"operations": []})
    assert not validator.is_valid({})
    assert not validator.is_valid({"operations": [OPERATION], "relations": []})


@pytest.mark.trace("TC-058", "FR-004-AC-9")
def test_audit_event_declares_an_occurrence_and_not_a_record(schema_registry):
    validator = schema_registry("AuditEvent")
    occurrence = field("occurred_at", "Timestamp")
    assert validator.is_valid({"fields": [occurrence]})
    assert not validator.is_valid({"fields": [field("actor")]})
    assert not validator.is_valid(
        {"fields": [occurrence, field("event_id", "UUID", identity=True)]}
    )
    assert not validator.is_valid({"fields": [occurrence], "operations": [OPERATION]})
    assert not validator.is_valid({"fields": [occurrence], "relations": []})


@pytest.mark.trace("TC-059", "FR-004-AC-10")
def test_trust_boundary_admits_no_crossing_it_has_not_ruled_on(schema_registry):
    validator = schema_registry("TrustBoundary")
    fields = [field("boundary_id", "UUID", identity=True), field("trust_level")]
    assert validator.is_valid({"fields": fields, "clauses": [CLAUSE]})
    assert not validator.is_valid({"fields": fields})
    assert not validator.is_valid({"fields": fields, "clauses": []})
    assert not validator.is_valid({"fields": [fields[0]], "clauses": [CLAUSE]})
    assert not validator.is_valid(
        {"fields": fields, "clauses": [CLAUSE], "trust_level": "absolute"}
    )


@pytest.mark.trace("TC-060", "FR-004-AC-11", "FR-004-CON-2")
def test_the_empty_record_fails_every_type(schema_registry):
    for model in MODELS:
        assert not schema_registry(model).is_valid({}), model


@pytest.mark.trace("TC-061", "FR-004-AC-12")
def test_an_unresolved_placeholder_is_a_semantic_id_and_a_bare_token_is_not(
    schema_registry, quire_engine, semantic_module
):
    validator = schema_registry("Asset")
    placeholder = "ix://agent-ix/spec-objects-security/unresolved/Mystery"
    record = {
        "fields": [
            field("asset_id", "UUID", identity=True),
            field("mystery", placeholder),
        ]
    }
    assert validator.is_valid(record)
    bare = {
        "fields": [
            field("asset_id", "UUID", identity=True),
            field("mystery", "Mystery"),
        ]
    }
    assert not validator.is_valid(bare)
    markdown = (
        '---\nid: probe-001\ntitle: "Probe"\ntype: asset\nobject: asset\n---\n'
        "# [probe-001] Probe\n\n## Description\n\nA probe.\n\n## Properties\n\n"
        "| Field | Type | Multiplicity | Constraints |\n|---|---|---|---|\n"
        "| asset_id | UUID | 1..1 | identity |\n"
        "| mystery | Mystery | 1..1 | |\n"
    )
    extracted = quire_engine.extract_semantic(
        {
            "markdown": markdown,
            "module": semantic_module,
            "path": "probe.md",
            "sourceIdentity": "ix://agent-ix/spec-objects-security/probe-001",
            "bundle": {
                "package": semantic_module["package"],
                "objects": [],
                "enumerations": [],
                "imports": {},
            },
        }
    )
    codes = {d.get("code") for d in extracted.get("diagnostics", [])}
    assert "semantic.unresolved-type" in codes, extracted.get("diagnostics")


@pytest.mark.trace("TC-062", "FR-004-AC-13", "FR-004-CON-1")
def test_no_module_schema_redeclares_a_semantic_core_model():
    core = {
        p.stem
        for p in (
            SCHEMAS_DIR.parent.parent
            / "node_modules"
            / "@agent-ix"
            / "semantic-core"
            / "generated"
            / "json-schema"
        ).glob("*.json")
    }
    shipped = {p.stem for p in SCHEMAS_DIR.glob("*.json") if p.name != "toolchain.json"}
    assert not (core & shipped), core & shipped
    grammar_keys = {"fields", "clauses", "operations", "relations", "params", "values"}
    for model in MODELS:
        doc = schema(model)
        for key, value in doc.get("properties", {}).items():
            if key not in grammar_keys:
                continue
            item = value.get("items", value)
            ref = item.get("$ref", "")
            assert ref.startswith(
                "https://schemas.agent-ix.org/semantic-core/0.1.0/"
            ), (model, key, ref)


@pytest.mark.trace("TC-063", "FR-004-AC-14")
def test_data_classification_carries_a_level_and_no_relations(schema_registry):
    validator = schema_registry("DataClassification")
    identity = field("classification_id", "UUID", identity=True)
    assert validator.is_valid({"fields": [identity, field("level")]})
    assert not validator.is_valid({"fields": [identity]})
    assert not validator.is_valid(
        {"fields": [identity, field("level")], "relations": []}
    )
