---
id: SR-009
title: "Security review of the #13 semantic module contract spec"
type: SpecReview
analysis: failure-domain
scope: "spec/functional/FR-006-security-safe-declarations.md, spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/functional/FR-003-semantic-manifest-contract.md, spec/spec.md, spec/tests.md, spec_objects_security/manifest.yaml, spec_objects_security/schemas/"
review_set: all
---
# SR-009: Security review of the #13 semantic module contract spec

## Summary

Security gate over the four merge-gate obligations of
`agent-ix/spec-objects-security#13`: security review before release, no schema
default granting permission/trust/effectiveness, secrets and credentials
referenced safely and never embedded in fixtures or provenance, and unknown or
unsupported security states failing closed. FR-006 is the requirement that
claims all four; FR-004 carries the item rules it leans on and FR-005 the
fixture rules. Grounded against the 49 emitted schemas under
`spec_objects_security/schemas/`, the 22 checked-in skeletons,
`@agent-ix/semantic-core` 0.1.0's emitted JSON Schema, `manifest.yaml`, and
the ticket text.

Two claims were checked by reading the artefacts rather than the prose and
both hold. No emitted schema of this module carries a JSON Schema `default`
keyword: the single `"default"` token in the schema tree is the property
*name* inside `DefaultedField.json`, which is the negative predicate itself.
All ten graded vocabularies are closed `enum`s over `type: string` with
exactly the members FR-006 tabulates and no open-string alternative, so a
value outside the list fails validation.

### The `default` refusal is defence-in-depth, not the primary gate

Stated plainly, because the requirement's weight rests on it: refusing
`FieldDecl.default` does not defend the Markdown path, because `default` is
not expressible on the Markdown path at all. semantic-core's
`ConstraintKeyword` is a closed eleven-member enum (`min`, `max`,
`exclusiveMin`, `exclusiveMax`, `pattern`, `minLength`, `maxLength`,
`enumValues`, `nonEmpty`, `unique`, `format`) with no `default`, and neither
authored form has a default slot — the typed table's columns are
`Field | Type | Multiplicity | Constraints` and the `sysml` fence is
`attribute <name> : <Type>[<mult>] { <constraints> }`. A `default:` cell is
therefore refused with `semantic.unknown-constraint-keyword` on *every* type,
guarded or not, and no extracted record can carry `FieldDecl.default` at all.
The closed keyword set is the primary gate; the schema rule is the second one.

FR-006 says this itself, in Behavior and in FR-006-AC-5, and that honesty is
the right call. What the spec does not draw is the consequence: because the
schema rule's only population is hand-built records, generated-language
fixtures and frontends, the two holes below are not edge cases in that
population — they are the whole of it. Nothing else validates against these
files.

## Verdict

**Not ready for release sign-off; ready for `spec-to-plan` once the two highs
are dispositioned.** Merge gate "no schema default grants permission, trust,
or control effectiveness" is substantively met at 0.2.0 and verifiable today.
Merge gate "secrets and credentials never embedded in fixtures or provenance"
is met for `fields` and for files in this repository, and is not met for
`operations[].params[]` (FND-160), for the free-text carriers (FND-164), or
for provenance, which no requirement owns (FND-163). Merge gate "unknown or
unsupported security states fail closed or remain explicitly unknown according
to profile" is met for the validation half and unowned for the interpretation
half: no profile concept exists anywhere in the spec, and "least-granting" is
true of two vocabularies out of ten (FND-162). Merge gate "security review is
required before release" has no owning artefact (FND-166).

