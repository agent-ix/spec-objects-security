---
id: SR-022
title: "Code review of PR #42 quire ^0.57.0 and semantic-core 0.4.4"
type: SpecReview
analysis: code-review
review_set: subset
scope: "agent-ix/spec-objects-security; pyproject.toml, poetry.lock, package.json, package-lock.json, typespec/main.tsp, spec_objects_security/schemas/*.json (26 changed), tests/conftest.py, tests/test_schema_emission.py, tests/test_skeletons_semantic.py (PR #42 diff, git diff origin/main...HEAD at 1b347ee)"
---
# SR-022: Code review of PR #42 quire ^0.57.0 and semantic-core 0.4.4

## Summary

Ticket: PLAT-350 (PR #42). The PR moves the Python binding to quire ^0.57.0
and the pinned grammar to `@agent-ix/semantic-core` 0.4.4, and adapts the one
model that names a `TypeRef` target, `OccurrenceTypeRef`, to the tagged form.
Tools: quoin 0.30.1, quire 0.57.0 (internal PyPI resolved), Python 3.13 venv.

Engine match, measured read-only:

- filament-core-data `origin/main` `packages/semantic-core/main.tsp` defines
  `union TypeRefTarget { SemanticId: {kind: "SemanticId"; value: SemanticId},
  KernelScalar: {kind: "KernelScalar"; value: KernelScalar} }`, introduced in
  semantic-core 0.4.0 (7a416a9a). The PR's `{kind: "KernelScalar"; value:
  KernelScalar.Timestamp}` is the `KernelScalar` arm exactly.
- quire-rs `v0.57.0` Cargo.lock embeds `agent-ix-semantic-schema` from
  filament-core-data `ce72bc51`, whose `packages/semantic-core/package.json`
  is 0.4.4 and whose semantic-core tree equals `origin/main`. Exact 0.4.4 is
  the version the engine embeds, and `scripts/generate-schemas.mjs` builds the
  `$id` base from the exact devDependency string, so an exact pin is required.
- `OccurrenceTypeRef` is the only model in `typespec/main.tsp` that names a
  `TypeRef` target. The other cross-references are `SemanticId` properties,
  which the tagged change does not touch.
- Generated schemas: 25 schemas carry semantic-core `$ref`s, all now
  `semantic-core/0.4.4/…`, and every referenced file (`ClauseRef`,
  `DefaultDecl`, `EnumValue`, `FieldDecl`, `Identifier`, `OperationDecl`,
  `RelationDecl`, `SemanticId`) exists in 0.4.4. The other 22 carry none and
  are unchanged. `OccurrenceTypeRef.json` matches the TypeSpec change. CI run
  43274055932 job `schemas-check` passed on 1b347ee. `make schemas-check` was
  not run here: it needs `@typespec/compiler` in `node_modules`, and this
  session has no registry access.
- `KERNEL_SCALARS` gaining `Float32`/`Float64` is justified: semantic-core
  0.4.4 `KernelScalar.json` enum is exactly the eleven names now listed.
- Lockfile test: the new assertion (every `resolved` URL starts with
  `https://registry.npmjs.org/`) is not vacuous. The lock has 70+ resolved
  entries, and the check fails on any `npm.pkg.github.com` or npm.ix URL. It
  is stricter than the old `@agent-ix/*` carve-out. filament-core-data's
  `schema-release.yml` publishes semantic-core to public npmjs.

Tests, run in a scratch worktree of 1b347ee with semantic-core 0.4.4 schema
bytes taken from filament-core-data `ce72bc51` (no registry):
198 passed, 1 xfailed, 4 failed. The 4 are the `tsp`-driven emission tests in
`tests/test_schema_emission.py`, failing with `MODULE_NOT_FOUND` because
`@typespec/compiler` is not installed. The two `test_manifest_engine_gate.py`
quoin tests passed with the local quoin 0.30.1, and the sha256 of
`~/.ix/filament/registry.json` was unchanged before and after. `origin/main`
under quire 0.57.0 fails `test_roundtrip_skeleton_validates[audit_event]`,
`test_every_skeleton_validates_with_no_error` and
`test_under_the_bundle_index_every_skeleton_extracts_clean`. The PR fixes all
three. ruff and black are clean. CI: 200 passed, 2 failed (the quoin CLI is
missing from the shared workflow; known and out of scope).

## Verdict

PASS with one low finding. The semantic change is correct for the engine,
the pins are right, and the test-helper changes keep their assertions.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | low | `KERNEL_SCALARS` is a hand-copied list of semantic-core's `KernelScalar` enum. It has already drifted once: this PR had to add `Float32`/`Float64` by hand. `field()` uses it to pick the `KernelScalar` or `SemanticId` arm, and `test_under_the_bundle_index_every_skeleton_extracts_clean` checks against it. Read the enum lazily from `node_modules/@agent-ix/semantic-core/generated/json-schema/KernelScalar.json`, which the schema-registry tests already require, instead of keeping a copy. | tests/conftest.py:213-227, tests/conftest.py:385-389, tests/test_skeletons_semantic.py:121 |

## Dispositions

| FND | outcome | reason |
|-----|---------|--------|
| FND-001 | fixed | `kernel_scalars()` in `tests/conftest.py` reads the enum from the installed semantic-core `KernelScalar.json` and fails with an actionable message when it is missing. The hand copy is deleted. |
