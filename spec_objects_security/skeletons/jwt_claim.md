---
id: CLAIM-001
title: "TenantIdentifierClaim"
type: jwt_claim
object: jwt_claim
---
<!-- jwt_claim authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: jwt_claim, object: jwt_claim.
     - "## Schema" (H2, required) holds a fenced `json` block. It is a
       derived, human-facing view; the typed table is the authority.
     - "## Properties" (H2): JwtClaim.json admits no field carrying a
       default, so no claim value is written into the declaration. -->
# [CLAIM-001] TenantIdentifierClaim

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| claim_id | UUID | 1..1 | identity |
| claim_name | String | 1..1 | minLength: 1, maxLength: 32 |
| value_type | String | 1..1 | minLength: 1 |
| required_in_access_token | Boolean | 1..1 |  |

## Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://specs.agent-ix.dev/claims/tenant-identifier.schema.json",
  "title": "TenantIdentifierClaim",
  "type": "object",
  "required": ["tid"],
  "properties": {
    "tid": { "type": "string", "format": "uuid" }
  }
}
```
