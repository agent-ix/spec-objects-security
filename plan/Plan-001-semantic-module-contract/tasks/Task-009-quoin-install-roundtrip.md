---
id: Task-009
title: "IT-002 - Quoin install roundtrip with unconditional restore"
type: Task
status: blocked
track: C
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-security/IT-002
    type: references
  - target: ix://agent-ix/spec-objects-security/TC-046
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-110
    type: verifies
---
# Task-009: IT-002 - Quoin install roundtrip with unconditional restore

## Scope

The install boundary between this module directory and the Quoin module
installer.

## Subtasks

- [x] Automate the precondition: the module directory the roundtrip would hand
      to Quoin is complete and self-consistent.
- [ ] Record the module listing, install by path, assert exit zero with no
      semantic error diagnostic, assert the listing and the derived package
      manifest, and restore the prior state unconditionally.

## Deliverables

- `tests/test_quoin_install_roundtrip.py` (precondition half)

## Notes

Blocked: it needs a Quoin built from agent-ix/quoin main at or after 3e842ce,
and no release tag carries the semantic module installer. The rows stay in
progress and say so; nothing here reports the manual half as done.
