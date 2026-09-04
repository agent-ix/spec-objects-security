---
id: SR-001
title: "Base review of the #13 semantic module contract spec"
type: SpecReview
analysis: base
scope: "spec/spec.md, spec/stakeholder/StR-001-module-activation.md, spec/usecase/US-001-declare-security-objects-against-semantic-core.md, spec/functional/FR-001-module-manifest-activates.md, spec/functional/FR-002-emitted-json-schemas.md, spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/functional/FR-006-security-safe-declarations.md, spec/non-functional/NFR-001-additive-compatibility.md, spec/integration/IT-001-manifest-activation-roundtrip.md, spec/integration/IT-002-quoin-module-install.md, spec/tests.md"
review_set: all
---
# SR-001: Base review of the #13 semantic module contract spec

## Summary

Checklist gate — id formats, story and requirement quality, verification-method
vocabulary, cross-reference integrity and the six coverage rules — over the
thirteen artifacts that deliver `agent-ix/spec-objects-security#13`. Grounded
against `spec_objects_security/manifest.yaml` on this branch (`version: 0.2.0`,
`manifest_version: 1.0.0`, 23 exported object types), the emitted schema set,
the skeleton set, the landing test suite, and the reference migration
`agent-ix/spec-objects-business` (issue #4) whose `base.md` this review follows.

Ids are well-formed and sequential per class: StR-001, US-001, FR-001..FR-006,
NFR-001, IT-001..IT-002, TM-001, and 74 `TC-NNN` rows allotted in per-FR blocks
with no duplicate and no collision. Every FR except FR-001 declares an
`implements` relationship to US-001, US-001 traces to StR-001, and every
internal link resolves. `quire validate --scope .` over the spec tree reports no
error.

Counts were checked against the tree rather than read from the prose, and the
declared populations hold: `semantic.exports` names 23 types and the manifest
declares 23 `object_type` entries; `spec_objects_security/schemas/` holds 47
schema files plus `toolchain.json`, which is exactly the 23 object-type models
of FR-004's table plus the 24 support models its Outputs declare (12 markers,
`ControlMapping`, `FlowStep`, 10 vocabularies); `skeletons/` holds 26 files,
the 23 types plus the three `sysml` alternates FR-005 Inputs names; and
`tests/fixtures/negative/` holds exactly the 10 cases FR-005 Behavior lists.

What the gate catches is bookkeeping, not design. One high: seven obligations
carry no Test Case Summary row while the matrix claims every one has a row, and
two rollup cells cite rows that assert something else. Three mediums: an
uncatalogued verification vocabulary in FR-001, two id schemes inside the IT
class, and coverage rule 5 stating a state no criterion tests.

## Verdict

