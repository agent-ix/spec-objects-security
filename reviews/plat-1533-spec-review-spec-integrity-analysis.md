<!-- reviewer repo=agent-ix/spec-objects-security visibility=public quoin=0.30.0 module=spec-artifacts-process@unresolved id=SR-1610 method=spec-review/spec-integrity-analysis lang=spec pr=spec-objects-security#61 model=claude-opus-5-5 run=plat-1533-pr61-r1 -->

Integrity analysis of FR-025. **Verdict: FAIL.** AC-10 contradicts FR-096's matching rule, so it cannot pass as written. Several SHALL statements have no acceptance criterion. AC-1 to AC-4, AC-6, AC-8 and AC-9 were examined and found clean.

| FND | Severity | Check | Summary |
| --- | --- | --- | --- |
| FND-001 | high | soundness | AC-10 requires every named remediation to match an `unless_any` condition. `remove-from-sink` is a `removes`, and FR-096 matches a `removes` only against a `match` condition. |
| FND-002 | medium | coverage | Five SHALL behaviours have no AC: the check equals the name, both sink rules fire, no region or purpose rule ships, the README gap, and no claim of compliance |
| FND-003 | low | other | The AC preamble says AC-1 to AC-9 are module-owned and that draft ACs a to g are held here. The table has AC-10, and draft AC f is not held here. |

+++ [reviewer data]

```yaml
clean: false
scope:
  - {id: FR-025-AC-1, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "Seeded model: `CONN-1` carries a classification with `regulated_categories: [health]` and crosses a boundary with `trust_level: untrusted`, and no control protects it. `quire relations --flow` reports exactly one denial under `trace:health-across-untrusted-boundary` that names `CONN-1`, the classification, the boundary and `encrypt-in-transit`."}
  - {id: FR-025-AC-2, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "The AC-1 model plus a control with `safeguards: [encrypt-in-transit]` that `protects` `CONN-1` reports no denial."}
  - {id: FR-025-AC-3, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "A `data_sink` of `kind: llm_prompt` with `processor_agreement: not_covered`, fed by a connection carrying `health`, is denied under `trace:health-in-llm-prompt-or-tool-call`."}
  - {id: FR-025-AC-4, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "The AC-3 sink with `processor_agreement: covered` is not denied by `health-in-llm-prompt-or-tool-call`. With `processor_agreement: unknown` it is denied."}
  - {id: FR-025-AC-6, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "A corpus in which no connection carries a classification and no sink exists produces no finding from any of the six starter rules."}
  - {id: FR-025-AC-8, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "`Safeguard.json` has exactly the nine members listed, and no `unknown` or `none` member. A control with `safeguards: [encrypt-in-transit]` validates; one with `safeguards: [shield]`, `safeguards: []` or a duplicated member fails validation with a located message. A control without the field validates and its record has no `safeguards` key. The `Control` schema carries no `default` for `safeguards`."}
  - {id: FR-025-AC-9, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "The `control` manifest entry lists `connection` and `data_sink` in `allowed_links.protects`; a `control` that `protects` a `connection` and one that `protects` a `data_sink` each validate without a link diagnostic. The `safeguards` locator has `required: false` and no `multiple: true`, and the `control` skeleton shows `safeguards` and validates with zero errors."}
  - {id: FR-025-AC-10, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "The `remediations` set equals the `Safeguard` set. Every remediation a starter rule names has a change that matches one of that rule's `unless_any` conditions."}
  - {id: FR-025, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "The module SHALL ship these six `flow_rules`, each with a `rationale` and `remediations`."}
findings:
  - fnd: FND-001
    severity: high
    confidence: high
    method: spec-review/spec-integrity-analysis
    check: soundness
    artifact_id: FR-025-AC-10
    related_ids: [FR-025, FR-096]
    path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md
    lines: "116, 169"
    excerpt: |-
      The `remediations` set equals the `Safeguard` set. Every remediation a starter rule names has a change that matches one of that rule's `unless_any` conditions.
    finding: "`remove-from-sink` is a `removes` (line 96). Under FR-096, a `removes` matches a rule through a `match` condition, never through `unless_any`, and none of the starter rules has an `unless_any` on `delivers_to`. Two starter rules name `remove-from-sink`. So AC-10 is false of the module's own declared data, and the Behavior bullet on line 116 contradicts FR-096. Fix: restate both to match FR-096: `adds` and `sets` against `unless_any`, `removes` against a `match` condition on all its paths. Then resolve SR-1612 FND-001, which is why even the FR-096 form fails here."
  - fnd: FND-002
    severity: medium
    confidence: high
    method: spec-review/spec-integrity-analysis
    check: coverage
    artifact_id: FR-025
    related_ids: [FR-025-AC-5]
    path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md
    lines: "99, 114, 118-122"
    excerpt: |-
      - Each rule's `check` SHALL equal its name, so a project lowers severity with `--severity trace:<name>=warning`.
    finding: "These SHALL behaviours are traced by no AC. (1) `check` equals the rule name (line 114). (2) Both `regulated-data-to-uncovered-processor` and `health-in-llm-prompt-or-tool-call` are reported for one health LLM sink (line 118). (3) No transfer-region rule and no per-role purpose rule ships, and the purpose gap is recorded in the README (lines 120-122). (4) A remediation SHALL NOT claim compliance (line 99). (5) Every rule carries a `rationale`. PLAT-1540 AC 5 (read as data) also asks for a scan that checks the rule text and README name no paywalled standard. No FR-025 AC carries it. Fix: add one Inspection AC and one Test AC that cover these items."
  - fnd: FND-003
    severity: low
    confidence: high
    method: spec-review/spec-integrity-analysis
    check: other
    artifact_id: FR-025
    related_ids: [FR-025-AC-10, FR-096]
    path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md
    lines: "153-156"
    excerpt: |-
      FR-025-AC-1 to AC-9 are module-owned. The seeded-model results (the draft ACs a to g of PLAT-1533) are held here as module fixtures
    finding: "The table has AC-10, which the preamble leaves out. AC-1 to AC-7 also need the engine, so 'module-owned' does not distinguish them. Draft AC f (an undeclared remediation, three path steps, a duplicate name, an `adds` that matches nothing) has no FR-025 AC. FR-096-AC-6 and AC-7 own it, and FR-015 says f is shared by FR-096 and FR-025. Fix: say AC-1 to AC-10, say which ACs need the engine, and say that f is owned by FR-096-AC-6 and AC-7."
bindings: []
```

