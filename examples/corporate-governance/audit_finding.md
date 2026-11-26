---
id: CG-FIND-001
title: "SyntheticAccessReviewGap"
type: audit_finding
object: audit_finding
relationships:
  - target: CG-RISK-001
    type: traces_to
  - target: CG-CTRL-001
    type: references
---
# [CG-FIND-001] SyntheticAccessReviewGap

## Recommendation

Record an owner for each privileged access review and verify completion
quarterly.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| finding_id | UUID | 1..1 | identity |
| status | String | 1..1 | minLength: 1 |
| observed_at | Timestamp | 1..1 |  |
