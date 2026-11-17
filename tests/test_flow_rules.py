"""Engine coverage for the starter flow rules declared by FR-025."""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess

import pytest
import yaml
from conftest import PACKAGE_ROOT, SCHEMAS_DIR, engine_tool, iso_module_path

ARCHITECTURE_MODULE = (
    PACKAGE_ROOT.parent / "node_modules" / "@agent-ix" / "spec-objects-architecture"
)


def _module(root, manifest: dict, *, include_threat_rules: bool = False) -> None:
    """Project the starter rules into an isolated engine module.

    The packaged security module imports many unrelated roles and edges. This
    probe keeps the engine check focused on the declarations under test. It
    uses the committed security schemas and the published architecture sink
    schema without copying either module's files.
    """
    root.mkdir()
    architecture_version = json.loads(
        (ARCHITECTURE_MODULE / "package.json").read_text()
    )["version"]
    assert architecture_version == "0.13.0"
    schemas = root / "schemas"
    schemas.mkdir()
    for schema_name in (
        "ControlFrontmatter.json",
        "DataClassificationFrontmatter.json",
        "TrustBoundaryFrontmatter.json",
    ):
        (schemas / schema_name).symlink_to(SCHEMAS_DIR / schema_name)
    (schemas / "DataSinkFrontmatter.json").symlink_to(
        ARCHITECTURE_MODULE / "schemas" / "DataSinkFrontmatter.json"
    )
    (schemas / "RiskFrontmatter.json").symlink_to(SCHEMAS_DIR / "RiskFrontmatter.json")
    selected_names = {
        "health-across-untrusted-boundary",
        "personal-across-untrusted-boundary",
        "regulated-data-to-uncovered-processor",
        "health-in-llm-prompt-or-tool-call",
        "health-in-log",
        "health-display-unvalidated",
    }
    if include_threat_rules:
        selected_names.update(
            {
                "crossing-without-threat",
                "classified-sink-without-threat",
                "threat-without-treatment",
            }
        )
    selected = [
        rule
        for rule in manifest["traceability"]["flow_rules"]
        if rule["name"] in selected_names
    ]
    remediations = manifest["traceability"]["remediations"]
    probe = {
        "manifest_version": "1.0.0",
        "name": "security-connection-flow-probe",
        "version": "0.1.0",
        "description": "Isolated engine coverage for the connection flow rules.",
        "roles": {
            "connection": {"description": "A data connection."},
            "data_classification": {
                "description": "A classification of regulated data."
            },
            "data_sink": {"description": "A data sink."},
            "trust_boundary": {
                "description": "A boundary between zones with different trust levels."
            },
            "threat_model": {"description": "A threat model."},
            "threat": {"description": "A threat."},
            "risk": {"description": "A risk."},
        },
        "archetypes": [
            {
                "name": "connection",
                "allowed_links": {
                    "carries": ["data_classification"],
                    "crosses": ["trust_boundary"],
                    "delivers_to": ["data_sink"],
                },
            },
            {
                "name": "data_classification",
                "frontmatter_schema_ref": "schemas/DataClassificationFrontmatter.json",
            },
            {
                "name": "trust_boundary",
                "frontmatter_schema_ref": "schemas/TrustBoundaryFrontmatter.json",
            },
            {
                "name": "control",
                "frontmatter_schema_ref": "schemas/ControlFrontmatter.json",
                "allowed_links": {
                    "protects": ["connection", "data_sink"],
                    "mitigates": ["threat"],
                },
            },
            {
                "name": "data_sink",
                "frontmatter_schema_ref": "schemas/DataSinkFrontmatter.json",
                "allowed_links": {"carries": ["data_classification"]},
            },
            {
                "name": "threat_model",
                "allowed_links": {
                    "scopes": ["connection", "data_sink"],
                    "considers": ["threat"],
                },
            },
            {
                "name": "threat",
                "allowed_links": {
                    "threatens": ["connection", "data_sink", "trust_boundary"]
                },
            },
            {
                "name": "risk",
                "frontmatter_schema_ref": "schemas/RiskFrontmatter.json",
                "allowed_links": {"arises_from": ["threat"]},
            },
        ],
        "edge_types": {
            "carries": {"description": "Carries data.", "category": "dataflow"},
            "crosses": {"description": "Crosses a boundary.", "category": "dataflow"},
            "delivers_to": {
                "description": "Delivers data to a sink.",
                "category": "dataflow",
            },
            "protects": {
                "description": "Protects a connection.",
                "category": "governance",
            },
            "scopes": {
                "description": "Threat model scopes element.",
                "category": "governance",
            },
            "considers": {
                "description": "Threat model considers threat.",
                "category": "governance",
            },
            "threatens": {
                "description": "Threat targets element.",
                "category": "governance",
            },
            "mitigates": {
                "description": "Control mitigates threat.",
                "category": "governance",
            },
            "arises_from": {
                "description": "Risk arises from threat.",
                "category": "governance",
            },
        },
        "traceability": {"flow_rules": selected, "remediations": remediations},
    }
    (root / "manifest.yaml").write_text(yaml.safe_dump(probe, sort_keys=False))


