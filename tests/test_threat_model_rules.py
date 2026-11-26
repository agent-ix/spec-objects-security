"""Threat-model completeness and treatment rules from FR-027."""

from __future__ import annotations

import json
import os
import shutil
import subprocess

import pytest
import yaml

from tests.conftest import (
    MANIFEST_PATH,
    PACKAGE_ROOT,
    SCHEMAS_DIR,
    engine_tool,
    validation_module_args,
)
from tests.test_flow_rules import _flow_report, _module

RULES = {
    "crossing-without-threat",
    "classified-sink-without-threat",
    "threat-without-treatment",
}
FIXTURES = PACKAGE_ROOT.parent / "tests" / "fixtures" / "threat_model_rules"


def _rule_report(tmp_path, fixture="uncovered"):
    tmp_path.mkdir(parents=True, exist_ok=True)
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    module = tmp_path / "module"
    _module(module, manifest, include_threat_rules=True)
    scope = tmp_path / "corpus"
    shutil.copytree(FIXTURES / fixture, scope)
    return scope, _flow_report(scope, module)


def _denials(report, rule):
    return [denial for denial in report["denials"] if denial["rule"] == rule]


@pytest.mark.trace("FR-027-AC-1", "FR-027-AC-2", "FR-027-AC-3")
def test_uncovered_fixture_reports_each_scoped_gap_and_covered_fixture_clears_it(
    tmp_path,
):
    _, uncovered = _rule_report(tmp_path / "uncovered")
    assert RULES <= {denial["rule"] for denial in uncovered["denials"]}
    expected_subjects = {
        "crossing-without-threat": "CONN-1",
        "classified-sink-without-threat": "SINK-1",
        "threat-without-treatment": "THREAT-1",
    }
    for rule, subject_id in expected_subjects.items():
        findings = _denials(uncovered, rule)
        assert len(findings) == 1, uncovered["denials"]
        assert findings[0]["subject"]["id"] == subject_id

    _, covered = _rule_report(tmp_path / "covered", "covered")
    assert not (set(denial["rule"] for denial in covered["denials"]) & RULES)


