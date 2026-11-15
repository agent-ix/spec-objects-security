---
id: SR-1605
title: Integrity analysis — FR-023 / NFR-004
type: SpecReview
analysis: integrity
scope: agent-ix/spec-objects-security; spec/functional/FR-023-regulated-data-categories-on-data-classification.md, spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md, spec/functional/index.md, spec/non-functional/index.md
review_set: subset
relationships:
- target: ix://agent-ix/spec-objects-security/FR-023
  type: reviews
- target: ix://agent-ix/spec-objects-security/NFR-004
  type: reviews
---
# SR-1605: Integrity analysis — FR-023 / NFR-004

## Summary

Ticket: PLAT-1439; PR agent-ix/spec-objects-security#60. Structural integrity of the two new files and index entries: frontmatter, relationships, section set against sibling FRs/NFRs, index completeness, and cross-repository references. Index entries are complete and `quire validate` passes. Two low findings.

## Verdict

**CONDITIONAL** — two low findings; no structural errors.

## Coverage

All FR-023 and NFR-004 units examined for structure and references.

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
| FND-001 | low | FR-023 opens with ticket and id-numbering history ('Tracked by Linear PLAT-1439. The draft number FR-022 ... this is the next free id.') and NFR-004 with 'Tracked by Linear PLAT-1439.' (NFR-004:12). No other FR or NFR in this repo carries such a line. It is tracking record, not requirement content. Delete both lines. | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:19, spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md:12 |
| FND-002 | low | FR-023 `references` quire-rs FR-075 (model feature extraction tables) and lists FR-075, FR-090 and FR-091 as the FRs that need no amendment. None of them governs this mechanism. The FRs involved are quire-rs FR-011 (body-extraction DSL, `frontmatter_field`) and FR-069 (frontmatter projection into the record that `data_schema` validates), with FR-081 for record-sections. Point the reference at the FR actually relied on. | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:14-15, spec/functional/FR-023-regulated-data-categories-on-data-classification.md:72 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Both tracking lines are deleted. In each file the H1 is now followed directly by the first section. After (FR-023): "# FR-023: A data_classification states its regulated-data categories as a list separate from its confidentiality level / ## Description". After (NFR-004): "# NFR-004: A regulated-data category or confidentiality level reaches a record only as written by a person / ## Statement". |
| FND-002 | fixed | The FR-075 reference and the FR-075/FR-090/FR-091 no-amendment sentence are gone. The references now point at the mechanisms actually relied on. After: "- target: \"ix://agent-ix/quire-rs/FR-011\" type: \"references\" - target: \"ix://agent-ix/quire-rs/FR-069\" type: \"depends_on\" - target: \"ix://agent-ix/quire-rs/FR-081\" type: \"references\"". |
