---
id: FR-009
title: "A SOUP record identifies one third-party component, promoted from an SBOM component"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-006"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-041"
    type: "references"
  - target: "ix://agent-ix/engineering-assurance/FR-038"
    type: "references"
---
# FR-009: A SOUP record identifies one third-party component, promoted from an SBOM component

## Description

A software-of-unknown-provenance (SOUP) record is the reviewed statement about one
third-party component that a product ships or builds with. The module SHALL ship a
`soup_record` object type for it. The component inventory is produced by Syft through the
producer request of `agent-ix/engineering-assurance` FR-038 and read by the SBOM adapter of
`agent-ix/quoin` FR-041; this requirement owns only what a record says once a component
has been promoted from that inventory. Neither the adapter nor the producer is restated here.

## Inputs

- An ingested SBOM component, identified by its package URL (purl) as in `agent-ix/quoin` FR-041.
- The models of [FR-004](./FR-004-role-schemas.md).

## Outputs

- A `soup_record` entry in the module manifest's exports and object types, with a schema shipped under `spec_objects_security/schemas/`.

## Behavior

- The module SHALL export a `soup_record` object type.
- A `soup_record` SHALL name exactly one third-party component.
- A `soup_record` SHALL carry the component's purl as its component identity.
- Two records SHALL describe the same component only when their purls are equal.
- A `soup_record` SHALL carry the component's name and version as the SBOM states them.
- The module SHALL refuse a `soup_record` whose purl is absent.
- The module SHALL report two `soup_record` documents that carry the same purl.
- The module SHALL NOT use a content digest, a file hash, or any other recorded digest as the identity of a `soup_record`.
- A promotion SHALL copy only the facts the SBOM component states: purl, name, version, and the license and supplier facts the SBOM carries.
- A field that the SBOM component cannot supply SHALL read `unknown`.
- The module SHALL NOT supply a default for a field the SBOM cannot supply, consistent with [FR-006](./FR-006-security-safe-declarations.md).
- A component the SBOM lists without a purl SHALL NOT be promoted to a `soup_record`.
- A `soup_record` SHALL NOT carry the SBOM document's own contents.
- A `soup_record` MAY name where the inventory lives by an optional `inventory_ref` `SemanticId`.
- An SBOM component that has a `soup_record` SHALL be bound to its obligation through the existing `--discharges` binding of `agent-ix/quoin` FR-041.
- The module SHALL NOT define a second binding.
- Where a component's license or provenance is already stated as a fact by the integrator package, the `soup_record` SHALL reference that fact by `SemanticId`.
- A `soup_record` SHALL NOT restate a license or provenance fact the integrator package states.
- Where a `cargo-deny` finding exists for the component, the `soup_record` SHALL reference the finding by `SemanticId`.
- A `soup_record` SHALL NOT restate the text of a `cargo-deny` finding.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-009-CON-1 | Record identity is the purl as text; no digest field is an identity field. | Design | Test |
| FR-009-CON-2 | The module defines no SBOM parser and no inventory format. | Design | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-009-AC-1 | The loaded manifest exports `soup_record` with a `data_schema` that resolves to a shipped schema file. | Test |
| FR-009-AC-2 | A fixture `soup_record` with a purl, name and version validates, and the same record without a purl fails its schema. | Test |
| FR-009-AC-3 | Two fixture `soup_record` documents carrying the same purl yield one duplicate-identity report naming both documents. | Test |
| FR-009-AC-4 | No identity field of the `soup_record` schema is a digest; a fixture record whose only distinguishing field is a digest and whose purl is absent fails. | Test |
| FR-009-AC-5 | A fixture promoted from a CycloneDX component that has no supplier carries `unknown` for the supplier, and the emitted schema carries no `default` keyword for any field. | Test |
| FR-009-AC-6 | A fixture SBOM component with no purl yields no `soup_record`, and the promotion report names the component by its SBOM-stated name. | Test |
| FR-009-AC-7 | A fixture `soup_record` carries references to an integrator license fact and a `cargo-deny` finding by `SemanticId`, and a record that embeds the finding text instead of referencing it fails. | Test |
| FR-009-AC-8 | The module declares no `--discharges` option, binding key, or SBOM reader; the `discharges` binding is read only from the quoin adapter. | Inspection |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-006](./FR-006-security-safe-declarations.md)
- **Downstream**: [FR-010](./FR-010-soup-record-fields.md), [FR-011](./FR-011-soup-risk-disposition.md), [FR-012](./FR-012-soup-record-relations.md)
