"""The clause sets the module ships (FR-017) and what an engine does with them.

The sets are public-source catalogues carried as identifiers and titles only
(``rights.text: none``). Every fixture here is synthetic: evidence references
and attesters use ``example.invalid``.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest
import yaml

from tests.conftest import MANIFEST_PATH, PACKAGE_ROOT, engine_tool

CLAUSES_DIR = PACKAGE_ROOT / "clauses"
NIST = ("nist", "sp800-53", "5.2.0")
NIST_FILE = CLAUSES_DIR / "nist-sp800-53-5.2.0.json"
PUBLISHABLE_TEXT = {"none", "original", "explicitly_cleared"}
AS_OF = "2026-11-13T00:00:00Z"


def _declared() -> list[dict]:
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    return [json.loads((PACKAGE_ROOT / p).read_text()) for p in manifest["clause_sets"]]


def _key(clause_set: dict) -> str:
    return f"{clause_set['authority']}/{clause_set['id']}@{clause_set['version']}"


def _by_key(key: str) -> dict:
    (found,) = [s for s in _declared() if _key(s) == key]
    return found


def _run(*args, env=None, **kwargs):
    return subprocess.run(args, capture_output=True, text=True, env=env, **kwargs)


def _stage_clause_only_module(tmp_path, *files):
    """A module holding only clause sets.

    ``quire clauses`` loads a module strictly and the object-type edges this
    module uses come from another module, so the sets are evaluated from a
    module that carries nothing but the committed set files.
    """
    root = tmp_path / "stage"
    (root / "clauses").mkdir(parents=True)
    for path in files:
        shutil.copy(path, root / "clauses" / path.name)
    listing = "".join(f"- clauses/{p.name}\n" for p in files)
    (root / "manifest.yaml").write_text(
        "manifest_version: 1.0.0\nname: staged-clause-sets\nversion: 0.0.1\n"
        f"clause_sets:\n{listing}"
    )
    return root


def _evaluate(root, key, *context):
    authority, rest = key.split("/")
    set_id, version = rest.split("@")
    args = [
        engine_tool("quire"),
        "clauses",
        "evaluate",
        "--module",
        str(root),
        "--authority",
        authority,
        "--set",
        set_id,
        "--version",
        version,
        "--json",
    ]
    for entry in context:
        args += ["--context", entry]
    result = _run(*args)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def _outcomes(report):
    return {c["clauseId"]: c["outcome"] for c in report["clauses"]}


@pytest.mark.trace("FR-017-AC-1")
def test_manifest_declares_the_nist_clause_set():
    keys = {_key(s) for s in _declared()}
    assert "nist/sp800-53@5.2.0" in keys


@pytest.mark.trace("FR-017-AC-2")
def test_every_declared_set_names_its_licence_and_a_publishable_text_right():
    for clause_set in _declared():
        rights = clause_set["rights"]
        assert rights["text"] in PUBLISHABLE_TEXT, _key(clause_set)
        assert rights["licence"].strip(), _key(clause_set)
        assert rights["attribution"].strip(), _key(clause_set)
        assert "share_alike" in rights, _key(clause_set)


@pytest.mark.trace("FR-017-AC-2")
def test_the_nist_set_is_truthful_about_a_public_domain_source():
    rights = _by_key("nist/sp800-53@5.2.0")["rights"]
    assert "Public domain" in rights["licence"]
    assert rights["share_alike"] == "none"
    assert rights["text"] == "none"


@pytest.mark.trace("FR-017-AC-3")
def test_publish_check_accepts_the_module():
    result = _run(engine_tool("quire"), "publish-check", "--module", str(PACKAGE_ROOT))
    assert result.returncode == 0, result.stderr + result.stdout


@pytest.mark.trace("FR-017-AC-4")
def test_publish_check_refuses_a_licensed_set(tmp_path):
    root = _stage_clause_only_module(tmp_path, NIST_FILE)
    path = root / "clauses" / NIST_FILE.name
    licensed = json.loads(path.read_text())
    licensed["authority"] = "example.invalid"
    licensed["rights"]["text"] = "licensed"
    licensed["clauses"][0]["text"] = "synthetic sentinel text"
    path.write_text(json.dumps(licensed))
    result = _run(engine_tool("quire"), "publish-check", "--module", str(root))
    assert result.returncode != 0
    assert "sentinel" not in result.stdout + result.stderr


def test_the_nist_set_carries_no_clause_text():
    nist = _by_key("nist/sp800-53@5.2.0")
    assert all("text" not in clause for clause in nist["clauses"])
    assert all(clause["title"].strip() for clause in nist["clauses"])


def test_the_nist_set_loads_and_validates_via_quire_clauses(tmp_path):
    root = _stage_clause_only_module(tmp_path, NIST_FILE)
    report = _evaluate(root, "nist/sp800-53@5.2.0", "baseline=low")
    assert report["clauseSet"] == {
        "authority": "nist",
        "id": "sp800-53",
        "version": "5.2.0",
    }
    assert len(report["clauses"]) == len(_by_key("nist/sp800-53@5.2.0")["clauses"])


def test_families_classify_and_baselines_are_an_ordered_applicability_dimension():
    nist = _by_key("nist/sp800-53@5.2.0")
    dimensions = nist["classificationDimensions"]
    assert len(dimensions["family"]["values"]) == 20
    assert dimensions["baseline"]["values"] == ["low", "moderate", "high"]
    assert dimensions["baseline"]["order"] == [["low"], ["moderate"], ["high"]]
    families = {c["subjects"][0] for c in nist["clauses"]}
    assert len(families) == 20
    gated = {
        c["applicability"].get("dimension")
        for c in nist["clauses"]
        if c["applicability"]["op"] == "at_least"
    }
    assert gated == {"baseline"}


def test_a_profile_binds_only_the_baseline_it_needs(tmp_path):
    root = _stage_clause_only_module(tmp_path, NIST_FILE)
    key = "nist/sp800-53@5.2.0"
    counts = {}
    for baseline in ("low", "moderate", "high"):
        outcomes = _outcomes(_evaluate(root, key, f"baseline={baseline}"))
        counts[baseline] = sum(1 for o in outcomes.values() if o == "binding")
    assert counts == {"low": 149, "moderate": 287, "high": 370}
    low = _outcomes(_evaluate(root, key, "baseline=low"))
    high = _outcomes(_evaluate(root, key, "baseline=high"))
    assert low["AC-2"] == "binding"
    assert low["AC-2(1)"] == "not_binding"
    assert high["AC-2(1)"] == "binding"
    unresolved = _outcomes(_evaluate(root, key))
    assert set(unresolved.values()) == {"unresolved"}


def _record_and_render_matrix(tmp_path, key, context, clause_id):
    root = _stage_clause_only_module(tmp_path, NIST_FILE)
    binding = tmp_path / "binding.json"
    binding.write_text(json.dumps(_evaluate(root, key, context)))
    facts = tmp_path / "facts.json"
    facts.write_text(
        json.dumps(
            [
                {
                    "kind": "direct",
                    "clauseId": clause_id,
                    "evidenceRefs": ["evidence://example.invalid/run/one"],
                    "attestation": {
                        "attestedBy": "reviewer",
                        "authority": "lead",
                        "attestedAt": "2026-11-01T00:00:00Z",
                        "expiresAt": "2027-11-01T00:00:00Z",
                    },
                }
            ]
        )
    )
    repo = tmp_path / "repo"
    repo.mkdir()
    quoin = engine_tool("quoin")
    recorded = _run(
        quoin,
        "evidence",
        "record-discharge",
        "--repo",
        str(repo),
        "--binding",
        str(binding),
        "--facts",
        str(facts),
    )
    assert recorded.returncode == 0, recorded.stderr
    return _run(
        quoin,
        "discharge",
        "--binding",
        str(binding),
        "--rmm",
        "--repo",
        str(repo),
        "--as-of",
        AS_OF,
    )


def test_quoin_renders_a_requirements_matrix_over_a_synthetic_corpus(tmp_path):
    rendered = _record_and_render_matrix(
        tmp_path, "nist/sp800-53@5.2.0", "baseline=low", "AC-1"
    )
    assert rendered.returncode == 0, rendered.stderr
    matrix = rendered.stdout
    assert "# Requirements mapping matrix: nist/sp800-53@5.2.0" in matrix
    row = "| AC-1 | Applicable | Compliant | evidence://example.invalid/run/one |"
    assert row in matrix
    assert "| AC-2 | Applicable | Not compliant - undischarged" in matrix
    assert "| AC-2\\(1\\) | Not applicable | Not applicable |" in matrix
