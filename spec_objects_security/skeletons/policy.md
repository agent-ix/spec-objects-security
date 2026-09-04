---
id: POL-001
title: "LeastPrivilegeAccessPolicy"
type: policy
object: policy
---
<!-- policy authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: policy, object: policy.
     - "## Policy" (H2, required): the rule in prose.
     - "## Invariants" (H2): Policy.json requires at least one clause — a
       policy that constrains nothing is prose. -->
# [POL-001] LeastPrivilegeAccessPolicy

## Policy

Every principal holds the smallest set of permissions that lets it complete
its task, for the shortest time that task takes. A grant that is not exercised
within 90 days is revoked automatically, and every standing administrative
grant is reviewed quarterly by the tenant owner.

## Invariants

The clauses this policy asserts. Each clause owns one `ocl` fence under its
own `### <clauseId>` heading.

### NoStandingAdministrativeGrant

```ocl
context LeastPrivilegeAccessPolicy
inv NoStandingAdministrativeGrant:
  TenantAdministrator.allInstances()->forAll(r | r.assignable_by_self_service = false)
```

### UnusedGrantsExpire

```ocl
context LeastPrivilegeAccessPolicy
inv UnusedGrantsExpire:
  TenantReadScope.allInstances()->forAll(s | s.includes_write = false)
```
