---
id: SR-1608
title: Base spec review — FR-026 / FR-027 / NFR-005 threat model
type: SpecReview
analysis: base
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
# SR-1608: Base spec review — FR-026 / FR-027 / NFR-005 threat model

## Summary

Ticket: PLAT-1542; PR agent-ix/spec-objects-security#63 at `c8d56c412920158a2b68d4f997e20c2af9f9e72d`. Base checklist over the new FR-026, FR-027 and NFR-005 and the amended FR-008-AC-6: ID format and sequence, FR quality, criterion coverage of Behavior, error paths and edge cases, and the hash/pin antipattern scan. Review set: subset (base, ears-conformance, integrity, dependency, plus spec-object-review). No AssuranceProfile document applies to this repository. FR-096 and FR-058 semantics were read from agent-ix/quire-rs `main` to check the rule data.

Method: `spec-review/base`. Frozen head `c8d56c412920158a2b68d4f997e20c2af9f9e72d`.

## Verdict

**CONDITIONAL** — the rule data in FR-027 is expressible in FR-096 as written (each path has two steps at most, `present` with `field: id`, `decision` resolvable through `RiskFrontmatter.json`, no remediations, so no remediation load check), and the error paths for `method`, `reviewed_by`, `decision` and `decided_by` each have an AC. No hash/pin antipattern was found. Four findings: one NFR AC cannot pass as written, two FR-027 Behavior bullets have no criterion, the removal of `threat-has-control` drops an existing check for corpora without a threat model, and one `where` value is never exercised.

## Coverage

Examined units:

- `FR-026-AC-1` (role: examined): A `threat_model` with `method: stride_per_element`, `reviewed_by: "A. Person"`, one `covers` edge to a `connection`, one `considers` edge to a `threat` and the three body sections validates with zero errors; so does the skeleton.
- `FR-026-AC-2` (role: examined): `method: guesswork` fails `quire validate` with a message naming `method`. `ThreatModelMethod.json` has exactly the two members and no `unknown` or `none`.
- `FR-026-AC-3` (role: examined): A `threat_model` with no `reviewed_by` fails validation naming `reviewed_by`; one with `reviewed_by: ""` fails.
- `FR-026-AC-4` (role: examined): A `threat_model` with no `covers` edge fails validation. One with `covers` edges to a `part`, a `connection`, a `data_sink` and a `trust_boundary` validates without a link diagnostic.
- `FR-026-AC-5` (role: examined): A `covers` edge to a `risk` and a `considers` edge to a `control` each yield a link diagnostic naming the edge. A `threat_model` with `covers` and no `considers` validates.
- `FR-026-AC-6` (role: examined): A `threat_model` missing `## Assumptions`, and one whose `## Out of scope` is empty, each fail validation naming the section.
- `FR-026-AC-7` (role: examined): `ThreatModel.json` carries no `default` for `method` or `reviewed_by`, and an extracted record has no `method` or `reviewed_by` key the author did not write.
- `FR-026-AC-8` (role: examined): No manifest entry, rule text, skeleton or README added by this requirement names or quotes a paywalled standard; the only sources named are STRIDE, OWASP's free threat-modelling guidance and NIST SP 800-154.
- `FR-026-AC-9` (role: examined): The module manifest declares `considers` and `covers` in `edge_types`; the module loads, and removing either declaration makes it fail to load naming the verb.
- `FR-027-AC-1` (role: examined): A connection `CONN-1` covered by a `threat_model`, carrying `CLASS-PHI` and crossing `BOUND-NET`, with no incoming `threatens`, yields one finding under `trace:crossing-without-threat` naming `CONN-1`. Adding `THREAT-1 --threatens--> CONN-1` clears it.
- `FR-027-AC-2` (role: examined): A sink covered by a `threat_model` that receives a classification through `delivers_to` then `carries` and has no incoming `threatens` yields one finding under `trace:classified-sink-without-threat` naming it; a sink whose own `carries` reaches a classification does the same; a threat that `threatens` the sink clears it.
- `FR-027-AC-3` (role: examined): A threat considered by a `threat_model`, mitigated by no control and with no risk arising from it, yields one finding under `trace:threat-without-treatment` naming `THREAT-1`. A `control` that `mitigates` it clears the finding.
- `FR-027-AC-4` (role: examined): A `risk` with `decision: accepted`, `decided_by: "A. Person"` and `arises_from: THREAT-1` clears the AC-3 finding. A `risk` with `decision: undecided`, and one with `decision: not_accepted`, do not.
- `FR-027-AC-5` (role: examined): The same corpus with its `threat_model` removed yields no finding under any of the three checks, and a corpus with no connection, sink or threat yields none.
- `FR-027-AC-6` (role: examined): A `risk` with `decision: accepted` and no `decided_by`, and one with `decision: accepted` and an empty `decided_by`, fail `quire validate` naming `decided_by`. A `risk` with no `decision` fails. A `risk` with `decision: undecided` and no `decided_by` validates; one with `decision: undecided` and a `decided_by` fails. `decision: maybe` fails. The updated `risk` skeleton validates with zero errors.
- `FR-027-AC-7` (role: examined): The `threat` manifest entry lists `asset`, `attack_surface`, `connection`, `data_sink` and `trust_boundary` in `allowed_links.threatens`; a `threat` that `threatens` each validates without a link diagnostic, and one that `threatens` a `risk` yields a link diagnostic.
- `FR-027-AC-8` (role: examined): The three rule `check` values equal their names, each rule has a non-empty `rationale`, no rule names a remediation, and the FR-025 registry still holds exactly nine entries. `RiskDecision.json` has exactly three members; `Risk.json` carries no `default` for `decision` or `decided_by`. Every `any_of` value is a member of its field's enum. The manifest declares `grammar_severity` `error` for the three checks, and every `present` condition sets `field: id`.
- `FR-027-AC-9` (role: examined): The module declares no engine kind, archetype, verb or field outside `traceability.flow_rules` data for these rules, and no rule, rationale or README text names or quotes a paywalled standard; only STRIDE, OWASP free guidance and NIST SP 800-154 are named.
- `FR-027-AC-10` (role: examined): A corpus with a `threat_model` considering `THREAT-1`, an `arises_from` risk with `decision: accepted` and no control raises no `trace:uncontrolled-threat` and no `trace:untreated-risk`; the same risk with `decision: undecided` raises `trace:untreated-risk`. The manifest has no `threat-has-control` rule.
- `NFR-005-AC-1` (role: examined): `ThreatModel.json`, `Threat.json` and `Risk.json` carry no `default` for `method`, `reviewed_by`, `decision`, `decided_by`, `likelihood` or `impact`, and no manifest entry has an `assert` or default value for any of them.
- `NFR-005-AC-2` (role: examined): A corpus in which a `connection` is covered by a `threat_model` that considers no threat produces no `threat`, no `considers` edge and no `risk` record; the only output is the finding of `trace:crossing-without-threat`.
- `NFR-005-AC-3` (role: examined): A `risk` with `likelihood` and `impact` stated and no `decision` fails validation; no rule reads `likelihood` or `impact`, and no output carries a computed score.
- `FR-008-AC-6` (role: examined): `risk-has-treatment` still declares `to: []` in the manifest.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | medium | NFR-005-AC-2 expects `trace:crossing-without-threat` from a connection that is only covered by a threat_model, but FR-027's rule also requires the connection to carry a data_classification and cross a trust_boundary, so the stated corpus yields no finding and the AC cannot pass; 'the only output' also ignores FR-025's starter rules, which can fire on the same connection. State the carries and crosses edges and scope 'only' to the threat-model checks. | spec/non-functional/NFR-005-threats-ratings-and-acceptance-are-person-authored.md:39 | wrong-requirement |
| FND-002 | medium | Two FR-027 Behavior bullets have no criterion: a covered connection that carries no classification, or crosses no boundary, owes no threat; and a threat that threatens the boundary a connection crosses does not clear the connection. Both are the edge cases most likely to be got wrong in the rule data. Add a negative case for each to AC-1. | spec/functional/FR-027-threat-treatment-and-completeness-rules.md:113-116 | correct-requirement-no-evidence |
| FND-003 | medium | Removing `threat-has-control` deletes `trace:uncontrolled-threat` for every threat, so a corpus that lists threats but has no threat_model, which is every existing corpus, goes from one finding per uncontrolled threat to none. FR-027 states this is intended but does not weigh the lost check or say where a consumer learns of it (README or FR-008 rationale). Confirm the trade-off and record it. | spec/functional/FR-027-threat-treatment-and-completeness-rules.md:84-85 | wrong-requirement |
| FND-004 | low | `risk-has-treatment` narrows to `values: [undecided, not_accepted]`, but FR-027-AC-10 exercises only `undecided`; no criterion shows a `not_accepted` risk with no `mitigates` still raising `trace:untreated-risk`. A mistyped second value would pass every AC. | spec/functional/FR-027-threat-treatment-and-completeness-rules.md:150 | correct-requirement-no-evidence |

