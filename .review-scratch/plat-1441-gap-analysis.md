---
id: SR-1608
title: "Gap analysis — PLAT-1441 regulated-data categories on data_classification"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-security; typespec/main.tsp, spec_objects_security/manifest.yaml, spec_objects_security/schemas/, spec_objects_security/skeletons/data_classification.md, tests/test_regulated_categories.py, tests/fixtures/regulated-categories/, spec/tests.md"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-023
    type: reviews
  - target: ix://agent-ix/spec-objects-security/NFR-004
    type: reviews
---
# SR-1608: Gap analysis — PLAT-1441 regulated-data categories on data_classification

## Summary

Ticket: PLAT-1441. PR agent-ix/spec-objects-security#62 (draft) at head `4702982a697c35513fb35673031774249aafdc62`. Scope was re-measured against merged FR-023 and NFR-004 and against the ticket's module-side scope: the enum, the optional frontmatter list, schema emission, the skeleton and tests. The ticket's engine and cross-repo items (quoin FR-121/FR-123, quire-rs FR-058/069/081/084, quire-cli FR-030, spec-objects-architecture FR-013, ticket AC-10 `quire relations`) are delivered in other PRs and were not counted against this one.

Plan completion: not assessed (planless).

Evidence used: `quoin matrix --json` (quoin 0.34.0) over the PR head; focused pytest runs on the pinned quire 0.58.0 and on a local wheel built from the quire-rs#690 head; and reading the diff. Every criterion has a test that names it in a `trace` marker. Code that belongs to no requirement: none, since every added line traces to FR-023 or NFR-004. Stubs or skipped tests: none. No paywalled text was found in the enum doc, the skeleton or the manifest comment (ticket AC-7).

## Verdict

**GAPS FOUND.** Four gaps:

- The computed matrix gives FR-023 and NFR-004 no coverage.
- Two NFR-004 clauses about `level` are not asserted.
- FR-023-AC-6 is tested only at the schema layer.
- Releasing quire-rs#690 will break five existing skeletons. The required version bump will then fail ticket AC-6 ("existing tests stay green") unless the skeletons or the engine are fixed first.

Examined units (role: examined): FR-023-AC-1 to AC-10 and NFR-004-AC-1 to AC-3, NFR-004-M-1 and NFR-004-M-2. Clean units, where the module side is complete and the test asserts the criterion: FR-023-AC-1, AC-2, AC-3, AC-4, AC-5, AC-7, AC-8, NFR-004-AC-2, NFR-004-M-1 (also covered by the all-schema `default_keywords` test in `tests/test_security_rules.py`) and NFR-004-M-2. AC-1, AC-9 and AC-10 are clean only once SR-1607 FND-001 to FND-003 are fixed.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | `quoin matrix` reports every FR-023 and NFR-004 criterion as `untagged` with reason `tagged-without-citing-matrix-row`: the tests cite TC-RC-01 to TC-RC-12, which TM-001 does not declare, and `spec/tests.md` has no FR-023 or NFR-004 rows | spec/tests.md:149 |
| FND-002 | medium | NFR-004-AC-3's clause "a classification without `level` extracts no `level` key" is not asserted. TC-RC-09 is tagged NFR-004-AC-3 but checks only `regulatedCategories` | tests/test_regulated_categories.py:166 |
| FND-003 | low | NFR-004-AC-1's `level` half is not asserted: no test checks that the manifest has no other locator and no `assert` or default that yields `level`. TC-RC-06 checks only the `regulated_categories` locator | tests/test_regulated_categories.py:126 |
| FND-004 | medium | FR-023-AC-6 ("`level: restricted` with `[health]` validates") is checked only against hand-built records in the schema validator (TC-RC-03). No fixture that states both a level and a category goes through `quire validate` | tests/test_regulated_categories.py:100 |
| FND-005 | medium | On the quire-rs#690 engine, five existing skeletons fail `semantic.record-invalid`: permission, encryption_key, csrf_token, mfa_method and threat. Their frontmatter keys are now projected into the closed record. The `data_classification` skeleton passes. Bumping quire to the #690 release, which this PR requires, will make `test_roundtrip_skeleton_validates` and `test_every_skeleton_validates_with_no_error` fail | spec_objects_security/skeletons/ |
