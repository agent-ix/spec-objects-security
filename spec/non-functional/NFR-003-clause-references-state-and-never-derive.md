---
id: NFR-003
title: "Clause references and scope exclusions state references and never derive coverage"
type: NFR
quality_attribute: maintainability
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-014"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-security/FR-017"
    type: "constrains"
---
# NFR-003: Clause references and scope exclusions state references and never derive coverage

## Statement

The `control` mapping and `scope_exclusion` schemas SHALL contain no field whose value is computed from other fields.

The module SHALL NOT assign a coverage, compliance, score or percentage to a clause, a set or a control.

## Scope

- Applies to: `ControlMapping` and `ScopeExclusion` schemas, skeletons and manifest entries.
- Out of scope: compliance of a clause, which Quoin derives from attested facts (`agent-ix/quoin` FR-135).

## Rationale

A control that names a clause has said it answers it. Whether it does is a person's attestation. A coverage figure in
the record would read as an assessment nobody made.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| Properties of the two schemas that hold a computed value | 0 | 0 | Test |
| Keys in a validated fixture that the module added | 0 | 0 | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-003-AC-1 | Neither `ControlMapping.json` nor `ScopeExclusion.json` has a property named or typed as coverage, compliance, score, percentage, rating or status. | Test |
| NFR-003-AC-2 | Validating a fixture control and exclusion emits exactly the keys the author wrote. | Test |

## Verification

Both are tests over the emitted schemas and validated fixtures.

## Dependencies

- **Upstream**: [FR-014](../functional/FR-014-control-mappings-are-clause-references.md), [FR-017](../functional/FR-017-scope-exclusion-object.md)
