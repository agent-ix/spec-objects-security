---
id: Task-000
title: "Freeze the 0.1.0 baseline before anything is edited"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-security/NFR-001
    type: references
---
# Task-000: Freeze the 0.1.0 baseline before anything is edited

## Scope

The 0.1.0 manifest and its twenty-three skeletons, copied to
`tests/fixtures/baseline-0.1.0/` before a single byte of either is changed.

## Subtasks

- [x] Copy `spec_objects_security/manifest.yaml` and every `skeletons/*.md` at
      version 0.1.0 into `tests/fixtures/baseline-0.1.0/`.
- [x] Assert the frozen copy is what it claims: `version: 0.1.0`, twenty-three
      skeletons, the same twenty-three type names.

## Deliverables

- `tests/fixtures/baseline-0.1.0/manifest.yaml` and `skeletons/*.md`

## Notes

This task exists because every locator, edge-vocabulary and additive criterion
of FR-003 and NFR-001 compares the live manifest against this copy. Freezing it
after the manifest is edited makes all four criteria compare the manifest
against itself and pass vacuously, so it runs first rather than alongside.
