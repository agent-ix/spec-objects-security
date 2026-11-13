---
id: SR-028
title: "Integrity review of the SOUP record object (FR-009..FR-012, NFR-001)"
type: SpecReview
analysis: integrity
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-009..FR-012, spec/non-functional/NFR-001 (PR #44 diff)"
---
# SR-028: Integrity review of the SOUP record object (FR-009..FR-012, NFR-001)

## Summary

Ticket: PLAT-1512. Checked the new requirements against each other and against the
existing spec set for consistency, completeness and testability. Context: `spec/spec.md`
Scope, FR-003-AC-1, FR-004-AC-1/AC-11, FR-005-AC-1/AC-7, FR-006-AC-4, and quoin's
disposition fact (`rust/crates/quoin-assurance/src/discharge/report.rs` and `parse.rs` on
quoin `main`).

Clean units: FR-010-AC-1, FR-010-AC-3, FR-010-AC-4 (closed enums and no-default are
testable against the emitted schema), FR-011-AC-1..AC-5, FR-011-AC-7, NFR-001-AC-1 and
NFR-001-AC-2. The three `SoupDispositionKind` members equal quoin's `DispositionDecision`
wire spellings (`accepted_risk`, `temporary_exception`, `delegated`). NFR-001 satisfies the
ticket's "no derived scores or classes" criterion.

## Verdict

FAIL. FND-001, FND-002 and FND-003 are high.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | high | FR-009-AC-1 adds a 24th export, `soup_record`. The existing requirements state the set is exactly twenty-three: FR-003 Behavior and FR-003-AC-1 ("`exports` equals the twenty-three object-type names"), FR-004-AC-1/AC-11, FR-005-AC-1/AC-7, FR-006-AC-4 and `spec/spec.md` Scope ("The 23 tier-2 ObjectTypes"). Implementing FR-009 makes FR-003-AC-1 false. The PR amends none of them. Nor does it say whether FR-004 (role-schema row), FR-005 (skeleton plus negative counterpart) and FR-006 (no default, explicit grade) apply to `soup_record`. | spec/functional/FR-009-soup-record-identity-and-promotion.md:71, spec/functional/FR-003-semantic-manifest-contract.md:47, spec/functional/FR-003-semantic-manifest-contract.md:68, spec/spec.md:28 |
| FND-002 | high | FR-011 says it reuses quoin's typed dispositions, but the fields it specifies are not quoin's. quoin's disposition fact (FR-046/FR-133, read by `discharge --rmm`) is `{kind: "disposition", clauseId, decision, rationale, approvalRef, attestation: {attestedBy, authority, attestedAt, expiresAt}}`, with exact keys. FR-011 uses `kind` (quoin: `decision`) and `approval_ref` (quoin: `approvalRef`). It adds `expires` on `temporary_exception` only, but quoin requires `expiresAt` on every disposition. It adds `approver` and `delegate`, which quoin does not have. So "SHALL pass `kind`, `approval_ref`, `rationale` and `expires` to `quoin discharge --rmm` unchanged" cannot be met. quoin dispositions also attach to a `clauseId`, which a component record lacks, and FR-011 names no path between the two. Fix: reuse quoin's disposition shape (decision, rationale, approvalRef, attestation with attestedBy/authority as the person-owned approval), or state the mapping explicitly. Then delete the restated enum and FR-011-AC-8's copy-equality check, which exists only because the vocabulary is copied. | spec/functional/FR-011-soup-risk-disposition.md:48 |
| FND-003 | high | FR-011-AC-6 ("a fixture whose `approver` names an agent identity fails") cannot be implemented. No identity vocabulary in this module, semantic-core or quoin distinguishes a person from an agent. None of the 23 object types models an identity kind, and `approver` is a bare `SemanticId`. Two implementers would build different checks, or none. This AC carries the ticket's "person-owned" criterion, so it needs a stated discriminator (for example, a `person` object type or quoin's `attestation.authority`). Alternatively, state the criterion as a reviewed process constraint with Inspection verification. | spec/functional/FR-011-soup-risk-disposition.md:66, spec/functional/FR-011-soup-risk-disposition.md:44 |
| FND-004 | medium | FR-010 contradicts itself and FR-009 on unknown and absent fields. The Description says each of the four fields "has an explicit `unknown` state". Only `support_status` and `end_of_support` do: `serves` is a `SemanticId[]` and `known_anomalies` uses absence. The Behavior says a record "SHALL carry `known_anomalies`" but also gives an absent field a meaning ("nobody looked"). FR-009 says a field the SBOM cannot supply "SHALL read `unknown`", which a list-typed `serves` or `known_anomalies` cannot do. State which fields are required, and how each one expresses "not assessed". | spec/functional/FR-010-soup-record-fields.md:19, spec/functional/FR-010-soup-record-fields.md:32 |
| FND-005 | medium | FR-009 has two rules that conflict when both apply. A promotion "SHALL copy ... the license and supplier facts the SBOM carries", and a record "SHALL NOT restate a license or provenance fact the integrator package states". When both the SBOM and the integrator package carry a license, nothing says which rule wins. | spec/functional/FR-009-soup-record-identity-and-promotion.md:47, spec/functional/FR-009-soup-record-identity-and-promotion.md:56 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-006 | medium | The fix for FND-002 keys a component's risk decision on `disposition_clause`, which FR-011 defines as "the obligation the component's SBOM entries are bound to by the `--discharges` binding". quoin FR-041 binds every component of one recording to the same stated obligation id, and a quoin disposition fact is keyed on `clauseId` alone. So every `soup_record` from one inventory names the same clause, and one disposition fact tailors the whole obligation. The model cannot record that component A's risk is accepted while component B's is not, so the per-component, person-owned decision the ticket asks for cannot be expressed. Either state a per-component clause id and say who mints it, or state that the decision is per inventory obligation and that per-component acceptance is out of scope. | spec/functional/FR-011-soup-risk-disposition.md:29-31 |

