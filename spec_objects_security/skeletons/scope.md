---
id: SCOPE-001
title: "TenantReadScope"
type: scope
object: scope
---
<!-- scope authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: scope, object: scope.
     - "## Grants" (H2, required): what a bearer of this scope may do.
     - "## Properties" (H2): the typed declaration. -->
# [SCOPE-001] TenantReadScope

## Grants

- Read access to the tenant's own records and audit trail.
- No write, no export, and no access to any other tenant.
- Downgrades to nothing when the grant family is revoked.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| scope_id | UUID | 1..1 | identity |
| name | String | 1..1 | minLength: 1, maxLength: 64 |
| includes_write | Boolean | 1..1 |  |
