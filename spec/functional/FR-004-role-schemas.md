---
id: FR-004
title: "Give every security object type a role-distinct declaration schema"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/filament-core-data/FR-031"
    type: "depends_on"
---
# FR-004: Give every security object type a role-distinct declaration schema

## Description

The TypeSpec source SHALL declare one model per security object type whose
emitted schema validates that type's declaration record
`{ fields?, relations?, clauses?, operations?, … }` with type-specific
required keys, forbidden keys, and item rules, so that no type is a
placeholder and each security role refuses the records that violate its own
rules.

## Inputs

- semantic-core 0.1.0 grammar models: `FieldDecl`, `RelationDecl`,
  `OperationDecl`, `ClauseRef`, `EnumValue`, `DefaultDecl`, `Identifier`,
  `SemanticId`, `KernelScalar`.
- The declaration record Quire assembles per artifact: `fields` from
  `## Properties`, `clauses` from `## Invariants`, `operations` from
  `## Operations` (quire-rs FR-070/FR-071), with any key absent when its
  section is absent.

## Outputs

- Twenty-three object-type models, each emitted as `schemas/<Model>.json`,
  sealed (`unevaluatedProperties: {not: {}}`).
- Support models emitted as sibling files: the open marker models
  `IdentityField`, `DefaultedField`, `OccurrenceField`, `OccurrenceTypeRef`,
  `StrideCategoryField`, `SeverityField`, `LikelihoodField`, `ImpactField`,
  `StatusField`, `LevelField`, `TrustLevelField`, `EffectivenessField`; the
  records `ControlMapping` and `FlowStep`; and the closed graded vocabularies
  `Severity`, `Likelihood`, `Impact`, `StrideCategory`, `ControlEffectiveness`,
  `FindingStatus`, `ConfidentialityLevel`, `TrustLevel`, `SecretLifecycle`,
  `MfaFactorKind`.

## Behavior

Each model SHALL enforce its row of the following table. "Identity field"
means a `FieldDecl` with `identity: true`; "occurrence field" a `FieldDecl`
whose `type.target` is `Timestamp`; "defaulted field" a `FieldDecl` carrying a
`default`; "a `<name>` field" a `FieldDecl` whose `name` is that literal.
These readings are semantic-core 0.1.0 reader conventions (the identity flag
is set only by a bare `identity` keyword in a Constraints cell and is absent,
not `false`, otherwise; the kernel scalar is the bare token `Timestamp`), so a
semantic-core release that renders `identity: false` or namespaces kernel
scalars is a breaking change to these schemas, and this module SHALL answer it
with a manifest version bump rather than by widening a rule.

