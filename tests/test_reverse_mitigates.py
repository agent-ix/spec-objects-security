"""FR-008: a security-classified NFR that mitigates nothing is reported.

The fixtures are the installed `spec-artifacts-iso` NFR skeleton and this
module's own threat skeleton, validated by the `quire` CLI with both modules
loaded. The reverse relation is declared in the manifest with the `where`
selector of quire-rs FR-058; nothing is copied into this repository.
"""

from __future__ import annotations

import importlib.util
import pathlib
import re
import shutil
import subprocess

import pytest
import yaml

from tests.conftest import MANIFEST_PATH, PACKAGE_ROOT, SKELETONS_DIR, engine_tool

CHECK = "unjustified-security-nfr"
THREAT_REF = "ix://agent-ix/spec-objects-security/THREAT-001"


def _iso() -> pathlib.Path:
    spec = importlib.util.find_spec("spec_artifacts_iso")
    if spec is None or not spec.origin:
        pytest.fail("spec-artifacts-iso is not installed; run `poetry install`")
    return pathlib.Path(spec.origin).parent


def _nfr(root, nfr_id, quality_attribute, mitigates=()):
    """Write an NFR from the iso skeleton, with one `mitigates` edge per target."""
    text = (_iso() / "skeletons" / "nfr.md").read_text()
    text = text.replace("NFR-001", nfr_id)
    text = re.sub(
        r"^quality_attribute: .*$",
        f"quality_attribute: {quality_attribute}",
        text,
        flags=re.M,
    )
    edges = "".join(f'  - target: "{t}"\n    type: mitigates\n' for t in mitigates)
    relationships = f"relationships:\n{edges}" if edges else ""
    text = re.sub(r"relationships:\n(?:  .*\n)+", relationships, text, count=1)
    # The skeleton's example upstream link would be a dangling reference.
    text = re.sub(r"\[(FR-001)\]\([^)]*\)", r"\1", text)
    (root / f"{nfr_id}.md").write_text(text)


def _threat(root):
    shutil.copy(SKELETONS_DIR / "threat.md", root / "THREAT-001.md")


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


def _registered(result):
    """Fail loudly when the iso NFR type is not registered.

    An iso that registers no types makes every fixture NFR an unknown type
    tolerated under OKF, so the tests would pass without the NFR archetype.
    """
    assert "unknown type 'NFR'" not in result.stderr, result.stderr
    return result


def _findings(result):
    return [line for line in result.stderr.splitlines() if line.endswith(f"[{CHECK}]")]


@pytest.mark.trace("TC-116", "FR-008-AC-1")
def test_security_nfr_relation_is_declared_with_a_where_selector():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    relations = manifest["traceability"]["required_relations"]
    (relation,) = [r for r in relations if r["from"] == "NFR"]
    assert relation["where"] == {"field": "quality_attribute", "values": ["security"]}
    assert relation["edges"] == ["mitigates"]
    assert relation["to"] == []
    assert relation["direction"] == "outgoing"
    assert relation["check"] == CHECK


@pytest.mark.trace("TC-117", "FR-008-AC-2")
def test_security_nfr_without_a_mitigates_edge_is_reported(tmp_path):
    _nfr(tmp_path, "NFR-001", "security")
    result = _registered(_validate(tmp_path))
    assert result.returncode == 0, result.stderr
    findings = _findings(result)
    assert len(findings) == 1, result.stderr
    assert "NFR-001" in findings[0] and "'security'" in findings[0], findings
    # The finding names the declaration and the selector field (FR-008 Outputs).
    assert "security-nfr-has-mitigation-target" in findings[0], findings
    assert "quality_attribute" in findings[0], findings


@pytest.mark.trace("TC-118", "FR-008-AC-3", "FR-008-AC-4")
def test_mitigating_or_differently_classified_nfr_is_not_reported(tmp_path):
    _threat(tmp_path)
    _nfr(tmp_path, "NFR-001", "security", [THREAT_REF])
    _nfr(tmp_path, "NFR-002", "security", ["ix://agent-ix/other-repo/THREAT-900"])
    _nfr(tmp_path, "NFR-003", "performance_efficiency")
    _nfr(tmp_path, "NFR-004", "safety")
    result = _registered(_validate(tmp_path))
    assert result.returncode == 0, result.stderr
    assert _findings(result) == [], result.stderr
    # Prove the rule is live over this very bundle: dropping one edge reports it.
    _nfr(tmp_path, "NFR-002", "security")
    findings = _findings(_validate(tmp_path))
    assert len(findings) == 1 and "NFR-002" in findings[0], findings


@pytest.mark.trace("TC-119", "FR-008-AC-5")
def test_finding_is_advisory_and_tunable(tmp_path):
    _nfr(tmp_path, "NFR-001", "security")
    strict = _registered(_validate(tmp_path, "--strict"))
    findings = _findings(strict)
    assert len(findings) == 1, strict.stderr
    # The rule never promotes itself: under strict it is still a warning.
    assert findings[0].startswith("warning:"), strict.stderr
    promoted = _registered(_validate(tmp_path, "--severity", f"trace:{CHECK}=error"))
    assert promoted.returncode != 0, promoted.stderr
    assert len(_findings(promoted)) == 1, promoted.stderr
    assert not _findings(promoted)[0].startswith("warning:"), promoted.stderr


@pytest.mark.trace("TC-120", "FR-008-AC-6")
def test_exposure_end_relations_keep_an_empty_to():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    by_name = {r["name"]: r for r in manifest["traceability"]["required_relations"]}
    for name in ("threat-has-control", "risk-has-treatment"):
        assert by_name[name]["to"] == [], name
