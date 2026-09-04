---
id: SR-003
title: "EARS review of the #13 semantic module contract spec"
type: SpecReview
analysis: ears-conformance
scope: "spec/stakeholder/StR-001-module-activation.md, spec/functional/FR-001-module-manifest-activates.md, spec/functional/FR-002-emitted-json-schemas.md, spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/functional/FR-006-security-safe-declarations.md, spec/non-functional/NFR-001-additive-compatibility.md"
review_set: all
---
# SR-003: EARS review of the #13 semantic module contract spec

## Summary

Every SHALL-bearing statement of `agent-ix/spec-objects-security#13` was read
for EARS pattern, single `shall`, named subject and concrete response: the
StR-001 Stakeholder Need, the Description, Behavior and Constraints cells of
FR-001 through FR-006, and the NFR-001 Statement — 118 statements carrying 122
`SHALL` tokens — plus the 23 unmodalled rows of the FR-004 per-type table and
the 10 unmodalled rows of the FR-006 vocabulary table.

**How the count was taken.** `SHALL` tokens were counted per document and per
H2 section with `awk`, restricted to `## Description`, `## Behavior`,
`## Constraints`, `## Statement` and `## Stakeholder Need`; the totals are
StR-001 1, NFR-001 3, FR-001 3, FR-002 31, FR-003 18, FR-004 18, FR-005 24,
FR-006 24 = 122, and every `SHALL` in these eight documents falls inside a
scoped cell (no acceptance criterion, rationale or dependency line uses the
modal). Statements were then counted as units — one Markdown bullet, one
constraint-table row, or one sentence of a Description/Statement paragraph:
FR-002 1 + 25 + 5, FR-003 1 + 14 + 3, FR-004 1 + 15 (13 bullets and 2
sentences of the Behavior preamble) + 2, FR-005 1 + 20 + 3, FR-006 1 + 18 + 2,
FR-001 1 + 2, NFR-001 2, StR-001 1 = 118. The four-token gap is two
non-singular units: the FR-006 Description (one sentence, four `SHALL`) and the
second NFR-001 Statement sentence (two `SHALL`). The unmodalled rows were
counted by hand off the rendered tables: FR-004 lines 60–82, FR-006 lines
40–49.

**Tool result, verbatim.** `quire validate --scope <worktree> "spec/**/*.md"
--summary` and the same command with `--strict` both print exactly:

```
spec/tests.md: line 76: [TestMatrix] 'functional_coverage': table columns ["Functional Req", "Acceptance Criteria", "Test Cases", "Status"] do not match asserted columns ["Functional Req", "Acceptance Criteria", "Test Cases", "Coverage Status"] [assert]
25/25 docs grammar-clean (100%); 0 grammar finding(s): none
36/60 criteria property-extractable (60%); 0 candidate (metamorphic, needs review)
1 document(s) failed structural validation
```

Both runs exit 1. The single failure is a Test Matrix column assertion in
`spec/tests.md`, not a grammar finding; `--strict` escalates `[ears:*]`
warnings to failures and produced none, so the EARS grammar gate is clean in
both modes. Quire 0.31.0 (engine 0.46.0). The `DuplicateModuleName` and
`DuplicateArchetype` lines the run also prints are registry noise from the
worktree being discovered beside its parent checkout, and are not findings of
this lens.

Both governed tables are governed: FR-004's per-type table is introduced by
"Each model **SHALL** enforce its row of the following table" and FR-006's
vocabulary table by "The module **SHALL** emit these closed vocabularies, each
with exactly the members listed and no others", so the unmodalled-table defect
of the sibling business review (FND-223 there) does not recur here. Neither do
its two highs: FR-005 states the field-bearing and clause-bearing skeleton
sets by enumeration and FR-005-AC-4 matches them, and NFR-001 names its
measured population and the mechanism that makes the metric hold. What remains
is one contradiction between two normative encoding rules, a family of
obligations whose subject is not a component this module controls or is the
specification's own test suite, several normative cells occupied by
description, and criteria that restate their mechanism.

## Verdict

