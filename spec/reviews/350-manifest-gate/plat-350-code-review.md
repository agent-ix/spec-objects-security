---
id: SR-019
title: "Code review of PR #41 manifest accepted by the engines' schema gate"
type: SpecReview
analysis: code-review
review_set: subset
scope: "agent-ix/spec-objects-security; tests/test_manifest_engine_gate.py (PR #41 diff, git diff origin/main...HEAD at 29c7445)"
---
# SR-019: Code review of PR #41 manifest accepted by the engines' schema gate

## Summary

Ticket: PLAT-350. Reviewed the new test module `tests/test_manifest_engine_gate.py`
(three tests tagged TC-115 / FR-003-AC-7). Tools: quire 0.40.0 (engine 0.56.0),
quoin 0.30.1, Python 3.13 venv.

Focused run: the three new tests pass. In `tests/test_manifest.py`,
`tests/test_manifest_semantic.py` and `tests/test_quoin_install_roundtrip.py`,
one test fails (an empty registry from the stale quire binding) and one errors
(semantic-core not installed). Both are known environment failures. The PR
changes none of those files, so the result is the same as the baseline.

Checks that passed:

- No schema, fixture, hash or pin was added. The diff touches six files, and
  the only one under `tests/` is the new test module.
- The negative tests bite. Done by hand, a manifest with `bogus_key` makes
  `quire validate --okf --module` exit 3 and name `bogus_key`. A manifest with
  `semantic.foo` makes `quoin module install` exit 1 and name `semantic.foo`.
- The positive test would fail on an invalid manifest. Each engine refuses
  its own mutation. `quire validate --module` replaces ambient discovery, so
  it reads the PR copy and not the installed module.
- A missing CLI fails the test and does not skip it. With PATH stripped, all
  three tests fail with "the `quire` CLI is not on PATH ... Install the
  Quoin/Quire release (npm i -g @agent-ix/quoin @agent-ix/quire-cli)".

## Verdict

FAIL. The quoin "isolated config root" is not isolated. Every run of the
positive test overwrites the user's real default install of
`spec-objects-security`.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | high | `IX_CONFIG_ROOT` does not redirect `quoin module install`. quoin 0.30.1 still reports `targetPath: ~/.ix/filament/modules/spec-objects-security` and rewrites `~/.ix/filament/registry.json`. The positive test therefore replaces the user's default `spec-objects-security` (git-subdir `v0.11.0`) with the PR copy, and leaves the registry entry pointing at a pytest tmp dir that is then deleted. Every quire/quoin session on the machine then sees the PR's module content. Reproduced: the registry mtime changed during the run. The real install had already been replaced about 2 min before this review, which fits an earlier run of this test. Restored with `quoin module install github:agent-ix/spec-objects-security//spec_objects_security@v0.11.0`. Fix: give the quoin subprocess `HOME=<tmp_path>/home`. Verified: targetPath then lands under the tmp HOME and the real registry is untouched. Then drop the `IX_CONFIG_ROOT` claim. | tests/test_manifest_engine_gate.py:55-63, tests/test_manifest_engine_gate.py:66-72 |
