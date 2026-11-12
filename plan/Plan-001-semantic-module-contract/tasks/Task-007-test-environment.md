---
id: Task-007
title: "Test environment - engine provisioning, the no-vacuous-skip rule"
type: Task
status: done
track: B
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-security/FR-001
    type: references
  - target: ix://agent-ix/spec-objects-security/TC-001
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-002
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-003
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-004
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-005
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-006
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-007
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-008
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-009
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-010
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-011
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-012
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-013
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-014
    type: verifies
---
# Task-007: Test environment - engine provisioning, the no-vacuous-skip rule

## Scope

The environment every semantic row runs in.

## Subtasks

- [x] `make dev-quire` provisions the wheel exposing the semantic extraction
      entry point.
- [x] The semantic tests fail rather than skip when it is absent, naming the
      missing function, the target and agent-ix/quire-rs#392. The twenty-four
      skipping tests of agent-ix/spec-objects-security#10 now run.
- [x] A schema registry resolving every reference locally - module schemas from
      the committed tree, grammar models from the installed semantic-core.

## Deliverables

- `tests/conftest.py`, the `dev-quire` target
