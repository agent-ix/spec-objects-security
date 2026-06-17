---
id: StR-001
title: "Tier-2 security + identity objects"
type: StR
---
# [StR-001] Tier-2 security + identity objects

## Stakeholder Need

The Filament platform, its spec authors, and its agent CLI generators **SHALL** be able to extract graph entities from security and identity specifications — threats, controls, risks, vulnerabilities, auth flows, secrets, and policies — so that those concepts are first-class, queryable objects rather than free prose.

## Rationale

Security and identity content is currently expressed as unstructured narrative, which cannot be traced, queried, or generated against. Without extractable object types for the tier-2 security domain, downstream consumers (editors, agent generators, the object graph) have no way to discover or reason about the threats, controls, risks, vulnerabilities, auth flows, secrets, and policies a spec declares. Providing this need as installable Module contributions makes the domain machine-addressable.

## Validation Criteria

This need is considered satisfied when:

- A Module activation against filament-core registers the contents this module declares.
- Agent CLI generators (minijinja-cli) can produce valid artifacts using the templates and schemas this module ships.

## Dependencies

- **Upstream**: filament-core-service FR-035 (Module Manifest Schema)
