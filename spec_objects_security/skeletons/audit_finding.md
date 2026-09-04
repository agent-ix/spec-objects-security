---
id: FIND-001
title: "MissingTokenRotation"
type: audit_finding
object: audit_finding
---
<!-- audit_finding authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: audit_finding,
       object: audit_finding.
     - "## Recommendation" (H2, required): what the auditor asks for.
     - "## Properties" (H2): the typed declaration. AuditFinding.json
       requires a `status` row, so an untriaged finding is refused. -->
# [FIND-001] MissingTokenRotation

## Recommendation

Enable refresh-token rotation with reuse detection on every tenant IdP
integration, and fail the release gate while any integration is without it.
Re-audit thirty days after the change lands.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| finding_id | UUID | 1..1 | identity |
| status | String | 1..1 | minLength: 1 |
| observed_at | Timestamp | 1..1 |  |
| traced_risk | TenantDataExfiltration | 0..1 |  |
