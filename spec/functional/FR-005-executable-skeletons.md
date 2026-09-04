---
id: FR-005
title: "Make every skeleton an executable typed fixture"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-071"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-072"
    type: "depends_on"
---
# FR-005: Make every skeleton an executable typed fixture

## Description

Every skeleton under `spec_objects_security/skeletons/` SHALL author its
declarations in the quoin FR-071/FR-072 Markdown forms (typed `## Properties`
table by default, `## Invariants` clause fences, `## Operations` subsections)
and validate through Quire against this module, accompanied by negative
fixtures that fail for a named reason, so that the skeletons are the module's
executable positive fixtures and the negatives pin what the schemas and the
engine refuse.

## Inputs

- The rewritten skeletons `skeletons/<type>.md`, one per object type, and the
  alternate-form skeletons `skeletons/asset.sysml.md`,
  `skeletons/secret.sysml.md`, `skeletons/threat.sysml.md`.
- Negative fixtures `tests/fixtures/negative/<type>-<case>.md`, each with
  frontmatter `expect:` naming the diagnostic code or reason the fixture must
  produce.
- The Quire wheel 0.46.0 or later, exposing `extract_semantic`,
  `validate_document`, and `Registry`, installed into the module's Python
  environment by `make dev-quire` (see Behavior).

## Outputs

- A validation result per skeleton with no error and no `semantic.record-invalid`.
- A semantic record per skeleton whose `fields`, `clauses`, and `operations`
  availability match the type's required set.

## Behavior

