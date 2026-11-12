---
id: FR-011
title: "A SOUP record's risk disposition is person-owned, typed, and carries an approval reference"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-010"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-135"
    type: "references"
---
# FR-011: A SOUP record's risk disposition is person-owned, typed, and carries an approval reference

## Description

Whether a component's remaining risk is tolerated is a decision a person makes and owns. The
`soup_record` records that decision with the same typed dispositions that
`quoin discharge --rmm` reads (`agent-ix/quoin` FR-135): accepted risk, temporary exception,
and delegated. This requirement reuses those three kinds and defines no fourth.
It records no score, class or level for the component.

## Inputs

- The `soup_record` model of [FR-009](./FR-009-soup-record-identity-and-promotion.md).

## Outputs

- The `SoupDispositionKind` closed vocabulary and the optional `disposition` block of the `soup_record` schema.

## Behavior

- A `soup_record` MAY carry a `disposition`.
- An absent `disposition` SHALL mean no decision has been recorded.
- A `disposition` SHALL carry `kind` from the closed vocabulary `SoupDispositionKind` with exactly the members `accepted_risk`, `temporary_exception`, `delegated`.
- A `disposition` SHALL carry `approver`, a `SemanticId` naming the person who owns the decision.
- A `disposition` SHALL carry `approval_ref`, a non-empty reference to where the approval is recorded.
- A `disposition` SHALL carry `rationale`, a non-empty free-text statement.
- A `disposition` of kind `temporary_exception` SHALL carry `expires`, a calendar date.
- The module SHALL refuse a `disposition` of kind `temporary_exception` that has no `expires`.
- A `disposition` of kind `delegated` SHALL carry `delegate`, a `SemanticId` naming the party who now owns the risk.
- The module SHALL refuse a `disposition` whose `approver` names an agent identity.
- The module SHALL refuse a `disposition` whose `approval_ref` or `rationale` is empty or whitespace only.
- The module SHALL NOT infer, default or compute a `disposition` from any other field of the record or from any advisory.
- The module SHALL NOT admit a `disposition` kind outside `SoupDispositionKind`.
- A `soup_record` SHALL pass `kind`, `approval_ref`, `rationale` and `expires` to `quoin discharge --rmm` unchanged.
- The module SHALL NOT define an alternative reading of those four keys.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-011-CON-1 | The kinds of `SoupDispositionKind` are exactly the kinds `quoin discharge --rmm` reads; this module adds none. | Design | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-011-AC-1 | `SoupDispositionKind` has exactly the members `accepted_risk`, `temporary_exception`, `delegated`; a record with an invented kind fails. | Test |
| FR-011-AC-2 | A fixture with no `disposition` validates, and the validated record carries no `disposition` key. | Test |
| FR-011-AC-3 | A `temporary_exception` fixture with `expires` validates, and the same fixture without `expires` fails. | Test |
| FR-011-AC-4 | A `delegated` fixture with `delegate` validates, and the same fixture without `delegate` fails. | Test |
| FR-011-AC-5 | A fixture whose `approval_ref` is empty, or whose `rationale` is whitespace only, fails. | Test |
| FR-011-AC-6 | A fixture whose `approver` names an agent identity fails. | Test |
| FR-011-AC-7 | A fixture carrying a `disposition` and a fixture without one are identical in every other emitted key, so the disposition derives nothing and nothing derives it. | Test |
| FR-011-AC-8 | The set of kinds in the `SoupDispositionKind` schema equals the set of kinds the installed `quoin discharge --rmm` accepts for a stored disposition. | Test |

## Dependencies

- **Upstream**: [FR-009](./FR-009-soup-record-identity-and-promotion.md), [FR-010](./FR-010-soup-record-fields.md)
- **Downstream**: [NFR-001](../non-functional/NFR-001-soup-records-state-and-never-derive.md)
