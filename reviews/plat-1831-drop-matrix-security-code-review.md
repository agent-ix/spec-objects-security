---
id: SR-20261116045017
title: "Code review of PLAT-1831 spec-objects-security PR #78 (drop hand-kept test matrix)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-security; spec/tests.md (deleted), spec/spec.md, tests/test_*.py (25 files)"
review_set: subset
---

## Summary

Ticket: PLAT-1831. Reviewed `git diff origin/main...HEAD` at a45633520ea928ac733bed3f6ed52cdf69ad2cf6 (spec-objects-security PR #78; merge-base is current origin/main 0e61c8c, which includes #77; GitHub reports MERGEABLE) in a fresh temp clone. The diff deletes `spec/tests.md` (448 lines) and its line in the `spec/spec.md` layout list. It strips `TC-NNN` ids from trace markers and docstrings in 25 test files, deletes TC-only markers (`TC-182`, `TC-183`, `TC-186`, `TC-114`), removes the now-unused `import pytest` from `test_quoin_install_roundtrip.py`, and rewords two docstrings that named TC rows (27 files, +270/-728).

Toolchain: `npm ci` from registry.npmjs.org (quoin 0.36.10, quire-cli 0.52.1), throwaway `HOME` with `quoin module ensure-defaults`. For pytest: `poetry install --no-root` into an in-clone Python 3.13 `.venv`.

## Verdict

**APPROVE**, with two low wording findings (stale matrix status marks). Neither blocks the merge.

- Matrix unchanged: `quoin matrix --json` at origin/main and at head lists the same 32 requirements and 240 criteria. With only `line`/`column` removed, the two documents are identical (210 tagged, 17 method-without-symbol, 13 untagged; 306 binders).
- No AC id dropped: a per-file count of every non-`TC-` id (FR/NFR/StR AC, CON, M ids) on removed lines equals the count on added lines in all 27 files. The only removed lines that do not reappear with their TC tokens taken out are four TC-only decorators, the unused `import pytest`, and two reflowed docstrings. The reflow in `test_regulated_categories.py` keeps all AC ids (multi-line marker joined into one line).
- References: outside `reviews/`, `spec/reviews/` and `plan/`, no reference to `tests.md`, `TC-NNN`, "test matrix" or "Test Case Summary" remains. `TM-001` remains only in `spec_objects_security/skeletons/threat_model.md`, which is sample data. Two prose mentions of the deleted matrix's status marks remain (FND-001, FND-002).
- `quire validate "spec/**/*.md"` exits 0 at head and at main, with no warnings and no errors.
- No behaviour change: the test diff is trace-marker arguments, docstrings and one unused import. No conftest hook reads trace markers. `ruff check tests` and `black --check tests` pass.
- pytest collection: in the repo's declared environment (Python 3.13 poetry venv, `npm ci`'d `node_modules`), `pytest --collect-only` collects 498 tests with 0 errors at both head and main. Main is not broken. The coder's 19 errors are reproduced exactly by running the system Python 3.10 user-site pytest: `~/.local/lib/python3.10/site-packages/_ix_workflow_runner.pth` puts `/home/peter/dev/ix-workflow-runner` on `sys.path`. Its `tests/` is a regular package (`__init__.py`). This repo's `tests/` has no `__init__.py`, so it is a namespace portion, and Python resolves the regular package first even though `pythonpath = ["."]` puts this repo earlier on the path. The 19 test files that do `from tests.conftest import ...` then fail with `ImportError: cannot import name ... from 'tests.conftest' (/home/peter/dev/ix-workflow-runner/tests/conftest.py)`. This is an environment problem, not a PR or main defect. It is noted for the lead: any environment with another regular `tests` package on the path shadows this suite.

Gap analysis did not run: the diff has no production code. The matrix comparison above covers the trace effect.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The module docstring still says the IT-002 success criteria "stay `Manual` and `🚧`". Those are the status marks of the deleted `spec/tests.md` row TC-110, which no longer exist anywhere, so the sentence cites a superseded status record. | tests/test_quoin_install_roundtrip.py:3 |
| FND-002 | low | The Out of scope prose still says activation (FR-001-AC-2) "is `🚧` here". That is the deleted matrix's status mark for the row. The generated matrix carries no such mark, so it is a leftover matrix status reference. | spec/spec.md:69 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | low | The replacement wording says activation (FR-001-AC-2) "is verified outside this module". It is verified inside this module: `tests/test_activation_core.py:278` `test_activation_noop_hash_and_contribution_tables` carries `@pytest.mark.integration` and `@pytest.mark.trace("FR-001-AC-2")` and activates against a deployed filament-core. The sentence should say the check is this repo's integration test, which needs a running filament-core (Kind cluster) and is outside the default `-m 'not integration'` run. | spec/spec.md:69-70 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | f8768ee rewrites the docstring with no `Manual`/`🚧` marks; the new text is accurate (the file has no trace marker, so it does not cover IT-002). |
| FND-002 | fixed | f8768ee removes the `🚧` mark from spec/spec.md:69; the replacement claim's own inaccuracy is FND-003. |
