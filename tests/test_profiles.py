"""Source profile files: the profile format and the default profiles.

A profile is a YAML file under ``spec_objects_security/profiles/`` naming clause
sets and an applicability context. Quoin reads it and refuses a profile that
breaks the same rules. The module ships no JSON Schema for it; the
rules in ``validate_profile`` are the definition.
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess

import pytest
import yaml
from conftest import MANIFEST_PATH, PACKAGE_ROOT, engine_tool

PROFILES_DIR = PACKAGE_ROOT / "profiles"
SCHEMA_VERSION = "source-profile-v1"
TOP_KEYS = {"schemaVersion", "name", "title", "description", "clauseSets", "context"}
SET_KEYS = {"authority", "id", "version"}
ALLOWED_NAMES = {
    "us-device-cybersecurity-hipaa",
    "eu-device-gdpr-ai-act",
    "web-app-baseline",
}


class ProfileError(ValueError):
    """A profile breaks a profile-format rule; the message names the file and rule."""


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def validate_profile(path: pathlib.Path) -> dict:
    """Return the parsed profile at ``path`` or raise ``ProfileError``."""

    def refuse(rule: str) -> ProfileError:
        return ProfileError(f"{path}: {rule}")

    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise refuse("a profile must be a mapping")
    unknown = set(data) - TOP_KEYS
    if unknown:
        raise refuse(f"unknown top-level key {sorted(unknown)}")
    if data.get("schemaVersion") != SCHEMA_VERSION:
        raise refuse(f"schemaVersion must be {SCHEMA_VERSION}")
    for field in ("name", "title", "description"):
        if not _non_empty(data.get(field)):
            raise refuse(f"{field} must be a non-empty string")
    if data["name"] != path.stem:
        raise refuse("name must equal the file stem")
    sets = data.get("clauseSets")
    if not isinstance(sets, list) or not sets:
        raise refuse("clauseSets must list at least one key")
    seen = set()
    for entry in sets:
        if not isinstance(entry, dict) or set(entry) != SET_KEYS:
            raise refuse("a clauseSets entry holds authority, id and version only")
        for field in SET_KEYS:
            if not isinstance(entry[field], str):
                raise refuse(f"clause-set key field {field} must be a string")
            if not entry[field].strip():
                raise refuse(f"clause-set key field {field} is empty")
        key = (entry["authority"], entry["id"], entry["version"])
        if key in seen:
            raise refuse(f"clause-set key {key} is repeated")
        seen.add(key)
    context = data.get("context", {})
    if not isinstance(context, dict):
        raise refuse("context must be a mapping")
    for dimension, value in context.items():
        if not _non_empty(dimension) or not _non_empty(value):
            raise refuse(f"context entry {dimension!r} needs a non-empty string value")
    return data


def _write(tmp_path: pathlib.Path, name: str, text: str) -> pathlib.Path:
    path = tmp_path / f"{name}.yaml"
    path.write_text(text)
    return path


BODY = (
    "schemaVersion: source-profile-v1\n"
    "name: {name}\ntitle: T\ndescription: D\n"
    "clauseSets:\n"
    "  - {{authority: example.invalid, id: a, version: '1'}}\n"
)


def _good(name: str = "p", extra: str = "") -> str:
    return BODY.format(name=name) + extra


def profile_files() -> list[pathlib.Path]:
    """Every file under profiles/, whatever its extension."""
    if not PROFILES_DIR.is_dir():
        return []
    return sorted(path for path in PROFILES_DIR.rglob("*") if path.is_file())


def shipped_profiles() -> list[pathlib.Path]:
    return [path for path in profile_files() if path.suffix == ".yaml"]


@pytest.mark.trace("TC-170", "TC-173", "FR-021-AC-5", "NFR-002-AC-1")
def test_profiles_holds_only_yaml_profile_files() -> None:
    stray = [
        p.name
        for p in profile_files()
        if p.suffix != ".yaml" or p.parent != PROFILES_DIR
    ]
    assert stray == [], f"files that are not profiles/<name>.yaml: {stray}"


@pytest.mark.trace("TC-160", "FR-020-AC-1")
def test_a_complete_profile_passes(tmp_path: pathlib.Path) -> None:
    data = validate_profile(
        _write(tmp_path, "p", _good(extra="context:\n  market: eu\n"))
    )
    assert data["clauseSets"][0]["id"] == "a"


@pytest.mark.trace("TC-161", "FR-020-AC-2")
@pytest.mark.parametrize("missing", ["name", "title", "description", "clauseSets"])
def test_a_profile_missing_a_required_key_fails(
    tmp_path: pathlib.Path, missing: str
) -> None:
    data = yaml.safe_load(_good())
    del data[missing]
    path = _write(tmp_path, "p", yaml.safe_dump(data))
    with pytest.raises(ProfileError, match=missing):
        validate_profile(path)


@pytest.mark.trace("TC-161", "FR-020-AC-2")
def test_a_name_differing_from_the_file_stem_fails(tmp_path: pathlib.Path) -> None:
    with pytest.raises(ProfileError, match="file stem"):
        validate_profile(_write(tmp_path, "p", _good(name="other")))


@pytest.mark.trace("TC-162", "FR-020-AC-3")
def test_empty_sets_empty_fields_and_repeats_fail(tmp_path: pathlib.Path) -> None:
    head = "schemaVersion: source-profile-v1\nname: p\ntitle: T\ndescription: D\n"
    cases = {
        "at least one": head + "clauseSets: []\n",
        "empty": head + "clauseSets:\n  - {authority: '', id: a, version: '1'}\n",
        "repeated": head
        + "clauseSets:\n"
        + "  - {authority: example.invalid, id: a, version: '1'}\n"
        + "  - {authority: example.invalid, id: a, version: '1'}\n",
    }
    for rule, text in cases.items():
        with pytest.raises(ProfileError, match=rule):
            validate_profile(_write(tmp_path, "p", text))


@pytest.mark.trace("TC-163", "FR-020-AC-4")
def test_unknown_keys_and_bad_context_values_fail(tmp_path: pathlib.Path) -> None:
    for extra in (
        "surprise: 1\n",
        "context:\n  market: ''\n",
        "context:\n  market: 2\n",
    ):
        with pytest.raises(ProfileError):
            validate_profile(_write(tmp_path, "p", _good(extra=extra)))


@pytest.mark.trace("TC-164", "FR-020-AC-5")
@pytest.mark.parametrize("field", ["text", "title"])
def test_a_clause_set_entry_carrying_text_or_title_fails(
    tmp_path: pathlib.Path, field: str
) -> None:
    text = _good().replace("version: '1'}", f"version: '1', {field}: x}}")
    with pytest.raises(ProfileError, match="authority, id and version only"):
        validate_profile(_write(tmp_path, "p", text))


@pytest.mark.trace("TC-165", "FR-020-AC-6")
def test_the_manifest_declares_no_profiles_key() -> None:
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert "profiles" not in manifest


@pytest.mark.trace("TC-166", "TC-173", "FR-021-AC-1", "NFR-002-AC-1", "NFR-002-M-1")
@pytest.mark.parametrize("path", shipped_profiles(), ids=lambda p: p.stem)
def test_every_shipped_profile_passes_the_profile_test(path: pathlib.Path) -> None:
    validate_profile(path)


@pytest.mark.trace("TC-170", "FR-021-AC-5")
def test_shipped_profile_names_are_among_the_three_defaults() -> None:
    names = {path.stem for path in shipped_profiles()}
    assert names <= ALLOWED_NAMES, sorted(names - ALLOWED_NAMES)


@pytest.mark.trace("TC-206", "FR-021-AC-1", "FR-021-AC-5")
def test_web_app_baseline_profile_is_shipped_with_only_its_public_sets() -> None:
    path = PROFILES_DIR / "web-app-baseline.yaml"
    assert path.is_file()

    profile = validate_profile(path)
    assert profile["name"] == "web-app-baseline"
    assert profile["clauseSets"] == [
        {"authority": "nist", "id": "sp800-53", "version": "5.2.0"},
        {"authority": "owasp", "id": "asvs", "version": "5.0.0"},
    ]
    assert "context" not in profile


def declared_keys(module_dir: pathlib.Path) -> set[tuple[str, str, str]]:
    """The clause-set keys a module's manifest lists, read from its set files."""
    manifest = yaml.safe_load((module_dir / "manifest.yaml").read_text()) or {}
    keys = set()
    for relative in manifest.get("clause_sets") or []:
        path = module_dir / relative
        data = (
            json.loads(path.read_text())
            if path.suffix == ".json"
            else yaml.safe_load(path.read_text())
        )
        keys.add((data["authority"], data["id"], str(data["version"])))
    return keys


