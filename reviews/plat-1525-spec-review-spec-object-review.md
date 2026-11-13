---
id: SR-057
title: spec-review/spec-object-review review of scope exclusion disposition metadata
type: SpecReview
analysis: base
scope: agent-ix/spec-objects-security; spec/functional/FR-004-role-schemas.md, spec/functional/FR-016-scope-exclusion-object.md;
  PR 54
review_set: subset
---

## Summary

Ticket: PLAT-1525. Two required authored fields cannot be extracted under the declared upstream mapping; the temporary expiry authored form is absent. Object review uses analysis base because the installed schema has no object-review enum value.

## Verdict

**FAIL** — Two required authored fields cannot be extracted under the declared upstream mapping; the temporary expiry authored form is absent. Object review uses analysis base because the installed schema has no object-review enum value.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The required Owner heading cannot populate owner through record-sections. FR-016 line 35 itself states that owner is reserved by the systems mapping, and upstream FR-081 treats headings for owned keys as prose. Thus a complete authored exclusion lacks required owner and cannot validate. Use a readable decision-owner key and map it in the consumer, or explicitly depend on an upstream mapping change; preserve the separate responsible-party meaning. | spec/functional/FR-016-scope-exclusion-object.md:37-42 |
| FND-002 | high | Approval reference does not name approval_ref under FR-081 normalization: the strings become approvalreference and approvalref. A body-extraction locator does not rename a record-sections key. Every fully authored exclusion therefore lacks the required approval_ref. Specify a heading that normalizes to the actual property, such as Approval ref, and verify the authored document path. | spec/functional/FR-016-scope-exclusion-object.md:37-39 |
| FND-003 | medium | The authored form and locator contract list only seven headings and never say where expires_at is written. The temporary_exception record requires it, but a conforming author has no defined heading, optional locator, or complete authored temporary-exception example. Define its authored section and conditional presence, and add a positive authored-document validation case for temporary_exception. | spec/functional/FR-016-scope-exclusion-object.md:59 |

## Examined scope

```yaml
scope:
- id: FR-016#behavior-L46
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: The `scope_exclusion` record schema SHALL require `set`, `clause`, `responsible`, `rationale`,
    `decision`, `owner` and `approval_ref`.
- id: FR-016#behavior-L47
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: '`responsible` SHALL be a `SemanticId` naming the component, service or document that is responsible
    for the clause.'
- id: FR-016#behavior-L48
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: The `responsible` value SHALL name the bare id of an artifact in the same bundle, for example
    `COMP-001`, which is the form Quire resolves with a bundle package.
- id: FR-016#behavior-L49
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: A `responsible` written as a cross-repository id such as `ix://agent-ix/example-platform/COMP-001`
    is refused by Quire as not a bundle artifact id when a bundle package is supplied, so this module
    does not admit it; a party outside the repository is named by an artifact in this bundle that stands
    for it.
- id: FR-016#behavior-L50
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: '`rationale` SHALL be a non-empty string.'
- id: FR-016#behavior-L51
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: '`decision` SHALL be exactly one of `delegated`, `accepted_risk` or `temporary_exception`.'
- id: FR-016#behavior-L52
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: '`owner` SHALL be a non-empty `SemanticId` naming the person or authority accountable for the
    decision.'
- id: FR-016#behavior-L53
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: '`approval_ref` SHALL be a non-empty string identifying the approval record. It SHALL NOT itself
    be treated as proof of approval.'
- id: FR-016#behavior-L54
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: A `temporary_exception` SHALL have a non-empty expiry value.
- id: FR-016#behavior-L55
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: '`delegated` and `accepted_risk` SHALL NOT carry an expiry value.'
- id: FR-016#behavior-L56
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: The expiry is an authored limit on the proposed disposition. FR-173 requires and enforces the
    FR-046 attestation validity interval.
- id: FR-016#behavior-L57
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: The `scope_exclusion` schema SHALL reject every property outside its seven and declare no approval-status
    or score property.
- id: FR-016#behavior-L58
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: The module SHALL export `scope_exclusion` and ship a skeleton that validates.
- id: FR-016#behavior-L59
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: The manifest entry for `scope_exclusion` SHALL require each of the seven authored sections,
    with a `section_body` locator.
- id: FR-016#behavior-L60
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: An authored exclusion with no `## Responsible` section SHALL fail validation with `semantic.record-invalid`
    naming `responsible`.
- id: FR-016-AC-1
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: '`ScopeExclusion.json` requires exactly `set`, `clause`, `responsible`, `rationale`, `decision`,
    `owner`, `approval_ref` and optional `expires_at`, is sealed, and `scope_exclusion` appears in the
    manifest `exports`.'
- id: FR-016-AC-2
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: A record without `responsible`, `owner` or `approval_ref`, with either identifier not a `SemanticId`,
    or with empty `rationale` or `approval_ref` fails validation.
