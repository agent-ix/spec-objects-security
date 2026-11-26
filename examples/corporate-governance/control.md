---
id: CG-CTRL-001
title: "SyntheticPrivilegedAccessReview"
type: control
object: control
option_type: protective
safeguards: [validate-before-display]
relationships:
  - target: CG-POL-001
    type: implements
  - target: CG-RISK-001
    type: mitigates
---
# [CG-CTRL-001] SyntheticPrivilegedAccessReview

## Effectiveness

`not_assessed`

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| control_id | UUID | 1..1 | identity |
| effectiveness | String | 1..1 | minLength: 1 |
| owner | String | 1..1 | minLength: 1 |

## Invariants

### AccessReviewHasAnOwner

```ocl
context SyntheticPrivilegedAccessReview
inv AccessReviewHasAnOwner:
  self.owner->notEmpty()
```
