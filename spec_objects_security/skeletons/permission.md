---
id: PERM-001
title: "ExportTenantData"
type: permission
object: permission
resource: "tenant/records"
verb: export
---
<!-- permission authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: permission, object: permission,
       resource (what is acted on) and verb (the action).
     - "## Properties" (H2): the typed declaration. Permission.json forbids
       `operations` and `relations`. -->
# [PERM-001] ExportTenantData

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| permission_id | UUID | 1..1 | identity |
| resource | String | 1..1 | minLength: 1 |
| verb | String | 1..1 | minLength: 1 |
| requires_reauthentication | Boolean | 1..1 |  |
