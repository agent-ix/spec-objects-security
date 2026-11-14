---
id: SR-1599
title: "Code review — scope exclusion dispositions"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-security; spec_objects_security/manifest.yaml, spec_objects_security/schemas/ScopeExclusion*.json, spec_objects_security/skeletons/scope_exclusion.md, typespec/main.tsp, tests/test_typed_controls.py, tests/conftest.py, tests/test_role_schemas.py, spec/tests.md (PR #55, head 8aaa49d)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-016"
    type: references
---
# SR-1599: Code review — scope exclusion dispositions

## Summary

Reviewed the PR #55 disposition contract in the module manifest, generated JSON Schemas, TypeSpec source, skeleton, and tests. The schema and extraction changes match FR-016's decision-owner and conditional-expiry contract; the remaining finding is stale test-matrix descriptions.

## Verdict

**CONDITIONAL** — one low-severity documentation inconsistency remains in `spec/tests.md`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The FR-016 summary and TC-198/199/203 descriptions in the hand-maintained test catalog still describe the old four-field exclusion contract. TC-199 says decisions and approval are not admitted, while this PR admits typed decisions and an approval reference; TC-203 says four locators although the manifest now has seven required locators plus optional expiry; the summary still stops at AC-7 and TC-203, omitting AC-8/9 and TC-205. Update these descriptions and the summary ranges to reflect the new rows and assertions. | spec/tests.md:147,314-319 |

## Coverage

The code-review pass checked duplication, boundary behavior, the authored-section to schema contract, test intent, generated-schema assertions, and the diff's alignment with FR-016. No AssuranceProfile applies. No test or aggregate gate was run in this review pass; the code lead owns the post-review gate.


## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | still-open | The summary now covers AC-1..9 and TC-205, and TC-199/203 no longer contradict the typed decision and locator contract. However, TC-198 still does not name the new `decision_owner` and `approval_ref` assertions, so the catalog description remains incomplete against the finding. |
