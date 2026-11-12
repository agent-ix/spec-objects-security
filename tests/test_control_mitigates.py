"""FR-007: a control admits `hazard` and `failure_mode` as `mitigates` targets."""

from __future__ import annotations

import importlib.util
import os
import pathlib
import shutil
import subprocess

import pytest
import yaml

from tests.conftest import MANIFEST_PATH, PACKAGE_ROOT, SKELETONS_DIR

ISO_MODULE_ENV = "SPEC_ARTIFACTS_ISO_MODULE"


def _iso_module() -> pathlib.Path:
    """The spec-artifacts-iso module root: the installed package, else the env path."""
    spec = importlib.util.find_spec("spec_artifacts_iso")
    if spec is not None and spec.origin:
        return pathlib.Path(spec.origin).parent
    env = os.environ.get(ISO_MODULE_ENV)
    if env:
        return pathlib.Path(env)
    pytest.fail(
        f"spec-artifacts-iso is not installed and {ISO_MODULE_ENV} names no checkout; "
        "it owns the edge vocabulary the bundle validation needs"
    )


@pytest.mark.trace("TC-091", "FR-007-AC-1")
def test_control_mitigates_targets_are_exactly_the_five_types():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    control = next(ot for ot in manifest["object_types"] if ot["name"] == "control")
    assert control["allowed_links"]["mitigates"] == [
        "threat",
        "risk",
        "vulnerability",
        "hazard",
        "failure_mode",
    ]


@pytest.mark.trace("TC-092", "FR-007-AC-2")
def test_control_mitigating_an_asset_is_a_disallowed_edge_target(tmp_path):
    quire = shutil.which("quire")
    if quire is None:
        pytest.fail("the `quire` CLI is not on PATH")
    for name in ("control", "asset"):
        shutil.copy(SKELETONS_DIR / f"{name}.md", tmp_path / f"{name}.md")
    control = tmp_path / "control.md"
    control.write_text(
        control.read_text().replace(
            "object: control\n---",
            "object: control\nrelationships:\n  - target: ASSET-001\n    type: mitigates\n---",
            1,
        )
    )
    result = subprocess.run(
        [
            quire,
            "validate",
            "--okf",
            "--module",
            str(_iso_module()),
            "--module",
            str(PACKAGE_ROOT),
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert "[disallowed-edge-target]" in result.stderr, result.stderr
    assert "'asset'" in result.stderr, result.stderr
