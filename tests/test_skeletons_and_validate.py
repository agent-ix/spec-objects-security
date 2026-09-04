"""Assert ↔ skeleton parity + roundtrip tests for the security object types.

Mirrors the spec-artifacts-iso pattern: each object_type ships an authoring
skeleton (``spec_objects_security/skeletons/<name>.md``) that is a complete
worked example of the manifest's ``body_extraction`` contract. The parity
tests are regex/yaml based (no quire import) and data-driven over every
object_type:

* a skeleton exists per type;
* every asserted ``section_body``/``code_block`` heading exists at H2 and
  every asserted code block carries the asserted fence language;
* reverse direction: the skeleton declares no headings, fence languages or
  frontmatter keys beyond the manifest's locators (no drift);
* required frontmatter fields are present, ``type`` equals the type
  name, and bodies are substantive (no placeholder tokens);
* roundtrip: each skeleton passes ``quire.validate_document``. The wheel is
  provisioned by ``make dev-quire`` and the tests **fail** without it; the old
  ``pytest.skip`` reported this gate green while it ran nothing, which is the
  defect agent-ix/spec-objects-security#10 named.
"""

from __future__ import annotations

import pathlib
import re

import pytest
import yaml

from tests.conftest import require_quire

PKG_ROOT = pathlib.Path(__file__).resolve().parent.parent / "spec_objects_security"
MANIFEST_PATH = PKG_ROOT / "manifest.yaml"
SKELETONS_DIR = PKG_ROOT / "skeletons"

_PLACEHOLDER_TOKENS = ("TODO", "TBD", "{{", "}}", "placeholder", "none specified")


def _object_types() -> list[dict]:
    return yaml.safe_load(MANIFEST_PATH.read_text()).get("object_types", [])


def _locators(ot: dict) -> dict:
    be = ot.get("body_extraction") or {}
    return (be.get("yield_pattern") or {}).get("match") or {}


def _skeleton_path(name: str) -> pathlib.Path:
    return SKELETONS_DIR / f"{name}.md"


def _skeleton_text(name: str) -> str:
    return _skeleton_path(name).read_text()


def _frontmatter(markdown: str) -> dict:
    m = re.match(r"---\n(.*?)\n---\n", markdown, re.DOTALL)
    assert m, "skeleton missing frontmatter block"
    return yaml.safe_load(m.group(1))