Grammar: **pass** — engine clean in both `--summary` and `--strict`, zero
`[ears:*]` findings over 25/25 documents. Semantics: **fail on one high**
(FND-240), a direct contradiction between FR-004's mandated schema encoding
and FR-006's prohibition of it, which two implementers would resolve
differently and which the implementation already resolves against FR-004 as
written. The eight mediums leave obligations unverifiable, unowned, or
verified by restating themselves; the lows are wording and subject choice.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-240 | high | FR-004 Behavior mandates the encoding "`@contains(IdentityField) @minContains(0) @maxContains(0)` for '0 identity fields', and … every further predicate on the same array as an `@extension("allOf", …)` clause whose `contains` references the marker file (`DefaultedField.json`, …)". FR-006 Behavior forbids exactly that: "The TypeSpec source SHALL encode every negative item rule as `items: { not: … }`" and "No schema of this module SHALL carry `minContains` or `maxContains`", with a stated inversion hazard as the reason. The two statements cannot both be satisfied, and FR-004-AC-9 (an audit-event record with an identity field fails) plus FR-006-AC-7 (no shipped schema uses `minContains`/`maxContains`) cannot both pass under FR-004's encoding. The implementation follows FR-006 — `AuditEvent.json` carries `allOf[].properties.fields.items.not.$ref` to `IdentityField.json` and `DefaultedField.json`, and no shipped schema contains either counting keyword — so FR-004's encoding bullet is the statement that is wrong, and it is the one an implementer reading FR-004 alone would build. Restate it as the positive rules only (`@contains` for "≥ 1"), and defer every negative rule to FR-006's `items`/`not` encoding | FR-004, FR-006 |
| FND-241 | medium | FR-006 places an item rule on `operations[].params[]` for the sensitive types that admit `operations` ("Each of those types that admits `operations` SHALL apply the same refusal to `operations[].params[]`", verified by FR-006-AC-4), but no row of the FR-004 per-type table carries it, while FR-004 states that table as the per-type contract each model SHALL enforce and seals the models against anything a row does not list. A reader building `Secret`, `EncryptionKey`, `MfaMethod` or `AuthFlow` from FR-004's row alone ships the fields-level refusal and misses the parameter-level one — which is the surface FR-006 says the guard exists for. Add the params rule to the four rows, or state in FR-004 that FR-006 contributes further item rules to named types | FR-004, FR-006 |
| FND-242 | medium | FR-005 "Only a criterion this specification names as blocked SHALL be exempt from the previous rule, as an explicit expected failure naming the blocking issue" resolves by position to the immediately preceding bullet, which forbids declaring `quire` in `pyproject.toml` — a rule a criterion cannot be exempt from. The intended referent is two bullets earlier ("If the installed Quire wheel is absent or lacks `extract_semantic`, then every semantic test SHALL fail — not skip"). Whether a criterion may be recorded as an expected failure instead of a hard failure is exactly what this sentence decides. Name the rule instead of ordering it | FR-005 |
| FND-243 | medium | FR-005 binds an enumerated obligation to a moving authority: "Every `Constraints` cell SHALL use only the constraint keywords the typed-table reader of the pinned Quire wheel accepts (`identity`, `min`, `max`, `exclusiveMin`, `exclusiveMax`, `minLength`, `maxLength`, `nonEmpty`, `unique`, and single-valued `enumValues`)", while FR-005 Inputs pins "The Quire wheel 0.46.0 **or later**". The admissible set is therefore both enumerated and delegated to an unbounded range of engine versions, and the two can diverge without any statement changing. Pin the wheel exactly (the Verification of NFR-001 and the `make dev-quire` bullet already speak of 0.46.0), or drop the parenthetical and let the reader be the authority — not both | FR-005 |
| FND-244 | medium | Obligations whose subject is the specification's own criteria and tests rather than a component of the system: FR-002 "No acceptance criterion, test, or fixture SHALL hard-code the version segment of the `$id` base" and, immediately after, "Each acceptance criterion, test, and fixture SHALL read the version segment of the `$id` base from the manifest `version`" — the same rule stated negatively and positively as two Behavior obligations; and FR-004 "The test suite SHALL verify every criterion over a key the extractor does not populate against a hand-built JSON record rather than an extracted one, naming that limitation in the test itself". These are verification-method rules; in a Behavior cell they are counted as system obligations and traced as if a build step enforced them. Move them to the Verification narrative or an NFR on the test suite, and state the version rule once | FR-002, FR-004 |
| FND-245 | medium | Process obligations on people, verifiable only by review, with no acceptance criterion of their own: FR-002 "If the manifest `version` changes, then the bump procedure SHALL be: edit … and commit … together; a commit that carries one half of the pair is refused by `make schemas-check`" (the response is a human editing sequence, and the enforceable half — the refusal — is stated without a modal); FR-003 "If Quoin or Quire rejects the manifest, then this module SHALL correct its own manifest or schemas rather than relax the contract keys, the digests, or the `$id` rules"; FR-006 "The module SHALL rewrite or remove a fixture that cannot satisfy a rule of this requirement" and "The module SHALL NOT relax a rule of this requirement to make a fixture pass". Restate each as the tool obligation that can fail a build (FR-002 already has it in `make schemas-check`), and move the maintainer rules to a constraint validated by Inspection or to an ADR | FR-002, FR-003, FR-006 |
| FND-246 | medium | NFR-001's criteria restate their mechanism rather than test the compatibility claim independently. The Verification states that no skeleton of the measured population carries a frontmatter `object:` key, so Quire never assembles or checks a typed record for it — under which NFR-001-AC-4 ("No skeleton of the checked-in 0.1.0 set yields a `semantic.record-invalid` finding under 0.2.0") cannot fail by construction, and AC-3's zero-error result follows from headings-only validation rather than from the schemas being additive. AC-1 and AC-2 compare the frozen baseline against the manifest, which is a diff, not a compatibility test. The document is honest about all of this and excludes the one population that can fail (corpus artifacts) in Scope; the finding is that the Statement's word "compatibility" is not what any criterion measures. Add a criterion over an artifact that does declare `object:` and is expected to keep validating, or restate the Statement as the diff and headings-only claim it actually verifies | NFR-001 |
| FND-247 | medium | Normative cells occupied by description rather than obligation. FR-003's Behavior carries a bullet with no modal at all — "Measured against quire 0.46.0: a refused schema drops that object type alone, while a manifest key the loader cannot parse … drops every object type of the module … Both refusals are silent …" — which is the sole statement of why half of FR-003-AC-6 is an expected failure; its `traceability` bullet then appends a cross-repository analysis of `control.allowed_links.mitigates` ending "That is a cross-repository decision and is out of scope here". FR-002's `$id`-base bullet argues a design decision and accepts its cost; FR-005's "While no committable index carries Quire 0.46.0 …" bullet closes out `agent-ix/spec-objects-security#10` and assigns blame. A Behavior bullet is read as one obligation; prose that states no obligation belongs in Rationale, and prose that states an engine limitation belongs in Dependencies | FR-002, FR-003, FR-005 |
| FND-248 | medium | FR-005 states its own gate as local: "The gate that runs this suite SHALL be the local `make test` and `make lint` targets … an automatic CI run would be red by construction until `agent-ix/quire-rs#392` lands". Every one of FR-005-AC-1 through AC-9 is nonetheless marked `Test` with no note that the evidence is produced by hand on a developer machine after `make dev-quire`, which is a different population of evidence from every other `Test` row in this spec. Mark the FR-005 rows as manual until `agent-ix/quire-rs#392` lands, so the matrix does not read as automated coverage | FR-005 |
| FND-249 | low | Obligations whose subject is a system this module does not build: FR-003 "The manifest SHALL install through `quoin module install path:<module dir>` with no `semantic.*` error diagnostic" and "When the install has completed, `quoin module` SHALL list `spec-objects-security`" are Quoin's behaviour; FR-001 "Re-activation SHALL be a no-op (idempotent by content hash per FR-026-AC-1)" is filament-core's, and takes a nominalised event as its subject; StR-001 "The Filament platform, its spec authors, and its agent CLI generators SHALL extract graph entities from security and identity specifications" places the doing on three consumers when the module's obligation is to make those entities extractable. Restate each as this module's obligation or as a stated contract check on a dependency. FR-001 and StR-001 pre-date this issue and are noted for completeness | FR-001, FR-003, StR-001 |
| FND-250 | low | Non-canonical state and condition keywords the engine lexicon does not flag: FR-003 "Where an object type gains a locator after 0.1.0, that locator SHALL be `required: false`" and "Until `agent-ix/quire-rs#394` names a digest mismatch, the module SHALL assert digest equality …"; FR-004 "Where a key is declared but the current extractor does not populate it … the key SHALL be optional"; FR-002 "When no `$id` or `$ref` is relative, the generator SHALL record the normalization as `applied: false`", which is the complement of the preceding `If … then` branch and not an event. Use `While …` for a state and `If … then …` for a condition; FR-005 already models the form with "While no committable index carries Quire 0.46.0, …" | FR-002, FR-003, FR-004, FR-005 |
| FND-251 | low | Unwanted-behaviour obligations stated as a ubiquitous subject-`SHALL` instead of `If … then … SHALL`: FR-006 "A value outside a vocabulary's member list SHALL fail validation", FR-004 "A record carrying a key its type's row does not list SHALL fail validation", FR-004-CON-2 "The empty record `{}` SHALL fail every one of the twenty-three types". The subject in each is the offending input rather than the schema that refuses it. FR-002 states seven of its own refusals as `If … then … SHALL` and FR-005 one; the inconsistency is within the same spec | FR-002, FR-004, FR-006 |
| FND-252 | low | Compound Descriptions the engine reads as one `SHALL`: FR-002 packs the emitter, the import, the pinned toolchain and the output directory into one obligation and puts the drift-check obligation in a trailing `so that` clause; FR-003 appends "while every existing extraction locator, edge vocabulary, and traceability rule keeps its meaning", a compatibility obligation restated in Behavior and owned by NFR-001; FR-005 appends "accompanied by negative fixtures that fail for a named reason", whose subject is not the skeleton; FR-006 packs four `SHALL` into one sentence. FR-001's Description additionally names the generic subject "The system" in a repository where that could be the module, the package or filament-core. Reduce each Description to one summary obligation and let Behavior atomise it | FR-001, FR-002, FR-003, FR-005, FR-006 |
| FND-253 | low | NFR-001's second Statement sentence packs two obligations ("SHALL keep every 0.1.0 `body_extraction` locator definition unchanged … and SHALL keep the `traceability` block, the `lexicon`, and every `allowed_links` and `roles` map equal to the frozen 0.1.0 baseline"), and the paragraph then carries three sentences of rationale — "Equality is asserted over the parsed structures, which is what a consumer reads; byte-for-byte identity of the file is neither asserted nor needed …" — inside the Statement cell. Split the obligation to match NFR-001-AC-1 and AC-2, which already separate them, and move the rationale to Rationale | NFR-001 |
| FND-254 | low | Redundant duals and uneven restatement in FR-004: "No model SHALL admit a key on a type whose row does not list it; the seal is the mechanism" and "A record carrying a key its type's row does not list SHALL fail validation" are one obligation stated from the schema side and the record side. The table's Item rules column then restates the seal for some types and not others — `role` says "`operations` forbidden", `permission` and `scope` say "`operations` and `relations` forbidden", `mfa_method` names neither although `relations` is equally absent from its Optional keys, and `asset` names none — so a reader cannot tell whether an unlisted key is forbidden by an item rule or only by omission. State the seal once and drop the per-row "forbidden" phrases, or carry them on every row | FR-004 |
| FND-255 | low | Version literals inside normative statements: FR-003 "The manifest `version` SHALL be `0.2.0`, because the emitted `$id` embeds it and the previous version was `0.1.0`", and NFR-001 names 0.1.0 and 0.2.0 throughout its Statement, Metrics and criteria. Every bump therefore falsifies a requirement statement and must edit it — which sits awkwardly beside FR-002's rule that no criterion, test or fixture hard-codes the version segment. State the obligation as "the manifest `version` SHALL be bumped when the `$id` base changes" (FR-002-CON-5 already carries the atomicity rule) and let 0.2.0 live in the manifest | FR-002, FR-003, NFR-001 |
| FND-256 | low | FR-006 "This module SHALL leave to the consumer's profile how `unknown` folds into a decision; the ticket admits both readings (fail closed, or remain explicitly unknown), and what this module guarantees is that `unknown` is stated rather than inferred and that no schema supplies it" attaches a modal to a deliberate non-obligation and cites "the ticket" as its authority. Nothing here can be verified, and the two things the sentence does guarantee are already obligations elsewhere in the same cell. State it as an exclusion in Scope, not as a `SHALL` | FR-006 |
| FND-257 | low | FR-002 constraint rows that mix obligation with description: CON-4 "`package-lock.json` SHALL resolve every public package from `registry.npmjs.org`; `@agent-ix/semantic-core` resolves from npm.ix until `agent-ix/filament-core-data#11` publishes it, so `make schemas`/`make schemas-check` run on a machine whose user-level npm config routes `@agent-ix` to npm.ix, not in the GitHub workflow" — the exception and the operating environment are stated as fact, and Inspection cannot check where a command was run; CON-1's second half "no custom emitter and no hand-edited emitted file" is an unmodalled fragment appended to the obligation; CON-3 "Emission SHALL be deterministic" names no actor (the generator emits). Split CON-4 into its obligation and a dependency note, give CON-1's second rule a modal, and name the generator in CON-3 | FR-002 |

