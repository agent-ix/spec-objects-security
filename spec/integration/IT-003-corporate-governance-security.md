---
id: IT-003
title: "Validate security artifacts alongside corporate governance"
type: IT
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-003"
    type: verifies
---
# IT-003: Validate security artifacts alongside corporate governance

## Objective

Verify that a pinned Security module installs alongside Governance and the
modules that provide its relation vocabulary, and that a synthetic security
governance corpus validates and extracts with released Quire CLI 0.53.1.

## Preconditions

- A clean test `HOME` and Quoin with GitHub module installation support.
- Quire CLI 0.53.1 on `PATH`.
- `SECURITY_REV` is the full Git commit of the Security module under review.
- Use these provider commits to make the module set reproducible:
  - Process: `17da2da1772e03c300c7e577f4e96c06a7a7b745`
  - Architecture: `df01e2430759452fdea23ef95cd7e251976719c3`
  - ISO: `88b2a8e041db3b889bd6ecf7170d8447a0b83a68`
  - Safety: `8e9b1f23f809aeef873e3a5574835718e7f7f39d`
  - Governance: `f9dad0d7580a9232b018d2028b953c8b3d42b411`

## Inputs

- `examples/corporate-governance/`, containing policy, role, control, threat,
  risk, and audit-finding documents with synthetic identifiers and statements.
- `tests/fixtures/corporate-governance/wrong-target/policy.md`, a negative
  policy document to substitute for the valid example policy.

## Test Procedure

1. Install the pinned modules into the clean `HOME`:

   ```sh
   quoin module install github:agent-ix/spec-artifacts-process//spec_artifacts_process@17da2da1772e03c300c7e577f4e96c06a7a7b745
   quoin module install github:agent-ix/spec-objects-architecture//spec_objects_architecture@df01e2430759452fdea23ef95cd7e251976719c3
   quoin module install github:agent-ix/spec-artifacts-iso//spec_artifacts_iso@88b2a8e041db3b889bd6ecf7170d8447a0b83a68
   quoin module install github:agent-ix/spec-objects-safety//spec_objects_safety@8e9b1f23f809aeef873e3a5574835718e7f7f39d
   quoin module install github:agent-ix/spec-objects-governance//spec_objects_governance@f9dad0d7580a9232b018d2028b953c8b3d42b411
   quoin module install github:agent-ix/spec-objects-security//spec_objects_security@$SECURITY_REV
   ```

   - IT-003-SC-01: `quoin module list` contains all six modules.
   - IT-003-SC-02: Quoin accepts the Security manifest without a semantic
     contract error.
2. Run `quire validate --okf` on `examples/corporate-governance/`, with the
   six installed module roots passed through repeatable `--module` options.
   - IT-003-SC-03: the six synthetic documents validate with no finding for a
     Security-authored link.
3. Run `quire extract --module <Security module root>` for `policy.md`,
   `control.md`, `risk.md`, and `audit_finding.md`.
   - IT-003-SC-04: each extraction contains its authored record and edges:
     policy `governs`, control `implements` and `mitigates`, risk `arises_from`,
     and finding `traces_to` and `references`.
4. Replace the example `policy.md` in a copy of the corpus with the negative
   fixture and run `quire validate --okf --strict` against the same six module
   roots.
   - IT-003-SC-05: validation reports `disallowed-edge-target` for a policy
     `governs` edge to a `threat` and exits non-zero.
5. Discard the test `HOME` and corpus copy.
   - IT-003-SC-06: the user's installed modules and repository are unchanged.

## Expected Results

All six modules install from the named Git revisions, the positive corpus
validates and extracts the documented links, and the negative policy target
is refused. `quire extract --module` accepts one root; it still emits the
authored cross-module edges but reports unknown edge or role vocabulary when
used alone. The combined validation in step 2 is the link-target check.

## Dependencies

**Upstream**: [FR-003](../functional/FR-003-semantic-manifest-contract.md).
**Downstream**: none.
