---
id: FR-016
title: "A mapping carries a set key and a clause id and never the text of a standard"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-014"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-006"
    type: "depends_on"
---
# FR-016: A mapping carries a set key and a clause id and never the text of a standard

## Description

Licence-restricted standards are served only from locally installed packs, by clause id. A control record lives in a
repository and can be public, so it SHALL carry no field that could hold what a clause says, a title, or a summary of
either. The sealed `{ set, clause }` shape of [FR-014](./FR-014-control-mappings-are-clause-references.md) is the
mechanism; this requirement states the rule it serves and its limits.

## Behavior

- The `ControlMapping` model SHALL declare no property other than `set` and `clause`.
- The `control` skeleton and the module SHALL contain no clause text, title or summary of any standard.
- The module SHALL NOT add a mapping field for a clause title, description, quotation or note.
- The author's own `clauses` and prose describe the control; they are the author's words and are outside this rule.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-016-AC-1 | A control mapping row carrying a third key (`title`, `text`, `note`) fails schema validation, for each of the three keys. | Test |
| FR-016-AC-2 | A `## Mappings` table with a third column is reported by Quire, and the extracted record holds no value from that column. | Test |
| FR-016-AC-3 | The emitted `ControlMapping.json` lists exactly the properties `set` and `clause`. | Test |

## Dependencies

- **Upstream**: [FR-014](./FR-014-control-mappings-are-clause-references.md), [FR-006](./FR-006-security-safe-declarations.md)
- **Downstream**: none