- id: FR-016-AC-3
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: Each of `delegated`, `accepted_risk` and `temporary_exception` is accepted as `decision`; any
    other value is rejected. `temporary_exception` without `expires_at` and either other value with `expires_at`
    are rejected.
- id: FR-016-AC-4
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: The `scope_exclusion` skeleton validates with no `semantic.record-invalid` and has no placeholder
    token; removing any required section makes it fail naming the corresponding key.
- id: FR-016-AC-7
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: With a bundle package supplied, a fixture whose `## Responsible` is the bare id of a bundle
    artifact validates, and one whose `## Responsible` is `ix://agent-ix/example-platform/COMP-001` fails
    with `not a bundle artifact id`.
- id: FR-016-AC-5
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: The empty record `{}` fails `ScopeExclusion.json`.
- id: FR-016-AC-6
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: The manifest entry for `scope_exclusion` declares a required `section_body` locator for each
    required authored heading.
- id: FR-016#description
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: context_only
  excerpt: 'A clause that is outside the component''s boundary was a prose row in a table with a responsible
    component named in

    free text, which a reader could leave blank. The module SHALL add a `scope_exclusion` object type
    that states it as a

    record whose responsible party is required.'
- id: FR-016#authorization
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: 'The `scope_exclusion` declares a boundary and carries a person''s proposed out-of-scope disposition
    metadata. Those

    fields do not approve the exclusion. Quoin emits a disposition fact only when a person separately
    supplies the

    FR-046 attestation naming the actor, authority and validity interval; the fact retains the approval
    reference as

    evidence of that authorization (see `agent-ix/quoin` FR-173).'
- id: FR-016#type-count
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: context_only
  excerpt: 'The type is the twenty-fifth object type of the module, so the counts of

    [FR-003](./FR-003-semantic-manifest-contract.md) through [FR-006](./FR-006-security-safe-declarations.md)
    include it: it has a

    role-schema row in [FR-004](./FR-004-role-schemas.md), a skeleton under [FR-005](./FR-005-executable-skeletons.md)
    and the

    no-default rule of FR-006.'
- id: FR-016#owner-reserved
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: context_only
  excerpt: The key is `responsible` and not `owner`, because `owner` is a key the engine's record-sections
    mapping never reads (it is a systems member of `agent-ix/quire-rs` FR-075).
- id: FR-016#authored-headings
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: 'The authored form has sections with one inline-code value: `## Set`, `## Clause`, `## Responsible`,
    `## Rationale`,

    `## Decision`, `## Owner` and `## Approval reference`. The last three are an explicit human-authored
    decision and its

    owner and approval reference; Quire validates their shape, not whether the reference actually approves
    the decision.'
- id: FR-016#mapping
  path: spec/functional/FR-016-scope-exclusion-object.md
  role: examined
  excerpt: 'Quire reads each into the record key of the same name through the `record-sections` mapping
    (`agent-ix/quire-rs` FR-081), the

    same mapping as [FR-014](./FR-014-control-mappings-are-clause-references.md). The mapping does not
    read frontmatter, so no

    key is authored there. The frontmatter carries `id`, `title`, `type` and `object`, as every skeleton
    does.'
- id: FR-004#scope_exclusion
  path: spec/functional/FR-004-role-schemas.md
  role: examined
  excerpt: '| scope_exclusion | `ScopeExclusion` | `set`, `clause`, `responsible: SemanticId`, `rationale`,
    `decision`, `owner: SemanticId`, `approval_ref`, optional `expires_at` | none | `fields`, `clauses`,
    `operations` and `relations` forbidden by the seal; see [FR-016](./FR-016-scope-exclusion-object.md)
    |'
- id: quire-rs/FR-081#heading-normalization
  path: ../quire-rs/spec/functional/FR-081-record-sections-extraction.md
  role: context_only
  excerpt: "The engine SHALL match a `##` heading to a property of the record by\n  lowercasing both and\
    \ removing spaces, hyphens and underscores, so\n  `## Retry Policy` names `retryPolicy` and `## Associated\
    \ Types` names\n  `associated_types`."
- id: quire-rs/FR-081#owned-key
  path: ../quire-rs/spec/functional/FR-081-record-sections-extraction.md
  role: context_only
  excerpt: "The engine SHALL treat a heading that names an owned key, or no key, as\n  prose."
- id: quoin/FR-173#temporary-expiry
  path: ../quoin/spec/functional/FR-173-facts-from-mappings.md
  role: context_only
  excerpt: A `temporary_exception` SHALL carry an authored expiry no later than the attestation's `expiresAt`.
- id: US-001
  path: spec/usecase/US-001-declare-security-objects-against-semantic-core.md
  role: context_only
  excerpt: Declare security object types against semantic-core
