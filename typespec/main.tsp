import "@typespec/json-schema";
import "@agent-ix/semantic-core";

using TypeSpec.JsonSchema;
using AgentIx.Semantic.Core;

/**
 * Tier-2 security object declaration schemas (agent-ix/spec-objects-security#13).
 *
 * One model per security object type this module contributes, each validating
 * that type's Quire declaration record (fields, relations, clauses,
 * operations; quire-rs FR-070..FR-072) with type-specific required keys,
 * forbidden keys, and item rules (FR-004). Every grammar item is a `$ref` to
 * `@agent-ix/semantic-core` 0.1.0 and is never redeclared here
 * (FR-004-CON-1); this namespace contributes archetype shapes only.
 *
 * Three security rules are encoded rather than described (FR-006): a
 * declaration of secret material carries no `default`, every graded value
 * comes from a closed vocabulary whose unassessed member is its least-granting
 * state, and no schema anywhere supplies a `default` keyword — so an omitted
 * grade reads as a refusal, never as an implicit grant.
 *
 * The `$id` base embeds the manifest `version` by intent (FR-002-CON-5): one
 * schema URL names exactly one immutable byte sequence, so a downstream
 * fixture reader that pinned a version can never silently read later bytes. A
 * bump edits this base and `manifest.yaml`'s `version` in one commit and
 * re-runs `make schemas`.
 */
@jsonSchema("https://schemas.agent-ix.org/agent-ix/spec-objects-security/0.2.0/")
namespace AgentIx.SpecObjects.Security;

// ---------------------------------------------------------------------------
// Closed graded vocabularies (FR-006)
//
// Each carries an explicit unassessed member, and that member is the
// least-granting state the vocabulary can express: naming it can never widen
// an allowance, and a value outside the set fails closed.
// ---------------------------------------------------------------------------

/** How bad a vulnerability is. `unknown` states that it was not assessed. */
enum Severity {
  none,
  low,
  medium,
  high,
  critical,
  `unknown`,
}

/** How likely a risk is to be realized. `unknown` states that it was not assessed. */
enum Likelihood {
  rare,
  unlikely,
  possible,
  likely,
  almost_certain,
  `unknown`,
}

/** What a realized risk costs. `unknown` states that it was not assessed. */
enum Impact {
  negligible,
  minor,
  moderate,
  major,
  severe,
  `unknown`,
}

/** The STRIDE class of a threat. `unknown` states that it was not classified. */
enum StrideCategory {
  spoofing,
  tampering,
  repudiation,
  information_disclosure,
  denial_of_service,
  elevation_of_privilege,
  `unknown`,
}

/**
 * How well a control works. `not_assessed` is both the unassessed member and
 * the least-granting one: no schema may supply any other value implicitly.
 */
enum ControlEffectiveness {
  not_assessed,
  ineffective,
  partially_effective,
  effective,
}

/** Where an audit finding stands. `unknown` states that it was not triaged. */
enum FindingStatus {
  open,
  in_remediation,
  remediated,
  risk_accepted,
  false_positive,
  `unknown`,
}

/** How sensitive data is. `unknown` states that it was not classified. */
enum ConfidentialityLevel {
  public,
  internal,
  confidential,
  restricted,
  `unknown`,
}

/**
 * How far a zone is trusted. `untrusted` is the unassessed member, because the
 * least-granting reading of "we never decided" is "we do not trust it".
 */
enum TrustLevel {
  untrusted,
  semi_trusted,
  trusted,
  `unknown`,
}

/** Where secret material is in its life. `unknown` states that it was not tracked. */
enum SecretLifecycle {
  proposed,
  active,
  rotating,
  revoked,
  compromised,
  `unknown`,
}

/** Which authentication factor an MFA method is. `unknown` states that it was not classified. */
enum MfaFactorKind {
  knowledge,
  possession,
  inherence,
  `unknown`,
}

// ---------------------------------------------------------------------------
// Support records
// ---------------------------------------------------------------------------

