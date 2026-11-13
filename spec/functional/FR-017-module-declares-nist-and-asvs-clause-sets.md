---
id: FR-017
title: "The module declares the NIST SP 800-53 and OWASP ASVS clause sets with truthful rights metadata"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-014"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-083"
    type: "depends_on"
---
# FR-017: The module declares the NIST SP 800-53 and OWASP ASVS clause sets with truthful rights metadata

## Description

Controls map to clauses ([FR-014](./FR-014-control-mappings-are-clause-references.md)), so the clause sets of the two free
standards the security analysis maps have a home. That home is this module. It declares the sets in its manifest
`clause_sets` list (`agent-ix/quire-rs` FR-083), each with rights metadata that states its source licence. Authoring the
clause content is PLAT-1521 (NIST SP 800-53) and PLAT-1522 (OWASP ASVS 5.0); this requirement fixes the keys, the home and
the rights rule they follow. `agent-ix/quoin` FR-172 states the same decision from the skill's side.

## Behavior

- The manifest `clause_sets` list SHALL name two sets, keyed `nist/sp800-53@5.2.0` and `owasp/asvs@5.0.0`.
- Each set's rights metadata SHALL state the licence of its source.
- Each set's `rights.text` SHALL be `none`, `original` or `explicitly_cleared`.
- No set's `rights.text` SHALL be `licensed`.
- The module SHALL carry no clause text beyond what its source licence allows.
- `quire publish-check` over the module SHALL exit 0.
- The module SHALL declare no clause set for a licence-restricted standard.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-017-AC-1 | The loaded manifest's `clause_sets` names exactly `nist/sp800-53@5.2.0` and `owasp/asvs@5.0.0`. | Test |
| FR-017-AC-2 | Each of the two sets declares rights metadata naming its source licence and a `rights.text` of `none`, `original` or `explicitly_cleared`. | Test |
| FR-017-AC-3 | `quire publish-check --module <this module>` exits 0. | Test |
| FR-017-AC-4 | A fixture manifest declaring a set with `rights.text: licensed` makes `quire publish-check` exit non-zero. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-014](./FR-014-control-mappings-are-clause-references.md); `agent-ix/quire-rs` FR-083
- **Downstream**: `agent-ix/quoin` FR-172; PLAT-1521 and PLAT-1522 author the clause content
