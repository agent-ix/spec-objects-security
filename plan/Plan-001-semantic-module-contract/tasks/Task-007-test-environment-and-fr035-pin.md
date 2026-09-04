---
id: Task-007
title: "Test environment - engine provisioning, the no-vacuous-skip rule and the FR-035 pin"
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
# Task-007: Test environment - engine provisioning, the no-vacuous-skip rule and the FR-035 pin

## Scope

The environment every semantic row runs in, and the manifest gate that had to
be kept alive across the contract change.

## Subtasks

- [x] `make dev-quire` provisions the wheel exposing the semantic extraction
      entry point.
- [x] The semantic tests fail rather than skip when it is absent, naming the
      missing function, the target and agent-ix/quire-rs#392. The twenty-four
      skipping tests of agent-ix/spec-objects-security#10 now run.
- [x] A schema registry resolving every reference locally - module schemas from
      the committed tree, grammar models from the installed semantic-core.
- [x] The FR-035 gate keeps running: the CR-012 schema revision is pinned under
      `tests/fixtures/`, and a second test proves the pin differs from the
      newest released spec-artifacts-iso only at the CR-012 pointers, so the
      gate is narrowed to one known key rather than skipped.

## Deliverables

- `tests/conftest.py`, `tests/fixtures/module-manifest.cr-012.schema.json`,
  the `dev-quire` target

## Notes

agent-ix/spec-artifacts-iso#36 asks that no consumer weaken or skip its FR-035
gate while waiting for a release, and that a pinned copy prove its delta. That
is what the second test is; when the release lands it fails with an empty delta
and the pin is deleted.
