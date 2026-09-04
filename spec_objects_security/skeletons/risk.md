---
id: RISK-001
title: "TenantDataExfiltration"
type: risk
object: risk
likelihood: possible
impact: major
---
<!-- risk authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: risk, object: risk,
       likelihood and impact.
     - "## Properties" (H2): the typed declaration. Risk.json requires both a
       `likelihood` row and an `impact` row: a risk scored on one axis is
       not scored. -->
# [RISK-001] TenantDataExfiltration

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| risk_id | UUID | 1..1 | identity |
| likelihood | String | 1..1 | minLength: 1 |
| impact | String | 1..1 | minLength: 1 |
| assessed_at | Timestamp | 1..1 |  |
| affected_asset | TenantDatabase | 0..1 |  |
