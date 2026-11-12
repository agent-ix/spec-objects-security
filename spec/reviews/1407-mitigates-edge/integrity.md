---
id: SR-014
title: "Integrity review of FR-007 control mitigates hazard and failure_mode"
type: SpecReview
analysis: integrity
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-007-control-mitigates-safety-objects.md (PR #39 diff)"
---
# SR-014: Integrity review of FR-007 control mitigates hazard and failure_mode

## Summary

Ticket: PLAT-1407. Checked FR-007 for consistency with the rest of the spec
set, completeness of its inputs, and atomicity and testability of
FR-007-AC-1..AC-4. Context: FR-003 Behavior, FR-004 control row
(`mitigates: SemanticId[]`), manifest `control.allowed_links`, and the
companion safety FR-007.

Clean units: FR-007-AC-1 (exact list, testable against the loaded manifest),
FR-007-AC-2 (both targets, both diagnostic names).

## Verdict

FAIL: FR-007 contradicts FR-003, which the PR leaves unchanged.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | high | FR-003 Behavior still states that `control.allowed_links.mitigates` is `[threat, risk, vulnerability]`, "which excludes `hazard` and `failure_mode`", and that changing it "is a cross-repository decision and is out of scope here". FR-007 makes exactly that change; the PR does not amend FR-003, so two requirements of the same module contradict each other. | spec/functional/FR-003-semantic-manifest-contract.md:49, spec/functional/FR-007-control-mitigates-safety-objects.md:15-19 |
| FND-002 | medium | FR-007 never says how a `control` document authors the edge. FR-004 gives `Control` a `mitigates: SemanticId[]` property, while `allowed_links` governs frontmatter `relationships` edges, and the companion safety FR-007 Inputs say "a `mitigates` relationship". Two implementers would write different AC-2/AC-3/AC-4 fixtures (a frontmatter relationship vs a Properties field), and only one of them is checked by `allowed_links`. | spec/functional/FR-007-control-mitigates-safety-objects.md:25-28, spec/functional/FR-004-role-schemas.md:77 |
| FND-003 | low | FR-007-AC-4 does not require the `disallowed-edge-target` diagnostic to name the target's type, nor say which out-of-list type the fixture uses; companion safety FR-007-AC-4 requires naming the type, so the two repos specify the same check differently. | spec/functional/FR-007-control-mitigates-safety-objects.md:56 |
