---
id: CG-RISK-001
title: "SyntheticUnauthorizedApprovalRisk"
type: risk
object: risk
likelihood: possible
impact: moderate
decision: undecided
relationships:
  - target: CG-THREAT-001
    type: arises_from
---
# [CG-RISK-001] SyntheticUnauthorizedApprovalRisk

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| risk_id | UUID | 1..1 | identity |
| likelihood | String | 1..1 | minLength: 1 |
| impact | String | 1..1 | minLength: 1 |
| assessed_at | Timestamp | 1..1 |  |
