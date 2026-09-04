---
id: SECRET-001
title: "AtlasOidcClientSecret"
type: secret
object: secret
---
<!-- secret authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: secret, object: secret.
     - "## Rotation" (H2, required): how and how often the secret rotates.
     - "## Properties" (H2): the typed declaration. Secret.json admits no
       field carrying a default, so the material can never be embedded here —
       a secret is named by its locator only. -->
# [SECRET-001] AtlasOidcClientSecret

## Rotation

- Rotated every 90 days by the `secret-rotator` job, which registers the new
  secret with the IdP before revoking the old one.
- Dual-secret overlap window of 24 hours so in-flight exchanges complete.
- Emergency rotation completes in under 5 minutes.
- Every rotation emits a `secret.rotated` audit event.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| secret_id | UUID | 1..1 | identity |
| locator | String | 1..1 | minLength: 1 |
| lifecycle | String | 1..1 | minLength: 1 |
| rotation_period | Duration | 1..1 |  |
| overlap_window | Duration | 0..1 |  |
