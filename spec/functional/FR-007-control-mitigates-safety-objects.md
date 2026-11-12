---
id: FR-007
title: "A control can declare a mitigates edge to a hazard or failure_mode"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-006"
    type: "depends_on"
---
# FR-007: A control can declare a mitigates edge to a hazard or failure_mode

## Description

The `control` object type SHALL admit `hazard` and `failure_mode` (owned by
`agent-ix/spec-objects-safety`) as `mitigates` targets, in addition to `threat`,
`risk` and `vulnerability`. Safety's `hazard-has-mitigation` and
`failure-mode-has-mitigation` relations require an incoming `mitigates` edge, and
the control end is where that mitigation is authored.

The change is a widening of one target list. No constraint is relaxed, no verb is
minted, and no direction changes: the safety side stays `incoming`, so a hazard
never lists its own mitigations.

## Inputs

- The `control` entry of this module's manifest.
- A `hazard` and a `failure_mode` document from `spec-objects-safety`.

## Outputs

- `control.allowed_links.mitigates` equal to `[threat, risk, vulnerability, hazard, failure_mode]`.

## Behavior

- The manifest SHALL list `hazard` and `failure_mode` in `control.allowed_links.mitigates`.
- The manifest SHALL keep `threat`, `risk` and `vulnerability` in that list.
- The manifest SHALL leave the `threat-has-control` and `risk-has-treatment` relations unchanged.
- Quire SHALL accept a `control` document's `mitigates` edge to a `hazard` or `failure_mode` with no `disallowed-edge-target` diagnostic.
- When the target of a `control` document's `mitigates` edge matches no loaded document, `quire validate` SHALL fail with a diagnostic naming the control's file, the verb and the missing target.
- The `mitigates` edge to any type outside the list SHALL still be reported `disallowed-edge-target`.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-007-CON-1 | This module SHALL widen the list only, keeping `compatibility_posture: additive`; no existing target, verb or direction is removed or changed. | Compatibility | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-007-AC-1 | The loaded `control` type lists exactly `threat`, `risk`, `vulnerability`, `hazard`, `failure_mode` under `allowed_links.mitigates`. | Test |
| FR-007-AC-2 | A fixture `control` with `mitigates` edges to a fixture `hazard` and a fixture `failure_mode`, validated with both modules loaded, yields no `disallowed-edge-target` and no `DisallowedEdgeType` diagnostic. | Test |
| FR-007-AC-3 | A fixture `control` whose `mitigates` target id is declared by no loaded document fails `quire validate` with a non-zero exit, and the message contains the file path, `mitigates` and the missing id. | Test |
| FR-007-AC-4 | A fixture `control` with a `mitigates` edge to a type outside the list is still reported `disallowed-edge-target`. | Test |
| FR-007-AC-5 | The `threat-has-control` and `risk-has-treatment` relations and `semantic.compatibility_posture` equal their pre-change values. | Test |

## Dependencies

- **Upstream**: [FR-006](./FR-006-security-safe-declarations.md); `agent-ix/spec-objects-safety` FR-007 and FR-008 (the coverage checks that read this edge)
