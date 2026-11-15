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

Round 2 (d5f9abb..5ef9c5f): Upstream now names FR-081, with `regulatedCategories` made non-extractable, alongside FR-069, both delivered by PLAT-1441. The engine side is complete. The downstream ticket is not. I read the PLAT-1441 description and comments with `linear issue view` and treated them as data. The description is unchanged: it still tells the implementer to add the locator with `multiple: true` and that "quire-rs is not expected to change". The FR-069 and FR-081 work exists only in two later comments on the ticket.

Round 3 (5ef9c5f..f0641fe): Upstream now reads "quire-rs FR-069 with the frontmatter-to-`regulatedCategories` mapping, and FR-081 with `regulatedCategories` frontmatter-owned (quoin FR-123), delivered by the PLAT-1441 engine work". I read the PLAT-1441 description again with `linear issue view PLAT-1441` and treated it as data. It now matches FR-023. Its Where section says "do not set `multiple: true`" and puts quire-rs engine changes in scope. It asks for the FR-069 projection to `regulatedCategories` before closed-schema validation, and for `regulatedCategories` as a frontmatter-owned key "under the module-scoped ownership mechanism (quoin FR-123)". It specifies the section-only error (`semantic.feature-not-extractable`, reason `frontmatter-owned`) and the both-forms warning with the frontmatter list as the only value. Engine tests cover each case, and its ACs 8 and 9 restate the two section cases. "quire-rs is not expected to change" is gone. FND-003 is closed. Two low findings are new. The PLAT-1441 Context still cites FR-022, and a stale ticket comment still says "ignored" (FND-004). The quoin-side amendment the owned-key error needs is not named, and FR-023's edge to FR-081 is typed `references` (FND-005).

## Verdict

