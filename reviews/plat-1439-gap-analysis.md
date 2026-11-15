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

Round 2 (d5f9abb..5ef9c5f): FR-023 adds a second engine change, the record-sections owned key, and rewrites AC-7 and AC-9 to depend on it. The list of ACs that hold only once PLAT-1441 lands was not updated to include them (FND-002). The PLAT-1441 description still says `multiple: true` and "quire-rs is not expected to change". Its scope expansion exists only as two ticket comments, so an implementer working from the description builds the opposite of FR-023 (recorded in SR-1606 FND-003). There is still no implementation in this PR, so FR-023/NFR-004 criteria stay untagged, as expected.

Round 3 (5ef9c5f..f0641fe): the gate now reads "FR-023-AC-1 to AC-3 and AC-6 to AC-10 hold only once the engine work lands", so AC-7, AC-9 and the new AC-10 are covered. AC-7 has lost its engine clause and is now a pure Inspection of this module's locator. The two criteria outside the gate are correct to be outside it: AC-4 (absent field, no key) and AC-5 (enum members) hold on the current engine. PLAT-1441's description now lists the matching engine test cases (section-only error, section-plus-frontmatter warning). One low gap is left: NFR-004-AC-3 also needs the engine mapping, and nothing gates it (FND-003). `quoin matrix` was not re-run in round 3: this session's permission layer needs approval for it. No test or source changed in the PR, so the round-1 untagged result stands.

## Verdict

**PASS** (round 3): FND-001 and FND-002 are closed. FND-003 (low) is open and does not block.

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
- `FR-023-AC-7` (role: examined): The `data_classification` locator for `regulated_categories` has `required: false` and no `multiple: true`.
- `FR-023-AC-8` (role: examined): The `data_classification` skeleton shows `regulated_categories` and validates with zero errors.
- `FR-023-AC-9` (role: examined): A classification with a `## Regulated Categories` section and no frontmatter `regulated_categories` fails `quire validate` with an error diagnostic `semantic.feature-not-extractable`, reason `frontmatter-owned`, and the extracted record has no `regulatedCategories` key.
- `FR-023-AC-10` (role: examined): A classification with a `## Regulated Categories` section and frontmatter `regulated_categories: [health]` reports a warning, and the extracted record carries `regulatedCategories: ["health"]` from the frontmatter only.
- `NFR-004` (role: examined): The module SHALL NOT derive or default a regulated-data category or a confidentiality level: a category comes only from the frontmatter `regulated_categories` field and a level only from the `## Properties` `level` row, each as written by a person, with no inference from any other field.
- `NFR-004-AC-1` (role: examined): `regulatedCategories` has the `regulated_categories` frontmatter locator as its only source and `level` has the `## Properties` `level` row as its only source; the `data_classification` manifest entry has no other locator that yields either key and no `assert` or default value for either, and `DataClassification.json` carries no `default` for either.
- `NFR-004-AC-2` (role: examined): A classification whose fields are named like health or personal data (for example `patient_name`) but that states no `regulated_categories` extracts a record with no `regulatedCategories` key.
- `NFR-004-AC-3` (role: examined): Validating a classification that states `regulated_categories: [health]` and no `personal` emits `["health"]` exactly, and a classification without `level` extracts no `level` key.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-023-AC-2 (and AC-3) cannot be bound to a passing test on the installed engine: a frontmatter-located `regulated_categories` is never checked against the data schema, so `[medical]`, `[]` and `[health, health]` validate. PLAT-1441 states quire-rs is not expected to change, so the criteria would land as strict expected failures or vacuous schema-only tests. Give the engine dependency an owner before PLAT-1441 starts (see SR-1603 FND-001). | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:87-88, tests/test_soup_record.py:453-460 |
| FND-002 | medium | Round 2. Engine impact ends "FR-023-AC-1 to AC-3, AC-6 and AC-8 hold only once it lands", but 5ef9c5f made two more ACs depend on the new PLAT-1441 record-sections change. FR-023-AC-9 requires a section-only classification to extract no `regulatedCategories`. On quire-rs main, `RecordSchema::owner` gives `regulatedCategories` (a `ScalarArray(Text)`) the `RecordSections` owner, so the section fills the key and AC-9 fails. FR-023-AC-7 now inspects "the engine's record-sections extraction", which is quire-rs code, not this module, and so AC-7 cannot pass from this repo before the change lands. A test written for AC-9 now would be a strict expected failure that the gate list does not mention. Fix: add AC-7 and AC-9 to the gated list. Drop AC-7's engine clause, because AC-9 already tests the behaviour, or move it to a quire-rs AC. | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:86-87, spec/functional/FR-023-regulated-data-categories-on-data-classification.md:110-111, quire-rs src/semantic/record.rs (`owner`) |
| FND-003 | low | Round 3. NFR-004-AC-3 requires that a classification stating `regulated_categories: [health]` "emits `["health"]` exactly". That needs the same FR-069 frontmatter-to-`regulatedCategories` mapping as FR-023-AC-1, which the current engine does not perform. FR-023's gate covers only FR-023 criteria, and NFR-004 names no engine dependency, so an NFR-004-AC-3 test written before PLAT-1441 lands is an unlisted expected failure. Fix: add NFR-004-AC-3 to the FR-023 gate sentence, or add the PLAT-1441 engine dependency to NFR-004 Dependencies. | spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md:39, spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md:45-47, spec/functional/FR-023-regulated-data-categories-on-data-classification.md:93 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 3: still fixed. The engine test list in FR-023 and in the PLAT-1441 description now includes the section-only error and the section-plus-frontmatter warning. Round 2: still fixed. 5ef9c5f keeps the owner (PLAT-1441) and the engine test list, and adds the `## Regulated Categories` section case to it. Its new gating gap is FND-002. Round 1: d5f9abb rewrites FR-023 Engine impact: the engine change now has an owner (PLAT-1441), its test cases are listed, and FR-023-AC-1..3, AC-6 and AC-8 are gated on it landing. PLAT-1441's Where section already says to implement any engine change the spec names, in the quire-rs FR it names. After: "PLAT-1441 carries the engine change and its test cases: a valid list, an unknown member, an empty list, a duplicated member, an absent field, and a section-form attempt. This requirement does not promise that code. FR-023-AC-1 to AC-3, AC-6 and AC-8 hold only once it lands." |
| FND-002 | fixed | Round 3 (f0641fe). The gate now covers AC-7, AC-9 and AC-10. AC-7's engine clause is gone, and the section behaviour is tested by AC-9 and AC-10. After (Engine impact): "FR-023-AC-1 to AC-3 and AC-6 to AC-10 hold only once the engine work lands." After (AC-7): "The `data_classification` locator for `regulated_categories` has `required: false` and no `multiple: true`." |