/** One external framework a control maps to. */
model ControlMapping {
  @minLength(1) framework: string;
  @minLength(1) control_id: string;
  doc?: string;
  ...Record<never>;
}

/** One exchange of an authentication flow, as a human-facing summary. */
model FlowStep {
  name: Identifier;
  actor: Identifier;
  doc?: string;
  ...Record<never>;
}

// ---------------------------------------------------------------------------
// Open marker models
//
// Each is a `@contains` predicate only, and is deliberately open so it matches
// any FieldDecl with the named shape.
// ---------------------------------------------------------------------------

/** A `FieldDecl` flagged as identity. */
model IdentityField {
  identity: true;
}

/**
 * A `FieldDecl` carrying a literal default. Used only as a negative predicate:
 * a declaration of secret material never carries the material (FR-006).
 */
model DefaultedField {
  `default`: DefaultDecl;
}

/** A `TypeRef` whose target is the kernel `Timestamp` scalar. */
model OccurrenceTypeRef {
  target: KernelScalar.Timestamp;
}

/** A `FieldDecl` whose type targets `Timestamp` — the occurrence time an audit event declaration must carry. */
model OccurrenceField {
  type: OccurrenceTypeRef;
}

/** A `FieldDecl` named `stride_category`. */
model StrideCategoryField {
  name: "stride_category";
}

/** A `FieldDecl` named `severity`. */
model SeverityField {
  name: "severity";
}

/** A `FieldDecl` named `likelihood`. */
model LikelihoodField {
  name: "likelihood";
}

/** A `FieldDecl` named `impact`. */
model ImpactField {
  name: "impact";
}

/** A `FieldDecl` named `status`. */
model StatusField {
  name: "status";
}

/** A `FieldDecl` named `level`. */
model LevelField {
  name: "level";
}

/** A `FieldDecl` named `trust_level`. */
model TrustLevelField {
  name: "trust_level";
}

/** A `FieldDecl` named `effectiveness`. */
model EffectivenessField {
  name: "effectiveness";
}

// ---------------------------------------------------------------------------
// Catalogued identities
// ---------------------------------------------------------------------------

/** A thing worth protecting. */
model Asset {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  operations?: OperationDecl[];
  classification?: ConfidentialityLevel;
  owner?: SemanticId;
  ...Record<never>;
}

/** A named bundle of grants. `operations` is forbidden by the seal: a role is a grant set, not behaviour. */
model Role {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  grants?: SemanticId[];
  ...Record<never>;
}

/** One allowed action on one resource. `operations` and `relations` are forbidden by the seal. */
model Permission {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  resource?: SemanticId;
  verb?: Identifier;
  ...Record<never>;
}

/** A named permission boundary on a grant. `operations` and `relations` are forbidden by the seal. */
model Scope {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  includes?: SemanticId[];
  ...Record<never>;
}

/** An authentication factor a principal can present. Carries no defaulted field. */
@extension(
  "allOf",
  #[
    #{ properties: #{ fields: #{ items: #{ not: #{ `$ref`: "DefaultedField.json" } } } } },
    #{
      properties: #{
        operations: #{
          items: #{ properties: #{ params: #{ items: #{ not: #{ `$ref`: "DefaultedField.json" } } } } },
        },
      },
    }
  ]
)
model MfaMethod {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  operations?: OperationDecl[];
  factor_kind?: MfaFactorKind;
  ...Record<never>;
}

// ---------------------------------------------------------------------------
// Assessments
// ---------------------------------------------------------------------------

/** An adversary capability against this system. `operations` is forbidden by the seal. */
@extension(
  "allOf",
  #[#{ properties: #{ fields: #{ contains: #{ `$ref`: "StrideCategoryField.json" } } } }]
)
model Threat {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  relations?: RelationDecl[];
  stride_category?: StrideCategory;
  exploits?: SemanticId[];
  ...Record<never>;
}

