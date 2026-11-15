---
id: FR-025
title: "A control states safeguards and protects a connection or data_sink, and the module ships the remediation vocabulary and starter flow rules"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-023"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-096"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-058"
    type: "references"
  - target: "ix://agent-ix/spec-objects-architecture/FR-015"
    type: "depends_on"
---
# FR-025: A control states safeguards and protects a connection or data_sink, and the module ships the remediation vocabulary and starter flow rules

## Description

A boundary-crossing rule needs to ask whether a connection or a sink is protected, and by what. Today a `control` can
`protects` only `externally-exposed` and `asset` documents, and it carries no machine-readable statement of what it
safeguards. The module SHALL let a person state, on a `control`, a `safeguards` list drawn from a closed remediation
vocabulary, and let the control `protects` a `connection` or a `data_sink`. The module SHALL also ship that vocabulary as
`traceability.remediations` data and a starter set of `traceability.flow_rules` that use it.

The rule kind `flow_rules` is the only new engine kind. It is defined and evaluated by quire-rs FR-096. This requirement owns
the module's declarations only: the `Control` schema, the manifest `protects` targets, the remediation entries and the starter
rule entries. Rule evaluation, path semantics, load-time validation of rules, the report and its exit codes belong to quire-rs
FR-096 and the quire-cli relation report.

A remediation names a change to the model. It does not assert that the change is adequate. A person decides whether a control
that states `encrypt-in-transit` really protects the connection. The engine reads authored values and resolved edges and
never derives a fact.

The `data_sink` object type and the `delivers_to` edge are owned by `agent-ix/spec-objects-architecture` FR-015. The
`regulated_categories` field is owned by [FR-023](./FR-023-regulated-data-categories-on-data-classification.md). The
`crosses` edge and the `trust_level` field of a `trust_boundary` belong to the trust-boundary requirement of PLAT-1532 (the
slot FR-024 is reserved for it).

Where a rule has a public-law source, its rationale may cite: HIPAA 45 CFR 164.312(e)(1) (transmission security) and
45 CFR 164.502(e) and 164.504(e) (business associate contracts); GDPR Art 28 (processor) and Art 32 (security of processing).
The free OWASP guidance for LLM applications may be cited for the prompt and tool-call rule. This requirement names and
quotes no paywalled standard.

## Inputs

- A `control` document whose frontmatter may carry `safeguards`, and whose `protects` edges may target a `connection` or a
  `data_sink`.
- The `Control` model in `typespec/main.tsp`.
- The `traceability` block of `spec_objects_security/manifest.yaml`.

## Outputs

- The closed enum `Safeguard`, emitted as `spec_objects_security/schemas/Safeguard.json`, with exactly the nine members
  `encrypt-in-transit`, `encrypt-at-rest`, `anonymize`, `pseudonymize`, `obtain-processor-agreement`, `obtain-consent`,
  `restrict-region`, `validate-before-display`, `remove-from-sink`.
- An optional `safeguards` key on the `Control` record and schema.
- A `frontmatter_field` locator on the `control` manifest entry.
- `protects: [externally-exposed, asset, connection, data_sink]` on the `control` manifest entry.
- `traceability.remediations`: one entry per `Safeguard` member.
- `traceability.flow_rules`: the six starter rules below.
- A `control` skeleton and fixtures that exercise each starter rule.

## Behavior

### Safeguards on a control

- The module SHALL declare `Safeguard` as a closed enum whose members are exactly the nine names above. Adding a member is a
  spec change.
- `Safeguard` SHALL have no `unknown` or `none` member: a control that states no safeguard is stated by leaving the field out.
- `Control` SHALL admit an optional `safeguards`, a `Safeguard[]` with at least one item and unique items.
- The `control` manifest entry SHALL extract the frontmatter list `safeguards` into `safeguards` with a `frontmatter_field`
  locator that has `required: false` and no `multiple: true`.
- Frontmatter `safeguards` SHALL be the sole authored source. The module SHALL NOT accept a section form for it.
- The schema SHALL carry no `default` for `safeguards`, and the module SHALL NOT derive a safeguard from a control's title,
  mappings, effectiveness or any other field.
- The `control` manifest entry SHALL list `connection` and `data_sink` in `allowed_links.protects`, in addition to the targets
  it already lists.
- The `control` skeleton SHALL show `safeguards` in its frontmatter and validate with zero errors.

### Remediation registry

