---
id: FR-016
title: "A scope_exclusion states that a clause is outside a component, with an owner"
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
# FR-016: A scope_exclusion states that a clause is outside a component, with an owner

## Description

A clause that is outside the component's boundary was a prose row in a table with a responsible component named in
free text, which a reader could leave blank. The module SHALL add a `scope_exclusion` object type that states it as a
record whose owner is required.

The `scope_exclusion` is a declaration of boundary. It is not an approval: the approval of the exclusion, with an
actor, an authority and an expiry, is the `delegated` disposition fact of `agent-ix/quoin` FR-046, recorded by a
person (see `agent-ix/quoin` FR-173).

The type is the twenty-fifth object type of the module, so the counts of
[FR-003](./FR-003-semantic-manifest-contract.md) through [FR-006](./FR-006-security-safe-declarations.md) include it: it has a
role-schema row in [FR-004](./FR-004-role-schemas.md), a skeleton under [FR-005](./FR-005-executable-skeletons.md) and the
no-default rule of FR-006.

The authored form is four sections, each with one inline-code value: `## Set`, `## Clause`, `## Owner` and `## Rationale`.
Quire reads each into the record key of the same name through the `record-sections` mapping (`agent-ix/quire-rs` FR-081), the
same mapping as [FR-014](./FR-014-control-mappings-are-clause-references.md). The mapping does not read frontmatter, so no
key is authored there. The frontmatter carries `id`, `title`, `type` and `object`, as every skeleton does.

## Behavior

- The `scope_exclusion` record schema SHALL require `set` and `clause` (the shape of FR-014), `owner` and `rationale`.
- `owner` SHALL be a `SemanticId` naming the component, service or document that is responsible for the clause.
- `rationale` SHALL be a non-empty string.
- The `scope_exclusion` schema SHALL reject every property outside its four and declare no decision, status, score or approval property.
- The module SHALL export `scope_exclusion` and ship a skeleton that validates.
- The manifest entry for `scope_exclusion` SHALL require the sections `## Set`, `## Clause`, `## Owner` and `## Rationale`, each with a `section_body` locator.
- An authored exclusion with no `## Owner` section SHALL fail validation, because the extracted record has no `owner`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-016-AC-1 | `ScopeExclusion.json` requires exactly `set`, `clause`, `owner` and `rationale`, is sealed, and `scope_exclusion` appears in the manifest `exports`. | Test |
| FR-016-AC-2 | A record without `owner`, with an `owner` that is a bare token, or with an empty `rationale` fails validation. An authored fixture with no `## Owner` section fails validation. | Test |
| FR-016-AC-3 | A record with `decision`, `status` or `approved_by` fails validation. | Test |
| FR-016-AC-4 | The `scope_exclusion` skeleton validates with no placeholder token, and `quire extract` over it yields the four keys from its four sections. | Test |
| FR-016-AC-5 | The empty record `{}` fails `ScopeExclusion.json`. | Test |
| FR-016-AC-6 | The manifest entry for `scope_exclusion` declares a required `section_body` locator for each of the four headings. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-role-schemas.md), [FR-005](./FR-005-executable-skeletons.md), [FR-014](./FR-014-control-mappings-are-clause-references.md); `agent-ix/quire-rs` FR-081
- **Downstream**: `agent-ix/quoin` FR-173