/** A weakness an implementation carries. `operations` is forbidden by the seal. */
@extension(
  "allOf",
  #[#{ properties: #{ fields: #{ contains: #{ `$ref`: "SeverityField.json" } } } }]
)
model Vulnerability {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  relations?: RelationDecl[];
  severity?: Severity;
  cve_id?: string;
  affects?: SemanticId[];
  ...Record<never>;
}

/** A scored exposure. Both axes are stated as rows, never inferred. */
@extension(
  "allOf",
  #[
    #{ properties: #{ fields: #{ contains: #{ `$ref`: "LikelihoodField.json" } } } },
    #{ properties: #{ fields: #{ contains: #{ `$ref`: "ImpactField.json" } } } }
  ]
)
model Risk {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  relations?: RelationDecl[];
  likelihood?: Likelihood;
  impact?: Impact;
  arises_from?: SemanticId[];
  ...Record<never>;
}

/** One audit observation. `operations` is forbidden by the seal. */
@extension(
  "allOf",
  #[#{ properties: #{ fields: #{ contains: #{ `$ref`: "StatusField.json" } } } }]
)
model AuditFinding {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  relations?: RelationDecl[];
  status?: FindingStatus;
  traces_to?: SemanticId[];
  ...Record<never>;
}

/** A handling class for data. `operations` and `relations` are forbidden by the seal. */
@extension(
  "allOf",
  #[#{ properties: #{ fields: #{ contains: #{ `$ref`: "LevelField.json" } } } }]
)
model DataClassification {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  level?: ConfidentialityLevel;
  values?: EnumValue[];
  ...Record<never>;
}

/** The reachable surface an attacker can address. `operations` is forbidden by the seal. */
model AttackSurface {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  relations?: RelationDecl[];
  exposes?: SemanticId[];
  ...Record<never>;
}

/**
 * A zone edge. `clauses` is required: a boundary that admits every crossing is
 * not a boundary. `operations` is forbidden by the seal.
 */
@extension(
  "allOf",
  #[#{ properties: #{ fields: #{ contains: #{ `$ref`: "TrustLevelField.json" } } } }]
)
model TrustBoundary {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  @minItems(1)
  clauses: ClauseRef[];

  relations?: RelationDecl[];
  trust_level?: TrustLevel;
  crosses?: SemanticId[];
  ...Record<never>;
}

// ---------------------------------------------------------------------------
// Sensitive material references
//
// Each admits 0 defaulted fields: the declaration names where the material
// lives and never carries it (FR-006). `relations` is forbidden by the seal.
// ---------------------------------------------------------------------------

/** A confidential value kept out of code. */
@extension(
  "allOf",
  #[
    #{ properties: #{ fields: #{ items: #{ not: #{ `$ref`: "DefaultedField.json" } } } } },
    #{
      properties: #{
        operations: #{
          items: #{ properties: #{ params: #{ items: #{ not: #{ `$ref`: "DefaultedField.json" } } } } },
        },
      },
    }
  ]
)
model Secret {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  operations?: OperationDecl[];
  lifecycle?: SecretLifecycle;
  material_ref?: SemanticId;
  custodian?: SemanticId;
  classification?: ConfidentialityLevel;
  ...Record<never>;
}

/** A cryptographic key. */
@extension(
  "allOf",
  #[
    #{ properties: #{ fields: #{ items: #{ not: #{ `$ref`: "DefaultedField.json" } } } } },
    #{
      properties: #{
        operations: #{
          items: #{ properties: #{ params: #{ items: #{ not: #{ `$ref`: "DefaultedField.json" } } } } },
        },
      },
    }
  ]
)
model EncryptionKey {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  operations?: OperationDecl[];
  lifecycle?: SecretLifecycle;
  material_ref?: SemanticId;
  custodian?: SemanticId;
  algorithm?: Identifier;
  ...Record<never>;
}

