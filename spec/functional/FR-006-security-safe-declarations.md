---
id: FR-006
title: "Refuse embedded material, and state every security grade explicitly"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "depends_on"
---
# FR-006: Refuse embedded material, and state every security grade explicitly

## Description

The shipped schemas SHALL encode three security rules the module is otherwise
only prose about: a declaration of secret material SHALL reference the
material and never carry it, every graded security value SHALL come from a
closed vocabulary carrying an explicit unassessed member, and no schema SHALL
supply a default that grants permission, trust, or control effectiveness, so
that an omitted grade reads as a refusal rather than as an implicit grant.

## Inputs

- The models of [FR-004](./FR-004-role-schemas.md).
- semantic-core `DefaultDecl` and `FieldDecl.default`, the representation of a
  literal value attached to a declared field.

## Outputs

- Ten closed enum schemas under `spec_objects_security/schemas/`.
- A `DefaultedField.json` marker schema, used as the negative `contains`
  predicate of the sensitive types.

## Behavior

- The module SHALL emit these closed vocabularies, each with exactly the members listed and no others:

| Vocabulary | Members | Unassessed member |
|---|---|---|
| `Severity` | `none`, `low`, `medium`, `high`, `critical`, `unknown` | `unknown` |
| `Likelihood` | `rare`, `unlikely`, `possible`, `likely`, `almost_certain`, `unknown` | `unknown` |
| `Impact` | `negligible`, `minor`, `moderate`, `major`, `severe`, `unknown` | `unknown` |
| `StrideCategory` | `spoofing`, `tampering`, `repudiation`, `information_disclosure`, `denial_of_service`, `elevation_of_privilege`, `unknown` | `unknown` |
| `ControlEffectiveness` | `not_assessed`, `ineffective`, `partially_effective`, `effective` | `not_assessed` |
| `FindingStatus` | `open`, `in_remediation`, `remediated`, `risk_accepted`, `false_positive`, `unknown` | `unknown` |
| `ConfidentialityLevel` | `public`, `internal`, `confidential`, `restricted`, `unknown` | `unknown` |
| `TrustLevel` | `untrusted`, `semi_trusted`, `trusted`, `unknown` | `unknown` |
| `SecretLifecycle` | `proposed`, `active`, `rotating`, `revoked`, `compromised`, `unknown` | `unknown` |
| `MfaFactorKind` | `knowledge`, `possession`, `inherence`, `unknown` | `unknown` |

- A value outside a vocabulary's member list SHALL fail validation, so an unrecognised security state fails closed rather than being stored as data.
- No vocabulary SHALL admit an open string.
- Each vocabulary SHALL make its unassessed member the least-granting state it can express — `not_assessed` for effectiveness, `untrusted` for trust — so naming the unassessed state can never widen an allowance.
- No emitted schema of this module SHALL carry a JSON Schema `default` keyword anywhere, so no consumer can read a permission, a trust level, or a control effectiveness that the author did not write.
- The sensitive types `secret`, `encryption_key`, `jwt_claim`, and `csrf_token`, and the `mfa_method` and `auth_flow` types, SHALL admit 0 defaulted fields: a `FieldDecl` carrying `default` is refused, so a declaration cannot carry the material it is about.
- `audit_event` SHALL likewise admit 0 defaulted fields, because an audit declaration that carries a literal payload value is carrying the record rather than declaring it.
- Each sensitive type SHALL admit an optional `material_ref` (`secret`, `encryption_key`), `issuer` (`jwt_claim`) or `binds` (`csrf_token`) `SemanticId` naming where the material or its binding lives.
- No sensitive type SHALL admit a key whose value is the material itself.
- The pinned Quire wheel's typed-table reader refuses a `default:` constraint cell with `semantic.unknown-constraint-keyword`, so the Markdown path reaches the same outcome earlier and a skeleton cannot express an embedded value at all. The schema rule is the second gate, for records that reach a consumer without passing the Markdown reader (a generated-language fixture, a frontend, a hand-built record), and is verified against hand-built records; the test says so rather than claiming extraction evidence.
- The module SHALL rewrite or remove a fixture that cannot satisfy a rule of this requirement.
- The module SHALL NOT relax a rule of this requirement to make a fixture pass.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-006-CON-1 | No vocabulary SHALL gain a member that expresses "assume the permissive value"; the unassessed member is always the least-granting one. | Security | Inspection |
| FR-006-CON-2 | The TypeSpec source SHALL express the `default`-refusal rule as a schema item rule, never as a lint or a convention. | Security | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-006-AC-1 | Each of the ten emitted vocabularies has exactly the members listed, as a closed `enum`, and admits no other value. | Test |
| FR-006-AC-2 | For each vocabulary, a record carrying its unassessed member validates and a record carrying an invented member fails. | Test |
| FR-006-AC-3 | No shipped schema of this module carries a JSON Schema `default` keyword at any depth. | Test |
| FR-006-AC-4 | A `secret`, `encryption_key`, `jwt_claim`, `csrf_token`, `mfa_method`, `auth_flow`, or `audit_event` record carrying a field with a `default` fails its schema; the same record without it validates. | Test |
| FR-006-AC-5 | A skeleton whose `Constraints` cell carries `default: <value>` is refused by the extractor with `semantic.unknown-constraint-keyword`, so the Markdown path cannot express embedded material. | Test |
| FR-006-AC-6 | `ControlEffectiveness` has no member above `not_assessed` that a schema can supply implicitly, and `TrustLevel`'s unassessed member is `untrusted`. | Test |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md)
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md)
