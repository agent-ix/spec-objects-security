---
id: SR-1603
title: Base spec review — FR-023 / NFR-004 regulated-data categories
type: SpecReview
analysis: base
scope: agent-ix/spec-objects-security; spec/functional/FR-023-regulated-data-categories-on-data-classification.md, spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md, spec/functional/index.md, spec/non-functional/index.md
review_set: subset
relationships:
- target: ix://agent-ix/spec-objects-security/FR-023
  type: reviews
- target: ix://agent-ix/spec-objects-security/NFR-004
  type: reviews
---
# SR-1603: Base spec review — FR-023 / NFR-004 regulated-data categories

## Summary

Ticket: PLAT-1439; PR agent-ix/spec-objects-security#60. Base checklist over FR-023 and NFR-004: id formats, AC quality, test coverage and whether the requirements' claims about the engine hold. Ids are well-formed and unique (FR-023 and NFR-004 are the next free ids), every AC carries a verification method, and the licensing rule holds. The engine-impact claim is false, which breaks four ACs.

## Verdict

**FAIL** — FR-023's 'no quire-rs change' premise is contradicted by the engine, so FR-023-AC-1..3 and AC-7 cannot all hold as written.

## Coverage

Review set: subset (base + ears-conformance + integrity + dependency). No AssuranceProfile document exists in the repository; the dispatch states `review_policy: recommend`. No hash, digest, pin or tracking-record antipattern was added beyond the numbering note recorded in SR-1605 FND-001.

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
| FND-001 | high | FR-023 states no quire-rs change is needed because the frontmatter-located list is validated against `data_schema`. It is not: Reproduced on the installed engine (quire 0.45.0, engine 0.60.0) in a scratch copy of the module carrying the PR's locator (`regulatedCategories` from frontmatter `regulated_categories`, `required: false`) and schema key (`regulatedCategories`: array, `minItems: 1`, `uniqueItems`, enum of the three members): documents with `regulated_categories: [medical]`, `[]` and `[health, health]` all pass `quire validate` with exit 0, while the same module still refuses a document missing `## Handling` or the `level` row (exit 3), so the module was loaded. The engine runs `data_schema` only over the semantic declaration record (quire-rs `src/validate_document.rs:452`), never over the `body_extraction` yield. This repo already records the same gap as strict expected failures (`tests/test_soup_record.py:453-460`, `spec/tests.md:79-85`). On quire-rs main after v0.60.0 (#681, FR-069-AC-32..36) authored frontmatter is projected into the record under its authored name, so `regulated_categories` would hit the closed DataClassification schema (`unevaluatedProperties`) as an unknown key and camelCase `regulatedCategories` would never be filled, failing AC-1, AC-6 and AC-8 instead. Fix: drop the no-change claim and either key the schema property as authored (`regulated_categories`) on the FR-069 projection, naming the engine release it needs, or name the quire-rs FR to amend (ticket AC 3) and route it to PLAT-1441. | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:66-72, spec/functional/FR-023-regulated-data-categories-on-data-classification.md:92, quire-rs src/validate_document.rs:452, tests/test_soup_record.py:453-460 |
| FND-002 | medium | FR-023 names frontmatter as the authored form but not that it is the only one. A `regulatedCategories` property in DataClassification.json is also a record-sections key (quire-rs `src/semantic/record.rs` `owner` falls through to `RecordSections` for a readable array), so a `## Regulated Categories` section is a second authored source. With FR-069 projection, the two together raise `semantic.duplicate-record-key`. State the single authored source and what happens to the other. | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:55-58, quire-rs src/semantic/record.rs:313-360 |
| FND-003 | medium | 'the manifest entry declares no derivation of either' names no manifest construct: the manifest has no derivation feature, so the clause has no concrete thing a test can look for and passes for any manifest. Name the forbidden content, for example no locator other than the `regulated_categories` frontmatter_field and no `assert`/default value for either key. | spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md:39 |
