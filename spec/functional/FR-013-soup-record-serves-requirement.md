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
  - target: "ix://agent-ix/quire-rs/FR-085"
    type: "depends_on"
---
# FR-013: A SOUP record that serves no requirement is reported as unjustified scope

## Description

A `soup_record` states which requirements it serves only as trace edges, so a completeness rule can
read them; the record carries no separate list of them. A reviewer authors a `supports` relationship
from the `soup_record` to each requirement it serves, and the module declares as manifest data that a record with no such edge
is reported. A component that serves no requirement is unjustified scope, as a security NFR that mitigates
nothing is ([FR-008](./FR-008-security-nfr-needs-mitigation-target.md)).

The reviewer authors the edge. Promotion of an SBOM component into a record ([FR-009](./FR-009-soup-record-identity-and-promotion.md))
never writes it, so a freshly promoted record is reported until a person states what it serves. The
requirement usually lives in the product repository, so a target in another repository is admitted; it
satisfies the rule when that repository is loaded into the same corpus, as in FR-008.

The rule is declaration, not engine code. `supports` is a verb the `spec-artifacts-iso` edge registry already
declares, so the module introduces no link verb. Without a repository identity, the engine resolves an
`ix://` target to a corpus document by its trailing id (`agent-ix/quire-rs` FR-085-AC-10), so a
single-repository run matches a target to a same-id local document whatever its repository segment says.

Two capabilities this requirement would use are not in the shipped engine and are tracked in PLAT-1519:
`quire trace` and `quire matrix` do not display document-to-document edges, so `quire extract` is the
way to read the authored edge today (AC-6); and `quire validate` has no `--repo`, so AC-7 is not yet
exercised.

## Inputs

- Documents of type `soup_record`, each with zero or more `supports` relationships.
- Documents of type `FR`, `NFR` or `StR`, in this corpus or in another repository loaded with it.

## Outputs

- `soup_record.allowed_links.supports` and one `required_relations` entry in the module manifest.
- A `[soup-serves-no-requirement]` finding for each `soup_record` with no outgoing `supports` edge to a resolved `FR`, `NFR` or `StR`.

## Behavior

- The manifest SHALL declare `soup_record.allowed_links.supports` as `[FR, NFR, StR]`.
- The manifest SHALL declare a `required_relations` entry named `soup-record-serves-requirement` with `from: soup_record`, `edges: [supports]`, `to: [FR, NFR, StR]`, `direction: outgoing` and `check: soup-serves-no-requirement`.
- Quire SHALL report a `soup_record` that has no outgoing `supports` edge to a resolved `FR`, `NFR` or `StR`.
- Quire SHALL report nothing for a `soup_record` with such an edge, including one to a requirement in a repository loaded into the same corpus.
- The finding SHALL be a warning.
- Quire SHALL accept `trace:soup-serves-no-requirement` as the severity key of the finding.
- The module SHALL NOT write a `supports` edge on promotion.
- The skeleton SHALL carry no `relationships` key.
- `quire extract` over a `soup_record` SHALL list each authored `supports` relationship as an edge of type `supports`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-013-AC-1 | The loaded `soup_record` type lists exactly `FR`, `NFR`, `StR` under `allowed_links.supports`, and the manifest declares one `required_relations` entry named `soup-record-serves-requirement` with `from: soup_record`, `edges: [supports]`, `to: [FR, NFR, StR]`, `direction: outgoing` and `check: soup-serves-no-requirement`. | Test |
| FR-013-AC-2 | Over a bundle holding a `soup_record` fixture with no `supports` relationship, `quire validate --okf` exits 0 and yields exactly one `soup-serves-no-requirement` finding naming the record. | Test |
| FR-013-AC-3 | Over a bundle holding the same record with a `supports` relationship to an `FR` in the bundle, `quire validate --okf` yields no `soup-serves-no-requirement` finding. | Test |
| FR-013-AC-4 | A `supports` relationship whose only target is a document of another kind, or an id that resolves to nothing, still yields the finding. | Test |
| FR-013-AC-5 | `--severity trace:soup-serves-no-requirement=error` promotes the finding and the run exits non-zero. | Test |
| FR-013-AC-6 | The `soup_record` skeleton carries no `relationships` key, and `quire extract` over a record with a `supports` relationship lists an edge of type `supports` to the requirement. | Test |
| FR-013-AC-7 | (Pending PLAT-1519.) `quire validate --okf --repo o/a=<A> --repo o/b=<B> --module $M` over a fixture where the record in `o/a` serves an `FR` in `o/b` yields no `soup-serves-no-requirement` finding. | Test |

## Dependencies

- **Upstream**: [FR-008](./FR-008-security-nfr-needs-mitigation-target.md), [FR-009](./FR-009-soup-record-identity-and-promotion.md), [FR-010](./FR-010-soup-record-fields.md); `agent-ix/quire-rs` FR-058 (required relations), FR-085 (cross-repository resolution)
- **Downstream**: none
