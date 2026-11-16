---
id: NFR-005
title: "The module never derives or defaults a threat, a rating or an acceptance"
type: NFR
quality_attribute: maintainability
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-026"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-security/FR-027"
    type: "constrains"
---
# NFR-005: The module never derives or defaults a threat, a rating or an acceptance

## Statement

The module SHALL NOT derive, default or score a threat, a threat model's `considers` list, a risk's `likelihood` or `impact`, or a risk's `decision` or `decided_by`. Each value is the authored frontmatter string or edge and nothing else; `reviewed_by` and `decided_by` are authored strings the module neither fills nor checks against any identity.

## Scope

- Applies to: the `ThreatModel`, `Threat` and `Risk` schemas, skeletons and manifest entries, and the three flow rules of FR-027.
- Out of scope: a draft document an agent proposes; it carries no weight until a person authors it as a threat or threat model.

## Rationale

A threat the tool invented, or an acceptance nobody made, would read as a person's judgement that nobody exercised, and a completeness rule satisfied by it would hide an untreated threat. The rules count a threat as treated only on a control or a named person's acceptance; an absent entry means nobody stated one.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| `default` keywords for `method`, `reviewed_by`, `decision`, `decided_by`, `likelihood` or `impact` in emitted schemas | 0 | 0 | Test |
| Threat, `considers`, rating, `decision` or `decided_by` keys in an extracted record that the author did not write | 0 | 0 | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-005-AC-1 | `ThreatModel.json`, `Threat.json` and `Risk.json` carry no `default` for `method`, `reviewed_by`, `decision`, `decided_by`, `likelihood` or `impact`, and no manifest entry has an `assert` or default value for any of them. | Test |
| NFR-005-AC-2 | A corpus in which a `connection` that carries a `data_classification` and crosses a `trust_boundary` is covered by a `threat_model` that considers no threat produces no `threat`, no `considers` edge and no `risk` record; of the three threat-model checks the only finding is `trace:crossing-without-threat` (starter rules of FR-025 are not counted). | Test |
| NFR-005-AC-3 | A `risk` with `likelihood` and `impact` stated and no `decision` fails validation; no rule reads `likelihood` or `impact`, and no output carries a computed score. | Test |

## Verification

Tests over the emitted schemas and validated fixtures.

## Dependencies

- **Upstream**: [FR-026](../functional/FR-026-threat-model-object.md), [FR-027](../functional/FR-027-threat-treatment-and-completeness-rules.md)