## Result

| Check | Result |
|---|---|
| Explicit subject | Pass with notes (FND-244, FND-249, FND-251, FND-257) |
| Canonical trigger/state wording | Pass on the engine lexicon; four `Where …`/`Until …`/condition-as-`When` clauses noted (FND-250) |
| Atomic primary obligation | Fail in the FR-002/FR-003/FR-005/FR-006 Descriptions and the second NFR-001 Statement sentence (FND-252, FND-253); pass in Behavior bullets and Constraint cells |
| Modal consistency | Pass: both the FR-004 per-type table (23 rows) and the FR-006 vocabulary table (10 rows) are governed by an introducing `SHALL`; two unmodalled fragments noted (FND-245, FND-257) |
| Unwanted-behaviour response stated | Pass for the eight `If … then … SHALL` statements; three refusals stated as subject-`SHALL` (FND-251) |
| Normative vs descriptive cells | Fail: one FR-003 Behavior bullet carries no modal at all, three further bullets carry argument rather than obligation (FND-247) |
| Consistency between normative statements | Fail: FR-004 and FR-006 mandate incompatible schema encodings (FND-240); FR-006 adds an item rule absent from FR-004's per-type contract (FND-241) |
| Statement vs verification population | Fail (FND-244, FND-246, FND-248) |
| Tool grammar validation | Pass: 25/25 docs grammar-clean, 0 grammar findings, identical under `--strict` |

