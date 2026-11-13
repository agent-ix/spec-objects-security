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

The key is `responsible` and not `owner`, because `owner` is a key the engine's record-sections mapping never reads (it is a systems member of `agent-ix/quire-rs` FR-075).

The authored form has sections with one inline-code value: `## Set`, `## Clause`, `## Responsible`, `## Rationale`,
`## Decision`, `## Owner` and `## Approval reference`. The last three are an explicit human-authored decision and its
owner and approval reference; Quire validates their shape, not whether the reference actually approves the decision.
Quire reads each into the record key of the same name through the `record-sections` mapping (`agent-ix/quire-rs` FR-081), the
same mapping as [FR-014](./FR-014-control-mappings-are-clause-references.md). The mapping does not read frontmatter, so no
key is authored there. The frontmatter carries `id`, `title`, `type` and `object`, as every skeleton does.

## Behavior

- The `scope_exclusion` record schema SHALL require `set`, `clause`, `responsible`, `rationale`, `decision`, `owner` and `approval_ref`.
- `responsible` SHALL be a `SemanticId` naming the component, service or document that is responsible for the clause.
- The `responsible` value SHALL name the bare id of an artifact in the same bundle, for example `COMP-001`, which is the form Quire resolves with a bundle package.
- A `responsible` written as a cross-repository id such as `ix://agent-ix/example-platform/COMP-001` is refused by Quire as not a bundle artifact id when a bundle package is supplied, so this module does not admit it; a party outside the repository is named by an artifact in this bundle that stands for it.
- `rationale` SHALL be a non-empty string.
- `decision` SHALL be exactly one of `delegated`, `accepted_risk` or `temporary_exception`.
- `owner` SHALL be a non-empty `SemanticId` naming the person or authority accountable for the decision.
- `approval_ref` SHALL be a non-empty string identifying the approval record. It SHALL NOT itself be treated as proof of approval.
- A `temporary_exception` SHALL have a non-empty expiry value.
- `delegated` and `accepted_risk` SHALL NOT carry an expiry value.
- The expiry is an authored limit on the proposed disposition. FR-173 requires and enforces the FR-046 attestation validity interval.
- The `scope_exclusion` schema SHALL reject every property outside its seven and declare no approval-status or score property.
- The module SHALL export `scope_exclusion` and ship a skeleton that validates.
- The manifest entry for `scope_exclusion` SHALL require each of the seven authored sections, with a `section_body` locator.
- An authored exclusion with no `## Responsible` section SHALL fail validation with `semantic.record-invalid` naming `responsible`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-016-AC-1 | `ScopeExclusion.json` requires exactly `set`, `clause`, `responsible`, `rationale`, `decision`, `owner`, `approval_ref` and optional `expires_at`, is sealed, and `scope_exclusion` appears in the manifest `exports`. | Test |
| FR-016-AC-2 | A record without `responsible`, `owner` or `approval_ref`, with either identifier not a `SemanticId`, or with empty `rationale` or `approval_ref` fails validation. | Test |
| FR-016-AC-3 | Each of `delegated`, `accepted_risk` and `temporary_exception` is accepted as `decision`; any other value is rejected. `temporary_exception` without `expires_at` and either other value with `expires_at` are rejected. | Test |
| FR-016-AC-4 | The `scope_exclusion` skeleton validates with no `semantic.record-invalid` and has no placeholder token; removing any required section makes it fail naming the corresponding key. | Test |
| FR-016-AC-7 | With a bundle package supplied, a fixture whose `## Responsible` is the bare id of a bundle artifact validates, and one whose `## Responsible` is `ix://agent-ix/example-platform/COMP-001` fails with `not a bundle artifact id`. | Test |
| FR-016-AC-5 | The empty record `{}` fails `ScopeExclusion.json`. | Test |
| FR-016-AC-6 | The manifest entry for `scope_exclusion` declares a required `section_body` locator for each required authored heading. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-role-schemas.md), [FR-005](./FR-005-executable-skeletons.md), [FR-014](./FR-014-control-mappings-are-clause-references.md); `agent-ix/quire-rs` FR-081
- **Downstream**: `agent-ix/quoin` FR-173
