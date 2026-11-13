---
id: CTRL-001
title: "RefreshTokenRotation"
type: control
object: control
---
<!-- control authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: control, object: control.
     - "## Mappings" (H2, optional): a Set / Clause table, one row per clause
       of a clause set this control answers. Set is the key
       authority/id@version; no standard text belongs here. Threats and risks
       are `mitigates` relationships, not mapping rows.
     - "## Effectiveness" (H2, optional): one inline-code ControlEffectiveness
       value; `not_assessed` unless a person states another.
     - "## Properties" (H2): Control.json requires an `effectiveness` row, so
       effectiveness is always stated and never assumed.
     - "## Invariants" (H2): Control.json requires at least one clause. -->
# [CTRL-001] RefreshTokenRotation

## Mappings

| Set | Clause |
|---|---|
| example.invalid/std@1 | EX-1 |
| example.invalid/std@1 | EX-2 |

## Effectiveness

`not_assessed`

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