## Dispositions

| ID | Disposition |
|---|---|
| FND-240 | Decide the encoding once. The shipped schemas and `typespec/main.tsp` already implement FR-006's rule, so rewrite FR-004's encoding bullet to describe `@contains` for the positive "≥ 1" rules only and to cite FR-006 for every negative rule; FR-006-CON-2 and FR-006-AC-7 then own the prohibition without a competing statement |
| FND-241 | Add ", and `operations[].params[]` carries 0 defaulted fields" to the `secret`, `encryption_key`, `mfa_method` and `auth_flow` rows of the FR-004 table, or add a sentence to FR-004 Behavior stating that FR-006 contributes further item rules to the sensitive types and naming them |
| FND-242 | Replace "the previous rule" with the rule's content ("exempt from the fail-not-skip rule above") |
| FND-243 | Pin the wheel to 0.46.0 exactly in FR-005 Inputs, matching NFR-001's Verification and the `make dev-quire` bullet, and keep the enumerated keyword list as the normative set |
| FND-244 | Merge the two FR-002 version-segment bullets into one obligation and move it, with FR-004's hand-built-record rule, out of Behavior into the Verification narrative |
| FND-245 | Restate FR-002's bump procedure as the `make schemas-check` refusal (which is testable and already has FR-002-AC-8), and move the FR-003 and FR-006 maintainer rules to constraints validated by Inspection |
| FND-246 | Either add a criterion over an artifact that declares `object:` and is required to keep validating at 0.2.0, or narrow the NFR-001 Statement to the diff-and-headings claim the four metrics actually measure |
| FND-247 | Move the FR-003 "Measured against quire 0.46.0" bullet and the `mitigates` analysis to Rationale/Dependencies, and reduce the FR-002 `$id` and FR-005 `pyproject` bullets to their obligations with the argument carried below |
| FND-248 | Mark FR-005-AC-1..AC-9 as manually verified until `agent-ix/quire-rs#392` lands, and say so in tests.md rather than leaving them indistinguishable from CI-run rows |
| FND-249 | Restate the FR-003 Quoin bullets as contract checks on a dependency, FR-001's re-activation as the manifest's obligation, and StR-001's need as "the module SHALL make … extractable"; FR-001 and StR-001 may be deferred as pre-existing |
| FND-250 | Convert the four clauses to `While …` (states) and `If … then …` (conditions) |
| FND-251 | Restate the three refusals as `If a record carries …, then the schema SHALL reject it` |
| FND-252 | Reduce each Description to one summary obligation; the Behavior cells already atomise every clause named here |
| FND-253 | Split the second NFR-001 Statement sentence to match NFR-001-AC-1 and AC-2, and move the equality rationale to Rationale |
| FND-254 | State the seal once in FR-004 Behavior and drop the per-row "forbidden" phrases, or carry them on all 23 rows |
| FND-255 | Replace FR-003's literal with the bump obligation and let the manifest carry 0.2.0; leave NFR-001's version literals, which name a frozen baseline and are correct as literals |
| FND-256 | Move the `unknown`-folding sentence from FR-006 Behavior to Scope as a stated exclusion |
| FND-257 | Split FR-002-CON-4 into its obligation and a dependency note, give CON-1's second rule a modal, and name the generator in CON-3 |

### Round record (2026-09-04)

Applied in the review-fix round: FND-240 (the FR-004/FR-006 encoding contradiction, same defect as SR-002 FND-221), FND-241 (the operations-parameter refusal written into the FR-004 per-type contract), FND-242 (the positional "previous rule" replaced by a named one), FND-243 (the admissible constraint keywords bound to 0.46.0 rather than to "the pinned wheel").

Recorded without change, and carried into the report rather than silently closed: FND-244..FND-259.
