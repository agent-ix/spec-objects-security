"""FR-030: a requirement a SOUP record serves is asked for its SOUP requirements.

The manifest declares the verb, the two relations and the design-relation names
as data. Every behavioural row runs the real `quire` CLI over a fixture corpus
built in `tmp_path`: requirements come from the installed `spec-artifacts-iso`
skeletons, the `soup_record` and `threat` from this module's own fixtures and
skeletons. Nothing is copied from another repository.
"""

from __future__ import annotations

import json
import re
import subprocess

import pytest
import yaml

from tests.conftest import (
    MANIFEST_PATH,
    PACKAGE_ROOT,
    SKELETONS_DIR,
    engine_tool,
    iso_module_path,
    object_type,
    validation_module_args,
)

FIXTURES = PACKAGE_ROOT.parent / "tests" / "fixtures" / "soup"
SERVED = FIXTURES / "served.md"
OWNER = "ix://agent-ix/spec-objects-security"
FR_RELATION = "fr-has-soup-requirements"
NFR_RELATION = "nfr-has-soup-requirements"
FR_CHECK = "fr-without-soup-requirements"
NFR_CHECK = "nfr-without-soup-requirements"
VERB = "soup_requirement_for"
INVERSE = "has_soup_requirement"
WHEN_ANY = [{"verb": "references", "direction": "incoming", "other": ["soup_record"]}]


def _manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text())


def _relations() -> dict[str, dict]:
    return {r["name"]: r for r in _manifest()["traceability"]["required_relations"]}


def _edges(edges) -> str:
    return "".join(
        f'  - target: "{OWNER}/{target}"\n    type: "{verb}"\n'
        for verb, target in edges
    )


def _requirement(root, kind, doc_id, edges=()):
    """An FR or NFR from the iso skeleton whose relationships are exactly `edges`."""
    text = (iso_module_path() / "skeletons" / f"{kind.lower()}.md").read_text()
    text = text.replace(f"{kind}-001", doc_id)
    block = _edges(edges)
    relationships = f"relationships:\n{block}" if block else ""
    text = re.sub(r"relationships:\n(?:  .*\n)+", relationships, text, count=1)
    (root / "spec").mkdir(parents=True, exist_ok=True)
    (root / "spec" / f"{doc_id}.md").write_text(text)


def _soup(root, serves=(), body_links=()):
    """The served record listing exactly `serves`, body-linking `body_links`."""
    text = SERVED.read_text()
    entries = "".join(f"  - {OWNER}/{target}\n" for target in serves)
    serves_block = f"serves:\n{entries}" if entries else ""
    text = re.sub(r"serves:\n(  - .*\n)+", serves_block, text, count=1)
    links = "".join(f"\nSee [{t}]({OWNER}/{t}).\n" for t in body_links)
    (root / "spec").mkdir(parents=True, exist_ok=True)
    (root / "spec" / "soup.md").write_text(text + links)


def _threat(root, edges=()):
    text = (SKELETONS_DIR / "threat.md").read_text()
    block = _edges(edges)
    text = text.replace("\n---\n<!--", f"\nrelationships:\n{block}---\n<!--", 1)
    (root / "spec").mkdir(parents=True, exist_ok=True)
    (root / "spec" / "THREAT-001.md").write_text(text)


def _modules() -> list[str]:
    """iso, then architecture, then this module: the order FR-030-AC-11 reads."""
    iso, security, architecture = [
        arg
        for arg in validation_module_args(PACKAGE_ROOT, include_iso=True)
        if arg != "--module"
    ]
    return ["--module", iso, "--module", architecture, "--module", security]


def _quire(*args):
    return subprocess.run([engine_tool("quire"), *args], capture_output=True, text=True)


def _validate(root, *flags):
    return _quire("validate", "--okf", *flags, *_modules(), str(root / "spec"))


def _disallowed(path):
    """Single-file validation: the only mode that reports `disallowed-edge-type`."""
    result = _quire("validate", *_modules(), str(path))
    return [ln for ln in result.stderr.splitlines() if "disallowed-edge-type" in ln]


def _report(root, *extra):
    result = _quire("relations", "--json", *extra, *_modules(), "--scope", str(root))
    assert result.returncode == 0, result.stderr
    rows = {}
    for relation in json.loads(result.stdout)["relations"]:
        for row in relation["rows"]:
            rows[(relation["name"], row["document"]["id"])] = row
    return rows


def _linked(row):
    return [(e["id"], e["archetype"]) for e in row["linked"]]


def _findings(result, check):
    return [line for line in result.stderr.splitlines() if line.endswith(f"[{check}]")]


def _rows_of(rows, relation):
    return sorted(doc for (name, doc) in rows if name == relation)


