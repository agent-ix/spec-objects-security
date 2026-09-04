"""Emitted JSON Schemas and the drift gate.

Every assertion reads the `$id` version segment from `manifest.yaml` rather
than hard-coding it (FR-002-CON-5), so a coordinated version bump churns no
test.
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

from tests.conftest import (
    MANIFEST_PATH,
    MODEL_OF,
    OBJECT_TYPES,
    REPO_ROOT,
    SCHEMAS_DIR,
    SEMANTIC_CORE_BASE,
    manifest_version,
    module_base,
)

GENERATOR = REPO_ROOT / "scripts" / "generate-schemas.mjs"

EXPECTED_MODELS = sorted(
    [MODEL_OF[name] for name in OBJECT_TYPES]
    + [
        "IdentityField",
        "DefaultedField",
        "OccurrenceField",
        "OccurrenceTypeRef",
        "StrideCategoryField",
        "SeverityField",
        "LikelihoodField",
        "ImpactField",
        "StatusField",
        "LevelField",
        "TrustLevelField",
        "EffectivenessField",
        "ControlMapping",
        "FlowStep",
        "Severity",
        "Likelihood",
        "Impact",
        "StrideCategory",
        "ControlEffectiveness",
        "FindingStatus",
        "ConfidentialityLevel",
        "TrustLevel",
        "SecretLifecycle",
        "MfaFactorKind",
    ]
)


def toolchain() -> dict:
    return json.loads((SCHEMAS_DIR / "toolchain.json").read_text())


def run_generator(*args: str, cwd=None) -> subprocess.CompletedProcess:
    """Run the generator that belongs to `cwd`.

    The generator resolves every path from its own location, not from the
    process working directory, so a scratch tree must be driven by its own
    copy. Running the repository's copy against a scratch `cwd` silently
    checks the repository instead, and every negative case then passes.
    """
    root = pathlib.Path(cwd) if cwd else REPO_ROOT
    return subprocess.run(
        ["node", str(root / "scripts" / "generate-schemas.mjs"), *args],
        cwd=str(root),
        capture_output=True,
        text=True,
    )


def shipped_schemas() -> list:
    return [p for p in sorted(SCHEMAS_DIR.glob("*.json")) if p.name != "toolchain.json"]


def clone_repo(destination) -> None:
    """Copy the pieces the generator reads into a scratch tree."""
    for item in ("typespec", "scripts", "node_modules", "package.json"):
        source = REPO_ROOT / item
        target = destination / item
        if source.is_dir():
            shutil.copytree(source, target, symlinks=True)
        else:
            shutil.copy2(source, target)
    package = destination / "spec_objects_security"
    package.mkdir()
    shutil.copy2(MANIFEST_PATH, package / "manifest.yaml")
    shutil.copytree(SCHEMAS_DIR, package / "schemas")


@pytest.mark.trace("TC-020", "FR-002-AC-1")
def test_emitted_set_equals_the_declared_models():
    record = toolchain()
    assert sorted(record["files"]) == [f"{m}.json" for m in EXPECTED_MODELS]
    assert sorted(p.name for p in shipped_schemas()) == [
        f"{m}.json" for m in EXPECTED_MODELS
    ]
    assert record["compiler"]["version"] == "1.15.0"
    assert record["emitter"]["version"] == "1.15.0"
    assert record["semanticCore"]["version"] == "0.1.0"


@pytest.mark.trace("TC-021", "FR-002-AC-2")
def test_every_schema_declares_the_draft_id_under_the_manifest_version_base():
    base = module_base()
    assert toolchain()["base"] == base
    for path in shipped_schemas():
        schema = json.loads(path.read_text())
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["$id"] == f"{base}{path.name}", path.name


@pytest.mark.trace("TC-022", "FR-002-AC-3")
def test_every_ref_resolves_to_a_sibling_or_semantic_core():
    base = module_base()
    shipped = {p.name for p in shipped_schemas()}
    found = 0
    for path in shipped_schemas():
        for ref in sorted(set(_refs(json.loads(path.read_text())))):
            found += 1
            if ref.startswith(base):
                assert ref[len(base) :] in shipped, (path.name, ref)
            else:
                assert ref.startswith(SEMANTIC_CORE_BASE), (path.name, ref)
    assert found > 0


def _refs(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str):
                yield value
            else:
                yield from _refs(value)
    elif isinstance(node, list):
        for item in node:
            yield from _refs(item)


@pytest.mark.trace("TC-023", "FR-002-AC-4")
def test_check_is_clean_and_names_a_mutated_schema_or_digest():
    assert run_generator("--check").returncode == 0
    with tempfile.TemporaryDirectory() as tmp:
        scratch = _scratch(tmp)
        victim = scratch / "spec_objects_security" / "schemas" / "Threat.json"
        victim.write_text(victim.read_text().replace("object", "object ", 1))
        result = run_generator("--check", cwd=scratch)
        assert result.returncode != 0
        assert "Threat.json" in result.stderr
    with tempfile.TemporaryDirectory() as tmp:
        scratch = _scratch(tmp)
        path = scratch / "spec_objects_security" / "manifest.yaml"
        text = path.read_text().replace("digest: sha256:", "digest: sha256:0", 1)
        path.write_text(text)
        result = run_generator("--check", cwd=scratch)
        assert result.returncode != 0
        assert "manifest.yaml" in result.stderr


def _scratch(tmp):
    scratch = pathlib.Path(tmp) / "repo"
    scratch.mkdir()
    clone_repo(scratch)
    return scratch


@pytest.mark.trace("TC-024", "FR-002-AC-5")
def test_a_base_version_differing_from_the_manifest_fails_naming_both():
    with tempfile.TemporaryDirectory() as tmp:
        scratch = _scratch(tmp)
        source = scratch / "typespec" / "main.tsp"
        version = manifest_version()
        source.write_text(source.read_text().replace(f"/{version}/", "/9.9.9/"))
        result = run_generator("--check", cwd=scratch)
        assert result.returncode != 0
        assert "9.9.9" in result.stderr and version in result.stderr


@pytest.mark.trace("TC-025", "FR-002-AC-6")
def test_the_built_wheel_contains_every_exported_schema():
    with tempfile.TemporaryDirectory() as tmp:
        build = subprocess.run(
            ["poetry", "build", "-f", "wheel", "-o", tmp],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        assert build.returncode == 0, build.stderr
        wheel = next(pathlib.Path(tmp).glob("*.whl"))
        with zipfile.ZipFile(wheel) as archive:
            names = set(archive.namelist())
        for name in OBJECT_TYPES:
            member = f"spec_objects_security/schemas/{MODEL_OF[name]}.json"
            assert member in names, member
        # Every shipped file, not only the twenty-three exports: a schema whose
        # `$ref` names a marker or vocabulary sibling that did not ship is
        # unresolvable at the consumer.
        for shipped in toolchain()["files"] + ["toolchain.json"]:
            assert f"spec_objects_security/schemas/{shipped}" in names, shipped


@pytest.mark.trace("TC-026", "FR-002-AC-7")
def test_the_npm_tarball_ships_the_manifest_beside_its_schemas():
    with tempfile.TemporaryDirectory() as tmp:
        pack = subprocess.run(
            ["npm", "pack", "--pack-destination", tmp],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            env={**os.environ, "npm_config_registry": "https://registry.npmjs.org/"},
        )
        assert pack.returncode == 0, pack.stderr
        tarball = next(pathlib.Path(tmp).glob("*.tgz"))
        with tarfile.open(tarball) as archive:
            names = set(archive.getnames())
        assert "package/manifest.yaml" in names
        for name in OBJECT_TYPES:
            member = f"package/schemas/{MODEL_OF[name]}.json"
            assert member in names, member
        for shipped in toolchain()["files"] + ["toolchain.json"]:
            assert f"package/schemas/{shipped}" in names, shipped
    assert not (REPO_ROOT / "manifest.yaml").exists(), "postpack left a staged manifest"


@pytest.mark.trace("TC-027", "FR-002-AC-8", "FR-002-CON-5")
def test_a_coordinated_version_bump_re_emits_everything():
    version = manifest_version()
    with tempfile.TemporaryDirectory() as tmp:
        scratch = _scratch(tmp)
        _bump(scratch, version, "9.9.9", both=True)
        assert run_generator(cwd=scratch).returncode == 0
        assert run_generator("--check", cwd=scratch).returncode == 0
        emitted = scratch / "spec_objects_security" / "schemas"
        schema = json.loads((emitted / "Threat.json").read_text())
        assert schema["$id"].endswith("/9.9.9/Threat.json")
        assert "/9.9.9/" in json.dumps(schema)
        assert json.loads((emitted / "toolchain.json").read_text())["base"].endswith(
            "/9.9.9/"
        )
    with tempfile.TemporaryDirectory() as tmp:
        scratch = _scratch(tmp)
        _bump(scratch, version, "9.9.9", both=False)
        result = run_generator("--check", cwd=scratch)
        assert result.returncode != 0
        assert "9.9.9" in result.stderr


def _bump(scratch, old, new, both):
    manifest = scratch / "spec_objects_security" / "manifest.yaml"
    manifest.write_text(
        manifest.read_text().replace(f"version: {old}\n", f"version: {new}\n", 1)
    )
    if both:
        source = scratch / "typespec" / "main.tsp"
        source.write_text(source.read_text().replace(f"/{old}/", f"/{new}/"))


@pytest.mark.trace("TC-028", "FR-002-AC-9")
def test_check_names_a_stale_schema_and_writes_nothing():
    with tempfile.TemporaryDirectory() as tmp:
        scratch = _scratch(tmp)
        stale = scratch / "spec_objects_security" / "schemas" / "Stale.json"
        stale.write_text("{}\n")
        before = {
            p.name: p.read_bytes()
            for p in (scratch / "spec_objects_security" / "schemas").glob("*.json")
        }
        result = run_generator("--check", cwd=scratch)
        assert result.returncode != 0
        assert "Stale.json" in result.stderr
        after = {
            p.name: p.read_bytes()
            for p in (scratch / "spec_objects_security" / "schemas").glob("*.json")
        }
        assert before == after


@pytest.mark.trace("TC-029", "FR-002-CON-3")
def test_emission_is_deterministic():
    with tempfile.TemporaryDirectory() as tmp:
        scratch = _scratch(tmp)
        emitted = scratch / "spec_objects_security" / "schemas"
        assert run_generator(cwd=scratch).returncode == 0
        first = {p.name: p.read_bytes() for p in emitted.glob("*.json")}
        assert run_generator(cwd=scratch).returncode == 0
        second = {p.name: p.read_bytes() for p in emitted.glob("*.json")}
        assert first == second


@pytest.mark.trace("TC-030", "FR-002-CON-1")
def test_the_official_emitter_only_and_no_hand_edited_output():
    config = (REPO_ROOT / "typespec" / "tspconfig.yaml").read_text()
    assert '"@typespec/json-schema"' in config
    assert "emitter:" not in config or "custom" not in config
    generator = GENERATOR.read_text()
    assert "@typespec/compiler/entrypoints/cli.js" in generator
    record = toolchain()
    assert record["emitter"]["name"] == "@typespec/json-schema"
    assert run_generator("--check").returncode == 0


@pytest.mark.trace("TC-031", "FR-002-CON-2")
def test_no_npmrc_no_local_refs_and_exact_pins():
    assert not (REPO_ROOT / ".npmrc").exists()
    package = json.loads((REPO_ROOT / "package.json").read_text())
    for name, spec in package["devDependencies"].items():
        assert not spec.startswith(("file:", "link:")), name
        assert spec[0].isdigit(), f"{name} is not pinned exactly: {spec}"


@pytest.mark.trace("TC-032", "FR-002-CON-4")
def test_the_lockfile_resolves_public_packages_from_npmjs():
    lock = json.loads((REPO_ROOT / "package-lock.json").read_text())
    offenders = []
    for name, entry in lock["packages"].items():
        resolved = entry.get("resolved")
        if not resolved:
            continue
        if "@agent-ix/" in name:
            assert resolved.startswith("http://npm.ix/"), name
        elif not resolved.startswith("https://registry.npmjs.org/"):
            offenders.append((name, resolved))
    assert not offenders, offenders


@pytest.mark.trace("TC-033", "FR-002-CON-5")
def test_no_test_hard_codes_the_id_version_segment():
    version = manifest_version()
    offenders = []
    for path in sorted((REPO_ROOT / "tests").rglob("*.py")):
        text = path.read_text()
        if f"spec-objects-security/{version}/" in text:
            offenders.append(path.name)
    assert not offenders, offenders
    assert module_base().endswith(f"/{version}/")


@pytest.mark.trace("TC-034", "FR-002-AC-10")
def test_the_generator_touches_only_the_schemas_and_the_digest_lines():
    with tempfile.TemporaryDirectory() as tmp:
        scratch = _scratch(tmp)
        manifest = scratch / "spec_objects_security" / "manifest.yaml"
        before = manifest.read_text().splitlines()
        elsewhere = {
            path: path.read_bytes()
            for path in scratch.rglob("*")
            if path.is_file()
            and "node_modules" not in path.parts
            and path.parent.name != "schemas"
            and path != manifest
        }
        assert run_generator(cwd=scratch).returncode == 0
        after = manifest.read_text().splitlines()
        assert len(before) == len(after)
        changed = [(a, b) for a, b in zip(before, after, strict=True) if a != b]
        assert all(b.strip().startswith("digest:") for _, b in changed), changed
        assert all(
            path.read_bytes() == blob for path, blob in elsewhere.items()
        ), "the generator wrote outside schemas/ and manifest.yaml"


@pytest.mark.trace("TC-035", "FR-002-AC-11")
def test_line_endings_are_pinned_and_packing_leaves_nothing_staged():
    attributes = (REPO_ROOT / ".gitattributes").read_text()
    for pattern in ("*.json", "*.tsp", "*.yaml", "*.md"):
        assert f"{pattern} text eol=lf" in attributes, pattern
    for staged in ("manifest.yaml", "schemas", "skeletons"):
        assert not (REPO_ROOT / staged).exists(), staged
