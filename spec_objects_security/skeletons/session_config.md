---
id: SESS-001
title: "TenantSessionConfig"
type: session_config
object: session_config
---
<!-- session_config authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: session_config,
       object: session_config.
     - "## Settings" (H2, required): the settings in prose.
     - "## Invariants" (H2): SessionConfig.json requires at least one clause. -->
# [SESS-001] TenantSessionConfig

## Settings

- Idle timeout 30 minutes; absolute lifetime 12 hours.
- Cookie flags `HttpOnly`, `Secure`, `SameSite=Lax`, host-only.
- Session identifier rotates on every privilege change.
- Bound to AuthorizationCodeWithPkce; no session outlives its grant family.

## Invariants

The clauses this configuration asserts. Each clause owns one `ocl` fence under
its own `### <clauseId>` heading.

### IdleTimeoutIsShorterThanAbsoluteLifetime

```ocl
context TenantSessionConfig
inv IdleTimeoutIsShorterThanAbsoluteLifetime:
  self.idle_timeout < self.absolute_lifetime
```

### IdentifierRotatesOnPrivilegeChange

```ocl
context TenantSessionConfig
inv IdentifierRotatesOnPrivilegeChange:
  self.rotate_on_privilege_change
```
