---
id: CORS-001
title: "TenantApiCorsPolicy"
type: cors_policy
object: cors_policy
---
<!-- cors_policy authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: cors_policy,
       object: cors_policy.
     - "## Origins" (H2, required): the allowed origins.
     - "## Invariants" (H2): CorsPolicy.json requires at least one clause. -->
# [CORS-001] TenantApiCorsPolicy

## Origins

- `https://app.example.com` — the first-party tenant console.
- `https://*.tenant.example.com` — per-tenant vanity hosts, exact-suffix matched.
- No wildcard origin, and no origin is echoed back unvalidated.

## Invariants

The clauses this policy asserts. Each clause owns one `ocl` fence under its
own `### <clauseId>` heading.

### NoWildcardOrigin

```ocl
context TenantApiCorsPolicy
inv NoWildcardOrigin:
  self.allowed_origins->excludes('*')
```

### CredentialsNeverWithWildcard

```ocl
context TenantApiCorsPolicy
inv CredentialsNeverWithWildcard:
  self.allow_credentials implies self.allowed_origins->size() > 0
```