- The module SHALL declare one `traceability.remediations` entry for each `Safeguard` member, and no entry that is not a
  member. The closed set of remediation names equals the `Safeguard` set.
- Each entry SHALL carry a `name`, a `description`, and exactly one model change: `adds` (an edge from a document with a
  field value), `sets` (a frontmatter value on the subject), or `removes` (an edge).
- The six safeguards that a control states (`encrypt-in-transit`, `encrypt-at-rest`, `anonymize`, `pseudonymize`,
  `validate-before-display`, `restrict-region`) SHALL use `adds` with the incoming `protects` edge from a `control` whose
  `safeguards` contain the name.
- `obtain-processor-agreement` SHALL use `sets` on the sink's `processor_agreement`, with the value `covered`.
- `obtain-consent` SHALL be declared with the same shape rules as the others. No starter rule names it. It exists so a project
  rule can.
- `remove-from-sink` SHALL use `removes` on a `delivers_to` edge.
- A remediation SHALL describe a change to the model only. It SHALL NOT claim that the change makes the system compliant;
  whether a stated control is adequate is a person's decision.

### Starter flow rules

The module SHALL ship these six `flow_rules`, each with a `rationale` and `remediations`. In each, "data reaching the sink" is
the `any_path` of `delivers_to` incoming then `carries` outgoing, together with the sink's own `carries` edges.

| Rule name and check | Subject | Match | Unless any | Remediations |
|---------------------|---------|-------|------------|--------------|
| `health-across-untrusted-boundary` | `connection` | carries `regulated_categories` containing `health`; crosses a boundary with `trust_level` in `untrusted`, `unknown` | a control with `safeguards` containing `encrypt-in-transit` protects it | `encrypt-in-transit` |
| `personal-across-untrusted-boundary` | `connection` | as above with `personal` | same | `encrypt-in-transit` |
| `regulated-data-to-uncovered-processor` | `data_sink` | data reaching it contains `health` or `personal`; `processor_agreement` in `not_covered`, `unknown` | a control with `safeguards` containing `anonymize` protects the sink; or the sink's own `processor_agreement` is `covered` | `obtain-processor-agreement`, `anonymize` |
| `health-in-llm-prompt-or-tool-call` | `data_sink` | `kind` in `llm_prompt`, `tool_call`; data reaching it contains `health`; `processor_agreement` in `not_covered`, `unknown` | a control with `safeguards` containing `anonymize` or `pseudonymize` protects the sink; or the sink's own `processor_agreement` is `covered` | `obtain-processor-agreement`, `pseudonymize`, `remove-from-sink` |
| `regulated-data-in-log` | `data_sink` | `kind: log`; data reaching it contains `health` | a control with `safeguards` containing `pseudonymize` protects it | `pseudonymize`, `remove-from-sink` |
| `health-display-unvalidated` | `data_sink` | `kind: ui_screen`; data reaching it contains `health` | a control with `safeguards` containing `validate-before-display` protects it | `validate-before-display` |

- Each rule's `check` SHALL equal its name, so a project lowers severity with `--severity trace:<name>=warning`.
- Every `any_of` value in a starter rule SHALL be a member of the enum of that field in the target archetype's schema.
- Every remediation a starter rule names SHALL have a model change matching one of that rule's `unless_any` conditions.
- No starter rule SHALL contain a value the engine infers. A rule reads authored frontmatter values and resolved edges only.
- The rule `regulated-data-to-uncovered-processor` and the rule `health-in-llm-prompt-or-tool-call` SHALL both be reported for
  a health-carrying LLM sink that fails both, each under its own check.
- The module SHALL ship no rule for transfer regions, which need a project's own region list. It SHALL ship no per-role
  purpose rule, which needs a role-to-purpose-to-category mapping the model lacks. A project declares such rules in its own
  module; the per-role purpose gap is recorded in the module README.

## Engine impact

None of the behaviors above can be evaluated until quire-rs delivers `flow_rules` and `remediations` (FR-096, with FR-058 and
FR-084 amended by cross-reference), the `delivers_to` edge and `data_sink` object exist in spec-objects-architecture
(FR-015), and the `crosses` edge and `trust_level` field exist (PLAT-1532). The `Safeguard` enum, the manifest `protects`
targets and the remediation and rule entries are module data and can be authored and schema-validated first. The rule
fixtures need the engine. This requirement does not promise that code.

The engine loads the module only if every rule passes its load-time validation (unknown archetype, verb, value or
remediation; duplicate name; empty `match`; more than two path steps; a remediation whose change matches none of the rule's
`unless_any`). The module's starter data SHALL pass that validation.