+++


- **@peter** - *7 minutes ago* [thread: 7143e103-7354-49b1-9f44-1c0000083b30]

<!-- reviewer repo=agent-ix/spec-objects-security visibility=public quoin=0.30.0 module=spec-artifacts-process@unresolved id=SR-1611 method=spec-review/spec-object-review lang=spec pr=spec-objects-security#61 model=claude-opus-5-5 run=plat-1533-pr61-r1 -->

Object review of the FR-025 domain objects: the `Safeguard` enum, `Control.safeguards`, the `control` `protects` targets, and the nine remediation entries. **Verdict: FAIL (medium).** The `protects` targets `connection` and `data_sink` agree with FR-015. Six of the nine remediation shapes are fully specified.

| FND | Severity | Check | Summary |
| --- | --- | --- | --- |
| FND-001 | medium | ambiguous | `obtain-consent` has no model change, so two implementers would declare different entries. No archetype has a consent field. |
| FND-002 | medium | other | `safeguards` gets an enum only on the `Control` record schema, with no control frontmatter schema. FR-096 therefore skips the remediation `value` check, and `vocabularies` leaves out `control.safeguards`. |
| FND-003 | low | other | `Safeguard` admits three values a control never states: `obtain-processor-agreement`, `obtain-consent` and `remove-from-sink` |

+++ [reviewer data]

