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

The `scope_exclusion` is a declaration of boundary. It is not an approval: the approval of the exclusion, with an
actor, an authority and an expiry, is the `delegated` disposition fact of `agent-ix/quoin` FR-046, recorded by a
person (see `agent-ix/quoin` FR-173).

The type is the twenty-fifth object type of the module, so the counts of
[FR-003](./FR-003-semantic-manifest-contract.md) through [FR-006](./FR-006-security-safe-declarations.md) include it: it has a
role-schema row in [FR-004](./FR-004-role-schemas.md), a skeleton under [FR-005](./FR-005-executable-skeletons.md) and the
no-default rule of FR-006.

The key is `responsible` and not `owner`, because `owner` is a key the engine's record-sections mapping never reads (it is a systems member of `agent-ix/quire-rs` FR-075).

The authored form is four sections, each with one inline-code value: `## Set`, `## Clause`, `## Responsible` and `## Rationale`.
Quire reads each into the record key of the same name through the `record-sections` mapping (`agent-ix/quire-rs` FR-081), the
same mapping as [FR-014](./FR-014-control-mappings-are-clause-references.md). The mapping does not read frontmatter, so no
key is authored there. The frontmatter carries `id`, `title`, `type` and `object`, as every skeleton does.

## Behavior

- The `scope_exclusion` record schema SHALL require `set` and `clause` (the shape of FR-014), `responsible` and `rationale`.
- `responsible` SHALL be a `SemanticId` naming the component, service or document that is responsible for the clause.
- The `responsible` value SHALL name the bare id of an artifact in the same bundle, for example `COMP-001`, which is the form Quire resolves with a bundle package.
- A `responsible` written as a cross-repository id such as `ix://agent-ix/example-platform/COMP-001` is refused by Quire as not a bundle artifact id when a bundle package is supplied, so this module does not admit it; a party outside the repository is named by an artifact in this bundle that stands for it.
- `rationale` SHALL be a non-empty string.
- The `scope_exclusion` schema SHALL reject every property outside its four and declare no decision, status, score or approval property.
- The module SHALL export `scope_exclusion` and ship a skeleton that validates.
- The manifest entry for `scope_exclusion` SHALL require the sections `## Set`, `## Clause`, `## Responsible` and `## Rationale`, each with a `section_body` locator.
- An authored exclusion with no `## Responsible` section SHALL fail validation with `semantic.record-invalid` naming `responsible`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-016-AC-1 | `ScopeExclusion.json` requires exactly `set`, `clause`, `responsible` and `rationale`, is sealed, and `scope_exclusion` appears in the manifest `exports`. | Test |
| FR-016-AC-2 | A record without `responsible`, with a `responsible` that is not a `SemanticId`, or with an empty `rationale` fails validation. An authored fixture with no `## Responsible` section fails `semantic.record-invalid` naming `responsible`. | Test |
| FR-016-AC-3 | A record with `decision`, `status` or `approved_by` fails validation. | Test |
| FR-016-AC-4 | The `scope_exclusion` skeleton validates with no `semantic.record-invalid` and has no placeholder token; each of the four sections removed in turn makes it fail `semantic.record-invalid` naming that key. | Test |
| FR-016-AC-7 | With a bundle package supplied, a fixture whose `## Responsible` is the bare id of a bundle artifact validates, and one whose `## Responsible` is `ix://agent-ix/example-platform/COMP-001` fails with `not a bundle artifact id`. | Test |
| FR-016-AC-5 | The empty record `{}` fails `ScopeExclusion.json`. | Test |
| FR-016-AC-6 | The manifest entry for `scope_exclusion` declares a required `section_body` locator for each of the four headings. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-role-schemas.md), [FR-005](./FR-005-executable-skeletons.md), [FR-014](./FR-014-control-mappings-are-clause-references.md); `agent-ix/quire-rs` FR-081
- **Downstream**: `agent-ix/quoin` FR-173
