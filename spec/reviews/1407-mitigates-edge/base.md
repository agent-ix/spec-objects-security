---
id: SR-012
title: "Base spec review of FR-007 control mitigates hazard and failure_mode"
type: SpecReview
analysis: base
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-007-control-mitigates-safety-objects.md, spec/functional/index.md (PR #39 diff)"
---
# SR-012: Base spec review of FR-007 control mitigates hazard and failure_mode

## Summary

Ticket: PLAT-1407. PR agent-ix/spec-objects-security#39, head `plat-1407-mitigates`
(0bb7f63). Review set: subset — base plus ears-conformance, integrity,
dependency and scope-boundary (SR-013..SR-016). No AssuranceProfile document
exists in the repository, so no profile requires an enforced review run.

Examined: FR-007 frontmatter, Description, Inputs, Outputs, Behavior (6 bullets),
FR-007-CON-1, FR-007-AC-1..AC-5, Dependencies, and the `spec/functional/index.md`
entry. Context read: `spec/spec.md` Out of Scope, FR-003 Behavior, FR-004 control
row, `spec/tests.md` (TM-001), `spec_objects_security/manifest.yaml` control and
traceability blocks, and the companion agent-ix/spec-objects-safety#30 diff.

ID formats (FR-007, FR-007-CON-1, FR-007-AC-1..5) are correct, sequential and
unique. The index entry matches the file and title. FR-007-AC-1 (the loaded list
equals exactly the five targets) is the functional check of the widening and
already fails if an existing target is dropped.

## Verdict

FAIL. FND-001 is a value-freeze check (pin/baseline antipattern) whose fix is
removal; SR-014, SR-015 and SR-016 carry further high findings.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | high | FR-007-AC-5 ("relations and `semantic.compatibility_posture` equal their pre-change values") and FR-007-CON-1 (validated by Test: no existing target, verb or direction removed or changed) specify a snapshot comparison against frozen pre-change values. That is a baseline/pin check, not behaviour: AC-1 already asserts the exact target list, FR-003-AC-1 already asserts `compatibility_posture`, and the two relations are asserted by their own tests. The companion safety review flags the same pattern (safety PR #20 deleted it there). Delete AC-5 and CON-1. | spec/functional/FR-007-control-mitigates-safety-objects.md:47, spec/functional/FR-007-control-mitigates-safety-objects.md:57 |
| FND-002 | low | `spec/tests.md` (TM-001) is not updated: no `covers` relationship to FR-007 and no rows for FR-007's criteria, although TM-001 states coverage is complete only when every AC maps to a test case. | spec/tests.md:1-20 |
