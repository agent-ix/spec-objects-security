---
id: SR-1600
title: "Gap analysis — scope exclusion dispositions"
type: SpecReview
analysis: gap-analysis
review_set: subset
scope: "agent-ix/spec-objects-security; FR-016 and PR #55's manifest, schemas, skeleton, tests, and trace rows (head 8aaa49d)"
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-016"
    type: references
---
# SR-1600: Gap analysis — scope exclusion dispositions

## Summary

The computed Quoin matrix reports every FR-016 criterion AC-1 through AC-9 as statically tagged. In the changed behavior, the manifest extracts `decision`, `decision_owner`, and `approval_ref` under their authored keys, the schema types `decision_owner` as a `SemanticId`, and the fixture test checks extraction without an `owner` key.

## Verdict

**PASS** — no traceability, reverse-specification, or stub gap was found in the changed scope.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |

## Coverage

- Computed with `quoin matrix --repo <PR worktree> --json` on Quoin 0.30.1. FR-016-AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, and AC-9 are all statically tagged. AC-8 binds to `test_validated_fixtures_emit_exactly_the_keys_the_author_wrote`; AC-9 binds to `test_exclusion_decisions_and_conditional_rfc3339_expiry`. The matrix reports no run evidence.
- The full repository matrix has nine untagged criteria outside this PR's changed requirement scope: FR-001-AC-2/3/4, FR-003-AC-5, FR-008-AC-7/8/9/10, and FR-013-AC-7. None is an FR-016 criterion or introduced by this diff.
- Reverse gap: every changed manifest/schema/TypeSpec/skeleton behavior is owned by FR-016; the changed assertions bind to FR-016 and NFR-003. No stub or coverage inflation was found.
- The `spec/tests.md` summary and some TC titles are stale; the code-review artifact records that finding. The computed matrix, not that hand-maintained table, was used to establish criterion coverage.
- Semantic review: skipped; it was not requested. Plan completion: not assessed.