@pytest.mark.trace("FR-027-AC-1", "FR-027-AC-2", "FR-027-AC-3")
def test_full_manifest_loads_threat_rules_with_the_published_module_set(tmp_path):
    scope = tmp_path / "uncovered"
    shutil.copytree(FIXTURES / "uncovered", scope)
    env = os.environ.copy()
    env.pop("IX_DEV", None)
    result = subprocess.run(
        [
            engine_tool("quire"),
            "relations",
            "--scope",
            str(scope),
            *validation_module_args(PACKAGE_ROOT, include_iso=True),
            "--flow",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    # The three new rules are module-promoted errors; the report is emitted
    # with exit 1 when this fixture contains the gaps.
    assert result.returncode == 1, result.stderr
    report = json.loads(result.stdout)
    assert RULES <= {denial["rule"] for denial in report["denials"]}


@pytest.mark.trace("FR-027-AC-2")
@pytest.mark.parametrize("edge_to_remove", ["sink carries", "connection carries"])
def test_sink_classification_is_found_through_either_data_path(
    tmp_path, edge_to_remove
):
    scope, _ = _rule_report(tmp_path / "fixture")
    if edge_to_remove == "sink carries":
        path = scope / "spec" / "SINK-1.md"
        content = path.read_text()
        content = content.replace(
            "relationships:\n  - type: carries\n    target: CLASS-1\n", ""
        )
    else:
        path = scope / "spec" / "CONN-1.md"
        content = path.read_text()
        content = content.replace("  - type: carries\n    target: CLASS-1\n", "")
    path.write_text(content)

    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    module = tmp_path / "module"
    _module(module, manifest, include_threat_rules=True)
    report = _flow_report(scope, module)
    assert len(_denials(report, "classified-sink-without-threat")) == 1


@pytest.mark.trace("FR-027-AC-1", "FR-027-AC-5")
def test_subject_target_clears_and_unscoped_elements_stay_quiet(tmp_path):
    scope, _ = _rule_report(tmp_path / "fixture")
    threat = scope / "spec" / "THREAT-1.md"
    threat.write_text(
        threat.read_text()
        .replace("target: CONN-1", "target: BOUND-1")
        .replace("target: SINK-1", "target: BOUND-1")
    )
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    module = tmp_path / "module"
    _module(module, manifest, include_threat_rules=True)
    report = _flow_report(scope, module)
    assert len(_denials(report, "crossing-without-threat")) == 1

    (scope / "spec" / "TM-1.md").unlink()
    quiet = _flow_report(scope, module)
    assert not (set(denial["rule"] for denial in quiet["denials"]) & RULES)


@pytest.mark.trace("FR-027-AC-1")
@pytest.mark.parametrize("edge_to_remove", ["carries", "crosses"])
def test_connection_without_either_crossing_precondition_is_not_reported(
    tmp_path, edge_to_remove
):
    scope, _ = _rule_report(tmp_path / edge_to_remove)
    connection = scope / "spec" / "CONN-1.md"
    edge_target = "CLASS-1" if edge_to_remove == "carries" else "BOUND-1"
    connection.write_text(
        connection.read_text().replace(
            f"  - type: {edge_to_remove}\n    target: {edge_target}\n", ""
        )
    )
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    module = tmp_path / f"{edge_to_remove}-module"
    _module(module, manifest, include_threat_rules=True)
    report = _flow_report(scope, module)
    assert not _denials(report, "crossing-without-threat")


@pytest.mark.trace("FR-027-AC-5")
def test_empty_corpus_is_quiet_for_all_threat_model_rules(tmp_path):
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    module = tmp_path / "module"
    _module(module, manifest, include_threat_rules=True)
    scope = tmp_path / "empty"
    (scope / "spec").mkdir(parents=True)

    report = _flow_report(scope, module)

    assert not (set(denial["rule"] for denial in report["denials"]) & RULES)


@pytest.mark.trace("FR-027-AC-3", "FR-027-AC-4")
@pytest.mark.parametrize(
    ("decision", "expected"),
    [("accepted", False), ("undecided", True), ("not_accepted", True)],
)
def test_control_or_only_accepted_risk_treats_a_considered_threat(
    tmp_path, decision, expected
):
    scope, _ = _rule_report(tmp_path / "fixture", "covered")
    threat = scope / "spec" / "THREAT-1.md"
    threat.write_text(
        threat.read_text()
        .replace("  - type: threatens\n    target: SINK-1\n", "")
        .replace("  - type: mitigates\n    target: THREAT-1\n", "")
    )
    (scope / "spec" / "CTRL-1.md").unlink()
    (scope / "spec" / "RISK-1.md").write_text(
        "---\nid: RISK-1\ntitle: Risk\ntype: risk\nobject: risk\n"
        f"decision: {decision}\n"
        "relationships:\n  - type: arises_from\n    target: THREAT-1\n---\n# Risk\n"
    )
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    module = tmp_path / "module"
    _module(module, manifest, include_threat_rules=True)
    report = _flow_report(scope, module)
    assert bool(_denials(report, "threat-without-treatment")) is expected


@pytest.mark.trace("FR-027-AC-8", "FR-027-AC-9", "FR-027-AC-10")
def test_rule_declarations_are_tunable_remediation_free_and_do_not_change_registry():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    declarations = {
        rule["name"]: rule for rule in manifest["traceability"]["flow_rules"]
    }
    assert RULES <= declarations.keys()
    for name in RULES:
        rule = declarations[name]
        assert rule["check"] == name
        assert rule["rationale"].strip()
        assert "remediations" not in rule
        for condition in [*rule["match"], *rule.get("unless_any", [])]:
            if condition.get("present"):
                assert condition["field"] == "id"

    assert manifest["grammar_severity"] == {
        f"trace:{name}": "error" for name in sorted(RULES)
    }
    assert len(manifest["traceability"]["remediations"]) == 9
    assert "threat-has-control" not in {
        rule["name"] for rule in manifest["traceability"]["required_relations"]
    }
    risk_rule = next(
        rule
        for rule in manifest["traceability"]["required_relations"]
        if rule["name"] == "risk-has-treatment"
    )
    assert risk_rule["where"] == {
        "field": "decision",
        "values": ["undecided", "not_accepted"],
    }
    enum = yaml.safe_load((SCHEMAS_DIR / "RiskDecision.json").read_text())
    enum_values = {"decision": enum["enum"]}
    for name in RULES:
        for condition in [
            *declarations[name]["match"],
            *declarations[name].get("unless_any", []),
        ]:
            if "any_of" in condition:
                assert set(condition["any_of"]) <= set(enum_values[condition["field"]])
    assert "risk" in {obj["name"] for obj in manifest["object_types"]}


@pytest.mark.trace("FR-027-AC-8")
def test_risk_frontmatter_schema_is_open_enum_only_and_referenced():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    risk_archetype = next(
        archetype
        for archetype in manifest["object_types"]
        if archetype["name"] == "risk"
    )
    assert risk_archetype["frontmatter_schema_ref"] == "schemas/RiskFrontmatter.json"

    enum = yaml.safe_load((SCHEMAS_DIR / "RiskDecision.json").read_text())
    assert enum["enum"] == ["undecided", "accepted", "not_accepted"]
    frontmatter = yaml.safe_load((SCHEMAS_DIR / "RiskFrontmatter.json").read_text())
    assert set(frontmatter["properties"]) == {"decision"}
    assert "additionalProperties" not in frontmatter
    assert "required" not in frontmatter
    assert frontmatter["properties"]["decision"]["enum"] == enum["enum"]
    risk = yaml.safe_load((SCHEMAS_DIR / "Risk.json").read_text())
    for key in ("decision", "decided_by"):
        assert "default" not in risk["properties"][key]


@pytest.mark.trace("FR-027-AC-10")
def test_accepted_risk_is_excluded_from_the_untreated_risk_relation(tmp_path):
    source = yaml.safe_load(MANIFEST_PATH.read_text())
    rule = next(
        relation
        for relation in source["traceability"]["required_relations"]
        if relation["name"] == "risk-has-treatment"
    )
    module = tmp_path / "module"
    module.mkdir()
    probe = {
        "manifest_version": "1.0.0",
        "name": "risk-treatment-probe",
        "version": "0.1.0",
        "roles": {"risk": {"description": "A risk."}},
        "archetypes": [{"name": "risk"}],
        "traceability": {"required_relations": [rule]},
    }
    (module / "manifest.yaml").write_text(yaml.safe_dump(probe, sort_keys=False))
    scope = tmp_path / "corpus"
    spec = scope / "spec"
    spec.mkdir(parents=True)
    for ident, decision, decided_by in (
        ("RISK-ACCEPTED", "accepted", "A. Person"),
        ("RISK-UNDECIDED", "undecided", None),
        ("RISK-REJECTED", "not_accepted", "A. Person"),
    ):
        decider = f"decided_by: {decided_by}\n" if decided_by else ""
        (spec / f"{ident}.md").write_text(
            f"---\nid: {ident}\ntitle: {ident}\ntype: risk\n"
            f"decision: {decision}\n{decider}---\n# {ident}\n"
        )

    result = subprocess.run(
        [
            engine_tool("quire"),
            "relations",
            "--scope",
            str(scope),
            "--module",
            str(module),
            "--relation",
            "risk-has-treatment",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    rows = json.loads(result.stdout)["relations"][0]["rows"]
    assert {row["document"]["id"] for row in rows} == {
        "RISK-UNDECIDED",
        "RISK-REJECTED",
    }


@pytest.mark.trace("NFR-005-AC-1", "NFR-005-M-1")
def test_threat_and_risk_fields_have_no_schema_or_manifest_defaults():
    """Threat, threat-model and risk judgments remain authored inputs.

    Criteria:
      * emitted schemas do not default threat method, reviewer, risk decision,
        decision owner, likelihood or impact;
      * the corresponding manifest extraction declarations do not assert or
        default any of those values.
    """
    fields = {
        "method",
        "reviewed_by",
        "decision",
        "decided_by",
        "likelihood",
        "impact",
    }
    schema_names = {"ThreatModel", "Threat", "Risk"}
    for name in schema_names:
        document = json.loads((SCHEMAS_DIR / f"{name}.json").read_text())
        for field_name in fields & set(document.get("properties", {})):
            assert "default" not in document["properties"][field_name], (
                name,
                field_name,
            )

    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    object_types = {
        item["name"]: item
        for item in manifest["object_types"]
        if item["name"] in {"threat_model", "threat", "risk"}
    }
    assert set(object_types) == {"threat_model", "threat", "risk"}
    for name, object_type in object_types.items():
        extracted = object_type["body_extraction"]["yield_pattern"]["match"]
        relevant = fields & set(extracted)
        for field_name in relevant:
            declaration = extracted[field_name]
            assert "assert" not in declaration, (name, field_name)
            assert "default" not in declaration, (name, field_name)


@pytest.mark.trace("NFR-005-AC-2", "NFR-005-M-2")
def test_unconsidered_crossing_emits_only_the_crossing_without_threat_finding(
    tmp_path,
):
    """An authored empty threat-model consideration list creates no judgments.

    The corpus contains a classified connection crossing a trust boundary and
    a threat model that scopes it without a ``considers`` edge. The relation
    report must preserve that absence and report only the missing-threat check.
    """
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    module = tmp_path / "module"
    _module(module, manifest, include_threat_rules=True)
    scope = tmp_path / "corpus"
    spec = scope / "spec"
    spec.mkdir(parents=True)
    (spec / "CONN-1.md").write_text(
        "---\nid: CONN-1\ntitle: Connection\ntype: connection\n"
        "relationships:\n  - type: carries\n    target: CLASS-1\n"
        "  - type: crosses\n    target: BOUND-1\n---\n# Connection\n"
    )
    (spec / "CLASS-1.md").write_text(
        "---\nid: CLASS-1\ntitle: Classification\ntype: data_classification\n"
        "regulated_categories: [health]\n---\n# Classification\n"
    )
    (spec / "BOUND-1.md").write_text(
        "---\nid: BOUND-1\ntitle: Boundary\ntype: trust_boundary\n"
        "trust_level: untrusted\n---\n# Boundary\n"
    )
    (spec / "TM-1.md").write_text(
        "---\nid: TM-1\ntitle: Threat model\ntype: threat_model\n"
        "relationships:\n  - type: scopes\n    target: CONN-1\n---\n"
        "# Threat model\n"
    )

    report = _flow_report(scope, module)

    assert {path.name for path in spec.iterdir()} == {
        "CONN-1.md",
        "CLASS-1.md",
        "BOUND-1.md",
        "TM-1.md",
    }
    facts = report["facts"]
    assert facts["threat"] == []
    assert facts["risk"] == []
    assert not any(
        edge["edge"] == "considers"
        for records in facts.values()
        for record in records
        for edge in record["edges"]
    )
    threat_findings = [
        denial for denial in report["denials"] if denial["rule"] in RULES
    ]
    assert [denial["rule"] for denial in threat_findings] == [
        "crossing-without-threat"
    ], report["denials"]
    assert threat_findings[0]["subject"]["id"] == "CONN-1"


@pytest.mark.trace("NFR-005-AC-3")
def test_risk_flow_rules_do_not_read_ratings_or_emit_a_score():
    """Risk completeness uses an authored decision and never computes a score."""
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    for rule in manifest["traceability"]["flow_rules"]:
        for condition in [*rule["match"], *rule.get("unless_any", [])]:
            assert condition.get("field") not in {"likelihood", "impact"}

    risk_schema = json.loads((SCHEMAS_DIR / "Risk.json").read_text())
    assert "score" not in risk_schema["properties"]


@pytest.mark.trace("NFR-005-M-2")
def test_threat_model_extraction_contains_only_authored_judgments(tmp_path):
    """Extraction preserves authored threat-model fields without inventing risk."""
    document = tmp_path / "threat_model.md"
    document.write_text(
        "---\nid: TM-1\ntitle: Threat model\ntype: threat_model\n"
        "method: stride_per_element\nreviewed_by: A. Person\n"
        "relationships:\n  - type: scopes\n    target: CONN-1\n---\n"
        "# Threat model\n\n## Scope\n\nThe connection.\n\n"
        "## Assumptions\n\nNone.\n\n## Out of scope\n\nExternal systems.\n\n"
        "## Properties\n\n| Field | Type | Multiplicity | Constraints |\n"
        "|---|---|---|---|\n| threat_model_id | UUID | 1..1 | identity |\n"
    )
    result = subprocess.run(
        [
            engine_tool("quire"),
            "extract",
            "--module",
            str(PACKAGE_ROOT),
            str(document),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    extraction_output = json.loads(result.stdout)
    record = extraction_output["extraction"]["records"][0]

    assert len(extraction_output["extraction"]["records"]) == 1
    assert extraction_output["edges"] == [{"target": "CONN-1", "type": "scopes"}]
    assert record["method"] == "stride_per_element"
    assert record["reviewed_by"] == "A. Person"
    assert not {
        "threat",
        "considers",
        "likelihood",
        "impact",
        "decision",
        "decided_by",
    } & set(record)


@pytest.mark.trace("NFR-005-AC-3")
def test_risk_extraction_keeps_ratings_authored_and_has_no_computed_score():
    """A risk extract contains the stated axes and decision without a score."""
    result = subprocess.run(
        [
            engine_tool("quire"),
            "extract",
            "--module",
            str(PACKAGE_ROOT),
            str(PACKAGE_ROOT / "skeletons" / "risk.md"),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout)["extraction"]

    assert len(payload["records"]) == 1
    record = payload["records"][0]
    assert record["likelihood"] == "possible"
    assert record["impact"] == "major"
    assert record["decision"] == "undecided"
    assert "score" not in record
