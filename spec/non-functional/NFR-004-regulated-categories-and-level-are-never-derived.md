---
id: NFR-004
title: "A regulated-data category or confidentiality level reaches a record only as written by a person"
type: NFR
quality_attribute: maintainability
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-023"
    type: "constrains"
---
# NFR-004: A regulated-data category or confidentiality level reaches a record only as written by a person

Tracked by Linear PLAT-1439.

## Statement

The module SHALL NOT derive or default a regulated-data category or a confidentiality level. A category reaches a record only as written by a person.

## Scope

- Applies to: the `DataClassification` schema, skeleton and manifest entry, and `RegulatedDataCategory`.
- Out of scope: the confidentiality `level` of other object types, which [FR-006](../functional/FR-006-security-safe-declarations.md) governs.

## Rationale

A category inferred from a field name, a data schema or code would read as a person's judgement that nobody made, and a wrong
inference would hide health data from the rules that depend on it. An absent category means nobody stated one.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| `default` keywords for `regulatedCategories` or `level` in emitted schemas | 0 | 0 | Test |
| Category or level keys in an extracted record that the author did not write | 0 | 0 | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-004-AC-1 | `DataClassification.json` carries no `default` for `regulatedCategories` or `level`, and the manifest entry declares no derivation of either. | Test |
| NFR-004-AC-2 | A classification whose fields are named like health or personal data (for example `patient_name`) but that states no `regulated_categories` extracts a record with no `regulatedCategories` key. | Test |
| NFR-004-AC-3 | Validating a classification that states `regulated_categories: [health]` and no `personal` emits `["health"]` exactly, and a classification without `level` extracts no `level` key. | Test |

## Verification

Tests over the emitted schema and validated fixtures.

## Dependencies

- **Upstream**: [FR-023](../functional/FR-023-regulated-data-categories-on-data-classification.md)
