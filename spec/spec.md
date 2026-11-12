---
type: master-requirements
name: spec-objects-security
org: agent-ix
component_type: filament-object-module
implementation_language: markdown
tags:
  - security
  - identity
  - filament-module
depends_on:
  - filament-core-service
standards_alignment:
  - iso-iec-ieee-29148
security_critical: true
---
# Master Requirements Specification

## Purpose

This document specifies the requirements for `spec-objects-security`, a Filament object module that contributes tier-2 security and identity ObjectTypes to filament-core. Security and identity specs need extractable graph entities for threats, controls, risks, vulnerabilities, auth flows, secrets, and policies, and this module makes those concepts first-class, queryable objects rather than free prose so that implementers, reviewers, and agent generators share one authoritative definition of the domain.

## Scope

### In Scope

- The Module manifest this package publishes and its activation against filament-core.
- The 23 tier-2 ObjectTypes the module contributes, covering threats/controls and authentication/authorization (identity folded in per ADR; revisit if identity grows past ~12 types).
- The templates, schemas, and grammars the module ships for those object types.
- The semantic-module contract (issue #13): a TypeSpec source importing
  `@agent-ix/semantic-core`, the emitted JSON Schema per object type
  shipped under `spec_objects_security/schemas/`, the manifest `semantic`
  block with reference-form `data_schema`, the skeletons rewritten as
  executable typed fixtures with negative counterparts, and the
  security-safety rules the schemas encode (no embedded material, closed
  graded vocabularies, no granting default).

### Out of Scope

- The implementation of filament-core-service itself, referenced here only by relationship.
- Deployment topology and infrastructure, which live in the operating environment rather than this specification.
- Generated-language fixtures for the security types: the Rust, TypeScript and
  Python backends are `agent-ix/filament-core-data#21`, `#22` and `#23` over
  the TypeSpec frontend `agent-ix/filament-core-data#19`, and they are
  published only behind the promotion gate (`agent-ix/quoin#290`); the
  semantic-core language packages are `agent-ix/filament-core-data#11`. None is
  produced or faked here.
- Changing this module's `traceability` block, or any `allowed_links` verb or
  target list other than `control.allowed_links.mitigates`, which gains `hazard`
  and `failure_mode` ([FR-007](./functional/FR-007-control-mitigates-safety-objects.md)).
  `agent-ix/spec-objects-safety` reads no field of this manifest; its
  `hazard-has-mitigation` and `failure-mode-has-mitigation` relations are
  declared in its own manifest, and the shared element is the verb `mitigates`,
  owned by `spec-artifacts-iso` FR-004.
- Making `FR` and `NFR` documents able to declare `mitigates`. That belongs to
  `spec-artifacts-iso` and is not made here.
- Reconciling this module's `Severity` and `Likelihood` vocabularies with
  `agent-ix/spec-objects-safety`'s `hazard-severity` and `hazard-likelihood`
  lint columns. The names collide and the member sets are disjoint; a shared
  grading vocabulary is a decision for the two modules' common owner, and
  nothing here depends on the other module's members.
- Holding a copy of the module-manifest schema. The schema is owned by
  `filament-core-data`; this repository commits no copy of it. The manifest is
  checked by the engines that apply it when they read a module (FR-003-AC-7):
  `quire validate --module` refuses an unknown top-level key but accepts bad
  `semantic.*`, and `quoin module install` refuses bad `semantic.*` but accepts
  an unknown top-level key, so together they cover what the schema closes. It is
  also checked by activation (FR-001-AC-2), which needs a running filament-core and is `🚧`
  here.
- Extraction of the declared-but-not-yet-extracted keys (`severity`,
  `likelihood`, `impact`, `status`, `level`, `trust_level`,
  `stride_category`, `effectiveness`, `lifecycle`, `material_ref`, and the
  cross-reference lists) from Markdown. `agent-ix/quoin#335` owns the mapping
  question and the extractor is `agent-ix/quire-rs` once a mapping is
  published, but that ticket's body scopes itself to the ten
  `spec-objects-business` keys and names none of this module's — so these keys
  are disclaimed here and claimed nowhere yet, which is recorded rather than
  assumed away. The schemas declare them as optional so the engine can fill
  them without a schema change, and eight of them carry an item rule over
  `fields` that enforces the obligation today.
- Widening the typed-table constraint reader. `pattern` is in semantic-core's
  closed `ConstraintKeyword` set but the reader of the pinned wheel rejects it
  (`agent-ix/quire-rs#397`), and a multi-valued `enumValues` is either split
  into bogus keywords or silently truncated to its first member
  (`agent-ix/quire-rs#401`, filed by this ticket). Neither is worked around by
  inventing a cell form here; the closed vocabularies live in emitted enum
  schemas instead, and FR-005 says why.
- Naming what a module load refused: `agent-ix/quire-rs#221` (an unknown
  manifest key empties the model silently) and `agent-ix/quire-rs#394`.
  FR-003-AC-6's "naming the key or the path" half is blocked on them and is
  carried as an explicit expected failure.
- Resolving a reference-form `data_schema` into a stored snapshot at
  activation: `agent-ix/filament-core-service#23`. Until it lands the service
  stores the reference verbatim.
- Editing any corpus repository or vendored fixture; the legacy-form sweep
  and corpus promotion (`agent-ix/quoin#291`).
- Hosting the semantic-core schema bundle. Every module schema `$ref`s
  `https://schemas.agent-ix.org/semantic-core/<declared version>/<Model>.json`, and nothing
  in this repository serves that host; a consumer resolves it from the
  `@agent-ix/semantic-core` package, and publishing the bundle is
  `agent-ix/filament-core-data#11`. The module's own tests resolve every such
  reference against the installed package rather than over the network, and
  say so.
- Runtime security enforcement: nothing here authenticates, authorizes, or
  encrypts anything. The module declares the vocabulary a specification uses
  to describe those mechanisms.

## System Overview

### System Description

The module is consumed as a Filament Module: its manifest is activated against filament-core-service, after which the declared archetypes, object types, grammars, and artifact types become discoverable through the platform's object graph and available to downstream editors and agent CLI generators.

### Intended Users

The Filament platform, its spec authors, and its agent CLI generators (minijinja-cli), which rely on the module's contributions to author and validate security and identity artifacts.

## Requirements Architecture

The specification is organized into the standard requirement classes, each in its own directory:

- `stakeholder/` — StR-XXX stakeholder requirements.
- `functional/` — FR-XXX functional requirements.
- `integration/` — IT-XXX integration tests.
- `usecase/` — US-XXX user stories.
- `tests.md` — the per-repo test matrix tracing functional requirements to their tests.

FR-001 activates the manifest against `filament-core`; FR-002 emits the
schemas; FR-003 declares the semantic contract in the manifest; FR-004 fixes
each type's role-distinct schema; FR-005 makes the skeletons executable
fixtures; FR-006 encodes the module's security rules into those schemas.
Integration tests in
`integration/` verify the activation and Quoin-install boundaries; the third
external boundary, the Quire engine (loader, extraction, record surface), has
no IT artifact of its own — the FR-003, FR-005 and FR-006 test harness is this
module's Quire contract test, and the wheel version is pinned once in FR-005
Inputs.

## References

- ISO/IEC/IEEE 29148 — Requirements engineering.
- `agent-ix/filament-core-data` — owner of the module-manifest schema.
- The component's source repository and README.
- `agent-ix/filament-core-data` FR-031..FR-034 (semantic-core grammar,
  scalars, JSON Schema projection, lowering) and ADR-0005 (TypeSpec source).
- `agent-ix/quoin` FR-070..FR-075 (semantic-module contract, mappings,
  `data_schema`, legacy forms, package manifests).
- `agent-ix/quire-rs` FR-069..FR-072 (contract at load, typed Properties,
  clauses and operations, extraction surface).
- `agent-ix/spec-objects-business#4`, the reference migration this module follows.
