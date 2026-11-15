<!-- reviewer repo=agent-ix/spec-objects-security visibility=public quoin=0.30.0 module=spec-artifacts-process@unresolved id=SR-1613 method=spec-review/spec-failure-domain-analysis lang=spec pr=spec-objects-security#61 model=claude-opus-5-5 run=plat-1533-pr61-r1 -->

Failure-domain analysis of the six starter rules, read under FR-096 semantics. **Verdict: PASS with findings (low).** Examined and clean:

- The connection rules over several boundaries: any untrusted boundary is enough to fire.
- A connection with no `crosses` edge is not denied. PLAT-1532 treats that as staying inside one zone.
- `semi_trusted` is deliberately not denied.
- A control that protects the connection does not clear a sink rule.

The `remove-from-sink` failure is SR-1612 FND-001.

| FND | Severity | Check | Summary |
| --- | --- | --- | --- |
| FND-001 | low | soundness | The new `unless_any` "sink's own `processor_agreement` is `covered`" can never hold while `match` holds, so it is a dead condition kept only to satisfy load-time matching |
| FND-002 | low | ambiguous | `regulated-data-in-log` matches only `health`, so personal data in a log is never denied, and the name says otherwise |

+++ [reviewer data]

```yaml
clean: false
scope:
  - {id: FR-025, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "| `regulated-data-to-uncovered-processor` | `data_sink` | data reaching it contains `health` or `personal`; `processor_agreement` in `not_covered`, `unknown` | a control with `safeguards` containing `anonymize` protects the sink; or the sink's own `processor_agreement` is `covered` | `obtain-processor-agreement`, `anonymize` |"}
  - {id: FR-025-AC-4, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: context_only, excerpt: "The AC-3 sink with `processor_agreement: covered` is not denied by `health-in-llm-prompt-or-tool-call`. With `processor_agreement: unknown` it is denied."}
findings:
  - fnd: FND-001
    severity: low
    confidence: medium
    method: spec-review/spec-failure-domain-analysis
    check: soundness
    artifact_id: FR-025
    related_ids: [FR-096]
    path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md
    lines: "109-110"
    excerpt: |-
      | `regulated-data-to-uncovered-processor` | `data_sink` | data reaching it contains `health` or `personal`; `processor_agreement` in `not_covered`, `unknown` | a control with `safeguards` containing `anonymize` protects the sink; or the sink's own `processor_agreement` is `covered` | `obtain-processor-agreement`, `anonymize` |
    finding: "`match` requires `processor_agreement` to be `not_covered` or `unknown`, so the zero-step `unless_any` `processor_agreement: covered` can never hold at the same time. It changes no outcome. It exists only so that FR-096's `sets` matching accepts `obtain-processor-agreement`, and the PR body presents it as a behaviour. This differs from the PLAT-1540 table (read as data), which has no such clause. A reader takes it for a second way to clear the denial. Fix: say in FR-025 that the clause is a load-time anchor for the `sets` remediation. Or ask quire-rs#691 to let a `sets` match by falsifying a zero-step `match` condition, and drop the clause."
  - fnd: FND-002
    severity: low
    confidence: low
    method: spec-review/spec-failure-domain-analysis
    check: ambiguous
    artifact_id: FR-025
    related_ids: []
    path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md
    lines: "111"
    excerpt: |-
      | `regulated-data-in-log` | `data_sink` | `kind: log`; data reaching it contains `health` | a control with `safeguards` containing `pseudonymize` protects it | `pseudonymize`, `remove-from-sink` |
    finding: "The rule is named for regulated data, but it matches `health` only. A log that receives `personal` (or `financial`) data is never denied, and a project lowering `trace:regulated-data-in-log` may believe it covers all regulated categories. PLAT-1540 has the same text, so this is inherited. Fix: rename it `health-in-log`, or add `personal` to `any_of`."
bindings: []
```

+++


- **@peter** - *6 minutes ago* [thread: b9dec41f-7028-410c-ada8-92e2a644a02a]

<!-- reviewer repo=agent-ix/spec-objects-security visibility=public quoin=0.30.0 module=spec-artifacts-process@unresolved id=SR-1608 method=spec-review/base lang=spec pr=spec-objects-security#61 model=claude-opus-5-5 run=plat-1533-pr61-r1 -->

Base spec-review of FR-025 at 6ab616f, against quire-rs FR-096 (#691), spec-objects-architecture FR-015 (#51), and the PLAT-1540 and PLAT-1532 ticket text (read as data; PLAT-1532 is Backlog).

**Verdict: changes requested.** FR-025 matches PLAT-1540 on rule names, subjects, matches and remediations. It adds a `covered` unless clause to the two processor rules. It matches FR-015 on sink kinds, `processor_agreement` values and `delivers_to`. It matches PLAT-1532 on `trust_level` values: `untrusted` and `unknown` are both in `TrustLevel` (`typespec/main.tsp:121`).

Three findings block merge:

- **SR-1612 FND-001 (high):** `remove-from-sink` stops FR-096 from loading the two sink rules, because their `any_path` includes the sink's own `carries` path.
- **SR-1610 FND-001 (high):** AC-10 and the Behavior bullet test the remediation against `unless_any`, but FR-096 matches a `removes` against `match`.
- **SR-1612 FND-002 (high, medium confidence):** AC-7's `medical` load failure needs a `data_classification` frontmatter-schema enum. Nothing declares one.

Medium findings: SR-1611 FND-001 and FND-002 (`obtain-consent` shape; no control frontmatter schema), SR-1610 FND-002 (behaviours with no AC), SR-1609 FND-001. The rest are low.

Not independently re-run: `quire validate` and `quoin` needed approval this session. The lead reports FR-025 and the index validate. This review adds no findings of its own. Base findings are distributed to the sub-analyses above.

+++ [reviewer data]

```yaml
clean: true
scope:
  - {id: FR-025, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "The module SHALL let a person state, on a `control`, a `safeguards` list drawn from a closed remediation vocabulary, and let the control `protects` a `connection` or a `data_sink`. The module SHALL also ship that vocabulary as `traceability.remediations` data and a starter set of `traceability.flow_rules` that use it."}
  - {id: spec/functional/index.md, path: spec/functional/index.md, role: context_only, excerpt: "* [FR-025: A control states safeguards and protects a connection or data_sink, and the module ships the remediation vocabulary and starter flow rules](./FR-025-control-safeguards-and-starter-flow-rules.md)"}
findings: []
bindings: []
```

+++
