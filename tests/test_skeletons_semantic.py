"""The skeletons as executable typed fixtures, and the negative
fixtures that pin what the schemas and the engine refuse.

Two resolution paths are exercised and are kept distinct: `validate_document`
runs the module's own registry over one document, while `extract_semantic` runs
under a bundle index built from the skeleton frontmatter. Only the second can
resolve a `Type` cell that names another skeleton.
"""

from __future__ import annotations

import re
import subprocess

import pytest

from tests.conftest import (
    ALTERNATES,
    CLAUSE_BEARING,
    FIELD_BEARING,
    IDENTIFIER,
    KERNEL_SCALARS,
    NEGATIVE_DIR,
    OBJECT_TYPES,
    OPERATION_BEARING,
    PACKAGE_ROOT,
    REPO_ROOT,
    SKELETONS_DIR,
    frontmatter,
    locators,
    object_type,
)

TYPE_PREFIX = "ix://agent-ix/spec-objects-security/type/"

# A literal that looks like live material. The scan is the gate for free text
# (prose, `doc` cells, clause bodies): no schema can forbid a string.
CREDENTIAL_SHAPES = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{6,}"),
    re.compile(r"\bAKIA[0-9A-Z]{12,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"(?i)\b(password|secret|token|api[_-]?key)\s*[:=]\s*[\"']?\S{8,}"),
)


def primary_skeletons() -> list:
    return sorted(p for p in SKELETONS_DIR.glob("*.md") if ".sysml." not in p.name)


def all_skeletons() -> list:
    return sorted(SKELETONS_DIR.glob("*.md"))


def extract(quire_engine, module, bundle, path):
    text = path.read_text()
    return quire_engine.extract_semantic(
        {
            "markdown": text,
            "module": module,
            "path": str(path),
            "sourceIdentity": (
                f"ix://agent-ix/spec-objects-security/{frontmatter(text)['id']}"
            ),
            "bundle": bundle,
        }
    )


@pytest.mark.trace("TC-080", "FR-005-AC-1")
def test_every_skeleton_validates_with_no_error(quire_engine):
    paths = all_skeletons()
    assert len(paths) == 26, [p.name for p in paths]
    for path in paths:
        text = path.read_text()
        result = quire_engine.validate_document(
            frontmatter(text)["type"], str(PACKAGE_ROOT), text
        )
        assert result["is_valid"], (path.name, result["errors"])
        assert not [
            e for e in result["errors"] if "semantic.record-invalid" in e["message"]
        ], path.name


@pytest.mark.trace("TC-081", "FR-005-AC-2", "FR-005-CON-2")
def test_table_and_sysml_skeletons_extract_to_identical_fields(
    quire_engine, semantic_module, bundle_index
):
    for name in ALTERNATES:
        table = extract(
            quire_engine, semantic_module, bundle_index, SKELETONS_DIR / f"{name}.md"
        )
        fence = extract(
            quire_engine,
            semantic_module,
            bundle_index,
            SKELETONS_DIR / f"{name}.sysml.md",
        )
        assert table["fieldsForm"] == "table", name
        assert fence["fieldsForm"] == "fence", name
        assert table["fields"] == fence["fields"], name


@pytest.mark.trace("TC-082", "FR-005-AC-3")
def test_under_the_bundle_index_every_skeleton_extracts_clean(
    quire_engine, semantic_module, bundle_index
):
    for path in all_skeletons():
        record = extract(quire_engine, semantic_module, bundle_index, path)
        diagnostics = record.get("diagnostics", [])
        assert not [d for d in diagnostics if d.get("severity") == "error"], (
            path.name,
            diagnostics,
        )
        assert not [
            d for d in diagnostics if d.get("code") == "semantic.unresolved-type"
        ], (path.name, diagnostics)
        for decl in record.get("fields") or []:
            target = decl["type"]["target"]
            if target in KERNEL_SCALARS:
                continue
            assert target.startswith(TYPE_PREFIX), (path.name, target)


