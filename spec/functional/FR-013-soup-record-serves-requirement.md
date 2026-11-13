---
id: FR-013
title: "A SOUP record that serves no requirement is reported as unjustified scope"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-008"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-010"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-058"
    type: "depends_on"
---
# FR-013: A SOUP record that serves no requirement is reported as unjustified scope

## Description

[FR-010](./FR-010-soup-record-fields.md) gives a `soup_record` a `serves` record field naming the
requirements the component serves. A record field is not a trace edge, so no completeness rule can read
it. This requirement adds the edge: a reviewer authors a `serves` relationship from the `soup_record`
to each requirement it serves, and the module declares as manifest data that a record with no such edge
is reported. A component that serves no requirement is unjustified scope, as a security NFR that mitigates
nothing is ([FR-008](./FR-008-security-nfr-needs-mitigation-target.md)).

The reviewer authors the edge. Promotion of an SBOM component into a record ([FR-009](./FR-009-soup-record-identity-and-promotion.md))
never writes it, so a freshly promoted record is reported until a person states what it serves. The
requirement usually lives in the product repository, so a target in another repository is admitted; it
satisfies the rule when that repository is loaded into the same corpus, as in FR-008.

The rule is declaration, not engine code, and adds no link verb the engine does not know.

## Inputs

- Documents of type `soup_record`, each with zero or more `serves` relationships.
- Documents of type `FR`, `NFR` or `StR`, in this corpus or in another repository loaded with it.

## Outputs

- `soup_record.allowed_links.serves` and one `required_relations` entry in the module manifest.
- A `[soup-serves-no-requirement]` finding for each `soup_record` with no outgoing `serves` edge to a resolved `FR`, `NFR` or `StR`.

## Behavior

- The manifest SHALL declare `soup_record.allowed_links.serves` as `[FR, NFR, StR]`.
- The manifest SHALL declare a `required_relations` entry named `soup-record-serves-requirement` with `from: soup_record`, `edges: [serves]`, `to: [FR, NFR, StR]`, `direction: outgoing` and `check: soup-serves-no-requirement`.
- Quire SHALL report a `soup_record` that has no outgoing `serves` edge to a resolved `FR`, `NFR` or `StR`.
- Quire SHALL report nothing for a `soup_record` with such an edge, including one to a requirement in a repository loaded into the same corpus.
- The finding SHALL be a warning.
- Quire SHALL accept `trace:soup-serves-no-requirement` as the severity key of the finding.
- The module SHALL NOT write a `serves` edge on promotion.
- The skeleton SHALL carry no `relationships` key.
- `quire extract` over a `soup_record` SHALL list each authored `serves` relationship as an edge of type `serves`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-013-AC-1 | The loaded `soup_record` type lists exactly `FR`, `NFR`, `StR` under `allowed_links.serves`, and the manifest declares one `required_relations` entry named `soup-record-serves-requirement` with `from: soup_record`, `edges: [serves]`, `to: [FR, NFR, StR]`, `direction: outgoing` and `check: soup-serves-no-requirement`. | Test |
| FR-013-AC-2 | Over a bundle holding a `soup_record` fixture with no `serves` relationship, `quire validate --okf` exits 0 and yields exactly one `soup-serves-no-requirement` finding naming the record. | Test |
| FR-013-AC-3 | Over a bundle holding the same record with a `serves` relationship to an `FR` in the bundle, `quire validate --okf` yields no `soup-serves-no-requirement` finding. | Test |
| FR-013-AC-4 | A `serves` relationship whose only target is a document of another kind, or an id that resolves to nothing, still yields the finding. | Test |
| FR-013-AC-5 | `--severity trace:soup-serves-no-requirement=error` promotes the finding and the run exits non-zero. | Test |
| FR-013-AC-6 | The `soup_record` skeleton carries no `relationships` key, and `quire extract` over a record with a `serves` relationship lists an edge of type `serves` to the requirement. | Test |
| FR-013-AC-7 | `quire validate --okf --repo o/a=<A> --repo o/b=<B> --module $M` over a fixture where the record in `o/a` serves an `FR` in `o/b` yields no `soup-serves-no-requirement` finding. | Test |

## Dependencies

- **Upstream**: [FR-008](./FR-008-security-nfr-needs-mitigation-target.md), [FR-009](./FR-009-soup-record-identity-and-promotion.md), [FR-010](./FR-010-soup-record-fields.md); `agent-ix/quire-rs` FR-058 (required relations), FR-085 (cross-repository resolution)
- **Downstream**: none
