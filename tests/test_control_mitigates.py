"""FR-007: a control admits `hazard` and `failure_mode` as `mitigates` targets."""

from __future__ import annotations

import shutil
import subprocess

import pytest
import yaml

from tests.conftest import (
    MANIFEST_PATH,
    SKELETONS_DIR,
    engine_tool,
    validation_module_args,
)


@pytest.mark.trace("FR-007-AC-1")
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


@pytest.mark.trace("FR-007-AC-2")
def test_control_mitigating_an_asset_is_a_disallowed_edge_target(tmp_path):
    quire = engine_tool("quire")
    for name in ("control", "asset"):
        shutil.copy(SKELETONS_DIR / f"{name}.md", tmp_path / f"{name}.md")
    control = tmp_path / "control.md"
    control.write_text(
        control.read_text().replace(
            "object: control\n",
            "object: control\nrelationships:\n"
            "  - target: ASSET-001\n    type: mitigates\n",
            1,
        )
    )
    result = subprocess.run(
        [
            quire,
            "validate",
            "--okf",
            *validation_module_args(),
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    lines = [
        line
        for line in result.stderr.splitlines()
        if line.endswith("[disallowed-edge-target]")
    ]
    assert len(lines) == 1, result.stderr
    assert "target type 'asset'" in lines[0], lines[0]
