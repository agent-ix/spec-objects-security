---
id: PWD-001
title: "TenantPasswordPolicy"
type: password_policy
object: password_policy
---
<!-- password_policy authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: password_policy,
       object: password_policy.
     - "## Rules" (H2, required): the rules in prose.
     - "## Invariants" (H2): PasswordPolicy.json requires at least one clause. -->
# [PWD-001] TenantPasswordPolicy

## Rules

- At least 12 characters, with no composition rule beyond length.
- Checked against the breached-password corpus at set time and at each login.
- No forced periodic expiry; rotation is event-driven on suspected compromise.
- Stored only as an Argon2id digest, never reversibly.

## Invariants

The clauses this policy asserts. Each clause owns one `ocl` fence under its
own `### <clauseId>` heading.

### MinimumLengthIsTwelve

```ocl
context TenantPasswordPolicy
inv MinimumLengthIsTwelve:
  self.minimum_length >= 12
```

### NoReversibleStorage

```ocl
context TenantPasswordPolicy
inv NoReversibleStorage:
  self.storage_scheme = 'argon2id'
```