## Dispositions

| FND | outcome | reason |
|-----|---------|--------|
| FND-001 | fixed | Fixed in PLAT-1514. FR-004 "Twenty-four object-type models", IT-002 "twenty-four exports", US-001 "twenty-four object types" and the FR-005-AC-4 "nineteen field-bearing types" now match the 24-type module and FR-005 Behavior. |
| FND-002 | fixed | Fixed in 3d75c3d. FR-011 now references the quoin FR-046 fact "{kind: \"disposition\", clauseId, decision, rationale, approvalRef, attestation: {attestedBy, authority, attestedAt, expiresAt}}". It says "This module defines no second shape and no copy of that vocabulary", refuses `decision`, `rationale`, `approvalRef`, `approval_ref`, `attestation`, `approver` and `expires`, and drops the copy-equality AC. |
| FND-003 | fixed | Fixed in 3d75c3d. The agent-identity AC is gone. FR-011-CON-1 (Process, Inspection) says "every disposition fact that a `disposition_clause` names carries an `attestation` whose `attestedBy` and `authority` identify the accountable person", and FR-011-AC-4 is a reviewer Inspection. |
| FND-004 | fixed | Fixed in 3d75c3d. FR-010 Description: "A scalar field (`support_status`, `end_of_support`) holds the literal `unknown`. A list field (`serves`, `known_anomalies`) has no `unknown` member: an absent list means nobody has stated it, and an empty list means the reviewer stated that there are none." Behavior now says "admit" rather than "carry". |
| FND-005 | fixed | Fixed in 3d75c3d. The promotion copy rule is gone. FR-009: "The `soup_record` schema SHALL refuse a record that carries both `license` and `license_fact_ref`, so the integrator fact is the only license statement when it exists", tested by FR-009-AC-6. |
| FND-006 | fixed | Fixed in PLAT-1514. FR-011 now says `disposition_clause` is the clause id a person's disposition fact is keyed on, minted by the record's author; quoin FR-141 fills it from the `--discharges` obligation id, so records promoted from one recording share a clause and one fact covers them, and an author who wants to decide one component separately gives that record its own distinct clause id. |
