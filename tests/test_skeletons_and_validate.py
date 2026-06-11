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
* required frontmatter fields are present, ``artifact_type`` equals the type
  name, and bodies are substantive (no placeholder tokens);
* roundtrip: each skeleton passes ``quire.validate_document`` when the
  installed quire wheel exposes it (skipped cleanly otherwise — quire is not
  a dependency of this pack).
"""

from __future__ import annotations

import pathlib
import re

import pytest
import yaml

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


def test_every_object_type_ships_a_skeleton_and_nothing_extra() -> None:
    missing = [n for n in _NAMES if not _skeleton_path(n).exists()]
    assert not missing, f"object_types without skeletons: {missing}"
    extra = sorted(p.stem for p in SKELETONS_DIR.glob("*.md") if p.stem not in _NAMES)
    assert not extra, f"skeletons without object_types: {extra}"


@pytest.mark.parametrize("name", _NAMES, ids=lambda n: n)
def test_frontmatter_matches_manifest_locators(name: str) -> None:
    """Required frontmatter fields are present and non-empty; artifact_type is
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
    assert fm["artifact_type"] == name
    assert fm["id"] and fm["title"]
    undeclared = set(fm) - declared_fields
    assert not undeclared, f"{name}: undeclared frontmatter keys {undeclared}"


@pytest.mark.parametrize("name", _NAMES, ids=lambda n: n)
def test_asserted_sections_and_code_blocks_present(name: str) -> None:
    """Every section_body/code_block locator's heading exists at H2; code_block
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


@pytest.mark.parametrize("name", _NAMES, ids=lambda n: n)
def test_no_skeleton_drift_beyond_manifest(name: str) -> None:
    """Reverse direction: every H2 heading and fence language in the skeleton
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
    asserted_langs = sorted(
        loc["language"] for loc in locators.values() if loc.get("from") == "code_block"
    )
    assert (
        sorted(_fence_languages(md)) == asserted_langs
    ), f"{name}: skeleton fence languages drifted from manifest asserts"


@pytest.mark.parametrize("name", _NAMES, ids=lambda n: n)
def test_skeleton_is_substantive(name: str) -> None:
    """Bodies are filled with real content: no placeholder tokens anywhere and
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


# ─── Roundtrip via the quire Python wheel (skipped on old wheels) ─────────


def _quire_doc_validator():
    """Return the quire wheel iff it exposes the markdown document validator."""
    try:
        import quire
    except ImportError:
        return None
    if not hasattr(quire, "validate_document"):
        return None
    return quire


@pytest.mark.parametrize("name", _NAMES, ids=lambda n: n)
def test_roundtrip_skeleton_validates(name: str) -> None:
    """Each filled skeleton passes validate_document against this module.

    Skips when the installed quire wheel predates the markdown-default
    validator; quire is intentionally not a dependency of this pack."""
    quire = _quire_doc_validator()
    if quire is None:
        pytest.skip("quire wheel lacks validate_document")
    res = quire.validate_document(name, str(PKG_ROOT), _skeleton_text(name))
    assert res["is_valid"], res["errors"]


def test_roundtrip_mutation_fails() -> None:
    """Deleting the required Schema code block from jwt_claim fails validation
    with a reason naming the missing locator."""
    quire = _quire_doc_validator()
    if quire is None:
        pytest.skip("quire wheel lacks validate_document")
    base = _skeleton_text("jwt_claim")
    mutated = re.sub(r"## Schema.*", "", base, flags=re.DOTALL)
    assert mutated != base, "mutation did not apply"
    res = quire.validate_document("jwt_claim", str(PKG_ROOT), mutated)
    assert not res["is_valid"]
    assert any("schema_json" in str(e) for e in res["errors"]), res["errors"]
