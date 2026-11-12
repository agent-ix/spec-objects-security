---
id: SR-024
title: "Code review of PR #43 reverse mitigates rule for security NFRs"
type: SpecReview
analysis: code-review
review_set: subset
scope: "agent-ix/spec-objects-security; spec_objects_security/manifest.yaml, tests/test_reverse_mitigates.py, tests/test_manifest.py, pyproject.toml, poetry.lock (PR #43 diff, git diff origin/main...HEAD at 8f26af7)"
---
# SR-024: Code review of PR #43 reverse mitigates rule for security NFRs

## Summary

Ticket: PLAT-1477 (PR #43). The PR declares `security-nfr-has-mitigation-target`
(`from: NFR`, `where: {field: quality_attribute, values: [security]}`,
`edges: [mitigates]`, `to: []`, `direction: outgoing`,
`check: unjustified-security-nfr`) and tests it with the real `quire` CLI.
Tools: quire 0.43.0 (engine 0.58.0) and quoin 0.30.1 on PATH, Python 3.13
venv from `poetry install` (quire 0.58.0, spec-artifacts-iso 0.22.1).

Measured:

- Schema: the PR manifest validates with 0 errors against filament-core-data
  `schema/semantic/v1/module-manifest.schema.json`. That file is identical
  at tag `semantic-schema-v0.6.0` and at `origin/main` (e29f23af, PLAT-1482).
  The schema rejects an extra `where` key, empty `values` and a missing
  `field`.
- Engine: `tests/test_manifest_engine_gate.py` passes 3/3 against the
  ambient quire 0.43.0 and quoin 0.30.1. No `node_modules` was present, so
  `_tool()` fell back to PATH. The sha256 of `~/.ix/filament/registry.json`
  was the same before and after every run.
- CI run 43284621578 fails only those 2 engine-gate tests. Both fail
  because `node_modules/.bin/quire` (the `@agent-ix/quire-cli` 0.41.0
  devDependency) rejects `where` with "unknown field `where`". All other
  tests passed: 204 passed, 1 xfailed. Bumping quire-cli to 0.43.0 fixes
  both. The quoin 0.30.1 pin needs no change, because the gate passes with
  quoin 0.30.1.
- Mutation testing on the manifest, over `test_reverse_mitigates.py` and
  `test_manifest.py`. Each of these mutations made at least one test fail:
  - rule removed
  - `where` dropped
  - `values: [safety]`
  - `values` plus `performance_efficiency`
  - `field` renamed
  - `edges: [threatens]`
  - `edges` plus `refines`
  - `direction: incoming`
  - `to: [threat, risk]`
  - `check` renamed
  - `from: FR`
  - module `grammar_severity` set to `error`
  - module `grammar_severity` set to `off`

  The `grammar_severity: error` mutation fails only TC-117, which asserts
  exit 0. TC-119 still passes under it (FND-001).
- Advisory behaviour: under `--okf`, the run exits 0 and the finding is
  reported as a warning. `--severity trace:unjustified-security-nfr=error`
  makes the run exit 3, and the finding becomes an error. `=off` drops it.
- No vendored copies. The iso skeleton is read from the installed wheel
  through `importlib`. ruff and black were not run on their own; CI's lint
  job was not in the failed log.

## Verdict

CHANGES REQUESTED, on FND-001 (test) together with the spec half in SR-026.
The rule shape is right, the engine accepts it and the tests are live.
The other two findings are a harness degradation (FND-002) and a nit (FND-003).

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | medium | TC-119 never checks the strict half of FR-008-AC-5. The `--strict` run asserts only that one finding is present. It asserts neither the exit code nor that the finding is still a warning. Measured on this fixture, `--okf --strict` exits 3: the iso-loaded NFR is an `unknown-type` error under strict. A module-level `grammar_severity: {trace:unjustified-security-nfr: error}` mutation leaves TC-119 green. Assert `_findings(strict)[0].startswith("warning:")`, and drop or restate the exit-0 claim (SR-026 FND-001). | tests/test_reverse_mitigates.py:121-129 |
| FND-002 | medium | The harness never applies the iso `NFR` archetype. Every fixture NFR is reported as "unknown type 'NFR' tolerated under OKF posture [unknown-type]" because `--module <site-packages>/spec_artifacts_iso` (0.22.1, and 0.24.0 too) registers no artifact types. Bisected: deleting the retired `semantic.semantic_core: 0.3.2` line from the wheel manifest restores registration. The installed `~/.ix/filament/modules/spec-artifacts-iso` copy registers NFR. The docstring says both modules are loaded, but the NFR frontmatter schema and `allowed_links` are never exercised. The `where` path still works because it reads raw frontmatter. This is an upstream iso/engine defect: route it to the owner. Here, either state the limitation or assert no `unknown-type` once upstream is fixed. | tests/test_reverse_mitigates.py:1-7, tests/test_reverse_mitigates.py:62-76 |
| FND-003 | low | `_quire()` resolves `quire` from PATH only. `_tool()` in `tests/test_manifest_engine_gate.py` prefers `node_modules/.bin`. One suite therefore runs two different engines. In CI they are 0.43.0 on PATH and the 0.41.0 devDependency, which is why only the gate failed. Reuse one resolver so the suite tests one engine. | tests/test_reverse_mitigates.py:32-36, tests/test_manifest_engine_gate.py:23-32 |
| FND-004 | low | The TC-007 docstring still states the old criteria: "`direction` is `incoming`" and "every `from` names an object type this module declares". The body now exempts `security-nfr-has-mitigation-target` from both (outgoing, `from: NFR` owned by iso). Update the criteria to match the special case. | tests/test_manifest.py:96-100, tests/test_manifest.py:128-136 |

## Dispositions

| ID | Disposition |
|----|-------------|
| FND-001 | Fixed in round 1: TC-119 asserts the strict finding is a `warning:`. |
| FND-002 | Fixed in round 1: fixtures use `ix://` targets, a `_registered()` guard fails on `unknown type 'NFR'`, and the iso dev dependency is `^0.25.0`, which registers the type. |
| FND-003 | Fixed in round 1: one `engine_tool()` lookup in `tests/conftest.py` (node_modules/.bin first, then PATH) is used by the reverse tests and the engine gate. |
| FND-004 | Fixed in round 1: the TC-007 docstring states the outgoing NFR exception. |
