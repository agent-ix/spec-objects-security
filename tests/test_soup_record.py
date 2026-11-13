"""The `soup_record` object type: identity, fields, disposition and relations.

Two kinds of evidence are kept apart. Hand-built declaration records, as in
`test_role_schemas.py`, are schema evidence: the keys beyond `fields` are not
populated by the extractor. Committed documents under `tests/fixtures/soup/`
go through the real engine. The engine does not yet validate or project the
frontmatter record keys of an authored document against the data schema, so
every test that needs that is a strict expected failure naming the missing
engine behaviour. All fixture components are fictional.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import re
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

FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "soup"
PURL = "pkg:cargo/example-http-client@1.4.2"
REQ = "ix://agent-ix/other-repo/FR-100"


def record(**extra):
    base = {
        "fields": [field("component_id", "UUID", identity=True), field("purl")],
        "purl": PURL,
    }
    return {**base, **extra}


def full_fixture() -> str:
    return (FIXTURES / "full.md").read_text()


def with_frontmatter(text: str, **keys) -> str:
    """The document with each key set in its frontmatter, replacing any value."""
    for key, value in keys.items():
        text = re.sub(rf"^{key}: .*\n", "", text, count=1, flags=re.M)
        text = text.replace("\n---\n#", f"\n{key}: {value}\n---\n#", 1)
    return text


def validate_doc(quire_engine, text: str) -> dict:
    return quire_engine.validate_document("soup_record", str(PACKAGE_ROOT), text)


def extract_doc(quire_engine, semantic_module, bundle_index, text, tmp_path):
    path = tmp_path / "doc.md"
    path.write_text(text)
    return extract(quire_engine, semantic_module, bundle_index, path)


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
    full = validate_doc(quire_engine, full_fixture())
    assert full["is_valid"], full["errors"]


@pytest.mark.trace("TC-122", "FR-009-AC-2")
def test_the_purl_is_required_as_a_frontmatter_key_and_as_a_field_row(
    validator, quire_engine
):
    assert validator.is_valid(record())
    # Schema half: the top-level key does not stand in for the row.
    identity = [field("component_id", "UUID", identity=True)]
    assert not validator.is_valid({"fields": identity, "purl": PURL})
    assert not validator.is_valid({"fields": identity})
    # Document half: the frontmatter key and the Properties row are each required.
    full = full_fixture()
    no_key = validate_doc(quire_engine, re.sub(r"^purl: .*\n", "", full, flags=re.M))
    assert not no_key["is_valid"]
    assert any("purl" in e["message"] for e in no_key["errors"]), no_key["errors"]
    row = "| purl | String | 1..1 | minLength: 1 |\n"
    no_row = validate_doc(quire_engine, full.replace(row, ""))
    assert not no_row["is_valid"]
    assert any("semantic.record-invalid" in e["message"] for e in no_row["errors"])


@pytest.mark.trace("TC-124", "FR-009-AC-4", "FR-009-CON-1")
def test_a_digest_is_refused_and_a_different_purl_is_a_distinct_component(
    validator, quire_engine
):
    assert not validator.is_valid(record(digest="sha256:" + "0" * 64))
    assert "digest" not in schema()["properties"]
    other = with_frontmatter(
        full_fixture(), purl='"pkg:cargo/example-parser-lib@3.0.0"'
    )
    assert validate_doc(quire_engine, other)["is_valid"]


@pytest.mark.trace("TC-125", "FR-009-AC-5")
def test_unknown_is_a_value_and_absence_is_not_filled(validator):
    assert validator.is_valid(record(supplier="unknown"))
    for key in ("name", "version", "license"):
        assert validator.is_valid(record(**{key: "unknown"})), key
    assert validator.is_valid(record())
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
def test_empty_and_absent_known_anomalies_both_validate(validator):
    assert validator.is_valid(record(known_anomalies=[]))
    assert validator.is_valid(record())
    stated = record(known_anomalies=[{"statement": "leaks a socket on retry"}])
    assert validator.is_valid(stated)
    assert not validator.is_valid(record(known_anomalies=[{"source_ref": REQ}]))


@pytest.mark.trace("TC-131", "FR-010-AC-3")
def test_end_of_support_is_a_calendar_date_or_unknown(validator):
    assert validator.is_valid(record(end_of_support="unknown"))
    assert validator.is_valid(record(end_of_support="2027-06-30"))
    assert validator.is_valid(record(end_of_support="2028-02-29"))
    for bad in (
        "soon",
        "2027-02-31",
        "2027-02-29",
        "2027-04-31",
        "2027-13-01",
        "2027-06-30T00:00:00Z",
        "UNKNOWN",
        "",
    ):
        assert not validator.is_valid(record(end_of_support=bad)), bad
    assert validator.is_valid(
        record(support_status="supported", end_of_support="unknown")
    )


@pytest.mark.trace("TC-132", "FR-010-AC-4")
def test_the_schema_carries_no_default_at_any_depth():
    assert "default" not in keywords(schema())
    anomaly = json.loads((SCHEMAS_DIR / "Anomaly.json").read_text())
    assert "default" not in keywords(anomaly)


def anomaly_statements(text: str) -> list[str]:
    anomalies = frontmatter(text).get("known_anomalies") or []
    return [a["statement"] for a in anomalies]


def credential_hits(text: str) -> list[str]:
    return [
        statement
        for statement in anomaly_statements(text)
        if any(p.search(statement) for p in CREDENTIAL_SHAPES)
    ]


@pytest.mark.trace("TC-134", "FR-010-AC-6")
def test_the_scan_refuses_a_credential_shaped_anomaly_statement():
    clean = full_fixture()
    assert anomaly_statements(clean), "the fixture must carry an anomaly statement"
    assert credential_hits(clean) == []
    canary = "api_key: " + "x9Zq" * 4
    dirty = clean.replace(
        "Rejects inputs over 16 MiB without an error code.",
        f"Ships a debug build with {canary}",
    )
    assert credential_hits(dirty) == [f"Ships a debug build with {canary}"]


@pytest.mark.trace("TC-135", "FR-011-AC-1")
def test_disposition_clause_must_be_non_blank(validator):
    assert validator.is_valid(record(disposition_clause="SOUP-RISK-EXAMPLE-001"))
    for blank in ("", " ", "\t\n"):
        assert not validator.is_valid(record(disposition_clause=blank)), repr(blank)


@pytest.mark.trace("TC-136", "FR-011-AC-2")
def test_absent_disposition_clause_adds_no_key(
    validator, quire_engine, semantic_module, bundle_index, tmp_path
):
    assert validator.is_valid(record())
    assert "disposition_clause" not in schema()["required"]
    text = re.sub(r"^disposition_clause: .*\n", "", full_fixture(), flags=re.M)
    assert validate_doc(quire_engine, text)["is_valid"]
    extracted = extract_doc(quire_engine, semantic_module, bundle_index, text, tmp_path)
    assert "disposition_clause" not in extracted


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
def test_disposition_clause_changes_no_other_key(validator, quire_engine):
    plain = record(support_status="supported")
    assert validator.is_valid(plain)
    assert validator.is_valid({**plain, "disposition_clause": "SOUP-RISK-EXAMPLE-001"})
    full = full_fixture()
    other = with_frontmatter(full, disposition_clause="SOUP-RISK-EXAMPLE-099")
    assert validate_doc(quire_engine, full)["is_valid"]
    assert validate_doc(quire_engine, other)["is_valid"]


@pytest.mark.trace("TC-143", "FR-012-AC-4")
def test_advisory_keys_are_refused(validator):
    for key, value in (
        ("severity", "high"),
        ("cve_id", "CVE-2026-00000"),
        ("advisories", ["CVE-2026-00000"]),
    ):
        assert not validator.is_valid(record(**{key: value})), key


@pytest.mark.trace("TC-144", "NFR-001-AC-1", "NFR-001-M-1")
def test_no_score_rating_class_tier_or_level_property():
    doc = schema()
    banned = {"score", "rating", "class", "tier", "level", "grade", "rank"}
    for name in doc["properties"]:
        assert not banned & set(name.lower().split("_")), name
    text = json.dumps(doc)
    for vocabulary in ("Severity", "Likelihood", "Impact"):
        assert f"/{vocabulary}.json" not in text, vocabulary


@pytest.mark.trace("TC-145", "NFR-001-AC-2", "NFR-001-M-2")
def test_a_validated_fixture_emits_exactly_the_keys_written(
    validator, quire_engine, semantic_module, bundle_index
):
    written = record(supplier="unknown", known_anomalies=[])
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


def _validate(root, *flags):
    return subprocess.run(
        [
            engine_tool("quire"),
            "validate",
            "--okf",
            *flags,
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
    assert list(object_type("soup_record")["allowed_links"]) == ["supports"]
    assert "required_relations" not in vulnerability


@pytest.mark.trace("TC-141", "FR-012-AC-2")
def test_affects_edge_to_soup_validates_and_to_a_threat_is_disallowed(
    tmp_path, quire_engine
):
    shutil.copy(SKELETONS_DIR / "soup_record.md", tmp_path / "soup.md")
    shutil.copy(SKELETONS_DIR / "threat.md", tmp_path / "threat.md")
    soup_text = (SKELETONS_DIR / "soup_record.md").read_text()
    assert validate_doc(quire_engine, soup_text)["is_valid"]
    soup_id = frontmatter(soup_text)["id"]
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
def test_a_soup_record_no_vulnerability_affects_has_no_finding(tmp_path, quire_engine):
    # Directory mode skips record keys, so the record is checked on its own too.
    assert validate_doc(quire_engine, full_fixture())["is_valid"]
    shutil.copy(SKELETONS_DIR / "soup_record.md", tmp_path / "soup.md")
    result = _validate(tmp_path)
    assert result.returncode == 0, result.stderr
    soup_id = frontmatter((SKELETONS_DIR / "soup_record.md").read_text())["id"]
    assert not [
        line
        for line in result.stderr.splitlines()
        if soup_id in line and CHECK not in line
    ]


# -- Engine gaps ---------------------------------------------------------------
#
# Each test below states the behaviour the spec requires and fails today. They
# are strict expected failures so the day the engine supplies the behaviour the
# rows turn red and are noticed.

ENGINE_RECORD_KEYS = (
    "The engine does not validate the frontmatter record keys of an authored "
    "document against the data schema."
)
ENGINE_PROJECTION = (
    "The engine does not project the frontmatter record keys of an authored "
    "document into the extracted record."
)


def refused_document(quire_engine, **keys) -> bool:
    bogus = with_frontmatter(full_fixture(), **keys)
    return not validate_doc(quire_engine, bogus)["is_valid"]


@pytest.mark.xfail(strict=True, reason=ENGINE_RECORD_KEYS)
@pytest.mark.trace("TC-129", "FR-010-AC-1")
def test_an_authored_document_with_an_invented_support_status_fails(quire_engine):
    assert refused_document(quire_engine, support_status="bogus_status")


@pytest.mark.xfail(strict=True, reason=ENGINE_RECORD_KEYS)
@pytest.mark.trace("TC-131", "FR-010-AC-3")
def test_an_authored_document_with_a_bad_end_of_support_fails(quire_engine):
    assert refused_document(quire_engine, end_of_support="soon")


@pytest.mark.xfail(strict=True, reason=ENGINE_RECORD_KEYS)
@pytest.mark.trace("TC-124", "FR-009-AC-4")
def test_an_authored_document_with_a_digest_fails(quire_engine):
    assert refused_document(quire_engine, digest='"sha256:00"')


@pytest.mark.xfail(strict=True, reason=ENGINE_RECORD_KEYS)
@pytest.mark.trace("TC-143", "FR-012-AC-4")
def test_an_authored_document_with_a_severity_fails(quire_engine):
    assert refused_document(quire_engine, severity="high")


@pytest.mark.xfail(strict=True, reason=ENGINE_PROJECTION)
@pytest.mark.trace("TC-130", "FR-010-AC-2")
def test_an_empty_known_anomalies_is_emitted_and_an_absent_one_is_not(
    quire_engine, semantic_module, bundle_index, tmp_path
):
    full = full_fixture()
    empty = re.sub(r"known_anomalies:\n(  .*\n)+", "known_anomalies: []\n", full)
    absent = re.sub(r"known_anomalies:\n(  .*\n)+", "", full)
    emitted = extract_doc(quire_engine, semantic_module, bundle_index, empty, tmp_path)
    omitted = extract_doc(quire_engine, semantic_module, bundle_index, absent, tmp_path)
    assert emitted["known_anomalies"] == []
    assert "known_anomalies" not in omitted


@pytest.mark.xfail(strict=True, reason=ENGINE_PROJECTION)
@pytest.mark.trace("TC-125", "FR-009-AC-5")
def test_unknown_supplier_is_emitted_and_an_omitted_supplier_is_not(
    quire_engine, semantic_module, bundle_index, tmp_path
):
    full = full_fixture()
    omitted = re.sub(r"^supplier: .*\n", "", full, flags=re.M)
    stated = extract_doc(quire_engine, semantic_module, bundle_index, full, tmp_path)
    left_out = extract_doc(
        quire_engine, semantic_module, bundle_index, omitted, tmp_path
    )
    assert stated["supplier"] == "unknown"
    assert "supplier" not in left_out


@pytest.mark.xfail(strict=True, reason=ENGINE_PROJECTION)
@pytest.mark.trace("TC-139", "FR-011-AC-5")
def test_disposition_clause_is_emitted_and_changes_no_other_key(
    quire_engine, semantic_module, bundle_index, tmp_path
):
    full = full_fixture()
    plain = re.sub(r"^disposition_clause: .*\n", "", full, flags=re.M)
    with_clause = extract_doc(
        quire_engine, semantic_module, bundle_index, full, tmp_path
    )
    without = extract_doc(quire_engine, semantic_module, bundle_index, plain, tmp_path)
    assert with_clause["disposition_clause"] == "SOUP-RISK-EXAMPLE-010"
    assert {
        k: v for k, v in with_clause.items() if k != "disposition_clause"
    } == without


@pytest.mark.xfail(
    strict=True,
    reason="The engine has no identity-uniqueness check over a frontmatter key.",
)
@pytest.mark.trace("TC-123", "FR-009-AC-3")
def test_two_documents_with_one_purl_yield_one_duplicate_identity_report(tmp_path):
    full = full_fixture()
    (tmp_path / "a.md").write_text(full)
    (tmp_path / "b.md").write_text(full.replace("SOUP-010", "SOUP-020"))
    result = _validate(tmp_path)
    reports = [
        line
        for line in result.stderr.splitlines()
        if "purl" in line and "SOUP-010" in line and "SOUP-020" in line
    ]
    assert len(reports) == 1, result.stderr


CHECK = "soup-serves-no-requirement"
SERVED = FIXTURES / "served.md"


def _requirement(root, req_id="FR-100"):
    """An FR from the installed iso skeleton, standing in for the served requirement."""
    text = (_iso() / "skeletons" / "fr.md").read_text().replace("FR-001", req_id)
    (root / f"{req_id}.md").write_text(text)


def _findings(result):
    return [line for line in result.stderr.splitlines() if line.endswith(f"[{CHECK}]")]


@pytest.mark.trace("TC-150", "FR-013-AC-1")
def test_supports_link_and_required_relation_are_declared():
    assert object_type("soup_record")["allowed_links"] == {
        "supports": ["FR", "NFR", "StR"]
    }
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    relations = manifest["traceability"]["required_relations"]
    (relation,) = [r for r in relations if r["from"] == "soup_record"]
    assert relation == {
        "name": "soup-record-serves-requirement",
        "from": "soup_record",
        "edges": ["supports"],
        "to": ["FR", "NFR", "StR"],
        "direction": "outgoing",
        "check": CHECK,
    }


@pytest.mark.trace("TC-151", "FR-013-AC-2")
def test_record_with_no_supports_edge_is_reported_by_name(tmp_path):
    _requirement(tmp_path)
    (tmp_path / "soup.md").write_text(full_fixture())
    result = _validate(tmp_path)
    assert result.returncode == 0, result.stderr
    findings = _findings(result)
    assert len(findings) == 1 and "SOUP-010" in findings[0], result.stderr


@pytest.mark.trace("TC-152", "FR-013-AC-3")
def test_record_with_a_supports_edge_is_not_reported(tmp_path):
    _requirement(tmp_path)
    (tmp_path / "soup.md").write_text(SERVED.read_text())
    result = _validate(tmp_path)
    assert result.returncode == 0, result.stderr
    assert _findings(result) == [], result.stderr
    # `supports` is a registered verb: loading the module reports no unknown edge.
    # The verb must come from the iso edge registry, not be invented here.
    registry = yaml.safe_load((_iso() / "manifest.yaml").read_text())["edge_types"]
    assert set(object_type("soup_record")["allowed_links"]) <= set(registry)


@pytest.mark.trace("TC-153", "FR-013-AC-4")
def test_supports_edge_to_another_kind_or_nothing_is_still_reported(tmp_path):
    shutil.copy(SKELETONS_DIR / "threat.md", tmp_path / "threat.md")
    threat_id = frontmatter((SKELETONS_DIR / "threat.md").read_text())["id"]
    text = SERVED.read_text().replace(
        'spec-objects-security/FR-100"\n    type: supports',
        f'spec-objects-security/{threat_id}"\n    type: supports',
    )
    assert text != SERVED.read_text(), "the relationship was not rewritten"
    assert threat_id in text
    (tmp_path / "soup.md").write_text(text)
    assert len(_findings(_validate(tmp_path))) == 1
    # No FR-100 in the bundle: the target resolves to nothing.
    (tmp_path / "soup.md").write_text(SERVED.read_text())
    assert len(_findings(_validate(tmp_path))) == 1


@pytest.mark.trace("TC-154", "FR-013-AC-5")
def test_finding_is_advisory_and_tunable(tmp_path):
    (tmp_path / "soup.md").write_text(full_fixture())
    plain = _validate(tmp_path)
    assert _findings(plain)[0].startswith("warning:"), plain.stderr
    promoted = _validate(tmp_path, "--severity", f"trace:{CHECK}=error")
    assert promoted.returncode != 0, promoted.stderr
    assert len(_findings(promoted)) == 1, promoted.stderr


@pytest.mark.trace("TC-155", "FR-013-AC-6")
def test_skeleton_carries_no_edge_and_extract_lists_the_authored_one():
    assert "relationships" not in frontmatter(
        (SKELETONS_DIR / "soup_record.md").read_text()
    )
    out = subprocess.run(
        [engine_tool("quire"), "extract", "--module", str(PACKAGE_ROOT), str(SERVED)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    edges = json.loads(out)["edges"]
    assert {"target": "FR-100", "type": "supports"} in edges, edges


def test_the_worked_disposition_example_pairs_a_record_with_a_fact(quire_engine):
    text = (FIXTURES / "disposition-example.md").read_text()
    front = frontmatter(text)
    assert validate_doc(quire_engine, text)["is_valid"]
    fact = json.loads(re.search(r"```json\n(.*?)\n```", text, re.DOTALL).group(1))
    assert fact["kind"] == "disposition"
    assert fact["clauseId"] == front["disposition_clause"]
    assert fact["attestation"]["attestedBy"] and fact["attestation"]["authority"]
