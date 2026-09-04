---
id: KEY-001
title: "TenantDataEncryptionKey"
type: encryption_key
object: encryption_key
algorithm: AES-256-GCM
rotation: P90D
---
<!-- encryption_key authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: encryption_key,
       object: encryption_key and algorithm; rotation is optional.
     - "## Properties" (H2): the typed declaration. EncryptionKey.json admits
       no field carrying a default, so key material is referenced, never held. -->
# [KEY-001] TenantDataEncryptionKey

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| key_id | UUID | 1..1 | identity |
| locator | String | 1..1 | minLength: 1 |
| lifecycle | String | 1..1 | minLength: 1 |
| key_length_bits | Integer | 1..1 | min: 256 |
| rotation_period | Duration | 1..1 |  |
