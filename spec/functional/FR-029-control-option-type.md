---
id: FR-029
title: "A control may state which risk-control option it is"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-025"
    type: depends_on
  - target: "ix://agent-ix/spec-objects-safety/FR-205"
    type: depends_on
---
# FR-029: A control may state which risk-control option it is

## Description

PLAT-1837. A risk-management process asks for risk-control options in priority order: inherently safe design, then protective measures, then information for safety. The security module SHALL let a person state, on a `control`, which of those three options it is. The module SHALL NOT derive the option from a title, safeguard, edge or any other field, SHALL NOT require it, and SHALL NOT rank, score or judge a control by it. A person decides the option; the tool records it.

## Inputs

- A `control` document whose frontmatter may carry `option_type`.
- The `Control` and `ControlFrontmatter` models in `typespec/main.tsp`.

## Outputs

- The closed enum `ControlOptionType`, emitted as `spec_objects_security/schemas/ControlOptionType.json`, with exactly `design`, `protective` and `information`.
- An optional `option_type` key on the `Control` record and on `ControlFrontmatter`.
- A `frontmatter_field` locator on the `control` manifest entry with `required: false`.

## Behavior

- The module SHALL declare `ControlOptionType` as a closed enum whose members are exactly `design`, `protective` and `information`, with no `unknown` or `none` member; a control that states no option leaves the field out.
- `Control` and `ControlFrontmatter` SHALL admit an optional single-valued `option_type` of that enum, with no `default`.
- The `control` manifest entry SHALL extract frontmatter `option_type` with a `frontmatter_field` locator that has `required: false`.
- The module SHALL declare no rule that reads, requires or orders `option_type`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-029-AC-1 | The emitted `ControlOptionType` schema enumerates exactly `design`, `protective`, `information`; `Control` and `ControlFrontmatter` admit `option_type` of it, do not require it and carry no default. | Test |
| FR-029-AC-2 | A `Control` record with each of the three values validates; a record with another value, a list, or an empty string fails; a record without `option_type` validates. | Test |
| FR-029-AC-3 | The `control` manifest entry extracts frontmatter `option_type` with a `frontmatter_field` locator that has `required: false`. | Test |
| FR-029-AC-4 | The manifest declares no `traceability` rule, flow rule or relation that names `option_type`. | Test |

## Dependencies

- **Upstream**: [FR-025](./FR-025-control-safeguards-and-starter-flow-rules.md); `agent-ix/spec-objects-safety` FR-205 (which leaves the option type to this module).
- **Downstream**: none.
