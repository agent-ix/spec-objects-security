<!-- reviewer repo=agent-ix/spec-objects-security visibility=public quoin=0.30.0 module=spec-artifacts-process@unresolved id=SR-1607 method=code-review lang=spec pr=spec-objects-security#61 model=claude-opus-5-5 run=plat-1533-pr61-r1 -->

Code review of PR #61 at 6ab616f: **clean**. The diff from `origin/main` (7dd7f1a) is two Markdown files: the new FR-025 and one index line. No code, tests, schemas, manifest, typespec or build files changed. The index entry matches the FR-025 title and path. There is no build artifact, vendored file, pin or tracking record. The `ix://agent-ix/quire-rs/FR-096` form matches this repo's existing cross-repo references. The spec-content findings are in SR-1608 to SR-1613.

Note: no writable scratchpad was available outside the frozen worktree, and `quire validate` / `quoin` needed approval this session. The SR text is held in these comments for the fix-round coder to commit as `reviews/plat-1533-<method>.md`.

+++ [reviewer data]

```yaml
clean: true
scope:
  - {id: spec/functional/index.md, path: spec/functional/index.md, role: examined, excerpt: "* [FR-025: A control states safeguards and protects a connection or data_sink, and the module ships the remediation vocabulary and starter flow rules](./FR-025-control-safeguards-and-starter-flow-rules.md)"}
  - {id: FR-025, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: context_only, excerpt: "The module SHALL let a person state, on a `control`, a `safeguards` list drawn from a closed remediation vocabulary, and let the control `protects` a `connection` or a `data_sink`."}
findings: []
bindings: []
```

+++


- **@peter** - *7 minutes ago* [thread: 6f25ed73-4ce0-4a7e-b616-5dfc0da565bd]

<!-- reviewer repo=agent-ix/spec-objects-security visibility=public quoin=0.30.0 module=spec-artifacts-process@unresolved id=SR-1612 method=spec-review/spec-dependency-analysis lang=spec pr=spec-objects-security#61 model=claude-opus-5-5 run=plat-1533-pr61-r1 -->

