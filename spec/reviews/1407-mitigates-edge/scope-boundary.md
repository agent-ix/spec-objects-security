---
id: SR-016
title: "Scope-boundary review of FR-007 control mitigates hazard and failure_mode"
type: SpecReview
analysis: scope-boundary
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-007-control-mitigates-safety-objects.md (PR #39 diff); companion agent-ix/spec-objects-safety#30 read only"
---
# SR-016: Scope-boundary review of FR-007 control mitigates hazard and failure_mode

## Summary

Ticket: PLAT-1407. Checked whether FR-007 fits the module's declared scope and
how responsibility for the widened `mitigates` edge is split with the companion
agent-ix/spec-objects-safety#30 (safety FR-006 edit, FR-007, FR-008, NFR-001).

Clean units: the split of ownership is right in principle — security owns
`control.allowed_links.mitigates` and widens it; safety keeps its relations
`incoming` with `to: []` and declares no outgoing `mitigates`. Both PRs agree
on the target set (`hazard`, `failure_mode`), the direction and additivity.

## Verdict

FAIL: the module's own Out of Scope section still forbids the change.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | high | `spec/spec.md` Out of Scope lists both "Changing this module's `traceability` block or any `allowed_links` verb or target list" and "Widening `control.allowed_links.mitigates` ... The fix is a coordinated change across at least two repositories and is not made here." FR-007 brings that change into scope, and the PR leaves both bullets standing, so the spec states it excludes the requirement it now contains. Move the item into In Scope (citing safety FR-007/FR-008) and narrow the `allowed_links` exclusion. | spec/spec.md:52-68, spec/functional/FR-007-control-mitigates-safety-objects.md:15-23 |
| FND-002 | medium | Both repositories specify the same Quire behaviour as their own acceptance criteria: security FR-007-AC-2/AC-3/AC-4 and safety FR-007-AC-1/AC-2/AC-3/AC-4 each require a fixture `control` mitigating a fixture `hazard`/`failure_mode` with both modules loaded, the dangling-target failure, and the out-of-list rejection. One behaviour gets two owners and two fixtures that can drift (they already differ: safety AC-4 requires naming the type). Keep the cross-module acceptance in one repo and have the other cite it. | spec/functional/FR-007-control-mitigates-safety-objects.md:54-56 |

## Dispositions

| FND | outcome | reason |
|-----|---------|--------|
| FND-001 | fixed | fixed in c667d46 |
| FND-002 | fixed | fixed in c667d46 |
