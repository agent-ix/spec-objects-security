---
id: SR-20261113181008
title: "Gap analysis of quoin PR 876 against FR-171, FR-172 and NFR-038"
type: SpecReview
analysis: base
scope: "agent-ix/quoin@5afac302; spec/functional/FR-171-security-analysis-emits-typed-controls.md, spec/functional/FR-172-clause-set-sources-and-licence-boundary.md, spec/non-functional/NFR-038-mapping-facts-state-and-never-decide.md, skills/spec-security-analysis/**, tests/fixtures/security-analysis/**, rust/crates/quoin-cli/tests/tc_171_security_analysis_skill.rs, spec/evals.md"
review_set: subset
---

# Gap analysis of quoin PR 876

## Summary

Ticket: PLAT-1427. Planless. Plan completion: not assessed. Each acceptance criterion of FR-171,
FR-172 and NFR-038 was read against the `#[trace]` tags in `tc_171_security_analysis_skill.rs`,
the skill text and the committed fixture. Tools: quoin 0.30.1, quire 0.44.0 (engine 0.59.1).
Companion: agent-ix/spec-objects-security PR 53 at bc6eba15.

Clean: FR-171-AC-1, AC-2, AC-3, AC-4, AC-5, AC-7; FR-171-AC-6 (data resolves; see SR-20261113181007
FND-001 for the test's blind spot); FR-172-AC-5; FR-172-AC-6 for `SKILL.md`. FR-172-AC-1 and AC-2
belong to PLAT-1521/PLAT-1522 and the companion module and were read as context only. NFR-038
constrains `facts-from-mappings` (FR-173, not in this PR); its one hook into the skill, never
assigning an effectiveness, is met by the `not_assessed` default and the "never write `effective`
yourself" rule.

## Verdict

**NOT MERGEABLE AS IS (two high, one medium, one low).** Two Demonstration criteria of FR-172 are bound in
the Test Matrix by tests that exercise neither a skill run nor a licensed pack, so the matrix
reports them covered when nothing demonstrates them.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-172-AC-3 (synthetic pack `example.invalid/std@1` in a temp `IX_HOME`, a skill run maps only its clause ids and states not-mapped for an absent set) is tagged on `a_mapping_to_a_clause_no_installed_set_holds_does_not_resolve`, which only calls the test's own `unresolved` helper on three literal rows, and on `expected_fixture_output_validates_and_every_mapping_resolves`, whose fixture has no pack. No product code, skill run or pack is involved; the test can only fail if the helper changes. Drop the AC-3 tags and add an eval scenario for the pack case, or a demonstration that installs the pack and runs the skill | rust/crates/quoin-cli/tests/tc_171_security_analysis_skill.rs:414-423 |
| FND-002 | high | FR-172-AC-4 (no artifact or reply of the AC-3 run contains the pack's clause-text sentinel) is tagged on `no_expected_artifact_carries_clause_text`, which asserts that Clause cells of the hand-written fixture contain no space. There is no pack, no sentinel and no reply; `mapping_rows` already forces two cells. Drop the tag and cover AC-4 in the same pack demonstration as FND-001 | rust/crates/quoin-cli/tests/tc_171_security_analysis_skill.rs:439-451 |
| FND-003 | medium | The skill is told never to supply the title or summary of a SOC 2 or ISO/IEC 27001 clause, yet step 2 still sends it to `references/iso27001/*.md` and `references/soc2/*.md`, which carry per-control titles and paraphrased descriptions for those licence-restricted sources. A run is primed to repeat them. The files predate this PR, but the new rule makes the conflict live. Needs an owner decision under the licensing boundary: reduce those references to ids, or state why their titles are permitted | skills/spec-security-analysis/SKILL.md:34-35 |
| FND-004 | low | FR-171-AC-5 (`SKILL.md` instructs the gap and no-responsible-party reply) is tagged on `the_review_records_each_gap_as_a_finding`, which reads the hand-written fixture SpecReview, not `SKILL.md`; the `SKILL.md` half is already covered by `skill_text_instructs_the_defaults_the_reply_and_the_set_check`. Drop the tag | rust/crates/quoin-cli/tests/tc_171_security_analysis_skill.rs:425-437 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | high | Round 1 removed the 20 TC-187..TC-203 rows from `spec/tests.md` (TM-001). quire's traceability model binds a trace tag only through a declared matrix row. At 33521a3, `quoin matrix` therefore reports all 17 criteria of FR-014, FR-015 and FR-016 as `untagged`, where they were `tagged` at bc6eba1. `quire matrix` warns `criterion-tagged-outside-row ... This tag does not provide backing` for each one. The new TC-204 and TC-205 have no rows either, so NFR-003-AC-1 and NFR-003-AC-2 stay untagged. Fix: restore the 20 rows and add rows for TC-204 (NFR-003-AC-1) and TC-205 (NFR-003-AC-2), with an NFR-003 summary row. Then confirm with `quoin matrix` that all 19 criteria read `tagged` | spec/tests.md, tests/test_typed_controls.py:326-356 |

## New findings (disposition pass 2)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-004 | low | At 2f18f96, `quoin matrix` reports all 19 FR-014, FR-015, FR-016 and NFR-003 acceptance criteria as `tagged`, and there is no `criterion-tagged-outside-row` warning. The NFR-003 measurement criteria NFR-003-M-1 and NFR-003-M-2 are still `untagged`. The repo binds measurements on the same test as their AC: NFR-002 uses `@pytest.mark.trace("TC-173", ..., "NFR-002-AC-1", "NFR-002-M-1")` at `tests/test_profiles.py:191`, and its TM-001 row lists `NFR-002-M-1..2`. Fix: add `"NFR-003-M-1"` to the TC-204 marker and `"NFR-003-M-2"` to the TC-205 marker, and list `NFR-003-M-1..2` in the NFR-003 summary row | tests/test_typed_controls.py:331, tests/test_typed_controls.py:341, spec/tests.md:148 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | still-open: the tests now exist and pass. TC-204 scans both schemas for the six terms, and TC-205 asserts that the extracted record keys equal the authored sections. But neither has a TM-001 row, so `quoin matrix` still reports NFR-003-AC-1 and NFR-003-AC-2 as `untagged` (see FND-003) | - |
| FND-002 | fixed | Round 1, head 33521a3. TC-195 now extracts the three-column fixture and asserts four things: an `invalid-model-cell` diagnostic with reason `column-unknown` at the header line, no `mappings` key, `recordKeys.mappings` state `unavailable`, and an absent sentinel. FR-015-AC-2 now notes that document validation reports reason `semantic`. The criterion's matrix backing was lost by the row removal (FND-003); the assertions themselves are complete |
| FND-001 | fixed | Round 2, head 2f18f96. TC-204 and TC-205 have TM-001 rows, and `quoin matrix` reports NFR-003-AC-1 and NFR-003-AC-2 as `tagged` |
| FND-003 | fixed | Round 2, head 2f18f96. The TC-187..TC-203 rows are restored, the TC-204 and TC-205 rows and an NFR-003 summary row are added, and the TM-001 frontmatter `covers` FR-014, FR-015, FR-016 and NFR-003. `quoin matrix` reports all 19 acceptance criteria as `tagged`, and `quire matrix` emits no `criterion-tagged-outside-row` warning |
