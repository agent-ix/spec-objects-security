---
id: SR-023
title: "Gap analysis of PR #42 quire ^0.57.0 and semantic-core 0.4.4"
type: SpecReview
analysis: gap-analysis
review_set: subset
scope: "agent-ix/spec-objects-security; typespec/main.tsp, spec_objects_security/schemas/OccurrenceTypeRef.json, package-lock.json, tests/conftest.py, tests/test_schema_emission.py, tests/test_skeletons_semantic.py against spec/functional/FR-002, FR-004, FR-005, spec/usecase/US-001 and spec/tests.md (PR #42 diff at 1b347ee)"
---
# SR-023: Gap analysis of PR #42 quire ^0.57.0 and semantic-core 0.4.4

## Summary

Ticket: PLAT-350 (PR #42). Plan completion: not assessed (planless). The
matrix comes from `quoin matrix --repo . --json` (quoin 0.30.1). The four
criteria the diff's tests bind to are each bound:

- FR-002-CON-4 is bound to `test_the_lockfile_resolves_public_packages_from_npmjs`.
- FR-004-AC-9 is bound to `test_audit_event_declares_an_occurrence_and_not_a_record`.
- FR-004-AC-12 is bound to `test_an_unresolved_placeholder_is_a_semantic_id_and_a_bare_token_is_not`.
- FR-005-AC-3 is bound to `test_under_the_bundle_index_every_skeleton_extracts_clean`.

The four tests pass on the PR head when semantic-core 0.4.4 bytes are
present. Across the repo, 4 of 61 criteria are unbound: FR-001-AC-2/3/4 and
FR-003-AC-5. The PR does not touch them, so they are outside this diff.

The FR-004-AC-12 negative still bites. `{kind: "SemanticId", value:
"Mystery"}` fails semantic-core's `SemanticId` pattern
`^ix://[a-z0-9][a-z0-9._-]*/…`, so the rejection is for the right reason.

The code is right. The spec text describing it is not. The PR changes two
behaviours the spec states explicitly and leaves the spec saying the old
thing. In each case the changed test now asserts the opposite of, or a
different shape from, the requirement it is traced to.

## Verdict

FAIL on spec-code agreement: two medium findings. Both can be fixed in this
PR with text edits. No code change is needed.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | medium | FR-002-CON-4 says `@agent-ix/semantic-core` resolves from `npm.pkg.github.com`. The TC-032 row in `spec/tests.md` says the lock resolves every package from npmjs "except `@agent-ix/semantic-core` (GitHub Packages)". The PR's TC-032 test, still traced to FR-002-CON-4, now asserts the opposite: every package resolves from npmjs. The same stale claim is in FR-002 Inputs ("semantic-core from GitHub Packages"), in US-001 Dependencies, and in the `schema_registry` failure message in `tests/conftest.py`. Fix: restate CON-4 as "`package-lock.json` SHALL resolve every package, `@agent-ix/semantic-core` included, from `registry.npmjs.org`". Update the TC-032 row, FR-002 Inputs, US-001 and the conftest message to match. | spec/functional/FR-002-emitted-json-schemas.md:73, spec/tests.md:137, spec/functional/FR-002-emitted-json-schemas.md:28, spec/usecase/US-001-declare-security-objects-against-semantic-core.md:78, tests/conftest.py:343 |
| FND-002 | medium | FR-004 Behavior still defines the occurrence field as a `FieldDecl` "whose `type.target` is `Timestamp`" and says "the kernel scalar is the bare token `Timestamp`". It then says a semantic-core release that namespaces kernel scalars is a breaking change, which "this module SHALL answer with a manifest version bump". semantic-core 0.4.x replaced the bare token with `{kind: "KernelScalar", value: "Timestamp"}`. The PR adapts `OccurrenceTypeRef`, which is breaking for a record that carries the bare string. It neither updates the FR-004 reading nor does what the clause demands: the manifest `version` stays 0.2.0. That clause is version-tracking ceremony. The manifest has stayed at 0.2.0 through semantic-core 0.1.0→0.3.2 and twelve release tags, and nothing enforces it. Fix: restate the reading as `type.target` = `{kind: "KernelScalar", value: "Timestamp"}` and delete the version-bump sentence; do not bump. While editing, change FR-005-AC-3's "every non-kernel `type.target` starts with" to `type.target.value`. Also align FR-004-AC-12's "a bare `Mystery` string" with what is tested: a `SemanticId`-tagged `Mystery` that fails the pattern. | spec/functional/FR-004-role-schemas.md:47-56, spec/functional/FR-005-executable-skeletons.md:83, spec/functional/FR-004-role-schemas.md:124, typespec/main.tsp:174-180 |

## Dispositions

| FND | outcome | reason |
|-----|---------|--------|
| FND-001 | fixed | Verified on 3709c28. FR-002-CON-4 now reads "`package-lock.json` SHALL resolve every package, `@agent-ix/semantic-core` included, from `registry.npmjs.org`". FR-002 Inputs, US-001 Dependencies, the TC-032 row and the `schema_registry` failure message all say npmjs. No "GitHub Packages" or `npm.pkg.github.com` is left in `spec/` (outside historical reviews) or `tests/`. The lock has 85 resolved entries, all on `registry.npmjs.org`, including the new exact-pinned `@agent-ix/quoin` 0.30.1 and `@agent-ix/quire-cli` 0.41.0 and their platform packages, so TC-032 still fails on any other host. |
| FND-002 | fixed | Verified on 3709c28. FR-004 Behavior defines the occurrence field as `type.target` = `{kind: "KernelScalar", value: "Timestamp"}` and states the tagged reading for both arms. The manifest-version-bump sentence is deleted and the manifest stays 0.2.0. FR-005-AC-3 reads `type.target.value` (kind `SemanticId`), and FR-004-AC-12 names the `SemanticId`-tagged `Mystery` with no `ix://` prefix. `quire validate` exits 0 on every changed spec file. The remaining "bare token" phrases (FR-004 line 91, TC-061) refer to non-`ix://` type tokens, not the kernel scalar, so they are accurate. |
