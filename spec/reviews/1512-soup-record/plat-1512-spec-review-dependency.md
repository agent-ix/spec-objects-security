---
id: SR-029
title: "Dependency review of the SOUP record object (FR-009..FR-012, NFR-001)"
type: SpecReview
analysis: dependency
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-009..FR-012, spec/non-functional/NFR-001 (PR #44 diff)"
---
# SR-029: Dependency review of the SOUP record object (FR-009..FR-012, NFR-001)

## Summary

Ticket: PLAT-1512. Checked every `relationships:` edge and every reuse claim against its
owning artifact. Context: quoin FR-041, FR-135 and FR-046 (disposition predicates);
engineering-assurance FR-038 and FR-030 (integrator package); spec-artifacts-iso FR-004 and
the `edge_types` vocabulary in `spec_artifacts_iso/manifest.yaml`.

Clean units: FR-009's references to quoin FR-041 (purl identity and `--discharges` binding)
and engineering-assurance FR-038 (Syft producer). FR-009-AC-8 and FR-009-CON-2 (the module
declares no second binding and no SBOM reader). The FR-012 `references: [soup_record]` link
uses a declared traceability verb. Cross-repo reuse is by ix id and prose, with no copied
content. The ticket's reuse criterion is stated for the SBOM adapter and `--discharges`
binding.

## Verdict

FAIL. FND-001 is high.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | high | `affected_by` is not in the edge vocabulary. spec-artifacts-iso declares `affects` with no `inverse`, and no module declares `affected_by`. Every authored `soup_record` `affected_by` edge therefore raises the advisory `UnknownEdgeType` (spec-artifacts-iso FR-004), which contradicts FR-012-AC-3 ("validate with no finding"). This is an undeclared dependency on a spec-artifacts-iso vocabulary change. The other route, authoring `affects` from the `vulnerability` side, is ruled out by FR-012's own "leave `vulnerability.affects` unchanged". Pick one: declare `inverse: affected_by` on `affects` upstream (a dependency with its own ticket), or add `soup_record` to `vulnerability.affects`. | spec/functional/FR-012-soup-record-relations.md:31, spec/functional/FR-012-soup-record-relations.md:49 |
| FND-002 | medium | `part_of` is not a forward verb. It is the inverse label of `aggregates` ("Aggregate root owns member entities", structural, `composite: true`). An authored `soup_record part_of asset` edge therefore normalizes to `asset aggregates soup_record`, which says the asset owns the component's lifecycle as an aggregate root. That is the wrong kind of fact for a shipped third-party dependency. FR-012 neither states this resolution nor checks that the `allowed_links` test (FR-012-AC-1/AC-2) holds after normalization. Choose a verb that records the intended fact (for example `uses` or `depends_on` from the asset), or state and test the normalization. | spec/functional/FR-012-soup-record-relations.md:32 |
| FND-003 | medium | FR-011 relates only to quoin FR-135, which is the read-only matrix view. The typed disposition and its predicates (required rationale, approval reference, attestation) are owned by quoin FR-046, with stored facts in FR-133, as FR-135's own Dependencies section states. Add a `references` edge to `ix://agent-ix/quoin/FR-046`, keeping FR-135 as the `--rmm` consumer. | spec/functional/FR-011-soup-risk-disposition.md:12 |
| FND-004 | medium | FR-009 reuses "integrator package" license and provenance facts and `cargo-deny` findings without naming their owners. The integrator package and its license/provenance fact kinds are engineering-assurance FR-030, but FR-009 has no relationship to it. It also does not say which object type or record a `SemanticId` reference resolves to, for either the integrator fact or the cargo-deny finding. An implementer cannot tell what FR-009-AC-7's fixture must reference. | spec/functional/FR-009-soup-record-identity-and-promotion.md:55, spec/functional/FR-009-soup-record-identity-and-promotion.md:57 |
