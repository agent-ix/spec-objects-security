---
id: FR-012
title: "A vulnerability can affect a SOUP record, and the advisory join stays open"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-009"
    type: "depends_on"
---
# FR-012: A vulnerability can affect a SOUP record, and the advisory join stays open

## Description

The module already declares `vulnerability`, whose `affects` edge names the things a vulnerability
touches. A component is such a thing, so this requirement adds `soup_record` to the targets of
`vulnerability.affects` and adds no new link verb. The edge is authored on the vulnerability, as every
`affects` edge is, and the only link a `soup_record` declares is the `serves` edge of [FR-013](./FR-013-soup-record-serves-requirement.md).

The record does not link to `asset`. The `part_of` verb is the inverse of `aggregates`, a structural composite,
which is the wrong fact for a third-party dependency; which requirements a component serves is stated by
`serves` ([FR-010](./FR-010-soup-record-fields.md), [FR-013](./FR-013-soup-record-serves-requirement.md)). Matching advisories to components is a later capability
and is not specified here.

## Inputs

- The `soup_record` and `vulnerability` entries of the module manifest.

## Outputs

- `vulnerability.allowed_links.affects` in the module manifest.

## Behavior

- The manifest SHALL list `soup_record` in `vulnerability.allowed_links.affects`.
- The manifest SHALL keep `asset` and `attack_surface` in `vulnerability.allowed_links.affects`.
- The manifest SHALL declare no `allowed_links` for `soup_record` other than `serves` (FR-013).
- The manifest SHALL declare no required relation that obliges a `soup_record` to have an incoming `affects` edge; its one required relation is the outgoing `serves` of FR-013.
- The manifest SHALL introduce no link verb that the engine does not already know.
- Quire SHALL report a `vulnerability` `affects` edge to a type outside the list as `disallowed-edge-target`, naming the target's type.
- The `soup_record` schema SHALL refuse the keys `severity`, `cve_id` and any advisory list.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-012-AC-1 | The loaded `vulnerability` type lists exactly `asset`, `attack_surface`, `soup_record` under `allowed_links.affects`, and the loaded `soup_record` type declares no `allowed_links` other than `serves`. | Test |
| FR-012-AC-2 | A fixture `vulnerability` with an `affects` edge to a fixture `soup_record` validates with no `UnknownEdgeType` advisory and no `disallowed-edge-target`, and the same edge to a fixture `threat` is reported `disallowed-edge-target` naming `threat`. | Test |
| FR-012-AC-3 | A fixture `soup_record` that no vulnerability affects validates with no finding other than the `soup-serves-no-requirement` finding of FR-013. | Test |
| FR-012-AC-4 | A fixture `soup_record` carrying `severity`, `cve_id` or an advisory list fails. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-009](./FR-009-soup-record-identity-and-promotion.md)
- **Downstream**: none; the advisory join is a later requirement of the owning project.
