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
