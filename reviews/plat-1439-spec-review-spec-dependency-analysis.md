---
id: SR-1606
title: Dependency analysis — FR-023 / NFR-004
type: SpecReview
analysis: dependency
scope: agent-ix/spec-objects-security; spec/functional/FR-023-regulated-data-categories-on-data-classification.md, spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md, spec/functional/index.md, spec/non-functional/index.md
review_set: subset
relationships:
- target: ix://agent-ix/spec-objects-security/FR-023
  type: reviews
- target: ix://agent-ix/spec-objects-security/NFR-004
  type: reviews
---
# SR-1606: Dependency analysis — FR-023 / NFR-004

## Summary

Ticket: PLAT-1439; PR agent-ix/spec-objects-security#60. The new `relationships` edges and Dependencies sections. FR-023 implements US-001 and depends on FR-004 and FR-006, which hold. Two defects: a dependency cycle with NFR-004, and an unstated enablement dependency on the engine.

## Verdict

**CONDITIONAL** — two medium findings.

## Coverage

FR-023 and NFR-004 frontmatter edges and Dependencies sections examined; ACs read as context.

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
| FND-001 | medium | FR-023 declares `depends_on` NFR-004 while NFR-004 `constrains` FR-023 and lists FR-023 as its Upstream, so the two form a cycle. The repo precedent puts the NFR downstream: NFR-001 constrains FR-009..011 and lists them as Upstream, and FR-011 lists NFR-001 as Downstream with no `depends_on`. Remove FR-023's `depends_on` NFR-004 edge, since `constrains` already records the link. | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:12-13, spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md:6-8, spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md:49 |
| FND-002 | medium | FR-023 needs engine enablement it does not list: validating a frontmatter-authored key against `data_schema` exists only on quire-rs main after v0.60.0 (#681, FR-069-AC-32..36) and is not in the installed engine. FR-023's Dependencies name only FR-004 and FR-006 upstream, and downstream PLAT-1441 inherits 'quire-rs is not expected to change'. Add the quire-rs FR and release as an upstream enablement dependency (see SR-1603 FND-001). | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:95-98 |