def _strip_frontmatter(markdown: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", markdown, count=1, flags=re.DOTALL)


def _h2_headings(markdown: str) -> list[str]:
    body = _strip_frontmatter(markdown)
    return [
        m.group(1).strip() for m in re.finditer(r"^##\s+(.*\S)\s*$", body, re.MULTILINE)
    ]


def _split_h2_sections(markdown: str) -> dict[str, str]:
    """Return {h2_heading: body_text} for the skeleton body."""
    body = _strip_frontmatter(markdown)
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in body.splitlines():
        m = re.match(r"^##\s+(.*\S)\s*$", line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = m.group(1).strip()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def _fence_languages(markdown: str) -> list[str]:
    body = _strip_frontmatter(markdown)
    return re.findall(r"^```(\w+)\s*$", body, re.MULTILINE)


_OBJECT_TYPES = _object_types()
_NAMES = [ot["name"] for ot in _OBJECT_TYPES]


def _ot(name: str) -> dict:
    return next(ot for ot in _OBJECT_TYPES if ot["name"] == name)


@pytest.mark.trace("TC-008", "FR-001-AC-1")
def test_every_object_type_ships_a_skeleton_and_nothing_extra() -> None:
    """TC-008: FR-001-AC-1."""
    missing = [n for n in _NAMES if not _skeleton_path(n).exists()]
    assert not missing, f"object_types without skeletons: {missing}"
    extra = sorted(
        p.name
        for p in SKELETONS_DIR.glob("*.md")
        if p.stem not in _NAMES and not p.name.endswith(".sysml.md")
    )
    assert not extra, f"skeletons without object_types: {extra}"
    orphan_alternates = sorted(
        p.name
        for p in SKELETONS_DIR.glob("*.sysml.md")
        if p.name[: -len(".sysml.md")] not in _NAMES
    )
    assert not orphan_alternates, orphan_alternates


@pytest.mark.trace("TC-009", "FR-001-AC-1")
@pytest.mark.parametrize("name", _NAMES, ids=lambda n: n)
def test_frontmatter_matches_manifest_locators(name: str) -> None:
    """TC-009: Required frontmatter fields are present and non-empty; type is
    the object_type name; no undeclared frontmatter keys (reverse drift)."""
    fm = _frontmatter(_skeleton_text(name))
    fm_locators = {
        key: loc
        for key, loc in _locators(_ot(name)).items()
        if loc.get("from") == "frontmatter_field"
    }
    declared_fields = {loc["path"][0] for loc in fm_locators.values()}
    for key, loc in fm_locators.items():
        field = loc["path"][0]
        if loc.get("required"):
            assert field in fm, f"{name}: required frontmatter {field!r} missing"
            value = fm[field]
            assert value not in (None, ""), f"{name}: frontmatter {field!r} empty"
    assert fm["type"] == name
    assert fm["id"] and fm["title"]
    assert fm["object"] == name, f"{name}: frontmatter `object` must equal `type`"
    undeclared = set(fm) - declared_fields - {"object"}
    assert not undeclared, f"{name}: undeclared frontmatter keys {undeclared}"


@pytest.mark.trace("TC-010", "FR-001-AC-1")
@pytest.mark.parametrize("name", _NAMES, ids=lambda n: n)
def test_asserted_sections_and_code_blocks_present(name: str) -> None:
    """TC-010: Every section_body/code_block locator's heading exists at H2; code_block
    locators have a fence with the asserted language inside their section."""
    md = _skeleton_text(name)
    sections = _split_h2_sections(md)
    for key, loc in _locators(_ot(name)).items():
        from_ = loc.get("from")
        if from_ not in ("section_body", "code_block"):
            continue
        heading = loc["after_heading"]
        assert (
            heading in sections
        ), f"{name}: locator {key!r} heading {heading!r} missing at H2"
        if from_ == "code_block":
            lang = loc["language"]
            assert (
                f"```{lang}" in sections[heading]
            ), f"{name}: section {heading!r} lacks a ```{lang} code block"


@pytest.mark.trace("TC-011", "FR-001-AC-1")
@pytest.mark.parametrize("name", _NAMES, ids=lambda n: n)
def test_no_skeleton_drift_beyond_manifest(name: str) -> None:
    """TC-011: Reverse direction: every H2 heading and fence language in the skeleton
    is asserted by the manifest, so skeletons can't drift ahead of contract."""
    md = _skeleton_text(name)
    locators = _locators(_ot(name))
    asserted_headings = {
        loc["after_heading"]
        for loc in locators.values()
        if loc.get("from") in ("section_body", "code_block")
    }
    assert (
        set(_h2_headings(md)) == asserted_headings
    ), f"{name}: skeleton H2 headings drifted from manifest asserts"
    asserted_langs = {
        loc["language"] for loc in locators.values() if loc.get("from") == "code_block"
    }
    # `ocl` and `sysml` are the semantic layer's own fence languages: an OCL
    # fence lives under `## Invariants` and a SysML fence is the alternate
    # `## Properties` form (quoin FR-071/FR-072). Neither is a `code_block`
    # locator, so both are admitted beside whatever the manifest asserts.
    admitted = asserted_langs | {"ocl", "sysml"}
    drifted = sorted(set(_fence_languages(md)) - admitted)
    assert not drifted, f"{name}: skeleton fence languages drifted: {drifted}"
    for lang in asserted_langs:
        assert lang in _fence_languages(md), f"{name}: missing ```{lang} fence"


@pytest.mark.trace("TC-012", "FR-001-AC-1")
@pytest.mark.parametrize("name", _NAMES, ids=lambda n: n)
def test_skeleton_is_substantive(name: str) -> None:
    """TC-012: Bodies are filled with real content: no placeholder tokens anywhere and
    every asserted section carries a non-empty body."""
    md = _skeleton_text(name)
    lowered = md.lower()
    for token in _PLACEHOLDER_TOKENS:
        assert (
            token.lower() not in lowered
        ), f"{name}: skeleton carries placeholder token {token!r}"
    body = _strip_frontmatter(md)
    prose = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    prose = re.sub(r"^#.*$", "", prose, flags=re.MULTILINE).strip()
    assert len(prose) > 100, f"{name}: skeleton body is not substantive"
    sections = _split_h2_sections(md)
    for key, loc in _locators(_ot(name)).items():
        if loc.get("from") == "section_body" and loc.get("required"):
            assert sections[
                loc["after_heading"]
            ], f"{name}: required section_body {key!r} is empty"


# ─── Roundtrip via the quire Python wheel (fails, never skips) ───────────


def _quire_doc_validator():
    """Return the quire wheel, or fail naming the provisioning path.

    agent-ix/spec-objects-security#10: this returned ``None`` and the callers
    skipped, so twenty-three unvalidated skeletons reported green. The wheel is
    provisioned by ``make dev-quire`` (agent-ix/quire-rs#392 tracks publishing
    it to an index this repository may depend on).
    """
    return require_quire()


@pytest.mark.trace("TC-013", "FR-001-AC-1")
@pytest.mark.parametrize("name", _NAMES, ids=lambda n: n)
def test_roundtrip_skeleton_validates(name: str) -> None:
    """TC-013: Each filled skeleton passes validate_document against this module.

    Skips when the installed quire wheel predates the markdown-default
    validator; quire is intentionally not a dependency of this pack."""
    quire = _quire_doc_validator()
    res = quire.validate_document(name, str(PKG_ROOT), _skeleton_text(name))
    assert res["is_valid"], res["errors"]


@pytest.mark.trace("TC-014", "FR-001-AC-1")
def test_roundtrip_mutation_fails() -> None:
    """TC-014: Deleting the required Schema code block from jwt_claim fails validation
    with a reason naming the missing locator."""
    quire = _quire_doc_validator()
    base = _skeleton_text("jwt_claim")
    mutated = re.sub(r"## Schema.*", "", base, flags=re.DOTALL)
    assert mutated != base, "mutation did not apply"
    res = quire.validate_document("jwt_claim", str(PKG_ROOT), mutated)
    assert not res["is_valid"]
    assert any("schema_json" in str(e) for e in res["errors"]), res["errors"]