@pytest.mark.trace("FR-030-AC-1")
def test_manifest_declares_the_verb_the_relations_and_the_design_names(tmp_path):
    manifest = _manifest()
    verb = manifest["edge_types"][VERB]
    assert verb["inverse"] == INVERSE and verb["category"] == "traceability"
    relations = _relations()
    for name, kind, check in (
        (FR_RELATION, "FR", FR_CHECK),
        (NFR_RELATION, "NFR", NFR_CHECK),
    ):
        assert relations[name] == {
            "name": name,
            "from": kind,
            "edges": [VERB],
            "to": ["FR", "NFR"],
            "direction": "incoming",
            "check": check,
            "when_any": WHEN_ANY,
        }
    assert manifest["traceability"]["design_relations"] == [FR_RELATION, NFR_RELATION]
    # The module loads under the engine beside iso and architecture without a
    # declaration error, and the two relations are read by the engine.
    _requirement(tmp_path, "FR", "FR-100")
    result = _quire("relations", "--json", *_modules(), "--scope", str(tmp_path))
    assert result.returncode == 0, result.stderr
    assert "DuplicateEdgeType" not in result.stderr, result.stderr
    names = [r["name"] for r in json.loads(result.stdout)["relations"]]
    assert FR_RELATION in names and NFR_RELATION in names


@pytest.mark.trace("FR-030-AC-2")
def test_served_fr_without_a_statement_is_uncovered_and_reported(tmp_path):
    _soup(tmp_path, serves=["FR-100"])
    _requirement(tmp_path, "FR", "FR-100")
    row = _report(tmp_path)[(FR_RELATION, "FR-100")]
    assert row["state"] == "uncovered" and row["linked"] == []
    result = _validate(tmp_path)
    assert result.returncode == 0, result.stderr
    findings = _findings(result, FR_CHECK)
    assert len(findings) == 1 and "FR-100" in findings[0], result.stderr


@pytest.mark.trace("FR-030-AC-3")
def test_a_statement_or_the_inverse_covers_the_served_fr(tmp_path):
    _soup(tmp_path, serves=["FR-100"])
    _requirement(tmp_path, "FR", "FR-100")
    _requirement(tmp_path, "FR", "FR-200", [(VERB, "FR-100")])
    row = _report(tmp_path)[(FR_RELATION, "FR-100")]
    assert row["state"] == "covered" and _linked(row) == [("FR-200", "FR")]
    result = _validate(tmp_path)
    assert _findings(result, FR_CHECK) == [], result.stderr
    # The served requirement authors the inverse toward the statement instead.
    inverse = tmp_path / "inverse"
    _soup(inverse, serves=["FR-100"])
    _requirement(inverse, "FR", "FR-100", [(INVERSE, "FR-200")])
    _requirement(inverse, "FR", "FR-200")
    row = _report(inverse)[(FR_RELATION, "FR-100")]
    assert row["state"] == "covered" and _linked(row) == [("FR-200", "FR")]
    result = _validate(inverse)
    assert _findings(result, FR_CHECK) == [], result.stderr
    assert _disallowed(inverse / "spec" / "FR-100.md") == []
    # The control: a verb outside the allowance is still reported by that mode.
    _requirement(inverse, "FR", "FR-300", [("blocks", "FR-100")])
    assert _disallowed(inverse / "spec" / "FR-300.md")


@pytest.mark.trace("FR-030-AC-4")
def test_requirements_no_record_serves_yield_no_row_and_no_finding(tmp_path):
    _requirement(tmp_path, "FR", "FR-100")
    _requirement(tmp_path, "NFR", "NFR-100")
    _soup(tmp_path, serves=["FR-300"])
    _requirement(tmp_path, "FR", "FR-300")
    rows = _report(tmp_path)
    for relation in (FR_RELATION, NFR_RELATION):
        assert not {"FR-100", "NFR-100"} & set(_rows_of(rows, relation))
    result = _validate(tmp_path)
    assert all(
        "FR-100" not in line and "NFR-100" not in line
        for check in (FR_CHECK, NFR_CHECK)
        for line in _findings(result, check)
    ), result.stderr
    # The control: the served requirement is the only row.
    assert _rows_of(rows, FR_RELATION) == ["FR-300"]


@pytest.mark.trace("FR-030-AC-5")
def test_only_the_verb_from_an_fr_or_nfr_covers_the_served_requirement(tmp_path):
    for verb in ("references", "satisfies"):
        root = tmp_path / verb
        _soup(root, serves=["FR-100"])
        _requirement(root, "FR", "FR-100")
        _requirement(root, "FR", "FR-200", [(verb, "FR-100")])
        row = _report(root)[(FR_RELATION, "FR-100")]
        assert row["state"] == "uncovered", verb
    other = tmp_path / "other-kind"
    _soup(other, serves=["FR-100"])
    _requirement(other, "FR", "FR-100")
    _threat(other, [(VERB, "FR-100")])
    assert _report(other)[(FR_RELATION, "FR-100")]["state"] == "uncovered"
    nfr = tmp_path / "nfr-statement"
    _soup(nfr, serves=["FR-100"])
    _requirement(nfr, "FR", "FR-100")
    _requirement(nfr, "NFR", "NFR-200", [(VERB, "FR-100")])
    row = _report(nfr)[(FR_RELATION, "FR-100")]
    assert row["state"] == "covered" and _linked(row) == [("NFR-200", "NFR")]


