---
id: FR-009
title: "A SOUP record identifies one third-party component by its purl"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-005"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-006"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-041"
    type: "references"
  - target: "ix://agent-ix/engineering-assurance/FR-038"
    type: "references"
  - target: "ix://agent-ix/engineering-assurance/FR-030"
    type: "references"
  - target: "ix://agent-ix/quoin/FR-034"
    type: "references"
---
# FR-009: A SOUP record identifies one third-party component by its purl

## Description

A software-of-unknown-provenance (SOUP) record is the reviewed statement about one third-party
component that a product ships or builds with. This module owns the validity of the authored
record: its shape, its identity and its refusals. It does not own the promotion of an SBOM
component into a record. The inventory is produced by Syft through the producer request of
`agent-ix/engineering-assurance` FR-038 and read by the SBOM adapter of `agent-ix/quoin` FR-041,
which is the consumer that promotes a component into a record and is context only here.

The `soup_record` type is the twenty-fourth object type of the module, so the counts of
[FR-003](./FR-003-semantic-manifest-contract.md) through [FR-006](./FR-006-security-safe-declarations.md)
include it: it has a role-schema row in [FR-004](./FR-004-role-schemas.md), a skeleton under
[FR-005](./FR-005-executable-skeletons.md) and the no-default rule of FR-006.

A license or provenance fact for the component already exists in the integrator package
(`agent-ix/engineering-assurance` FR-030), and a `cargo-deny` finding already exists as quoin
finding-shaped evidence (`agent-ix/quoin` FR-034). The record references them and does not copy them.

## Inputs

- The models of [FR-004](./FR-004-role-schemas.md).
- A purl, name, version and supplier as an SBOM states them.

## Outputs

- A `soup_record` entry in the manifest exports and object types, with a schema under `spec_objects_security/schemas/`.
- A `soup_record` skeleton under `spec_objects_security/skeletons/`.

## Behavior

- The module SHALL export a `soup_record` object type.
- The `soup_record` schema SHALL require `purl`, the component's package URL, as the component identity.
- The `soup_record` schema SHALL admit `name`, `version` and `supplier` as the SBOM states them.
- The `soup_record` schema SHALL admit the literal `unknown` as the value of `name`, `version`, `supplier` and `license`.
- The `soup_record` schema SHALL admit no key beyond those listed in the `soup_record` row of [FR-004](./FR-004-role-schemas.md).
- The `soup_record` schema SHALL NOT admit a digest as an identity or as any other key.
- Quire SHALL report two `soup_record` documents that carry the same purl, naming both.
- The module SHALL NOT supply a default for a field an SBOM cannot supply, consistent with [FR-006](./FR-006-security-safe-declarations.md).
- The `soup_record` schema SHALL admit `license_fact_ref`, a `SemanticId` naming the license or provenance fact of the integrator package (`agent-ix/engineering-assurance` FR-030).
- The `soup_record` schema SHALL refuse a record that carries both `license` and `license_fact_ref`, so the integrator fact is the only license statement when it exists.
- The `soup_record` schema SHALL admit `finding_refs`, a `SemanticId[]` naming `cargo-deny` finding entries of `agent-ix/quoin` FR-034.
- The `soup_record` schema SHALL admit `inventory_ref`, a `SemanticId` naming the inventory the component came from.
- The `soup_record` schema SHALL refuse a key that carries the text of a finding, a license text or an SBOM document.
- The module SHALL NOT define an SBOM parser, a promotion command, or a binding option; the `--discharges` binding stays with `agent-ix/quoin` FR-041.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-009-CON-1 | Record identity is the purl as text; the schema is closed to every other key. | Design | Test |
| FR-009-CON-2 | The module defines no SBOM reader and no `--discharges` option. | Design | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-009-AC-1 | The loaded manifest exports `soup_record` with a `data_schema` that resolves to a shipped schema file, and a `soup_record` skeleton validates with no `semantic.record-invalid` error. | Test |
| FR-009-AC-2 | A fixture `soup_record` with a purl validates, and the same record without a purl fails its schema. | Test |
| FR-009-AC-3 | Two fixture `soup_record` documents carrying the same purl yield one duplicate-identity report naming both documents. | Test |
| FR-009-AC-4 | A fixture that adds a `digest` key to an otherwise valid record fails, and a fixture whose only difference from a valid record is a different digest-free purl validates as a distinct component. | Test |
| FR-009-AC-5 | A fixture with `supplier: unknown` validates, a fixture that omits `supplier` validates with no `supplier` key added, and the emitted schema carries no `default` keyword. | Test |
| FR-009-AC-6 | A fixture carrying both `license` and `license_fact_ref` fails, and a fixture carrying only one of the two validates. | Test |
| FR-009-AC-7 | A fixture carrying `finding_refs` and `license_fact_ref` ids validates, and a fixture carrying a `finding_text` key fails. | Test |
| FR-009-AC-8 | The module declares no `--discharges` option, binding key or SBOM reader. | Inspection |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-005](./FR-005-executable-skeletons.md), [FR-006](./FR-006-security-safe-declarations.md)
- **Context only**: `agent-ix/quoin` FR-041 promotes an SBOM component into a record; its promotion requirement is not authored here.
- **Downstream**: [FR-010](./FR-010-soup-record-fields.md), [FR-011](./FR-011-soup-risk-disposition.md), [FR-012](./FR-012-soup-record-relations.md)