```yaml
clean: false
scope:
  - {id: FR-025, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "The module SHALL declare `Safeguard` as a closed enum whose members are exactly the nine names above. Adding a member is a spec change."}
  - {id: FR-025-AC-8, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: context_only, excerpt: "`Safeguard.json` has exactly the nine members listed, and no `unknown` or `none` member."}
  - {id: FR-025-AC-9, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: context_only, excerpt: "The `control` manifest entry lists `connection` and `data_sink` in `allowed_links.protects`"}
  - {id: FR-015, path: "spec-objects-architecture#51 spec/functional/FR-015-data-sink.md", role: context_only, excerpt: "The `control` `safeguards` field, `protects` onto `connection` and `data_sink`, and the starter rules: `agent-ix/spec-objects-security` FR-025 (PLAT-1540)."}
findings:
  - fnd: FND-001
    severity: medium
    confidence: high
    method: spec-review/spec-object-review
    check: ambiguous
    artifact_id: FR-025
    related_ids: [FR-096]
    path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md
    lines: "94-95"
    excerpt: |-
      `obtain-consent` SHALL be declared with the same shape rules as the others. No starter rule names it. It exists so a project rule can.
    finding: "Each of the other eight entries gets one specific change: `adds` with protects from control, `sets` on `processor_agreement`, or `removes` on `delivers_to`. `obtain-consent` gets none. FR-096 refuses an entry with no `adds`, `sets` or `removes`, so an implementer has to invent one. It could be `adds` with protects from a control whose safeguards contain `obtain-consent`, or `sets` on a consent field that no archetype declares. A project rule written against one form fails FR-096's matching check against the other. Fix: state the change. The likely choice is `adds: {edge: protects, direction: incoming, from: control, field: safeguards, value: obtain-consent}`, making it a seventh control-stated safeguard."
  - fnd: FND-002
    severity: medium
    confidence: medium
    method: spec-review/spec-object-review
    check: other
    artifact_id: FR-025
    related_ids: [FR-025-AC-8, FR-096, FR-015]
    path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md
    lines: "54-58, 73-75"
    excerpt: |-
      - The `control` manifest entry SHALL extract the frontmatter list `safeguards` into `safeguards` with a `frontmatter_field` locator that has `required: false` and no `multiple: true`.
    finding: "FR-096 checks a remediation `adds.value` against 'the `enum` of its `field` by the lookup above', which is the frontmatter schema of `from` (`control`). Its `vocabularies` list only frontmatter-schema enums. FR-025 puts `Safeguard` only on the `Control` record and record schema. No `ControlFrontmatter` exists, and the module declares no `frontmatter_schema_ref` anywhere. So a typo such as `value: encrypt-in-transt` in a remediation loads unchecked. The report also never states the safeguard vocabulary that PLAT-1541 lowers to an enum sort. FR-015 fixed the same problem with `DataSinkFrontmatter`. Fix: declare an open `ControlFrontmatter` with `safeguards: Safeguard[]`, referenced through `frontmatter_schema_ref`, list it in Outputs, and add an AC."
  - fnd: FND-003
    severity: low
    confidence: low
    method: spec-review/spec-object-review
    check: other
    artifact_id: FR-025
    related_ids: [FR-025-AC-8, FR-025-AC-10]
    path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md
    lines: "57-59, 85-87"
    excerpt: |-
      - The six safeguards that a control states (`encrypt-in-transit`, `encrypt-at-rest`, `anonymize`, `pseudonymize`, `validate-before-display`, `restrict-region`) SHALL use `adds` with the incoming `protects` edge from a `control` whose `safeguards` contain the name.
    finding: "FR-025 itself says only six names are safeguards that a control states. Because `Safeguard` must equal the remediation set, `control.safeguards: [remove-from-sink]` or `[obtain-processor-agreement]` validates, and that statement satisfies no rule and protects nothing. This follows the PLAT-1533 design note (read as data), so confidence is low. A tighter model would make `Safeguard` the six (seven with `obtain-consent`) and the remediation vocabulary a superset of it."
bindings: []
```

+++
