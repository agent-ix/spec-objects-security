---
id: FR-027
title: "A threat targets model elements, a risk records a named person's decision, and the module ships the threat-model completeness flow rules"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-025"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-026"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-008"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-058"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-096"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/NFR-005"
    type: "constrained_by"
---
# FR-027: A threat targets model elements, a risk records a named person's decision, and the module ships the threat-model completeness flow rules

## Description

For a threat model to mean anything, a threat must be able to target the model's connections, sinks and boundaries; a threat
left untreated must be accepted by a named person; and the model must say which scoped elements still lack a threat or a
treatment. The module SHALL (1) widen `threat.threatens`, (2) add a person's decision to `risk`, and (3) ship three
`traceability.flow_rules` that report the gaps.

The rules are module data in the `flow_rules` form that [FR-025](./FR-025-control-safeguards-and-starter-flow-rules.md) already
uses and quire-rs FR-096 defines. **No engine change is made** beyond the `present: true` test that FR-096 already includes.
Rule evaluation, path semantics, severity defaults and exit codes belong to FR-096 and the quire-cli relation report.

Two existing upward rules contradict this definition of treated and are changed here: `threat-has-control`
(`trace:uncontrolled-threat`) and `risk-has-treatment` (`trace:untreated-risk`) each require an incoming `mitigates` edge,
so a threat accepted through a risk, and the accepting risk, would still be reported. `threat-has-control` is replaced by
`threat-without-treatment`; `risk-has-treatment` is narrowed to risks whose `decision` is not `accepted`.

The decision vocabulary on `risk` (`undecided`, `accepted`, `not_accepted`) is the vocabulary of spec-objects-safety
`residual_risk` Determination. It is a frontmatter key here because `flow_rules` reads frontmatter only. The person who
decided is named in the record; the date of the decision comes from git and is not a key.

A threat is **treated** only when a `control` mitigates it, or when a `risk` that arises from it has `decision: accepted`
and a named `decided_by`. A threat SHALL NOT count as treated on any other basis. The rules never derive a threat, a rating or
an acceptance; those are person-authored ([NFR-005](../non-functional/NFR-005-threats-ratings-and-acceptance-are-person-authored.md)).

## Inputs

- `threat`, `risk` and `threat_model` documents ([FR-026](./FR-026-threat-model-object.md)); `connection`, `data_sink`,
  `trust_boundary` and `data_classification` documents; `control` documents (FR-025).
- The `Threat` and `Risk` models and the `traceability` block of `spec_objects_security/manifest.yaml`.

## Outputs

- `allowed_links.threatens: [asset, attack_surface, connection, data_sink, trust_boundary]` on the `threat` manifest entry.
- `Risk` frontmatter keys `decision` and `decided_by`; the closed enum `RiskDecision` (`undecided`, `accepted`,
  `not_accepted`), emitted as `RiskDecision.json`; an open frontmatter schema `RiskFrontmatter.json` referenced by the `risk`
  manifest entry through `frontmatter_schema_ref`.
- `traceability.flow_rules`: the three rules below, in addition to FR-025's six.
- Updated `threat` and `risk` skeletons, and fixtures that exercise each rule.

## Behavior

### Threat targets

- The `threat` manifest entry SHALL list `connection`, `data_sink` and `trust_boundary` in `allowed_links.threatens`, in
  addition to `asset` and `attack_surface`. `exploits: [vulnerability]` is unchanged.
- A `threatens` edge to any other archetype SHALL be refused with a link diagnostic.

### Risk decision

- `Risk` SHALL require `decision`, a `RiskDecision`. `RiskDecision` SHALL be a closed enum of exactly `undecided`,
  `accepted` and `not_accepted`.
- `Risk` SHALL require a non-empty `decided_by` when `decision` is `accepted` or `not_accepted`. A risk with
  `decision: accepted` and no `decided_by`, or an empty one, SHALL fail validation naming `decided_by`.
- The module SHALL NOT fill `decided_by` from git, a tool identity or an agent.
- The module SHALL reject a risk with `decision: undecided` and a `decided_by`, as spec-objects-safety `residual_risk` does: an undecided risk has no decider.
- The conditional rule is enforced by the `Risk.json` record schema, as `if`/`then`/`else` over `decision` (`then`: `decided_by` required and non-empty; `else`: `decided_by` forbidden). `RiskFrontmatter.json` is open and constrains only the `decision` enum; a manifest locator's `required` flag cannot express the condition and is not used for it.
- The schema SHALL carry no `default` for `decision` or `decided_by`. A risk with no `decision` fails validation: undecided is
  stated, never assumed.
