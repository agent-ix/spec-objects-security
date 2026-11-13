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

[FR-010](./FR-010-soup-record-fields.md) gives a `soup_record` the `serves` list: the requirements the
component serves. That list is the single authored source of the fact, and the record carries no second
copy of it. The engine harvests each `ix://` value of a frontmatter field as a `references` edge, so the
list is also a set of trace edges that a completeness rule can read. The module declares as manifest data
that a record with no outgoing `references` edge to a requirement is reported. A component that serves no
requirement is unjustified scope, as a security NFR that mitigates nothing is
([FR-008](./FR-008-security-nfr-needs-mitigation-target.md)).

A manifest cannot bind a list field to a typed verb, so the edge is the generic `references` verb of the
`spec-artifacts-iso` registry, and the module introduces no link verb. The same verb is harvested from body
links, so a body link from the record to a requirement also satisfies the rule; the `serves` list remains
the authored statement that the report of quoin FR-144 reads.

The reviewer authors the list. Promotion of an SBOM component into a record ([FR-009](./FR-009-soup-record-identity-and-promotion.md))
never writes it, so a freshly promoted record is reported until a person states what it serves. The
requirement usually lives in the product repository, so a target in another repository is admitted; it
satisfies the rule when that repository is loaded into the same corpus, as in FR-008. Without a repository
identity the engine resolves an `ix://` target to a corpus document by its trailing id
(`agent-ix/quire-rs` FR-085-AC-10), so a single-repository run matches a target to a same-id local document
whatever its repository segment says.

Two capabilities this requirement would use are not in the shipped engine and are tracked in PLAT-1519:
`quire trace` and `quire matrix` do not display document-to-document edges, so `quire extract` is the
way to read the edge today (AC-6); and `quire validate` has no `--repo`, so AC-7 is not yet exercised.

## Inputs

- Documents of type `soup_record`, each with a `serves` list that is absent, empty or holds `ix://` ids.
- Documents of type `FR`, `NFR` or `StR`, in this corpus or in another repository loaded with it.

## Outputs

- One `required_relations` entry in the module manifest.
- A `[soup-serves-no-requirement]` finding for each `soup_record` with no outgoing `references` edge to a resolved `FR`, `NFR` or `StR`.

## Behavior

- The manifest SHALL declare no `allowed_links` for `soup_record`.
- The manifest SHALL declare a `required_relations` entry named `soup-record-serves-requirement` with `from: soup_record`, `edges: [references]`, `to: [FR, NFR, StR]`, `direction: outgoing` and `check: soup-serves-no-requirement`.
- Quire SHALL report a `soup_record` that has no outgoing `references` edge to a resolved `FR`, `NFR` or `StR`.
- Quire SHALL report nothing for a `soup_record` with such an edge, including one to a requirement in a repository loaded into the same corpus.
- The finding SHALL be a warning.
- Quire SHALL accept `trace:soup-serves-no-requirement` as the severity key of the finding.
- The module SHALL NOT write a `serves` entry on promotion.
- The skeleton SHALL carry no `serves` key.
- `quire extract` over a `soup_record` SHALL list each `serves` entry as an edge of type `references`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-013-AC-1 | The loaded `soup_record` type declares no `allowed_links`, and the manifest declares one `required_relations` entry named `soup-record-serves-requirement` with `from: soup_record`, `edges: [references]`, `to: [FR, NFR, StR]`, `direction: outgoing` and `check: soup-serves-no-requirement`. | Test |
| FR-013-AC-2 | Over a bundle holding a `soup_record` fixture with no `serves` entry, `quire validate --okf` exits 0 and yields exactly one `soup-serves-no-requirement` finding naming the record. | Test |
| FR-013-AC-3 | Over a bundle holding the same record with a `serves` entry naming an `FR` in the bundle, `quire validate --okf` yields no `soup-serves-no-requirement` finding. | Test |
| FR-013-AC-4 | A `serves` list whose only entries name is a document of another kind, or an id that resolves to nothing, still yields the finding. | Test |
| FR-013-AC-5 | `--severity trace:soup-serves-no-requirement=error` promotes the finding and the run exits non-zero. | Test |
| FR-013-AC-6 | The `soup_record` skeleton carries no `serves` key, and `quire extract` over a record with a `serves` entry lists an edge of type `references` to the requirement. | Test |
| FR-013-AC-7 | (Pending PLAT-1519.) `quire validate --okf --repo o/a=<A> --repo o/b=<B> --module $M` over a fixture where the record in `o/a` serves an `FR` in `o/b` yields no `soup-serves-no-requirement` finding. | Test |

## Dependencies

- **Upstream**: [FR-008](./FR-008-security-nfr-needs-mitigation-target.md), [FR-009](./FR-009-soup-record-identity-and-promotion.md), [FR-010](./FR-010-soup-record-fields.md); `agent-ix/quire-rs` FR-058 (required relations), FR-085 (cross-repository resolution)
- **Downstream**: none
