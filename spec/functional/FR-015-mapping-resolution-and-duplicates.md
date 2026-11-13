---
id: FR-015
title: "A mapping to a loaded clause set must name a clause of it, and a mapping is stated once"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-014"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-083"
    type: "references"
---
# FR-015: A mapping to a loaded clause set must name a clause of it, and a mapping is stated once

## Description

A mapping ([FR-014](./FR-014-control-mappings-are-clause-references.md)) names a clause set that might not be
installed where the spec is validated. A licensed set is installed only on a machine that holds its pack, so a
public repository's CI cannot load it. The module therefore checks a mapping only against sets it can see and never
reports a set it cannot see.

## Behavior

- Quire SHALL report a mapping whose `set` is a loaded clause set and whose `clause` is not a clause of that set, as an error `control-mapping-clause-unresolved` naming the control, the set key and the clause id.
- Quire SHALL report nothing about a mapping whose `set` is not loaded.
- Quire SHALL report two rows of one control with the same `set` and `clause` as an error `control-mapping-duplicate`, naming both rows.
- Quire SHALL treat the same clause in two different controls as valid, because several controls answer one clause.
- The two findings SHALL carry no text of the clause.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-015-AC-1 | With a synthetic clause set `example.invalid/std@1` loaded, a control mapping to a clause it does not contain yields exactly one `control-mapping-clause-unresolved` error naming control, set key and clause id. | Test |
| FR-015-AC-2 | With the set loaded, a control mapping to a clause it contains yields no finding. | Test |
| FR-015-AC-3 | With the set not loaded, the same control yields no finding about the mapping and validation exits 0. | Test |
| FR-015-AC-4 | Two identical rows in one control yield one `control-mapping-duplicate` error; the same row in two controls yields none. | Test |
| FR-015-AC-5 | No finding output contains the clause-text sentinel of the loaded synthetic set. | Test |

## Dependencies

- **Upstream**: [FR-014](./FR-014-control-mappings-are-clause-references.md); `agent-ix/quire-rs` FR-083 (clause sets and their rights)
- **Downstream**: none
