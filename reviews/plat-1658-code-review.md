---
id: SR-1620
title: "code-review review — PLAT-1658 spec-objects-security"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-security; typespec/main.tsp; spec_objects_security/manifest.yaml; spec_objects_security/schemas/ProcessingActivity*.json; tests/test_processing_activity.py; tests/test_regulated_categories.py"
review_set: subset
---

## Summary

Reviewed the ProcessingActivity schemas, manifest relation, skeleton and tests against FR-028. The required-coverage rule is advisory, so an activity without a covers edge still exits validation successfully; the record schema also permits a controller role to carry a controller list contrary to the role contract.

## Verdict

**FAIL** — one high-severity requirement mismatch and one schema contract defect remain.

## Scope

- Examined: FR-028-AC-1 through FR-028-AC-8; ProcessingActivity TypeSpec and generated schemas; manifest relation; skeleton; new focused tests and the regulated-category test adjustment.
- Ticket: PLAT-1658; PR #69; reviewed published head `84b182f01a6db11c1c72c42f4b94442afe365268`.
- Applicable AssuranceProfile: none found under `spec/`.
- Checks: schema drift passed (67 schemas match); focused tests had 19 passed and 13 failed in pre-existing `test_regulated_categories.py` cases because the activated Python Quire wheel rejects baseline `where` fields in `manifest.yaml`; Ruff and Black passed. The ProcessingActivity-focused test file passed; the combined focused run had 19 passes and 13 pre-existing regulated-category failures because the activated Python Quire wheel rejects baseline `where` fields in `manifest.yaml`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The required `covers` relation only emits an advisory warning: a valid-looking processing activity with no covers edge produces `processing-activity-covers-nothing` but `quire validate --okf` exits 0, violating the explicit fail behavior in AC-5. The new tests check declaration shape and only a valid edge, never a no-edge failure. | spec/functional/FR-028-processing-activity.md:61; spec_objects_security/manifest.yaml:844-851; tests/test_processing_activity.py:69-87,98-123 |
| FND-002 | medium | `ProcessingActivity.json` allows `controller` to be a string or array at the base schema, while its controller-role conditional only adds required fields and never narrows that property to a string. A controller record with a controller list therefore validates, although FR-028 requires one name-and-contact string; the frontmatter schema correctly narrows it, so the published record schema disagrees. | spec/functional/FR-028-processing-activity.md:35; spec_objects_security/schemas/ProcessingActivity.json:9-20,72-90; spec_objects_security/schemas/ProcessingActivityFrontmatter.json:98-109 |

## Evidence

For FND-001, running Quire CLI 0.46.0 / engine 0.61.0 against a bundle containing an activity with no `covers` edge returned exit 0 and emitted: `warning: ... 'PA-EMPTY' has no 'covers' edge to any connection/data_sink/part ... [processing-activity-covers-nothing]`. Quire FR-058-AC-7 and `quire-rs/src/corpus/required_relations.rs` route required-relation findings at grammar severity, advisory by default. The PR test only asserts that the manifest declares `covers`; its bundle test exercises only a positive connection edge.

For FND-002, Draft 2020-12 schema inspection shows `controller` has an `anyOf` string/array at the top level, while the controller conditional requires only `purposes`, `data_subject_categories`, and `retention`. The corresponding controller conditional in `ProcessingActivityFrontmatter.json` explicitly sets `controller.type: string`; that restriction is absent from the record schema.

## Examined Units

- `FR-028-AC-1` (examined): “A controller activity with controller details, purposes, data-subject categories, retention, home regions and a valid `covers` edge validates.”
- `FR-028-AC-2` (examined): “A processor activity with a processor name and contact, a non-empty controller list and home regions validates without `purposes`, `data_subject_categories` or `retention`.”
- `FR-028-AC-3` (examined): “A controller activity without `retention`, `purposes` or `data_subject_categories`, and a processor activity without its own `processor` identity/contact or with an empty controller list, each fail with a diagnostic naming the missing or invalid field.”
- `FR-028-AC-4` (examined): “An unknown role, an empty home-region list, or a home-region value outside the stated vocabulary fails validation.”
- `FR-028-AC-5` (examined): “A `processing_activity` with no `covers` edge fails validation; an edge to a `connection`, `data_sink` or `part` validates.”
- `FR-028-AC-6` (examined): “A `covers` edge to a `queue` fails with a wrong-kind diagnostic, and an edge to an absent target fails with a dangling-target diagnostic.”
- `FR-028-AC-7` (examined): “The module exports `processing_activity`; its generated schema and skeleton pass the module schema-drift and `quire validate` checks.”
- `FR-028-AC-8` (examined): “Omitting any optional authored field leaves it absent in the extracted record; no omitted value is populated from another field, artifact, code or runtime source.”


## Dispositions

Round 1, published head 7e27cf4934f5c0e6dfc5dde0f7adfcd6c87d66b3.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | FR-028 and AC-5 now specify the located advisory warning and the warning's non-failing effect, matching the generic required-relation behavior. The test asserts the warning's location, declared check, and message; a direct run of the same fixture returned 0. |
| FND-002 | fixed | The controller-role branch of `ProcessingActivity.json` now applies the `NonBlankText` schema to `controller`, rejecting an array in the controller role while the processor role still accepts its list. `node scripts/generate-schemas.mjs --check` reports 67 schemas match. |

Round-1 verification note: `tests/test_processing_activity.py` yielded 9 passed, 1 failed after npm dependencies were installed. The remaining extraction assertion used the globally installed Python Quire 0.53.0, while the repository requires `quire >=0.61.0`; it returned an empty record for the processor fixture. The rest of the focused tests ran against npm quire-cli 0.46.0 / engine 0.61.0.
