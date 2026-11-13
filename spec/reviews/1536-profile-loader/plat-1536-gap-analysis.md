---
id: SR-050
title: "Gap analysis of PR #52 source profile format test"
type: SpecReview
analysis: gap-analysis
review_set: subset
scope: "agent-ix/spec-objects-security; tests/test_profiles.py (PR #52 at 135be4a), read against spec/functional/FR-020-source-profile-format.md, spec/functional/FR-021-default-source-profiles.md, spec/non-functional/NFR-002-profiles-never-name-or-carry-licensed-content.md and spec/tests.md"
---
# SR-050: Gap analysis of PR #52 source profile format test

## Summary

Ticket: PLAT-1536. Plan completion: not assessed (planless). The PR adds only
tests. No production code or `profiles/` data ships, so there is no code
without an owning requirement and no stub.

Every Test-method AC has a test that asserts it:

- FR-020-AC-1..5: synthetic fixtures.
- FR-020-AC-6: the manifest-key half only (FND-002).
- FR-021-AC-1, AC-2, AC-3, AC-5 and NFR-002-AC-1, AC-2: over shipped profiles,
  plus a synthetic-module lookup test.
- FR-021-AC-4, AC-6, AC-7 are Inspection.

None of the shipped-profile cases runs yet, because no profile ships. That is
allowed: FR-021 permits zero profiles while no module declares a clause set
(see SR-049).

`quoin matrix --repo . --json` (quoin 0.30.1), run at the PR head, does not
see these tests. Every FR-020, FR-021 and NFR-002 Test row is still
`untagged` (FND-001).

## Verdict

**FAIL**: one medium and one low finding.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The computed matrix lists FR-020-AC-1..6, FR-021-AC-1, AC-2, AC-3, AC-5, NFR-002-AC-1, AC-2 and NFR-002-M-1, M-2 as `untagged`, even though the tests carry `@pytest.mark.trace("FR-...-AC-n")`. The matrix binds tests through the TC ids that `spec/tests.md` assigns (TC-160..TC-174), and every other suite here puts that id in the marker (for example `trace("TC-151", "FR-013-AC-2")`). Measured: adding `"TC-160"` to the AC-1 marker turns FR-020-AC-1 `tagged`, and AC-2 stays `untagged`. The NFR-002 metrics M-1 and M-2 are not tagged at all, and the TC-160..TC-174 rows in `spec/tests.md` are still 🚧. Fix: add each TC id to its marker, tag NFR-002-M-1/M-2 (TC-173, TC-174), and update the `spec/tests.md` status for the rows that are now implemented | tests/test_profiles.py:101-247, spec/tests.md:132-134, spec/tests.md:261-275 |
| FND-002 | low | FR-020-AC-6 says the manifest has no `profiles` key "and still activates against filament-core". The test checks only that the key is absent. Activation is FR-001-AC-2, which is 🚧 here because it needs a running filament-core. The absence check is enough for the part this PR can test, but the tag claims the whole AC. Fix: mark TC-165 in `spec/tests.md` as covering the key-absence half, with activation pending FR-001-AC-2 | tests/test_profiles.py:164-167, spec/tests.md:266 |