Dependency analysis of FR-025 against quire-rs FR-096 (quire-rs#691), spec-objects-architecture FR-015 (spec-objects-architecture#51), and the PLAT-1532 and PLAT-1540 ticket text (read as data). **Verdict: FAIL.** Two high findings: under FR-096, the starter rules as declared do not load, and AC-7's load failure depends on a frontmatter schema that no requirement owns.

| FND | Severity | Check | Summary |
| --- | --- | --- | --- |
| FND-001 | high | soundness | `remove-from-sink` cannot clear the two sink rules that name it. FR-096 then refuses them at load, so the module does not load. |
| FND-002 | high | untestable-ac | AC-7's `any_of: [medical]` load failure needs a `data_classification` frontmatter-schema enum that no requirement declares |
| FND-003 | low | other | The `crosses` edge is attributed to the PLAT-1532 security FR-024 slot. PLAT-1532 and FR-015 put it in spec-objects-architecture FR-014. |
| FND-004 | low | trace | Dependencies says NFR-004 constrains FR-025, but no frontmatter relationship records that edge |

+++ [reviewer data]

```yaml
clean: false
scope:
  - {id: FR-025, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "The module SHALL also ship that vocabulary as `traceability.remediations` data and a starter set of `traceability.flow_rules` that use it."}
  - {id: FR-025-AC-5, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "Each of the six starter rules has one fail fixture that yields exactly one denial under its check naming the expected subject, and one pass fixture with no denial under that check. Applying one of the rule's remediations to the fail fixture clears the denial."}
  - {id: FR-025-AC-7, path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md, role: examined, excerpt: "The module loads with the six starter rules and the nine remediations. A copy of the module whose rule has `any_of: [medical]` on `regulated_categories` fails to load, and the error names the rule and the value `medical`."}
  - {id: FR-096, path: "quire-rs#691 spec/functional/FR-096-flow-rules.md", role: context_only, excerpt: "`removes`: some `match` condition tested with `any_of` or `present` has every one of its paths containing a step with that `edge` and `direction`, so removing the edge makes the condition fail."}
  - {id: FR-058-AC-22, path: "quire-rs spec/functional/FR-058-upward-trace-completeness.md", role: context_only, excerpt: "the vocabulary comes from the `from` archetype's frontmatter schema ... a field whose schema declares no `enum` has its `values` unchecked."}
  - {id: FR-015, path: "spec-objects-architecture#51 spec/functional/FR-015-data-sink.md", role: context_only, excerpt: "The module declares them on a self-contained open frontmatter schema, `DataSinkFrontmatter`, referenced by the `data_sink` object type through `frontmatter_schema_ref`"}
  - {id: FR-023, path: spec/functional/FR-023-regulated-data-categories-on-data-classification.md, role: context_only, excerpt: "The `data_classification` manifest entry SHALL extract the frontmatter list `regulated_categories` into `regulatedCategories`"}
findings:
  - fnd: FND-001
    severity: high
    confidence: high
    method: spec-review/spec-dependency-analysis
    check: soundness
    artifact_id: FR-025
    related_ids: [FR-025-AC-5, FR-025-AC-7, FR-096]
    path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md
    lines: "96, 105, 110-111"
    excerpt: |-
      `remove-from-sink` SHALL use `removes` on a `delivers_to` edge. ... In each, "data reaching the sink" is the `any_path` of `delivers_to` incoming then `carries` outgoing, together with the sink's own `carries` edges.
    finding: "Two rules name `remove-from-sink`: `health-in-llm-prompt-or-tool-call` and `regulated-data-in-log`. FR-096 accepts a `removes` remediation only when every path of some `match` condition has a step with that edge and direction. These rules read their data through `any_path`, and one path is the sink's own one-step `carries`, with no `delivers_to` step. So FR-096 refuses both rules at load, and the module does not load. That contradicts AC-7 ('loads with the six starter rules') and FR-025 line 134. The semantics are also wrong: on a sink with its own `carries` to `health`, removing `delivers_to` does not clear the denial, so AC-5 fails too. FR-025 also gives no `direction` for the `removes`, and FR-096 requires one. Fix: drop `remove-from-sink` from those two rules. Or split each sink rule into a delivers_to-path rule and an own-carries rule. Or get FR-096 to accept a `removes` that empties one path of an `any_path`. That last option is a quire-rs#691 decision."
  - fnd: FND-002
    severity: high
    confidence: medium
    method: spec-review/spec-dependency-analysis
    check: untestable-ac
    artifact_id: FR-025-AC-7
    related_ids: [FR-023, FR-096, FR-058-AC-22, FR-015]
    path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md
    lines: "166"
    excerpt: |-
      The module loads with the six starter rules and the nine remediations. A copy of the module whose rule has `any_of: [medical]` on `regulated_categories` fails to load, and the error names the rule and the value `medical`.
    finding: "FR-096 checks an `any_of` value against the enum of the field in the end archetype's frontmatter schema. It uses the FR-058-AC-22 lookup, and 'a field whose schema declares no `enum` leaves its values unchecked'. This module declares no `frontmatter_schema_ref` for any object type, so `data_classification` has none. FR-023 puts `RegulatedDataCategory` only on the record schema, under the key `regulatedCategories`. As specified, `any_of: [medical]` loads without error, so AC-7's second sentence cannot pass. FR-015 hit the same problem for `data_sink` and fixed it with `DataSinkFrontmatter`. FR-025 needs a `DataClassificationFrontmatter` schema declared here, or in an FR-023 amendment, as an upstream dependency. `trust_boundary.trust_level`, owned by PLAT-1532, has the same gap. Confidence is medium: if quire-rs resolves the enum through `data_schema` via the FR-069 mapping, the gap closes, but FR-096 and FR-058 both say frontmatter schema."
  - fnd: FND-003
    severity: low
    confidence: high
    method: spec-review/spec-dependency-analysis
    check: other
    artifact_id: FR-025
    related_ids: [FR-015]
    path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md
    lines: "39-41, 140, 175-176"
    excerpt: |-
      The `crosses` edge and the `trust_level` field of a `trust_boundary` belong to the trust-boundary requirement of PLAT-1532 (the slot FR-024 is reserved for it).
    finding: "PLAT-1532 (read as data, state Backlog) puts the `crosses` verb and `connection.allowed_links` in spec-objects-architecture FR-014. FR-015 also cites 'PLAT-1532 (FR-014)'. Only the frontmatter `trust_level` is spec-objects-security FR-024. FR-025 assigns both to the FR-024 slot, so a reader follows the wrong repo for `crosses`. Fix: name spec-objects-architecture FR-014 for `crosses` and this repo's FR-024 for `trust_level`, in the Description, Out of scope and Dependencies."
  - fnd: FND-004
    severity: low
    confidence: medium
    method: spec-review/spec-dependency-analysis
    check: trace
    artifact_id: FR-025
    related_ids: [NFR-004]
    path: spec/functional/FR-025-control-safeguards-and-starter-flow-rules.md
    lines: "1-18, 176-177"
    excerpt: |-
      - **Constrained by**: [NFR-004](../non-functional/NFR-004-regulated-categories-and-level-are-never-derived.md) for the never-derive principle, which applies equally to `safeguards`
    finding: "FR-025 says NFR-004 constrains it and 'applies equally to `safeguards`'. NFR-004 covers only `regulated_categories` and `level`, and neither document records the edge in `relationships`. So the trace graph does not show the constraint, and NFR-004 does not cover `safeguards` at all. Fix: add a `constrains` edge on NFR-004 (the FR-023 precedent) and extend NFR-004 to cover safeguards. Or state the never-derive rule for `safeguards` in FR-025 alone (it already has a SHALL NOT derive bullet) and drop the claim about NFR-004."
bindings: []
```

+++
