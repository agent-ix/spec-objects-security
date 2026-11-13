---
id: FR-016
title: "A scope_exclusion states that a clause is outside a component, with a responsible party"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-014"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-005"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-081"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-040"
    type: "depends_on"
---
# FR-016: A scope_exclusion states that a clause is outside a component, with a responsible party

## Description

A clause that is outside the component's boundary was a prose row in a table with a responsible component named in
free text, which a reader could leave blank. The module SHALL add a `scope_exclusion` object type that states it as a
record whose responsible party is required.

The `scope_exclusion` declares a boundary and carries a person's proposed out-of-scope disposition metadata. Those
fields do not approve the exclusion. Quoin emits a disposition fact only when a person separately supplies the
FR-046 attestation naming the actor, authority and validity interval; the fact retains the approval reference as
evidence of that authorization (see `agent-ix/quoin` FR-173).

The type is the twenty-fifth object type of the module, so the counts of
[FR-003](./FR-003-semantic-manifest-contract.md) through [FR-006](./FR-006-security-safe-declarations.md) include it: it has a
role-schema row in [FR-004](./FR-004-role-schemas.md), a skeleton under [FR-005](./FR-005-executable-skeletons.md) and the
no-default rule of FR-006.

The key is `responsible` for the component, service or document accountable for the clause, and `decision_owner` for the person or authority accountable for the proposed disposition. The key `owner` is reserved by the engine's systems mapping and cannot be populated from a section (agent-ix/quire-rs FR-075/FR-081). Quoin FR-173 maps the extracted `decision_owner` to the discharge fact's `owner`; it does not conflate either value with `responsible`.

The authored form has one inline-code value under each required heading: `## Set`, `## Clause`, `## Responsible`,
`## Rationale`, `## Decision`, `## Decision owner` and `## Approval ref`. `## Expires at` is an additional inline-code
value required only for `temporary_exception`. The headings normalize to their record keys (`decision_owner`,
`approval_ref`, and `expires_at`) under `record-sections` (agent-ix/quire-rs FR-081); the `Owner` heading is intentionally
not used. The decision, owner and approval reference are explicit human-authored proposed disposition metadata; Quire
validates their shape, not whether the reference actually approves the decision. The mapping does not read frontmatter,
so no record key is authored there. The frontmatter carries `id`, `title`, `type` and `object`, as every skeleton does.

## Behavior

- The `scope_exclusion` record schema SHALL require `set`, `clause`, `responsible`, `rationale`, `decision`, `decision_owner` and `approval_ref`.
- The sealed `scope_exclusion` schema SHALL additionally permit the optional `expires_at` property; no property outside these eight keys is admitted.
- `responsible` SHALL be a `SemanticId` naming the component, service or document that is responsible for the clause.
- The `responsible` value SHALL name the bare id of an artifact in the same bundle, for example `COMP-001`, which is the form Quire resolves with a bundle package.
- A `responsible` written as a cross-repository id such as `ix://agent-ix/example-platform/COMP-001` is refused by Quire as not a bundle artifact id when a bundle package is supplied, so this module does not admit it; a party outside the repository is named by an artifact in this bundle that stands for it.
- `rationale` SHALL be a non-empty string.
- `decision` SHALL be exactly one of `delegated`, `accepted_risk` or `temporary_exception`.
- `decision_owner` SHALL be a non-empty `SemanticId` naming the person or authority accountable for the decision.
- The `decision_owner` value SHALL name the bare id of an artifact in the same bundle that represents that person or authority.
- `decision_owner` SHALL remain distinct from `responsible`.
- `approval_ref` SHALL be a non-empty string identifying the approval record.
- `approval_ref` SHALL NOT itself be treated as proof of approval.
- `expires_at` SHALL be a string containing an RFC 3339 date-time instant with an explicit UTC designator or numeric UTC offset, using the instant comparison contract of Quoin FR-040.
- The schema SHALL declare `expires_at` as a `string` with `format: date-time` and enforce the format during record validation.
- A `temporary_exception` SHALL have a valid `expires_at`.
- `delegated` and `accepted_risk` SHALL NOT carry `expires_at`.
- An empty `expires_at`, a non-RFC-3339 value such as `tomorrow`, or a date-time with no timezone SHALL fail record validation.
- The expiry is an authored limit on the proposed disposition. Quoin FR-173 requires and enforces that it is no later than the FR-046 attestation's `expiresAt`.
- The `scope_exclusion` schema SHALL reject every property outside the seven required properties and optional `expires_at`.
- The `scope_exclusion` schema SHALL declare no approval-status or score property.
- The module SHALL export `scope_exclusion` and ship a skeleton that validates.
- The manifest entry for `scope_exclusion` SHALL require `section_body` locators for the seven required headings and a `required: false` `section_body` locator for `## Expires at`.
- An authored exclusion with no `## Responsible` section SHALL fail validation with `semantic.record-invalid` naming `responsible`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-016-AC-1 | `ScopeExclusion.json` requires exactly `set`, `clause`, `responsible`, `rationale`, `decision`, `decision_owner` and `approval_ref`, permits optional `expires_at`, rejects every other key, and `scope_exclusion` appears in the manifest `exports`. | Test |
| FR-016-AC-2 | A record without `responsible`, `decision_owner` or `approval_ref`, with either identifier not a `SemanticId`, or with empty `rationale` or `approval_ref` fails validation. | Test |
| FR-016-AC-3 | Each of `delegated`, `accepted_risk` and `temporary_exception` is accepted as `decision`; any other value is rejected. `temporary_exception` without `expires_at` and either other value with `expires_at` are rejected. | Test |
| FR-016-AC-4 | The `scope_exclusion` skeleton validates with no `semantic.record-invalid` and has no placeholder token; removing any required section makes it fail naming the corresponding key. | Test |
| FR-016-AC-7 | With a bundle package supplied, a fixture whose `## Responsible` is the bare id of a bundle artifact validates, and one whose `## Responsible` is `ix://agent-ix/example-platform/COMP-001` fails with `not a bundle artifact id`. | Test |
| FR-016-AC-5 | The empty record `{}` fails `ScopeExclusion.json`. | Test |
| FR-016-AC-6 | The manifest entry declares a required `section_body` locator for each required heading and an optional locator for `## Expires at`. | Test |
| FR-016-AC-8 | The authored fixture `tests/fixtures/positive/scope-exclusion-temporary-exception.md`, validated with bundle artifacts `COMP-001` and `SEC-OWNER-001`, has `example.invalid/std@1`, `EX-1`, `COMP-001`, `The deployment platform owns this clause for every service it hosts.`, `temporary_exception`, `SEC-OWNER-001`, `APPROVAL-001` and `2026-11-14T12:00:00Z` under headings `Set`, `Clause`, `Responsible`, `Rationale`, `Decision`, `Decision owner`, `Approval ref` and `Expires at`; it validates and extraction yields `decision_owner`, `approval_ref` and `expires_at`, without producing an `owner` key from those sections. | Test |
| FR-016-AC-9 | An expiry `2026-11-14T12:00:00Z` validates, while empty expiry, `tomorrow`, and `2026-11-14T12:00:00` fail validation; an explicit numeric UTC offset is also accepted. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-role-schemas.md), [FR-005](./FR-005-executable-skeletons.md), [FR-014](./FR-014-control-mappings-are-clause-references.md); `agent-ix/quire-rs` FR-081; `agent-ix/quoin` FR-040
- **Downstream**: `agent-ix/quoin` FR-173
