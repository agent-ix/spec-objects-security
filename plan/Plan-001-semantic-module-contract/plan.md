---
id: Plan-001
title: "spec-objects-security — semantic module contract (issue #13)"
type: Plan
status: active
relationships:
  - target: ix://agent-ix/spec-objects-security/StR-001
    type: references
  - target: ix://agent-ix/spec-objects-security/US-001
    type: references
  - target: ix://agent-ix/spec-objects-security/FR-001
    type: references
  - target: ix://agent-ix/spec-objects-security/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-security/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-security/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-security/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-security/FR-006
    type: references
  - target: ix://agent-ix/spec-objects-security/NFR-001
    type: references
  - target: ix://agent-ix/spec-objects-security/IT-001
    type: references
  - target: ix://agent-ix/spec-objects-security/IT-002
    type: references
---
# Implementation Plan: semantic module contract

## Requirements Summary

`[x]` delivered and verified in this repository. `[~]` partly delivered: the
remainder needs a running `filament-core-service`, a Quoin built from `quoin`
main, or a human, and is owned by the two `blocked` tasks.

### Stakeholder Requirements
- [~] **StR-001**: Security and identity specifications yield extractable graph entities; every security object carries one typed structural contract downstream frontends can read (VC-1..VC-3).

### User Stories
- [x] **US-001**: Declare every security object type against the shared semantic-core grammar, so one declaration record per object validates identically in Quire, Quoin and the compiler.

### Functional Requirements
- [~] **FR-001**: The manifest conforms to filament-core-service FR-035 and activates idempotently.
- [x] **FR-002**: Emit one JSON Schema 2020-12 document per model from `typespec/main.tsp` with the official emitter at a pinned toolchain; normalize `$id`/`$ref`; gate drift; package into the wheel and the npm tarball; version-embedded `$id` with an atomic bump procedure.
- [x] **FR-003**: `manifest.yaml` at 0.2.0 carries the quoin FR-070 `semantic` block and a reference-form `data_schema` per exported type, with every 0.1.0 locator, the `traceability` block, the `lexicon` and every `allowed_links`/`roles` map unchanged.
- [x] **FR-004**: One role-distinct model per security object type — required keys, sealed key set and item rules — with every grammar item by `$ref` to semantic-core 0.1.0.
- [x] **FR-005**: Every skeleton is an executable typed fixture in the quoin FR-071/FR-072 Markdown forms, with three `sysml` alternates and ten negative fixtures; the semantic suite fails rather than skips when the engine is absent.
- [x] **FR-006**: No embedded material, ten closed graded vocabularies each with an explicit unassessed member, and no schema default that grants permission, trust or control effectiveness.

### Non-Functional Requirements
- [x] **NFR-001**: Additive compatibility — the frozen 0.1.0 skeleton set still validates at 0.2.0 and every 0.1.0 locator and edge-vocabulary entry is unchanged.

### Integration Test Requirements
- [~] **IT-001**: Activation roundtrip against a running filament-core-service.
- [~] **IT-002**: `quoin module install path:<dir>` accepts the semantic contract and the prior module state is restored unconditionally.

## Dependency Graph

### Core dependency edges

- `FR-002 (toolchain half) -> FR-004`
  Reason: no model can be authored until `tsp compile` runs against
  `@agent-ix/semantic-core` 0.1.0 and the generator normalizes what it emits.
- `FR-004 -> FR-002 (emitted-set half)`
  Reason: FR-002-AC-1/AC-2/AC-3 assert the emitted file set, its `$id`s and its
  `$ref`s, none of which exist before FR-004 declares the models. The apparent
  cycle is broken by splitting FR-002 into an enablement half (generator, drift
  gate, packaging) that precedes FR-004 and an emitted-set half that follows
  it; FR-002 `depends_on` FR-004 in the frontmatter.
