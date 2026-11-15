---
id: FR-023
title: "A data_classification states its regulated-data categories as a list separate from its confidentiality level"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-006"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-011"
    type: "references"
  - target: "ix://agent-ix/quire-rs/FR-069"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-081"
    type: "references"
---
# FR-023: A data_classification states its regulated-data categories as a list separate from its confidentiality level

## Description

A `data_classification` has a confidentiality `level` but says nothing about which regulated kind of data it describes, so
nothing can state that a flow carries health data. The module SHALL let a person state, on a `data_classification`, the
regulated-data categories its data belongs to: `health`, `personal` and `financial`. The categories are a separate axis from
`level`. Health data may be `confidential` or `restricted`; the module defines no consistency rule between the two. The axis
extends the existing `data_classification`; no parallel object type is added.

The category names are generic. The categories take their meaning from public law: "personal data" and "data concerning
health" in GDPR Art 4(1), Art 4(15) and Art 9, and "protected health information" in HIPAA, 45 CFR 160.103. This requirement
names and quotes no paywalled standard.

The `carries` edge that puts a classification on a connection is owned by `agent-ix/spec-objects-architecture` FR-013. The
trust-boundary crossing edge on a connection is owned by PLAT-1532. Boundary-crossing rules, denials and sinks are
[out of scope](#out-of-scope).

## Inputs

- A `data_classification` document whose frontmatter may carry `regulated_categories`.
- The `DataClassification` model in `typespec/main.tsp`.

## Outputs

- The closed enum `RegulatedDataCategory` with exactly `health`, `personal`, `financial`, emitted as
  `spec_objects_security/schemas/RegulatedDataCategory.json`.
- An optional `regulatedCategories` key on the `DataClassification` record and schema.
- A `frontmatter_field` locator on the `data_classification` manifest entry.

## Behavior

- The module SHALL declare `RegulatedDataCategory` as a closed enum whose members are exactly `health`, `personal` and
  `financial`.
- `RegulatedDataCategory` SHALL have no `unknown` member: a classification that names no category is not regulated-category
  data, and that is stated by leaving the field out. Adding a member is a spec change.
- `DataClassification` SHALL admit an optional `regulatedCategories`, a `RegulatedDataCategory[]` with at least one item and
  unique items.
- The `data_classification` manifest entry SHALL extract the frontmatter list `regulated_categories` into
  `regulatedCategories` with a `frontmatter_field` locator that has `required: false`. The located value is already a list,
  so the locator sets no `multiple: true`, which would wrap the list in a second array (see Engine impact).
- Frontmatter `regulated_categories` SHALL be the sole authored source of the categories. The module SHALL NOT accept a
  section form such as a `## Regulated Categories` section or a `## Properties` row for them, and the schema property
  `regulatedCategories` SHALL NOT be a record-sections key. The authored source of `level` stays as it is: its
  `## Properties` table row.
- `level` SHALL stay as it is, independent of the categories.
- `health` SHALL NOT imply `personal`; the author states each category.
- The schema SHALL carry no `default` for `regulatedCategories`
  ([NFR-004](../non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md)).
- The `data_classification` skeleton SHALL show `regulated_categories` in its frontmatter and validate with zero errors.

## Engine impact

A quire-rs change is required, owned by PLAT-1441. Current quire-rs does not validate `body_extraction` values against the
semantic `data_schema` (quire-rs FR-011 defines the extraction, and `data_schema` runs over the semantic declaration record),
and the frontmatter projection of quire-rs FR-069 keeps the authored key, `regulated_categories`. Against the closed
`DataClassification` schema that key is an unknown property, and `regulatedCategories` is never filled. So FR-069 (or the
quire-rs requirement that owns the projection) must map the frontmatter key `regulated_categories` into the extracted
`regulatedCategories` key before closed-schema validation, so that `enum`, `minItems` and `uniqueItems` apply to the list and
a bad member is reported with its path. PLAT-1441 carries the engine change and its test cases: a valid list, an unknown
member, an empty list, a duplicated member, an absent field, and a section-form attempt. This requirement does not promise
that code. FR-023-AC-1 to AC-3, AC-6 and AC-8 hold only once it lands.

The `multiple: true` setting named in the ticket's design notes would produce a list inside a list and is therefore not
used. A section form is not accepted, so quire-rs FR-081 record-sections extraction does not apply to `regulatedCategories`.

## Out of scope

- Boundary-crossing rules, denials and sinks (the LLM prompt and tool call): PLAT-1533, PLAT-1535, PLAT-1537, PLAT-1538.
- The trust-boundary crossing edge on a connection: PLAT-1532 owns it.
- Records of processing: PLAT-1657. The threat-model artifact: milestone M3.
- Any automatic derivation of category or level from field names, data schemas or code.
- A consistency rule between category and `level`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-023-AC-1 | A classification with `regulated_categories: [health]` passes `quire validate`, and its extracted record carries `regulatedCategories: ["health"]` (a flat list, not a nested one). | Test |
| FR-023-AC-2 | A classification with `regulated_categories: [medical]` fails `quire validate` with a located message naming `regulated_categories` (or `regulatedCategories`) and the value `medical`. | Test |
| FR-023-AC-3 | A classification with `regulated_categories: []` fails validation, and one with a duplicated member (`[health, health]`) fails validation. | Test |
| FR-023-AC-4 | A classification without the field validates, and its record has no `regulatedCategories` key. No default is filled in. | Test |
| FR-023-AC-5 | `RegulatedDataCategory.json` has exactly the members `health`, `personal`, `financial`, and no `unknown` member. | Test |
| FR-023-AC-6 | `[health, personal]` and `[financial]` validate; a classification with `level: restricted` and `regulated_categories: [health]` validates, and one with `regulated_categories: [health]` and no `personal` validates, so neither axis implies the other. | Test |
| FR-023-AC-7 | The `data_classification` locator for `regulated_categories` has `required: false` and no `multiple: true`, and no locator or record-sections key accepts a section form of the categories. | Inspection |
| FR-023-AC-9 | A classification that states the categories in a `## Regulated Categories` section and not in frontmatter extracts a record with no `regulatedCategories` key. | Test |
| FR-023-AC-8 | The `data_classification` skeleton shows `regulated_categories` and validates with zero errors. | Test |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-006](./FR-006-security-safe-declarations.md); quire-rs FR-069 with the
  frontmatter-to-`regulatedCategories` mapping that PLAT-1441 delivers
- **Constrained by**: [NFR-004](../non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md)
- **Downstream**: `agent-ix/spec-objects-architecture` FR-013 (the `carries` edge); PLAT-1440, PLAT-1441, PLAT-1532 (these tickets block on this spec)
