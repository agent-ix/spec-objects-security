---
id: FR-024
title: "A trust_boundary states its trust level as a required frontmatter value"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: depends_on
  - target: "ix://agent-ix/spec-objects-security/FR-023"
    type: depends_on
  - target: "ix://agent-ix/spec-objects-architecture/FR-014"
    type: depends_on
---
# FR-024: A trust_boundary states its trust level as a required frontmatter value

## Description

A trust boundary identifies the zone on its far side and the trust given to that zone. A field row in `## Properties` describes a value but does not supply the value to consumers. The authored boundary therefore states `trust_level` in frontmatter, where the extractor places it in the typed `TrustBoundary` record. Connection crossings are relationship edges owned by the connection and are specified by spec-objects-architecture FR-014; `TrustBoundary` carries no `crosses` record key.

## Behavior

- Each `trust_boundary` SHALL author frontmatter `trust_level` with exactly one value from the existing `TrustLevel` enumeration: `untrusted`, `semi_trusted`, `trusted`, or `unknown`.
- The manifest locator for `trust_boundary` SHALL require frontmatter `trust_level`.
- The manifest locator for `trust_boundary` SHALL extract frontmatter `trust_level` to the record key `trust_level`.
- A missing `trust_level` SHALL make `quire validate` fail with a diagnostic naming `trust_level`.
- An out-of-vocabulary value SHALL make `quire validate` fail with a diagnostic naming the value.
- The emitted `TrustBoundary` schema SHALL admit the typed `trust_level` key.
- The emitted `TrustBoundary` schema SHALL reject the retired `crosses` record key. Crossing relationships are authored on connections.
- The existing `fields` row for `trust_level` remains required by FR-004-AC-10 and its `TrustLevelField` item rule. The row and the frontmatter value serve distinct purposes: the row documents a boundary property, while the frontmatter value is the extracted machine-readable value.
- The trust-boundary skeleton SHALL include a valid frontmatter `trust_level`.
- No trust level is inferred from a boundary name, diagram, relation, or property row.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-024-AC-1 | A `trust_boundary` with a valid `trust_level` frontmatter value passes `quire validate`. | Test |
| FR-024-AC-2 | A `trust_boundary` without frontmatter `trust_level` fails validation and names the missing field. | Test |
| FR-024-AC-3 | A `trust_level` outside `untrusted`, `semi_trusted`, `trusted`, and `unknown` fails validation and names the value. | Test |
| FR-024-AC-4 | `trust_level: untrusted` is extracted as the record key `trust_level` with value `untrusted`. | Test |
| FR-024-AC-5 | The `TrustBoundary` schema rejects a record containing `crosses`, while a valid typed `trust_level` is admitted; the `TrustLevelField` item rule remains. | Test |
| FR-024-AC-6 | The trust-boundary skeleton carries valid frontmatter `trust_level` and validates. | Test |
| FR-024-AC-7 | A trust level is not derived from the `## Properties` row: removing frontmatter leaves no extracted `trust_level` and validation fails. | Test |

## Dependencies

- FR-004 defines the `TrustBoundary` record shape and the `TrustLevelField` item rule.
- FR-023 defines the security module's typed frontmatter extraction pattern for authored enum values.
- spec-objects-architecture FR-014 owns the connection-to-boundary `crosses` edge and its relation report.

## Licensing

Use generic terms only. Do not name or quote paywalled standards.