@pytest.fixture(scope="session")
def reference_modules(tmp_path_factory: pytest.TempPathFactory) -> list[pathlib.Path]:
    """The reference module set: the modules `quoin module
    ensure-defaults` installs into a fresh home, plus this module.

    Built from scratch rather than read from an ambient install, so a stale or
    unpublished local module cannot make a profile pass or fail. It is only
    built when a shipped profile needs it.
    """
    home = tmp_path_factory.mktemp("reference-home")
    result = subprocess.run(
        [engine_tool("quoin"), "module", "ensure-defaults"],
        env={**os.environ, "IX_HOME": str(home)},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    installed = sorted((home / "filament" / "modules").glob("*"))
    return [PACKAGE_ROOT, *(d for d in installed if (d / "manifest.yaml").is_file())]


def declaring_module(
    key: tuple[str, str, str], modules: list[pathlib.Path]
) -> pathlib.Path | None:
    for module in modules:
        if key in declared_keys(module):
            return module
    return None


def publish_check(module: pathlib.Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [engine_tool("quire"), "publish-check", "--module", str(module)],
        capture_output=True,
        text=True,
        check=False,
    )


def _synthetic_module(root: pathlib.Path, text_rights: str) -> pathlib.Path:
    root.mkdir()
    (root / "manifest.yaml").write_text(
        f"name: {root.name}\nversion: 0.1.0\nclause_sets:\n  - rules.yaml\n"
    )
    text = "" if text_rights == "none" else "    text: synthetic\n"
    (root / "rules.yaml").write_text(
        "schemaVersion: clause-set-v1\nauthority: example.invalid\nid: rules\n"
        "title: Rules\nversion: '2'\nrights:\n  structure: original\n"
        f"  text: {text_rights}\n"
        f"clauses:\n  - id: C-1\n    force: mandatory\n{text}"
    )
    return root


def _shipped_keys(path: pathlib.Path) -> list[tuple[str, str, str]]:
    return [
        (e["authority"], e["id"], e["version"])
        for e in validate_profile(path)["clauseSets"]
    ]


@pytest.mark.trace("TC-167", "FR-021-AC-2")
@pytest.mark.parametrize("path", shipped_profiles(), ids=lambda p: p.stem)
def test_every_shipped_key_is_declared_by_a_reference_module(
    path: pathlib.Path, reference_modules: list[pathlib.Path]
) -> None:
    for key in _shipped_keys(path):
        module = declaring_module(key, reference_modules)
        assert module, f"{path.stem}: no module declares {key}"


@pytest.mark.trace("TC-168", "TC-174", "FR-021-AC-3", "NFR-002-AC-2", "NFR-002-M-2")
@pytest.mark.parametrize("path", shipped_profiles(), ids=lambda p: p.stem)
def test_every_shipped_key_has_a_publishable_declaring_module(
    path: pathlib.Path, reference_modules: list[pathlib.Path]
) -> None:
    for key in _shipped_keys(path):
        module = declaring_module(key, reference_modules)
        assert module is not None, f"{path.stem}: no module declares {key}"
        result = publish_check(module)
        assert result.returncode == 0, f"{module}: {result.stdout}{result.stderr}"


@pytest.mark.trace("TC-167", "TC-168", "FR-021-AC-2", "FR-021-AC-3")
def test_the_declaration_and_publishability_lookups_tell_modules_apart(
    tmp_path: pathlib.Path,
) -> None:
    open_module = _synthetic_module(tmp_path / "open-mod", "none")
    licensed = _synthetic_module(tmp_path / "licensed-mod", "licensed")
    key = ("example.invalid", "rules", "2")
    assert declaring_module(key, [open_module]) == open_module
    assert declaring_module(("example.invalid", "rules", "3"), [open_module]) is None
    assert publish_check(open_module).returncode == 0
    refused = publish_check(licensed)
    # Exit 2 is "restricted"; 3 would be a usage or I/O error, not a verdict.
    assert refused.returncode == 2, refused.stderr
    assert "example.invalid/rules@2" in refused.stdout + refused.stderr


@pytest.mark.trace("TC-162", "FR-020-AC-3")
def test_a_numeric_version_is_refused_as_not_a_string(tmp_path: pathlib.Path) -> None:
    text = _good().replace("version: '1'", "version: 5")
    with pytest.raises(ProfileError, match="must be a string"):
        validate_profile(_write(tmp_path, "p", text))
