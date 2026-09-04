---
id: Task-002
title: "FR-004 and FR-006 - twenty-three role-distinct models and twenty-four support models"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-security/FR-006
    type: references
  - target: ix://agent-ix/spec-objects-security/TC-050
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-051
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-052
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-053
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-054
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-055
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-056
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-057
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-058
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-059
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-060
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-061
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-062
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-063
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-070
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-071
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-072
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-073
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-075
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-076
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-077
    type: verifies
---
# Task-002: FR-004 and FR-006 - twenty-three role-distinct models and twenty-four support models

## Scope

One model per security object type, sealed, with its required keys and item
rules; the twelve open marker models the `contains` predicates need; the two
support records; and the ten closed graded vocabularies.

## Subtasks

- [x] Twenty-three sealed models grouped by security role: catalogued
      identities require `fields` with an identity row; the four assessment
      types additionally require the row that scores them; the five governing
      types require at least one clause; `auth_flow` requires its operations;
      `audit_event` declares an occurrence and refuses identity.
- [x] Every grammar item by reference to semantic-core 0.1.0; no redeclaration.
- [x] Ten closed vocabularies, each with an explicit unassessed member, and the
      two ordered ones starting at their least-granting state.
- [x] Every negative item rule encoded as `items` over `not`, never as a
      counting predicate.
- [x] The defaulted-field refusal extended to operation parameters on every
      guarded type that admits operations.
- [x] No `default` in schema position anywhere.

## Deliverables

- `typespec/main.tsp` (all models), `spec_objects_security/schemas/*.json`

## Notes

The encoding choice is a security decision, not a style one. A validator that
does not implement `minContains` and `maxContains` - precisely the
generated-fixture and frontend population these rules exist for - reads a bare
`contains` as "at least one item matches", inverting "no defaulted field" into
"carries a defaulted field". The `items`/`not` form cannot invert, and TC-076
asserts that no schema carries a counting keyword.

The parameter guard matters because `auth_flow` requires its operations while
its guarded `fields` key is optional and no skeleton authors it: without the
guard the rule reaches nothing on the one type whose exchanges name a code and
a verifier.

Gate 1 of the plan sits here: three types spanning the three shapes were
validated against the real 2020-12 validator, with the schemas sealed, before
the other twenty were written.
