---
id: SR-052
title: "Gap analysis of PR #53 typed controls and scope_exclusion"
type: SpecReview
analysis: gap-analysis
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-014-control-mappings-are-clause-references.md, spec/functional/FR-015-mappings-carry-no-standard-text.md, spec/functional/FR-016-scope-exclusion-object.md, spec/non-functional/NFR-003-clause-references-state-and-never-derive.md, tests/test_typed_controls.py (PR #53, git diff origin/main...HEAD at bc6eba1)"
---
# SR-052: Gap analysis of PR #53 typed controls and scope_exclusion

## Summary

Ticket: PLAT-1427. Planless. The matrix was computed with `quoin matrix --repo
<worktree> --json` on quoin 0.30.1.

- All 17 criteria of FR-014 (AC-1..7), FR-015 (AC-1..3) and FR-016 (AC-1..7) are
  `tagged`, each by one test in `tests/test_typed_controls.py`, and all of those
  tests pass. Their evidence status is `no run evidence`, because no run evidence
  was recorded.
- NFR-003 constrains FR-014 and FR-016. Its scope is the `ControlMapping` and
  `ScopeExclusion` schemas, skeletons and manifest entries that this PR ships.
  Its criteria NFR-003-AC-1 and NFR-003-AC-2 are `untagged`, and so are its
  metrics NFR-003-M-1 and M-2.
- Reverse gap: every changed source line is owned by FR-014, FR-015, FR-016 or
  FR-004. No stubs were found and there is no coverage inflation; the coverage
  denominator is the 4-statement `__init__.py` and it is unchanged.
- quoin FR-171, FR-172 and NFR-038 were read as context only. Their criteria are
  over the quoin skill and `facts-from-mappings`, not over this module. The keys
  `nist/sp800-53@5.2.0` and `owasp/asvs@5.0.0` appear in FR-014, which FR-172-AC-6
  asks for. FR-017 was not changed by this PR.
- Pre-existing untagged criteria outside this PR (for example FR-001-AC-2..4,
  FR-008-AC-7..10) are not findings here.

## Verdict

**FAIL** under the verdict rule, because two criteria are untagged:
NFR-003-AC-1 and NFR-003-AC-2. TC-196 and TC-197 already pin the exact property
sets, so NFR-003-AC-1 holds in fact and only needs a test bound to it. One
medium finding is also open: half of FR-015-AC-2 is not asserted.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | NFR-003-AC-1 (no property named or typed as coverage, compliance, score, percentage, rating or status in `ControlMapping.json` or `ScopeExclusion.json`) and NFR-003-AC-2 (validating a fixture control and exclusion emits exactly the keys the author wrote) have no test tagged with their ids. NFR-003 constrains FR-014 and FR-016, and its scope is exactly the schemas this PR emits. Fix: add a test that scans both schemas' property names and types for the six terms (`@pytest.mark.trace(..., "NFR-003-AC-1")`). Add a second test that extracts the skeleton control and exclusion and asserts that the record keys equal the authored sections (`NFR-003-AC-2`) | spec/non-functional/NFR-003-clause-references-state-and-never-derive.md:37-38, tests/test_typed_controls.py |
| FND-002 | medium | FR-015-AC-2 has three parts: `semantic.invalid-model-cell` with reason `column-unknown` at the header line; an extracted record with no `mappings` key (`unavailable`); and none of the column's values in that record. TC-195 asserts only the first, by the message `header ... matches no property` and the line. It never extracts the record, so a regression that kept the third column's values in `mappings` would pass. The engine's error dict carries `reason: semantic`, not `column-unknown`. Fix: run `extract_semantic` on the three-column fixture and assert that there is no `mappings` key and that a sentinel cell value is absent. Either assert `column-unknown` from wherever the engine exposes it, or amend the AC to the observable message | tests/test_typed_controls.py:168-185, spec/functional/FR-015-mappings-carry-no-standard-text.md:39 |

## Coverage

- Criteria in scope: 19 (FR-014 ×7, FR-015 ×3, FR-016 ×7, NFR-003 ×2). 17 are
  tagged and 2 are untagged.
- Semantic review: not run as a separate pass. The intent checks that were done
  are recorded in SR-051 and in the findings above.
- Plan completion: not assessed
