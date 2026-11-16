---
id: SR-1609
title: EARS conformance — FR-026 / FR-027 / NFR-005
type: SpecReview
analysis: ears-conformance
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
# SR-1609: EARS conformance — FR-026 / FR-027 / NFR-005

## Summary

Ticket: PLAT-1542; PR agent-ix/spec-objects-security#63 at `c8d56c412920158a2b68d4f997e20c2af9f9e72d`. EARS grammar over the FR-026 and FR-027 description statements and Behavior SHALL bullets, the NFR-005 statement and the amended FR-008 Behavior bullet. Most bullets are ubiquitous SHALL / SHALL NOT clauses with one subject and one response.

Method: `spec-review/spec-ears-analysis`. Frozen head `c8d56c412920158a2b68d4f997e20c2af9f9e72d`.

## Verdict

**CONDITIONAL** — the NFR-005 statement promises more than any test can check, and two bullets either have no observable response or bundle three obligations into one.

## Coverage

Examined units:

- `FR-026` (role: examined): a person has analysed for threats, so no rule can ask "was this crossing considered?". The module SHALL add a `threat_model` object type that scopes an analysis to the parts of the model it covers and names the threats it considered.
- `FR-027` (role: examined): For a threat model to mean anything, a threat must be able to target the model's connections, sinks and boundaries; a threat left untreated must be accepted by a named person; and the model must say which covered elements still lack a threat or a treatment. The module SHALL (1) widen `threat.threatens`, (2) add a person's decision to `risk`, and (3) ship three `traceability.flow_rules` that report the gaps.
- `NFR-005` (role: examined): The module SHALL NOT derive, default or score a threat, a threat model's `considers` list, a risk's `likelihood` or `impact`, or a risk's `decision` or `decided_by`. Each comes only from the frontmatter a person wrote, and the person who led a model or decided a risk is named in the record.
- `FR-008` (role: examined): - The manifest SHALL keep `to: []` on `risk-has-treatment` ([FR-027](./FR-027-threat-treatment-and-completeness-rules.md) removes `threat-has-control` and narrows `risk-has-treatment`).
- `FR-026-AC-1` (role: context_only): A `threat_model` with `method: stride_per_element`, `reviewed_by: "A. Person"`, one `covers` edge to a `connection`, one `considers` edge to a `threat` and the three body sections validates with zero errors; so does the skeleton.
- `FR-026-AC-2` (role: context_only): `method: guesswork` fails `quire validate` with a message naming `method`. `ThreatModelMethod.json` has exactly the two members and no `unknown` or `none`.
- `FR-026-AC-3` (role: context_only): A `threat_model` with no `reviewed_by` fails validation naming `reviewed_by`; one with `reviewed_by: ""` fails.
- `FR-026-AC-4` (role: context_only): A `threat_model` with no `covers` edge fails validation. One with `covers` edges to a `part`, a `connection`, a `data_sink` and a `trust_boundary` validates without a link diagnostic.
- `FR-026-AC-5` (role: context_only): A `covers` edge to a `risk` and a `considers` edge to a `control` each yield a link diagnostic naming the edge. A `threat_model` with `covers` and no `considers` validates.
- `FR-026-AC-6` (role: context_only): A `threat_model` missing `## Assumptions`, and one whose `## Out of scope` is empty, each fail validation naming the section.
- `FR-026-AC-7` (role: context_only): `ThreatModel.json` carries no `default` for `method` or `reviewed_by`, and an extracted record has no `method` or `reviewed_by` key the author did not write.
- `FR-026-AC-8` (role: context_only): No manifest entry, rule text, skeleton or README added by this requirement names or quotes a paywalled standard; the only sources named are STRIDE, OWASP's free threat-modelling guidance and NIST SP 800-154.
- `FR-026-AC-9` (role: context_only): The module manifest declares `considers` and `covers` in `edge_types`; the module loads, and removing either declaration makes it fail to load naming the verb.
- `FR-027-AC-1` (role: context_only): A connection `CONN-1` covered by a `threat_model`, carrying `CLASS-PHI` and crossing `BOUND-NET`, with no incoming `threatens`, yields one finding under `trace:crossing-without-threat` naming `CONN-1`. Adding `THREAT-1 --threatens--> CONN-1` clears it.
- `FR-027-AC-2` (role: context_only): A sink covered by a `threat_model` that receives a classification through `delivers_to` then `carries` and has no incoming `threatens` yields one finding under `trace:classified-sink-without-threat` naming it; a sink whose own `carries` reaches a classification does the same; a threat that `threatens` the sink clears it.
- `FR-027-AC-3` (role: context_only): A threat considered by a `threat_model`, mitigated by no control and with no risk arising from it, yields one finding under `trace:threat-without-treatment` naming `THREAT-1`. A `control` that `mitigates` it clears the finding.
- `FR-027-AC-4` (role: context_only): A `risk` with `decision: accepted`, `decided_by: "A. Person"` and `arises_from: THREAT-1` clears the AC-3 finding. A `risk` with `decision: undecided`, and one with `decision: not_accepted`, do not.
- `FR-027-AC-5` (role: context_only): The same corpus with its `threat_model` removed yields no finding under any of the three checks, and a corpus with no connection, sink or threat yields none.
- `FR-027-AC-6` (role: context_only): A `risk` with `decision: accepted` and no `decided_by`, and one with `decision: accepted` and an empty `decided_by`, fail `quire validate` naming `decided_by`. A `risk` with no `decision` fails. A `risk` with `decision: undecided` and no `decided_by` validates; one with `decision: undecided` and a `decided_by` fails. `decision: maybe` fails. The updated `risk` skeleton validates with zero errors.
- `FR-027-AC-7` (role: context_only): The `threat` manifest entry lists `asset`, `attack_surface`, `connection`, `data_sink` and `trust_boundary` in `allowed_links.threatens`; a `threat` that `threatens` each validates without a link diagnostic, and one that `threatens` a `risk` yields a link diagnostic.
- `FR-027-AC-8` (role: context_only): The three rule `check` values equal their names, each rule has a non-empty `rationale`, no rule names a remediation, and the FR-025 registry still holds exactly nine entries. `RiskDecision.json` has exactly three members; `Risk.json` carries no `default` for `decision` or `decided_by`. Every `any_of` value is a member of its field's enum. The manifest declares `grammar_severity` `error` for the three checks, and every `present` condition sets `field: id`.
- `FR-027-AC-9` (role: context_only): The module declares no engine kind, archetype, verb or field outside `traceability.flow_rules` data for these rules, and no rule, rationale or README text names or quotes a paywalled standard; only STRIDE, OWASP free guidance and NIST SP 800-154 are named.
- `FR-027-AC-10` (role: context_only): A corpus with a `threat_model` considering `THREAT-1`, an `arises_from` risk with `decision: accepted` and no control raises no `trace:uncontrolled-threat` and no `trace:untreated-risk`; the same risk with `decision: undecided` raises `trace:untreated-risk`. The manifest has no `threat-has-control` rule.
- `NFR-005-AC-1` (role: context_only): `ThreatModel.json`, `Threat.json` and `Risk.json` carry no `default` for `method`, `reviewed_by`, `decision`, `decided_by`, `likelihood` or `impact`, and no manifest entry has an `assert` or default value for any of them.
- `NFR-005-AC-2` (role: context_only): A corpus in which a `connection` is covered by a `threat_model` that considers no threat produces no `threat`, no `considers` edge and no `risk` record; the only output is the finding of `trace:crossing-without-threat`.
- `NFR-005-AC-3` (role: context_only): A `risk` with `likelihood` and `impact` stated and no `decision` fails validation; no rule reads `likelihood` or `impact`, and no output carries a computed score.
- `FR-008-AC-6` (role: context_only): `risk-has-treatment` still declares `to: []` in the manifest.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | medium | NFR-005's title and second sentence ('Each comes only from the frontmatter a person wrote, and the person who led a model or decided a risk is named in the record') have no SHALL and cannot be verified: a `threat` has no field naming a person, and the module cannot tell a person's frontmatter from an agent's. Its metrics and ACs measure only non-derivation and non-default. Narrow the title and statement to what is checked (no derivation, no default; `reviewed_by` and `decided_by` are authored strings). | spec/non-functional/NFR-005-threats-ratings-and-acceptance-are-person-authored.md:3,16 | wrong-requirement |
| FND-002 | low | The FR-026 'Person-authored documents' bullet ('SHALL treat a committed threat_model or threat document as person-authored, and SHALL NOT distinguish a document by author') has no observable response, and its draft sentences describe agents and commits outside the system. No AC can fail. Drop it, or state it as rationale. | spec/functional/FR-026-threat-model-object.md:89-93 | wrong-requirement |
| FND-003 | low | One FR-027 bullet carries three obligations: `decided_by` 'SHALL be a person's name as written' (untestable), SHALL NOT be filled from git, a tool or an agent, and SHALL reject `decision: undecided` with a `decided_by`. Split it so the testable rejection (covered by AC-6) stands alone. | spec/functional/FR-027-threat-treatment-and-completeness-rules.md:74 | wrong-requirement |

## Dispositions

Round 1, after fix commit `7b2a707c74423739330d19e35a7811d3912cab75`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | - |
| FND-002 | fixed | - |
| FND-003 | fixed | - |

After excerpts (round 1, verbatim):

- FND-001:

```text
title: "The module never derives or defaults a threat, a rating or an acceptance" ... The module SHALL NOT derive, default or score a threat, a threat model's `considers` list, a risk's `likelihood` or `impact`, or a risk's `decision` or `decided_by`. Each value is the authored frontmatter string or edge and nothing else; `reviewed_by` and `decided_by` are authored strings the module neither fills nor checks against any identity.
```

- FND-002:

```text
## Rationale  A committed `threat_model` or `threat` document is person-authored; the module does not distinguish a document by author, and a draft outside the corpus is never loaded. This is context for NFR-005, not a testable obligation of this requirement.
```

- FND-003:

```text
- The module SHALL NOT fill `decided_by` from git, a tool identity or an agent. / - The module SHALL reject a risk with `decision: undecided` and a `decided_by`, as spec-objects-safety `residual_risk` does: an undecided risk has no decider.
```
