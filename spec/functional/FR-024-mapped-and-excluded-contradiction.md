---
id: FR-024
title: "A clause that is both mapped by a control and excluded from scope is reported"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-020"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-023"
    type: "depends_on"
---
# FR-024: A clause that is both mapped by a control and excluded from scope is reported

## Description

A component cannot both answer a clause with a control and declare the clause outside its scope. The module SHALL
report the contradiction within one corpus so that Quoin never receives a clause that is simultaneously evidence and
delegation.

## Behavior

- Quire SHALL report, as an error `clause-mapped-and-excluded`, a `(set, clause)` pair that appears in a `control` mapping and in a `scope_exclusion` of the same corpus, naming the control and the exclusion.
- Quire SHALL report two `scope_exclusion` records for one `(set, clause)` as an error `scope-exclusion-duplicate`.
- The findings SHALL not depend on whether the clause set is loaded.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-024-AC-1 | A corpus with a control mapping `(example.invalid/std@1, C1)` and a `scope_exclusion` for the same pair yields one `clause-mapped-and-excluded` error naming both artifacts. | Test |
| FR-024-AC-2 | Different clauses in the control and the exclusion yield no finding. | Test |
| FR-024-AC-3 | Two exclusions for one pair yield one `scope-exclusion-duplicate` error. | Test |
| FR-024-AC-4 | The findings appear with the set not loaded. | Test |

## Dependencies

- **Upstream**: [FR-020](./FR-020-control-mappings-are-clause-references.md), [FR-023](./FR-023-scope-exclusion-object.md)
- **Downstream**: none