@pytest.mark.trace("TC-083", "FR-005-AC-4")
def test_availability_states_match_each_type(
    quire_engine, semantic_module, bundle_index
):
    for path in all_skeletons():
        name = frontmatter(path.read_text())["type"]
        record = extract(quire_engine, semantic_module, bundle_index, path)
        states = {k: v["state"] for k, v in record["availability"].items()}
        expected = {
            "fields": "available" if name in FIELD_BEARING else "not_applicable",
            "clauses": "available" if name in CLAUSE_BEARING else "not_applicable",
            "operations": (
                "available" if name in OPERATION_BEARING else "not_applicable"
            ),
        }
        assert states == expected, (path.name, states)


@pytest.mark.trace("TC-084", "FR-005-AC-5")
def test_every_negative_fixture_produces_its_expected_code(quire_engine):
    fixtures = sorted(NEGATIVE_DIR.glob("*.md"))
    assert len(fixtures) == 10, [p.name for p in fixtures]
    expected = {
        "semantic.record-invalid",
        "semantic.properties-both-forms",
        "semantic.dangling-clause-ref",
        "semantic.invalid-type-token",
        "semantic.unknown-constraint-keyword",
    }
    seen = set()
    for path in fixtures:
        text = path.read_text()
        front = frontmatter(text)
        code = front["expect"]
        assert front.get("because"), path.name
        seen.add(code)
        result = quire_engine.validate_document(front["type"], str(PACKAGE_ROOT), text)
        assert not result["is_valid"], path.name
        assert any(code in e["message"] for e in result["errors"]), (
            path.name,
            code,
            [e["message"] for e in result["errors"]],
        )
    assert seen == expected, seen


@pytest.mark.trace("TC-090", "FR-005-CON-2")
def test_a_section_carrying_both_forms_is_refused(quire_engine):
    path = NEGATIVE_DIR / "properties-both-forms.md"
    text = path.read_text()
    result = quire_engine.validate_document(
        frontmatter(text)["type"], str(PACKAGE_ROOT), text
    )
    assert not result["is_valid"]
    assert any(
        "semantic.properties-both-forms" in e["message"] for e in result["errors"]
    ), result["errors"]


@pytest.mark.trace("TC-085", "FR-005-AC-6")
def test_every_skeleton_heading_is_asserted_by_the_manifest():
    for path in all_skeletons():
        name = frontmatter(path.read_text())["type"]
        declared = locators(object_type(name))
        asserted = {
            loc["after_heading"]
            for loc in declared.values()
            if loc.get("from") in ("section_body", "code_block")
        }
        required = {
            loc["after_heading"]
            for loc in declared.values()
            if loc.get("from") in ("section_body", "code_block") and loc.get("required")
        }
        headings = set(_h2(path.read_text()))
        assert headings <= asserted, (path.name, headings - asserted)
        assert required <= headings, (path.name, required - headings)


def _h2(markdown: str) -> list[str]:
    body = re.sub(r"^---\n.*?\n---\n", "", markdown, count=1, flags=re.DOTALL)
    return [m.group(1).strip() for m in re.finditer(r"^##\s+(.*\S)\s*$", body, re.M)]


@pytest.mark.trace("TC-086", "FR-005-AC-7")
def test_every_skeleton_is_placeholder_free_and_substantive():
    tokens = ("TODO", "TBD", "{{", "}}", "placeholder", "none specified")
    for path in primary_skeletons():
        text = path.read_text()
        lowered = text.lower()
        for token in tokens:
            assert token.lower() not in lowered, (path.name, token)
        sections = _sections(text)
        name = frontmatter(text)["type"]
        for key, loc in locators(object_type(name)).items():
            if loc.get("from") == "section_body" and loc.get("required"):
                assert sections[loc["after_heading"]].strip(), (path.name, key)
    assert len(primary_skeletons()) == 23


def _sections(markdown: str) -> dict:
    body = re.sub(r"^---\n.*?\n---\n", "", markdown, count=1, flags=re.DOTALL)
    out: dict[str, str] = {}
    current = None
    buf: list[str] = []
    for line in body.splitlines():
        match = re.match(r"^##\s+(.*\S)\s*$", line)
        if match:
            if current is not None:
                out[current] = "\n".join(buf)
            current = match.group(1).strip()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf)
    return out


