---
id: SR-1623
title: "Gap analysis — FR-010 anomaly origin"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-security; typespec/main.tsp, spec_objects_security/schemas/Anomaly.json, spec_objects_security/schemas/AnomalyOrigin.json, tests/test_soup_record.py, spec/functional/FR-010-soup-record-fields.md, spec/tests.md"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-010
    type: reviews
---
# SR-1623: Gap analysis — FR-010 anomaly origin

## Summary

Ticket: PLAT-1835 (part 1 of 2). PR agent-ix/spec-objects-security#75 at head `ae367fae36386063429272b3c614d1a43df3f1fa`. `quoin matrix --repo . --json` binds FR-010-AC-7 to exactly one test, `test_anomaly_origin_is_a_closed_optional_vocabulary` (tests/test_soup_record.py:210, static_status `tagged`). The new code has an owning requirement: the `AnomalyOrigin` enum and `Anomaly.origin` are covered by the FR-010 Behavior bullets. There are no stubs, skips or coverage-threshold changes in the diff. Two of AC-7's four clauses are not asserted by its bound test.

## Verdict

**CONDITIONAL**: one medium and one low coverage finding. There is no untagged criterion.

## Coverage

Plan completion: not assessed

The matrix computation is quoin's (`quoin matrix --repo . --json`, quoin 0.36.8). FR-010-AC-1..4, AC-6 and AC-7 are all tagged. Mutation probes on the bound test: deleting the `enum` from `AnomalyOrigin.json` fails it, adding a `severity` property to `Anomaly.json` fails it, and adding `"default": "field"` to `AnomalyOrigin.json` leaves it passing. The optional semantic review was not requested and was skipped. No plan was supplied.

Examined requirement units:

- `FR-010-AC-7` (role: examined): An anomaly carrying each of `internal-test`, `field`, `complaint` and `soup-advisory` as `origin` validates; an anomaly with no `origin` validates and emits no `origin` key; an anomaly with any other `origin` fails; the `Anomaly` schema declares no `default` and no severity or acceptability key.
- `FR-010-AC-2` (role: context_only): The precedent for an emission clause: TC-130 is `🚧`, and its emission half is a strict expected failure (`test_an_empty_known_anomalies_is_emitted_and_an_absent_one_is_not`).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-010-AC-7 requires that "an anomaly with no `origin` ... emits no `origin` key", but no test extracts a record. TC-274 only calls `validator.is_valid`, yet `spec/tests.md` marks TC-274 ✅. The repo's own convention for the same engine gap (TC-130 and TC-125: authored frontmatter record keys are not projected into the extracted record) is a `@pytest.mark.xfail(strict=True, reason=ENGINE_PROJECTION)` emission test plus a `🚧` row, which turns red when the engine supplies the projection. Add that strict-xfail emission test, traced TC-274 / FR-010-AC-7, and mark TC-274 `🚧` with the emission half named. Alternatively, drop the emission clause from AC-7. | spec/functional/FR-010-soup-record-fields.md:65, spec/tests.md:270, tests/test_soup_record.py:209-224 |
| FND-002 | low | AC-7's clause "the `Anomaly` schema declares no `default`" is not asserted by its bound test. Adding `"default": "field"` to `AnomalyOrigin.json` leaves TC-274 passing. Only TC-072 (all schemas, traced FR-006-AC-3) and TC-132 (`Anomaly.json` only, traced FR-010-AC-4) would catch it, and neither is traced to AC-7. Add a `"default" not in keywords(...)` assertion over `Anomaly.json` and `AnomalyOrigin.json` to TC-274. | tests/test_soup_record.py:209-224 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1, head `9d159e85e7717997f3044cf8fc164b11c19f91eb`: added `test_an_anomaly_without_origin_emits_no_origin_key`, a strict xfail with `reason=ENGINE_PROJECTION` traced TC-274 / FR-010-AC-7. Under `--runxfail` with quire 0.62.0 it fails with `KeyError: 'known_anomalies'` after a successful extraction, which is the projection gap itself and the same failure as TC-130. In a normal run it reports XFAIL. The TC-274 row is now 🚧 and names the emission half. The xfail would also absorb an unrelated exception, but it follows the repo's existing TC-130 and TC-125 convention. |
| FND-002 | fixed | Round 1: TC-274 now asserts that neither `Anomaly.json` nor `AnomalyOrigin.json` carries a `default` keyword. Mutations confirm it: adding `"default": "field"` to `AnomalyOrigin.json` fails TC-274 at tests/test_soup_record.py:223, and so does a default on `Anomaly.json` `properties.origin`. |
