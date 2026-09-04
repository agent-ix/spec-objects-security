---
id: ROLE-001
title: "TenantAdministrator"
type: role
object: role
---
<!-- role authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: role, object: role.
     - "## Permissions" (H2, required): the permissions this role grants.
     - "## Properties" (H2): the typed declaration. A role is a grant set,
       so Role.json forbids `operations`. -->
# [ROLE-001] TenantAdministrator

## Permissions

- ExportTenantData — export the tenant's records for portability requests.
- Manage tenant members, their roles and their MFA enrolment.
- Read the tenant audit trail; the role grants no write on it.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| role_id | UUID | 1..1 | identity |
| name | String | 1..1 | minLength: 1, maxLength: 64 |
| granted_permission | ExportTenantData | 0..1 |  |
| assignable_by_self_service | Boolean | 1..1 |  |
