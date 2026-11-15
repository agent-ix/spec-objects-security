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


- **@peter** - *7 minutes ago* [thread: a3e9d02b-769a-4160-94e8-e3ae71fc7582]

<!-- reviewer repo=agent-ix/quire-rs visibility=unmeasured quoin=unmeasured module=spec-artifacts-process@unresolved id=SR-20261115183663 method=code-review lang=spec pr=quire-rs#691 model=claude-opus-5-5 run=plat-1533-qrs691-r1 -->

Clean. Spec-only diff at head 33a95e3 (FR-096 new; FR-058, FR-084, index amended). No Rust or production code, so rust-review and gap-analysis do not apply. No build artifacts, copied files, pins or private-repo internals. quoin/quire/gh were not runnable in this reviewer session (approval gate), so `quoin=` and `visibility=` are unmeasured.

+++ [reviewer data]

```yaml
clean: true
scope:
  - {id: FR-096, path: spec/functional/FR-096-flow-rules.md, role: examined, excerpt: "The engine SHALL evaluate each flow_rules declaration of a loaded module over every document of its subject archetypes and SHALL report a denial under trace:<check> for each subject where all match conditions hold and no unless_any condition holds."}
  - {id: FR-058, path: spec/functional/FR-058-upward-trace-completeness.md, role: examined, excerpt: "A rule that must read a field at the far end of an edge, or combine several such conditions, is not a required_relations entry; it is a flow_rules declaration (FR-096)"}
  - {id: FR-084, path: spec/functional/FR-084-two-way-relation-coverage-report.md, role: examined, excerpt: "The relations report gains a flow section: the quire.flow-report/v1 of FR-096"}
  - {id: spec/functional/index.md, path: spec/functional/index.md, role: examined, excerpt: "* [FR-096: Flow rules and remediations, declared as module data](./FR-096-flow-rules.md)"}
findings: []
bindings: []
```

+++
