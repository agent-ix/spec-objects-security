---
id: FR-010
title: "A SOUP record states requirements served, anomalies, support status and end of support"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-006"
    type: "depends_on"
---
# FR-010: A SOUP record states requirements served, anomalies, support status and end of support

## Description

Beyond identity ([FR-009](./FR-009-soup-record-identity-and-promotion.md)), a `soup_record`
carries four reviewer-authored facts that an SBOM cannot supply. The module states "not stated"
in two ways, by field kind. A scalar field (`support_status`, `end_of_support`) holds the literal
`unknown`. A list field (`serves`, `known_anomalies`) has no `unknown` member: an absent list
means nobody has stated it, and an empty list means the reviewer stated that there are none.
Neither form has a default, in the manner of [FR-006](./FR-006-security-safe-declarations.md).

The module reports a record with no `serves` edge (FR-013), because a component that serves no
requirement is unjustified scope. `SoupSupportStatus` is owned by this requirement and is not one of
the ten vocabularies counted by FR-006.

## Inputs

- The `soup_record` model of [FR-009](./FR-009-soup-record-identity-and-promotion.md).

## Outputs

- The `SoupSupportStatus` closed vocabulary and the field set of the `soup_record` schema under `spec_objects_security/schemas/`.

## Behavior

- The `soup_record` schema SHALL admit `serves`, a `SemanticId[]` naming the requirements the component serves.
- The `soup_record` schema SHALL admit `known_anomalies`, a list of anomaly statements, each with a free-text `statement` and an optional `source_ref` `SemanticId`.
- The `soup_record` schema SHALL treat an absent `serves` or `known_anomalies` as not stated and an empty one as stated none.
- The `soup_record` schema SHALL admit `support_status` only from the closed vocabulary `SoupSupportStatus`, whose members are exactly `supported`, `community_supported`, `unsupported`, `unknown`.
- The `soup_record` schema SHALL admit `end_of_support` only as a calendar date or the literal `unknown`.
- The `soup_record` schema SHALL admit an `end_of_support` of `unknown` together with a `support_status` of `supported`.
- The module SHALL emit no default for `serves`, `known_anomalies`, `support_status` or `end_of_support`.
- Quire SHALL report a `soup_record` that has no `serves` edge, as [FR-013](./FR-013-soup-record-serves-requirement.md) specifies; the `serves` record field is not read by that check.
- The module SHALL accept `serves` entries that name requirements declared in another repository.
- The module SHALL apply the credential-shape scan of [FR-005](./FR-005-executable-skeletons.md) to the `known_anomalies` statements.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-010-CON-1 | `SoupSupportStatus` is a closed `enum` whose unassessed member is `unknown`. | Design | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-010-AC-1 | `SoupSupportStatus` has exactly the members `supported`, `community_supported`, `unsupported`, `unknown` as a closed enum; a record carrying `unknown` validates and one carrying an invented member fails. | Test |
| FR-010-AC-2 | A fixture with `known_anomalies: []` validates, a fixture with the field absent validates, and the two emit different records, the first with an empty list and the second with no key. | Test |
| FR-010-AC-3 | A fixture with `end_of_support: unknown` validates, a fixture with a calendar date validates, and a fixture with any other string fails. | Test |
| FR-010-AC-4 | The emitted `soup_record` schema carries no `default` keyword at any depth. | Test |
| FR-010-AC-5 | A fixture `soup_record` with no `serves` relationship yields one finding naming the record (FR-013-AC-2), and a fixture whose `serves` relationship names a requirement in the bundle yields none (FR-013-AC-3). | Test |
| FR-010-AC-6 | A fixture whose anomaly statement contains a credential-shaped string is refused by the FR-005 scan. | Test |

## Dependencies

- **Upstream**: [FR-006](./FR-006-security-safe-declarations.md), [FR-009](./FR-009-soup-record-identity-and-promotion.md)
- **Downstream**: [FR-011](./FR-011-soup-risk-disposition.md), [FR-013](./FR-013-soup-record-serves-requirement.md)
