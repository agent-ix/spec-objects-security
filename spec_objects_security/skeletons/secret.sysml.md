---
id: SECRET-001
title: "AtlasOidcClientSecret"
type: secret
object: secret
---
<!-- secret authoring skeleton, alternate Properties form. Declares exactly the
     same fields as secret.md, authored as one ```sysml``` fence instead of the
     typed table (FR-005-AC-2). No row carries a value: a secret is named by
     its locator only (FR-006). -->
# [SECRET-001] AtlasOidcClientSecret

## Rotation

- Rotated every 90 days by the `secret-rotator` job, which registers the new
  secret with the IdP before revoking the old one.
- Dual-secret overlap window of 24 hours so in-flight exchanges complete.
- Emergency rotation completes in under 5 minutes.
- Every rotation emits a `secret.rotated` audit event.

## Properties

```sysml
attribute secret_id : UUID[1..1] { identity }
attribute locator : String[1..1] { minLength: 1 }
attribute lifecycle : String[1..1] { minLength: 1 }
attribute rotation_period : Duration[1..1]
attribute overlap_window : Duration[0..1]
```
