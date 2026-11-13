---
id: SR-030
title: "EARS conformance review of the SOUP record object (FR-009..FR-012, NFR-001)"
type: SpecReview
analysis: ears-conformance
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-009..FR-012, spec/non-functional/NFR-001 (PR #44 diff)"
---
# SR-030: EARS conformance review of the SOUP record object (FR-009..FR-012, NFR-001)

## Summary

Ticket: PLAT-1512. Checked every Behavior bullet and NFR-001's Statement for EARS shape:
one subject that is the system or a part of it, one SHALL per statement, no embedded
rationale. `Quire SHALL report ...` follows this repository's precedent (FR-007, FR-008)
and is not flagged.

Clean units: NFR-001 Statement (two ubiquitous statements), FR-009 Behavior except the
promotion bullets, FR-011 Behavior except the hand-off bullet, and FR-012 Behavior except
the embedded rationale.

## Verdict

PASS with findings. No finding here is high.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | medium | Some statements have a subject that is neither the module nor part of it. In "A `soup_record` SHALL pass `kind`, ... to `quoin discharge --rmm` unchanged", the record, which is passive data, is the actor. "A promotion SHALL copy only the facts ..." names an activity that has no owning system (see SR-031 FND-001). Restate each with the system that performs it. | spec/functional/FR-011-soup-risk-disposition.md:48, spec/functional/FR-009-soup-record-identity-and-promotion.md:47 |
| FND-002 | low | Some Behavior statements embed their rationale ("because a component that serves no requirement is unjustified scope", "because they are free text", "because a component with no linked vulnerability is a valid state"). Move the reason to a Rationale or Description section. | spec/functional/FR-010-soup-record-fields.md:39, spec/functional/FR-010-soup-record-fields.md:41, spec/functional/FR-012-soup-record-relations.md:39 |
