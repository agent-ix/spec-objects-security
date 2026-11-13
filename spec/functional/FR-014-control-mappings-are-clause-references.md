---
id: FR-014
title: "A control's mappings are clause references: a clause set key and a clause id"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-005"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-081"
    type: "depends_on"
---
# FR-014: A control's mappings are clause references: a clause set key and a clause id

## Description

The `control` object's `mappings` property SHALL hold clause references, each naming one clause of one
clause set. It replaces the `ControlMapping` of [FR-004](./FR-004-role-schemas.md), which named a free-text
`framework`, a free-text `control_id` and a `doc` string and so could not be resolved to a clause.

A clause set is identified by its key `authority/id@version`, the key form of `agent-ix/quoin` FR-137 to FR-140.
A clause is identified by its id inside that set. The identifier rules of `agent-ix/quoin` FR-133 apply to all four parts,
so a mapping this module accepts never yields a fact that `quoin evidence record-discharge` refuses on length: each part is
1 to 64 bytes. FR-133's refusal of two ids that differ only by case is applied by Quoin when it records (`agent-ix/quoin`
FR-173), not by this module.

The control states which clauses it answers. Whether it discharges them is a person's attestation recorded by Quoin, never a
property of this record. Whether a clause exists in a set, and whether a mapping is repeated or contradicted by a scope
exclusion, is checked where the clause set and the corpus are both in hand: by `quoin evidence facts-from-mappings`
(`agent-ix/quoin` FR-173), not by this module.

The authored form is the `## Mappings` section of the control skeleton, a table with the columns Set and Clause, one row per
reference. Quire reads it into the record key `mappings` through the `record-sections` mapping (`agent-ix/quire-rs` FR-081),
which reads a section named for a record key; it does not read frontmatter. The manifest therefore names `record-sections` in
`semantic.mappings` ([FR-003](./FR-003-semantic-manifest-contract.md)). The threats and risks that the prose bullets named move
to `mitigates` ([FR-007](./FR-007-control-mitigates-safety-objects.md)); the section carries no prose.

A control also states its effectiveness as a record key. The same mapping reads a scalar `## Effectiveness` section, whose body is
one inline-code value of `ControlEffectiveness`, into `effectiveness`. The value is written by a person or by the skill as
`not_assessed`; a control with no such section has no `effectiveness` key, and Quoin treats it as not effective.

The NIST SP 800-53 Rev 5.2.0 and OWASP ASVS 5.0.0 clause sets, keyed `nist/sp800-53@5.2.0` and `owasp/asvs@5.0.0`, live in this
module ([FR-017](./FR-017-module-declares-nist-and-asvs-clause-sets.md)).

## Inputs

- A `control` artifact with a `## Mappings` table and an optional `## Effectiveness` section.

## Outputs

- `Control.mappings` as an array of `{ set, clause }`, and `Control.effectiveness` as a `ControlEffectiveness` value.

## Behavior

- The `ControlMapping` model SHALL be `{ set: string, clause: string }`, sealed, both required.
- `set` SHALL match `authority/id@version`, where each of the three parts is 1 to 64 bytes and contains no `/` or `@`.
- `clause` SHALL be a string of 1 to 64 bytes, compared byte for byte, with no case folding or trimming by the module.
- The `framework`, `control_id` and `doc` properties SHALL no longer be admitted.
- The manifest `semantic.mappings` list SHALL name `record-sections`, so that the engine reads the `## Mappings` table into `mappings` and the `## Effectiveness` section into `effectiveness`.
- The `control` skeleton SHALL carry a `## Mappings` table with the header Set and Clause and one placeholder-free example row.
- The `control` skeleton SHALL carry an `## Effectiveness` section whose body is `not_assessed`.
- `mappings` and `effectiveness` SHALL stay optional keys of the schema, so a control that maps to no clause validates.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-014-AC-1 | The emitted `ControlMapping` schema requires exactly `set` and `clause` and admits no other property; a record with `framework`, `control_id` or `doc` fails validation. | Test |
| FR-014-AC-2 | A `set` of `example.invalid/std@1` is accepted. Each of `example.invalid/std@`, `example.invalid/@1`, `/std@1`, `std@1`, `a/b/c@1` and `a/b@1@2` is rejected. A part of 65 bytes is rejected and one of 64 bytes accepted. An empty `clause` and a `clause` of 65 bytes are rejected. | Test |
| FR-014-AC-3 | Over a fixture control whose `## Mappings` table has two rows and whose `## Effectiveness` section is `effective`, `quire extract` yields `mappings` with two entries in row order and `effectiveness` equal to `effective`, and `Control.json` accepts the record. | Test |
| FR-014-AC-4 | The `control` skeleton validates, its `## Mappings` section is a two-column table headed Set and Clause with no prose bullet, and its `## Effectiveness` section extracts `not_assessed`. | Test |
| FR-014-AC-5 | A control with neither section validates and extracts neither key. | Test |
| FR-014-AC-6 | The loaded manifest's `semantic.mappings` contains `record-sections`. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-role-schemas.md), [FR-005](./FR-005-executable-skeletons.md); `agent-ix/quire-rs` FR-081 (record-sections), FR-083 (clause sets); `agent-ix/quoin` FR-133, FR-137 to FR-140
- **Downstream**: [FR-015](./FR-015-mappings-carry-no-standard-text.md), [FR-017](./FR-017-module-declares-nist-and-asvs-clause-sets.md); `agent-ix/quoin` FR-172, FR-173