FND-160 and FND-161 are the two that must move before this is a security
guarantee rather than a security intention. Both are failures of the same
kind — the negative predicate is placed where the material is not, or
expressed in a way that a conforming-enough consumer reads backwards.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-160 | high | The 0-defaulted-fields rule reaches `fields` only, never `operations[].params[]`, and `OperationDecl.params` items are `FieldDecl`s that admit `default` (whose `DefaultDecl.value` is unconstrained — any JSON, including a PEM block). `Secret`, `EncryptionKey` and `MfaMethod` all admit `operations`; `AuthFlow` *requires* it and its `fields` key — the only key its `allOf` guards — is optional and authored by no skeleton. The `auth_flow` skeleton's param tables are exactly the credential-bearing surface (`code`, `code_verifier`, `presented_token_locator`), so the one place a hand-built record would carry material is the one place the schema does not look | FR-006 Behavior ("SHALL admit 0 defaulted fields"), FR-004 table rows `secret`/`encryption_key`/`mfa_method`/`auth_flow`, `schemas/AuthFlow.json`, `schemas/Secret.json`, semantic-core `OperationDecl.json`, `skeletons/auth_flow.md` |
| FND-161 | high | Every negative predicate is emitted as `contains` + `minContains: 0` + `maxContains: 0`. A consumer validator that does not implement `minContains`/`maxContains` — draft-07 validators, and older 2020-12 implementations, which is precisely the "generated-language fixture, a frontend, a hand-built record" population FR-006 names as this rule's reason to exist — sees a bare `contains` and inverts the rule from "no defaulted field" into "must contain a defaulted field". `AuditEvent`'s 0-identity rule inverts the same way. No requirement pins the validator conformance level the guarantee depends on, and no criterion is a canary for it | FR-004 Behavior (`@minContains(0) @maxContains(0)`), `schemas/Secret.json`, `schemas/AuditEvent.json`, FR-006-AC-4, FR-002 |
| FND-162 | medium | "Each vocabulary SHALL make its unassessed member the least-granting state it can express" is true of two vocabularies. `ControlEffectiveness` folds unassessed into `not_assessed` and `TrustLevel` into `untrusted`; the other eight add an orthogonal `unknown` member whose relation to the scale is undeclared, so `ConfidentialityLevel.unknown` is not `restricted`, `SecretLifecycle.unknown` is not `compromised`, and `FindingStatus.unknown` is not `open`. FR-006-AC-6 tests exactly the two vocabularies that already hold and no other, and FR-006-CON-1 is verified by Inspection (TC-076, Static, P2) — the weakest method in the matrix for the module's central security claim. The ticket's "according to profile" names a profile concept that appears in no requirement, so no artefact says how a consumer must fold `unknown` | FR-006 Behavior, FR-006-AC-6, FR-006-CON-1, tests.md TC-075/TC-076, `schemas/ConfidentialityLevel.json`, `schemas/SecretLifecycle.json`, `schemas/FindingStatus.json` |
| FND-163 | medium | The merge gate reads "never embedded in fixtures **or provenance**". FR-005-AC-9 covers skeletons and negative fixtures; nothing covers provenance or evidence, no requirement mentions either word, and spec.md Out of Scope does not exclude them. The ticket's own Dependencies name "shared provenance/evidence" as a sequencing input, so the omission is silent rather than dispositioned | issue #13 acceptance criteria and dependencies, FR-005-AC-9, FR-005-CON-3, spec.md Out of Scope |
| FND-164 | medium | "No sensitive type SHALL admit a key whose value is the material itself" is not discharged for the free-text carriers every sensitive type admits: `FieldDecl.doc`, `ControlMapping.doc`, `FlowStep.doc`, and the clause bodies reached through `ClauseRef`. All are unconstrained strings, and the only credential-shaped-literal scan in the spec (FR-005-AC-9) runs over files in this repository — not over the hand-built and generated records the schema gate exists for | FR-006 Behavior, FR-005-AC-9, semantic-core `FieldDecl.json`, `schemas/ControlMapping.json`, `schemas/FlowStep.json` |
| FND-165 | medium | FR-006-AC-3 and TC-072 are written as "no shipped schema carries a JSON Schema `default` keyword at any depth", and the module's own `DefaultedField.json` falsifies that sentence under any recursive key scan: it carries `properties.default` and the string `"default"` in `required`. A test must distinguish keyword position from name position — see Dispositions for the exact rule. As written the criterion either fails on a correct tree or is quietly implemented as something other than what it says | FR-006-AC-3, tests.md TC-072, `schemas/DefaultedField.json`, semantic-core `FieldDecl.json` |
| FND-166 | medium | "Security review is required before release" is a merge gate with no owning artefact: no requirement, constraint, acceptance criterion or matrix row names a security review as a release condition, and no NFR-001 release/promotion step references one. This document exists only because it was commissioned | issue #13 safety/merge gate, NFR-001, tests.md |
| FND-167 | medium | The module's principal fail-open path is a schema that is never bound: `agent-ix/quire-rs#394` drops an object type with no diagnostic on a `data_schema` digest mismatch, and `#221` empties the model silently on an unknown manifest key. FR-003-AC-6 owns the refusal but is carried as an explicit expected failure, so for a `security_critical: true` module the interim posture is "every rule in FR-006 may be silently inactive". No requirement states that posture, and FR-001-AC-4 asserts archetype/object-type rows, not `data_schema` binding | spec.md Out of Scope, FR-003-AC-6, FR-001-AC-4, `manifest.yaml` `data_schema` digests |
| FND-168 | low | `material_ref`, `issuer`, `binds` and `custodian` are optional on every sensitive type and are populated by no extractor today, so "referenced safely" is an admitted capability rather than an obligation: no criterion requires a secret or key declaration to name where its material lives. The `secret` skeleton carries a `locator` row, which is an ordinary `FieldDecl`, not the typed key | FR-006 Behavior, FR-004 table, `skeletons/secret.md`, spec.md Out of Scope (extraction owned by `agent-ix/quoin#335`) |
| FND-169 | low | `Severity`, `Likelihood` and `Impact` place `unknown` after `critical`, `almost_certain` and `severe`, so a consumer ranking members by enum index reads unassessed as the top of the scale for those three and near the bottom for others. The enums declare no ordering and the spec says nothing about whether one may be inferred | `schemas/Severity.json`, `schemas/Likelihood.json`, `schemas/Impact.json`, FR-006 Behavior |
| FND-170 | low | FR-006-AC-4's "the same record without it validates" is schema evidence over a hand-built record, correctly labelled in FR-006 and FR-004. Worth stating once in tests.md beside TC-073 as well, so the matrix reader does not read a P0 Integration row as extraction evidence | FR-006 Behavior, FR-004 Behavior, tests.md TC-073 |

