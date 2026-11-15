---
id: SR-1602
title: Gap analysis — FR-023 / NFR-004 regulated-data categories
type: SpecReview
analysis: gap-analysis
scope: agent-ix/spec-objects-security; spec/functional/FR-023-regulated-data-categories-on-data-classification.md, spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md, spec/functional/index.md, spec/non-functional/index.md
review_set: subset
relationships:
- target: ix://agent-ix/spec-objects-security/FR-023
  type: reviews
- target: ix://agent-ix/spec-objects-security/NFR-004
  type: reviews
---
# SR-1602: Gap analysis — FR-023 / NFR-004 regulated-data categories

## Summary

Ticket: PLAT-1439; PR agent-ix/spec-objects-security#60. Planless gap analysis over the PR's new requirements. `quoin matrix --repo . --json` lists FR-023-AC-1..8, NFR-004-AC-1..3 and NFR-004-M-1..2 as `untagged` with no run evidence, and no test or source file carries those ids. That is expected for a spec-first PR whose implementation is PLAT-1441 (vocabulary) and PLAT-1440 (connections), both Backlog. The one real gap is that two Test criteria have no implementable binding on the installed engine, and the implementation ticket is told no engine work is needed.

## Verdict

**CONDITIONAL** — untagged criteria are expected at spec stage; FR-023-AC-2/AC-3 have no path to a passing test without engine work nobody owns.

## Coverage

Plan completion: not assessed. No production code changed in this PR. Optional semantic review not requested and skipped.

Examined requirement units:

- `FR-023` (role: examined): The module SHALL let a person state, on a `data_classification`, the regulated-data categories its data belongs to: `health`, `personal` and `financial`. The categories are a separate axis from `level`.
- `FR-023-AC-1` (role: examined): A classification with `regulated_categories: [health]` passes `quire validate`, and its extracted record carries `regulatedCategories: ["health"]` (a flat list, not a nested one).
- `FR-023-AC-2` (role: examined): A classification with `regulated_categories: [medical]` fails `quire validate` with a located message naming `regulated_categories` (or `regulatedCategories`) and the value `medical`.
- `FR-023-AC-3` (role: examined): A classification with `regulated_categories: []` fails validation, and one with a duplicated member (`[health, health]`) fails validation.
- `FR-023-AC-4` (role: examined): A classification without the field validates, and its record has no `regulatedCategories` key. No default is filled in.
- `FR-023-AC-5` (role: examined): `RegulatedDataCategory.json` has exactly the members `health`, `personal`, `financial`, and no `unknown` member.
- `FR-023-AC-6` (role: examined): `[health, personal]` and `[financial]` validate; a classification with `level: restricted` and `regulated_categories: [health]` validates, and one with `regulated_categories: [health]` and no `personal` validates, so neither axis implies the other.
- `FR-023-AC-7` (role: examined): The `data_classification` locator for `regulated_categories` has `required: false` and no `multiple: true`, and the module needs no quire-rs change.
- `FR-023-AC-8` (role: examined): The `data_classification` skeleton shows `regulated_categories` and validates with zero errors.
- `NFR-004` (role: examined): The module SHALL NOT derive or default a regulated-data category or a confidentiality level. A category reaches a record only as written by a person.
- `NFR-004-AC-1` (role: examined): `DataClassification.json` carries no `default` for `regulatedCategories` or `level`, and the manifest entry declares no derivation of either.
- `NFR-004-AC-2` (role: examined): A classification whose fields are named like health or personal data (for example `patient_name`) but that states no `regulated_categories` extracts a record with no `regulatedCategories` key.
- `NFR-004-AC-3` (role: examined): Validating a classification that states `regulated_categories: [health]` and no `personal` emits `["health"]` exactly, and a classification without `level` extracts no `level` key.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-023-AC-2 (and AC-3) cannot be bound to a passing test on the installed engine: a frontmatter-located `regulated_categories` is never checked against the data schema, so `[medical]`, `[]` and `[health, health]` validate. PLAT-1441 states quire-rs is not expected to change, so the criteria would land as strict expected failures or vacuous schema-only tests. Give the engine dependency an owner before PLAT-1441 starts (see SR-1603 FND-001). | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:87-88, tests/test_soup_record.py:453-460 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | d5f9abb rewrites FR-023 Engine impact: the engine change now has an owner (PLAT-1441), its test cases are listed, and FR-023-AC-1..3, AC-6 and AC-8 are gated on it landing. PLAT-1441's Where section already says to implement any engine change the spec names, in the quire-rs FR it names. After: "PLAT-1441 carries the engine change and its test cases: a valid list, an unknown member, an empty list, a duplicated member, an absent field, and a section-form attempt. This requirement does not promise that code. FR-023-AC-1 to AC-3, AC-6 and AC-8 hold only once it lands." |