@pytest.mark.trace("TC-087", "FR-005-AC-8")
def test_titles_are_distinct_identifiers_and_object_equals_type():
    titles = []
    for path in primary_skeletons():
        front = frontmatter(path.read_text())
        assert IDENTIFIER.match(front["title"]), (path.name, front["title"])
        assert front["title"] not in KERNEL_SCALARS, front["title"]
        assert front["object"] == front["type"] == path.stem, path.name
        titles.append(front["title"])
    assert len(titles) == len(set(titles)), titles
    assert sorted(p.stem for p in primary_skeletons()) == sorted(OBJECT_TYPES)
    for name in ALTERNATES:
        alternate = frontmatter((SKELETONS_DIR / f"{name}.sysml.md").read_text())
        primary = frontmatter((SKELETONS_DIR / f"{name}.md").read_text())
        assert alternate["id"] == primary["id"], name
        assert alternate["title"] == primary["title"], name
        assert alternate["object"] == alternate["type"] == name, name


@pytest.mark.trace("TC-088", "FR-005-AC-9", "FR-005-CON-3")
def test_no_skeleton_or_fixture_carries_a_credential_shaped_literal():
    paths = all_skeletons() + sorted(NEGATIVE_DIR.glob("*.md"))
    assert paths
    for path in paths:
        text = path.read_text()
        for pattern in CREDENTIAL_SHAPES:
            assert not pattern.search(text), (path.name, pattern.pattern)
    canary = "password: hunter2hunter2"
    assert any(p.search(canary) for p in CREDENTIAL_SHAPES), "the scan detects nothing"


@pytest.mark.trace("TC-089", "FR-005-CON-1")
def test_the_repository_holds_no_corpus_or_vendored_fixture():
    """FR-005-CON-1 as a **tree** assertion, never as a diff against a moving ref.

    The obvious form — `git diff --name-only origin/main...HEAD`, then check no
    changed path is under `corpus/` or a vendor tree — degrades the moment the
    branch merges. `origin/main...HEAD` then resolves to the empty set, so the
    loops iterate over nothing and the guard passes while checking nothing; the
    positive-diff variant of the same guard (`assert changed`) goes one worse
    and turns main red for a branch that is no longer a branch. A merged
    change's path set is a fixed historical fact, and an assertion about it must
    not be computed against a ref that keeps moving.

    The tree form says something stronger and merge-invariant: these paths are
    absent from the repository at all, not merely untouched by one branch. It is
    exactly equivalent in intent here because no `corpus/`,
    `fixtures/semantic-module` or vendor path exists in this repository, on this
    branch or on `main`. No `git diff` survives in this guard, so there is no
    range whose rename detection could hide a deletion.
    """
    listing = subprocess.run(
        ["git", "ls-files"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert listing.returncode == 0, listing.stderr
    tracked = [line for line in listing.stdout.splitlines() if line]
    # Liveness: without this the guard passes vacuously in a tree git cannot
    # read, which is the failure mode the diff form had after merge.
    assert tracked, "the repository tracks no files, so this gate did not run"
    assert len(tracked) > 100, len(tracked)

    forbidden = [
        path
        for path in tracked
        if path.startswith("corpus/")
        or path.startswith("vendor/")
        or "/vendor/" in path
        or "fixtures/semantic-module" in path
    ]
    assert not forbidden, forbidden

    # Every tracked path belongs to this module rather than to a corpus or a
    # vendored copy of someone else's fixtures.
    allowed_prefixes = (
        "spec/",
        "spec_objects_security/",
        "tests/",
        "typespec/",
        "scripts/",
        "plan/",
        ".github/",
        ".agent/",
    )
    allowed_files = {
        "package.json",
        "package-lock.json",
        "pyproject.toml",
        "poetry.lock",
        "Makefile",
        "README.md",
        "AGENTS.md",
        "CLAUDE.md",
        "LICENSE",
        ".gitattributes",
        ".gitignore",
    }
    stray = [
        path
        for path in tracked
        if not path.startswith(allowed_prefixes) and path not in allowed_files
    ]
    assert not stray, stray


@pytest.mark.trace("TC-074", "FR-006-AC-5")
def test_the_markdown_path_cannot_express_embedded_material(
    quire_engine, semantic_module, bundle_index
):
    path = NEGATIVE_DIR / "secret-embedded-material-default.md"
    record = extract(quire_engine, semantic_module, bundle_index, path)
    codes = {d.get("code") for d in record.get("diagnostics", [])}
    assert "semantic.unknown-constraint-keyword" in codes, record.get("diagnostics")
