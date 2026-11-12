---
id: SR-018
title: "Gap analysis of PR #40 against FR-007 and FR-003"
type: SpecReview
analysis: gap-analysis
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-007-control-mitigates-safety-objects.md, spec/functional/FR-003-semantic-manifest-contract.md, tests/test_control_mitigates.py, spec_objects_security/manifest.yaml (PR #40 diff)"
---
# SR-018: Gap analysis of PR #40 against FR-007 and FR-003

## Summary

Ticket: PLAT-1408. Plan completion: not assessed.

`quire matrix --scope .` lists FR-007-AC-1 as tagged by
`tests/test_control_mitigates.py:34` (TC-091) and FR-007-AC-2 as tagged by
`tests/test_control_mitigates.py:47` (TC-092).

- FR-007 Behavior "list hazard and failure_mode" and "keep threat, risk and
  vulnerability": the manifest is changed to exactly the five targets, and
  TC-091 asserts the list with exact equality, so both a dropped target and an
  extra target fail it.
- FR-007 Behavior "report a disallowed target, naming its type": TC-092 covers
  it.
- FR-003 Behavior names the same five-entry list. TC-091 asserts it, and FR-003
  has no AC of its own over that list, so nothing is untraced.
- The diff adds no production code without an owning requirement.

The only weaknesses in AC-2's binder are SR-017 FND-001 (the test cannot run in
CI as configured) and SR-017 FND-002 (the naming assertion is loose). They are
recorded once, in SR-017.

## Verdict

PASS for traceability and coverage of FR-007 and FR-003 within this diff. The
AC-2 binder is only as sound as the SR-017 fixes make it.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | low | No findings (placeholder) | - |
