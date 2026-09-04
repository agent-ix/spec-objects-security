---
id: SR-004
title: "Evidence review of the #13 semantic module contract spec set"
type: SpecReview
analysis: evidence
scope: "spec/functional/FR-001-module-manifest-activates.md, spec/functional/FR-002-emitted-json-schemas.md, spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/functional/FR-006-security-safe-declarations.md, spec/non-functional/NFR-001-additive-compatibility.md, spec/stakeholder/StR-001-module-activation.md, spec/tests.md"
review_set: all
---
# SR-004: Evidence review of the #13 semantic module contract spec set

## Summary

Every `Verification` cell in FR-001..FR-006, every `Validation` cell in the
constraint tables and in StR-001's Validation Criteria, every NFR-001
`Measurement` `Method` cell, and every Test Matrix `Type` was checked against
the declared catalog in `spec-artifacts-process/manifest.yaml` — 33 method ids
across the classes `Test`, `Analysis`, `Inspection`, `Demonstration`, and the
matrix `Type` vocabulary `Unit | Integration | E2E | Property | Fuzz |
Benchmark | Static | Compile | Snapshot | Manual | Eval | Inspection |
Analysis | Demonstration`. `quoin advise` was run over the 57 obligations
`quire coverage --json` derives (53 acceptance criteria plus the 4 NFR-001
measurement rows): **1 mismatch, 4 uncatalogued, 0 inconclusive**. Context:
agent-ix/spec-objects-security#13; grounded against the sibling evidence
review `agent-ix/spec-objects-business` SR-005 and against the implementation
landing concurrently on this branch.

Three vocabulary checks come back clean and are recorded here so the next
reviewer does not re-run them. **Matrix `Type`**: the matrix uses only `Unit`,
`Integration`, `Static`, `Property` and `Manual`, all five declared. **Status
markers**: `^(✅|❌|🚧|⛔)(\s+.*)?$` holds for all 74 rows and all six
traceability rows; no `⚠️` appears anywhere under `spec/`, so no row is exempt
from the status-lie check by construction (the quire-rs CR-083 trap). **Skips**:
`tests/conftest.py` makes the missing Quire wheel a hard failure rather than a
skip, and no `pytest.mark.skip` exists in the suite; the one `xfail` is
`strict=True` with an issue reference, and its matrix row says so.