```

## Review context and verification

Reviewed only the two-file `git diff origin/main...HEAD` at PR #54. Upstream FR-081 and companion quoin PR #882 FR-173 were read as context, not reviewed as changes. No applicable AssuranceProfile exists in the repository spec tree. The selected direct review is not a human acceptance of an enforced review run. No risk decision was made.

`quoin --version`: 0.30.1, exit 0; `quire --version`: quire 0.44.0 (engine 0.59.1), exit 0. Resolved executables: `/home/peter/.npm-global/bin/quoin` and `/home/peter/.npm-global/bin/quire` on terra. `quoin write . --types SpecReview` exited 0; installed contract is spec-artifacts-process@v0.31.0. `quire validate --scope . "spec/**/*.md" --summary` exited 0: 88/88 documents grammar-clean, no grammar findings. Validation emitted unused-import and duplicate-module-name warnings; the latter uses first-wins discovery. These advisory results do not establish semantic correctness.

`quire matrix --scope .` exited 0; all FR-016 criteria have existing trace tags. Inspection of the existing tests confirms they assert the previous four-key shape, so tagging is not evidence that this proposed extension is implemented. This specification-only PR intentionally does not claim implementation completion. An initial `quire matrix --scope . --json` exited 3 because --json is unsupported; `quire matrix --help` exited 0 and the supported command above succeeded. No older binary was substituted. Full output and exact commands are retained in the scratchpad logs.

## Traceability and applicability

US-001 traces to StR-001, and FR-004/FR-016 link to US-001; each changed criterion declares Test verification. The integrity failure-domain cross-check found no new callback, graph traversal, or executable user logic in this change. Human attestation and the opaque approval reference remain separate from the boundary assertion.

Language-specific Rust, React and Python execution checks and gap-analysis were skipped because no production or test code changed. Dependency analysis was skipped because no relationship edges changed. Evidence, risk-complexity, scope-boundary and full failure-domain reports were not selected: this narrow contract edit changes no verification method, algorithm, component allocation or execution model. Criterion-strength, correctness and fuzz generation were not selected for this review. No aggregate gate was run, per the review brief.

## Dispositions

Round 1: checked directly against fix commit `fbee533` and the current security PR diff.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | The authored key is decision_owner and its heading is Decision owner. FR-016 separates its accountable-person meaning from responsible, specifies a bare bundle artifact id, and names the consumer mapping to fact owner. No owner key is requested from record-sections. The consumer PR is outside this disposition scope. |
| FND-002 | fixed | The required heading is now Approval ref, which normalizes to approvalref, the same as approval_ref. AC-8 explicitly checks that authored fixture extraction yields approval_ref. |
| FND-003 | fixed | The authored form names Expires at, the manifest requires an optional section_body locator, and temporary_exception requires a valid expiry. New AC-8 supplies the complete authored fixture values and asserts successful validation plus extraction of expires_at. |

### Round 1 evidence

```yaml
dispositions:
- fnd: FND-001
  outcome: fixed
  after_excerpt: The key is `responsible` for the component, service or document accountable for the clause,
    and `decision_owner` for the person or authority accountable for the proposed disposition. The key
    `owner` is reserved by the engine's systems mapping and cannot be populated from a section (agent-ix/quire-rs
    FR-075/FR-081). Quoin FR-173 maps the extracted `decision_owner` to the discharge fact's `owner`;
    it does not conflate either value with `responsible`.
- fnd: FND-002
  outcome: fixed
  after_excerpt: 'The authored form has one inline-code value under each required heading: `## Set`, `##
    Clause`, `## Responsible`,

    `## Rationale`, `## Decision`, `## Decision owner` and `## Approval ref`. `## Expires at` is an additional
    inline-code'
- fnd: FND-003
  outcome: fixed
  after_excerpt: 'The manifest entry for `scope_exclusion` SHALL require `section_body` locators for the
    seven required headings and a `required: false` `section_body` locator for `## Expires at`.'
```

### Round 1 verdict

**PASS** for this method after dispositions: all original findings are fixed; no new findings. Original findings and verdict above remain the immutable initial review. The original review scope and method skips remain in force. The added FR-040 reference was checked only as evidence for the expiry fix; it is an instant-ordering contract in companion Quoin FR-040 AC-19. No implementation claim or human risk decision is made.

Quoin 0.30.1; Quire 0.44.0 (engine 0.59.1); both version commands exited 0. `quoin module list` exited 0 and identifies spec-artifacts-process@v0.31.0. `quire validate --scope . "spec/functional/FR-004-role-schemas.md" "spec/functional/FR-016-scope-exclusion-object.md" --summary` exited 0 with 2/2 documents grammar-clean and zero grammar findings. Unused-import and duplicate-module-name advisories remain visible in the log. No aggregate gate ran.

GitHub reports PR #54 OPEN and MERGEABLE at this head, with mergeStateStatus BLOCKED and reviewDecision REVIEW_REQUIRED. The observed CLA checks succeeded (one conditional CLA check skipped). This disposition clears the recorded semantic findings; it does not supply GitHub approval or merge authorization.
