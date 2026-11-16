---
id: SR-1612
title: Object review — threat_model, threat and risk
type: SpecReview
analysis: base
scope: agent-ix/spec-objects-security; spec/functional/FR-008-security-nfr-needs-mitigation-target.md, spec/functional/FR-026-threat-model-object.md, spec/functional/FR-027-threat-treatment-and-completeness-rules.md, spec/functional/index.md, spec/non-functional/NFR-005-threats-ratings-and-acceptance-are-person-authored.md, spec/non-functional/index.md
review_set: subset
relationships:
- target: ix://agent-ix/spec-objects-security/FR-026
  type: reviews
- target: ix://agent-ix/spec-objects-security/FR-027
  type: reviews
- target: ix://agent-ix/spec-objects-security/NFR-005
  type: reviews
- target: ix://agent-ix/spec-objects-security/FR-008
  type: reviews
---
# SR-1612: Object review — threat_model, threat and risk

## Summary

Ticket: PLAT-1542; PR agent-ix/spec-objects-security#63 at `c8d56c412920158a2b68d4f997e20c2af9f9e72d`. Domain-object completeness for the new `threat_model` and the changed `threat` and `risk`: manifest entry, schemas, skeleton, exports, allowed links, cross-references to sibling-module objects, and agreement with the module-wide object-type contracts in FR-003..FR-006.

Method: `spec-review/spec-object-review`. Frozen head `c8d56c412920158a2b68d4f997e20c2af9f9e72d`.

## Verdict

**FAIL** — FR-026 adds a twenty-sixth object type while FR-003, FR-004, FR-005 and FR-006 still require exactly twenty-five, and FR-026 neither amends them nor lists `threat_model` in `semantic.exports`. The `threat.threatens` widening and `control.mitigates` / `risk.arises_from` links are consistent with the existing manifest.

## Coverage

Examined units:

- `FR-026` (role: examined): a person has analysed for threats, so no rule can ask "was this crossing considered?". The module SHALL add a `threat_model` object type that scopes an analysis to the parts of the model it covers and names the threats it considered.
- `FR-027` (role: examined): For a threat model to mean anything, a threat must be able to target the model's connections, sinks and boundaries; a threat left untreated must be accepted by a named person; and the model must say which covered elements still lack a threat or a treatment. The module SHALL (1) widen `threat.threatens`, (2) add a person's decision to `risk`, and (3) ship three `traceability.flow_rules` that report the gaps.
- `FR-003` (role: context_only): - `semantic.exports` SHALL name all twenty-five object types: `auth_flow`, `permission`, `scope`, `role`, `secret`, `encryption_key`, `session_config`, `data_classification`, `trust_boundary`, `audit_event`, `csrf_token`, `cors_policy`, `password_policy`, `mfa_method`, `jwt_claim`, `threat`, `control`, `risk`, `vulnerability`, `asset`, `attack_surface`, `policy`, `audit_finding`, `soup_record`, `scope_exclusion`.
- `FR-003-AC-1` (role: context_only): The loaded `semantic` block equals the eight admitted keys with the values above, and `exports` equals the twenty-five object-type names.
- `FR-026-AC-1` (role: examined): A `threat_model` with `method: stride_per_element`, `reviewed_by: "A. Person"`, one `covers` edge to a `connection`, one `considers` edge to a `threat` and the three body sections validates with zero errors; so does the skeleton.
- `FR-027-AC-6` (role: examined): A `risk` with `decision: accepted` and no `decided_by`, and one with `decision: accepted` and an empty `decided_by`, fail `quire validate` naming `decided_by`. A `risk` with no `decision` fails. A `risk` with `decision: undecided` and no `decided_by` validates; one with `decision: undecided` and a `decided_by` fails. `decision: maybe` fails. The updated `risk` skeleton validates with zero errors.
- `FR-027-AC-7` (role: examined): The `threat` manifest entry lists `asset`, `attack_surface`, `connection`, `data_sink` and `trust_boundary` in `allowed_links.threatens`; a `threat` that `threatens` each validates without a link diagnostic, and one that `threatens` a `risk` yields a link diagnostic.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | FR-026 adds a twenty-sixth object type, but FR-003 says `semantic.exports` SHALL name exactly the twenty-five listed types (AC-1, AC-4), and FR-004, FR-005 and FR-006 bind their schema, skeleton and no-default contracts to 'the twenty-five'. FR-026 does not amend them, add `threat_model` to the exports, or say whether it is under FR-004 and FR-006, so an implementation must break FR-003-AC-1 or leave `threat_model` unexported. | spec/functional/FR-026-threat-model-object.md:45-52 | missing-requirement |
| FND-002 | low | FR-027 requires `decided_by` when `decision` is accepted or not_accepted and forbids it when undecided, but it does not say which artifact enforces this: the `Risk.json` record schema, the open `RiskFrontmatter.json`, or a manifest locator. A locator's `required` flag cannot express the condition, and an open schema implies no constraint. | spec/functional/FR-027-threat-treatment-and-completeness-rules.md:72-80 | wrong-requirement |

## Dispositions

Round 1, after fix commit `7b2a707c74423739330d19e35a7811d3912cab75`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | - |
| FND-002 | fixed | - |

After excerpts (round 1, verbatim):

- FND-001:

```text
- `threat_model` is the twenty-sixth object type. `semantic.exports` SHALL name it ([FR-003](./FR-003-semantic-manifest-contract.md)), and it is one of the twenty-six types covered by the schema, skeleton and no-default contracts of [FR-004](./FR-004-role-schemas.md), [FR-005](./FR-005-executable-skeletons.md) and [FR-006](./FR-006-security-safe-declarations.md). / FR-003: `semantic.exports` SHALL name all twenty-six object types: ... `scope_exclusion`, `threat_model`.
```

- FND-002:

```text
- The conditional rule is enforced by the `Risk.json` record schema, as `if`/`then`/`else` over `decision` (`then`: `decided_by` required and non-empty; `else`: `decided_by` forbidden). `RiskFrontmatter.json` is open and constrains only the `decision` enum; a manifest locator's `required` flag cannot express the condition and is not used for it.
```