def _document(root, doc_id: str, kind: str, fields: str = "", links: str = "") -> None:
    spec = root / "spec"
    spec.mkdir(exist_ok=True)
    text = (
        f"---\nid: {doc_id}\ntitle: {doc_id}\ntype: {kind}\n"
        f"{fields}{links}---\n# {doc_id}\n"
    )
    (spec / f"{doc_id}.md").write_text(text)


def _flow_report(scope, module) -> dict:
    result = subprocess.run(
        [
            engine_tool("quire"),
            "relations",
            "--scope",
            str(scope),
            "--module",
            str(module),
            "--flow",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


@pytest.mark.trace("TC-273", "FR-028-AC-9")
def test_dossier_facts_are_visible_in_flow_report_for_plat_fixture(tmp_path):
    fixture_value = os.environ.get("PLAT1658_ARCHITECTURE_FIXTURE_ROOT")
    if not fixture_value:
        pytest.skip(
            "set PLAT1658_ARCHITECTURE_FIXTURE_ROOT to the PLAT fixture checkout"
        )
    fixture_root = pathlib.Path(fixture_value).resolve()
    assert fixture_root.is_dir(), fixture_root
    architecture_module = fixture_root.parents[3] / "spec_objects_architecture"
    assert (architecture_module / "manifest.yaml").is_file(), architecture_module
    iso_module_value = os.environ.get("PLAT1658_SPEC_ARTIFACTS_ISO_MODULE")
    iso_module = (
        pathlib.Path(iso_module_value) if iso_module_value else iso_module_path()
    )

    activity = tmp_path / "activity"
    activity_docs = activity / "spec" / "model"
    activity_docs.mkdir(parents=True)
    (activity_docs / "PA-001.md").write_text(
        "---\n"
        "id: PA-001\n"
        "title: Support processing\n"
        "type: processing_activity\n"
        "role: controller\n"
        'controller: "Example Controller; privacy@example.invalid"\n'
        "home_regions: [eu]\n"
        "joint_controllers: [Joint Controller]\n"
        "representative: Representative\n"
        "dpo_contact: dpo@example.invalid\n"
        "purposes: [provide-support]\n"
        "data_subject_categories: [customers]\n"
        "retention: support-period\n"
        "relationships:\n"
        "  - target: ix://example/fixtures/CONN-DELIVERS\n"
        "    type: scopes\n"
        "  - target: ix://example/fixtures/PART-DELIVERS\n"
        "    type: scopes\n"
        "---\n"
        "# Support processing\n"
    )
    (activity_docs / "PA-002.md").write_text(
        "---\n"
        "id: PA-002\n"
        "title: Processor work\n"
        "type: processing_activity\n"
        "role: processor\n"
        "processor: Processor Co; processor@example.invalid\n"
        "controller: [Controller Co; controller@example.invalid]\n"
        "home_regions: [US]\n"
        "relationships:\n"
        "  - target: ix://example/fixtures/CONN-DELIVERS\n"
        "    type: scopes\n"
        "---\n"
        "# Processor work\n"
    )
    module_args = [
        arg
        for module in (
            PACKAGE_ROOT,
            architecture_module,
            iso_module,
        )
        for arg in ("--module", str(module))
    ]
    result = subprocess.run(
        [
            engine_tool("quire"),
            "relations",
            "--repo",
            f"example/fixtures={fixture_root}",
            "--repo",
            f"example/pa={activity}",
            *module_args,
            "--flow",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)

    activities = {item["id"]: item for item in report["facts"]["processing_activity"]}
    controller = activities["PA-001"]
    assert {
        "role",
        "controller",
        "home_regions",
        "joint_controllers",
        "representative",
        "dpo_contact",
        "purposes",
        "data_subject_categories",
        "retention",
    } <= set(controller["fields"])
    assert {(edge["edge"], edge["target"]["id"]) for edge in controller["edges"]} == {
        ("scopes", "CONN-DELIVERS"),
        ("scopes", "PART-DELIVERS"),
    }
    assert {"processor", "controller", "home_regions"} <= set(
        activities["PA-002"]["fields"]
    )
    sink = next(
        item for item in report["facts"]["data_sink"] if item["id"] == "SINK-LLM-PROMPT"
    )
    assert {
        "processor",
        "audience_roles",
        "region",
        "purpose",
    } <= set(sink["fields"])
    classification = next(
        item
        for item in report["facts"]["data_classification"]
        if item["id"] == "CLASS-PHI"
    )
    assert classification["fields"]["title"] == "HealthData"
    part = next(
        item for item in report["facts"]["part"] if item["id"] == "PART-DELIVERS"
    )
    assert any(
        edge["edge"] == "delivers_to" and edge["target"]["id"] == "SINK-LLM-PROMPT"
        for edge in part["edges"]
    )
    assert not [
        denial for denial in report["denials"] if denial["rule"].startswith("dossier-")
    ]


@pytest.mark.trace("TC-258", "FR-025-AC-1", "FR-025-AC-2")
@pytest.mark.parametrize(
    ("fixture_name", "expected_rule"),
    [
        ("health-across-untrusted-boundary", "health-across-untrusted-boundary"),
        ("personal-across-untrusted-boundary", "personal-across-untrusted-boundary"),
    ],
)
def test_connection_flow_rules_deny_unprotected_data_and_clear_with_control(
    tmp_path, fixture_name, expected_rule
):
    source_manifest = yaml.safe_load((PACKAGE_ROOT / "manifest.yaml").read_text())
    module = tmp_path / "module"
    _module(module, source_manifest)
    fixtures = PACKAGE_ROOT.parent / "tests" / "fixtures" / "flow_rules" / fixture_name
    report = _flow_report(fixtures / "fail", module)
    assert [denial["rule"] for denial in report["denials"]] == [expected_rule]
    assert report["denials"][0]["subject"]["id"] == "CONN-001"
    assert report["denials"][0]["remediations"][0]["name"] == "encrypt-in-transit"
    protected_report = _flow_report(fixtures / "pass", module)
    assert not any(
        denial["rule"] == expected_rule for denial in protected_report["denials"]
    )


FLOW_FIXTURES = {
    "health-across-untrusted-boundary": ("control", "encrypt-in-transit", "CONN-001"),
    "personal-across-untrusted-boundary": (
        "control",
        "encrypt-in-transit",
        "CONN-001",
    ),
    "regulated-data-to-uncovered-processor": ("agreement", "covered", "SINK-001"),
    "health-in-llm-prompt-or-tool-call": ("control", "anonymize", "SINK-001"),
    "health-in-log": ("control", "pseudonymize", "SINK-001"),
    "health-display-unvalidated": (
        "control",
        "validate-before-display",
        "SINK-001",
    ),
}


def _apply_fixture_remediation(scope, rule: str) -> None:
    action, value, subject_id = FLOW_FIXTURES[rule]
    if action == "agreement":
        sink_path = scope / "spec" / f"{subject_id}.md"
        sink_path.write_text(
            sink_path.read_text().replace(
                "processor_agreement: not_covered", "processor_agreement: covered"
            )
        )
        return
    _document(
        scope,
        "CTRL-001",
        "control",
        f"safeguards: [{value}]\n",
        f"relationships:\n  - type: protects\n    target: {subject_id}\n",
    )


@pytest.mark.trace("TC-262", "FR-025-AC-5")
@pytest.mark.parametrize("rule", FLOW_FIXTURES)
def test_each_rule_fixture_denies_passes_and_clears_with_its_remediation(
    tmp_path, rule
):
    manifest = yaml.safe_load((PACKAGE_ROOT / "manifest.yaml").read_text())
    module = tmp_path / "module"
    _module(module, manifest)
    fixtures = PACKAGE_ROOT.parent / "tests" / "fixtures" / "flow_rules" / rule

    failing = _flow_report(fixtures / "fail", module)
    matching = [denial for denial in failing["denials"] if denial["rule"] == rule]
    assert len(matching) == 1, failing["denials"]
    assert matching[0]["subject"]["id"] == FLOW_FIXTURES[rule][2]

    passing = _flow_report(fixtures / "pass", module)
    assert not any(denial["rule"] == rule for denial in passing["denials"])

    remediated = tmp_path / "remediated"
    shutil.copytree(fixtures / "fail", remediated)
    _apply_fixture_remediation(remediated, rule)
    after = _flow_report(remediated, module)
    assert not any(denial["rule"] == rule for denial in after["denials"])


def _sink_case(
    scope,
    *,
    sink_id: str,
    kind: str,
    category: str,
    agreement: str,
    via_connection: bool = False,
):
    classification_id = f"CLASS-{sink_id}"
    _document(
        scope,
        classification_id,
        "data_classification",
        f"regulated_categories: [{category}]\n",
    )
    sink_links = ""
    if via_connection:
        connection_id = f"CONN-{sink_id}"
        _document(
            scope,
            connection_id,
            "connection",
            links=(
                "relationships:\n"
                f"  - type: carries\n    target: {classification_id}\n"
                f"  - type: delivers_to\n    target: {sink_id}\n"
            ),
        )
    else:
        sink_links = (
            "relationships:\n" f"  - type: carries\n    target: {classification_id}\n"
        )
    _document(
        scope,
        sink_id,
        "data_sink",
        f"kind: {kind}\nprocessor_agreement: {agreement}\n",
        sink_links,
    )


def _protect_sink(scope, sink_id: str, safeguard: str) -> None:
    _document(
        scope,
        f"CTRL-{sink_id}",
        "control",
        f"safeguards: [{safeguard}]\n",
        f"relationships:\n  - type: protects\n    target: {sink_id}\n",
    )


@pytest.mark.trace("TC-259", "FR-025-AC-3", "FR-025-AC-4", "FR-025-AC-5")
@pytest.mark.parametrize(
    ("rule", "kind", "category", "agreement", "safeguard", "via_connection"),
    [
        (
            "regulated-data-to-uncovered-processor",
            "datastore",
            "personal",
            "not_covered",
            None,
            True,
        ),
        (
            "health-in-llm-prompt-or-tool-call",
            "llm_prompt",
            "health",
            "not_covered",
            "anonymize",
            False,
        ),
        ("health-in-log", "log", "health", "covered", "pseudonymize", False),
        (
            "health-display-unvalidated",
            "ui_screen",
            "health",
            "covered",
            "validate-before-display",
            False,
        ),
    ],
)
def test_sink_rules_deny_each_risky_flow_and_accept_the_declared_remediation(
    tmp_path, rule, kind, category, agreement, safeguard, via_connection
):
    source_manifest = yaml.safe_load((PACKAGE_ROOT / "manifest.yaml").read_text())
    module = tmp_path / "module"
    _module(module, source_manifest)
    scope = tmp_path / "corpus"
    (scope / "spec").mkdir(parents=True)
    sink_id = "SINK-001"
    _sink_case(
        scope,
        sink_id=sink_id,
        kind=kind,
        category=category,
        agreement=agreement,
        via_connection=via_connection,
    )

    report = _flow_report(scope, module)
    matching = [denial for denial in report["denials"] if denial["rule"] == rule]
    assert len(matching) == 1, report["denials"]
    assert matching[0]["subject"]["id"] == sink_id

    if rule == "regulated-data-to-uncovered-processor":
        sink_path = scope / "spec" / f"{sink_id}.md"
        sink_path.write_text(
            sink_path.read_text().replace(
                "processor_agreement: not_covered", "processor_agreement: covered"
            )
        )
    else:
        _protect_sink(scope, sink_id, safeguard)
    cleared = _flow_report(scope, module)
    assert not any(denial["rule"] == rule for denial in cleared["denials"])


@pytest.mark.trace("TC-259", "FR-025-AC-4")
def test_llm_sink_unknown_agreement_is_denied_but_covered_is_not(tmp_path):
    source_manifest = yaml.safe_load((PACKAGE_ROOT / "manifest.yaml").read_text())
    module = tmp_path / "module"
    _module(module, source_manifest)

    unknown_scope = tmp_path / "unknown-corpus"
    (unknown_scope / "spec").mkdir(parents=True)
    _sink_case(
        unknown_scope,
        sink_id="SINK-UNKNOWN",
        kind="llm_prompt",
        category="health",
        agreement="unknown",
    )
    unknown_report = _flow_report(unknown_scope, module)
    assert any(
        denial["rule"] == "health-in-llm-prompt-or-tool-call"
        for denial in unknown_report["denials"]
    )

    covered_scope = tmp_path / "covered-corpus"
    (covered_scope / "spec").mkdir(parents=True)
    _sink_case(
        covered_scope,
        sink_id="SINK-COVERED",
        kind="llm_prompt",
        category="health",
        agreement="covered",
    )
    covered_report = _flow_report(covered_scope, module)
    assert not any(
        denial["rule"] == "health-in-llm-prompt-or-tool-call"
        for denial in covered_report["denials"]
    )


@pytest.mark.trace("TC-260", "FR-025-AC-6", "FR-025-AC-13")
def test_sink_rules_read_both_paths_and_do_not_extend_health_log_to_personal_data(
    tmp_path,
):
    source_manifest = yaml.safe_load((PACKAGE_ROOT / "manifest.yaml").read_text())
    module = tmp_path / "module"
    _module(module, source_manifest)
    scope = tmp_path / "corpus"
    (scope / "spec").mkdir(parents=True)

    _sink_case(
        scope,
        sink_id="SINK-LLM",
        kind="llm_prompt",
        category="health",
        agreement="not_covered",
    )
    report = _flow_report(scope, module)
    assert {denial["rule"] for denial in report["denials"]} == {
        "regulated-data-to-uncovered-processor",
        "health-in-llm-prompt-or-tool-call",
    }
    assert all(denial["subject"]["id"] == "SINK-LLM" for denial in report["denials"])

    personal_scope = tmp_path / "personal-corpus"
    (personal_scope / "spec").mkdir(parents=True)
    _sink_case(
        personal_scope,
        sink_id="SINK-LOG",
        kind="log",
        category="personal",
        agreement="not_covered",
    )
    personal_report = _flow_report(personal_scope, module)
    assert [denial["rule"] for denial in personal_report["denials"]] == [
        "regulated-data-to-uncovered-processor"
    ]

    empty_scope = tmp_path / "empty-corpus"
    (empty_scope / "spec").mkdir(parents=True)
    empty_report = _flow_report(empty_scope, module)
    assert empty_report["denials"] == []


@pytest.mark.trace("TC-261", "FR-025-AC-7", "FR-025-AC-11", "FR-025-AC-12")
def test_all_six_rules_load_against_published_sink_schema_and_reject_bad_enum(
    tmp_path,
):
    source_manifest = yaml.safe_load((PACKAGE_ROOT / "manifest.yaml").read_text())
    module = tmp_path / "module"
    _module(module, source_manifest)
    scope = tmp_path / "corpus"
    (scope / "spec").mkdir(parents=True)
    report = _flow_report(scope, module)
    assert {rule["name"] for rule in report["rules"]} == {
        "health-across-untrusted-boundary",
        "personal-across-untrusted-boundary",
        "regulated-data-to-uncovered-processor",
        "health-in-llm-prompt-or-tool-call",
        "health-in-log",
        "health-display-unvalidated",
    }
    for rule in report["rules"]:
        assert rule["check"] == rule["name"]
        assert rule["rationale"].strip()
        assert rule["remediations"]
        assert set(rule["remediations"]) <= {
            "encrypt-in-transit",
            "restrict-access",
            "pseudonymize",
            "anonymize",
            "restrict-region",
            "validate-before-display",
            "obtain-processor-agreement",
            "remove-from-sink",
            "audit-access",
        }

    invalid_manifest = yaml.safe_load((PACKAGE_ROOT / "manifest.yaml").read_text())
    invalid_rule = next(
        rule
        for rule in invalid_manifest["traceability"]["flow_rules"]
        if rule["name"] == "health-in-llm-prompt-or-tool-call"
    )
    next(
        condition
        for condition in invalid_rule["match"]
        if condition.get("field") == "regulated_categories"
    )["any_of"] = ["medical"]
    invalid_module = tmp_path / "invalid-module"
    _module(invalid_module, invalid_manifest)
    invalid = subprocess.run(
        [
            engine_tool("quire"),
            "relations",
            "--scope",
            str(scope),
            "--module",
            str(invalid_module),
            "--flow",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert invalid.returncode != 0
    invalid_diagnostic = invalid.stdout + invalid.stderr
    assert "health-in-llm-prompt-or-tool-call" in invalid_diagnostic
    assert "medical" in invalid_diagnostic
    assert "regulated_categories" in invalid_diagnostic
    assert str(invalid_module / "manifest.yaml") in invalid_diagnostic

    invalid_remediation_manifest = yaml.safe_load(
        (PACKAGE_ROOT / "manifest.yaml").read_text()
    )
    remediation = next(
        item
        for item in invalid_remediation_manifest["traceability"]["remediations"]
        if item["name"] == "encrypt-in-transit"
    )
    remediation["adds"]["value"] = "encrypt-in-transt"
    invalid_remediation_module = tmp_path / "invalid-remediation-module"
    _module(invalid_remediation_module, invalid_remediation_manifest)
    invalid_remediation = subprocess.run(
        [
            engine_tool("quire"),
            "relations",
            "--scope",
            str(scope),
            "--module",
            str(invalid_remediation_module),
            "--flow",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert invalid_remediation.returncode != 0
    remediation_diagnostic = invalid_remediation.stdout + invalid_remediation.stderr
    assert "health-across-untrusted-boundary" in remediation_diagnostic
    assert "encrypt-in-transit" in remediation_diagnostic
    assert str(invalid_remediation_module / "manifest.yaml") in remediation_diagnostic


@pytest.mark.trace("TC-263", "FR-025-AC-14")
def test_public_privacy_scope_is_limited_and_disclosed():
    manifest = yaml.safe_load((PACKAGE_ROOT / "manifest.yaml").read_text())
    rules = manifest["traceability"]["flow_rules"]
    fields = {
        condition.get("field")
        for rule in rules
        if not rule["name"].startswith("dossier-")
        for condition in rule.get("match", [])
    }
    assert "home_regions" not in fields
    assert "purposes" not in fields

    readme = (PACKAGE_ROOT.parent / "README.md").read_text().lower()
    assert "does not map roles to purposes" in readme
    assert (
        "do not decide whether a safeguard is adequate or establish compliance"
        in readme
    )
    assert "ecfr.gov" in readme
    assert "eur-lex.europa.eu" in readme
    assert "owasp.org" in readme
    for text in (readme, *(rule.get("rationale", "").lower() for rule in rules)):
        assert "compliant" not in text
        assert "nist sp 800-53" not in text
        assert "owasp asvs" not in text
