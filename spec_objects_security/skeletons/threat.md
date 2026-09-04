---
id: THREAT-001
title: "RefreshTokenReplay"
type: threat
object: threat
stride_category: Spoofing
vector: "exfiltrated refresh token replayed from attacker infrastructure"
---
<!-- threat authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: threat, object: threat,
       stride_category (STRIDE class) and vector (the attack vector).
     - "## Properties" (H2): the typed declaration. Threat.json requires an
       identity row AND a `stride_category` row: a threat nobody classified
       is not a threat statement. -->
# [THREAT-001] RefreshTokenReplay

An attacker who exfiltrates a refresh token replays it against the token
endpoint to mint fresh access tokens and impersonate the user across tenant
APIs. Detection is hard because the requests are well formed; mitigation
relies on RefreshTokenRotation and the TenantNetworkEdge controls.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| threat_id | UUID | 1..1 | identity |
| stride_category | String | 1..1 | minLength: 1 |
| vector | String | 1..1 | minLength: 1 |
| first_observed_at | Timestamp | 0..1 |  |
