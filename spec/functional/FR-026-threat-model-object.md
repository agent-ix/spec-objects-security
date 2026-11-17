---
id: FR-026
title: "A threat_model states its method, who led it, what it covers and which threats it considers"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-005"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-006"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-025"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/NFR-005"
    type: "constrained_by"
---
# FR-026: A threat_model states its method, who led it, what it covers and which threats it considers

## Description

The model already records what data each connection carries, which trust boundaries it crosses, where data lands and which
controls protect it. The module already has `threat`, `control`, `risk` and `asset`. Nothing yet says which part of the model
a person has analysed for threats, so no rule can ask "was this crossing considered?". The module SHALL add a
`threat_model` object type that scopes an analysis to the parts of the model it covers and names the threats it considered.

A `threat_model` is a document a person writes. It does not generate threats, rate them or conclude that a system is secure.
The method names a free, public technique: STRIDE applied per element or per interaction, as described in OWASP's free
threat-modelling guidance and in NIST SP 800-154 (free). This requirement names and quotes no paywalled standard.

The `covers` verb is owned by spec-artifacts-iso as a generic traceability relation (a source document covers a target).
This module reuses that canonical edge and SHALL NOT declare a duplicate. A resolved module set loading this module SHALL
include spec-artifacts-iso. This requirement declares the new verb `considers` in this module's `edge_types` block, with a
description (a threat model considers a threat). The objects `connection`, `data_sink` and `part`, and the `crosses` edge, are owned by
`agent-ix/spec-objects-architecture` (PR #51 / PLAT-1532 and PR #52 / PLAT-1440); `trust_boundary` is declared by this
module. This requirement names no requirement id for the architecture objects until those land.

## Inputs

- A `threat_model` document: frontmatter `id`, `title`, `type: threat_model`, `object: threat_model`, `method`,
  `reviewed_by`; edges `covers` and `considers`; body sections `## Scope`, `## Assumptions`, `## Out of scope`.
- The `ThreatModel` model in `typespec/main.tsp` and the `threat_model` entry of `spec_objects_security/manifest.yaml`.

## Outputs

- The closed enum `ThreatModelMethod`, emitted as `spec_objects_security/schemas/ThreatModelMethod.json`, with exactly the
  members `stride_per_element` and `stride_per_interaction`.
- The record schema `ThreatModel.json` and an open frontmatter schema `ThreatModelFrontmatter.json`, referenced by the
  `threat_model` manifest entry through `frontmatter_schema_ref`.
- A `threat_model` manifest entry and a `threat_model` skeleton `spec_objects_security/skeletons/threat_model.md`.

## Behavior

### Frontmatter

- `ThreatModel` SHALL require `method`, a `ThreatModelMethod`, and `reviewed_by`, a non-empty string naming the person who
  led the analysis.
- `ThreatModelMethod` SHALL be a closed enum of exactly `stride_per_element` and `stride_per_interaction`, with no `unknown`
  or `none` member. A value outside it, such as `guesswork`, SHALL fail validation with a located message.
- A `threat_model` with no `reviewed_by`, or with an empty `reviewed_by`, SHALL fail validation.
- The schema SHALL carry no `default` for `method` or `reviewed_by`, and the module SHALL NOT fill either from git history,
  a tool identity or any other field.
- Frontmatter `method` and `reviewed_by` SHALL be the sole authored source of each.

### Edges

- The module manifest SHALL declare `considers` in `edge_types` and SHALL NOT declare `covers`. A resolved module set
  loading a `threat_model` entry or a rule that uses `covers` SHALL include spec-artifacts-iso, which declares the canonical
  `covers` edge. Loading a rule that uses `considers` without its local declaration SHALL fail naming that verb.
- The `threat_model` manifest entry SHALL list `allowed_links.covers: [part, connection, data_sink, trust_boundary]` and
  `allowed_links.considers: [threat]`.
- A `threat_model` SHALL declare at least one `covers` edge. A `threat_model` with no `covers` edge SHALL fail validation,
  because a model that covers nothing scopes nothing.
- A `considers` edge MAY be absent. A model that covers an element and considers no threat is the case the completeness rules
  of [FR-027](./FR-027-threat-treatment-and-completeness-rules.md) report.
- A `covers` edge to a document that is not a `part`, `connection`, `data_sink` or `trust_boundary`, and a `considers` edge
  to a document that is not a `threat`, SHALL be refused with a link diagnostic.

### Body

- A `threat_model` SHALL carry the level-2 sections `## Scope`, `## Assumptions` and `## Out of scope`, each non-empty free
  text. A missing or empty section SHALL fail validation.
- The module SHALL NOT parse these sections into facts. They are for a reader.

### Skeleton

- The `threat_model` skeleton SHALL show every required key and section and SHALL validate with zero errors.

### Exports

- `threat_model` is one of the twenty-seven object types. `semantic.exports` SHALL name it ([FR-003](./FR-003-semantic-manifest-contract.md)),
  and it is one of the twenty-seven types covered by the schema, skeleton and no-default contracts of
  [FR-004](./FR-004-role-schemas.md), [FR-005](./FR-005-executable-skeletons.md) and
  [FR-006](./FR-006-security-safe-declarations.md).

## Rationale

A committed `threat_model` or `threat` document is person-authored; the module does not distinguish a document by author, and
a draft outside the corpus is never loaded. This is context for [NFR-005](../non-functional/NFR-005-threats-ratings-and-acceptance-are-person-authored.md),
not a testable obligation of this requirement.

## Out of scope

- Generating threats by machine (STRIDE per element) and any default `considers` list.
- Rating a threat. `likelihood` and `impact` stay on `risk`, as written by a person.
- Runtime monitoring of a threat.
- The completeness rules and the acceptance of an untreated threat: [FR-027](./FR-027-threat-treatment-and-completeness-rules.md).
- The generated report: quoin FR-202.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-026-AC-1 | A `threat_model` with `method: stride_per_element`, `reviewed_by: "A. Person"`, one `covers` edge to a `connection`, one `considers` edge to a `threat` and the three body sections validates with zero errors; so does the skeleton. | Test |
| FR-026-AC-2 | `method: guesswork` fails `quire validate` with a message naming `method`. `ThreatModelMethod.json` has exactly the two members and no `unknown` or `none`. | Test |
| FR-026-AC-3 | A `threat_model` with no `reviewed_by` fails validation naming `reviewed_by`; one with `reviewed_by: ""` fails. | Test |
| FR-026-AC-4 | A `threat_model` with no `covers` edge fails validation. One with `covers` edges to a `part`, a `connection`, a `data_sink` and a `trust_boundary` validates without a link diagnostic. | Test |
| FR-026-AC-5 | A `covers` edge to a `risk` and a `considers` edge to a `control` each yield a link diagnostic naming the edge. A `threat_model` with `covers` and no `considers` validates. | Test |
| FR-026-AC-6 | A `threat_model` missing `## Assumptions`, and one whose `## Out of scope` is empty, each fail validation naming the section. | Test |
| FR-026-AC-7 | `ThreatModel.json` carries no `default` for `method` or `reviewed_by`, and an extracted record has no `method` or `reviewed_by` key the author did not write. | Test |
| FR-026-AC-8 | No manifest entry, rule text, skeleton or README added by this requirement names or quotes a paywalled standard; the only sources named are STRIDE, OWASP's free threat-modelling guidance and NIST SP 800-154. | Inspection |
| FR-026-AC-9 | The security manifest declares `considers` and does not declare `covers`; the resolved module set includes spec-artifacts-iso's canonical `covers` declaration and loads a threat_model using it. Removing the ISO declaration makes loading fail naming `covers`; removing security's `considers` declaration makes loading fail naming `considers`. | Test |
| FR-026-AC-10 | `semantic.exports` names `threat_model`; `ThreatModel.json` is emitted without `default` keys; the `threat_model` skeleton validates; the empty record `{}` fails `ThreatModel.json`. | Test |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-005](./FR-005-executable-skeletons.md),
  [FR-006](./FR-006-security-safe-declarations.md), [FR-025](./FR-025-control-safeguards-and-starter-flow-rules.md);
  spec-artifacts-iso owns the canonical `covers` edge; spec-objects-architecture owns `part`, `connection`, `data_sink`
  (PLAT-1532, PLAT-1440, PR #51/#52).
- **Downstream**: [FR-027](./FR-027-threat-treatment-and-completeness-rules.md), quoin FR-202, PLAT-1543.
