---
id: Task-006
title: "FR-003 - the optional locators the new sections need"
type: Task
status: done
track: A
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-security/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-security/TC-043
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-085
    type: verifies
---
# Task-006: FR-003 - the optional locators the new sections need

## Scope

Twenty-five `section_body` locators, all optional, asserting the
`## Properties`, `## Invariants` and `## Operations` sections the skeletons
introduced.

## Subtasks

- [x] One properties locator per field-bearing type, one invariants locator per
      clause-bearing type, one operations locator for `auth_flow`.
- [x] Every added locator optional, so no existing artifact is invalidated by
      the addition.

## Deliverables

- the `body_extraction` additions in `spec_objects_security/manifest.yaml`

## Notes

Ordered after Task-005 by intent: the section lands before the locator that
asserts it, so no intermediate commit asserts a heading nothing writes.
