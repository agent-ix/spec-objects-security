---
id: SR-1623
title: "Gap analysis — FR-029 optional control option type"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-security; spec/functional/FR-029-control-option-type.md, tests/test_control_option_type.py, spec_objects_security/manifest.yaml, typespec/main.tsp, spec_objects_security/schemas/ControlOptionType.json, spec_objects_security/schemas/Control.json, spec_objects_security/schemas/ControlFrontmatter.json"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-029
    type: reviews
---
# SR-1623: Gap analysis — FR-029 optional control option type

## Summary

Ticket: PLAT-1837 (part 2); PR agent-ix/spec-objects-security#76 at head `5f4abbc85c8727c5ae429c3a24c9601387d83519`.

## Verdict

**PASS with one low finding.** Every FR-029 criterion is tagged and each tagged test can fail.

## Coverage

Plan completion: not assessed.

`quire matrix --scope <worktree>` binds FR-029-AC-1..4 to `tests/test_control_option_type.py` (lines 19, 35, 55, 67), all `tagged`. The `requirement-without-design` note on these rows is repository-wide (244 rows) and not attributed to this PR. All four tests pass. Each can fail: AC-1 on an added enum member, a `default` or a `required` entry; AC-2 on an accepted wrong value, list, empty string or `null`; AC-3 on a changed locator; AC-4 on a `traceability` entry naming `option_type`. No production code in the diff lacks an owning requirement; no stubs, skips or coverage-threshold changes.

Observation outside this PR: with quire 0.52.0 (engine 0.62.2), `quire validate --okf` over a control document whose frontmatter has `option_type: shield` or `option_type: [design]` exits 0 with no finding. The same is true on `origin/main` for `safeguards: [bogus-value]`, so the engine does not enforce this module's frontmatter schema at authoring time. That is pre-existing and not attributed to this PR.

Examined units:

- `FR-029-AC-1` (role: examined): The emitted `ControlOptionType` schema enumerates exactly `design`, `protective`, `information`; `Control` and `ControlFrontmatter` admit `option_type` of it, do not require it and carry no default.
- `FR-029-AC-2` (role: examined): A `Control` record with each of the three values validates; a record with another value, a list, or an empty string fails; a record without `option_type` validates.
- `FR-029-AC-3` (role: examined): The `control` manifest entry extracts frontmatter `option_type` with a `frontmatter_field` locator that has `required: false`.
- `FR-029-AC-4` (role: examined): The manifest declares no `traceability` rule, flow rule or relation that names `option_type`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The FR-029-AC-4 test scans only the `traceability` block. A relation that names `option_type` in the top-level `edge_types`, an object type's `allowed_links`, `grammar_severity` or `lint_rules` would still pass, although the AC and FR-029 forbid any relation or rule that reads it | tests/test_control_option_type.py:66-70 |
