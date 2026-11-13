---
id: FR-011
title: "A SOUP record's risk disposition is a person-owned quoin disposition fact, referenced by clause id"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-010"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-046"
    type: "references"
  - target: "ix://agent-ix/quoin/FR-133"
    type: "references"
  - target: "ix://agent-ix/quoin/FR-135"
    type: "references"
---
# FR-011: A SOUP record's risk disposition is a person-owned quoin disposition fact, referenced by clause id

## Description

Whether a component's remaining risk is tolerated is a decision a person makes and owns. Quoin already
owns the shape of that decision: a disposition fact of `agent-ix/quoin` FR-046, kept in the evidence store of
FR-133 and read by `quoin discharge --rmm` (FR-135). The fact is `{kind: "disposition", clauseId, decision, rationale,
approvalRef, attestation: {attestedBy, authority, attestedAt, expiresAt}}` with `decision` one of `accepted_risk`,
`temporary_exception`, `delegated`. This module defines no second shape and no copy of that vocabulary.

A disposition fact is keyed on a clause id. For a component record, that clause id is the obligation the
component's SBOM entries are bound to by the `--discharges` binding of `agent-ix/quoin` FR-041. The record
therefore holds that one clause id, `disposition_clause`, and does not embed the fact. The decision, rationale,
approval reference and expiry live in the fact and are read from it.

A person accepts each risk. That is a process constraint over the attestation authority fields of the fact
(FR-011-CON-1); no schema rule can know what a person is. Nothing here records a score, class or level.

## Inputs

- The `soup_record` model of [FR-009](./FR-009-soup-record-identity-and-promotion.md).
- The disposition fact shape of `agent-ix/quoin` FR-046.

## Outputs

- The optional `disposition_clause` key of the `soup_record` schema.

## Behavior

- The `soup_record` schema SHALL admit `disposition_clause`, a non-empty string naming the clause id under which a disposition fact is recorded.
- The `soup_record` schema SHALL treat an absent `disposition_clause` as no decision recorded.
- The `soup_record` schema SHALL refuse a `disposition_clause` that is empty or whitespace only.
- The `soup_record` schema SHALL refuse the keys `decision`, `rationale`, `approvalRef`, `approval_ref`, `attestation`, `approver` and `expires`.
- The module SHALL define no disposition kind, no approval vocabulary and no expiry rule of its own.
- The module SHALL NOT derive a `disposition_clause` from any other key of the record.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-011-CON-1 | A person accepts each risk: every disposition fact that a `disposition_clause` names carries an `attestation` whose `attestedBy` and `authority` identify the accountable person and the authority they hold. | Process | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-011-AC-1 | A fixture with a non-empty `disposition_clause` validates, and a fixture with an empty or whitespace-only one fails. | Test |
| FR-011-AC-2 | A fixture with no `disposition_clause` validates and the validated record carries no such key. | Test |
| FR-011-AC-3 | A fixture embedding any of `decision`, `rationale`, `approvalRef`, `attestation`, `approver` or `expires` fails, and the emitted schema declares none of them. | Test |
| FR-011-AC-4 | A worked example pairs a fixture record with a disposition fact of the `agent-ix/quoin` FR-046 shape under the named clause id, and a reviewer confirms that `attestedBy` and `authority` are present and name a person. | Inspection |
| FR-011-AC-5 | Two fixtures that differ only by a `disposition_clause` are identical in every other emitted key. | Test |

## Dependencies

- **Upstream**: [FR-009](./FR-009-soup-record-identity-and-promotion.md), [FR-010](./FR-010-soup-record-fields.md)
- **Downstream**: [NFR-001](../non-functional/NFR-001-soup-records-state-and-never-derive.md)
