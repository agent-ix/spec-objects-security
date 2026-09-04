---
id: THREAT-001
title: "RefreshTokenReplay"
type: threat
object: threat
stride_category: Spoofing
vector: "exfiltrated refresh token replayed from attacker infrastructure"
---
<!-- threat authoring skeleton, alternate Properties form. Declares exactly the
     same fields as threat.md, authored as one ```sysml``` fence instead of the
     typed table (FR-005-AC-2). -->
# [THREAT-001] RefreshTokenReplay

An attacker who exfiltrates a refresh token replays it against the token
endpoint to mint fresh access tokens and impersonate the user across tenant
APIs. Detection is hard because the requests are well formed; mitigation
relies on RefreshTokenRotation and the TenantNetworkEdge controls.

## Properties

```sysml
attribute threat_id : UUID[1..1] { identity }
attribute stride_category : String[1..1] { minLength: 1 }
attribute vector : String[1..1] { minLength: 1 }
attribute first_observed_at : Timestamp[0..1]
```
