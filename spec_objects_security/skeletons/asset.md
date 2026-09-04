---
id: ASSET-001
title: "TenantDatabase"
type: asset
object: asset
---
<!-- asset authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: asset, object: asset.
     - "## Description" (H2, required): what the asset is and why it matters.
     - "## Properties" (H2): one typed row per attribute, header exactly
       `Field | Type | Multiplicity | Constraints`. At least one row carries
       the `identity` constraint (Asset.json refuses a record without one). -->
# [ASSET-001] TenantDatabase

## Description

The per-tenant PostgreSQL database holding customer records, order history and
audit trails. It is the primary confidentiality and integrity asset of the
platform: its compromise discloses every tenant's data at once.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| asset_id | UUID | 1..1 | identity |
| name | String | 1..1 | minLength: 1, maxLength: 128 |
| classification | DataRestricted | 1..1 |  |
| steward | String | 1..1 | minLength: 1 |
| replica_count | Integer | 0..1 | min: 0 |
