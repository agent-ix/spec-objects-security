---
id: SR-1622
title: "Code review — FR-029 optional control option type"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-security; typespec/main.tsp, spec_objects_security/schemas/ControlOptionType.json, spec_objects_security/schemas/Control.json, spec_objects_security/schemas/ControlFrontmatter.json, spec_objects_security/manifest.yaml, spec/functional/FR-029-control-option-type.md, spec/functional/index.md, tests/test_control_option_type.py"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-029
    type: reviews
---
# SR-1622: Code review — FR-029 optional control option type

## Summary

Ticket: PLAT-1837 (part 2); PR agent-ix/spec-objects-security#76 at head `5f4abbc85c8727c5ae429c3a24c9601387d83519`, scoped to `git diff origin/main...HEAD`.

The PR adds a closed `ControlOptionType` enum (`design`, `protective`, `information`) in TypeSpec, an optional `option_type` on `Control` and `ControlFrontmatter`, a `frontmatter_field` locator with `required: false` on the `control` manifest entry, FR-029 and four tagged tests.

Measured: `node scripts/generate-schemas.mjs --check` after `npm ci` reports all 70 schemas match the committed output, so TypeSpec and the regenerated schemas agree. The enum has no `unknown`/`none` member and no `default` in TypeSpec or either schema; `option_type` is absent from every `required` list. No `traceability` rule, flow rule, required relation, edge type or allowed link names `option_type`. `tests/__init__.py` is absent at the tip. `tests/test_control_option_type.py` passes (4/4). The failure in `tests/test_control_safeguards.py` (1 with `node_modules` present, 3 without) is identical on `origin/main`. No issue-id, SHA or count pins in the tests. `quire validate` on FR-029 and the index exits 0 with one `ears:non-singular` warning.

Examined units:

- `FR-029` (role: examined): A control may state which risk-control option it is; the module SHALL NOT derive, require, rank, score or judge a control by it.
- `FR-029-AC-1` (role: examined): The emitted `ControlOptionType` schema enumerates exactly `design`, `protective`, `information`; `Control` and `ControlFrontmatter` admit `option_type` of it, do not require it and carry no default.
- `FR-029-AC-2` (role: examined): A `Control` record with each of the three values validates; a record with another value, a list, or an empty string fails; a record without `option_type` validates.
- `FR-029-AC-3` (role: examined): The `control` manifest entry extracts frontmatter `option_type` with a `frontmatter_field` locator that has `required: false`.
- `FR-029-AC-4` (role: examined): The manifest declares no `traceability` rule, flow rule or relation that names `option_type`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | FR-029 Description opens with the ticket id `PLAT-1837.` and packs four SHALL/SHALL NOT clauses into one paragraph that the Behavior bullets already state; quire reports `ears:non-singular` at line 15 | spec/functional/FR-029-control-option-type.md:15 |
| FND-002 | low | The control authoring skeleton's contract comment lists the optional `safeguards` key but not the new optional `option_type`, so an author reading the skeleton cannot find the field | spec_objects_security/skeletons/control.md:7-11 |

## Verdict

**PASS with low findings.** The enum is closed and optional, carries no default, no rule reads, requires or orders it, and the TypeSpec and generated schemas agree. Both findings are wording or discoverability nits with no wrong behaviour; the PR is mergeable once the fix round addresses or dispositions them.
