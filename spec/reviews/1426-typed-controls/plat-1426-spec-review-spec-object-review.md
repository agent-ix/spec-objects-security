---
id: SR-042
title: "Spec object review of PR #49 ControlMapping and scope_exclusion"
type: SpecReview
analysis: base
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-004-role-schemas.md, spec/functional/FR-014..FR-018, spec/non-functional/NFR-003-clause-references-state-and-never-derive.md (PR #49, git diff origin/main...HEAD at d3658e0); companion agent-ix/quoin#871 FR-171..FR-174, NFR-038 read as context"
---
# SR-042: Spec object review of PR #49 ControlMapping and scope_exclusion

## Summary

Ticket: PLAT-1426. This review covers the domain objects only:
`ControlMapping` (FR-014, FR-016), the new `scope_exclusion` type (FR-017), the
cross-object rule of FR-018, and NFR-003. It also checks that these objects
agree with the companion quoin#871 (FR-171 to FR-174, NFR-038) that consumes
them. The method is spec-review / spec-object-review. The SpecReview `analysis`
enum has no object-review value, so `analysis: base` is used.

Scope-item check against PLAT-1426, with both PRs read together:

- Replace the prose section with controls that map clause ids: decided
  (FR-014, quoin FR-171).
- Publishable sets as clause sets: decided in quoin FR-172. That requirement
  homes the NIST and ASVS sets in this module, but this repo's spec does not say
  so (FND-005).
- Licensed sources served by clause id from local packs: decided (FR-016,
  quoin FR-172).
- Feeding record-discharge and the RMM: decided (quoin FR-173, FR-174).
- Out-of-scope controls get a typed disposition with an owner: decided
  (FR-017, quoin FR-173).
- No cleanup of standard names: decided (quoin FR-171).

## Verdict

**FAIL**: three medium findings and two low. The objects are sound in intent.
`ControlMapping` is sealed and carries no text. `scope_exclusion` is a
boundary declaration with no approval property, and approval stays a
person-owned quoin FR-046 fact, which NFR-003 and quoin NFR-038 agree on. The
gaps are in how the authored documents produce these records, and in one input
that quoin FR-173 consumes but neither PR defines. FR-015, FR-018 and NFR-003
are clean at the object level; their engine-ownership gap is SR-041.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-017 does not state where an author writes a `scope_exclusion`'s `set`, `clause`, `owner` and `rationale`. They could be frontmatter keys, `##` sections, or a typed table. It also does not state which manifest locators or required headings the type gets. FR-017-AC-2 ("a record without `owner` fails validation") and AC-4 ("the skeleton validates") can therefore be met in incompatible ways. If they are frontmatter keys, this repo's own tests.md (TC-124, TC-125) records that "the frontmatter record keys of an authored document are neither validated against the data schema nor projected into the extracted record", so an authored exclusion with no owner would not fail today. Name the authored form, its locators, and the engine path (quire-rs FR-081 record-sections, or frontmatter projection) | spec/functional/FR-017-scope-exclusion-object.md:33-38, spec/functional/FR-017-scope-exclusion-object.md:45, spec/functional/FR-017-scope-exclusion-object.md:47, spec/tests.md:224-225 |
| FND-002 | medium | quoin#871 FR-173 emits a `direct` fact only for a control that "states `effectiveness: effective`", and FR-171 writes "a control's `effectiveness` row as `not_assessed`". In this module, a control's effectiveness is only a `FieldDecl` row (`\| effectiveness \| String \| 1..1 \| minLength: 1 \|` in the skeleton), which declares that the field exists and carries no value. FR-004 Behavior lists the typed `effectiveness` key as one the extractor does not populate. Neither PR decides where a control's effectiveness value is authored, or how it reaches the record that `facts-from-mappings` reads. Every control would therefore yield no fact. Decide the authored form here, because this module owns the control's shape | spec/functional/FR-004-role-schemas.md:76, spec/functional/FR-004-role-schemas.md:94, spec_objects_security/skeletons/control.md:29 |
| FND-003 | medium | FR-016-AC-2 says "A `## Mappings` table with a third column is reported by Quire". It names no diagnostic code and no owning engine behaviour, and it does not say whether the record still extracts with two keys or is refused. Two implementers could read it differently, for example as a `semantic.invalid-model-cell` refusal that leaves `mappings` unavailable, or as a warning with the column dropped. Name the code and the extraction outcome | spec/functional/FR-016-mappings-carry-no-standard-text.md:34 |
| FND-004 | low | FR-014-AC-2's negative `example.invalid//1` lacks the `@` as well, so it does not isolate an empty `id` part. No negative case covers a part that contains `/` or `@` (for example `a/b/c@1` or `a/b@1@2`), although Behavior forbids it. A pattern such as `^[^/@]+/.*@[^/@]+$`, which admits an empty or slash-bearing id, passes the AC. Use `example.invalid/@1` and add one embedded-separator case | spec/functional/FR-014-control-mappings-are-clause-references.md:40, spec/functional/FR-014-control-mappings-are-clause-references.md:52 |
| FND-005 | low | quoin#871 FR-172 says the `nist/sp800-53@r5` and `owasp/asvs@5.0.0` clause sets are "published as clause sets in the `spec-objects-security` module", but this repo's spec says nothing about the module declaring `clause_sets` (quire-rs FR-083). The spec-objects-security half of PLAT-1426 scope item 2 is left to PLAT-1521 and PLAT-1522 without a line here. Add one sentence, or a Dependencies entry, that names this module as the home and those tickets as the owners | spec/functional/FR-014-control-mappings-are-clause-references.md:59 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-006 | high | `## Owner` can never populate `owner`, so the claim that no quire-rs change is needed is false for `scope_exclusion`. FR-081 lists "the FR-075 systems members" among the keys that record-sections never reads, and quire-rs `src/semantic/record.rs` `SYSTEMS_MEMBERS` starts with `"owner"`. Measured with the quire 0.58.0 wheel against a scratch module that has a sealed `ScopeExclusion` and required `## Set/Clause/Owner/Rationale` locators. A complete exclusion fails `semantic.record-invalid ... "owner" is a required property`, with or without a bundle package. FR-016-AC-4 (the skeleton validates and extracts four keys) therefore cannot pass, and the second half of FR-016-AC-2 passes for the wrong reason. A renamed key (`responsible`) was read correctly. Two more problems with that key, measured: a cross-repository id `ix://agent-ix/example-platform/COMP-001` is refused (`not a bundle artifact id`) when the bundle package is supplied, and a bare `COMP-001` is accepted rather than refused. FR-016 and quoin FR-171 both want the owner to name the responsible component, which is often in another repository. Rename the key and update quoin FR-171 and FR-173 to match, or route an engine change to quire-rs. Then state how a cross-repository owner resolves | spec/functional/FR-016-scope-exclusion-object.md:34, spec/functional/FR-016-scope-exclusion-object.md:46-47, spec/functional/FR-016-scope-exclusion-object.md:54, spec/functional/FR-004-role-schemas.md:76 |
| FND-007 | medium | FR-014-AC-5 says "A control with neither section validates". The manifest's `control.mappings` locator is `required: true`, and FR-014 does not change it. Measured: a control without `## Mappings` fails `[control] required 'mappings' (section_body(Mappings)) is missing`. FR-014 also adds `## Effectiveness` to the skeleton, but names no manifest locator for it. FR-005 Behavior forbids a skeleton section that the manifest does not assert, and FR-005-AC-6 tests that rule. State that the `Mappings` locator becomes `required: false` and that an `Effectiveness` locator is added | spec/functional/FR-014-control-mappings-are-clause-references.md:76, spec/functional/FR-014-control-mappings-are-clause-references.md:65, spec_objects_security/manifest.yaml:467-470, spec/functional/FR-005-executable-skeletons.md:86 |
| FND-008 | low | FR-014-AC-3 and AC-4, and FR-016-AC-4, verify through `quire extract`. In quire-cli 0.44.0 that command emits the body-extraction section text (`"mappings": "\| Set \| Clause \|..."`) and no semantic record. The Python `extract_semantic` takes no `mappings` token or data schema either. Only `validate_document` runs record-sections, and the only thing it exposes is the validation outcome. Name a surface that returns the record (the quire-rs FR-072 `declaration_record`), or restate these criteria as validation outcomes over valid and invalid values | spec/functional/FR-014-control-mappings-are-clause-references.md:74-75, spec/functional/FR-016-scope-exclusion-object.md:56 |

## Dispositions

Round 1, checked against fix commit f61e87f, with the PR head at aa90516.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | FR-016 now names the authored form (four `##` sections, one inline-code value each, no frontmatter keys) and the required `section_body` locators (Behavior, AC-6). The new FND-006 is a separate defect in that form. |
| FND-002 | fixed | FR-014 adds a scalar `## Effectiveness` section, read into `effectiveness` by record-sections, and the skeleton writes `not_assessed`. quoin#871 FR-173 at 5d1878c2 reads the extracted `effectiveness` key. Measured: `effective` validates, and `bogus` fails `semantic.record-invalid` at `effectiveness`. |
| FND-003 | fixed | FR-015-AC-2 (renumbered from FR-016) now names `semantic.invalid-model-cell` with reason `column-unknown` at the header, and a `mappings` key that is unavailable. Measured: a `Title` third column yields `semantic.invalid-model-cell ... header Title matches no property of the record key`. |
| FND-004 | fixed | FR-014-AC-2 adds `example.invalid/@1`, `/std@1`, `a/b/c@1` and `a/b@1@2`, and 64/65-byte boundaries for the parts and for `clause`. |
| FND-005 | fixed | The new FR-017 makes this module the home of `nist/sp800-53@5.2.0` and `owasp/asvs@5.0.0` in `clause_sets` (quire-rs FR-083), with truthful rights metadata and authoring owned by PLAT-1521 and PLAT-1522. quoin#871 FR-172 at 5d1878c2 uses the same keys. |
| FND-006 | still-open | Found in this pass, and no fix has landed: `owner` is a record-sections owned key (FR-075 systems member), so an authored `## Owner` is never read. |
| FND-007 | still-open | Found in this pass, and no fix has landed: the `control.mappings` locator is still `required: true`, and `## Effectiveness` has no locator. |
| FND-008 | still-open | Found in this pass, and no fix has landed: `quire extract` does not emit the semantic record that the criteria read. |
