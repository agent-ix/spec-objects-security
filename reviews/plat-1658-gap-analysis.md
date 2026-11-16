---
id: SR-1621
title: "gap-analysis review — PLAT-1658 spec-objects-security"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-security; spec/functional/FR-028-processing-activity.md; typespec/main.tsp; spec_objects_security/manifest.yaml; spec_objects_security/schemas/ProcessingActivity*.json; tests/test_processing_activity.py; tests/test_regulated_categories.py"
review_set: subset
---

## Summary

The computed matrix has no test binders for any FR-028 acceptance criterion. The newly added `pytest.mark.trace` annotations do not back criteria because the module has no FR-028 rows in its trace matrix; the source tags consequently produce `criterion-tagged-outside-row` warnings. Plan completion was not assessed. Optional semantic review was skipped because it was not requested.

## Verdict

**FAIL** — all eight examined acceptance criteria are untagged in the computed Test Matrix.

## Scope

- Examined: FR-028-AC-1 through FR-028-AC-8, their test annotations, generated schemas, TypeSpec model, manifest relation and skeleton.
- Ticket: PLAT-1658; PR #69; reviewed published head `84b182f01a6db11c1c72c42f4b94442afe365268`.
- Plan completion: not assessed.
- Semantic review: skipped (not requested).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The computed Test Matrix reports FR-028-AC-1 through AC-8 as untagged with zero binders. `tests/test_processing_activity.py` contains trace markers, but `quire matrix` reports `criterion-tagged-outside-row` for these tags because no matrix row declares the new criterion ids; the tags do not establish coverage. | spec/functional/FR-028-processing-activity.md:57-64; tests/test_processing_activity.py:21-27,59-70,98-99 |

## Coverage

`quoin matrix --repo . --json` exited 0 and reported `static_status=untagged` and no binders for each FR-028-AC-1 through FR-028-AC-8. `quire matrix --scope . --format json` exited 0 and reported the added tags as `criterion-tagged-outside-row`; the report identifies the expected same-test tag in a declared matrix row, but none exists for these criteria. The module has no `spec/tests.md` row changes in this PR. Reverse-gap and stub scan found no other new unowned behavior or stubs in the reviewed change. The PR's schema generation check passed (67 schemas match). The focused test run produced 19 passes; 13 unrelated regulated-category tests failed because the active Python Quire wheel rejects a pre-existing `where` manifest field.


## New findings (round 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-002 | medium | FR-028's changed coverage behavior explicitly requires an advisory warning that does not make `quire validate` exit non-zero. The tagged no-covers test checks the warning location and text but never asserts `result.returncode == 0`, so it cannot catch a regression that emits the warning and still fails validation. A direct run currently returns 0. | spec/functional/FR-028-processing-activity.md:44; tests/test_processing_activity.py:160-174 |

## Dispositions

Round 1, published head 7e27cf4934f5c0e6dfc5dde0f7adfcd6c87d66b3.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | `spec/tests.md` now contains TC-248 through TC-255 rows for FR-028-AC-1 through AC-8. Quoin 0.35.0 and Quire 0.46.0 computed matrices both report all eight criteria tagged with their expected `tests/test_processing_activity.py` binders. |
| FND-002 | still-open | The warning test still checks only output text. Add an assertion that `result.returncode == 0` to enforce the explicit advisory/non-failing rule in FR-028 line 44. |

Round-1 verification note: schema generation check passed (67 schemas match). Focused Python tests: 9 passed, 1 failed. The remaining extraction assertion ran against globally installed Python Quire 0.53.0 while the repository requires `quire >=0.61.0`; it returned an empty record for the processor fixture. Matrix evidence came from Quoin 0.35.0 and npm Quire CLI 0.46.0 / engine 0.61.0.
