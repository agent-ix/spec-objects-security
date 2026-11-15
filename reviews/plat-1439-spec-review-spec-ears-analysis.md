---
id: SR-1604
title: EARS conformance — FR-023 / NFR-004
type: SpecReview
analysis: ears-conformance
scope: agent-ix/spec-objects-security; spec/functional/FR-023-regulated-data-categories-on-data-classification.md, spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md, spec/functional/index.md, spec/non-functional/index.md
review_set: subset
relationships:
- target: ix://agent-ix/spec-objects-security/FR-023
  type: reviews
- target: ix://agent-ix/spec-objects-security/NFR-004
  type: reviews
---
# SR-1604: EARS conformance — FR-023 / NFR-004

## Summary

Ticket: PLAT-1439; PR agent-ix/spec-objects-security#60. EARS grammar over the FR-023 description statement, its Behavior SHALL bullets and the NFR-004 statement. FR-023's statement and its eight Behavior bullets are ubiquitous SHALL / SHALL NOT clauses with one subject each. NFR-004's statement has one non-conforming sentence.

Round 2 (d5f9abb..5ef9c5f): the only new normative text is the second Engine impact paragraph of FR-023. Its SHALL has a ticket as its subject (FND-002).

Round 3 (5ef9c5f..f0641fe): Engine impact now gives each SHALL a system as its subject: "The engine SHALL therefore make `regulatedCategories` a frontmatter-owned key" and "The engine SHALL report the two section cases". PLAT-1441 appears only descriptively ("are delivered by PLAT-1441"). The two new Behavior bullets are event-driven clauses with one subject and one response each: "When a `## Regulated Categories` section appears without frontmatter …, validation SHALL report an error …" and "When … both appear, validation SHALL report a warning, and the record SHALL use only the frontmatter list". No new EARS finding.

## Verdict

**PASS** (round 3): FND-001 and FND-002 are closed. No finding is open.

## Coverage

FR-023 and NFR-004 statements examined; ACs read as context.

Examined requirement units:

- `FR-023` (role: examined): The module SHALL let a person state, on a `data_classification`, the regulated-data categories its data belongs to: `health`, `personal` and `financial`. The categories are a separate axis from `level`.
- `FR-023-AC-1` (role: context_only): A classification with `regulated_categories: [health]` passes `quire validate`, and its extracted record carries `regulatedCategories: ["health"]` (a flat list, not a nested one).
- `FR-023-AC-2` (role: context_only): A classification with `regulated_categories: [medical]` fails `quire validate` with a located message naming `regulated_categories` (or `regulatedCategories`) and the value `medical`.
- `FR-023-AC-3` (role: context_only): A classification with `regulated_categories: []` fails validation, and one with a duplicated member (`[health, health]`) fails validation.
- `FR-023-AC-4` (role: context_only): A classification without the field validates, and its record has no `regulatedCategories` key. No default is filled in.
- `FR-023-AC-5` (role: context_only): `RegulatedDataCategory.json` has exactly the members `health`, `personal`, `financial`, and no `unknown` member.
- `FR-023-AC-6` (role: context_only): `[health, personal]` and `[financial]` validate; a classification with `level: restricted` and `regulated_categories: [health]` validates, and one with `regulated_categories: [health]` and no `personal` validates, so neither axis implies the other.
- `FR-023-AC-7` (role: context_only): The `data_classification` locator for `regulated_categories` has `required: false` and no `multiple: true`.
- `FR-023-AC-8` (role: context_only): The `data_classification` skeleton shows `regulated_categories` and validates with zero errors.
- `FR-023-AC-9` (role: context_only): A classification with a `## Regulated Categories` section and no frontmatter `regulated_categories` fails `quire validate` with an error diagnostic `semantic.feature-not-extractable`, reason `frontmatter-owned`, and the extracted record has no `regulatedCategories` key.
- `FR-023-AC-10` (role: context_only): A classification with a `## Regulated Categories` section and frontmatter `regulated_categories: [health]` reports a warning, and the extracted record carries `regulatedCategories: ["health"]` from the frontmatter only.
- `NFR-004` (role: examined): The module SHALL NOT derive or default a regulated-data category or a confidentiality level: a category comes only from the frontmatter `regulated_categories` field and a level only from the `## Properties` `level` row, each as written by a person, with no inference from any other field.
- `NFR-004-AC-1` (role: context_only): `regulatedCategories` has the `regulated_categories` frontmatter locator as its only source and `level` has the `## Properties` `level` row as its only source; the `data_classification` manifest entry has no other locator that yields either key and no `assert` or default value for either, and `DataClassification.json` carries no `default` for either.
- `NFR-004-AC-2` (role: context_only): A classification whose fields are named like health or personal data (for example `patient_name`) but that states no `regulated_categories` extracts a record with no `regulatedCategories` key.
- `NFR-004-AC-3` (role: context_only): Validating a classification that states `regulated_categories: [health]` and no `personal` emits `["health"]` exactly, and a classification without `level` extracts no `level` key.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The second sentence, 'A category reaches a record only as written by a person.', has no SHALL and covers only the category, while the title and first sentence cover category and level. Fold it into one SHALL clause covering both, or drop it as redundant. | spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md:16 |
| FND-002 | low | Round 2. 'PLAT-1441 SHALL therefore also make `regulatedCategories` non-extractable from record-sections in this module' makes a Linear ticket the subject of a SHALL. A ticket cannot conform to a requirement, and the clause repeats the Behavior bullet 'the schema property `regulatedCategories` SHALL NOT be a record-sections key'. Fix: say it descriptively ('PLAT-1441 makes …'), or give the SHALL a system subject (the engine's record-sections extraction SHALL NOT read `regulatedCategories`). | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:81-83 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | The NFR-004 statement is now one SHALL NOT clause that covers both category and level. After: "The module SHALL NOT derive or default a regulated-data category or a confidentiality level: a category comes only from the frontmatter `regulated_categories` field and a level only from the `## Properties` `level` row, each as written by a person, with no inference from any other field." |
| FND-002 | fixed | Round 3 (f0641fe). The ticket-subject SHALL is gone, and the engine is now the subject. After: "The engine SHALL therefore make `regulatedCategories` a frontmatter-owned key in this module, using the module-scoped ownership mechanism of quoin FR-123. … The engine SHALL report the two section cases as stated in Behavior". |
