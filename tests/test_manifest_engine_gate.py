"""The engines that read this manifest accept it and refuse a bad one.

The module-manifest schema is owned by filament-core-data. This repository holds
no copy of it; the gate is the real engines applying it as they load a module:
`quire validate --module` (the manifest parse) and `quoin module install` (the
`semantic` contract). Each negative case writes a deliberately invalid manifest
to a temporary module directory and expects the engine to name the offending key.
"""

from __future__ import annotations

import os
import pathlib
import shutil
import subprocess

import pytest
import yaml

from tests.conftest import PACKAGE_ROOT, SKELETONS_DIR
from tests.conftest import engine_tool as _tool


def _module(tmp_path, mutate=None):
    module = tmp_path / "module" / "spec_objects_security"
    shutil.copytree(PACKAGE_ROOT, module)
    if mutate is not None:
        manifest = module / "manifest.yaml"
        data = yaml.safe_load(manifest.read_text())
        mutate(data)
        manifest.write_text(yaml.safe_dump(data, sort_keys=False))
    return module


def _quire_validate(module, tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir(exist_ok=True)
    shutil.copy(SKELETONS_DIR / "control.md", docs / "control.md")
    return subprocess.run(
        [_tool("quire"), "validate", "--okf", "--module", str(module), str(docs)],
        capture_output=True,
        text=True,
    )


def _quoin_install(module, tmp_path):
    # `quoin module install` writes under $HOME/.ix/filament, and IX_CONFIG_ROOT
    # does not move that, so the install is isolated by pointing HOME at tmp.
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    env = {**os.environ, "HOME": str(home)}
    env.pop("IX_CONFIG_ROOT", None)
    return subprocess.run(
        [_tool("quoin"), "module", "install", f"path:{module}", "--no-project-config"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env=env,
    )


@pytest.mark.trace("TC-115", "FR-003-AC-7")
def test_the_shipped_manifest_is_accepted_by_both_engines(tmp_path):
    module = _module(tmp_path)
    quire = _quire_validate(module, tmp_path)
    assert quire.returncode == 0, quire.stderr
    real_registry = pathlib.Path.home() / ".ix" / "filament" / "registry.json"
    before = real_registry.read_bytes() if real_registry.exists() else None
    quoin = _quoin_install(module, tmp_path)
    assert quoin.returncode == 0, quoin.stderr + quoin.stdout
    assert (tmp_path / "home" / ".ix" / "filament" / "registry.json").is_file()
    after = real_registry.read_bytes() if real_registry.exists() else None
    assert after == before, "the install escaped the temporary HOME"


@pytest.mark.trace("TC-115", "FR-003-AC-7")
def test_quire_refuses_an_unknown_top_level_key_and_names_it(tmp_path):
    module = _module(tmp_path, lambda d: d.update(bogus_key=1))
    result = _quire_validate(module, tmp_path)
    assert result.returncode != 0
    assert "bogus_key" in result.stderr, result.stderr


@pytest.mark.trace("TC-115", "FR-003-AC-7")
def test_quoin_refuses_an_unknown_semantic_key_and_names_it(tmp_path):
    module = _module(tmp_path, lambda d: d["semantic"].update(foo="bar"))
    result = _quoin_install(module, tmp_path)
    assert result.returncode != 0
    assert "semantic.foo" in result.stderr + result.stdout, result.stderr
