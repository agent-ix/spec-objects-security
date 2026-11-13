"""FR-009..FR-012 and NFR-001: the `soup_record` object type.

Records here are hand-built declaration records, as in `test_role_schemas.py`:
the keys beyond `fields` are not populated by the extractor, so these rows are
schema evidence. The skeleton and the manifest relations run through the real
engine. All fixture components are fictional.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import shutil
import subprocess

import pytest
import yaml

from tests.conftest import (
    MANIFEST_PATH,
    PACKAGE_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    engine_tool,
    field,
    frontmatter,
    object_type,
)
from tests.test_skeletons_semantic import CREDENTIAL_SHAPES, extract

PURL = "pkg:cargo/example-http-client@1.4.2"
REQ = "ix://agent-ix/other-repo/FR-100"


def record(**extra):
    base = {
        "fields": [field("component_id", "UUID", identity=True), field("purl")],
        "purl": PURL,
    }
    return {**base, **extra}


def schema() -> dict:
    return json.loads((SCHEMAS_DIR / "SoupRecord.json").read_text())


def keywords(node, found=None):
    """Every key that appears at any depth of a JSON document."""
    found = set() if found is None else found
    if isinstance(node, dict):
        for key, value in node.items():
            found.add(key)
            keywords(value, found)
    elif isinstance(node, list):
        for item in node:
            keywords(item, found)
    return found


@pytest.fixture
def validator(schema_registry):
    return schema_registry("SoupRecord")


@pytest.mark.trace("TC-121", "FR-009-AC-1")
def test_manifest_exports_soup_record_with_a_shipped_schema(quire_engine):
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert "soup_record" in manifest["semantic"]["exports"]
    soup = object_type("soup_record")
    path = PACKAGE_ROOT / soup["data_schema"]["schema"]
    assert path == SCHEMAS_DIR / "SoupRecord.json" and path.is_file()
    skeleton = (SKELETONS_DIR / "soup_record.md").read_text()
    result = quire_engine.validate_document("soup_record", str(PACKAGE_ROOT), skeleton)
    assert result["is_valid"], result["errors"]
    assert not [
        e for e in result["errors"] if "semantic.record-invalid" in e["message"]
    ]


@pytest.mark.trace("TC-122", "FR-009-AC-2")
def test_the_purl_is_required(validator):
    assert validator.is_valid(record())
    assert not validator.is_valid(
        {"fields": [field("component_id", "UUID", identity=True)]}
    )


@pytest.mark.trace("TC-124", "FR-009-AC-4", "FR-009-CON-1")
def test_a_digest_is_refused_and_a_different_purl_is_a_distinct_component(validator):
    assert not validator.is_valid(record(digest="sha256:" + "0" * 64))
    other = record(purl="pkg:cargo/example-http-client@2.0.0")
    assert validator.is_valid(other)
    assert other["purl"] != record()["purl"]
    assert "digest" not in schema()["properties"]


@pytest.mark.trace("TC-125", "FR-009-AC-5")
def test_unknown_is_a_value_and_absence_is_not_filled(validator):
    assert validator.is_valid(record(supplier="unknown"))
    for key in ("name", "version", "license"):
        assert validator.is_valid(record(**{key: "unknown"})), key
    absent = record()
    before = copy.deepcopy(absent)
    assert validator.is_valid(absent)
    assert absent == before and "supplier" not in absent
    assert "default" not in keywords(schema())


@pytest.mark.trace("TC-126", "FR-009-AC-6")
def test_license_and_license_fact_ref_are_exclusive(validator):
    fact = "ix://agent-ix/engineering-assurance/LIC-001"
    assert validator.is_valid(record(license="Apache-2.0"))
    assert validator.is_valid(record(license_fact_ref=fact))
    assert not validator.is_valid(record(license="Apache-2.0", license_fact_ref=fact))


@pytest.mark.trace("TC-127", "FR-009-AC-7")
def test_references_validate_and_finding_text_is_refused(validator):
    refs = record(
        license_fact_ref="ix://agent-ix/engineering-assurance/LIC-001",
        finding_refs=["ix://agent-ix/quoin/FIND-001"],
        inventory_ref="ix://agent-ix/example/INV-001",
    )
    assert validator.is_valid(refs)
    assert not validator.is_valid(record(finding_text="advisory prose"))
    assert not validator.is_valid(record(license_text="full text"))
    assert not validator.is_valid(record(sbom={"components": []}))


@pytest.mark.trace("TC-128", "FR-009-AC-8", "FR-009-CON-2")
def test_module_declares_no_discharges_option_or_sbom_reader():
    sources = [MANIFEST_PATH, *SKELETONS_DIR.glob("*.md")]
    sources += [p for p in PACKAGE_ROOT.glob("*.py")]
    sources += [pathlib.Path(__file__).parent.parent / "typespec" / "main.tsp"]
    for path in sources:
        text = path.read_text().lower()
        assert "discharges" not in text, path.name
        assert "sbom_reader" not in text and "parse_sbom" not in text, path.name
    assert "discharges" not in json.dumps(schema())


@pytest.mark.trace("TC-129", "FR-010-AC-1", "FR-010-CON-1")
def test_support_status_is_a_closed_four_member_enum(validator):
    enum = json.loads((SCHEMAS_DIR / "SoupSupportStatus.json").read_text())
    assert enum["enum"] == [
        "supported",
        "community_supported",
        "unsupported",
        "unknown",
    ]
    for member in enum["enum"]:
        assert validator.is_valid(record(support_status=member)), member
    assert not validator.is_valid(record(support_status="end_of_life"))


@pytest.mark.trace("TC-130", "FR-010-AC-2")
def test_empty_and_absent_known_anomalies_are_different_records(validator):
    empty, absent = record(known_anomalies=[]), record()
    assert validator.is_valid(empty) and validator.is_valid(absent)
    assert "known_anomalies" in empty and "known_anomalies" not in absent
    assert empty != absent
    stated = record(known_anomalies=[{"statement": "leaks a socket on retry"}])
    assert validator.is_valid(stated)
    assert not validator.is_valid(record(known_anomalies=[{"source_ref": REQ}]))


@pytest.mark.trace("TC-131", "FR-010-AC-3")
def test_end_of_support_is_a_calendar_date_or_unknown(validator):
    assert validator.is_valid(record(end_of_support="unknown"))
    assert validator.is_valid(record(end_of_support="2027-06-30"))
    for bad in ("soon", "2027-13-01", "2027-06-30T00:00:00Z", "UNKNOWN", ""):
        assert not validator.is_valid(record(end_of_support=bad)), bad
    assert validator.is_valid(
        record(support_status="supported", end_of_support="unknown")
    )


@pytest.mark.trace("TC-132", "FR-010-AC-4")
def test_the_schema_carries_no_default_at_any_depth():
    assert "default" not in keywords(schema())
    anomaly = json.loads((SCHEMAS_DIR / "Anomaly.json").read_text())
    assert "default" not in keywords(anomaly)


@pytest.mark.trace("TC-134", "FR-010-AC-6")
def test_a_credential_shaped_anomaly_statement_is_caught_by_the_scan():
    canary = "api_key: " + "x9Zq" * 4
    statement = {"statement": f"ships a debug build with {canary}"}
    assert any(p.search(statement["statement"]) for p in CREDENTIAL_SHAPES)
    skeleton = (SKELETONS_DIR / "soup_record.md").read_text()
    assert not any(p.search(skeleton) for p in CREDENTIAL_SHAPES)


@pytest.mark.trace("TC-135", "FR-011-AC-1")
def test_disposition_clause_must_be_non_blank(validator):
    assert validator.is_valid(record(disposition_clause="SOUP-RISK-EXAMPLE-001"))
    for blank in ("", " ", "\t\n"):
        assert not validator.is_valid(record(disposition_clause=blank)), repr(blank)


@pytest.mark.trace("TC-136", "FR-011-AC-2")
def test_absent_disposition_clause_adds_no_key(validator):
    absent = record()
    before = copy.deepcopy(absent)
    assert validator.is_valid(absent)
    assert absent == before and "disposition_clause" not in absent
    assert "disposition_clause" not in schema()["required"]


@pytest.mark.trace("TC-137", "FR-011-AC-3")
def test_an_embedded_decision_is_refused(validator):
    for key in (
        "decision",
        "rationale",
        "approvalRef",
        "approval_ref",
        "attestation",
        "approver",
        "expires",
    ):
        assert not validator.is_valid(record(**{key: "x"})), key
        assert key not in schema()["properties"], key


@pytest.mark.trace("TC-139", "FR-011-AC-5")
def test_disposition_clause_changes_no_other_key(validator):
    plain = record(support_status="supported", serves=[REQ])
    clause = {**plain, "disposition_clause": "SOUP-RISK-EXAMPLE-001"}
    assert validator.is_valid(plain) and validator.is_valid(clause)
    stripped = {k: v for k, v in clause.items() if k != "disposition_clause"}
    assert stripped == plain


@pytest.mark.trace("TC-143", "FR-012-AC-4")
def test_advisory_keys_are_refused(validator):
    for key, value in (
        ("severity", "high"),
        ("cve_id", "CVE-2026-00000"),
        ("advisories", ["CVE-2026-00000"]),
    ):
        assert not validator.is_valid(record(**{key: value})), key


@pytest.mark.trace("TC-144", "NFR-001-AC-1")
def test_no_score_rating_class_tier_or_level_property():
    doc = schema()
    banned = {"score", "rating", "class", "tier", "level", "grade", "rank"}
    for name in doc["properties"]:
        assert not banned & set(name.lower().split("_")), name
    text = json.dumps(doc)
    for vocabulary in ("Severity", "Likelihood", "Impact"):
        assert f"/{vocabulary}.json" not in text, vocabulary


@pytest.mark.trace("TC-145", "NFR-001-AC-2")
def test_a_validated_fixture_emits_exactly_the_keys_written(
    validator, quire_engine, semantic_module, bundle_index
):
    written = record(supplier="unknown", serves=[REQ], known_anomalies=[])
    before = copy.deepcopy(written)
    assert validator.is_valid(written)
    assert written == before
    extracted = extract(
        quire_engine, semantic_module, bundle_index, SKELETONS_DIR / "soup_record.md"
    )
    assert [f["name"] for f in extracted["fields"]] == [
        "component_id",
        "purl",
        "supplier",
    ]
    for key in (
        "serves",
        "known_anomalies",
        "support_status",
        "end_of_support",
        "disposition_clause",
        "license",
    ):
        assert key not in extracted, key


# -- FR-012: the vulnerability affects edge (engine) --------------------------


def _iso() -> pathlib.Path:
    spec = importlib.util.find_spec("spec_artifacts_iso")
    if spec is None or not spec.origin:
        pytest.fail("spec-artifacts-iso is not installed; run `poetry install`")
    return pathlib.Path(spec.origin).parent


def _validate(root):
    return subprocess.run(
        [
            engine_tool("quire"),
            "validate",
            "--okf",
            "--module",
            str(_iso()),
            "--module",
            str(PACKAGE_ROOT),
            str(root),
        ],
        capture_output=True,
        text=True,
    )


def _vulnerability_affecting(root, target):
    text = (SKELETONS_DIR / "vulnerability.md").read_text()
    text = text.replace(
        "severity: high\n",
        f"severity: high\nrelationships:\n  - target: {target}\n    type: affects\n",
        1,
    )
    (root / "vulnerability.md").write_text(text)


@pytest.mark.trace("TC-140", "FR-012-AC-1")
def test_vulnerability_affects_lists_soup_record_and_soup_declares_no_links():
    vulnerability = object_type("vulnerability")
    assert vulnerability["allowed_links"]["affects"] == [
        "asset",
        "attack_surface",
        "soup_record",
    ]
    assert "allowed_links" not in object_type("soup_record")
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    required = manifest["traceability"]["required_relations"]
    assert not [r for r in required if r["from"] == "soup_record"]
    assert "required_relations" not in vulnerability


@pytest.mark.trace("TC-141", "FR-012-AC-2")
def test_affects_edge_to_soup_validates_and_to_a_threat_is_disallowed(tmp_path):
    shutil.copy(SKELETONS_DIR / "soup_record.md", tmp_path / "soup.md")
    shutil.copy(SKELETONS_DIR / "threat.md", tmp_path / "threat.md")
    soup_id = frontmatter((SKELETONS_DIR / "soup_record.md").read_text())["id"]
    threat_id = frontmatter((SKELETONS_DIR / "threat.md").read_text())["id"]

    _vulnerability_affecting(tmp_path, soup_id)
    ok = _validate(tmp_path)
    assert ok.returncode == 0, ok.stderr
    assert "disallowed-edge-target" not in ok.stderr, ok.stderr
    assert "UnknownEdgeType: archetype 'vulnerability'" not in ok.stderr, ok.stderr

    _vulnerability_affecting(tmp_path, threat_id)
    bad = [
        line
        for line in _validate(tmp_path).stderr.splitlines()
        if line.endswith("[disallowed-edge-target]")
    ]
    assert len(bad) == 1, bad
    assert "(object type 'threat')" in bad[0], bad[0]


@pytest.mark.trace("TC-142", "FR-012-AC-3")
def test_a_soup_record_no_vulnerability_affects_has_no_finding(tmp_path):
    shutil.copy(SKELETONS_DIR / "soup_record.md", tmp_path / "soup.md")
    result = _validate(tmp_path)
    assert result.returncode == 0, result.stderr
    soup_id = frontmatter((SKELETONS_DIR / "soup_record.md").read_text())["id"]
    assert not [line for line in result.stderr.splitlines() if soup_id in line]
