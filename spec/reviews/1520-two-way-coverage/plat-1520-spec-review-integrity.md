---
id: SR-036
title: "Integrity review of PR #46 FR-008 constrained mitigation target"
type: SpecReview
analysis: integrity
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-008-security-nfr-needs-mitigation-target.md (PR #46 diff at 60b5bab)"
---
# SR-036: Integrity review of PR #46 FR-008 constrained mitigation target

## Summary

Ticket: PLAT-1520 (PR #46). Checked FR-008's Description, Inputs, Outputs,
Behavior and Acceptance Criteria for internal consistency after the
amendment. The new Description, the new `SHALL NOT` bullet and AC-3 agree:
an NFR whose only `mitigates` edge targets a wrong kind or an unloaded
repository keeps the finding. Two unchanged statements still define the
trigger as "no outgoing `mitigates` edge", which that NFR does have.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | Behavior bullet 2 still triggers the report only on "no outgoing `mitigates` edge", contradicting bullet 4 and AC-3, where an NFR with a wrong-kind or dangling `mitigates` edge is also reported | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:58 |
| FND-002 | low | Outputs still emit the finding "for each `security` NFR with no outgoing `mitigates` edge", omitting NFRs whose only edges are wrong-kind or dangling | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:53 |

## Verdict

Changes requested (1 medium, 1 low).

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Behavior bullet 2 now reads "no outgoing `mitigates` edge to a resolved `threat` or `risk`" (c6ee512) |
| FND-002 | fixed | Outputs now read "no outgoing `mitigates` edge to a resolved `threat` or `risk`" (c6ee512) |
