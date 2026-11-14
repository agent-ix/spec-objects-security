---
id: FR-022
title: "A SOUP record carries optional person-authored VEX statements"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-010"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-142"
    type: "references"
---
# FR-022: A SOUP record carries optional person-authored VEX statements

## Description

A SOUP record may carry `vex_statements`, an optional list of a person's
vulnerability-exploitability statements for advisories that the advisory join
reports for that component. Each statement records the advisory identifier,
status, any required justification or action, the named assessor and assessment
date, and optional impact and evidence references. The list describes authored
facts only: its absence means no statement is recorded, and an empty list means
the author explicitly recorded that there are none. Nothing derives or defaults
a status from an advisory, reachability result, or other analysis.

## Inputs

- A `soup_record` as specified by [FR-009](./FR-009-soup-record-identity-and-promotion.md).
- Advisory identifiers reported for the component by the join in
  `agent-ix/quoin` [FR-142](ix://agent-ix/quoin/FR-142).
- A person's statement and its supporting evidence references.

## Outputs

- An optional `vex_statements` field in the `soup_record` schema.
- A closed set of VEX statement status and justification values.

## Behavior

- The `soup_record` schema SHALL admit the optional `vex_statements` field as a
  list of VEX statement objects, with no default.
- Each VEX statement SHALL carry `advisory`, a non-empty identifier exactly as
  reported by the advisory join; `status`; `assessed_by`, a non-blank person's
  name; and `assessed_at`, a valid calendar date in `YYYY-MM-DD` form.
- The `status` field SHALL admit exactly `affected`, `not_affected`,
  `under_investigation`, and `fixed`.
- The `justification` field SHALL admit exactly `component_not_present`,
  `vulnerable_code_not_present`, `vulnerable_code_not_in_execute_path`,
  `vulnerable_code_cannot_be_controlled_by_adversary`, and
  `inline_mitigations_already_exist`.
- A statement whose status is `not_affected` SHALL carry `justification`.
- A statement whose status is `affected` SHALL carry a non-blank
  `action_statement`.
- A statement MAY carry `impact_statement` and `evidence_refs`; each evidence
  reference SHALL be a `SemanticId`.
- The `soup_record` schema SHALL refuse two `vex_statements` entries with the
  same `advisory` identifier.
- The module SHALL NOT supply a default for any VEX statement field, including
  `status`.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-022-CON-1 | VEX statement values are person-authored record data; neither advisory presence nor analysis results create or change a statement. | Design | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-022-AC-1 | A fixture with `vex_statements` absent validates and emits no such key; a fixture with `vex_statements: []` validates and emits an empty list. | Test |
| FR-022-AC-2 | Fixtures with each of the four allowed `status` values and valid required fields validate; a fixture with any other status fails with a located message naming `status`. | Test |
| FR-022-AC-3 | A fixture with `status: not_affected` and each allowed `justification` validates; one without `justification` or with an unlisted value fails with a located message naming `justification`. | Test |
| FR-022-AC-4 | A fixture with `status: affected` and a non-blank `action_statement` validates; one without the field or with a blank value fails with a located message naming `action_statement`. | Test |
| FR-022-AC-5 | A fixture with a missing or blank `assessed_by`, or with a missing, malformed, or impossible `assessed_at` date, fails with a located message naming the field; a fixture with a named assessor and valid `YYYY-MM-DD` date validates. | Test |
| FR-022-AC-6 | Two statements with the same exact `advisory` identifier fail with a located duplicate error naming `advisory`; statements with distinct identifiers validate. | Test |
| FR-022-AC-7 | A fixture containing `evidence_refs` with `SemanticId` values validates, and one containing a non-`SemanticId` value fails with a located message naming `evidence_refs`. | Test |
| FR-022-AC-8 | The emitted schema contains no default for any VEX statement field. | Test |

## Dependencies

- **Upstream**: [FR-009](./FR-009-soup-record-identity-and-promotion.md), [FR-010](./FR-010-soup-record-fields.md)
- **Context**: `agent-ix/quoin` [FR-142](ix://agent-ix/quoin/FR-142) reports advisories joined to SOUP records.