**CONDITIONAL** — one high (FND-100), three mediums, all bookkeeping fixes
applicable before `spec-to-plan`. No requirement is withdrawn or reworded by
this review.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-100 | high | Coverage rule 1 is unmet for seven obligations, and `## Coverage Gaps` states the opposite ("Every criterion, constraint, and metric above has a row"). No Test Case Summary row traces FR-001-AC-2, FR-001-AC-3, FR-001-AC-4, IT-001-AC-1, IT-001-AC-2, StR-001-VC-1 or StR-001-VC-2. The rollup cells that appear to cover them cite rows that assert something else: the IT-001 row cites TC-002..TC-004, whose Traces To is `FR-001-AC-1` and whose titles are YAML-parse and duplicate-name unit tests, not an activation roundtrip; the StR-001 row cites TC-005/TC-006, likewise `FR-001-AC-1` rows for schema validation and lexicon completeness, neither of which demonstrates a registration or a minijinja generation. Every one of TC-001..TC-014 traces to `FR-001-AC-1` alone. Concurs with SR-006 FND-140, reached independently. Escape cause: correct-requirement-no-evidence. | spec/tests.md (rollup tables, Test Case Summary, Coverage Gaps), FR-001, IT-001, StR-001 |
| FND-101 | medium | FR-001's Verification cells read `Schema Test` (1 row) and `Integration Test` (3 rows); `quire coverage --scope .` reports both as `uncatalogued-verification-method` — "neither a declared verification_catalog method id nor a declared class". Every other requirement in the set uses the declared classes `Test`, `Demonstration` and `Inspection`. This is the same defect the reference migration fixed as `spec-objects-business` FND-003; the fix was not carried across when FR-001 was brought into the #13 scope. Escape cause: wrong-requirement. | FR-001-AC-1..4, `quire coverage` output |
| FND-102 | medium | One requirement class, two id schemes: IT-001 names its criteria `IT-001-AC-1..2` in an Expected Results table, IT-002 names its `IT-002-SC-01..06` per procedure step with zero-padded numbering. The matrix carries both forms verbatim (`IT-001-AC-1..2` in one cell, `IT-002-SC-01..IT-002-SC-06` in a Traces To cell), so a reader cannot tell whether `SC` is a distinct obligation kind or a spelling variant, and a range written into a Traces To cell hides that six criteria hang on one row. Escape cause: wrong-requirement. | IT-001, IT-002, spec/tests.md TC-110 |
| FND-103 | medium | Coverage rule 5 as written in `## Test Matrix Rules` names three availability states — `available`, `not_applicable`, `unavailable` — but the only criterion and row that test availability (FR-005-AC-4, TC-083) assert `available` and `not_applicable` only; `unavailable` is asserted nowhere, and no other criterion in the set mentions it. Either the rule overstates what is tested or a criterion for the `unavailable` state is missing. Escape cause: correct-requirement-no-evidence. | spec/tests.md rule 5, FR-005-AC-4, spec/tests.md TC-083 |
| FND-104 | low | StR-001-VC-3 — the only stakeholder criterion with a row — is discharged solely by TC-111, a `Manual` P2 row, which `quire coverage` reports as minting no source symbol. The stakeholder-level claim that "two records of different types are distinguishable by schema alone" is in fact discharged automatically by FR-004-AC-1 / TC-050; pointing VC-3 at that row as well would give it evidence a gate can run. | StR-001-VC-3, spec/tests.md TC-111, TC-050 |
| FND-105 | low | Matrix status lags the concurrently landing implementation: 50 TC ids (TC-001..TC-014, TC-020..TC-033, TC-040..TC-045, TC-047, TC-050..TC-063, TC-111) now carry tracking tags in `tests/`, while every row from TC-020 down still reads `🚧`. The matrix's own rule — "Rows are `🚧` until a tagged test asserts them" — makes the statuses refreshable now; the refresh belongs to the gap-analysis pass, not to this review. | spec/tests.md Test Case Summary, tests/ |
| FND-106 | low | Status markers conform to the archetype pattern `^(✅\|❌\|🚧\|⛔)(\s+.*)?$`: only `✅` and `🚧` appear, each optionally followed by a note. A search across `spec/` finds no `⚠️` in any status cell or anywhere else, so the invalid-marker risk the review brief names is not present. No change. | spec/tests.md |
| FND-107 | low | US-001 carries illustrative examples (US-001-EX-1..3) rather than Given/When/Then acceptance criteria. This follows the `spec-artifacts-iso` US skeleton, which keeps verification out of stories, and the matrix rows them through the FR criteria they lead to. Same disposition as `spec-objects-business` FND-004. No change. | US-001 |
| FND-108 | low | TC ids are allotted in non-contiguous per-FR blocks (TC-015..019, 034..039, 064..069, 077..079, 091..099, 104..109 unused). This is intentional block allocation, matching the reference migration; no duplicate id, no id out of format, no gap that hides a dropped row. No change. | spec/tests.md |
| FND-109 | low | `StR-001-module-activation.md`'s filename slug predates its content: the requirement's title and need are "Tier-2 security + identity objects", and activation is FR-001's subject. Cosmetic only — the id, title and links are consistent — and renaming the file would break the checked-in `spec/stakeholder/index.md` link for no gain. No change. | spec/stakeholder/StR-001-module-activation.md |
| FND-110 | low | FR-002 declares `depends_on` FR-004 while FR-004 names FR-002 as its Build upstream. The pair is mutually referencing by design (FR-004 declares the models, FR-002 emits them) and is not a cycle in the relationship graph, since only FR-002 declares the edge. Recorded so a dependency sweep does not read it as one. No change. | FR-002, FR-004 |

