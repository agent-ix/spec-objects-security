---
id: US-001
title: "Declare security object types against semantic-core"
type: US
relationships:
  - target: "ix://agent-ix/spec-objects-security/StR-001"
    type: "traces_to"
---
# US-001: Declare security object types against semantic-core

## Story

**As a** maintainer of the security object module
**I want** every security object type — identities and grants, secrets and keys, policies and controls, threats, vulnerabilities, risks, assets, trust boundaries, audit events and findings — to carry a real structural contract expressed in the shared semantic-core grammar
**So that** spec authors write one typed `## Properties` table per object, reviewers and generators read one declaration record per object, and the same record validates identically in Quire, Quoin, and the compiler.

The story is stated from the maintainer's perspective and does not prescribe
the emitter, the file layout, or the extraction engine.

## Context

Today all twenty-three object types in `manifest.yaml` carry
`data_schema: {type: object}`, which types nothing: a `secret` and a `risk` are
indistinguishable to a consumer, every `## Properties` equivalent is free
prose, and no cross-reference between two objects is checked. For a security
module the consequence is sharper than for a business one — nothing stops a
fixture from embedding a credential value, nothing stops a control from
claiming an effectiveness it was never assessed for, and an unrecognised
severity token reads as data rather than as a refusal.

The semantic-core grammar (`agent-ix/filament-core-data#35`) and the
semantic-module contract (`agent-ix/quoin#293`, `agent-ix/quire-rs#388`) now
exist and are merged. `agent-ix/spec-objects-business#4` is the reference
migration this story follows.

## Acceptance Examples (Illustrative)

These examples clarify the maintainer's expectations. They are illustrative
only, not test cases and not verification criteria.

### US-001-EX-1: A threat skeleton extracts to typed fields

- **Given** the `threat` skeleton with a `| Field | Type | Multiplicity | Constraints |` table
- **When** Quire extracts it under this module
- **Then** the record carries one `FieldDecl` per row, the identity row is flagged, and the record validates against the shipped `Threat.json`

### US-001-EX-2: A secret declaration carrying a literal value is refused

- **Given** a `secret` artifact whose typed table gives a field a default value
- **When** Quire validates it
- **Then** validation fails naming the secret schema, because a secret declaration references its material and never carries it

### US-001-EX-3: An unrecognised severity is refused rather than stored

- **Given** a vulnerability record whose `severity` is `catastrophic`
- **When** it is validated against `Vulnerability.json`
- **Then** validation fails, while the same record with `unknown` validates — an unassessed state is stated, never inferred

## Options (Exploratory)

Approaches discussed: hand-authoring one JSON Schema per type; generating the
schemas from a TypeSpec package that imports `@agent-ix/semantic-core`;
deriving the schemas from the skeletons. Only the TypeSpec route keeps one
source for the grammar and its vocabulary; it is the route the authoring
contract on the ticket already names.

## Constraints (Contextual)

No corpus repository may be edited; existing `body_extraction` locators stay
as they are so current artifacts keep extracting; the `traceability` and
`allowed_links` blocks stay byte-identical because `agent-ix/spec-objects-safety`
reads them for bidirectional hazard coverage; the change is advisory until
corpus promotion. This context is not binding here and is refined in the
functional and non-functional requirements.

## Dependencies (Contextual)

Upstream: semantic-core 0.1.0 on npm.ix, the module-manifest schema with the
`semantic` block, Quire 0.46.0 with `extract_semantic`. Downstream: the
frontends that read this module's skeletons as fixtures.

## Priority and Risk (Informative)

P1 on the Track A programme. The risk if unmet is that the security domain has
no typed fixture set, and that the module's security-relevant rules — no
embedded material, no granted-by-default state — stay prose that nothing
enforces.

## Notes (Informative)

Open question captured for later analysis: which sections beyond
`## Properties`, `## Invariants`, and `## Operations` the extraction engine
should read. The schemas declare the graded keys (`severity`, `likelihood`,
`impact`, `effectiveness`, `status`, `level`, `trust_level`, `lifecycle`);
extraction of them is an engine concern, so each is optional and the
corresponding obligation is carried today as an item rule over `fields`.

## Traceability (Informative)

Traces to [StR-001](../stakeholder/StR-001-module-activation.md); implemented
by [FR-002](../functional/FR-002-emitted-json-schemas.md),
[FR-003](../functional/FR-003-semantic-manifest-contract.md),
[FR-004](../functional/FR-004-role-schemas.md),
[FR-005](../functional/FR-005-executable-skeletons.md), and
[FR-006](../functional/FR-006-security-safe-declarations.md).
