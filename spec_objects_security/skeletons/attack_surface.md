---
id: SURF-001
title: "PublicTokenEndpoint"
type: attack_surface
object: attack_surface
---
<!-- attack_surface authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: attack_surface,
       object: attack_surface.
     - "## Entry Points" (H2, required): the reachable entry points.
     - "## Properties" (H2): the typed declaration. -->
# [SURF-001] PublicTokenEndpoint

## Entry Points

- `POST /oauth/token` — authorization-code and refresh-token grants.
- `POST /oauth/revoke` — grant-family revocation.
- `GET /.well-known/openid-configuration` — unauthenticated metadata.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| surface_id | UUID | 1..1 | identity |
| transport | String | 1..1 | minLength: 1 |
| internet_reachable | Boolean | 1..1 |  |
| rate_limit_per_minute | Integer | 0..1 | min: 1 |
