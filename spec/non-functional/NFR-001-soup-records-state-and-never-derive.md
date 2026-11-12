---
id: NFR-001
title: "SOUP records state facts and decisions and never derive a score or class"
type: NFR
quality_attribute: maintainability
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-009"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-security/FR-010"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-security/FR-011"
    type: "constrains"
---
# NFR-001: SOUP records state facts and decisions and never derive a score or class

## Statement

The `soup_record` schema SHALL contain no field whose value is computed from other fields.

The module SHALL NOT assign a score, rating, class, tier or level to a component.

## Scope

- Applies to: the `soup_record` schema, skeleton and manifest entry.
- Out of scope: the `severity` of a `vulnerability`, which is that object's own stated field.

## Rationale

A computed class reads as an assessment nobody made. Every value in a `soup_record` is either an
SBOM-stated fact, a reviewer-authored statement, or a person-owned disposition, so a reader
can always tell who said it.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| `soup_record` schema keys that hold a score, rating, class, tier or level | 0 | 0 | Test |
| `soup_record` keys whose value the module computes | 0 | 0 | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-001-AC-1 | The `soup_record` schema has no property named or typed as a score, rating, class, tier or level, and no property reuses `Severity`, `Likelihood` or `Impact`. | Test |
| NFR-001-AC-2 | Validating a fixture record emits exactly the keys the author wrote, with none added by the module. | Test |

## Verification

Both criteria are tests over the emitted schema and over a validated fixture.

## Dependencies

- **Upstream**: [FR-009](../functional/FR-009-soup-record-identity-and-promotion.md), [FR-010](../functional/FR-010-soup-record-fields.md), [FR-011](../functional/FR-011-soup-risk-disposition.md)
