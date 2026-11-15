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
safeguards. The module SHALL let a person state, on a `control`, a `safeguards` list drawn from a closed set of seven
safeguards a control can state, and let the control `protects` a `connection` or a `data_sink`. The module SHALL also ship
`traceability.remediations`, the nine changes a person may make to clear a denial, and a starter set of
`traceability.flow_rules` that use them. The seven safeguards are seven of the nine remediations; the other two,
`obtain-processor-agreement` and `remove-from-sink`, change a sink and are never stated by a control. The `Safeguard` set is
closed, and adding a member is a spec change.

The rule kind `flow_rules` is the only new engine kind. It is defined and evaluated by quire-rs FR-096. This requirement owns
the module's declarations only: the `Control` schema, the manifest `protects` targets, the remediation entries and the starter
rule entries. Rule evaluation, path semantics, load-time validation of rules, the report and its exit codes belong to quire-rs
FR-096 and the quire-cli relation report.

A remediation names a change to the model. It does not assert that the change is adequate. A person decides whether a control
that states `encrypt-in-transit` really protects the connection. The engine reads authored values and resolved edges and
never derives a fact.

The engine checks a rule's `any_of` value and a remediation's `value` against the `enum` of the field in the end archetype's
frontmatter schema (quire-rs FR-096 and FR-058-AC-22). A field with no frontmatter-schema `enum` is left unchecked. The module
therefore declares an open frontmatter schema for each of the two archetypes whose enum fields the starter data reads, and
depends on the trust-boundary requirement for the third.

The `data_sink` object type and the `delivers_to` edge are owned by `agent-ix/spec-objects-architecture` FR-015. The
`regulated_categories` field is owned by [FR-023](./FR-023-regulated-data-categories-on-data-classification.md). The
`crosses` edge and the `trust_boundary` object are not yet owned by an authored requirement: the architecture requirement for
`crosses` is supplied by spec-objects-architecture PR #51 / PLAT-1532, and this requirement names no requirement id for it
until that lands. The `trust_level` field of a `trust_boundary` belongs to this repository's FR-024 slot (PLAT-1532), which is
reserved and not yet authored.

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

- The closed enum `Safeguard`, emitted as `spec_objects_security/schemas/Safeguard.json`, with exactly the seven members
  `encrypt-in-transit`, `encrypt-at-rest`, `anonymize`, `pseudonymize`, `obtain-consent`, `restrict-region`,
  `validate-before-display`.
- An optional `safeguards` key on the `Control` record and schema.
- An open frontmatter schema `ControlFrontmatter` whose `safeguards` is a `Safeguard[]`, emitted as
  `spec_objects_security/schemas/ControlFrontmatter.json` and referenced by the `control` manifest entry through
  `frontmatter_schema_ref`.
- An open frontmatter schema `DataClassificationFrontmatter` whose `regulated_categories` is a `RegulatedDataCategory[]`
  (the enum of FR-023), emitted as `spec_objects_security/schemas/DataClassificationFrontmatter.json` and referenced by the
  `data_classification` manifest entry through `frontmatter_schema_ref`.
- A `frontmatter_field` locator on the `control` manifest entry.
- `protects: [externally-exposed, asset, connection, data_sink]` on the `control` manifest entry.
- `traceability.remediations`: one entry per `Safeguard` member, plus `obtain-processor-agreement` and `remove-from-sink`
  (nine entries).
- `traceability.flow_rules`: the six starter rules below.
- A `control` skeleton and fixtures that exercise each starter rule.

## Behavior

### Safeguards on a control

- The module SHALL declare `Safeguard` as a closed enum whose members are exactly the seven names above.
- `Safeguard` SHALL have no `unknown` or `none` member: a control that states no safeguard is stated by leaving the field out.
- `Safeguard` SHALL NOT contain `obtain-processor-agreement` or `remove-from-sink`, so that a control cannot state a change
  that only a sink can carry.
- `Control` SHALL admit an optional `safeguards`, a `Safeguard[]` with at least one item and unique items.
- The `control` manifest entry SHALL extract the frontmatter list `safeguards` into `safeguards` with a `frontmatter_field`
  locator that has `required: false` and no `multiple: true`.
- The module SHALL declare `ControlFrontmatter` and `DataClassificationFrontmatter` as open frontmatter schemas, each
  referenced by its manifest entry through `frontmatter_schema_ref`, so that the engine resolves the `enum` of
  `safeguards` and of `regulated_categories` when it checks a rule or a remediation.