- The module SHALL NOT compute, score or order `likelihood` or `impact`, and SHALL NOT derive `decision` from either.
- `decision` and `decided_by` SHALL be frontmatter keys and the sole authored source. This is a change to existing `risk`
  documents, which gain a required key; the module keeps no reader for a `risk` without it. The `risk` skeleton, and every fixture of this module with `type: risk`,
  SHALL be updated to carry `decision`.

### Existing upward rules

- The manifest SHALL NOT declare `threat-has-control`. Unconsidered threats are outside every threat model and get no
  finding, as the rule below requires.
- **Rationale for the loss of `trace:uncontrolled-threat`.** Removing `threat-has-control` removes that finding for every
  threat. A corpus that lists threats but has no `threat_model`, which is every existing corpus, goes from one finding per
  uncontrolled threat to none. This is intended: a threat outside every threat model has not been scoped for analysis, so
  no one has stated that it must be treated, and the old rule also reported threats that a risk accepted. The check returns
  for a threat as soon as a person adds a `threat_model` that `considers` it (`trace:threat-without-treatment`). A consumer
  who wants the old behaviour for unscoped threats adds a `threat_model` that considers them.
- The manifest SHALL declare `risk-has-treatment` with `where: {field: decision, values: [undecided, not_accepted]}`
  (quire-rs FR-058), so that a risk with `decision: accepted` owes no `mitigates` edge, and keep `to: []`.
- This amends FR-008, whose text and AC-6 name `threat-has-control` and `risk-has-treatment`.

### Completeness rules

