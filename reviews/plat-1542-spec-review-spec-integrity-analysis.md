---
id: SR-1610
title: Integrity analysis — FR-026 / FR-027 / NFR-005 / FR-008
type: SpecReview
analysis: integrity
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
# SR-1610: Integrity analysis — FR-026 / FR-027 / NFR-005 / FR-008

## Summary

Ticket: PLAT-1542; PR agent-ix/spec-objects-security#63 at `c8d56c412920158a2b68d4f997e20c2af9f9e72d`. Structural consistency of the new and amended documents: ID sequence, AC tables, index entries, and agreement with existing text that names `threat-has-control`.

Method: `spec-review/spec-integrity-analysis`. Frozen head `c8d56c412920158a2b68d4f997e20c2af9f9e72d`.

## Verdict

**CONDITIONAL** — indexes, frontmatter ids and titles agree, and quire validates the spec tree. Three low findings: AC ordering and the AC preamble in FR-027, and two places that still name the removed `threat-has-control`.

## Coverage

Examined units:

- `FR-026` (role: examined): a person has analysed for threats, so no rule can ask "was this crossing considered?". The module SHALL add a `threat_model` object type that scopes an analysis to the parts of the model it covers and names the threats it considered.
- `FR-027` (role: examined): For a threat model to mean anything, a threat must be able to target the model's connections, sinks and boundaries; a threat left untreated must be accepted by a named person; and the model must say which covered elements still lack a threat or a treatment. The module SHALL (1) widen `threat.threatens`, (2) add a person's decision to `risk`, and (3) ship three `traceability.flow_rules` that report the gaps.
- `NFR-005` (role: examined): The module SHALL NOT derive, default or score a threat, a threat model's `considers` list, a risk's `likelihood` or `impact`, or a risk's `decision` or `decided_by`. Each comes only from the frontmatter a person wrote, and the person who led a model or decided a risk is named in the record.
- `FR-008` (role: examined): - The manifest SHALL keep `to: []` on `risk-has-treatment` ([FR-027](./FR-027-threat-treatment-and-completeness-rules.md) removes `threat-has-control` and narrows `risk-has-treatment`).
- `FR-008-AC-6` (role: examined): `risk-has-treatment` still declares `to: []` in the manifest.
- `FR-027-AC-9` (role: examined): The module declares no engine kind, archetype, verb or field outside `traceability.flow_rules` data for these rules, and no rule, rationale or README text names or quotes a paywalled standard; only STRIDE, OWASP free guidance and NIST SP 800-154 are named.
- `FR-027-AC-10` (role: examined): A corpus with a `threat_model` considering `THREAT-1`, an `arises_from` risk with `decision: accepted` and no control raises no `trace:uncontrolled-threat` and no `trace:untreated-risk`; the same risk with `decision: undecided` raises `trace:untreated-risk`. The manifest has no `threat-has-control` rule.
- `spec/functional/index.md` (role: examined): index entries for FR-026 and FR-027
- `spec/non-functional/index.md` (role: examined): index entry for NFR-005
- `TC-120` (role: context_only): | TC-120 | `threat-has-control` and `risk-has-treatment` still declare `to: []` | Unit | P1 | FR-008-AC-6 | ✅ |

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | low | The FR-027 AC table lists AC-10 before AC-9, and the preamble ('AC-6 to AC-9 are module-only checks') leaves AC-10, which evaluates rules through the engine, in neither group. Order the rows and name AC-10 in the preamble. | spec/functional/FR-027-threat-treatment-and-completeness-rules.md:137,150-151 | wrong-requirement |
| FND-002 | low | FR-008's Description still opens with '`threat-has-control` and `risk-has-treatment` read the `mitigates` edge from the exposure end', which is no longer true once FR-027 removes `threat-has-control`; the PR amended only the Behavior bullet and AC-6. | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:21-22 | wrong-requirement |
| FND-003 | low | `spec/tests.md` TC-120 still reads '`threat-has-control` and `risk-has-treatment` still declare `to: []`' against FR-008-AC-6, which now names only `risk-has-treatment`; the row is marked done against the old text. | spec/tests.md:246 | wrong-requirement |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-004 | medium | Fix round 1 rewrote TC-040, TC-044, TC-050, TC-060, TC-080 and TC-120 to the new twenty-six-type and no-`threat-has-control` text but kept their ✅ status, and the FR-003 row stays ✅. The manifest at 7b2a707 still exports 25 types and still declares `threat-has-control`, and tests/test_reverse_mitigates.py asserts it is present, so six rows now claim passing evidence that does not exist until PLAT-1543. Set them to 🚧 (FR-008 is already 🚧). US-001's 'Today all twenty-six object types' also rewrites a historical statement. | spec/tests.md:134,197-198,201,211,223,246 | wrong-requirement |

## New findings (disposition pass 2)

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-005 | low | Same class as FND-004, missed by the fix: FR-006-AC-4 and FR-005-AC-7 now cover twenty-six types, but TC-073 (FR-006-AC-4), TC-086 (FR-005-AC-7) and the FR-006 summary row stay ✅. No `ThreatModel.json` or `threat_model` skeleton exists at b1d7d31, so they claim evidence for the new type that does not exist until PLAT-1543. Set them to 🚧. | spec/tests.md:137,218,229 | wrong-requirement |

## Dispositions

Round 1, after fix commit `7b2a707c74423739330d19e35a7811d3912cab75`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | - |
| FND-002 | fixed | - |
| FND-003 | fixed | - |
| FND-004 | fixed | - |

After excerpts (round 1, verbatim):

- FND-001:

```text
AC-1 to AC-5 and AC-10 are draft ACs a to d of PLAT-1542 and evaluate the rule data through the engine. AC-6 to AC-9 are module-only checks. ... rows now ordered FR-027-AC-8, FR-027-AC-9, FR-027-AC-10.
```

- FND-002:

```text
`risk-has-treatment` reads the `mitigates` edge from the exposure end: a risk nothing mitigates is reported ([FR-027](./FR-027-threat-treatment-and-completeness-rules.md) removes the matching `threat-has-control` rule). This requirement
```

- FND-003:

```text
| TC-120 | `risk-has-treatment` still declares `to: []` and `threat-has-control` is absent | Unit | P1 | FR-008-AC-6 | ✅ |
```

After excerpts (round 2, verbatim; fix commits `b7920b1`, `b1d7d317c9bcaa4614578b36d7fa02f945136514`):

- FND-004:

```text
| TC-040 | The `semantic` block equals the eight admitted keys and `exports` equals the twenty-six types | Unit | P0 | FR-003-AC-1, FR-003-CON-1 | 🚧 | / | TC-120 | `risk-has-treatment` still declares `to: []` and `threat-has-control` is absent | Unit | P1 | FR-008-AC-6 | 🚧 | / FR-003, FR-004, FR-005 summary rows now 🚧; TC-044, TC-050, TC-060, TC-080 now 🚧; US-001: 'Today all twenty-five object types in `manifest.yaml` carry'
```
