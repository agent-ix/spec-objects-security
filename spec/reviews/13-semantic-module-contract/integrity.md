---
id: SR-006
title: "Integrity review of the #13 semantic module contract spec"
type: SpecReview
analysis: integrity
scope: "spec/spec.md, spec/stakeholder/StR-001-module-activation.md, spec/usecase/US-001-declare-security-objects-against-semantic-core.md, spec/functional/FR-001-module-manifest-activates.md, spec/functional/FR-002-emitted-json-schemas.md, spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/functional/FR-006-security-safe-declarations.md, spec/non-functional/NFR-001-additive-compatibility.md, spec/integration/IT-001-manifest-activation-roundtrip.md, spec/integration/IT-002-quoin-module-install.md, spec/tests.md"
review_set: all
---
# SR-006: Integrity review of the #13 semantic module contract spec

## Summary

Integrity gate — completeness, consistency, atomicity and testability — over
the thirteen artifacts that deliver `agent-ix/spec-objects-security#13`,
grounded against `spec_objects_security/manifest.yaml` (0.1.0, on `main`), the
23 checked-in skeletons, the `@agent-ix/semantic-core` 0.1.0 TypeSpec source,
and the sibling review `agent-ix/spec-objects-business` SR-003.

Every type-name population was counted, not assumed, and the counts agree
without exception. The spec also closes the high finding of the business
review: FND-120 there was FR-004's required record keys contradicting NFR-001's
zero-error metric. Here NFR-001 names its population explicitly (the 23
skeletons as they stood at 0.1.0), states the mechanism that makes the metric
hold (Quire runs the semantic layer only on a document declaring a frontmatter
`object:` key), and asserts it rather than assuming it. That mechanism is
verified against the repository: 0 of the 23 checked-in skeletons carry
`object:`, and FR-005 introduces the key only on the rewritten skeletons, which
FR-005-AC-1 requires to validate. The `quire-rs#391` residue is carried beside
NFR-001-AC-4 as a named expected failure. **There is no NFR-001/FR-004
contradiction in this spec.**

What the gate does catch is evidence, not design: a Test Matrix whose
completeness claim is false for seven criteria, and a fail-not-skip test rule
whose execution environment nothing in the spec disposes of, against a CI
workflow that runs the whole `pytest` suite and will therefore be red by
construction.

### Counts

| Population | Counted | Source | Agrees |
|---|---|---|---|
| Object types in the manifest | 23 | `manifest.yaml` `- name:` entries | baseline |
| `spec.md` In Scope | 23 | "the 23 tier-2 ObjectTypes" | yes |
| FR-003 `semantic.exports` list | 23 | FR-003 Behavior | yes, same names and order |
| FR-003 admitted `semantic` keys | 9 | FR-003 Behavior vs "nine admitted keys" (AC-1) | yes |
| FR-004 table rows | 23 | one row per manifest name, no extra, none missing | yes |
| FR-004 `fields`-required types | 18 | FR-004 table Required keys column | yes |
| FR-004 `clauses`-required types | 6 | FR-004 table Required keys column | yes |
| FR-004 `operations`-required types | 1 (`auth_flow`) | FR-004 table Required keys column | yes |
| FR-005 field-bearing list | 18 | FR-005 Behavior | identical set to FR-004 |
| FR-005 clause-bearing list | 6 | FR-005 Behavior | identical set to FR-004 |
| Partition check | 18 + 6 + 1 − 2 = 23 | overlap is exactly `trust_boundary` and `control`, both required-`fields`-and-`clauses` in FR-004 | exact partition |
| FR-004 marker models | 12 | FR-004 Outputs | matches the 8 graded-row rules + identity/defaulted/occurrence/occurrence-typeref |
| Graded vocabularies | 10 | FR-006 table = FR-004 Outputs list = TC-070 | yes |
| FR-006 defaulted-field-refusing types | 7 | FR-006 Behavior = FR-006-AC-4 = FR-004 rows carrying "0 defaulted fields" | yes |
| Named negative fixture cases | 10 | FR-005 Behavior vs FR-005-AC-5 "the ten cases" vs TC-084 | yes |
| Skeleton files | 23 + 3 alternates = 26 | FR-005 Inputs vs FR-005-AC-1 | yes |
| Test-case rows | 74 | tests.md Test Case Summary | — |
| AC / CON / SC / VC obligations | 79 | 68 FR+NFR AC and CON, 8 IT, 3 StR VC | — |
| Obligations with no TC row | 7 | FR-001-AC-2..4, IT-001-AC-1..2, StR-001-VC-1..2 | **no** |

