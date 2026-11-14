"""The clause sets the module ships (FR-017) and what an engine does with them.

The sets are public-source catalogues carried as identifiers and titles only
(``rights.text: none``). Every fixture here is synthetic: evidence references
and attesters use ``example.invalid``.
"""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import tarfile
import tempfile
import zipfile

import pytest
import yaml

from tests.conftest import MANIFEST_PATH, PACKAGE_ROOT, REPO_ROOT, engine_tool

CLAUSES_DIR = PACKAGE_ROOT / "clauses"
NIST = ("nist", "sp800-53", "5.2.0")
NIST_FILE = CLAUSES_DIR / "nist-sp800-53-5.2.0.json"
ASVS_FILE = CLAUSES_DIR / "owasp-asvs-5.0.0.json"
ASVS_KEY = "owasp/asvs@5.0.0"
CC_BY_SA_URI = "https://creativecommons.org/licenses/by-sa/4.0/"
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


NIST_KEY = "nist/sp800-53@5.2.0"
DECLARED_SETS = [NIST_KEY, ASVS_KEY]
NIST_FAMILIES = [
    "ac", "at", "au", "ca", "cm", "cp", "ia", "ir", "ma", "mp",
    "pe", "pl", "pm", "ps", "pt", "ra", "sa", "sc", "si", "sr",
]  # fmt: skip


@pytest.mark.trace("TC-175", "FR-017-AC-1")
def test_manifest_declares_exactly_the_expected_clause_sets():
    assert sorted(_key(s) for s in _declared()) == DECLARED_SETS


@pytest.mark.trace("TC-176", "FR-017-AC-2")
def test_every_declared_set_has_a_publishable_text_right():
    for clause_set in _declared():
        assert clause_set["rights"]["text"] in PUBLISHABLE_TEXT, _key(clause_set)


@pytest.mark.trace("TC-177", "FR-017-AC-3")
def test_publish_check_accepts_the_module():
    result = _run(engine_tool("quire"), "publish-check", "--module", str(PACKAGE_ROOT))
    assert result.returncode == 0, result.stderr + result.stdout


@pytest.mark.trace("TC-178", "FR-017-AC-4")
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


@pytest.mark.trace("TC-179", "FR-017-AC-5")
def test_every_set_names_its_licence_and_the_nist_set_is_public_domain():
    for clause_set in _declared():
        assert clause_set["rights"]["licence"].strip(), _key(clause_set)
    rights = _by_key(NIST_KEY)["rights"]
    assert "Public domain" in rights["licence"]
    assert "attribution" not in rights
    assert "share_alike" not in rights
    asvs = _by_key(ASVS_KEY)["rights"]
    assert CC_BY_SA_URI in asvs["licence"]
    assert CC_BY_SA_URI in asvs["attribution"]
    assert "OWASP" in asvs["attribution"]
    assert asvs["share_alike"].strip()


@pytest.mark.trace("TC-180", "FR-017-AC-6")
def test_each_nist_clause_names_its_official_family_dimension_value():
    nist = _by_key(NIST_KEY)
    dimension = nist["classificationDimensions"]["family"]["values"]
    assert dimension == NIST_FAMILIES
    for clause in nist["clauses"]:
        prefix = clause["id"].split("-")[0].lower()
        assert clause["subjects"] == [prefix], clause["id"]
        assert prefix in dimension, clause["id"]
    assert {c["subjects"][0] for c in nist["clauses"]} == set(NIST_FAMILIES)


@pytest.mark.trace("TC-184", "FR-017-AC-6")
def test_each_asvs_clause_names_its_chapter_dimension_value():
    asvs = _by_key(ASVS_KEY)
    dimension = asvs["classificationDimensions"]["chapter"]["values"]
    assert dimension == [f"V{n}" for n in range(1, 18)]
    for clause in asvs["clauses"]:
        prefix = clause["id"].split(".")[0]
        assert clause["subjects"] == [prefix], clause["id"]
        assert prefix in dimension, clause["id"]
    assert {c["subjects"][0] for c in asvs["clauses"]} == set(dimension)


def test_the_asvs_set_carries_only_identifiers():
    asvs = _by_key(ASVS_KEY)
    assert len(asvs["clauses"]) == 345
    for clause in asvs["clauses"]:
        assert set(clause) == {
            "id",
            "force",
            "subjects",
            "obligatedActors",
            "approvalRoles",
            "styles",
            "applicability",
            "expectedOutputs",
        }, clause["id"]


def test_levels_are_an_ordered_applicability_dimension():
    asvs = _by_key(ASVS_KEY)
    dimension = asvs["classificationDimensions"]["level"]
    assert dimension["values"] == ["1", "2", "3"]
    assert dimension["order"] == [["1"], ["2"], ["3"]]
    assert {c["applicability"]["dimension"] for c in asvs["clauses"]} == {"level"}


@pytest.mark.trace("TC-185", "FR-017-AC-7")
def test_a_profile_binds_only_the_asvs_level_it_needs(tmp_path):
    root = _stage_clause_only_module(tmp_path, ASVS_FILE)
    counts = {}
    for level in ("1", "2", "3"):
        outcomes = _outcomes(_evaluate(root, ASVS_KEY, f"level={level}"))
        counts[level] = sum(1 for o in outcomes.values() if o == "binding")
    assert counts == {"1": 70, "2": 253, "3": 345}
    unresolved = _outcomes(_evaluate(root, ASVS_KEY))
    assert set(unresolved.values()) == {"unresolved"}