- `FR-004 -> FR-006 -> FR-004 (encoding)`
  Reason: FR-006 constrains how FR-004's negative item rules are encoded
  (`items`/`not`, never `minContains`) and adds the operations-parameter guard,
  while FR-004 declares the models FR-006 constrains. Broken by ordering:
  Task-002 authors the models under the FR-006 encoding rule from the start, so
  no model is ever emitted with a counting predicate that a later task removes.
- `FR-002 (emitted set) + FR-001 -> FR-003`
  Reason: the manifest references the emitted files by path and digest, and the
  0.2.0 manifest must still be an FR-035-valid manifest.
- `FR-003 + FR-004 -> FR-005`
  Reason: a skeleton validates only once the archetype loads with its schema,
  and the negative fixtures pin refusals the FR-004 rules define.
- `FR-005 -> FR-003 (added locators)`
  Reason: the `required: false` locators the manifest gains exist to assert
  sections the skeletons introduce, so the section lands before its locator.
- `FR-003 + FR-005 -> NFR-001`
  Reason: the compatibility metrics compare the frozen 0.1.0 baseline against
  the finished 0.2.0 manifest and its loader behaviour. The baseline must be
  frozen **before** the manifest is edited, which is why Task-000 exists.
- `FR-003 -> IT-002`
  Reason: the Quoin install exercises the finished `semantic` block and digests.

### External dependencies

| Dependency | Owner | Effect if unresolved |
|---|---|---|
| Quire 0.46.0 on a committable index | `agent-ix/quire-rs#392` | `quire` stays undeclared; `make dev-quire` provisions it and the suite fails rather than skips |
| FR-035 schema release carrying CR-012 | `agent-ix/spec-artifacts-iso#36` | the gate runs against a pinned copy, with a test proving the pin's delta |
| Naming a refused module load / digest | `agent-ix/quire-rs#221`, `#394` | FR-003-AC-6's naming half is a strict expected failure |
| Record validation of a legacy `object:` form | `agent-ix/quire-rs#391` | carried as a strict expected failure beside NFR-001-AC-4 |
| Multi-valued `enumValues` in a Constraints cell | `agent-ix/quire-rs#401` | closed vocabularies live in emitted enum schemas, not in cells |
| `pattern` refused by the constraint reader | `agent-ix/quire-rs#397` | no skeleton uses `pattern` |
| Markdown mapping for the graded keys | `agent-ix/quoin#335` | every graded key is optional; eight carry an item rule over `fields` instead |
| Reference-form `data_schema` resolved at activation | `agent-ix/filament-core-service#23` | the service stores the reference verbatim |
| Generated-language fixtures | `agent-ix/filament-core-data#19`/`#21`/`#22`/`#23`, `agent-ix/quoin#290` | none is produced or faked here |

## Execution Tracks

**Track A (critical path)** — Task-000, Task-001, Task-002, Task-003, Task-004, Task-005, Task-006.
**Track B (parallel with A once Task-002 lands)** — Task-007, Task-008.
**Track C (post-critical-path)** — Task-009, Task-010.

## Quality Gates

- **Gate 1 (after Task-002)**: three types spanning the three shapes — a
  catalogued identity (`Asset`), a governing rule (`Control`) and the occurrence
  declaration (`AuditEvent`) — validate hand-built records against the real
  2020-12 validator with the schemas sealed, including the multi-predicate
  `allOf` and the `items`/`not` negatives. The remaining twenty types are gated
  on it because the encoding they all rest on is unprototyped in this module.
- **Gate 2 (before the PR)**: `make lint` and `make test` green with zero
  skipped tests, `quire validate` over `spec/` and `plan/` structurally clean,
  and `quire coverage` reconciled against `spec/tests.md`.

## Test Plan

Every `TC` id of `spec/tests.md` is owned by exactly one task; the mapping is
authoritative in each task's `verifies` frontmatter rather than repeated here.
Rows that no task can discharge in this repository — TC-015..TC-019, TC-046,
TC-110, TC-112, TC-113 — are owned by Task-009 and Task-010 and stay `🚧` with
their blocking environment named on the row.
