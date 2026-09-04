---
id: Task-003
title: "FR-002 - emitted set, toolchain.json, digests and packaging"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-security/TC-020
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-021
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-022
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-025
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-026
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-027
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-041
    type: verifies
---
# Task-003: FR-002 - emitted set, toolchain.json, digests and packaging

## Scope

The emitted-set half of FR-002, which exists only once Task-002 has declared
the models.

## Subtasks

- [x] Assert the emitted set equals the twenty-three object-type models plus
      the twenty-four declared support models, with compiler, emitter and
      semantic-core versions recorded in `toolchain.json`.
- [x] Every `$id` under the manifest-version base; every `$ref` a shipped
      sibling or semantic-core 0.1.0.
- [x] Wheel and npm tarball carry every exported schema beside the manifest.
- [x] The coordinated bump re-emits every `$id`, `$ref` and digest; half a bump
      is refused.

## Deliverables

- `spec_objects_security/schemas/toolchain.json` and the packaging assertions

## Notes

No test hard-codes the `$id` version segment: each reads it from the manifest
`version`, and TC-033 asserts that of the test suite itself.