- Frontmatter `safeguards` SHALL be the sole authored source. The module SHALL NOT accept a section form for it.
- The schema SHALL carry no `default` for `safeguards`, and the module SHALL NOT derive a safeguard from a control's title,
  mappings, effectiveness or any other field.
- The `control` manifest entry SHALL list `connection` and `data_sink` in `allowed_links.protects`, in addition to the targets
  it already lists.
- The `control` skeleton SHALL show `safeguards` in its frontmatter and validate with zero errors.

### Remediation registry

- The module SHALL declare one `traceability.remediations` entry for each `Safeguard` member, plus
  `obtain-processor-agreement` and `remove-from-sink`, and no other entry. The remediation vocabulary is thus nine
  names.
- Each entry SHALL carry a `name`, a `description`, and exactly one model change: `adds` (an edge from a document with a
  field value), `sets` (a frontmatter value on the subject), or `removes` (an edge).
- Each of the seven `Safeguard` members (`encrypt-in-transit`, `encrypt-at-rest`, `anonymize`, `pseudonymize`,
  `obtain-consent`, `restrict-region`, `validate-before-display`) SHALL use `adds: {edge: protects, direction: incoming,
  from: control, field: safeguards, value: <name>}`.
- `obtain-processor-agreement` SHALL use `sets: {field: processor_agreement, value: covered}` on the sink.
- `remove-from-sink` SHALL use `removes: {edge: delivers_to, direction: incoming}`.
- No starter rule names `obtain-consent` (it is there for a project rule to name). No starter rule names `remove-from-sink`:
  under FR-096 a `removes` matches only a `match` condition all of whose paths contain that edge, and the sink rules read
  their data by `any_path` that includes the sink's own `carries` edges, which have no `delivers_to` step. Removing the
  `delivers_to` edge would not clear a denial from the sink's own data.
- A remediation SHALL describe a change to the model only. It SHALL NOT claim that the change makes the system compliant;
  whether a stated control is adequate is a person's decision.

### Starter flow rules

The module SHALL ship these six `flow_rules`, each with a non-empty `rationale` and `remediations`. In each, "data reaching the sink" is
the `any_path` of `delivers_to` incoming then `carries` outgoing, together with the sink's own `carries` edges.

| Rule name and check | Subject | Match | Unless any | Remediations |
|---------------------|---------|-------|------------|--------------|
| `health-across-untrusted-boundary` | `connection` | carries `regulated_categories` containing `health`; crosses a boundary with `trust_level` in `untrusted`, `unknown` | a control with `safeguards` containing `encrypt-in-transit` protects it | `encrypt-in-transit` |
| `personal-across-untrusted-boundary` | `connection` | as above with `personal` | same | `encrypt-in-transit` |
| `regulated-data-to-uncovered-processor` | `data_sink` | data reaching it contains `health` or `personal`; `processor_agreement` in `not_covered`, `unknown` | a control with `safeguards` containing `anonymize` protects the sink; or the sink's own `processor_agreement` is `covered` | `obtain-processor-agreement`, `anonymize` |
| `health-in-llm-prompt-or-tool-call` | `data_sink` | `kind` in `llm_prompt`, `tool_call`; data reaching it contains `health`; `processor_agreement` in `not_covered`, `unknown` | a control with `safeguards` containing `anonymize` or `pseudonymize` protects the sink; or the sink's own `processor_agreement` is `covered` | `obtain-processor-agreement`, `anonymize`, `pseudonymize` |
| `health-in-log` | `data_sink` | `kind: log`; data reaching it contains `health` | a control with `safeguards` containing `pseudonymize` protects it | `pseudonymize` |
| `health-display-unvalidated` | `data_sink` | `kind: ui_screen`; data reaching it contains `health` | a control with `safeguards` containing `validate-before-display` protects it | `validate-before-display` |

- Each rule's `check` SHALL equal its name, so a project lowers severity with `--severity trace:<name>=warning`.
- Every `any_of` value in a starter rule SHALL be a member of the enum of that field in the target archetype's schema.
- Every remediation a starter rule names SHALL match that rule under FR-096: an `adds` matches an `unless_any` condition by
  `edge`, `direction`, `from`, `field` and `value`, and a `sets` matches a zero-step `unless_any` condition by `field` and
  `value`. A starter rule names no `removes`.
- In the sink rules, the `unless_any` condition "the sink's own `processor_agreement` is `covered`" SHALL be a zero-step
  condition, so that FR-096 accepts `obtain-processor-agreement` (a `sets`) at load.
