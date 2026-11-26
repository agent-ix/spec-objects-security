# Corporate governance authoring with security artifacts

The `policy`, `control`, `risk`, and `audit_finding` types in this module are
security artifacts. Use them for corporate governance records only when those
records make security claims.

The current link vocabulary supports this chain: a policy `governs` a security
`role` or `control`; a control `implements` a policy and `mitigates` a risk; a
risk `arises_from` a threat or vulnerability; and an audit finding `traces_to`
a risk. Quire validates each edge against the target types declared by the
module. For example, a policy cannot `govern` an audit finding.

The types do not currently link directly to Governance's organizational units,
teams, principals, role assignments, or Process's `RoleSpec`. The module's
`role` means a security permission set, not an organizational role. A corpus
can include those modules, but installing them does not add cross-module links
to these four types.

Quire CLI 0.53.1 `extract --module` loads one module root. It emits these
authored edges, but reports `UnknownEdgeType` or `UnknownRole` for the links
whose vocabulary comes from other modules. Use bundle validation with the full
module set to check those links; this single-root extraction limitation is an
engine gap.

The field contracts also limit reuse:

- `policy` itself has no security-only field, but its module description and
  sample policy concern access and behavior, and `governs` targets only
  security controls, roles, permissions, and data classifications.
- `control` is explicitly a mechanism that reduces exposure. Its
  `safeguards` vocabulary, `mitigates` targets, and `protects` targets are
  security or safety specific. `implements: policy` is the reusable relation.
- `risk` requires security-style likelihood and impact assessments. Its
  causal links name threats and vulnerabilities; its `decision` and
  `decided_by` fields record treatment, not a general enterprise risk process.
- `audit_finding` requires a recommendation and status. Its `traces_to` link
  names a risk, and `references` is limited to controls, vulnerabilities, and
  assets.

Do not use these types for a non-security corporate policy, control, risk, or
finding by treating their security fields as generic. The smallest extension
that preserves these meanings is a separately specified governance-owned set
of domain-neutral policy, control, risk, and finding types, with links to
organizational units and processes. Adding those meanings or links to this
module requires a specification change first.

All identifiers and statements in the accompanying acceptance example are
synthetic. The invalid-target fixture under `tests/fixtures/corporate-governance/`
replaces the example policy when checking that the edge validator rejects a
policy `governs` link to a threat.
