---
id: Task-004
title: "FR-003 - manifest 0.2.0, semantic block, reference-form data_schema and the freeze"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-security/TC-040
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-042
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-043
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-044
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-045
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-047
    type: verifies
---
# Task-004: FR-003 - manifest 0.2.0, semantic block, reference-form data_schema and the freeze

## Scope

The manifest at version 0.2.0: the nine-key `semantic` block, a reference-form
`data_schema` per exported type, and the freeze that protects the sibling
safety module.

## Subtasks

- [x] `semantic` block with exactly the nine admitted keys and all twenty-three
      exports.
- [x] Reference-form `data_schema` per type; no inline schema survives.
- [x] Every 0.1.0 locator unchanged against the frozen baseline.
- [x] `traceability`, `lexicon`, and every `allowed_links` and `roles` map
      equal to the baseline.
- [x] The registry loads all twenty-three archetypes; an unknown `semantic` key
      and an altered digest are each refused.

## Deliverables

- `spec_objects_security/manifest.yaml` at version 0.2.0

## Notes

The registry loader takes search paths that contain modules, not a module
directory: handed the module itself it finds nothing, lists nothing, and a
"does the registry load" test passes against an empty set. The test says so.

The freeze is stated for the right reason. `agent-ix/spec-objects-safety` reads
no field of this manifest today; what couples the repositories is the
traceability shape it mirrored from here, and this module's
`control.allowed_links.mitigates` list, which excludes hazard and failure mode
and so decides whether a security control can ever satisfy a safety coverage
check.