Grounding against semantic-core 0.1.0 `main.tsp` confirms the readings the spec
depends on: `SemanticId` carries a `^ix://…` pattern (so FR-004-AC-12's "a bare
token is rejected by the schema" holds), `Timestamp` is a `KernelScalar` member
(so the occurrence-field rule is expressible), `FieldDecl.identity` and
`FieldDecl.default` exist as optional keys, and `pattern` and `format` are
indeed members of the closed `ConstraintKeyword` enum that FR-005 reports the
pinned reader rejecting.

## Verdict

**Not ready for `spec-to-plan`.** Two highs must be dispositioned first. FND-140
is a matrix edit (add the missing rows, or state the exemption in Coverage Gaps
and drop the "every criterion has a row" claim). FND-141 is a real decision, not
an edit: something must say which gate runs the semantic suite while `quire` is
deliberately undeclared, because the repository's CI runs the whole `pytest`
suite and FR-005 forbids the skip that would keep it green. The six mediums are
one-line spec additions or new AC/TC rows; the lows can be swept with them. No
finding requires re-opening the schema design, the vocabulary set, or the
NFR-001 compatibility argument, all three of which hold.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-140 | high | tests.md Coverage Gaps claims "Every criterion, constraint, and metric above has a row", but seven obligations have no Test Case Summary row tracing them: FR-001-AC-2, AC-3, AC-4, IT-001-AC-1, AC-2, StR-001-VC-1, VC-2. The IT-001 row maps TC-002..TC-004, whose Traces To column is FR-001-AC-1 and whose titles are YAML-parse unit tests, not activation tests; the StR row maps TC-005/TC-006, likewise FR-001-AC-1 rows | tests.md, FR-001, IT-001, StR-001 |
| FND-141 | high | FR-005 requires every semantic test to fail rather than skip when the Quire wheel is absent, and forbids declaring `quire` in `pyproject.toml` until `agent-ix/quire-rs#392`; nothing states which gate runs that suite. `.github/workflows/ci.yml` delegates to `agent-ix/python-service-actions` `lib-ci.yml`, which does `poetry install` then `poetry run pytest` over the whole suite and never `make dev-quire`, so every semantic row fails in CI by construction from the day it lands | FR-005, tests.md Test Environment, .github/workflows/ci.yml |
| FND-142 | medium | FR-004 states "the obligation each of them carries SHALL also be expressed as an item rule over `fields` … one row per optional graded key its table row names", but the table itself carries such a rule for only 8 keys (`stride_category`, `severity`, `likelihood`, `impact`, `status`, `level`, `trust_level`, `effectiveness`). `lifecycle`, `classification` and `factor_kind` are graded (closed-vocabulary) optional keys with no item rule and no marker model, and FR-005's authored-row list and FR-004's 12 marker models both stop at the same 8. The universal sentence and the table disagree | FR-004, FR-005, FR-006 |
| FND-143 | medium | The "checked-in 0.1.0 baseline" is a deliverable that four criteria compare against — FR-003-AC-3, FR-003-AC-7, NFR-001-AC-1, AC-2 — and NFR-001-AC-3/AC-4 validate "the checked-in 0.1.0 skeleton set" after FR-005 has rewritten the live skeletons; no requirement states where that baseline lives, what it contains, how it is produced, or that it is frozen | FR-003, FR-005, NFR-001 |
| FND-144 | medium | FR-002 requires the generator to "edit `manifest.yaml` only at `data_schema.digest` values" while FR-003-CON-3 and NFR-001-AC-2 require the `traceability` block and every `allowed_links` map to stay byte-identical. This manifest is anchor-bearing (`&id001`/`*id001`, six aliases) and carries the FR-043/FR-058 comment blocks; a structural YAML round-trip drops both. Whether the edit is textual or structural, and whether the baseline comparisons are byte-level or structural, is unstated | FR-002, FR-003-CON-3, FR-003-AC-7, NFR-001-AC-2 |
| FND-145 | medium | Five FR-002 Behavior obligations have no acceptance criterion and no TC row, behind the matrix's completeness claim: the Node-20 / unresolvable-`tsp` error message, "SHALL write files under `spec_objects_security/schemas/` only", "SHALL edit `manifest.yaml` only at `data_schema.digest`", the `.gitattributes` `eol=lf` marking that protects the digested bytes, and `stage-npm.mjs`'s `postpack` removal of the staged copies (AC-7 tests only the presence half) | FR-002, tests.md |
| FND-146 | medium | FR-002 binds `make schemas-check` to `make lint` "so a `typespec/` edit that was never regenerated fails before push rather than at review", while FR-002-CON-4 rules the check out of the GitHub workflow. `lib-ci.yml` runs `black --check`, `ruff check` and `pytest` directly and never `make lint`, so the drift guard is voluntary and unenforced; the spec names no replacement gate | FR-002, FR-002-CON-4, .github/workflows/ci.yml |
| FND-147 | low | FR-005 lists `identity` among "the constraint keywords the typed-table reader … accepts". `identity` is not a member of semantic-core's closed `ConstraintKeyword` enum (`main.tsp`: min, max, exclusiveMin, exclusiveMax, pattern, minLength, maxLength, enumValues, nonEmpty, unique, format); it is the `FieldDecl.identity` flag, which FR-004 states correctly. The two readings should be one | FR-005, FR-004, semantic-core main.tsp |
| FND-148 | low | `FieldDecl.identity` is `identity?: boolean`, so `identity: false` is expressible in a hand-built record. FR-004 declares the absent-not-false reader convention and pins a semantic-core change to a manifest bump, but FR-004-AC-2 tests only "the identity flag removed"; the `identity: false` edge, and the `maxContains: 0` edge for `AuditEvent`, are unpinned | FR-004-AC-2, FR-004-AC-9 |
| FND-149 | low | FR-001 carries no `implements`/`traces_to` relationship to StR-001 or US-001 in frontmatter — only to filament-core-service FR-035 — so the stakeholder trace for FR-001 exists in tests.md alone. FR-002..FR-006 reach StR-001 transitively through US-001 | FR-001, StR-001, tests.md |
| FND-150 | low | Process obligations authored as system behaviour and unverifiable as written: FR-003's "this module SHALL correct its own manifest or schemas rather than relax the contract keys", FR-006's "The module SHALL rewrite or remove a fixture" and "SHALL NOT relax a rule of this requirement". None is externally observable; no TC traces them | FR-003, FR-006 |
| FND-151 | low | FR-004 requires every `fields`, `params`, `clauses`, `operations` and `relations` item to be `$ref`ed to semantic-core, but `params` is not a declaration-record key: FR-004 Inputs shapes the record as `{ fields?, relations?, clauses?, operations?, … }` and no table row admits `params`. It lives inside `OperationDecl.params`, already covered by the `$ref` to `OperationDecl` | FR-004, semantic-core main.tsp |
| FND-152 | low | FR-002 carries four separable obligations — deterministic emission, the `$id`-embeds-version policy with its bump procedure, `--check` mode, and wheel/npm packaging plus `stage-npm.mjs` — under one requirement id, which is why FND-145's orphan behaviours had nowhere to hang. Atomicity favours splitting the packaging/staging half | FR-002 |
| FND-153 | low | IT-002 and FR-003-AC-5 depend on a Quoin built from `agent-ix/quoin` main at or after `3e842ce` with no released tag and no fallback, so TC-110 is reproducible only on a developer checkout; the paths are parameterised (an improvement on the business review's FND-128) but the unreleased-dependency half stands. IT-001 has no TC of its own — see FND-140 | IT-002, FR-003-AC-5, IT-001 |

## Dispositions

| ID | Disposition |
|---|---|
| FND-140 | Add Test Case Summary rows for FR-001-AC-2, AC-3, AC-4 and IT-001-AC-1, AC-2 (one integration row per activation assertion, `🚧 needs a running filament-core`), and for StR-001-VC-1 and VC-2; retarget the IT-001 row away from TC-002..TC-004. If any is deliberately unrowed, say so in Coverage Gaps and drop the "every criterion … has a row" sentence — the claim and the table must agree before the matrix is a verification contract |
| FND-141 | Decide and record: either (a) mark the semantic suite with a marker the CI `pytest` invocation deselects while `agent-ix/quire-rs#392` is open, and state in FR-005 that the suite's enforcing gate is the local `make test` after `make dev-quire`; or (b) provision the wheel in CI. Add the decision to FR-005 Behavior and to the tests.md Test Environment note, and add an AC that the suite is red — not absent — when the engine is missing on the gate that owns it. Do not resolve it by restoring the skip, which is exactly what `agent-ix/spec-objects-security#10` disposed of |
| FND-142 | Narrow the FR-004 sentence to the eight keys the table and the marker set actually carry, and state why `lifecycle`, `classification` and `factor_kind` carry no row obligation (no skeleton authors them today), or add the three rules with their marker models and the matching FR-005 authored-row entries. Keep FR-005's list and FR-004's marker list in lockstep with whichever is chosen |
| FND-143 | Add the baseline to FR-003 or FR-005 Outputs as a named deliverable — path, content (the 0.1.0 `body_extraction`, `traceability`, `allowed_links` blocks and the 23 0.1.0 skeletons), and the rule that it is written once from the 0.1.0 tag and never edited afterwards — and reference it from NFR-001 Verification |
| FND-144 | State in FR-002 that the digest rewrite is a targeted textual edit that preserves anchors, aliases and comments, and add an AC that `git diff` after `make schemas` touches only `digest:` lines. State in FR-003-AC-7 and NFR-001-AC-2 whether the comparison is byte-level or structural |
| FND-145 | Add acceptance criteria and TC rows for the five orphan behaviours, or move them into FR-002-CON rows so the matrix's constraint sweep picks them up. The `.gitattributes` one matters most: without it a CRLF checkout invalidates every digest |
| FND-146 | Either name the gate that runs `make schemas-check` (a workflow step that does not need npm.ix, or a documented pre-push hook) or restate the FR-002 sentence as a local convenience and record that schema drift is caught at review until `agent-ix/filament-core-data#11` publishes semantic-core publicly. Resolve alongside FND-141 — both are the same unstated question about which gate owns which evidence |
| FND-147 | Reword the FR-005 sentence to "the bare `identity` flag token plus the constraint keywords …", matching FR-004's reading |
| FND-148 | Extend FR-004-AC-2 to the `identity: false` record and FR-004-AC-9 to a record with two identity fields, so both `contains` edges are pinned |
| FND-149 | Add an `implements` relationship from FR-001 to StR-001 (or a `traces_to` to US-001) in frontmatter so the trace lives in the artifact rather than only in the matrix |
| FND-150 | Move the three process obligations to a Notes or Rationale block, or restate each as an observable refusal (the check that fails, the fixture that is absent). A `SHALL` with no observable subject is not a requirement |
| FND-151 | Drop `params` from the FR-004 `$ref` sentence, or add "including `OperationDecl.params`" to make the nesting explicit |
| FND-152 | Optional before tasking: split FR-002 into emission plus check (FR-002) and packaging plus staging (a new FR), moving AC-6, AC-7 and the `.gitattributes`/`stage-npm` behaviours across. If it is kept whole, FND-145's rows must land on FR-002 |
| FND-153 | Keep the dependency, add the escape: state the Quoin version or tag that will replace `3e842ce` once released, and mark TC-110 `Manual` and exempt in Coverage Gaps rather than pending, since no automatable gate can run it today |

### Round record (2026-09-04)

Applied in the review-fix round: FND-140 (the seven obligations with no row now have one, and the Coverage Gaps claim is corrected), FND-141 (FR-005 states which gate runs this suite and why an automatic CI run would be red by construction), FND-142 (FR-004's graded-key claim narrowed to the eight keys that actually carry an item rule, with the other three stated as carrying none), FND-143 (the frozen baseline named as an FR-003 deliverable with its path), FND-144 (the textual digest rewrite stated, with the anchors-and-comments reason), FND-145 (FR-002-AC-10 and AC-11 added, with TC-034 and TC-035), FND-151 (the operations-parameter nesting made explicit in FR-004).

Recorded without change, and carried into the report rather than silently closed: FND-146..FND-150, FND-152..FND-156.
