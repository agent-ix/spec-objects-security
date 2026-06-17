---
id: IT-001
title: "Manifest activation roundtrip against filament-core"
type: IT
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-001"
    type: "verifies"
---
# [IT-001] Manifest activation roundtrip

## Objective

Verify that this Module's manifest activates end to end against a clean filament-core-service instance, that every declared contribution lands in the database, and that re-activation is an idempotent no-op. This exercises [FR-001](../functional/FR-001-module-manifest-activates.md) across the real activation boundary.

## Target Integration

The system under test is filament-core-service, reached over its HTTP API. The integration exercised is the manifest activation call `POST /api/v1/modules/activate` followed by reads of the `/api/v1/archetypes`, `/api/v1/object-types`, `/api/v1/grammars`, and `/api/v1/artifact-types` endpoints that surface the persisted contributions.

## Preconditions

A filament-core-service instance is deployed to a clean cluster (or the kind dev cluster) and reachable, with an empty `modules` table so that the presence of newly created rows is meaningful for this run.

## Inputs

The activation payload is this repo's packaged manifest, `spec_objects_security/manifest.yaml`, declaring the module's archetypes, object types, grammars, and artifact types.

## Test Procedure

Each step performs one discrete action against the running service.

1. Deploy filament-core-service to a clean cluster (or use the kind dev cluster).
2. POST `spec_objects_security/manifest.yaml` to `/api/v1/modules/activate`.
3. Assert 200 OK and that a `modules` row was created.
4. GET `/api/v1/archetypes`, `/api/v1/object-types`, `/api/v1/grammars`, and `/api/v1/artifact-types`.
5. Assert each declared item is present with the correct attributes.
6. Re-POST the same manifest and assert an idempotent no-op (same `modules.id`, no row duplication).

## Expected Results

Activation succeeds, every archetype, object type, grammar, and artifact type the manifest declares is present in the corresponding filament-core table, and re-activation produces the same content hash without duplicating rows. The test passes only when all of the following hold:

| ID | Criteria |
|----|----------|
| IT-001-AC-1 | All assertions in steps 3-6 pass |
| IT-001-AC-2 | Re-activation produces the same SHA-256 content hash |
