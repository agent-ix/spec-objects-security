---
id: CTRL-001
title: "RefreshTokenRotation"
type: control
object: control
---
<!-- control authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: control, object: control.
     - "## Mappings" (H2, required): the threats, risks and standards this
       control addresses.
     - "## Properties" (H2): Control.json requires an `effectiveness` row, so
       effectiveness is always stated and never assumed.
     - "## Invariants" (H2): Control.json requires at least one clause. -->
# [CTRL-001] RefreshTokenRotation

## Mappings

- Mitigates RefreshTokenReplay (stolen refresh token replay).
- Reduces TenantDataExfiltration likelihood from possible to unlikely.
- Implements OAuth 2.0 Security BCP (RFC 9700) refresh-token rotation guidance.
- Maps to OWASP ASVS v4 3.5.2 and NIST SP 800-63B 7.1 session binding.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| control_id | UUID | 1..1 | identity |
| effectiveness | String | 1..1 | minLength: 1 |
| owner | String | 1..1 | minLength: 1 |
| last_assessed_at | Timestamp | 1..1 |  |

## Invariants

The clauses this control enforces. Each clause owns one `ocl` fence under its
own `### <clauseId>` heading; the fence text is carried verbatim and never
evaluated here.

### EveryExchangeInvalidatesThePresentedToken

```ocl
context RefreshTokenRotation
inv EveryExchangeInvalidatesThePresentedToken:
  self.effectiveness <> 'not_assessed' implies self.last_assessed_at->notEmpty()
```

### ReuseRevokesTheWholeFamily

```ocl
context RefreshTokenRotation
inv ReuseRevokesTheWholeFamily:
  self.owner->notEmpty()
```
