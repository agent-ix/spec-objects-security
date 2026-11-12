---
id: SR-013
title: "EARS review of FR-007 control mitigates hazard and failure_mode"
type: SpecReview
analysis: ears-conformance
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-007-control-mitigates-safety-objects.md (PR #39 diff)"
---
# SR-013: EARS review of FR-007 control mitigates hazard and failure_mode

## Summary

Ticket: PLAT-1407. Every SHALL-bearing statement of FR-007 was read for EARS
pattern, a single `shall`, a named subject and a concrete response: the
Description's first sentence, the six Behavior bullets and FR-007-CON-1 (8
statements, 8 `SHALL`). Seven are ubiquitous or event-driven with a named
subject (the manifest, Quire, `quire validate`, this module).

## Verdict

Conformant except one Behavior bullet with no named system.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | low | Behavior bullet "The `mitigates` edge to any type outside the list SHALL still be reported `disallowed-edge-target`." is passive with no named system; every sibling bullet names Quire or the manifest. Restate as "Quire SHALL report `disallowed-edge-target` for a `control` document's `mitigates` edge to any type outside the list." | spec/functional/FR-007-control-mitigates-safety-objects.md:41 |