What the engine found on its own: FR-001's four `Verification` cells (`Schema
Test` x1, `Integration Test` x3) are strings no catalog entry or class
declares, so `uncatalogued-verification-method` fires twice and nothing can say
what discharging them means; FR-003-AC-5 is the single authored/recommended
mismatch; two `Manual` rows are flagged as verified by a method that mints no
source symbol; and no `SuiteRegistry` or `Inspections` document exists to
discharge anything that is not a tagged test.

What judgement adds: **StR-001-VC-1 and VC-2 are `Demonstration` criteria with
no discharging artifact at all** — the matrix cites TC-005 and TC-006 for them,
and those two rows trace `FR-001-AC-1`, not the stakeholder criteria (FND-180).
TC-111 is typed `Manual` but is an ordinary tagged pytest. TC-071 is typed
`Property` and is an example test over ten named vocabularies. And the
advisor's `performance-benchmarking`, `dast`/`iast` and `demonstration`
recommendations are characteristic misfires the author should decline, not
follow.

## Verdict

**Revise before the matrix is treated as the verification contract.** The
authored methods are mostly right: 53 of 57 obligations carry a declared class
and the advisor agrees with them at class level, the honest-disclosure
paragraph about hand-built records in `spec/tests.md` is exactly the
distinction this analysis exists to force, and the tests that have landed
(FR-002, FR-003, FR-004, StR-001-VC-3 — 80 of 130 rows backed) discharge what
they claim. The blocking items are the stakeholder criteria that nothing can
verify (FND-180), the four uncatalogued FR-001 cells (FND-181), and the two
`no_source_symbol` rows that have no registry to be discharged through
(FND-182, FND-186).

Counts: 1 high, 5 medium, 9 low.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|----|----------|---------|------|--------------|
| FND-180 | high | StR-001-VC-1 (activation registers the declared contents) and VC-2 (minijinja-cli generators produce valid artifacts from the shipped templates) are authored `Demonstration` and have no discharging artifact. The `Stakeholder Requirement Coverage` row cites `TC-005, TC-006, TC-111`, but TC-005 and TC-006 are `Unit` rows whose `Traces To` is `FR-001-AC-1` (manifest validates against the FR-035 schema; lexicon entries carry a definition) — neither asserts anything about activation or about generator output — and TC-111 traces VC-3 only. `quire coverage` reports StR-001 1/3. `demonstration` produces `Manual` evidence discharged through an inspections registry, which does not exist, so as authored two of the three stakeholder criteria are unverifiable by any means the repository has. Either give VC-1 a row against a running filament-core (the FR-001-AC-4 evidence already planned as TC-004-equivalent), give VC-2 a row that runs minijinja-cli over a shipped template, or withdraw them. | StR-001-VC-1, StR-001-VC-2, TC-005, TC-006, TC-111 | correct-requirement-no-evidence |
| FND-181 | medium | FR-001-AC-1 is authored `Schema Test` and FR-001-AC-2..AC-4 `Integration Test`; neither string is a catalog method id nor a class, and `quire coverage` reports `uncatalogued-verification-method` for both (1 row and 3 rows). Nothing can say what discharging them means, and `quoin advise` marks all four `⚠ uncatalogued`. Recommend `Test` in the class form the rest of this spec set uses: AC-1 is `unit-testing` (the manifest validated against the vendored FR-035 schema — one component, fixed oracle, which is what TC-005 already is), AC-2..AC-4 are `integration-testing` (`cross-component`, `io-boundary` — a real HTTP activation). The advisor's `bdd-spec-by-example`/`unit-testing`/`property-based-testing` for AC-2..AC-4 comes from the `example` and catch-all `universal` shapes and is set aside by judgement; the statements carry no `cross-component` token the rules can read. This is the same defect as spec-objects-business SR-005 FND-160/FND-161 and should take the same disposition. | FR-001-AC-1, FR-001-AC-2, FR-001-AC-3, FR-001-AC-4 | wrong-requirement |
| FND-182 | medium | The two `Manual` rows are flagged by the engine — `TC-046 is verified by Manual, which mints no source symbol` and the same for `TC-110` — and neither has a discharge path. Both carry FR-003-AC-5 (`Demonstration`: `quoin module install path:` exits zero, `quoin module` lists the module, the prior entry is restored) and TC-110 also carries IT-002-SC-01..06. The engine that would run them is unprovisioned: the installed Quoin is `0.23.1-2-g3e842ce`, a build from main, and no release carries the semantic installer, so no CI fixture can discharge these rows and no `Inspections` document exists to record a human doing it. The criterion has an executable oracle (exit code, listing membership, restored state) and should be retyped `Test`/`Integration` the day a Quoin release carries FR-070/FR-073/FR-075; until then the `Demonstration` is honest but undischargeable, and the matrix should say which of the two it is. | FR-003-AC-5, IT-002, TC-046, TC-110 | correct-requirement-no-evidence |
| FND-183 | medium | TC-111 is typed `Manual` in the Test Case Summary but is an automated test: `test_two_records_of_different_types_are_distinguishable_by_schema_alone` at `tests/test_manifest_semantic.py:178`, carrying `@pytest.mark.trace("TC-111", "StR-001-VC-3")` and bound by `quire coverage` (StR-001 1/3 is this row). `Manual` is a `no_source_symbol` type, which withdraws the status-lie accusation from the row by construction — so a row that is in fact a green unit assertion is typed as one nothing could ever back. Retype `Unit` and change StR-001-VC-3's `Validation` from `Demonstration` to `Test`; the criterion as written ("a fixture reader can consume", "distinguishable by schema alone") is a fixed-oracle assertion over shipped files, which is `unit-testing`, not a witnessed operation. | StR-001-VC-3, TC-111 | wrong-requirement |
| FND-184 | medium | TC-071 is the only `Property`-typed row and is not property-shaped. FR-006-AC-2 reads "for each vocabulary, a record carrying its unassessed member validates and a record carrying an invented member fails" — ten named vocabularies from the FR-006 table, two fixed example records each: a parameterized example test, which is `unit-testing` (Unit). The advisor's `property-based-testing (universal)` is the catch-all, not a shape match: `quire coverage` reports `catch-all-universal` for 8 of 8 documents, meaning no criterion in this spec set named a specific property shape at all. `Property` becomes the honest type only if the invented-member half generates arbitrary non-member strings against the closed `enum` (a genuine universally-quantified refusal); if the implementation lands two literals per vocabulary, type it `Unit`. | FR-006-AC-2, TC-071 | wrong-requirement |
| FND-186 | medium | No evidence-plan artifacts exist. `quire coverage` reports `declaration 'suite' declares archetype 'SuiteRegistry', which no document in the corpus has` and `declaration 'inspection' declares archetype 'Inspections', which no document in the corpus has`. Every `Integration` row needs a suite that says where its Quire wheel and (for FR-001/IT-001) its running filament-core come from, and every `no_source_symbol` row (TC-046, TC-110) plus every judgement-only constraint (FR-002-CON-1, FR-006-CON-1, FR-005-CON-1) needs the inspections registry to be discharged. `spec/tests.md` Coverage Gaps names the absence, which is the right place for it — this is a gap in the plan, not in the spec — but the gap is currently open and eleven rows depend on it. | TC-046, TC-110, FR-002-CON-1, FR-005-CON-1, FR-006-CON-1, IT-001 | correct-requirement-no-evidence |
| FND-185 | low | NFR-001's four `Measurement` rows are authored `Test`; the advisor recommends `performance-benchmarking` on `quantified-threshold` for all four, which is a rule misfire — the targets are `0`, not a latency or a throughput. Judgement: M-1 (0.1.0 locators changed) and M-2 (`traceability`/`allowed_links` bytes changed) are diffs against a checked-in 0.1.0 baseline, which is `golden-approval-testing` (Snapshot); M-3 and M-4 (error findings and `semantic.record-invalid` findings per 0.1.0 skeleton under 0.2.0) run Quire over the module, which is `integration-testing` (Integration). The matrix types TC-100 and TC-101 `Unit`; `Snapshot` is the honest type for a baseline diff, and TC-102/TC-103 are already `Integration`. Class-level the authored `Test` is not wrong, so this is a sharpening, not a correction. | NFR-001-M-1, NFR-001-M-2, NFR-001-M-3, NFR-001-M-4, TC-100, TC-101, TC-102, TC-103 | wrong-requirement |
| FND-187 | low | The `Coverage Gaps` section of `spec/tests.md` lists `TC-005, TC-006, TC-030, TC-031, TC-033, TC-046, TC-076, TC-089, TC-110, TC-111` as the `Static`/`Manual` rows needing an `Inspections` document. Three of those are neither: TC-005 and TC-006 are `Unit` and TC-111 is an automated pytest (FND-183). The list overstates what the missing registry blocks and understates what is already discharged; trim it to the two `Manual` rows and the five `Static` rows. | TC-005, TC-006, TC-111 | correct-requirement-no-evidence |
| FND-188 | low | FR-002-CON-1, CON-2 and CON-4 are authored `Inspection`, the `judgement-required, no-executable-oracle` method, but each already has an executable matrix row that asserts it over the tree: TC-030 (`Static`, official emitter only, no hand-edited file), TC-031 (`Static`, no `.npmrc`, no `file:`/`link:`, exact pins), TC-032 (`Unit`, every lockfile resolution from npmjs except `@agent-ix/semantic-core`). All three are backed by tests in `tests/test_schema_emission.py`. The authored `Validation` cell contradicts its own discharging artifact; write `Test` for CON-2 and CON-4. CON-1's "no hand-edited file" half is defensibly judgement, but the emitter half is executable and TC-030 executes it. | FR-002-CON-1, FR-002-CON-2, FR-002-CON-4, TC-030, TC-031, TC-032 | wrong-requirement |
| FND-189 | low | FR-006-CON-1 ("no vocabulary gains a member expressing 'assume the permissive value'") and FR-005-CON-1 ("no corpus repository or vendored fixture is edited") are authored `Inspection`, and that is the right class: both are judgement over authored intent with no oracle a schema could hold. Their matrix rows are typed `Static` (TC-076, TC-089), which is the type a diff-over-the-branch check and a member-name review can be made to carry — but `Static` is deliberately not a `no_source_symbol` type, so both rows will be reported as unbacked overclaims until either a real check lands or they move to the inspections registry. Pick one; do not leave a judgement criterion typed as if code asserted it. | FR-005-CON-1, FR-006-CON-1, TC-076, TC-089 | correct-requirement-no-evidence |
| FND-190 | low | Advisor residue recorded as judgement, not verdict. `dast`/`iast`/`negative-abuse-testing` were recommended on FR-004-AC-3, FR-005-AC-2, FR-005-AC-7, FR-005-AC-9 and FR-006-AC-4 from a `security` characteristic read off security-domain nouns in the statements; none of these obligations touches a running exposed surface — they are JSON Schema validations over records and static scans over checked-in Markdown — so the authored `Test` stands. Likewise `grammar-based-fuzzing` on FR-004-AC-13, `fuzzing` on FR-006-AC-6, `model-checking`/`runtime-monitoring` on FR-002-AC-8 (a `temporal` read of "then"), and `demonstration` on FR-004-AC-12 (`stakeholder-acceptance`). The one defensible refinement is FR-005-AC-9, where `negative-abuse-testing` reads on the credential-literal scan; a static scan over the skeleton set discharges it more cheaply. | FR-004-AC-3, FR-004-AC-12, FR-004-AC-13, FR-005-AC-2, FR-005-AC-7, FR-005-AC-9, FR-006-AC-4, FR-006-AC-6, FR-002-AC-8 | wrong-requirement |
| FND-191 | low | `quire coverage` reports `status-column-matches-nothing`: the `Functional Requirement Coverage` table uses the header `Coverage Status` while the module configures `traceability.status.column: Status`, so status classification was skipped for that table and a complete-but-unbacked requirement row could not be checked for a status lie. FR-002 is now 9/9 and FR-004 14/14 backed while both rows still read `🚧 pending implementation`, which is the class of drift this check exists to catch and currently cannot. The per-test `Test Case Summary` does carry `Status` and was classified. | TM-001 | correct-requirement-no-evidence |
| FND-192 | low | Binding hygiene that costs three rows: `tag-on-non-binding-symbol` fires for `FR-002`, `FR-003` and `FR-004` written in the module docstrings of `tests/test_schema_emission.py`, `tests/test_manifest_semantic.py` and `tests/test_role_schemas.py` — a container does not bind a trace id (CR-061), so the tag reached no channel and the requirement it names is reported unbacked, indistinguishable from a test nobody wrote. Separately `marker-form-mismatch` names `test_every_schema_declares_the_2020_12_id_under_the_manifest_version_base` at `tests/test_schema_emission.py:110` as carrying an id in its own name that no declared name form read, and `coverage.self_named_binding.python` publishes 0 of 1 with a `hollow-denominator` warning. None of these is a method question; all three make the evidence census read worse than the suite is. | TM-001, FR-002, FR-003, FR-004 | correct-requirement-no-evidence |
| FND-193 | low | FR-001's own rows are 0/4 backed although TC-001..TC-014 all exist and pass, because those tests carry their ids in a `"""TC-002: FR-001-AC-1."""` docstring where only the leading id binds. The criteria FR-001-AC-1..AC-4 therefore report `has no backing symbol [verification]` while fourteen tests assert AC-1. Once FND-181 gives the cells a catalogued method, the tags should carry both ids the way the newer `@pytest.mark.trace(...)` rows do, so the method and its evidence meet. | FR-001-AC-1, TC-001, TC-002, TC-003, TC-004 | correct-requirement-no-evidence |
| FND-194 | low | No obligation was inconclusive — `quoin advise` placed 57 of 57 — and no `fault-detection-unmeasured` or `fault-detection-failed` characteristic minted, so `mutation-testing` and `concolic-execution` were correctly recommended for nothing. That is a consequence of the evidence store, not of the requirements: 80 of 130 rows are backed and nothing yet measures whether those tests would catch a seeded fault. When FR-005, FR-006 and NFR-001 land their rows, run the advisor again; `mutation-testing` over the schema-validation suite is the cheap first escalation, and is the one to take before anything symbolic. | TM-001 | correct-requirement-no-evidence |

## Method recommendations per obligation

Only obligations whose authored method should change or be sharpened are
listed. The 49 acceptance criteria authored `Test` whose advisor
recommendation is a `Test`-class method (`unit-testing`,
`property-based-testing`, `bdd-spec-by-example`) match at class level and need
no edit.

| Obligation | Authored | Advisor | Recommended | Basis |
|---|---|---|---|---|
| FR-001-AC-1 | Schema Test (uncatalogued) | bdd-spec-by-example, unit-testing (example) | `Test` / `unit-testing` | rule + judgement: one component, fixed oracle; TC-005 already is this |
| FR-001-AC-2, AC-3, AC-4 | Integration Test (uncatalogued) | bdd-spec-by-example, unit-testing, property-based-testing | `Test` / `integration-testing` | judgement: real HTTP activation boundary; the advisor cannot read `cross-component` from the statement |
| FR-003-AC-5 | Demonstration | bdd-spec-by-example, unit-testing (mismatch) | `Test` / `integration-testing`, once a Quoin release carries it | rule + judgement: exit-code and listing oracle; blocked on the engine, not on the method |
| StR-001-VC-1 | Demonstration | not an obligation (VC table) | `Test` / `integration-testing` against a running filament-core | judgement: the same outcome is FR-001-AC-4 |
| StR-001-VC-2 | Demonstration | not an obligation (VC table) | `Test` / `e2e-testing` over minijinja-cli, or withdraw | judgement: no artifact discharges it today |
| StR-001-VC-3 | Demonstration | not an obligation (VC table) | `Test` / `unit-testing` | rule-free judgement: TC-111 already discharges it as a tagged pytest |
| FR-002-CON-2, CON-4 | Inspection | not an obligation (constraint) | `Test` | judgement: executable oracle over `package.json` and the lockfile; TC-031/TC-032 execute it |
| FR-006-AC-2 | Test | property-based-testing (universal catch-all) | `Test` / `unit-testing` unless the negative half generates | judgement: ten named vocabularies, fixed records — see FND-184 |
| NFR-001-M-1, M-2 | Test | performance-benchmarking (misfire) | `Test` / `golden-approval-testing` | judgement: baseline diff, `stable-output` |
| NFR-001-M-3, M-4 | Test | performance-benchmarking (misfire) | `Test` / `integration-testing` | judgement: Quire validates the 0.1.0 skeleton set |

## Suite plan implied

The methods above imply these evidence kinds, and no `SuiteRegistry` declares a
producer for any of them (FND-186):

- `Unit` (pytest over `spec_objects_security/`, `schemas/`, `manifest.yaml`, no engine): FR-002-AC-1..3, FR-003-AC-1..3, FR-003-AC-7, FR-004-AC-1, FR-004-AC-11, FR-004-AC-13, FR-005-AC-6..9, FR-006-AC-1..3, FR-006-AC-6, StR-001-VC-3.
- `Integration` (pytest with the Quire wheel `make dev-quire` provisions, and for FR-001/IT-001 a running filament-core): FR-001-AC-2..4, FR-002-AC-4..9, FR-003-AC-4, FR-003-AC-6, FR-004-AC-2..10, FR-004-AC-12, FR-004-AC-14, FR-005-AC-1..5, FR-006-AC-4..5, NFR-001-M-3..4, StR-001-VC-1.
- `Snapshot` (checked-in 0.1.0 baseline under `tests/fixtures/baseline-0.1.0/`): NFR-001-M-1, M-2, FR-002-CON-3.
- `Static` (checks over the committed tree and the branch diff): FR-002-CON-1..2, FR-002-CON-5, FR-005-CON-1, FR-006-CON-1.
- `Manual` via an inspections registry: FR-003-AC-5 and IT-002 while no Quoin release carries the installer, and StR-001-VC-2 if it is kept as a demonstration.

## Diagnostics consulted

From `quire coverage --scope .` (quire 0.31.0, engine 0.46.0@ca7362d4):
`uncatalogued-verification-method` x2 (`Integration Test` 3 rows, `Schema Test`
1 row), `status-column-matches-nothing` (functional-coverage),
`archetype-matches-nothing` x2 (`SuiteRegistry`, `Inspections`),
`tag-on-non-binding-symbol` x3 (module docstrings carrying `FR-002`, `FR-003`,
`FR-004`), `marker-form-mismatch` x1, `hollow-denominator`
(`coverage.self_named_binding.python`), `catch-all-universal` (8 of 8
documents), plus `Manual` mints-no-source-symbol notes for TC-046 and TC-110.
Headline: `Coverage: 80/130 rows backed (61%)`, `python: 51/51/51
bound/tagged/candidates`. From `quoin advise`: 57 of 57 obligations shown, 1
mismatch (FR-003-AC-5), 4 uncatalogued (FR-001-AC-1..AC-4), 0 inconclusive.
`DuplicateArchetype`/`DuplicateInverseEdge` module-load noise ignored.

## Dispositions

| Finding | Disposition |
|---|---|
| FND-180 | Open. Blocking: two of three stakeholder validation criteria have no artifact that could discharge them, and the matrix rows cited for them assert a different requirement. |
| FND-181 | Open. Blocking: four obligations carry a method nothing can define. The sibling repository applied the class form `Test`; the same disposition fits here. |
| FND-182 | Open, expected to be recorded rather than fixed: the method is honest and the engine is unavailable. The matrix should say which rows are blocked on the Quoin release and which on the missing registry. |
| FND-183 | Open. A one-word matrix edit (`Manual` → `Unit`) and a one-word spec edit (`Demonstration` → `Test`); both are in files this review may not edit. |
| FND-184 | Open, to be settled when TC-071 lands: `Property` is legal only if the implementation generates the invented members. |
| FND-185 | Open, advisory. Class-level the authored `Test` is defensible; the refinement is a matrix `Type` question. |
| FND-186 | Open, carried to the plan rather than to the spec, as `spec/tests.md` Coverage Gaps already does. |
| FND-187 | Open, advisory: trim the Coverage Gaps list to the rows the missing registry actually blocks. |
| FND-188 | Open, advisory. |
| FND-189 | Open, advisory: choose between a real static check and the inspections registry for TC-076 and TC-089. |
| FND-190 | Recorded, no change: the authored `Test` stands on all nine. |
| FND-191 | Open, advisory; the same header/configuration mismatch is open in the sibling repository (SR-005 FND-169) and is a process-module question, not a spec change. |
| FND-192 | Open, implementation hygiene: move the three module-docstring ids onto the evidence symbols. |
| FND-193 | Open, implementation hygiene, to be taken with FND-181. |
| FND-194 | Recorded, no change; re-run the advisor when FR-005, FR-006 and NFR-001 land their rows. |

### Round record (2026-09-04)

Applied in the review-fix round: FND-180 (TC-112 and TC-113 added for StR-001-VC-1 and VC-2, each naming the environment it needs), FND-181 (FR-001's uncatalogued cells changed to `Test`), FND-183 (TC-111 retyped `Unit`, since it is a tagged pytest quire binds), FND-184 (TC-071 retyped `Unit`: it is ten named vocabularies with fixed records, not a generated property), FND-192 (the module-docstring ids moved off the containers that bind nothing — `quire coverage` now reports zero `tag-on-non-binding-symbol` and zero `marker-form-mismatch`).

Recorded without change, and carried into the report rather than silently closed: FND-182, FND-185..FND-191, FND-193, FND-194.
