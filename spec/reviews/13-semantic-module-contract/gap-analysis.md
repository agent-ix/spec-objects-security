---
id: SR-011
title: "Gap analysis of the #13 semantic module contract branch"
type: SpecReview
analysis: gap-analysis
scope: "plan/Plan-001-semantic-module-contract/, spec/tests.md, spec/functional/FR-001-module-manifest-activates.md, spec/functional/FR-002-emitted-json-schemas.md, spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/functional/FR-006-security-safe-declarations.md, spec/non-functional/NFR-001-additive-compatibility.md, spec/stakeholder/StR-001-module-activation.md, spec/usecase/US-001-declare-security-objects-against-semantic-core.md, spec/integration/IT-001-manifest-activation-roundtrip.md, spec/integration/IT-002-quoin-module-install.md, typespec/main.tsp, scripts/generate-schemas.mjs, scripts/stage-npm.mjs, tests/, spec_objects_security/manifest.yaml, spec_objects_security/schemas/"
review_set: all
---
# SR-011: Gap analysis of the #13 semantic module contract branch

## Summary

Post-implementation verification gate over `spec/13-semantic-module-contract`
against `origin/main`, delivering `agent-ix/spec-objects-security#13`. Every
claim below was taken from a run rather than from prose: `make test`, `make
lint` (which runs `node scripts/generate-schemas.mjs --check`), `quire coverage
--scope . --json` at quire 0.31.0 / engine 0.46.0, and direct measurement over
the 47 emitted schemas, the 26 skeleton files, the 23 baseline fixtures and the
81 candidate test symbols.

**What holds.** `make lint` is clean and the drift gate reports 47 schemas
matching the committed output. `make test` reports 211 passed, 2 xfailed, 0
skipped over 213 collected — the zero-skip claim of
`agent-ix/spec-objects-security#10` is genuinely discharged, and the suite fails
rather than skips when the engine is absent. All 23 object types carry a
distinct, sealed, non-placeholder schema: measured over `required`,
`properties` and `allOf`, the 23 signatures are 23 distinct values and none is
`type: object` only. No emitted schema carries a JSON Schema `default` keyword
at any depth. All ten graded vocabularies are closed `enum`s. The tree is
clean; no dangling uncommitted work.

**What does not.** Two things are wrong rather than merely unfinished. First,
`TC-110` — owned by the blocked Task-009, marked `🚧` in the matrix — is counted
**backed** by `quire coverage`, because a precondition-only test carries its
tracking tag. The 131/145 headline the branch publishes therefore includes one
row whose evidence does not exist. Second, `spec/tests.md`'s own reconciliation
of that headline enumerates fifteen targets as "the 14 it cannot back" and its
Coverage Gaps section says "seven rows" while naming nine. The numbers, the
enumeration and the engine disagree three ways.

Everything else found is an honestly-declared incompleteness (Task-009,
Task-010 and the eight rows needing a running `filament-core-service`, a Quoin
from `quoin` main, or a generator run), a small census defect in a sibling
review, or an unowned behaviour in `scripts/stage-npm.mjs`.

### Coverage reconciliation, and what each number counts

`quire coverage --scope .` reports **131/145 rows backed (90%)**, which matches
`spec/tests.md`'s claim exactly. The **145** are trace targets minted from
`spec/`: 85 `## Test Case Summary` rows, 53 FR acceptance criteria and
constraints, 4 NFR acceptance criteria and 3 StR validation criteria. `IT-001`
and `IT-002` mint nothing, so `IT-001-AC-1..2` and `IT-002-SC-01..06` are
outside the measured population. "Backed" means at least one source symbol
outside `spec/` carries a matching tracking tag; it is not a test count and
says nothing about whether the tagged test asserts the row.

The **14 unbacked** are `FR-001-AC-2`, `FR-001-AC-3`, `FR-001-AC-4`,
`FR-003-AC-5`, `StR-001-VC-1`, `StR-001-VC-2`, `TC-015`, `TC-016`, `TC-017`,
`TC-018`, `TC-019`, `TC-046`, `TC-112`, `TC-113`. `TC-110` is **not** among
them, contrary to what `spec/tests.md` states.

