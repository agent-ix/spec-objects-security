---
id: FR-003
title: "Declare the semantic-module contract in the manifest"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-070"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-073"
    type: "depends_on"
---
# FR-003: Declare the semantic-module contract in the manifest

## Description

`spec_objects_security/manifest.yaml` SHALL carry the quoin FR-070 `semantic`
block and reference every exported object type's emitted schema by path
(quoin FR-073), so that Quoin verifies the
shipped schemas at install and Quire validates every declaration record
against them, while every existing extraction locator, edge vocabulary, and
traceability rule keeps its meaning.

## Inputs

- The emitted schemas of [FR-002](./FR-002-emitted-json-schemas.md).
- The module-manifest schema with the `semantic` block, owned by
  `filament-core-data`. The Quire engine embeds it, and the engines apply it
  when they read this manifest, each over a different part. Measured:
  `quire validate --module` refuses an unknown top-level key but accepts bad
  `semantic.*` content, while `quoin module install` refuses bad `semantic.*`
  content (QM020) but accepts an unknown top-level key. Together they cover
  what the schema closes; neither is the whole schema, and they are not one byte
  set. This repository commits no copy of the schema; the gate is the real
  engines applying it (FR-003-AC-7).

## Outputs

- `manifest.yaml` with a `version`, a `semantic` block, and reference-form
  `data_schema` on every exported object type.

## Behavior

- The manifest `semantic` block SHALL carry exactly these keys and values: `contract_version: 1.0.0`, `package: agent-ix/spec-objects-security`, `exports` listing every object type that ships a schema, `imports: {}`, `targets: [json-schema, markdown]`, `mappings: [typed-table, sysml-fence, ocl-clause, record-sections]`, `compatibility_posture: additive`, `legacy_forms: warning`.
- `semantic.exports` SHALL name all twenty-five object types: `auth_flow`, `permission`, `scope`, `role`, `secret`, `encryption_key`, `session_config`, `data_classification`, `trust_boundary`, `audit_event`, `csrf_token`, `cors_policy`, `password_policy`, `mfa_method`, `jwt_claim`, `threat`, `control`, `risk`, `vulnerability`, `asset`, `attack_surface`, `policy`, `audit_finding`, `soup_record`, `scope_exclusion`.
- Every exported object type's `data_schema` SHALL be `{ schema: schemas/<Model>.json }`.
- No exported object type SHALL carry an inline `data_schema`.
- The manifest SHALL carry the `traceability` block (`required_relations`, `acyclic_edges`) and every object type's `allowed_links` and `roles`. `control.allowed_links.mitigates` is `[threat, risk, vulnerability, hazard, failure_mode]` ([FR-007](./FR-007-control-mitigates-safety-objects.md)); the other target lists are as authored in the manifest.
- The `data_schema` reference form and the `semantic` block SHALL be judged by the consumer that reads them today: Quire's registry loader accepts the block and drops the module's object types when it is mutated (FR-003-AC-4, FR-003-AC-6). `quoin module install` is run in a temporary HOME by FR-003-AC-7; the AC-5 Demonstration additionally lists the module and restores the prior entry. The manifest is accepted by the engines applying the authoritative schema (FR-003-AC-7); activation (FR-001-AC-2) needs a running service.
- The manifest SHALL load through Quire's registry loader with no `ArchetypeLoadFailure` for any object type.
- A refused schema drops that object type alone, while a manifest key the loader cannot parse (an unknown `semantic` key) drops every object type of the module, so a consumer sees the module as absent. Both refusals are silent — no diagnostic names the offending key or path — which `agent-ix/quire-rs#221` and `agent-ix/quire-rs#394` record as engine defects; the naming half of FR-003-AC-6 is blocked on them and is verified as an explicit expected failure rather than dropped.
- The manifest SHALL install through `quoin module install path:<module dir>` with no `semantic.*` error diagnostic.
- When the install has completed, `quoin module` SHALL list `spec-objects-security`.
- If Quoin or Quire rejects the manifest, then this module SHALL correct its own manifest or schemas rather than relax the contract keys or the `$id` rules to make a consumer accept them.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-003-CON-1 | The `semantic` block SHALL contain no key outside the admitted list. Quire's loader refusal of an unknown key is verified here (FR-003-AC-6); Quoin's refusal of an unknown `semantic` key is verified by FR-003-AC-7 (`quoin module install` names `semantic.foo`). | Compatibility | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-003-AC-1 | The loaded `semantic` block equals the eight admitted keys with the values above, and `exports` equals the twenty-five object-type names. | Test |
| FR-003-AC-4 | `quire.Registry.load_from([module dir])` lists all twenty-five archetypes and `validate_document` on each skeleton reports no `semantic.*` load failure. | Test |
| FR-003-AC-5 | `quoin module install path:<module dir>` exits zero and `quoin module` lists `spec-objects-security`; the previously installed entry is restored afterwards. | Demonstration |
| FR-003-AC-6 | A manifest copy whose `semantic` block gains a key `foo` is refused by Quire's loader. The refusal is verified; the half that requires the diagnostic to *name* `foo` or the path is an explicit expected failure while `agent-ix/quire-rs#221` and `agent-ix/quire-rs#394` are open. | Test |
| FR-003-AC-7 | `quire validate --module <module dir>` and `quoin module install path:<module dir>` (with `HOME` pointed at a temporary directory, so the real install and registry are untouched) both accept the shipped manifest; a copy with an unknown top-level key is refused by `quire validate` naming `bogus_key`, and a copy with an unknown `semantic` key is refused by `quoin module install` naming `semantic.foo`. No copy of the schema is held here. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md), [FR-002](./FR-002-emitted-json-schemas.md); quoin FR-070/FR-073 (`ix://agent-ix/quoin/FR-070`, `ix://agent-ix/quoin/FR-073`); quire-rs FR-069 (`ix://agent-ix/quire-rs/FR-069`)
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md), [IT-002](../integration/IT-002-quoin-module-install.md)