## Dispositions

| ID | Disposition |
|----|-------------|
| FND-160 | Extend the rule to the nested surface: add "0 defaulted params" to the `secret`, `encryption_key`, `mfa_method` and `auth_flow` rows of the FR-004 table, expressed as a marker model over `operations` (a `DefaultedParamsOperation` whose `params` contains a `DefaultedField`) with the same `@contains @minContains(0) @maxContains(0)` shape, and extend FR-006-AC-4 to a record whose defaulted field sits in `operations[0].params[0]`. If the nesting is judged out of reach of the emitter, say so in FR-006 Behavior and name the ticket — do not leave the sentence reading as though `fields` were the whole surface |
| FND-161 | Add an FR-006 constraint that the guarantee is stated against a JSON Schema 2020-12 validator implementing `minContains`/`maxContains`, and an acceptance criterion that is a canary: a record whose only defaulted field would satisfy a bare `contains` must fail, and the test must assert the failure reason rather than the boolean, so a validator that silently ignores `maxContains` is caught rather than reported green. State in FR-002 or FR-006 that consumers on a lower draft get no guarantee from these files |
| FND-162 | Separate the two halves the sentence conflates. Keep the validation half (an out-of-vocabulary value fails) as it stands. For the interpretation half, either (a) define the profile the ticket names — one paragraph in FR-006 stating, per vocabulary, the member a consumer must treat an absent or `unknown` grade as, with `restricted`, `compromised` and `open` as the named collapses — or (b) state explicitly that this module declares vocabulary only and that folding is the consumer's obligation, and drop the "least-granting" sentence to the two vocabularies it is true of. Either way widen FR-006-AC-6 past `ControlEffectiveness` and `TrustLevel`, and raise TC-076 above a P2 Static row |
| FND-163 | Either add a requirement sentence and criterion covering provenance and evidence records — the same credential-shaped-literal refusal FR-005-AC-9 applies to skeletons — or add provenance to spec.md Out of Scope naming the owning ticket. The gate names it; the spec must answer it one way or the other |
| FND-164 | Add to FR-006 that the credential-shaped-literal refusal applies to every free-text carrier a sensitive type admits (`doc` on `FieldDecl`, `ControlMapping` and `FlowStep`, and clause bodies), and extend the FR-005-AC-9 pattern set into a shared check the record-level tests of FR-006 also run, so the rule holds for hand-built records and not only for files in this repository |
| FND-165 | Restate FR-006-AC-3 and TC-072 as a JSON-Schema-aware walk and say the discriminator in the criterion itself: starting at each schema object, flag the key `default` only when it appears in *schema position* — that is, as a keyword of a schema object — and never descend into the *keys* of `properties`, `$defs`, `patternProperties` or `dependentSchemas` (descend into their values, which are schemas), never treat a string member of `required`, `enum` or `const` as a keyword, and skip subtrees under `enum` and `const` entirely. Under that rule `DefaultedField.json` is clean and the criterion is true of the current tree, which is the outcome the requirement wants. Name `DefaultedField.json` in the test as the case that proves the discriminator works |
| FND-166 | Add the security review to NFR-001 (or to a release section of spec.md) as a named release condition with this document's id, and add a matrix row for it, so the gate is discharged by an artefact rather than by a commission |
| FND-167 | State the interim posture in spec.md Out of Scope beside the `#394`/`#221` entry: while the digest-mismatch and unknown-key diagnostics are absent, the module's security rules are enforced only where the schemas are demonstrably bound, and the module is advisory-only until promotion for that reason. Add an FR-001 or FR-003 criterion asserting all twenty-three types are bound with their schemas after activation — a count assertion, which `#394` does not block |
| FND-168 | Either state in FR-006 that naming the locator is an obligation the day `agent-ix/quoin#335` publishes the mapping, with an FR-004 item rule over `fields` requiring a `material_ref` row today (the same device FR-004 already uses for the eight graded keys), or record deliberately that the module admits a secret declaration naming no locator, and why |
| FND-169 | Either declare the graded enums unordered — one sentence in FR-006, since three of them place `unknown` at the high end — or order each vocabulary so the array index is meaningful and say that consumers may rely on it |
| FND-170 | Add the "schema evidence, not extraction evidence" note to the TC-073 row of tests.md, matching the sentence already carried at tests.md line 182 |

### Round record (2026-09-04)

Applied in the review-fix round: FND-160 (the defaulted-field refusal extended to `operations[].params[]` on every guarded type that admits operations, in the schemas and in FR-004/FR-006), FND-161 (every negative predicate re-encoded as `items`/`not`; no shipped schema carries `minContains` or `maxContains`, and FR-006-AC-7 with TC-076 asserts it), FND-162 (the least-granting claim narrowed to the two ordered vocabularies, with the other eight stated as unordered), FND-163 and FND-164 (the free-text carriers allocated to the FR-005 credential-shape scan, since no schema can forbid a string), FND-165 (FR-006-AC-3 rewritten around schema position, and TC-072 names `DefaultedField.json` as the case that proves the discriminator), FND-166 (FR-006-AC-8), FND-167 (FR-003 states the interim posture for `quire-rs#394`).

Recorded without change, and carried into the report rather than silently closed: FND-168, FND-169, FND-170.