`make test` reports **211 passed, 2 xfailed, 0 skipped** over 213 collected.
That counts pytest test functions under `tests/`, not matrix rows. Of 81
candidate symbols the engine sees, 79 are tagged and bound (97%); the two
untagged ones are in `tests/test_additive_compatibility.py`. Both xfails are
`strict=True` — the legacy `object:` form (`agent-ix/quire-rs#391`) and the
`TC-045` refusal-naming half (`agent-ix/quire-rs#221`, `#394`).

The two numbers are unrelated populations and neither is a substitute for the
other: 131/145 measures whether spec targets have tags; 211/213 measures
whether tagged code runs green.

### Ticket acceptance criteria, one verdict each

- **Every security object type has a reviewed non-placeholder schema — MET.**
  23 object types, 23 schema files, 23 distinct structural signatures, every one
  sealed with `unevaluatedProperties: {not: {}}` and carrying type-specific
  `required` keys or item rules. Reviewed by the eight-document review set,
  `security.md` (SR-009) in particular — whose object counts are themselves
  wrong (FND-338), which does not unmake the review.
- **Secrets and credentials referenced safely, never embedded in fixtures or
  provenance — MET IN SUBSTANCE, PARTIALLY GATED.** `Secret`, `EncryptionKey`,
  `JwtClaim` and `CsrfToken` carry `material_ref` as a `SemanticId` reference
  and refuse a `DefaultedField` both in `fields` and in `operations[].params`
  via `items`/`not`. A credential-shape census over the populations `TC-088`
  does *not* scan — the 23 baseline fixtures, the 47 schemas, both manifests
  and all of `tests/` — returned 9 matches, every one a lexicon term name
  (`token:`, `secret:`) or a Python identifier, and no credential material. The
  criterion holds; the "or provenance" half is not gated (FND-337).
- **Unknown or unsupported security states fail closed or remain explicitly
  unknown according to profile — MET.** Ten closed `enum`s over `type: string`
  with no open-string alternative; eight carry an explicit `unknown` member;
  the two where "unknown" must not read as permissive resolve the other way —
  `ControlEffectiveness` starts at `not_assessed` and `TrustLevel` at
  `untrusted`. No `default` keyword at any depth (the single `default` token in
  the tree is the *property name* inside `DefaultedField.json`, the negative
  predicate itself), and `minContains`/`maxContains` appear nowhere, so no
  negative rule can invert on a validator that skips them.
- **Existing #6 and #10 findings have recorded dispositions — PARTIALLY MET.**
  Both dispositions exist and are substantive: `#6` is fixed (both flow
  mappings quoted) and guarded structurally by `tests/test_manifest.py`, which
  asserts the *form* rather than the two terms; `#10` is disposed in FR-005
  Behavior and `spec/tests.md` Test Environment and discharged by 0 skips. But
  both issues are OPEN with zero comments, so nothing outside this branch
  records either disposition, and `#6`'s restored lexicon wording — which its
  finder deferred for sign-off — carries no recorded approval (FND-339).

## Verdict

**FAIL.**

Two `high` findings, two `blocked` plan tasks with four unchecked subtasks, and
eight matrix Test Cases with no backing tagged test. By the gate's rule any one
of those is a FAIL, and the verdict should be read for what it is: this is a
statement that Plan-001 is not complete and cannot be closed, not an accusation
that the branch misreports itself. Most of the incompleteness is declared
honestly on the row, with a named external blocker.

The part that is *not* honest reporting is FND-330: a blocked task's row is
counted as backed by the very tool the gate relies on, so the published
131/145 overstates real backing by one row, and FND-332/FND-333, where
`spec/tests.md`'s own arithmetic contradicts itself. Those are the findings that
must close before the number is quoted anywhere else.

