---
id: Task-010
title: "FR-001, StR-001 and IT-001 - activation re-verification and the rows a human owns"
type: Task
status: blocked
track: C
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-001
    type: references
  - target: ix://agent-ix/spec-objects-security/IT-001
    type: references
  - target: ix://agent-ix/spec-objects-security/StR-001
    type: references
  - target: ix://agent-ix/spec-objects-security/TC-015
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-016
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-017
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-018
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-019
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-111
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-112
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-113
    type: verifies
---
# Task-010: FR-001, StR-001 and IT-001 - activation re-verification and the rows a human owns

## Scope

The criteria that need a running filament-core-service or a human, now that the
manifest has changed under them.

## Subtasks

- [x] StR-001-VC-3 as an executable demonstration: two records of different
      types are distinguishable by schema alone.
- [ ] Re-verify activation against a running filament-core: 200 on a clean
      instance, a content-hash no-op on re-activation, every declared
      contribution in the registry tables.
- [ ] A generator run producing a valid artifact from a shipped skeleton.

## Deliverables

- the StR-001-VC-3 demonstration test; matrix rows TC-015 to TC-019, TC-112 and
  TC-113 carrying their blocking environment

## Notes

agent-ix/filament-core-service#23 is why the reference-form `data_schema` is
still stored verbatim rather than resolved into a snapshot; FR-001-AC-4 asserts
what the service does today, not what it will do.
