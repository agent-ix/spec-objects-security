---
id: SR-031
title: "Scope-boundary review of the SOUP record object (FR-009..FR-012, NFR-001)"
type: SpecReview
analysis: scope-boundary
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-009..FR-012, spec/non-functional/NFR-001 (PR #44 diff)"
---
# SR-031: Scope-boundary review of the SOUP record object (FR-009..FR-012, NFR-001)

## Summary

Ticket: PLAT-1512. Checked that each obligation is assigned to a system that can meet it,
and that this declarative object module (manifest, schemas, skeletons) claims only what it
can do. Context: `spec/spec.md` Scope and Out of Scope, quoin FR-041 (the SBOM adapter
reads an inventory as run evidence and introduces no record type, FR-041-CON-2), and
engineering-assurance FR-038.

Clean units: FR-009-CON-2 and FR-009-AC-8 (no SBOM parser, inventory format or second
binding in this module). FR-012's exclusion of advisory matching. NFR-001 (the module
derives nothing). FR-011's "no inferred or computed disposition".

## Verdict

FAIL. FND-001 is high.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | high | No system owns promotion. FR-009-CON-2 and FR-009-AC-8 say this module has no SBOM parser or reader, and quoin FR-041-CON-2 says quoin introduces no inventory record type. Yet FR-009 requires that "a promotion SHALL copy" SBOM facts, that a purl-less component "SHALL NOT be promoted", FR-009-AC-5 ("a fixture promoted from a CycloneDX component ... carries `unknown`") and FR-009-AC-6 ("the promotion report names the component"). No owner can meet those ACs, and a test in this repository has nothing to run. Name the promoter by ix id, with its own requirement in its repository, and move AC-5/AC-6 there. Or restate them as schema checks on an authored record. | spec/functional/FR-009-soup-record-identity-and-promotion.md:47, spec/functional/FR-009-soup-record-identity-and-promotion.md:75, spec/functional/FR-009-soup-record-identity-and-promotion.md:76 |
| FND-002 | low | "An `affected_by` edge SHALL exist only when an author wrote it" and "The module SHALL NOT populate `affected_by` from an advisory feed" state limits on a module that writes no edges at all. No test can observe either one. Both are already implied by FR-012's Description and by FR-009-CON-2. Fold them into a constraint verified by Inspection, or delete them. | spec/functional/FR-012-soup-record-relations.md:36, spec/functional/FR-012-soup-record-relations.md:37 |