The work itself is in good shape. Fix FND-330 by untagging or retitling the
precondition test, correct the three arithmetic statements, re-tick the plan
summary, and the remaining gate is entirely the external environments
Task-009 and Task-010 name.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-330 | high | `TC-110` is owned by the blocked Task-009 and marked `🚧`, yet `quire coverage` counts it **backed**: `tests/test_quoin_install_roundtrip.py::test_the_module_directory_quoin_would_install_is_complete` carries `@pytest.mark.trace("TC-110", "IT-002-SC-01")` while asserting only that the module directory is complete — no `quoin module` listing is recorded, no install is run, no state is restored. The 131/145 headline therefore includes one row whose evidence does not exist, and `IT-002-SC-01` ("the listing is captured, including any existing `spec-objects-security` entry") is tagged by a test that captures no listing. Something Task-009 owns *is* reported as backed | tests/test_quoin_install_roundtrip.py, spec/tests.md:188, IT-002-SC-01, Task-009 |
| FND-331 | high | Plan-001 is not complete: Task-009 and Task-010 are `status: blocked` with four unchecked subtasks between them, and eight matrix Test Cases (`TC-015`..`TC-019`, `TC-046`, `TC-112`, `TC-113`) plus six criteria (`FR-001-AC-2..4`, `FR-003-AC-5`, `StR-001-VC-1`, `StR-001-VC-2`) have no backing tagged test anywhere. The blockers are external and named on every row — a running `filament-core-service`, a Quoin built from `quoin` main at or after `3e842ce`, a `minijinja-cli` generator run — so this is a completion gap, not a reporting gap; the plan cannot be closed on it | Plan-001, Task-009, Task-010, spec/tests.md |
| FND-332 | medium | `spec/tests.md` Overview states "The 14 it cannot back are exactly the rows below that read `🚧`: TC-015..TC-019, TC-046, TC-110, TC-112 and TC-113, and the criteria they carry (FR-001-AC-2..4, FR-003-AC-5, StR-001-VC-1..2)" — that enumerates fifteen targets, not fourteen, and includes `TC-110`, which the engine counts as backed. The number and its own enumeration cannot both be right | spec/tests.md Overview, FND-330 |
| FND-333 | medium | `spec/tests.md` Coverage Gaps says "Seven rows cannot be discharged in this repository and are `🚧` with the reason on the row" and then names nine: `TC-015`, `TC-016`, `TC-017`, `TC-018`, `TC-019`, `TC-046`, `TC-110`, `TC-112`, `TC-113` | spec/tests.md Coverage Gaps |
| FND-334 | medium | Every one of the twelve requirement checkboxes in `plan.md`'s Requirements Summary is unchecked — `StR-001`, `US-001`, `FR-001`..`FR-006`, `NFR-001`, `IT-001`, `IT-002` — although Task-000 through Task-008 are all `status: done` and FR-002..FR-006 and NFR-001 are fully backed at 100% each. The plan reports itself at zero against its own summary, so the summary is worthless as a completion signal and a genuinely-unfinished requirement would be indistinguishable | plan/Plan-001-semantic-module-contract/plan.md:35-53 |
| FND-335 | medium | Underspecified code: `scripts/stage-npm.mjs` reads `GITHUB_REF_NAME`, matches `v?X.Y.Z`, and rewrites `package.json`'s `version` when it differs. FR-002 Inputs names the script and FR-002 Behavior owns exactly two of its obligations (copy the payload at pack time, remove the staged copies on `postpack`); no requirement, acceptance criterion or TC row owns the version stamping. It is precisely the skew `FND-230` describes — tagging `v0.3.0` publishes `@agent-ix/spec-objects-security@0.3.0` whose every `$id` still reads `…/0.2.0/…` — implemented in code that no obligation governs | scripts/stage-npm.mjs, FR-002 Behavior, FR-002-CON-5, FND-230 |
| FND-336 | medium | `tests/test_additive_compatibility.py::test_a_legacy_form_declaring_object_is_not_an_error` is a `strict=True` xfail carrying **no** trace tag, though `TC-103`'s status cell asserts its existence ("the `object:`-declaring case is an expected failure"). The matrix's claim about the expected failure is prose only: delete the test and no coverage row moves | tests/test_additive_compatibility.py, spec/tests.md TC-103, NFR-001-AC-4 |
| FND-337 | medium | Ticket AC-2's "or provenance" half is ungated. `TC-088` scans `spec_objects_security/skeletons/*.md` and `tests/fixtures/negative/*.md` only — not the 23 baseline fixtures under `tests/fixtures/baseline-0.1.0/`, not the 47 emitted schemas, not `manifest.yaml` or `toolchain.json`, not `tests/`. A census over those populations with the same six patterns returns 9 matches, all lexicon term names or Python identifiers and no credential material, so the criterion holds today; nothing keeps it holding | tests/test_skeletons_semantic.py:264, FR-005-AC-9, FR-005-CON-3, issue #13 AC-2 |
| FND-338 | medium | `security.md` (SR-009) Summary states it was grounded against "the 49 emitted schemas under `spec_objects_security/schemas/`" and "the 22 checked-in skeletons". Measured: 47 emitted schemas plus `toolchain.json` (48 files), which `toolchain.json` itself lists as 47 and `make lint` confirms as 47; 26 skeleton files (23 primary plus 3 `sysml` alternates) and 23 baseline fixtures. Neither figure matches any population in the tree | spec/reviews/13-semantic-module-contract/security.md:11-30 |
| FND-339 | medium | Ticket AC-4's dispositions exist only inside this branch. `agent-ix/spec-objects-security#6` and `#10` are both OPEN with zero comments, so a reader of either ticket sees no disposition; and `#6` explicitly deferred the restored lexicon wording for sign-off ("lexicon vocabulary changes are sweep-and-report, so the restored wording needs sign-off"), which the branch supplies with no recorded approval | issue #6, issue #10, spec_objects_security/manifest.yaml lexicon, tests/test_manifest.py:152 |
| FND-340 | medium | `IT-001-AC-1`, `IT-001-AC-2` and `IT-002-SC-01`..`IT-002-SC-06` mint no coverage target: the engine's 145 decompose as 85 test-case rows, 53 FR criteria/constraints, 4 NFR criteria and 3 StR validation criteria, and IT documents contribute nothing. Eight integration success criteria therefore sit outside the measured population entirely and are visible only through the `🚧` TC rows that reference them, so an IT criterion silently losing its row would not move the headline | spec/integration/IT-001, spec/integration/IT-002, quire coverage minted_targets |
| FND-341 | medium | The `make test` coverage gate enforces 100% over 4 statements — the whole of `spec_objects_security/__init__.py`. Neither `scripts/generate-schemas.mjs` (319 lines, the drift gate and normalizer) nor `scripts/stage-npm.mjs` is under any coverage measurement, so `log.md`'s "coverage 100%" states nothing about the code this change adds | pyproject.toml, plan/Plan-001-semantic-module-contract/log.md |
| FND-342 | medium | `quire coverage` reports `status-column-matches-nothing` on the Functional Requirement Coverage table: `traceability.status.column` names `Status` while the archetype asserts the header `Coverage Status`, so status classification is skipped for that table and a row marked `✅` while unbacked cannot be caught there. `spec/tests.md` declares this and routes it to `agent-ix/spec-artifacts-process#81`/`#82`; recorded here because it is live on this branch and it is the exact check FND-330 needed | spec/tests.md Coverage Gaps, quire coverage diagnostics |
| FND-343 | low | Underspecified code: `tests/test_additive_compatibility.py::test_the_frozen_baseline_is_the_previous_module_version` — the guard that Task-000's frozen baseline really is 0.1.0 with 23 skeletons and the same 23 object types — carries no trace tag and no matrix row, though its docstring states it is a deliverable ("without it every NFR-001 criterion compares the manifest against itself") | tests/test_additive_compatibility.py:32, Task-000 |
| FND-344 | low | The ticket's Deliverables list "generated-language fixtures", and none is produced. The plan declares the omission deliberately against `agent-ix/filament-core-data#19`/`#21`/`#22`/`#23` and `agent-ix/quoin#290` ("none is produced or faked here"), but no requirement, criterion or matrix row records it; `StR-001-VC-2` is its only proxy and is unbacked | issue #13 Deliverables, plan.md external dependencies, StR-001-VC-2 |
| FND-345 | low | The ticket's safety gate "Advisory-only until promotion" is expressed only as `semantic.legacy_forms: warning` in the manifest, asserted by `TC-040` as one of nine admitted key/value pairs. No requirement states the advisory-only posture as an obligation and no test asserts that promotion is gated, so the gate is met by coincidence of a key's value | issue #13 safety gate, FR-003-AC-1, TC-040 |
| FND-346 | low | `TC-005` and `TC-045` are each carried by two symbols (`shared_trace_ids`): `test_manifest_validates_against_fr035_schema` + `test_the_pinned_schema_differs_from_the_release_only_where_admitted`, and `test_an_unknown_key_and_an_altered_digest_are_refused` + `test_the_refusal_names_the_offending_key_or_path`. Benign and deliberate — the second of each pair is the pin delta and the strict-xfail naming half — but a row that stays backed when half its evidence is deleted is worth a matrix row each | quire coverage shared_trace_ids, spec/tests.md TC-005, TC-045 |
| FND-347 | low | `log.md` records that the plan bundle was authored alongside the implementation rather than before it, against the governed spec → matrix → review → plan → implementation order, so each done task's Subtasks section is a record rather than an instruction. Recorded honestly by the author; carried here so the process deviation survives the plan's closure rather than living only in a log entry | plan/Plan-001-semantic-module-contract/log.md |
| FND-348 | low | Overspecification census: six criteria — `FR-001-AC-2`, `FR-001-AC-3`, `FR-001-AC-4`, `FR-003-AC-5`, `StR-001-VC-1`, `StR-001-VC-2` — and both IT documents in full have no implementation anywhere in this repository. Every one is honestly marked and blocker-named, and `FR-001-AC-2..4` predate this ticket; recorded as the census result so the branch's overspecified surface is a stated number rather than an inference | FR-001, FR-003-AC-5, StR-001, IT-001, IT-002 |
| FND-349 | low | Underspecified-code census result, recorded so it is on the record rather than implied: `typespec/main.tsp` declares 10 enums, 14 support models and 23 object models (47, matching `toolchain.json`), every one owned by FR-004 or FR-006 including the `@contains` / `@extension("allOf", …)` encoding FR-004 Behavior specifies explicitly; every function in `scripts/generate-schemas.mjs` traces to an FR-002 Behavior bullet; 79 of 81 test symbols are tagged. The only unowned behaviours found in the whole change are FND-335 and FND-343 | typespec/main.tsp, scripts/generate-schemas.mjs, tests/ |