def test_the_nist_set_carries_no_clause_text():
    nist = _by_key(NIST_KEY)
    assert all("text" not in clause for clause in nist["clauses"])
    assert all(clause["title"].strip() for clause in nist["clauses"])


def test_the_nist_set_loads_and_validates_via_quire_clauses(tmp_path):
    root = _stage_clause_only_module(tmp_path, NIST_FILE)
    report = _evaluate(root, NIST_KEY, "baseline=low")
    assert report["clauseSet"] == {
        "authority": "nist",
        "id": "sp800-53",
        "version": "5.2.0",
    }
    assert len(report["clauses"]) == len(_by_key(NIST_KEY)["clauses"])


def test_baselines_are_an_ordered_applicability_dimension():
    nist = _by_key(NIST_KEY)
    dimension = nist["classificationDimensions"]["baseline"]
    assert dimension["values"] == ["low", "moderate", "high"]
    assert dimension["order"] == [["low"], ["moderate"], ["high"]]
    gated = {
        c["applicability"].get("dimension")
        for c in nist["clauses"]
        if c["applicability"]["op"] == "at_least"
    }
    assert gated == {"baseline"}


@pytest.mark.trace("TC-181", "FR-017-AC-7")
def test_a_profile_binds_only_the_baseline_it_needs(tmp_path):
    root = _stage_clause_only_module(tmp_path, NIST_FILE)
    counts = {}
    for baseline in ("low", "moderate", "high"):
        outcomes = _outcomes(_evaluate(root, NIST_KEY, f"baseline={baseline}"))
        counts[baseline] = sum(1 for o in outcomes.values() if o == "binding")
    assert counts == {"low": 149, "moderate": 287, "high": 370}
    low = _outcomes(_evaluate(root, NIST_KEY, "baseline=low"))
    high = _outcomes(_evaluate(root, NIST_KEY, "baseline=high"))
    assert low["AC-2"] == "binding"
    assert low["AC-2(1)"] == "not_binding"
    assert high["AC-2(1)"] == "binding"
    # PM-1 is in no baseline: not_binding under every baseline.
    for outcomes in (low, high):
        assert outcomes["PM-1"] == "not_binding"
    unresolved = _outcomes(_evaluate(root, NIST_KEY))
    assert set(unresolved.values()) == {"unresolved"}


@pytest.mark.trace("TC-182")
def test_the_module_data_files_ship_in_the_wheel_and_the_npm_tarball():
    shipped = [
        PACKAGE_ROOT / p
        for p in yaml.safe_load(MANIFEST_PATH.read_text())["clause_sets"]
    ]
    shipped.extend((PACKAGE_ROOT / "profiles").glob("*.yaml"))
    assert shipped
    with tempfile.TemporaryDirectory() as tmp:
        built = subprocess.run(
            ["poetry", "build", "-f", "wheel", "-o", tmp],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        assert built.returncode == 0, built.stderr
        with zipfile.ZipFile(next(pathlib.Path(tmp).glob("*.whl"))) as archive:
            wheel = set(archive.namelist())
        packed = subprocess.run(
            ["npm", "pack", "--pack-destination", tmp],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            env={**os.environ, "npm_config_registry": "https://registry.npmjs.org/"},
        )
        assert packed.returncode == 0, packed.stderr
        with tarfile.open(next(pathlib.Path(tmp).glob("*.tgz"))) as archive:
            tarball = set(archive.getnames())
    for path in shipped:
        relative = path.relative_to(PACKAGE_ROOT).as_posix()
        assert f"spec_objects_security/{relative}" in wheel, relative
        assert f"package/{relative}" in tarball, relative
    assert not (REPO_ROOT / "clauses").exists(), "postpack left a staged clauses dir"


def _record_and_render_matrix(tmp_path, source, key, context, clause_id):
    root = _stage_clause_only_module(tmp_path, source)
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


@pytest.mark.trace("TC-183")
def test_quoin_renders_a_requirements_matrix_over_a_synthetic_corpus(tmp_path):
    rendered = _record_and_render_matrix(
        tmp_path, NIST_FILE, NIST_KEY, "baseline=low", "AC-1"
    )
    assert rendered.returncode == 0, rendered.stderr
    matrix = rendered.stdout
    assert "# Requirements mapping matrix: nist/sp800-53@5.2.0" in matrix
    row = "| AC-1 | Applicable | Compliant | evidence://example.invalid/run/one |"
    assert row in matrix
    assert "| AC-2 | Applicable | Not compliant - undischarged" in matrix
    assert "| AC-2\\(1\\) | Not applicable | Not applicable |" in matrix


@pytest.mark.trace("TC-186")
def test_quoin_renders_an_asvs_requirements_matrix_over_a_synthetic_corpus(tmp_path):
    rendered = _record_and_render_matrix(
        tmp_path, ASVS_FILE, ASVS_KEY, "level=1", "V1.2.1"
    )
    assert rendered.returncode == 0, rendered.stderr
    matrix = rendered.stdout
    assert "# Requirements mapping matrix: owasp/asvs@5.0.0" in matrix
    row = "| V1.2.1 | Applicable | Compliant | evidence://example.invalid/run/one |"
    assert row in matrix
    assert "| V1.2.2 | Applicable | Not compliant - undischarged" in matrix
    assert "| V1.2.6 | Not applicable | Not applicable |" in matrix
