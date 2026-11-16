---
id: SR-1611
title: Dependency analysis — FR-026 / FR-027 / NFR-005
type: SpecReview
analysis: dependency
scope: agent-ix/spec-objects-security; spec/functional/FR-008-security-nfr-needs-mitigation-target.md, spec/functional/FR-026-threat-model-object.md, spec/functional/FR-027-threat-treatment-and-completeness-rules.md, spec/functional/index.md, spec/non-functional/NFR-005-threats-ratings-and-acceptance-are-person-authored.md, spec/non-functional/index.md
review_set: subset
relationships:
- target: ix://agent-ix/spec-objects-security/FR-026
  type: reviews
- target: ix://agent-ix/spec-objects-security/FR-027
  type: reviews
- target: ix://agent-ix/spec-objects-security/NFR-005
  type: reviews
- target: ix://agent-ix/spec-objects-security/FR-008
  type: reviews
---
# SR-1611: Dependency analysis — FR-026 / FR-027 / NFR-005

## Summary

Ticket: PLAT-1542; PR agent-ix/spec-objects-security#63 at `c8d56c412920158a2b68d4f997e20c2af9f9e72d`. New `relationships:` edges and stated upstream enablement: FR-026 needs the `covers` verb (PLAT-1657) and the spec-objects-architecture `part`, `connection`, `data_sink` and `crosses`; FR-027 needs quire-rs FR-096 and the PLAT-1537/PLAT-1538 loader. Measured in Linear: PLAT-1657 is Backlog and blocks only PLAT-1658; PLAT-1543 (implementation) is blocked only by PLAT-1542.

Method: `spec-review/spec-dependency-analysis`. Frozen head `c8d56c412920158a2b68d4f997e20c2af9f9e72d`.

## Verdict

**CONDITIONAL** — every `ix://` target resolves to an existing artifact in this repo or quire-rs `main` (FR-096 landed in cd817f0). Enablement is separated from feature work in the prose (Engine impact sections), but the tracker does not carry the hard blockers, and FR-027 omits two relationship edges it depends on.

## Coverage

Examined units:

- `FR-026` (role: examined): a person has analysed for threats, so no rule can ask "was this crossing considered?". The module SHALL add a `threat_model` object type that scopes an analysis to the parts of the model it covers and names the threats it considered.
- `FR-027` (role: examined): For a threat model to mean anything, a threat must be able to target the model's connections, sinks and boundaries; a threat left untreated must be accepted by a named person; and the model must say which covered elements still lack a threat or a treatment. The module SHALL (1) widen `threat.threatens`, (2) add a person's decision to `risk`, and (3) ship three `traceability.flow_rules` that report the gaps.
- `NFR-005` (role: examined): The module SHALL NOT derive, default or score a threat, a threat model's `considers` list, a risk's `likelihood` or `impact`, or a risk's `decision` or `decided_by`. Each comes only from the frontmatter a person wrote, and the person who led a model or decided a risk is named in the record.
- `FR-008` (role: context_only): - The manifest SHALL keep `to: []` on `risk-has-treatment` ([FR-027](./FR-027-threat-treatment-and-completeness-rules.md) removes `threat-has-control` and narrows `risk-has-treatment`).

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | medium | FR-026 calls PLAT-1657 (`covers`) a hard upstream blocker and FR-027 needs PLAT-1537/PLAT-1538 and the architecture objects (PLAT-1532, PLAT-1440), but none of these blocks PLAT-1543, the implementation ticket, in Linear; PLAT-1543 shows as blocked only by PLAT-1542, so it can be picked up while FR-026-AC-9 is unsatisfiable. Add blocked-by edges to PLAT-1543. | spec/functional/FR-026-threat-model-object.md:32-34 | missing-requirement |
| FND-002 | low | FR-027's relationships omit quire-rs FR-058, whose `where` selector its narrowed `risk-has-treatment` uses, and carry no edge to FR-008, which it says it amends; both dependencies exist only in prose. | spec/functional/FR-027-threat-treatment-and-completeness-rules.md:4-16,86-88 | wrong-requirement |

## Dispositions

Round 1, after fix commit `7b2a707c74423739330d19e35a7811d3912cab75`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | - |
| FND-002 | fixed | - |

After excerpts (round 1, verbatim):

- FND-001:

```text
Linear, measured 2026-11-15 after 7b2a707: PLAT-1543 inverseRelations = blocks from PLAT-1657, PLAT-1535, PLAT-1542; PLAT-1544 (completeness rules) inverseRelations = PLAT-1538, PLAT-1532, PLAT-1543. The covers verb and data_sink blockers now gate the object ticket and the loader and crosses blockers gate the rule ticket.
```

- FND-002:

```text
  - target: "ix://agent-ix/spec-objects-security/FR-008"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-058"
    type: "depends_on"
```