## Dispositions

| Finding | Disposition |
|---|---|
| FND-330 | Blocking. Either drop the `TC-110` and `IT-002-SC-01` tags from `test_the_module_directory_quoin_would_install_is_complete` and let the row read unbacked as its `🚧` status says, or mint a distinct row (e.g. `TC-109`, "the module directory Quoin would install is complete and self-consistent") for what the test actually asserts and leave `TC-110` untagged. Do not resolve it by widening `TC-110`'s title: the row's evidence is the install roundtrip, and Task-009 is blocked on it. Re-run `quire coverage` afterwards; the headline becomes 130/145 |
| FND-331 | Accepted as the completion state, not a defect to fix here. Task-009 and Task-010 stay `blocked` and Plan-001 stays `active`; close them only when `agent-ix/quire-rs#392`, a Quoin from `quoin` main at or after `3e842ce`, and a running `filament-core-service` are available. The eight rows keep their `🚧` and their named blocker |
| FND-332 | Blocking with FND-330. Restate the sentence from the engine's own list once FND-330 lands: fourteen targets, `TC-110` excluded if it is untagged and included in the backed count if the row is split |
| FND-333 | Correct "Seven" to the count actually enumerated in the same sentence. Free-standing; fix with FND-332 in one edit to `spec/tests.md` |
| FND-334 | Tick the eleven requirement boxes Task-000..Task-008 discharge and leave `IT-001` and `IT-002` unticked, or delete the checkbox form from the Requirements Summary and let each task's `status` be the single completion signal. Either is acceptable; a summary that reads zero while nine of eleven tracks are done is not |
| FND-335 | Owner's call, and it needs one before the next tag. Preferred: add the tag to FR-002's bump procedure as FND-230 asks, add an FR-002 Behavior bullet owning the `GITHUB_REF_NAME` stamping, and an acceptance criterion that a tag disagreeing with the manifest `version` fails rather than publishes. Minimum: delete the stamping and let the release workflow own the version, so no unspecified code can skew the pair |
| FND-336 | Add `@pytest.mark.trace("TC-103", "NFR-001-AC-4")` to the strict xfail, so `TC-103`'s claim about the expected failure is carried by a tag rather than by its status cell |
| FND-337 | Widen `TC-088`'s population to the baseline fixtures, the emitted schemas, both manifests and `toolchain.json`. The census run for this review shows the widened scan passes today, so this is a gate extension with no expected fallout, not a new finding surface |
| FND-338 | Correct the two counts in `security.md`'s Summary to 47 emitted schemas and the skeleton population it actually read. The review's conclusions are unaffected — both were checked against the tree here and hold — but a review that states a wrong census cannot be re-run against its own numbers |
| FND-339 | Comment the disposition onto `agent-ix/spec-objects-security#6` and `#10` and close them, quoting the branch's evidence (the structural lexicon assertion; 0 skips at 211 passed). Hold `#6`'s close until Peter signs off the two restored definitions, per the sweep-and-report rule the ticket itself invokes |
| FND-340 | Spec-side, not fixable in the matrix. Either the IT archetype should mint its per-step criteria as trace targets — an upstream ask against `spec-artifacts-process` — or FR-003 and FR-001 should carry the criteria the IT steps assert. Record the choice; until then the eight criteria are covered only through their `🚧` TC rows |
| FND-341 | Restate the claim rather than raise the gate. Replace "coverage 100%" in `log.md` with what it measures (4 statements of the package `__init__`), and if a real gate is wanted over the two Node scripts, that is its own ticket — this branch should not grow one |
| FND-342 | Already disposed by `spec/tests.md` to `agent-ix/spec-artifacts-process#81`/`#82` and left as-is here, correctly: renaming the column locally fails structural validation. Carried in this review because FND-330 is exactly the class of defect the skipped classification would have caught, which raises the priority of the upstream fix |
| FND-343 | Add a matrix row for the baseline guard under NFR-001 (it is Task-000's deliverable and NFR-001's precondition) and tag the test to it, or state in Task-000 that the guard is deliberately untraced. Either way the choice should be recorded |
| FND-344 | No action on this branch — the plan's declaration is correct and the fixtures genuinely belong upstream. Record the omission on the ticket when it is closed, so `#13` is not read as having delivered its full Deliverables list |
| FND-345 | Add an FR-003 Behavior bullet stating the advisory-only posture as an obligation, so `legacy_forms: warning` is the implementation of a stated rule rather than the rule itself. Low priority; the value is correct today |
| FND-346 | Accepted as-is. Optionally split each pair into its own matrix row so neither half can be deleted silently. No change required for this gate |
| FND-347 | Accepted and recorded. No remediation — the deviation is already logged by the author, and this entry exists so it survives the plan bundle's closure |
| FND-348 | Accepted. This is the census, not a defect: every one of the six is honestly marked with a named external blocker, and FND-331 owns their completion. No spec should be deleted to make the number smaller |
| FND-349 | Accepted. No action beyond FND-335 and FND-343, which are the census's only two hits |

### Round record (2026-09-04)

Applied in the fix round: FND-330 and FND-332 (TC-110 was counted backed by a test that performs no install; split into TC-114, and the headline corrected from 131/145 to 131/146 with TC-110 unbacked), FND-333 (the Coverage Gaps count corrected from seven to nine, and every named row listed), FND-334 (the plan's Requirements Summary now distinguishes delivered from partly delivered), FND-335 (FR-002 now owns the `GITHUB_REF_NAME` version stamping, and states why the npm package version is deliberately independent of the manifest version the `$id` embeds), FND-336 (the strict xfail now carries its marker), FND-338 (the two miscounts in SR-009 corrected in place), FND-339 (dispositions posted as comments on issues #6 and #10), FND-341 (the matrix and the plan log now say the 100% is four statements of `__init__.py` and is not evidence about this change).

Recorded without change, and carried into the report rather than silently closed: FND-331 and FND-337 (the two blocked tasks and the provenance half of the credential gate: both need an environment or a decision this ticket does not own, and both are named on the rows they affect), FND-340, FND-342 (upstream), FND-343..FND-349.
