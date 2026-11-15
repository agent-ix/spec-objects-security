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

## Verdict

**PASS** — one low wording finding.

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
- `FR-023-AC-7` (role: context_only): The `data_classification` locator for `regulated_categories` has `required: false` and no `multiple: true`, and the module needs no quire-rs change.
- `FR-023-AC-8` (role: context_only): The `data_classification` skeleton shows `regulated_categories` and validates with zero errors.
- `NFR-004` (role: examined): The module SHALL NOT derive or default a regulated-data category or a confidentiality level. A category reaches a record only as written by a person.
- `NFR-004-AC-1` (role: context_only): `DataClassification.json` carries no `default` for `regulatedCategories` or `level`, and the manifest entry declares no derivation of either.
- `NFR-004-AC-2` (role: context_only): A classification whose fields are named like health or personal data (for example `patient_name`) but that states no `regulated_categories` extracts a record with no `regulatedCategories` key.
- `NFR-004-AC-3` (role: context_only): Validating a classification that states `regulated_categories: [health]` and no `personal` emits `["health"]` exactly, and a classification without `level` extracts no `level` key.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The second sentence, 'A category reaches a record only as written by a person.', has no SHALL and covers only the category, while the title and first sentence cover category and level. Fold it into one SHALL clause covering both, or drop it as redundant. | spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md:16 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | The NFR-004 statement is now one SHALL NOT clause that covers both category and level. After: "The module SHALL NOT derive or default a regulated-data category or a confidentiality level: a category comes only from the frontmatter `regulated_categories` field and a level only from the `## Properties` `level` row, each as written by a person, with no inference from any other field." |