## Coverage Rules

1. **Coverage** — every acceptance criterion, named constraint and NFR metric has ≥ 1 TC, *except* the seven of FND-100. Counted: FR-002 (9 AC + 5 CON), FR-003 (7 AC + 3 CON), FR-004 (14 AC + 2 CON), FR-005 (9 AC + 3 CON), FR-006 (6 AC + 2 CON), NFR-001 (4 AC, one per Measurement metric), IT-002 (6 SC) — all rowed. FR-001-AC-2..4, IT-001-AC-1..2 and StR-001-VC-1..2 are not.
2. **Option permutation** — both Properties forms (typed table, `sysml` fence) at TC-081/TC-090, all 23 object types at TC-050 and TC-080, and the three alternate-form skeletons at TC-081.
3. **Constraint boundary** — item rules tested at both edges: zero versus one identity field (TC-051, TC-058), empty versus one-item `clauses` (TC-055, TC-056, TC-059) and `operations` (TC-057), present versus absent graded row (TC-053, TC-054, TC-059, TC-063), zero defaulted fields (TC-073).
4. **Error path** — every named refusal has a failing fixture or row: digest mismatch and unknown `semantic` key (TC-045), stale schema (TC-028), version-pair skew (TC-024, TC-027), both Properties forms (TC-090), dangling clause ref and non-`Identifier` token (TC-084), embedded `default:` (TC-074), invented vocabulary member (TC-071), empty record (TC-060). The 10 negative fixtures exist in `tests/fixtures/negative/`.
5. **State transition** — availability per declaration kind at TC-083, covering `available` and `not_applicable` only; the rule as written also names `unavailable`, which nothing tests — FND-103.
6. **Edge case** — legacy 0.1.0 artifacts under 0.2.0 (TC-102, TC-103), unresolved type placeholder (TC-061, TC-082), empty record (TC-060), non-populated record keys verified against hand-built records and labelled as such in `## Test Environment`.

## Dispositions

| Finding | Disposition |
|---|---|
| FND-100 | Add Test Case Summary rows for FR-001-AC-2, AC-3, AC-4 and IT-001-AC-1, AC-2 (integration rows, `🚧 needs a running filament-core`) and for StR-001-VC-1 and VC-2 (demonstration rows); retarget the IT-001 and StR-001 rollup cells away from TC-002..TC-006. If any obligation is deliberately unrowed, say so in `## Coverage Gaps` and delete the "every criterion … has a row" sentence — the claim and the table must agree before the matrix is a verification contract. |
| FND-101 | Change FR-001's four Verification cells from `Schema Test`/`Integration Test` to the declared class `Test`, matching FR-002..FR-006 and clearing the `uncatalogued-verification-method` finding. |
| FND-102 | Pick one criterion id scheme for the IT class and apply it to both files (the ISO IT skeleton's per-step `SC` form is the better fit for IT-001's numbered procedure). When the FND-100 rows land, give each IT criterion its own row rather than a range in a Traces To cell. |
| FND-103 | Either add a criterion and row for the `unavailable` availability state (a skeleton whose section the manifest asserts but the document omits), or narrow rule 5 to the two states FR-005-AC-4 asserts. |
| FND-104 | Add TC-050 to the StR-001-VC-3 evidence so the stakeholder criterion has automatable backing beside the manual row. |
| FND-105 | Refresh the Status column against the tracking tags now present in `tests/` as part of the gap-analysis pass; not actioned here, since the implementation is still landing in this worktree. |
| FND-106..FND-110 | Recorded, no change. |

### Round record (2026-09-04)

Applied in the review-fix round: FND-100 (TC-015..TC-019, TC-112 and TC-113 added, and the Coverage Gaps claim corrected to say which rows cannot be discharged and why), FND-101 (FR-001's four cells changed to the declared class `Test`), FND-103 (matrix rule 5 reworded to the two availability states the fixtures produce), FND-105 (every backed row's status refreshed against the tracking tags now in `tests/`).

Recorded without change, and carried into the report rather than silently closed: FND-102, FND-104, FND-106..FND-110.
