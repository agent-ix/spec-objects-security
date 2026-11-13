---
id: FR-014
title: "A control's mappings are clause references: a clause set key and a clause id"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-005"
    type: "depends_on"
---
# FR-014: A control's mappings are clause references: a clause set key and a clause id

## Description

The `control` object's `mappings` property SHALL hold clause references, each naming one clause of one
clause set. It replaces the `ControlMapping` of [FR-004](./FR-004-role-schemas.md), which named a free-text
`framework`, a free-text `control_id` and a `doc` string and so could not be resolved to a clause.

A clause set is identified by its key `authority/id@version`, the key the Quoin evidence store uses
(`agent-ix/quoin` FR-133). A clause is identified by its id inside that set. The control states which clauses it
answers; whether it discharges them is a person's attestation recorded by Quoin, never a property of this record.

The authored form is the `## Mappings` section of the control skeleton, which carries a typed table of
two columns, `Set` and `Clause`, one row per reference. The threats and risks the prose bullets named move to
`mitigates` ([FR-007](./FR-007-control-mitigates-safety-objects.md)); the section no longer carries prose.

## Inputs

- A `control` artifact with a `## Mappings` table.

## Outputs

- `Control.mappings` as an array of `{ set, clause }`.

## Behavior

- The `ControlMapping` model SHALL be `{ set: string, clause: string }`, sealed, both required.
- `set` SHALL match `authority/id@version`, where each of the three parts is non-empty and contains no `/` or `@`.
- `clause` SHALL be a non-empty string, compared byte for byte, with no case folding or trimming by the module.
- The `framework`, `control_id` and `doc` properties SHALL no longer be admitted.
- The extractor SHALL read the `## Mappings` typed table into `mappings`, one entry per row, in row order.
- The `control` skeleton SHALL carry a `## Mappings` table with the header Set and Clause and one placeholder-free example row.
- `mappings` SHALL stay optional, so a control that maps to no clause validates.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-014-AC-1 | The emitted `ControlMapping` schema requires exactly `set` and `clause` and admits no other property; a record with `framework`, `control_id` or `doc` fails validation. | Test |
| FR-014-AC-2 | A `set` of `example.invalid/std@1` is accepted; `example.invalid/std@`, `example.invalid//1` and `std@1` are each rejected; an empty `clause` is rejected. | Test |
| FR-014-AC-3 | A fixture control whose `## Mappings` table has two rows extracts `mappings` with two entries in row order, and `Control.json` accepts the record. | Test |
| FR-014-AC-4 | The `control` skeleton validates, its `## Mappings` section is a two-column table headed Set and Clause, and it contains no prose bullet in that section. | Test |
| FR-014-AC-5 | A control with no `## Mappings` rows validates. | Test |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-005](./FR-005-executable-skeletons.md); `agent-ix/quoin` FR-133 for the set key form
- **Downstream**: [FR-015](./FR-015-mapping-resolution-and-duplicates.md), [FR-016](./FR-016-mappings-carry-no-standard-text.md)
