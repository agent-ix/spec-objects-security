---
id: TM-001
title: "TokenServiceThreatModel"
type: threat_model
object: threat_model
method: stride_per_interaction
reviewed_by: "A. Person"
---
<!-- threat_model authoring skeleton (spec-objects-security). Fill every section
     with substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: threat_model,
       object: threat_model, method (stride_per_element or
       stride_per_interaction) and reviewed_by (the person who led the analysis).
     - "## Properties" (H2): the typed declaration; ThreatModel.json requires
       an identity row.
     - Author at least one `scopes` edge (part, connection, data_sink or
       trust_boundary) in `relationships`; `considers` edges (threat) are
       optional.
     - "## Scope", "## Assumptions" and "## Out of scope" (H2) are required and
       non-empty free text. -->
# [TM-001] TokenServiceThreatModel

## Scope

The token endpoint and the tenant network edge, analysed per interaction with STRIDE.

## Assumptions

The tenant database is reachable only from inside the tenant VPC.

## Out of scope

The tenant browser and the identity provider.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| threat_model_id | UUID | 1..1 | identity |
| method | String | 1..1 | minLength: 1 |
| reviewed_by | String | 1..1 | minLength: 1 |
