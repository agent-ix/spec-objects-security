---
id: Task-008
title: "NFR-001 - additive compatibility against the frozen baseline"
type: Task
status: done
track: B
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-security/NFR-001
    type: references
  - target: ix://agent-ix/spec-objects-security/TC-100
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-101
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-102
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-103
    type: verifies
---
# Task-008: NFR-001 - additive compatibility against the frozen baseline

## Scope

The four compatibility metrics, measured against the Task-000 freeze.

## Subtasks

- [x] Zero 0.1.0 locators changed.
- [x] Zero traceability, lexicon, allowed-links or roles entries changed.
- [x] Every frozen skeleton validates under 0.2.0 with zero errors.
- [x] No frozen skeleton yields a record-invalid finding, asserted through the
      mechanism that makes it true - none declares `object:` - rather than
      assumed.
- [x] The `object:`-declaring legacy case carried as a strict expected failure
      on agent-ix/quire-rs#391.

## Deliverables

- `tests/test_additive_compatibility.py`

## Notes

The population is named and bounded: the twenty-three skeletons this repository
ships. Corpus artifacts outside it are deliberately not measured, and the
NFR-001 Scope section says so rather than implying a guarantee nothing tested.
