---
id: FR-010
title: "A SOUP record states requirements served, anomalies, support status and end of support, with unknown explicit"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-006"
    type: "depends_on"
---
# FR-010: A SOUP record states requirements served, anomalies, support status and end of support, with unknown explicit

## Description

Beyond identity ([FR-009](./FR-009-soup-record-identity-and-promotion.md)), a `soup_record`
carries four reviewer-authored facts. An SBOM cannot supply any of them, so each has an
explicit `unknown` state and no default, in the manner of [FR-006](./FR-006-security-safe-declarations.md).

## Inputs

- The `soup_record` model of [FR-009](./FR-009-soup-record-identity-and-promotion.md).

## Outputs

- The `SoupSupportStatus` closed vocabulary and the `soup_record` field set under `spec_objects_security/schemas/`.

## Behavior

- A `soup_record` SHALL carry `serves`, a `SemanticId[]` naming the requirements the component serves.
- A `soup_record` SHALL carry `known_anomalies`, a list of anomaly statements, each with a free-text `statement` and an optional `source_ref` `SemanticId`.
- The `known_anomalies` field SHALL distinguish an empty list, meaning the reviewer found none, from an absent field, meaning nobody looked.
- A `soup_record` SHALL carry `support_status` from the closed vocabulary `SoupSupportStatus`, with exactly the members `supported`, `community_supported`, `unsupported`, `unknown`.
- A `soup_record` SHALL carry `end_of_support`, which is either a calendar date or the literal `unknown`.
- A `soup_record` SHALL accept an `end_of_support` of `unknown` for a component whose support status is `supported`.
- A record carrying a value outside `SoupSupportStatus` SHALL fail validation.
- The module SHALL emit no default for `serves`, `known_anomalies`, `support_status` or `end_of_support`.
- The module SHALL report a `soup_record` whose `serves` is empty, because a component that serves no requirement is unjustified scope.
- The module SHALL accept `serves` entries that name requirements declared in another repository.
- The `known_anomalies` statements SHALL pass the credential-shape scan of [FR-005](./FR-005-executable-skeletons.md), because they are free text.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-010-CON-1 | `SoupSupportStatus` is a closed `enum` whose unassessed member is `unknown`. | Design | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-010-AC-1 | `SoupSupportStatus` has exactly the members `supported`, `community_supported`, `unsupported`, `unknown` as a closed enum; a record carrying `unknown` validates and one carrying an invented member fails. | Test |
| FR-010-AC-2 | A fixture with `known_anomalies: []` validates and is distinguishable from the same fixture with the field absent. | Test |
| FR-010-AC-3 | A fixture with `end_of_support: unknown` validates, a fixture with a calendar date validates, and a fixture with any other string fails. | Test |
| FR-010-AC-4 | The emitted `soup_record` schema carries no `default` keyword at any depth. | Test |
| FR-010-AC-5 | A fixture `soup_record` with an empty `serves` list yields one finding naming the record, and a fixture whose `serves` names a requirement in another repository yields none. | Test |
| FR-010-AC-6 | A fixture whose anomaly statement contains a credential-shaped string is refused by the FR-005 scan. | Test |

## Dependencies

- **Upstream**: [FR-006](./FR-006-security-safe-declarations.md), [FR-009](./FR-009-soup-record-identity-and-promotion.md)
- **Downstream**: [FR-011](./FR-011-soup-risk-disposition.md)
