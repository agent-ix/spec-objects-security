---
id: SR-027
title: "Base spec review of the SOUP record object (FR-009..FR-012, NFR-001)"
type: SpecReview
analysis: base
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-009..FR-012, spec/non-functional/NFR-001, spec/functional/index.md, spec/non-functional/index.md, spec/index.md, spec/tests.md (PR #44 diff)"
---
# SR-027: Base spec review of the SOUP record object (FR-009..FR-012, NFR-001)

## Summary

Ticket: PLAT-1512. PR agent-ix/spec-objects-security#44, head `plat-1512-soup-spec`
(81febbe). Review set: subset — base plus integrity, dependency, ears-conformance and
scope-boundary (SR-028..SR-031). No AssuranceProfile document exists in the repository, so
no profile requires an enforced review run.

Examined: FR-009 (Behavior, CON-1..2, AC-1..8), FR-010 (Behavior, CON-1, AC-1..6), FR-011
(Behavior, CON-1, AC-1..8), FR-012 (Behavior, AC-1..5), NFR-001 (Statement, Measurement,
AC-1..2), the three index edits, and the `spec/tests.md` additions (five `covers` edges,
five coverage rows, TC-121..TC-149). Context read: `spec/spec.md`, FR-003..FR-008,
`spec_objects_security/manifest.yaml`, quoin FR-041, FR-135 and its disposition fact
implementation, engineering-assurance FR-030 and FR-038, spec-artifacts-iso FR-004 and its
edge vocabulary.

`quire validate --scope .` over the nine changed files: no document error (exit 0; only the
unrelated module-load diagnostics `semantic.unused-import` and `DuplicateModuleName`).

ID formats are correct, sequential and unique (FR-009..FR-012, NFR-001, AC/CON ids,
TC-121..TC-149). Index entries match their files and titles. Every new AC has a TC row.

Hash / digest / pin check: clean. Identity is the purl as text (FR-009-CON-1), and FR-009
forbids any digest as identity. No ledger, manifest, SHA or version record is introduced.

`spec/tests.md`: the 29 new `🚧` TC rows follow this repository's convention, not ceremony.
TM-001 states rows are `🚧` until a tagged test asserts them, and the previous spec-only PR
(#39, FR-007) added `🚧` TC-091/TC-092 that the implementation PR (#40) flipped to `✅`.
The rows are the test plan the implementation PR tags against.

No paywalled standard text or name is used (CycloneDX, SPDX and purl are open). No roadmap
content beyond FR-012's one-line pointer that the advisory join is out of scope.

## Verdict

FAIL. This file holds two minor findings. The blocking findings are high findings in SR-028
(integrity), SR-029 (dependency) and SR-031 (scope-boundary).

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | medium | FR-009-AC-4 cannot fail on the defect it targets. Its second clause ("a record whose only distinguishing field is a digest and whose purl is absent fails") is FR-009-AC-2's purl-absent case again. The first clause ("no identity field is a digest") names a schema notion, "identity field", that the schema does not have. Neither clause fails if a digest is used as identity. A falsifiable form: two records with equal purls and different digests are reported as duplicates. | spec/functional/FR-009-soup-record-identity-and-promotion.md:74 |
| FND-002 | low | The `spec/tests.md` StR-001 and US-001 coverage rows still trace `FR-001..FR-008`, but FR-009..FR-012 `implements` US-001. | spec/tests.md:81, spec/tests.md:87 |

## Dispositions

| FND | outcome | reason |
|-----|---------|--------|
| FND-001 | fixed | Fixed in 3d75c3d. FR-009-AC-4 now reads "A fixture that adds a `digest` key to an otherwise valid record fails, and a fixture whose only difference from a valid record is a different digest-free purl validates as a distinct component." That test fails if a digest is admitted. |
| FND-002 | fixed | Fixed in 3d75c3d. The `spec/tests.md` StR-001 row traces "US-001, FR-001..FR-012, NFR-001", and the US-001 row says "implemented by FR-002..FR-012". |