## Dispositions

Round 1, after fix commit `7b2a707c74423739330d19e35a7811d3912cab75`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | - |
| FND-002 | fixed | - |
| FND-003 | still-open | No text weighing the lost check landed in 7b2a707. FR-027's 'Existing upward rules' bullet is unchanged, and FR-008 gained only the parenthetical '(FR-027 removes the matching `threat-has-control` rule)'. Nothing states that a corpus with threats but no threat_model loses every `trace:uncontrolled-threat` finding, or why that is acceptable. The PR body says 'Rationale and consumer note for removing `threat-has-control`' was added, but the diff contains none. To resolve it, add the trade-off sentence to FR-027 (or README), or record an explicit accepted-no-change decision. |
| FND-004 | fixed | - |
| FND-003 | fixed | - |

After excerpts (round 1, verbatim):

- FND-001:

```text
A corpus in which a `connection` that carries a `data_classification` and crosses a `trust_boundary` is covered by a `threat_model` that considers no threat produces no `threat`, no `considers` edge and no `risk` record; of the three threat-model checks the only finding is `trace:crossing-without-threat` (starter rules of FR-025 are not counted).
```

- FND-002:

```text
A covered connection that carries `CLASS-PHI` but crosses no `trust_boundary`, and one that crosses `BOUND-NET` but carries no `data_classification`, each yield no finding. A threat that `threatens` only `BOUND-NET` leaves the finding on `CONN-1`.
```

- FND-004:

```text
A corpus with a `threat_model` considering `THREAT-1`, an `arises_from` risk with `decision: accepted` and no control raises no `trace:uncontrolled-threat` and no `trace:untreated-risk`; the same risk with `decision: undecided`, and one with `decision: not_accepted`, each raise `trace:untreated-risk` (with no `mitigates` edge). The manifest has no `threat-has-control` rule.
```

After excerpts (round 2, verbatim; fix commits `b7920b1`, `b1d7d317c9bcaa4614578b36d7fa02f945136514`):

- FND-003:

```text
- **Rationale for the loss of `trace:uncontrolled-threat`.** Removing `threat-has-control` removes that finding for every threat. A corpus that lists threats but has no `threat_model`, which is every existing corpus, goes from one finding per uncontrolled threat to none. This is intended: a threat outside every threat model has not been scoped for analysis, so no one has stated that it must be treated, and the old rule also reported threats that a risk accepted. The check returns
```