/** One assertion carried in a token. `operations` is forbidden by the seal. */
@extension(
  "allOf",
  #[
    #{ properties: #{ fields: #{ items: #{ not: #{ `$ref`: "DefaultedField.json" } } } } }
  ]
)
model JwtClaim {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  classification?: ConfidentialityLevel;
  issuer?: SemanticId;
  ...Record<never>;
}

/** A single-use anti-forgery token. `operations` is forbidden by the seal. */
@extension(
  "allOf",
  #[
    #{ properties: #{ fields: #{ items: #{ not: #{ `$ref`: "DefaultedField.json" } } } } }
  ]
)
model CsrfToken {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  binds?: SemanticId;
  ...Record<never>;
}

// ---------------------------------------------------------------------------
// Governing rules
//
// Each requires at least one clause: a rule that constrains nothing is prose.
// ---------------------------------------------------------------------------

/** A declarative rule governing access or behaviour. `operations` is forbidden by the seal. */
model Policy {
  @minItems(1)
  clauses: ClauseRef[];

  fields?: FieldDecl[];
  relations?: RelationDecl[];
  governs?: SemanticId[];
  ...Record<never>;
}

/**
 * A mechanism that reduces an exposure. Effectiveness is always stated as a
 * row and never inferred. `relations` is forbidden by the seal.
 */
model Control {
  @minItems(1)
  clauses: ClauseRef[];

  @minItems(1)
  @contains(EffectivenessField)
  fields: FieldDecl[];

  operations?: OperationDecl[];
  effectiveness?: ControlEffectiveness;
  mitigates?: SemanticId[];
  mappings?: ControlMapping[];
  ...Record<never>;
}

/** The rules a password must satisfy. `operations` and `relations` are forbidden by the seal. */
model PasswordPolicy {
  @minItems(1)
  clauses: ClauseRef[];

  fields?: FieldDecl[];
  ...Record<never>;
}

/** The cross-origin rules a surface enforces. `operations` and `relations` are forbidden by the seal. */
model CorsPolicy {
  @minItems(1)
  clauses: ClauseRef[];

  fields?: FieldDecl[];
  allowed_origins?: string[];
  ...Record<never>;
}

/** The rules a session obeys. `operations` and `relations` are forbidden by the seal. */
model SessionConfig {
  @minItems(1)
  clauses: ClauseRef[];

  fields?: FieldDecl[];
  binds_flow?: SemanticId;
  ...Record<never>;
}

// ---------------------------------------------------------------------------
// Behaviour and occurrence declarations
// ---------------------------------------------------------------------------

/**
 * An authentication or authorization exchange. A flow is its exchanges, so
 * `operations` is required. `relations` is forbidden by the seal, and no field
 * carries a default: a flow never embeds a credential.
 */
@extension(
  "allOf",
  #[
    #{ properties: #{ fields: #{ items: #{ not: #{ `$ref`: "DefaultedField.json" } } } } },
    #{
      properties: #{
        operations: #{
          items: #{ properties: #{ params: #{ items: #{ not: #{ `$ref`: "DefaultedField.json" } } } } },
        },
      },
    }
  ]
)
model AuthFlow {
  @minItems(1)
  operations: OperationDecl[];

  fields?: FieldDecl[];
  clauses?: ClauseRef[];
  steps?: FlowStep[];
  ...Record<never>;
}

/**
 * An auditable event declaration.
 *
 * The declared shape carries no identity field: occurrence identity belongs to
 * the runtime record, not the declaration. It must carry at least one
 * occurrence field (a `Timestamp`), and no field carries a default — an audit
 * declaration that pins a literal payload value is carrying the record rather
 * than declaring it. `operations` and `relations` are forbidden by the seal.
 */
@extension(
  "allOf",
  #[
    #{ properties: #{ fields: #{ items: #{ not: #{ `$ref`: "IdentityField.json" } } } } },
    #{ properties: #{ fields: #{ items: #{ not: #{ `$ref`: "DefaultedField.json" } } } } }
  ]
)
model AuditEvent {
  @minItems(1)
  @contains(OccurrenceField)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  source?: SemanticId;
  ...Record<never>;
}
