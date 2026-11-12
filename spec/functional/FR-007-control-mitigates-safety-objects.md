---
id: FR-007
title: "A control admits hazard and failure_mode as mitigates targets"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "depends_on"
---
# FR-007: A control admits hazard and failure_mode as mitigates targets

## Description

The `control` object type SHALL admit `hazard` and `failure_mode` (owned by
`agent-ix/spec-objects-safety`) as `mitigates` targets, in addition to `threat`,
`risk` and `vulnerability`. Safety's `hazard-has-mitigation` and
`failure-mode-has-mitigation` relations require an incoming `mitigates` edge, and
the control end is where that mitigation is authored.

A control writes the edge as a frontmatter `relationships` entry with
`type: mitigates`, which `allowed_links` governs. The `Control.mitigates`
`SemanticId[]` property of [FR-004](./FR-004-role-schemas.md) is a separate
record-schema field and is unchanged by this requirement.

Everything that involves both modules (Quire accepting the edge with no
diagnostic, the coverage checks firing, a dangling target failing validation)
is specified once, in `agent-ix/spec-objects-safety` FR-007 and FR-008. This
requirement covers only this module's own target list.

## Inputs

- The `control` entry of this module's manifest.

## Outputs

- `control.allowed_links.mitigates` equal to `[threat, risk, vulnerability, hazard, failure_mode]`.

## Behavior

- The manifest SHALL list `hazard` and `failure_mode` in `control.allowed_links.mitigates`.
- The manifest SHALL keep `threat`, `risk` and `vulnerability` in that list.
- Quire SHALL report a `control` `mitigates` edge to a type outside the list as `disallowed-edge-target`, naming the target's type.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-007-AC-1 | The loaded `control` type lists exactly `threat`, `risk`, `vulnerability`, `hazard`, `failure_mode` under `allowed_links.mitigates`. | Test |
| FR-007-AC-2 | A fixture `control` with a `mitigates` relationship to a fixture `asset` is reported `disallowed-edge-target`, and the diagnostic names the type `asset`. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-role-schemas.md)
- **Downstream**: `agent-ix/spec-objects-safety` FR-007 and FR-008, which carry the cross-module behavior