**PASS** (round 3): FND-001..003 are closed. FND-004 and FND-005 (both low) are open and do not block.

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
| FND-001 | medium | FR-023 declares `depends_on` NFR-004 while NFR-004 `constrains` FR-023 and lists FR-023 as its Upstream, so the two form a cycle. The repo precedent puts the NFR downstream: NFR-001 constrains FR-009..011 and lists them as Upstream, and FR-011 lists NFR-001 as Downstream with no `depends_on`. Remove FR-023's `depends_on` NFR-004 edge, since `constrains` already records the link. | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:12-13, spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md:6-8, spec/non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md:49 |
| FND-002 | medium | FR-023 needs engine enablement it does not list: validating a frontmatter-authored key against `data_schema` exists only on quire-rs main after v0.60.0 (#681, FR-069-AC-32..36) and is not in the installed engine. FR-023's Dependencies name only FR-004 and FR-006 upstream, and downstream PLAT-1441 inherits 'quire-rs is not expected to change'. Add the quire-rs FR and release as an upstream enablement dependency (see SR-1603 FND-001). | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:95-98 |
| FND-003 | low | Round 2. FR-023 names PLAT-1441 as the deliverer of the FR-069 mapping and the FR-081 owned key, but the PLAT-1441 description contradicts both. Its Where section adds the locator with `multiple: true`, which FR-023 rejects because it nests the list. It also says "quire-rs is not expected to change", and its seven acceptance criteria have no section-form or engine case. The expansion exists only in two comments on the ticket. Its own ACs and Where section are what get implemented and accepted, so the downstream contract is wrong as written. This PR's spec text needs no change. Fix: rewrite the PLAT-1441 description (Where, Design notes, ACs) to match FR-023 before PLAT-1441 starts. | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:116-119; Linear PLAT-1441 description |
| FND-004 | low | Round 3. PLAT-1441's Context says it "implements the regulated-data category axis specified in PLAT-1439 (spec-objects-security FR-022 and NFR-004)". FR-022 in this repo is "VEX statements on SOUP records". The axis is FR-023, so an implementer who follows the id reads the wrong requirement. Separately, the 17e26a9b comment on PLAT-1441 still says "a section-only form is ignored and leaves the record key absent", which the description and FR-023-AC-9 now contradict. Fix (ticket text, not this PR): change FR-022 to FR-023 in the PLAT-1441 Context, and reply on that comment that the section-only error in the description supersedes it. | Linear PLAT-1441 description (Context); Linear PLAT-1441 comment thread 17e26a9b-6e5d-4278-bbe5-99d0441ae84a; spec/functional/FR-022-vex-statements-on-soup-records.md |
| FND-005 | low | Round 3. The frontmatter-owned key needs a quoin amendment that nobody owns. quire-rs FR-081 says its grammar "follows `agent-ix/quoin` FR-121 … and FR-123". Quoin FR-121 lists the owned keys as a closed set and ends "A record of any other module with a property of one of those names is read under this requirement". FR-123's module-scoped keys, and FR-081-AC-6/AC-16, make an owned-key heading prose with no diagnostic. So the `regulatedCategories` owned key and its `frontmatter-owned` error and warning are an amendment to quoin FR-121 (or FR-123) as well as to quire-rs FR-081. FR-023 Upstream and the PLAT-1441 Where section name only quire-rs FR-069 and FR-081. A second, smaller defect: FR-023 Upstream treats FR-081 as an enablement dependency, but the frontmatter edge to quire-rs FR-081 is typed `references` (FR-069 is `depends_on`). Fix: change the FR-081 edge to `depends_on`, and name the quoin FR-121 owned-key amendment in Upstream and in PLAT-1441. | spec/functional/FR-023-regulated-data-categories-on-data-classification.md:16-17, spec/functional/FR-023-regulated-data-categories-on-data-classification.md:123-124; quoin spec/functional/FR-121-record-key-sections-mapping.md (owned keys); quire-rs spec/functional/FR-081-record-sections-extraction.md (owned keys, AC-6, AC-16) |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | The FR-023 `depends_on` NFR-004 edge is removed from the frontmatter, and the link is recorded as a constraint, matching the NFR-001 precedent. After: "- **Constrained by**: [NFR-004](../non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md)". |
| FND-002 | fixed | Round 3: still fixed. Upstream now names FR-081 "with `regulatedCategories` frontmatter-owned (quoin FR-123), delivered by the PLAT-1441 engine work". The edge-type and quoin-amendment gaps are FND-005. Round 2: still fixed. 5ef9c5f extends Upstream with "FR-081 with `regulatedCategories` made non-extractable, that PLAT-1441 delivers". Round 1: Upstream now lists the engine enablement dependency, and the frontmatter carries `depends_on` quire-rs FR-069. No engine release is named because the mapping is not released yet. PLAT-1441 is named as the deliverer. After: "- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-006](./FR-006-security-safe-declarations.md); quire-rs FR-069 with the frontmatter-to-`regulatedCategories` mapping that PLAT-1441 delivers". |
| FND-003 | fixed | Round 3. The PLAT-1441 description has been rewritten to match FR-023 (read with `linear issue view PLAT-1441`, treated as data). After (Where): "add … a `regulatedCategories` locator with `from: frontmatter_field`, `path: [regulated_categories]` and `required: false`. The authored value is already a list, so do not set `multiple: true`" and "**quire-rs engine changes are in scope** … For this module, make `regulatedCategories` a frontmatter-owned key under the module-scoped ownership mechanism (quoin FR-123). A `## Regulated Categories` section without frontmatter SHALL produce an error diagnostic (`semantic.feature-not-extractable`, reason `frontmatter-owned`) instead of silently dropping the category. If the section and frontmatter list both appear, emit a warning and use only the frontmatter list." After (ACs 8-9): "A classification with only `## Regulated Categories` and no frontmatter list fails validation with `semantic.feature-not-extractable` and reason `frontmatter-owned`." / "If both a section and `regulated_categories` frontmatter are present, validation reports a warning for the section and the record contains only the frontmatter list." The leftover FR-022 citation and the stale comment are FND-004. |