- The rule named `health-in-log` SHALL match `health` only. A `kind: log` sink that receives only `personal` data is not
  denied by `health-in-log`; it is denied only under `regulated-data-to-uncovered-processor`, and only when its
  `processor_agreement` is `not_covered` or `unknown`. A project declares its own rule for any other log case.

Rationale (not requirements):

- The zero-step `covered` condition is a load-time anchor. Because `match` requires `processor_agreement` to be `not_covered`
  or `unknown`, it never holds together with `match` and clears no denial. A person clears the denial by agreement by setting
  `covered`, which makes `match` fail.
- The rule is named `health-in-log`, not `regulated-data-in-log` (the name PLAT-1540 uses), because it matches `health` only.
  This requirement's name is the one the module ships.

- No starter rule SHALL contain a value the engine infers. A rule reads authored frontmatter values and resolved edges only.
- The starter rules SHALL be declared so that a `data_sink` of `kind: llm_prompt` that receives `health` data, has
  `processor_agreement: not_covered` and has no protecting control satisfies the `match` of both
  `regulated-data-to-uncovered-processor` and `health-in-llm-prompt-or-tool-call`. Each rule has its own `check`.
- The module SHALL ship no rule for transfer regions, which need a project's own region list, and no per-role purpose rule,
  which needs a role-to-purpose-to-category mapping the model lacks. A project declares such rules in its own module.
- The module README SHALL record the per-role purpose gap.

## Engine impact