@pytest.mark.trace("FR-030-AC-6")
def test_the_fr_finding_is_a_tunable_warning(tmp_path):
    _soup(tmp_path, serves=["FR-100"])
    _requirement(tmp_path, "FR", "FR-100")
    plain = _validate(tmp_path)
    assert _findings(plain, FR_CHECK)[0].startswith("warning:"), plain.stderr
    promoted = _validate(tmp_path, "--severity", f"trace:{FR_CHECK}=error")
    assert promoted.returncode != 0, promoted.stderr
    assert len(_findings(promoted, FR_CHECK)) == 1, promoted.stderr
    off = _validate(tmp_path, "--severity", f"trace:{FR_CHECK}=off")
    assert _findings(off, FR_CHECK) == [], off.stderr


@pytest.mark.trace("FR-030-AC-7")
def test_the_serves_relation_keeps_its_declaration_and_stays_out_of_design():
    assert "allowed_links" not in object_type("soup_record")
    manifest = _manifest()
    assert _relations()["soup-record-serves-requirement"] == {
        "name": "soup-record-serves-requirement",
        "from": "soup_record",
        "edges": ["references"],
        "to": ["FR", "NFR", "StR"],
        "direction": "outgoing",
        "check": "soup-serves-no-requirement",
    }
    assert "soup-record-serves-requirement" not in (
        manifest["traceability"]["design_relations"]
    )


@pytest.mark.trace("FR-030-AC-9")
def test_served_nfr_is_covered_by_a_statement_and_its_finding_is_tunable(tmp_path):
    _soup(tmp_path, serves=["NFR-100"])
    _requirement(tmp_path, "NFR", "NFR-100")
    row = _report(tmp_path)[(NFR_RELATION, "NFR-100")]
    assert row["state"] == "uncovered"
    plain = _validate(tmp_path)
    findings = _findings(plain, NFR_CHECK)
    assert len(findings) == 1 and "NFR-100" in findings[0], plain.stderr
    assert findings[0].startswith("warning:") and plain.returncode == 0, plain.stderr
    promoted = _validate(tmp_path, "--severity", f"trace:{NFR_CHECK}=error")
    assert promoted.returncode != 0, promoted.stderr
    off = _validate(tmp_path, "--severity", f"trace:{NFR_CHECK}=off")
    assert _findings(off, NFR_CHECK) == [], off.stderr
    for kind, doc_id in (("FR", "FR-200"), ("NFR", "NFR-200")):
        root = tmp_path / doc_id
        _soup(root, serves=["NFR-100"])
        _requirement(root, "NFR", "NFR-100")
        _requirement(root, kind, doc_id, [(VERB, "NFR-100")])
        row = _report(root)[(NFR_RELATION, "NFR-100")]
        assert row["state"] == "covered" and _linked(row) == [(doc_id, kind)]
        assert _findings(_validate(root), NFR_CHECK) == []


@pytest.mark.trace("FR-030-AC-10")
def test_a_body_link_from_a_record_puts_the_requirement_in_scope(tmp_path):
    _soup(tmp_path, serves=["FR-100"], body_links=["FR-300"])
    _requirement(tmp_path, "FR", "FR-100")
    _requirement(tmp_path, "FR", "FR-300")
    row = _report(tmp_path)[(FR_RELATION, "FR-300")]
    assert row["state"] == "uncovered"
    _requirement(tmp_path, "FR", "FR-400", [(VERB, "FR-300")])
    assert _report(tmp_path)[(FR_RELATION, "FR-300")]["state"] == "covered"
    # The control: without the body link FR-300 is outside the scope.
    plain = tmp_path / "plain"
    _soup(plain, serves=["FR-100"])
    _requirement(plain, "FR", "FR-100")
    _requirement(plain, "FR", "FR-300")
    assert "FR-300" not in _rows_of(_report(plain), FR_RELATION)


@pytest.mark.trace("FR-030-AC-11")
def test_the_design_join_lists_the_relations_after_earlier_modules_and_gates(tmp_path):
    _soup(tmp_path, serves=["FR-100"])
    _requirement(tmp_path, "FR", "FR-100")
    _requirement(tmp_path, "FR", "FR-500")
    design = _quire(
        "relations", "--design", "--json", *_modules(), "--scope", str(tmp_path)
    )
    assert design.returncode == 0, design.stderr
    names = [r["name"] for r in json.loads(design.stdout)["relations"]]
    # iso and architecture load before this module, so its two relations come last.
    assert names[-2:] == [FR_RELATION, NFR_RELATION], names
    assert len(names) > 2
    matrix = _quire("matrix", "--strict", *_modules(), "--scope", str(tmp_path))
    assert matrix.returncode == 1, matrix.stderr
    gap = [ln for ln in matrix.stderr.splitlines() if "FR-100" in ln and FR_CHECK in ln]
    assert gap, matrix.stderr
    # FR-500 is outside the scope: no block of either relation names it.
    assert not [
        ln
        for ln in matrix.stderr.splitlines()
        if "FR-500" in ln and "soup-requirements" in ln
    ]
