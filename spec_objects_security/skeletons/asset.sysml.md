---
id: ASSET-001
title: "TenantDatabase"
type: asset
object: asset
---
<!-- asset authoring skeleton, alternate Properties form. Declares exactly the
     same fields as asset.md, authored as one ```sysml``` fence instead of the
     typed table (FR-005-AC-2). One artifact carries one form; the alternate is
     a separate file, never a second block in the same artifact. -->
# [ASSET-001] TenantDatabase

## Description

The per-tenant PostgreSQL database holding customer records, order history and
audit trails. It is the primary confidentiality and integrity asset of the
platform: its compromise discloses every tenant's data at once.

## Properties

```sysml
attribute asset_id : UUID[1..1] { identity }
attribute name : String[1..1] { minLength: 1, maxLength: 128 }
ref item classification : DataRestricted[1..1]
attribute steward : String[1..1] { minLength: 1 }
attribute replica_count : Integer[0..1] { min: 0 }
```