None of the behaviors above can be evaluated until quire-rs delivers `flow_rules` and `remediations` (FR-096, with FR-058 and
FR-084 amended by cross-reference; quire-rs#691 is open and this requirement follows its text), the `delivers_to` edge and
`data_sink` object exist in spec-objects-architecture (FR-015), the `crosses` edge exists in spec-objects-architecture (the requirement for it comes with PR #51 / PLAT-1532),
and the `trust_level` field and its frontmatter schema exist in this repository's FR-024 (PLAT-1532). The `Safeguard` enum, the manifest `protects`
targets and the remediation and rule entries are module data and can be authored and schema-validated first. The rule
fixtures need the engine. This requirement does not promise that code.

The engine loads the module only if every rule passes its load-time validation (unknown archetype, verb, value or
remediation; duplicate name; empty `match`; more than two path steps; a remediation that matches no condition of the rule
in the way FR-096 defines). The module's starter data SHALL pass that validation.

The solver lowering of the flow report (enum sorts, records and finite-collection quantifiers, quire-analyze FR-020 and
FR-031) is owned by PLAT-1541 in quire-spec-language and waits on QSL-1900, the production contract-package step. The module
declares no QSL.

## Out of scope

- Evaluation semantics, path walking, severity defaults, the `--flow` report and the `--strict` exit code: quire-rs FR-096 and
  the quire-cli relation-report requirement.
- The `data_sink` object type, its kinds and `processor_agreement` values, and the `delivers_to` verb: spec-objects-architecture
  FR-015.
- The `crosses` edge: spec-objects-architecture (PR #51 / PLAT-1532). The `trust_level` field and its frontmatter schema: this repository's
  FR-024 (both PLAT-1532).
- Records of processing (PLAT-1657), threat-model artifacts (milestone M3), runtime monitors, Cedar.
- Automatic derivation of a category, trust level, processor-agreement state or safeguard, and any judgement that a stated
  safeguard is adequate.

## Acceptance Criteria

FR-025-AC-1 to AC-6 and AC-13 evaluate the module's rule data through the engine and need the quire-rs and
spec-objects-architecture work above; they are held here as module fixtures. AC-1 to AC-4 are draft ACs a to d of PLAT-1533,
AC-7 is draft AC e and needs the engine's load-time validation, and AC-6 is the module-side fixture for draft AC g. AC-5 and
AC-13 add per-rule and overlap fixtures. AC-8 to AC-12 and AC-14 are module-only checks. Draft AC f (undeclared remediation,
three path steps, duplicate name, an `adds` that matches nothing) is owned by quire-rs FR-096-AC-6 and AC-7. Draft ACs g, h, i
and j (no finding without a modelled fact, byte-identical JSON, `--strict` exit codes, severity override) are owned by quire-rs
FR-096 and the quire-cli relation-report requirement, where they are evaluated over the engine and not over this module's data.

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-025-AC-1 | Seeded model: `CONN-1` carries a classification with `regulated_categories: [health]` and crosses a boundary with `trust_level: untrusted`, and no control protects it. `quire relations --flow` reports exactly one denial under `trace:health-across-untrusted-boundary` that names `CONN-1`, the classification, the boundary and `encrypt-in-transit`. | Test |
| FR-025-AC-2 | The AC-1 model plus a control with `safeguards: [encrypt-in-transit]` that `protects` `CONN-1` reports no denial. | Test |
| FR-025-AC-3 | A `data_sink` of `kind: llm_prompt` with `processor_agreement: not_covered`, fed by a connection carrying `health`, is denied under `trace:health-in-llm-prompt-or-tool-call`. | Test |
| FR-025-AC-4 | The AC-3 sink with `processor_agreement: covered` is not denied by `health-in-llm-prompt-or-tool-call`. With `processor_agreement: unknown` it is denied. | Test |
| FR-025-AC-5 | Each of the six starter rules has one fail fixture that yields exactly one denial under its check naming the expected subject, and one pass fixture with no denial under that check. Applying one of the rule's remediations to the fail fixture clears the denial. | Test |
| FR-025-AC-6 | A corpus in which no connection carries a classification and no sink exists produces no finding from any of the six starter rules. | Test |
| FR-025-AC-7 | The module loads with the six starter rules and the nine remediations. A copy of the module whose rule has `any_of: [medical]` on `regulated_categories` fails to load, and the error names the rule and the value `medical`. A copy whose remediation has `value: encrypt-in-transt` fails to load naming the remediation. | Test |
| FR-025-AC-8 | `Safeguard.json` has exactly the seven members listed, and no `unknown`, `none`, `obtain-processor-agreement` or `remove-from-sink` member. A control with `safeguards: [encrypt-in-transit]` validates; one with `safeguards: [shield]`, `safeguards: [remove-from-sink]`, `safeguards: []` or a duplicated member fails validation with a located message. A control without the field validates and its record has no `safeguards` key. The `Control` schema carries no `default` for `safeguards`. | Test |
| FR-025-AC-9 | The `control` manifest entry lists `connection` and `data_sink` in `allowed_links.protects`; a `control` that `protects` a `connection` and one that `protects` a `data_sink` each validate without a link diagnostic. The `safeguards` locator has `required: false` and no `multiple: true`, and the `control` skeleton shows `safeguards` and validates with zero errors. | Test |
| FR-025-AC-10 | The remediation names are the seven `Safeguard` members plus `obtain-processor-agreement` and `remove-from-sink`. Every remediation a starter rule names matches that rule under FR-096: an `adds` matches an `unless_any` condition, a `sets` matches a zero-step `unless_any` condition, and no starter rule names a `removes`. | Inspection |
| FR-025-AC-11 | `ControlFrontmatter.json` and `DataClassificationFrontmatter.json` exist and are open schemas. The first holds `safeguards` as a `Safeguard[]` and the second holds `regulated_categories` as a `RegulatedDataCategory[]`; the `control` and `data_classification` manifest entries reference them through `frontmatter_schema_ref`. Every starter-rule `any_of` value and every remediation `value` is a member of the enum of its field in the frontmatter schema of the end archetype that the module declares. | Test |
| FR-025-AC-12 | Each starter rule's `check` equals its `name`, and each carries a non-empty `rationale`. Each rule's `remediations` are in the nine. | Test |
| FR-025-AC-13 | A `data_sink` of `kind: llm_prompt` that receives `health` data, with `processor_agreement: not_covered` and no protecting control, is denied under both `trace:regulated-data-to-uncovered-processor` and `trace:health-in-llm-prompt-or-tool-call`, each naming the sink. A `kind: log` sink receiving only `personal` data, with `processor_agreement: covered`, yields no denial from any starter rule; with `processor_agreement: not_covered` it is denied under `trace:regulated-data-to-uncovered-processor` and not under `trace:health-in-log`. | Test |
| FR-025-AC-14 | The manifest declares no rule for transfer regions and no per-role purpose rule. The README records the per-role purpose gap. No remediation or rule text claims that a change makes a system compliant, and no rule text, rationale or README names or quotes a paywalled standard. | Inspection |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-023](./FR-023-regulated-data-categories-on-data-classification.md);
  quire-rs FR-096 (`flow_rules` and `remediations`); spec-objects-architecture FR-015 (`data_sink`, `delivers_to`); spec-objects-architecture `crosses`
  requirement (PR #51 / PLAT-1532, no id yet); this repository's FR-024 (`trust_level`, PLAT-1532)
- **Downstream**: PLAT-1479 (remediations), PLAT-1540 (starter rules), PLAT-1541 (solver lowering, waits on QSL-1900)
