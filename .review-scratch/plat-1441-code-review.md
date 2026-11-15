---
id: SR-1607
title: "Code review — PLAT-1441 regulated-data categories on data_classification"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-security; typespec/main.tsp, spec_objects_security/manifest.yaml, spec_objects_security/schemas/DataClassification.json, spec_objects_security/schemas/RegulatedDataCategory.json, spec_objects_security/skeletons/data_classification.md, tests/test_regulated_categories.py, tests/fixtures/regulated-categories/"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-023
    type: reviews
  - target: ix://agent-ix/spec-objects-security/NFR-004
    type: reviews
---
# SR-1607: Code review — PLAT-1441 regulated-data categories on data_classification

## Summary

Ticket: PLAT-1441. PR agent-ix/spec-objects-security#62 (draft) at head `4702982a697c35513fb35673031774249aafdc62`, diff `origin/main...HEAD`, 17 files. No Rust in the diff, so rust-review did not run.

Focused checks:

- `make schemas-check`: 56 schemas match the committed output.
- `tests/test_regulated_categories.py` on the pinned quire 0.58.0: 13 passed, 11 failed. The failures are expected until the engine ships.
- The same file on a local wheel built from the quire-rs#690 head (`plat-1441-quire-rs-runtime`, built with `maturin build --release` and loaded through `PYTHONPATH`; the repo venv was not changed): 17 passed, 7 failed. The 4 invalid-fixture tests (TC-RC-10) now pass. The 7 remaining failures come from the test code, not from the missing release (FND-001 to FND-003).
- A probe that passes the object type's `bodyExtraction` and the module's `mappings` to `extract_semantic` on the #690 wheel gives the behaviour the spec requires: `regulatedCategories: ["health","personal"]`; no `record` for `absent.md`; an error with reason `frontmatter-owned` for `section-only.md`; and a warning with reason `frontmatter-owned` for `section-and-frontmatter.md`, with `regulatedCategories: ["health"]`.

The TypeSpec enum and property, the emitted schemas, the manifest locator and the skeleton all match FR-023 and NFR-004. The manifest locator is enough for #690 to treat the key as frontmatter-owned, because ownership comes from the `frontmatter_field` locator.

## Verdict

**CHANGES REQUESTED.** The module-side implementation is correct. The engine tests in `tests/test_regulated_categories.py` will still fail after quire-rs#690 is released, for three reasons in the tests themselves. Releasing quire-rs#690 is a real dependency, but it does not make this PR's tests pass by itself.

Examined units (role: examined): FR-023-AC-1 to AC-10, NFR-004-AC-1 to AC-3, the `RegulatedDataCategory` enum and the `DataClassification.regulatedCategories` property in `typespec/main.tsp`, the `data_classification` manifest locator, the skeleton, and the 11 fixtures.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | `_extract` passes no `bodyExtraction` and no `module.mappings`, so the engine never treats `regulatedCategories` as frontmatter-owned. On the #690 engine the record holds `regulated_categories` and no section diagnostic is raised, so TC-RC-08, TC-RC-11 and TC-RC-12 keep failing after the release | tests/test_regulated_categories.py:54 |
| FND-002 | high | TC-RC-09 and TC-RC-11 index `result["record"]`, but the engine leaves `record` out when no key is extracted, so they raise `KeyError: 'record'` on every engine | tests/test_regulated_categories.py:172 |
| FND-003 | medium | TC-RC-11 and TC-RC-12 look for `frontmatter-owned` in the `validate_document` message text. The #690 engine reports that message as `reason: semantic` without the reason token, so both tests fail even though the right diagnostic is raised. The reason is exposed on the `extract_semantic` diagnostics | tests/test_regulated_categories.py:202 |
| FND-004 | low | TC-RC-10's `needle` is `"regulated"` for the empty, duplicate and scalar cases, which repeats the assertion just before it and checks nothing extra | tests/test_regulated_categories.py:191 |