- Each skeleton whose type requires `fields` (`asset`, `role`, `permission`, `scope`, `mfa_method`, `threat`, `vulnerability`, `risk`, `audit_finding`, `data_classification`, `attack_surface`, `trust_boundary`, `secret`, `encryption_key`, `jwt_claim`, `csrf_token`, `control`, `audit_event`) SHALL author `## Properties` as one table with the header exactly `Field | Type | Multiplicity | Constraints`.
- Each skeleton whose type requires `clauses` (`trust_boundary`, `policy`, `control`, `password_policy`, `cors_policy`, `session_config`) SHALL author `## Invariants` with one `### <clauseId>` per clause, each owning exactly one ```` ```ocl ```` fence.
- The `auth_flow` skeleton SHALL author `## Operations` with one `### <name>` per exchange, an optional `| Param | Type | Multiplicity | Constraints |` table, a `Returns: <Type>[<multiplicity>]` line where the exchange returns a value, and optional `Pre:`/`Post:` lines that, when present, name clause ids declared in the same artifact.
- No skeleton SHALL carry a section its type does not require and its manifest entry does not assert.
- The `asset`, `secret`, and `threat` alternate skeletons SHALL author the same declarations as one ```` ```sysml ```` fence of `attribute <name> : <Type>[<mult>] { <constraints> }` lines, under that skeleton's frontmatter `id` and `title`; the module therefore ships two files under one id by intent, and the identity of their extracted `FieldDecl[]` is the obligation FR-005-AC-2 tests.
- Each skeleton's frontmatter SHALL carry `object: <type name>` beside `type: <type name>`, because Quire runs the semantic layer (extraction and record validation) on the `object:` archetype of a document; a skeleton without it validates its headings only.
- The manifest SHALL gain a `required: false` `section_body` locator for every `## Properties`, `## Invariants`, and `## Operations` section a skeleton introduces, so the section is asserted by the manifest and remains optional for existing artifacts.
- Every `Constraints` cell SHALL use only the constraint keywords the typed-table reader of the pinned Quire wheel accepts (`identity`, `min`, `max`, `exclusiveMin`, `exclusiveMax`, `minLength`, `maxLength`, `nonEmpty`, `unique`, and single-valued `enumValues`). `pattern` and `format` are members of semantic-core's closed `ConstraintKeyword` set that the reader rejects, and a multi-valued `enumValues` is either split by the constraint separator or silently truncated to its first value; both are engine defects reported upstream and neither is worked around by inventing a cell form.
- Because a closed vocabulary cannot be written into a `Constraints` cell today, each graded value SHALL be authored as a named field row (`severity`, `likelihood`, `impact`, `status`, `level`, `trust_level`, `stride_category`, `effectiveness`) whose closed set is carried by the emitted enum schema of [FR-006](./FR-006-security-safe-declarations.md); the item rules of FR-004 enforce the row's presence, and the enum enforces the value the day the extractor populates the typed key.
- Every skeleton `title` SHALL be an `Identifier` (`^[A-Za-z_][A-Za-z0-9_]*$`), distinct across all skeletons and outside the `KernelScalar` names, so a `Type` cell can name it.
- Every `Type` cell that names another skeleton SHALL use that skeleton's `title`, so that under a bundle index built from the skeletons every non-kernel token resolves to `ix://agent-ix/spec-objects-security/type/<Title>` with no `semantic.unresolved-type` finding.
- Every skeleton SHALL keep every H2 heading whose manifest locator is `required: true` for its type, and every frontmatter key those locators assert.
- No skeleton SHALL carry material that is or resembles a live credential.
- Every secret, key, token, and claim skeleton SHALL reference its material by locator only.
- Each negative fixture SHALL fail with a diagnostic whose code equals the fixture's `expect:` value, covering at least: an asset without an identity row (`semantic.record-invalid`), an audit event without a `Timestamp` row (`semantic.record-invalid`), an audit event with an identity row (`semantic.record-invalid`), a threat without a `stride_category` row (`semantic.record-invalid`), a control without an `effectiveness` row (`semantic.record-invalid`), a policy whose `## Invariants` declares no clause (`semantic.record-invalid`), a secret attempting to embed material through a `default:` constraint cell (`semantic.unknown-constraint-keyword`), a `## Properties` section carrying both a table and a fence (`semantic.properties-both-forms`), an operation whose `Post:` names an undeclared clause (`semantic.dangling-clause-ref`), and a `Type` token that is not an `Identifier` (`semantic.invalid-type-token`); the last three re-check the engine's published diagnostics under this module's schemas rather than re-specify them.
- The repository SHALL provide a `make dev-quire` target that installs the Quire wheel this requirement names into the module's Python environment, so the semantic test dependency is provisioned by a documented command rather than by an undeclared side install.
- If the installed Quire wheel is absent or lacks `extract_semantic`, then every semantic test SHALL fail — not skip — with a message naming the missing function, the `make dev-quire` target, and `agent-ix/quire-rs#392`, so that no matrix row can pass or be reported green without the engine under test.
- While no committable index carries Quire 0.46.0, the module SHALL NOT declare `quire` in `pyproject.toml`. `internal-pypi` (the index this repo's CI uses) serves 0.33.0 at most and no `quire-rs` tag carries the semantic layer, so the wheel exists only on the dev-only `pypi.ix`; `agent-ix/quire-rs#392` is the blocking issue, and its resolution replaces the `make dev-quire` target with a committed dev dependency. This is the disposition of `agent-ix/spec-objects-security#10`, which asked for exactly this and named the wrong blame in its skip message.
- Only a criterion this specification names as blocked SHALL be exempt from the previous rule, as an explicit expected failure naming the blocking issue.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-005-CON-1 | The module SHALL keep the skeletons and negatives in this repository only, editing no corpus repository and no vendored quoin/quire fixture. | Boundary | Inspection |
| FR-005-CON-2 | A skeleton SHALL carry one Properties form; the alternate form is a separate file, never a second block in the same artifact. | Integrity | Test |
| FR-005-CON-3 | No skeleton or fixture SHALL contain a credential-shaped literal; a secret is named by its locator only. | Security | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-005-AC-1 | Every skeleton file (twenty-three types plus three alternates) passes `validate_document` against this module with `is_valid` true and no `semantic.record-invalid` error. | Test |
| FR-005-AC-2 | For `asset`, `secret`, and `threat`, the table and `sysml` skeletons extract to identical normalized `fields` with `fieldsForm` `table` and `fence` respectively. | Test |
| FR-005-AC-3 | Under a bundle index built from the skeleton frontmatter, every skeleton extracts with zero `error` diagnostics and zero `semantic.unresolved-type` findings, and every non-kernel `type.target` starts with `ix://agent-ix/spec-objects-security/type/`. | Test |
| FR-005-AC-4 | Each skeleton's `availability` states match its type: `fields` `available` for the eighteen field-bearing types, `clauses` `available` for the six clause-bearing types, `operations` `available` for `auth_flow`; `not_applicable` for every other kind. | Test |
| FR-005-AC-5 | Every negative fixture produces a diagnostic carrying its `expect:` code, and at least the ten cases listed in Behavior are present. | Test |
| FR-005-AC-6 | Every skeleton's H2 set equals a subset of the headings the manifest asserts for its type and includes every `required: true` heading. | Test |
| FR-005-AC-7 | The skeleton for each of the twenty-three types has no placeholder token and every asserted section body is non-empty. | Test |
| FR-005-AC-8 | Every skeleton `title` matches the `Identifier` pattern, is unique across the skeletons, and is not a `KernelScalar` name; every skeleton frontmatter carries `object` equal to `type`. | Test |
| FR-005-AC-9 | No skeleton or negative fixture matches a credential-shaped literal (a private-key PEM header, a JWT triple, an `AKIA` or `ghp_`/`sk-` prefixed token, or a `password`/`secret`/`token` assignment to a literal). | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-role-schemas.md), [FR-006](./FR-006-security-safe-declarations.md); quoin FR-071/FR-072 (`ix://agent-ix/quoin/FR-071`, `ix://agent-ix/quoin/FR-072`); quire-rs FR-070/FR-071/FR-072
- **Upstream (unpinned neighbour contract)**: the `semantic.record-invalid` diagnostic this requirement's Outputs and FR-005-AC-1 depend on exists in quire-rs source but in no quire-rs acceptance criterion; `agent-ix/quire-rs#391` is where that record-validation contract, and the code naming it, are being settled.
- **Upstream (provisioning)**: `agent-ix/quire-rs#392` — publish the 0.46.0 wheel to `internal-pypi` so `quire` can become a committed dev dependency.
- **Downstream**: `agent-ix/quire-contract-ir#52` and `agent-ix/filament-core-data#36` consume the skeletons read-only
