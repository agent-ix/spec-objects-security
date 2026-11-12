---
id: SR-021
title: "Gap analysis of PR #41 against FR-003, FR-001 and StR-001"
type: SpecReview
analysis: gap-analysis
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-001-module-manifest-activates.md, spec/stakeholder/StR-001-module-activation.md, spec/tests.md, tests/test_manifest_engine_gate.py (PR #41 diff at 29c7445)"
---
# SR-021: Gap analysis of PR #41 against FR-003, FR-001 and StR-001

## Summary

Ticket: PLAT-350. Plan completion: not assessed.

`quire matrix --scope . --format tsv` lists FR-003-AC-7 as tagged by
`tests/test_manifest_engine_gate.py` lines 67, 76 and 84. All three carry
`trace("TC-115", "FR-003-AC-7")`. TC-115 appears once in `spec/tests.md`, its
row binds FR-003-AC-7, and the FR-003 coverage row now reads `AC-4..7` and
includes TC-115. The numbering is consistent.

- FR-001: the Behavior change only re-points the conformance judgement to
  AC-7 and AC-2. FR-001-AC-2 stays `🚧`, correctly. No AC changed.
- StR-001: only the upstream-dependency text changed. No VC changed.
- FR-003-AC-5 stays untagged as a Demonstration. That contradiction is
  recorded in SR-020 FND-005.
- TC-114's row drops "and hashes". `tests/test_quoin_install_roundtrip.py`
  asserts only that each file exists and has its `$id`, so the row now matches
  the test.
- The diff adds no production code.

## Verdict

PASS on trace and coverage, apart from one low gap: the ownership correction
did not reach `plan/`.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | low | The ownership correction is incomplete. `plan/Plan-001-semantic-module-contract/plan.md` still says FR-001 "conforms to filament-core-service FR-035". Task-007 still records an FR-035 schema pin under `tests/fixtures/` as delivered `[x]`, but that fixture no longer exists. Delete the pin record and correct the owner. | plan/Plan-001-semantic-module-contract/plan.md:45, plan/Plan-001-semantic-module-contract/tasks/Task-007-test-environment-and-fr035-pin.md:58-61 |