| Object type | Model | Required keys | Optional keys | Item rules |
|---|---|---|---|---|
| asset | `Asset` | `fields` | `relations`, `clauses`, `operations`, `classification: ConfidentialityLevel`, `owner: SemanticId` | `fields` has ≥ 1 item and ≥ 1 identity field |
| role | `Role` | `fields` | `relations`, `clauses`, `grants: SemanticId[]` | `fields` has ≥ 1 item and ≥ 1 identity field; `operations` forbidden — a role is a grant set, not behaviour |
| permission | `Permission` | `fields` | `clauses`, `resource: SemanticId`, `verb: Identifier` | `fields` has ≥ 1 item and ≥ 1 identity field; `operations` and `relations` forbidden |
| scope | `Scope` | `fields` | `clauses`, `includes: SemanticId[]` | `fields` has ≥ 1 item and ≥ 1 identity field; `operations` and `relations` forbidden |
| mfa_method | `MfaMethod` | `fields` | `clauses`, `operations`, `factor_kind: MfaFactorKind` | `fields` has ≥ 1 item, ≥ 1 identity field, and 0 defaulted fields |
| threat | `Threat` | `fields` | `clauses`, `relations`, `stride_category: StrideCategory`, `exploits: SemanticId[]` | `fields` has ≥ 1 item, ≥ 1 identity field, and ≥ 1 `stride_category` field; `operations` forbidden |
| vulnerability | `Vulnerability` | `fields` | `clauses`, `relations`, `severity: Severity`, `cve_id: string`, `affects: SemanticId[]` | `fields` has ≥ 1 item, ≥ 1 identity field, and ≥ 1 `severity` field; `operations` forbidden |
| risk | `Risk` | `fields` | `clauses`, `relations`, `likelihood: Likelihood`, `impact: Impact`, `arises_from: SemanticId[]` | `fields` has ≥ 1 item, ≥ 1 identity field, ≥ 1 `likelihood` field and ≥ 1 `impact` field; `operations` forbidden |
| audit_finding | `AuditFinding` | `fields` | `clauses`, `relations`, `status: FindingStatus`, `traces_to: SemanticId[]` | `fields` has ≥ 1 item, ≥ 1 identity field, and ≥ 1 `status` field; `operations` forbidden |
| data_classification | `DataClassification` | `fields` | `clauses`, `level: ConfidentialityLevel`, `values: EnumValue[]` | `fields` has ≥ 1 item, ≥ 1 identity field, and ≥ 1 `level` field; `operations` and `relations` forbidden |
| attack_surface | `AttackSurface` | `fields` | `clauses`, `relations`, `exposes: SemanticId[]` | `fields` has ≥ 1 item and ≥ 1 identity field; `operations` forbidden |
| trust_boundary | `TrustBoundary` | `fields`, `clauses` | `relations`, `trust_level: TrustLevel`, `crosses: SemanticId[]` | `fields` has ≥ 1 item, ≥ 1 identity field and ≥ 1 `trust_level` field; `clauses` has ≥ 1 item — a boundary that admits every crossing is not a boundary; `operations` forbidden |
| secret | `Secret` | `fields` | `clauses`, `operations`, `lifecycle: SecretLifecycle`, `material_ref: SemanticId`, `custodian: SemanticId`, `classification: ConfidentialityLevel` | `fields` has ≥ 1 item, ≥ 1 identity field, and 0 defaulted fields; `relations` forbidden |
| encryption_key | `EncryptionKey` | `fields` | `clauses`, `operations`, `lifecycle: SecretLifecycle`, `material_ref: SemanticId`, `custodian: SemanticId`, `algorithm: Identifier` | `fields` has ≥ 1 item, ≥ 1 identity field, and 0 defaulted fields; `relations` forbidden |
| jwt_claim | `JwtClaim` | `fields` | `clauses`, `classification: ConfidentialityLevel`, `issuer: SemanticId` | `fields` has ≥ 1 item, ≥ 1 identity field, and 0 defaulted fields; `operations` and `relations` forbidden |
| csrf_token | `CsrfToken` | `fields` | `clauses`, `binds: SemanticId` | `fields` has ≥ 1 item, ≥ 1 identity field, and 0 defaulted fields; `operations` and `relations` forbidden |
| policy | `Policy` | `clauses` | `fields`, `relations`, `governs: SemanticId[]` | `clauses` has ≥ 1 item — a policy that constrains nothing is prose; `operations` forbidden |
| control | `Control` | `clauses`, `fields` | `operations`, `effectiveness: ControlEffectiveness`, `mitigates: SemanticId[]`, `mappings: ControlMapping[]` | `clauses` has ≥ 1 item; `fields` has ≥ 1 item and ≥ 1 `effectiveness` field, so effectiveness is always stated and never inferred; `relations` forbidden |
| password_policy | `PasswordPolicy` | `clauses` | `fields` | `clauses` has ≥ 1 item; `operations` and `relations` forbidden |
| cors_policy | `CorsPolicy` | `clauses` | `fields`, `allowed_origins: string[]` | `clauses` has ≥ 1 item; `operations` and `relations` forbidden |
| session_config | `SessionConfig` | `clauses` | `fields`, `binds_flow: SemanticId` | `clauses` has ≥ 1 item; `operations` and `relations` forbidden |
| auth_flow | `AuthFlow` | `operations` | `fields`, `clauses`, `steps: FlowStep[]` | `operations` has ≥ 1 item — a flow is its exchanges; `fields` has 0 defaulted fields; `relations` forbidden |
| audit_event | `AuditEvent` | `fields` | `clauses`, `source: SemanticId` | `fields` has ≥ 1 item, 0 identity fields, ≥ 1 occurrence field, and 0 defaulted fields; `operations` and `relations` forbidden |