The solver lowering of the flow report (enum sorts, records and finite-collection quantifiers, quire-analyze FR-020 and
FR-031) is owned by PLAT-1541 in quire-spec-language and waits on QSL-1900, the production contract-package step. The module
declares no QSL.

## Out of scope

- Evaluation semantics, path walking, severity defaults, the `--flow` report and the `--strict` exit code: quire-rs FR-096 and
  the quire-cli relation-report requirement.
- The `data_sink` object type, its kinds and `processor_agreement` values, and the `delivers_to` verb: spec-objects-architecture
  FR-015.
- The trust-boundary crossing edge and `trust_level`: PLAT-1532.
- Records of processing (PLAT-1657), threat-model artifacts (milestone M3), runtime monitors, Cedar.
- Automatic derivation of a category, trust level, processor-agreement state or safeguard, and any judgement that a stated
  safeguard is adequate.

## Acceptance Criteria

FR-025-AC-1 to AC-9 are module-owned. The seeded-model results (the draft ACs a to g of PLAT-1533) are held here as module
fixtures and need the quire-rs and spec-objects-architecture work above. Draft ACs h, i and j (byte-identical JSON, `--strict`
exit codes, severity override) are owned by quire-rs FR-096 and the quire-cli relation-report requirement, where they are
evaluated over the engine and not over this module's data.

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-025-AC-1 | Seeded model: `CONN-1` carries a classification with `regulated_categories: [health]` and crosses a boundary with `trust_level: untrusted`, and no control protects it. `quire relations --flow` reports exactly one denial under `trace:health-across-untrusted-boundary` that names `CONN-1`, the classification, the boundary and `encrypt-in-transit`. | Test |
| FR-025-AC-2 | The AC-1 model plus a control with `safeguards: [encrypt-in-transit]` that `protects` `CONN-1` reports no denial. | Test |
| FR-025-AC-3 | A `data_sink` of `kind: llm_prompt` with `processor_agreement: not_covered`, fed by a connection carrying `health`, is denied under `trace:health-in-llm-prompt-or-tool-call`. | Test |
| FR-025-AC-4 | The AC-3 sink with `processor_agreement: covered` is not denied by `health-in-llm-prompt-or-tool-call`. With `processor_agreement: unknown` it is denied. | Test |
| FR-025-AC-5 | Each of the six starter rules has one fail fixture that yields exactly one denial under its check naming the expected subject, and one pass fixture with no denial under that check. Applying one of the rule's remediations to the fail fixture clears the denial. | Test |
| FR-025-AC-6 | A corpus in which no connection carries a classification and no sink exists produces no finding from any of the six starter rules. | Test |
| FR-025-AC-7 | The module loads with the six starter rules and the nine remediations. A copy of the module whose rule has `any_of: [medical]` on `regulated_categories` fails to load, and the error names the rule and the value `medical`. | Test |
| FR-025-AC-8 | `Safeguard.json` has exactly the nine members listed, and no `unknown` or `none` member. A control with `safeguards: [encrypt-in-transit]` validates; one with `safeguards: [shield]`, `safeguards: []` or a duplicated member fails validation with a located message. A control without the field validates and its record has no `safeguards` key. The `Control` schema carries no `default` for `safeguards`. | Test |
| FR-025-AC-9 | The `control` manifest entry lists `connection` and `data_sink` in `allowed_links.protects`; a `control` that `protects` a `connection` and one that `protects` a `data_sink` each validate without a link diagnostic. The `safeguards` locator has `required: false` and no `multiple: true`, and the `control` skeleton shows `safeguards` and validates with zero errors. | Test |
| FR-025-AC-10 | The `remediations` set equals the `Safeguard` set. Every remediation a starter rule names has a change that matches one of that rule's `unless_any` conditions. | Inspection |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-023](./FR-023-regulated-data-categories-on-data-classification.md);
  quire-rs FR-096 (`flow_rules` and `remediations`); spec-objects-architecture FR-015 (`data_sink`, `delivers_to`); the PLAT-1532
  trust-boundary requirement (`crosses`, `trust_level`)
- **Constrained by**: [NFR-004](../non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md) for the
  never-derive principle, which applies equally to `safeguards`
- **Downstream**: PLAT-1479 (remediations), PLAT-1540 (starter rules), PLAT-1541 (solver lowering, waits on QSL-1900)
