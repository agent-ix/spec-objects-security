"""Threat-model completeness and treatment rules from FR-027."""

from __future__ import annotations

import shutil

import pytest
import yaml

from tests.conftest import MANIFEST_PATH, PACKAGE_ROOT, SCHEMAS_DIR
from tests.test_flow_rules import _flow_report, _module

RULES = {
    "crossing-without-threat",
    "classified-sink-without-threat",
    "threat-without-treatment",
}
FIXTURES = PACKAGE_ROOT.parent / "tests" / "fixtures" / "threat_model_rules"


def _rule_report(tmp_path, fixture="uncovered"):
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    module = tmp_path / "module"
    _module(module, manifest)
    scope = tmp_path / "corpus"
    shutil.copytree(FIXTURES / fixture, scope)
    return scope, _flow_report(scope, module)


def _denials(report, rule):
    return [denial for denial in report["denials"] if denial["rule"] == rule]


@pytest.mark.trace("TC-264", "FR-027-AC-1", "FR-027-AC-2", "FR-027-AC-3")
def test_uncovered_fixture_reports_each_scoped_gap_and_covered_fixture_clears_it(
    tmp_path,
):
    _, uncovered = _rule_report(tmp_path / "uncovered")
    assert {denial["rule"] for denial in uncovered["denials"]} == RULES
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


@pytest.mark.trace("TC-265", "FR-027-AC-2")
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
    _module(module, manifest)
    report = _flow_report(scope, module)
    assert len(_denials(report, "classified-sink-without-threat")) == 1


@pytest.mark.trace("TC-266", "FR-027-AC-1", "FR-027-AC-5")
def test_only_the_subject_threat_target_clears_and_unscoped_or_incomplete_elements_are_quiet(
    tmp_path,
):
    scope, _ = _rule_report(tmp_path / "fixture")
    threat = scope / "spec" / "THREAT-1.md"
    threat.write_text(
        threat.read_text()
        .replace("target: CONN-1", "target: BOUND-1")
        .replace("target: SINK-1", "target: BOUND-1")
    )
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    module = tmp_path / "module"
    _module(module, manifest)
    report = _flow_report(scope, module)
    assert len(_denials(report, "crossing-without-threat")) == 1

    (scope / "spec" / "TM-1.md").unlink()
    quiet = _flow_report(scope, module)
    assert not (set(denial["rule"] for denial in quiet["denials"]) & RULES)

    scope, _ = _rule_report(tmp_path / "incomplete")
    connection = scope / "spec" / "CONN-1.md"
    connection.write_text(
        connection.read_text()
        .replace("  - type: carries\n    target: CLASS-1\n", "")
        .replace("  - type: crosses\n    target: BOUND-1\n", "")
    )
    sink = scope / "spec" / "SINK-1.md"
    sink.write_text(
        sink.read_text().replace(
            "relationships:\n  - type: carries\n    target: CLASS-1\n", ""
        )
    )
    module = tmp_path / "incomplete-module"
    _module(module, manifest)
    incomplete = _flow_report(scope, module)
    assert not _denials(incomplete, "crossing-without-threat")
    assert not _denials(incomplete, "classified-sink-without-threat")


@pytest.mark.trace("TC-267", "FR-027-AC-3", "FR-027-AC-4")
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
    _module(module, manifest)
    report = _flow_report(scope, module)
    assert bool(_denials(report, "threat-without-treatment")) is expected


@pytest.mark.trace("TC-268", "FR-027-AC-8", "FR-027-AC-9", "FR-027-AC-10")
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
    assert enum["enum"] == ["undecided", "accepted", "not_accepted"]
    assert "risk" in {obj["name"] for obj in manifest["object_types"]}
