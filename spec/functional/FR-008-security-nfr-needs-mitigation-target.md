---
id: FR-008
title: "A security-classified NFR that mitigates nothing is reported as unjustified scope"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-007"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-058"
    type: "depends_on"
---
# FR-008: A security-classified NFR that mitigates nothing is reported as unjustified scope

## Description

`threat-has-control` and `risk-has-treatment` read the `mitigates` edge from the
exposure end: a threat or risk nothing mitigates is reported. This requirement
reads it from the requirement end. A non-functional requirement that claims to
be about security and answers no threat or risk is scope nobody asked for, and
no per-document check can see it.

The classification is the `quality_attribute` frontmatter field that
`spec-artifacts-iso` declares on `NFR` with `security` among its values. The
module declares the obligation as data, using the `where` selector of
`agent-ix/quire-rs` FR-058 (FR-058-AC-12..22) to narrow it to NFRs holding
`security`. The NFR authors the edge, so the direction is `outgoing`. `to` stays
empty: the threat or risk an NFR answers is usually declared in another
repository, and FR-058 does not let a dangling edge satisfy a constrained `to`.

### What `to: []` lets through

With `to: []` any outgoing `mitigates` edge discharges the obligation: an edge to a threat or risk, to a hazard, to a document in another repository, to another NFR, or to a mistyped local id (reported only by `dangling-reference`). iso's `NFR.allowed_links` does not constrain the target kind either. So a clean run does not mean the NFR traces to a threat or risk. This is the accepted cost: a cross-repo `ix://` target cannot satisfy a constrained `to`, and constraining it would report correct NFRs whose threat lives elsewhere.

The finding is advisory (`warning`, exit 0) and is tunable on its own key,
`trace:unjustified-security-nfr`. The safety counterpart (`safety` NFRs and
hazards) is declared by `agent-ix/spec-objects-safety` FR-009.

## Inputs

- Documents of type `NFR` (`spec-artifacts-iso`) with a `quality_attribute`.
- Documents of type `threat` or `risk`, or an edge to one declared elsewhere.
- The `spec-artifacts-iso` and `spec-objects-security` manifests loaded together.

## Outputs

- An `[unjustified-security-nfr]` finding for each `security` NFR with no outgoing `mitigates` edge, naming the NFR, the declaration and the selector (`quality_attribute` and its value).

## Behavior

- The manifest SHALL declare a `required_relations` entry `from: NFR` with `where: {field: quality_attribute, values: [security]}`, `edges: [mitigates]`, `to: []`, `direction: outgoing` and `check: unjustified-security-nfr`.
- Quire SHALL report an NFR whose `quality_attribute` is `security` and which has no outgoing `mitigates` edge.
- Quire SHALL report nothing for a `security` NFR with an outgoing `mitigates` edge, including an edge to a document in another repository.
- Quire SHALL report nothing for an NFR whose `quality_attribute` is any other value.
- The finding SHALL be a warning under `--okf` and under `--okf --strict`; unrelated errors that `--strict` raises (for example iso's `unowned-quality-characteristic`) are not this rule's.
- When `--severity trace:unjustified-security-nfr=error` is given, Quire SHALL promote the finding to an error.
- The module SHALL NOT narrow the `to: []` of `threat-has-control` or `risk-has-treatment`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-008-AC-1 | The manifest declares one `required_relations` entry with `from: NFR`, `where` over `quality_attribute` with `values: [security]`, `edges: [mitigates]`, `to: []`, `direction: outgoing` and `check: unjustified-security-nfr`. | Test |
| FR-008-AC-2 | Over a bundle holding a `security` NFR with no `mitigates` edge, `quire validate --okf` exits 0 and yields exactly one `unjustified-security-nfr` finding, naming the NFR and the value `security`. | Test |
| FR-008-AC-3 | Giving that NFR a `mitigates` edge to a `threat` removes the finding, as does an edge to a document in another repository. | Test |
| FR-008-AC-4 | An NFR whose `quality_attribute` is not `security` and which has no `mitigates` edge yields no `unjustified-security-nfr` finding. | Test |
| FR-008-AC-5 | Under `--okf --strict` the finding stays a warning, and a bundle whose only faults are these findings stays valid (`agent-ix/quire-rs` FR-058-AC-18). `--severity trace:unjustified-security-nfr=error` promotes it and the run exits non-zero. | Test |
| FR-008-AC-6 | `threat-has-control` and `risk-has-treatment` still declare `to: []`. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-007](./FR-007-control-mitigates-safety-objects.md); `agent-ix/quire-rs` FR-058 (`where` selector, AC-12..22); `spec-artifacts-iso` (`NFR` and `quality_attribute`)
