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
  - target: "ix://agent-ix/quire-rs/FR-085"
    type: "depends_on"
  - target: "ix://agent-ix/quire-cli/FR-030"
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
`security`. The NFR authors the edge, so the direction is `outgoing`. `to` names
`threat` and `risk`: the threat an NFR answers is often declared in another
repository, and `agent-ix/quire-rs` FR-085 resolves an edge to a repository
loaded into the same corpus, so a cross-repository target satisfies the
constrained `to`. A target of any other kind is reported by quire as a kind
mismatch (FR-085) and does not satisfy the obligation. An edge to a repository
that is not loaded is dangling in a corpus whose members declare identities
(FR-085) and does not satisfy it either.

The coverage report of `agent-ix/quire-rs` FR-084 reads this declaration as the
reverse view: each `security` NFR with the threats it mitigates, and a
`security` NFR with none as a gap.

The cross-repository case is reached through `quire validate --okf --repo ORG/REPO=DIR`
(`agent-ix/quire-cli` FR-030), which loads the sibling repositories into one
corpus. Without `--repo`, validate sees one repository and an edge into another
repository is dangling.

The finding is advisory (`warning`, exit 0) and is tunable on its own key,
`trace:unjustified-security-nfr`. The safety counterpart (`safety` NFRs and
hazards) is declared by `agent-ix/spec-objects-safety` FR-009.

## Inputs

- Documents of type `NFR` (`spec-artifacts-iso`) with a `quality_attribute`.
- Documents of type `threat` or `risk`, in this corpus or in another repository loaded with it.
- The `spec-artifacts-iso` and `spec-objects-security` manifests loaded together.

## Outputs

- A `[unjustified-security-nfr]` finding for each `security` NFR that has no outgoing `mitigates` edge to a resolved `threat` or `risk`, naming the NFR, the declaration and the selector (`quality_attribute` and its value). It is produced by `quire validate --okf`, with `--repo ORG/REPO=DIR` loading the repositories that hold the targets.

## Behavior

- The manifest SHALL declare a `required_relations` entry `from: NFR` with `where: {field: quality_attribute, values: [security]}`, `edges: [mitigates]`, `to: [threat, risk]`, `direction: outgoing` and `check: unjustified-security-nfr`.
- Quire SHALL report an NFR whose `quality_attribute` is `security` and which has no outgoing `mitigates` edge to a resolved `threat` or `risk`.
- Quire SHALL report nothing for a `security` NFR with an outgoing `mitigates` edge to a resolved `threat` or `risk`, including one in a repository loaded with `--repo`.
- If a `security` NFR's only outgoing `mitigates` edges target a document of another kind, or a repository that is not loaded, then Quire SHALL report the NFR.
- Quire SHALL report nothing for an NFR whose `quality_attribute` is any other value.
- The finding SHALL be a warning under `--okf` and under `--okf --strict`; unrelated errors that `--strict` raises (for example iso's `unowned-quality-characteristic`) are not this rule's.
- When `--severity trace:unjustified-security-nfr=error` is given, Quire SHALL promote the finding to an error.
- The manifest SHALL keep `to: []` on `threat-has-control` and `risk-has-treatment`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-008-AC-1 | The manifest declares one `required_relations` entry with `from: NFR`, `where` over `quality_attribute` with `values: [security]`, `edges: [mitigates]`, `to: [threat, risk]`, `direction: outgoing` and `check: unjustified-security-nfr`. | Test |
| FR-008-AC-2 | Over a bundle holding a `security` NFR with no `mitigates` edge, `quire validate --okf` exits 0 and yields exactly one `unjustified-security-nfr` finding, naming the NFR and the value `security`. | Test |
| FR-008-AC-3 | Giving that NFR a `mitigates` edge to a `threat` in the same repository removes the finding. | Test |
| FR-008-AC-4 | An NFR whose `quality_attribute` is not `security` and which has no `mitigates` edge yields no `unjustified-security-nfr` finding. | Test |
| FR-008-AC-5 | Under `--okf --strict` the finding is a warning and never an error; strict still exits 3 on warnings by design. `--severity trace:unjustified-security-nfr=error` promotes it and the run exits non-zero. | Test |
| FR-008-AC-6 | Giving that NFR a `mitigates` edge to a `risk` in the same repository removes the finding. | Test |
| FR-008-AC-7 | `quire validate --okf --repo o/a=<A> --repo o/b=<B> --module $M` over a fixture where the NFR in `o/a` has a `mitigates` edge to a `threat` in `o/b` yields no `unjustified-security-nfr` finding. | Test |
| FR-008-AC-8 | An NFR whose only `mitigates` edge targets a `hazard` in the same repository still yields the `unjustified-security-nfr` finding. | Test |
| FR-008-AC-9 | An NFR whose only `mitigates` edge targets a `threat` in a repository not named by any `--repo` still yields the `unjustified-security-nfr` finding. | Test |
| FR-008-AC-10 | `threat-has-control` and `risk-has-treatment` still declare `to: []` in the manifest. | Test |

## Dependencies

- **Upstream**: [FR-007](./FR-007-control-mitigates-safety-objects.md); `agent-ix/quire-rs` FR-058 (`where` selector, AC-12..22), FR-085 (cross-repository resolution); `agent-ix/quire-cli` FR-030 (`validate --okf --repo`); `spec-artifacts-iso` (`NFR` and `quality_attribute`)
- **Downstream**: `agent-ix/quire-rs` FR-084 (reads this declaration as the reverse view of the coverage report)
