---
id: NFR-002
title: "Published profiles name no licensed pack and carry no standard text"
type: NFR
quality_attribute: compliance
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-020"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-security/FR-021"
    type: "constrains"
---
# NFR-002: Published profiles name no licensed pack and carry no standard text

## Statement

Every file under `profiles/` SHALL contain only clause-set keys, a context map and descriptive prose about the profile.

A file under `profiles/` SHALL name no pack whose source text is licensed.

## Scope

- Applies to: shipped profile files and the profile JSON Schema.
- Out of scope: local configuration files outside this repository.

## Rationale

A published name or sentence from a licensed standard is a disclosure that cannot be undone in git history. A licensed
pack joins a profile only through local configuration ([quoin FR-182](ix://agent-ix/quoin/FR-182)).

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| Shipped profile keys outside `schemaVersion`, `name`, `title`, `description`, `clauseSets`, `context` | 0 | 0 | Test |
| Shipped profile entries whose declaring module fails `quire publish-check` | 0 | 0 | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-002-AC-1 | Parsing every shipped profile finds no top-level key outside the six listed and no `clauseSets` entry field outside `authority`, `id`, `version`. | Test |
| NFR-002-AC-2 | `quire publish-check --module <declaring module>` exits 0 for the declaring module of every key in every shipped profile; no authority list is kept in the test. | Test |

## Verification

Both criteria are tests over the shipped profile files; the licence signal is the engine's publishability check alone.

## Dependencies

- **Upstream**: [FR-020](../functional/FR-020-source-profile-format.md), [FR-021](../functional/FR-021-default-source-profiles.md)
