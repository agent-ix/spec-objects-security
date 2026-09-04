---
id: Task-005
title: "FR-005 - twenty-three executable skeletons, three alternates, ten negatives"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-security/TC-080
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-081
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-082
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-083
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-084
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-085
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-086
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-087
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-088
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-089
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-090
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-074
    type: verifies
---
# Task-005: FR-005 - twenty-three executable skeletons, three alternates, ten negatives

## Scope

Every skeleton rewritten as a typed fixture, the alternate-form skeletons, and
the negative fixtures that pin what the schemas and the engine refuse.

## Subtasks

- [x] Eighteen field-bearing skeletons author a typed `## Properties` table;
      six clause-bearing skeletons author `## Invariants` with one clause fence
      per heading; `auth_flow` authors `## Operations`.
- [x] Every skeleton carries `object:` beside `type:`, without which Quire
      validates headings only and the typed record is never checked.
- [x] Titles are distinct identifiers outside the kernel scalar names, so a
      Type cell can name another skeleton and resolve under the bundle index.
- [x] Three alternate skeletons extract to fields identical to their tables.
- [x] Ten negative fixtures, each failing with its own expected code.
- [x] No skeleton or fixture carries a credential-shaped literal; the scan is
      the gate for free text, since no schema can forbid a string.

## Deliverables

- `spec_objects_security/skeletons/*.md`, `tests/fixtures/negative/*.md`

## Notes

Constraint cells use only the keywords the pinned reader accepts. `pattern` is
refused (agent-ix/quire-rs#397) and a multi-valued `enumValues` is split or
silently truncated (agent-ix/quire-rs#401, filed by this ticket), so the closed
vocabularies live in emitted enum schemas and each graded value is authored as
a named field row instead. Neither defect is worked around by inventing a cell
form.