- `ControlMapping` SHALL be `{ framework: string (minLength 1), control_id: string (minLength 1), doc?: string }`.
- `FlowStep` SHALL be `{ name: Identifier, actor: Identifier, doc?: string }`.
- Each graded vocabulary SHALL be a closed enum whose members are exactly those listed in [FR-006](./FR-006-security-safe-declarations.md), including its explicit unassessed member.
- Every `fields`, `params`, `clauses`, `operations`, and `relations` item SHALL be validated by `$ref` to the semantic-core 0.1.0 model, never by a copied definition.
- Where a row above says "0 defaulted fields" and the type also admits `operations`, that row SHALL be read as covering `operations[].params[]` as well, because a parameter is a `FieldDecl` too. It applies to `secret`, `encryption_key`, `mfa_method` and `auth_flow`; `jwt_claim`, `csrf_token` and `audit_event` forbid `operations` outright, so nothing is left uncovered.
- The TypeSpec source SHALL express every positive item rule through the official emitter's `@contains` decorator over an open marker model: `@contains(IdentityField)` for "≥ 1 identity field", `@contains(OccurrenceField)` for "≥ 1 occurrence field".
- The TypeSpec source SHALL express every negative item rule ("0 identity fields", "0 defaulted fields") as `items: { not: { $ref: <marker> } }` rather than as a counting predicate, for the reason [FR-006](./FR-006-security-safe-declarations.md) gives: a counting predicate inverts under a validator that does not implement `minContains`/`maxContains`, and `items`/`not` cannot.
- Because JSON Schema admits one `contains` per array, the TypeSpec source SHALL carry every predicate beyond the first on that array as an `@extension("allOf", …)` clause referencing the marker file (`DefaultedField.json`, `OccurrenceField.json`, `IdentityField.json`, `SeverityField.json`, and the rest); the generator normalizes those relative `$ref`s per FR-002.
- Every cross-reference a declaration makes (`type.target`, `RelationDecl.target`, `owner`, `resource`, `grants`, `includes`, `exploits`, `affects`, `arises_from`, `traces_to`, `exposes`, `crosses`, `material_ref`, `custodian`, `issuer`, `binds`, `binds_flow`, `governs`, `mitigates`, `source`) SHALL be a `SemanticId` or `KernelScalar` per semantic-core, so a bare token is rejected by the schema; resolution against the bundle, and the placeholder `ix://<org>/<repo>/unresolved/<Token>` with its `semantic.unresolved-type` finding, exist today for `type.target` only (quire-rs FR-070). No published mapping covers the other keys: `agent-ix/quoin#335` is the ticket that would own one, and its body scopes itself to the ten `spec-objects-business` keys and names none of these, so this module records the gap rather than assuming that ticket will close it.
- Each schema SHALL describe the declared shape only, never a runtime occurrence (a session, an emitted audit record, a scanner hit), which is why `AuditEvent` carries no identity field: occurrence identity belongs to the runtime record, not the declaration.
- Where a key is declared but the current extractor does not populate it (`relations`, `classification`, `owner`, `grants`, `includes`, `resource`, `verb`, `factor_kind`, `stride_category`, `severity`, `cve_id`, `likelihood`, `impact`, `status`, `level`, `values`, `trust_level`, `crosses`, `exposes`, `lifecycle`, `material_ref`, `custodian`, `algorithm`, `issuer`, `binds`, `binds_flow`, `governs`, `mitigates`, `mappings`, `effectiveness`, `steps`, `source`, `affects`, `arises_from`, `traces_to`, `exploits`, `allowed_origins`) the key SHALL be optional, so a record produced by today's extractor validates and a future extractor can fill it without a schema change.
- Eight of the optional graded keys SHALL additionally be expressed as an item rule over `fields`, which the extractor does populate — `stride_category`, `severity`, `likelihood`, `impact`, `status`, `level`, `trust_level` and `effectiveness`, one open marker model each — so a threat states its STRIDE class as a row and a control its effectiveness as a row, and the obligation is enforced today rather than deferred.
- The remaining graded keys (`lifecycle`, `classification`, `factor_kind`) SHALL carry no item rule: they record how something is held rather than how bad it is, and no refusal in this module turns on them. They are declared, typed, and optional; nothing else is claimed for them.
- The test suite SHALL verify every criterion over a key the extractor does not populate against a hand-built JSON record rather than an extracted one, naming that limitation in the test itself, so that no row claims extraction evidence it does not have.
- No model SHALL admit a key on a type whose row does not list it; the seal is the mechanism.
- A record carrying a key its type's row does not list SHALL fail validation.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-004-CON-1 | No model SHALL redeclare a semantic-core model or scalar; the module namespace contributes archetype shapes only (semantic-core NFR-014 kernel discipline). | Architecture | Test |
| FR-004-CON-2 | The empty record `{}` SHALL fail every one of the twenty-three types, because every type has a non-empty required set. | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-004-AC-1 | Each of the twenty-three shipped object-type schemas differs from every other in at least one required key, admitted key, or item rule listed in the table; a schema with only `type: object` is absent. | Test |
| FR-004-AC-2 | An asset record with one identity field validates against `Asset.json`; the same record with the identity flag removed fails; a record with no `fields` fails. | Test |
| FR-004-AC-3 | A role record validates; a record carrying `operations` fails. A permission and a scope record each fail when they carry `relations`. | Test |
| FR-004-AC-4 | A threat record with a `stride_category` field validates; the same record without that field fails; a `stride_category` outside `StrideCategory` fails. | Test |
| FR-004-AC-5 | A vulnerability record with a `severity` field validates and one without it fails; a risk record needs both a `likelihood` and an `impact` field, and fails when either is absent; an audit-finding record without a `status` field fails. | Test |
| FR-004-AC-6 | A control record with one clause and an `effectiveness` field validates; the same record without `clauses` fails, and without the `effectiveness` field fails. | Test |
| FR-004-AC-7 | A policy, password-policy, cors-policy and session-config record each validate with one clause and each fail with an empty `clauses` array or with `operations` present. | Test |
| FR-004-AC-8 | An auth-flow record with one operation validates; an empty `operations` array fails; a record carrying `relations` fails. | Test |
| FR-004-AC-9 | An audit-event record with a `Timestamp` field and no identity field validates against `AuditEvent.json`; a record whose only fields are non-`Timestamp` fails; a record with an identity field fails; a record with `operations` fails. | Test |
| FR-004-AC-10 | A trust-boundary record with one clause and a `trust_level` field validates; the same record without `clauses` fails; a `trust_level` outside `TrustLevel` fails. | Test |
| FR-004-AC-11 | The empty record `{}` fails against all twenty-three schemas. | Test |
| FR-004-AC-12 | A `type.target` of `ix://agent-ix/spec-objects-security/unresolved/Mystery` is accepted by the schema (it is a `SemanticId`) and reported by the extractor as `semantic.unresolved-type`; a bare `Mystery` string is rejected by the schema. | Test |
| FR-004-AC-13 | No module schema redeclares a semantic-core model; every grammar item is a `$ref` to semantic-core 0.1.0. | Test |
| FR-004-AC-14 | A data-classification record with a `level` field validates; one without it fails; a record carrying `relations` fails. | Test |

## Dependencies

- **Upstream**: semantic-core FR-031 (`ix://agent-ix/filament-core-data/FR-031`)
- **Build**: [FR-002](./FR-002-emitted-json-schemas.md) emits these models
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md), [FR-006](./FR-006-security-safe-declarations.md); `agent-ix/quire-contract-ir#52` and `agent-ix/filament-core-data#36` read these schemas as fixtures
