---
id: SR-1622
title: "Code review — FR-010 anomaly origin"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-security; typespec/main.tsp, spec_objects_security/schemas/Anomaly.json, spec_objects_security/schemas/AnomalyOrigin.json, tests/test_soup_record.py, spec/functional/FR-010-soup-record-fields.md, spec/tests.md"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-010
    type: reviews
---
# SR-1622: Code review — FR-010 anomaly origin

## Summary

Ticket: PLAT-1835 (part 1 of 2; the incident and maintenance-plan half is the sibling PR in spec-objects-operational, reviewed separately). PR agent-ix/spec-objects-security#75 at head `ae367fae36386063429272b3c614d1a43df3f1fa`, scoped to `git diff origin/main...HEAD` (6 files, +50).

The change adds an optional `origin?: AnomalyOrigin` on the `Anomaly` model and a new closed enum `AnomalyOrigin` (`internal-test`, `field`, `complaint`, `soup-advisory`). `Anomaly` keeps `...Record<never>`, so no severity, score or acceptability key is admitted. The emitted JSON matches the TypeSpec source: `node scripts/generate-schemas.mjs --check` reports "70 schema(s) match the committed output". There is no `default` keyword, no compatibility layer, and no pinned issue id, SHA or count. No standard text is quoted. The PR body cites ISO 14971 clause 10 by number only.

## Verdict

**CONDITIONAL**: two low spec-consistency findings. The schema and TypeSpec change is correct.

## Assurance Context

No applicable AssuranceProfile document exists in the repository.

## Coverage

Review set: subset. Examined: the TypeSpec enum and model change, both emitted schemas, the new test `test_anomaly_origin_is_a_closed_optional_vocabulary` (TC-274), the FR-010 Behavior and AC edits, and the `spec/tests.md` rows. Focused tests ran in a detached worktree of the PR head, with semantic-core 0.4.4 from `npm ci`: TC-274, TC-129, TC-130, TC-132, TC-144 and TC-072 passed. `test_an_authored_document_with_an_invented_support_status_fails` failed because the local quire wheel rejects the manifest's `flow_rules` key. That is an environment version skew, it is unrelated to this diff, and it was not attributed to the PR. Mutation probes on TC-274: removing the `enum` from `AnomalyOrigin.json` fails it, and adding a `severity` property to `Anomaly.json` fails it. No Rust or React files are in the diff.

Examined requirement units:

- `FR-010-AC-7` (role: examined): An anomaly carrying each of `internal-test`, `field`, `complaint` and `soup-advisory` as `origin` validates; an anomaly with no `origin` validates and emits no `origin` key; an anomaly with any other `origin` fails; the `Anomaly` schema declares no `default` and no severity or acceptability key.
- `FR-010` (role: context_only): Behavior bullets added for the `AnomalyOrigin` vocabulary, absent-means-not-stated, and no severity or acceptability key.
- `FR-006` (role: context_only): "Ten closed enum schemas" and the unassessed-member rule for graded vocabularies.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | FR-010 Description and Outputs still name only `SoupSupportStatus` as the vocabulary FR-010 owns and as "not one of the ten vocabularies counted by FR-006". `AnomalyOrigin` is a new closed enum schema with no unassessed member. Read against FR-006 ("Ten closed enum schemas"; every graded value has an explicit unassessed member), a reader cannot tell that it is a deliberately ungraded, FR-010-owned vocabulary where absence means not stated. Add `AnomalyOrigin` to the Description sentence and the Outputs bullet. | spec/functional/FR-010-soup-record-fields.md:24-34 |
| FND-002 | low | The `spec/tests.md` coverage summary row for FR-010 still reads `FR-010-AC-1..4, FR-010-AC-6, FR-010-CON-1 \| TC-129..TC-132, TC-134`, so it omits FR-010-AC-7 and TC-274, which this PR added a few lines below. Update the row, or delete the hand-kept summary row in favour of the computed matrix. | spec/tests.md:141 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1, head `9d159e85e7717997f3044cf8fc164b11c19f91eb`: the FR-010 Description now names `SoupSupportStatus` and `AnomalyOrigin` as owned by FR-010 and outside FR-006's ten, and states that `AnomalyOrigin` is deliberately ungraded with absence meaning not stated. The Outputs bullet names both vocabularies. `quire validate` with explicit `--module` roots (process, iso, security, architecture) exits 0 on FR-010 and `spec/tests.md`, and a section-rename mutation of FR-010 exits 3. |
| FND-002 | fixed | Round 1: the `spec/tests.md` FR-010 summary row now lists `FR-010-AC-7` and `TC-274`. |