The module SHALL ship these three `flow_rules`, each with a non-empty `rationale`, a `check` equal to its `name`, and no
`remediations` (a remediation names a change the registry of FR-025 defines; the nine entries stay unchanged and a
threat, a control or a person's decision is not one of them). Only an element scoped by a `threat_model` is required to
have a threat; a corpus without a `threat_model` yields no finding from any of the three.

| Rule name and check | Subject | Match | Unless any |
|---------------------|---------|-------|------------|
| `crossing-without-threat` | `connection` | incoming `scopes` from a `threat_model` (`present`); outgoing `carries` to a `data_classification` (`present`); outgoing `crosses` to a `trust_boundary` (`present`) | incoming `threatens` from a `threat` (`present`) |
| `classified-sink-without-threat` | `data_sink` | incoming `scopes` from a `threat_model` (`present`); `any_path` of `delivers_to` incoming then `carries` outgoing, together with the sink's own `carries`, reaching a `data_classification` (`present`) | incoming `threatens` from a `threat` (`present`) |
| `threat-without-treatment` | `threat` | incoming `considers` from a `threat_model` (`present`) | incoming `mitigates` from a `control` (`present`); incoming `arises_from` from a `risk` whose `decision` is in `accepted` |

- Every `any_of` value in these rules SHALL be a member of the enum of that field in the target archetype's frontmatter schema;
  `decision` is checked against `RiskFrontmatter.json`.
- `threat-without-treatment` SHALL treat a risk as accepting only when its `decision` is `accepted`; a risk with `undecided`
  or `not_accepted` SHALL NOT clear it. The rule reads `decision`; the requirement that an accepted risk names `decided_by` is
  enforced by validation above, so an accepted risk without a name cannot reach the rule.
- The engine's default severity for a flow rule is `warning`. The manifest SHALL declare `grammar_severity` for
  `trace:crossing-without-threat`, `trace:classified-sink-without-threat` and `trace:threat-without-treatment` as `error`.
  A project lowers one with `--severity trace:<name>=warning`.
- Every `present` condition SHALL set `field: id`. The `unless_any` condition on `arises_from` SHALL read the risk's
  `field: decision` with `any_of: [accepted]`.
- A `connection` that carries no `data_classification`, or crosses no `trust_boundary`, is not required to have a threat by
  `crossing-without-threat`.
- Only an incoming `threatens` edge on the subject itself clears `crossing-without-threat` or
  `classified-sink-without-threat`. A threat that targets the boundary a connection crosses does not clear the connection.
- The module declares the rules as data only. It adds no archetype, verb, field or value to the engine.

## Engine impact

None of the rule behaviors can be evaluated until quire-rs delivers `flow_rules` (FR-096, including `present: true`; the
`traceability.flow_rules` loader of PLAT-1537/PLAT-1538), FR-026 declares the security-owned `scopes` relation, distinct from ISO `covers`,
and the `connection`, `data_sink` and `crosses` objects exist in spec-objects-architecture. The enum, link, `Risk` and
manifest data can be authored and schema-validated first. This requirement does not promise that code.

## Out of scope

- Automatic threat generation and any machine-built `considers` list.
- Computing or scoring `likelihood` and `impact`.
- Judging that a control adequately mitigates a threat, or that a person's acceptance is wise.
- Runtime monitoring.
- Signing an acceptance record: signed records are a separate feature and are not enabled by this requirement.
- The generated report: quoin FR-202.

## Acceptance Criteria

AC-1 to AC-5 and AC-10 are draft ACs a to d of PLAT-1542 and evaluate the rule data through the engine. AC-6 to AC-9 are
module-only checks.

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-027-AC-1 | A connection `CONN-1` scoped by a `threat_model`, carrying `CLASS-PHI` and crossing `BOUND-NET`, with no incoming `threatens`, yields one finding under `trace:crossing-without-threat` naming `CONN-1`. Adding `THREAT-1 --threatens--> CONN-1` clears it. A scoped connection that carries `CLASS-PHI` but crosses no `trust_boundary`, and one that crosses `BOUND-NET` but carries no `data_classification`, each yield no finding. A threat that `threatens` only `BOUND-NET` leaves the finding on `CONN-1`. | Test |
| FR-027-AC-2 | A sink scoped by a `threat_model` that receives a classification through `delivers_to` then `carries` and has no incoming `threatens` yields one finding under `trace:classified-sink-without-threat` naming it; a sink whose own `carries` reaches a classification does the same; a threat that `threatens` the sink clears it. | Test |
| FR-027-AC-3 | A threat considered by a `threat_model`, mitigated by no control and with no risk arising from it, yields one finding under `trace:threat-without-treatment` naming `THREAT-1`. A `control` that `mitigates` it clears the finding. | Test |
| FR-027-AC-4 | A `risk` with `decision: accepted`, `decided_by: "A. Person"` and `arises_from: THREAT-1` clears the AC-3 finding. A `risk` with `decision: undecided`, and one with `decision: not_accepted`, do not. | Test |
| FR-027-AC-5 | The same corpus with its `threat_model` removed yields no finding under any of the three checks, and a corpus with no connection, sink or threat yields none. | Test |
| FR-027-AC-6 | A `risk` with `decision: accepted` and no `decided_by`, and one with `decision: accepted` and an empty `decided_by`, fail `quire validate` naming `decided_by`. A `risk` with no `decision` fails. A `risk` with `decision: undecided` and no `decided_by` validates; one with `decision: undecided` and a `decided_by` fails. `decision: maybe` fails. The updated `risk` skeleton validates with zero errors. | Test |
| FR-027-AC-7 | The `threat` manifest entry lists `asset`, `attack_surface`, `connection`, `data_sink` and `trust_boundary` in `allowed_links.threatens`; a `threat` that `threatens` each validates without a link diagnostic, and one that `threatens` a `risk` yields a link diagnostic. | Test |
| FR-027-AC-8 | The three rule `check` values equal their names, each rule has a non-empty `rationale`, no rule names a remediation, and the FR-025 registry still holds exactly nine entries. `RiskDecision.json` has exactly three members; `Risk.json` carries no `default` for `decision` or `decided_by`. Every `any_of` value is a member of its field's enum. The manifest declares `grammar_severity` `error` for the three checks, and every `present` condition sets `field: id`. | Test |
| FR-027-AC-9 | The module declares no engine kind, archetype, verb or field outside `traceability.flow_rules` data for these rules, and no rule, rationale or README text names or quotes a paywalled standard; only STRIDE, OWASP free guidance and NIST SP 800-154 are named. | Inspection |
| FR-027-AC-10 | A corpus with a `threat_model` considering `THREAT-1`, an `arises_from` risk with `decision: accepted` and no control raises no `trace:uncontrolled-threat` and no `trace:untreated-risk`; the same risk with `decision: undecided`, and one with `decision: not_accepted`, each raise `trace:untreated-risk` (with no `mitigates` edge). The manifest has no `threat-has-control` rule. | Test |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-008](./FR-008-security-nfr-needs-mitigation-target.md) (amended here), quire-rs FR-058 (`where` selector), [FR-025](./FR-025-control-safeguards-and-starter-flow-rules.md),
  [FR-026](./FR-026-threat-model-object.md); quire-rs FR-096; PLAT-1537 / PLAT-1538; FR-026 (`scopes`); the architecture
  objects `connection`, `data_sink` and the `crosses` edge.
- **Downstream**: quoin FR-202 (the report reads the findings of these three checks), PLAT-1543, PLAT-1544.
