---
id: NFR-001
title: "Additive compatibility of the semantic contract"
type: NFR
quality_attribute: compatibility
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-003"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-security/FR-005"
    type: "constrains"
---
# NFR-001: Additive compatibility of the semantic contract

## Statement

The module SHALL keep every artifact of the checked-in 0.1.0 skeleton set —
the twenty-three skeletons as they stood at manifest version 0.1.0, which is
the population this NFR measures — validating against version 0.2.0 with at
most warning-level semantic findings.

The module SHALL keep every 0.1.0 `body_extraction` locator definition
unchanged at 0.2.0, and SHALL keep the `traceability` block, the `lexicon`, and
every `allowed_links` and `roles` map equal to the frozen 0.1.0 baseline under
`tests/fixtures/baseline-0.1.0/`. Equality is asserted over the parsed
structures, which is what a consumer reads; byte-for-byte identity of the file
is neither asserted nor needed, since the generator rewrites `digest:` lines in
the same file. Yields of the 0.1.0 locators other than the sections this change
adds are unmeasured and are not claimed.

## Scope

- Applies to: `manifest.yaml`, the shipped schemas, and the skeletons.
- Deliberately **not** measured: corpus artifacts outside this repository. At
  0.1.0 every type carried `data_schema: {type: object}`, so a corpus artifact
  declaring `object: threat` was validated against nothing; at 0.2.0 it is
  validated against a sealed schema and can newly fail
  `semantic.record-invalid` at error severity, which `legacy_forms: warning`
  does not soften. That population is real and is the reason the change is
  advisory until corpus promotion (`agent-ix/quoin#291`); this module measures
  only what it ships, and says so rather than implying a guarantee it never
  tested.
- Operational context: existing corpus artifacts authored in legacy
  Properties forms under `legacy_forms: warning`; no corpus repository is
  edited.

## Rationale

The ticket's merge gate is advisory-only until corpus promotion. A module that
turned legacy artifacts into errors would force corpus edits this campaign
forbids; a module that changed a locator would change every existing
extraction record; a module that changed an edge verb would break a sibling
repository's coverage checks silently.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| 0.1.0 locators changed | 0 | 0 | Test |
| `traceability`, `lexicon`, `allowed_links`, `roles` entries changed | 0 | 0 | Test |
| Checked-in 0.1.0 skeleton set under 0.2.0: error findings, per skeleton | 0 | 0 | Test |
| Each 0.1.0 skeleton under 0.2.0: `semantic.record-invalid` findings | 0 | 0 | Test |

## Verification

NFR-001-AC-3 holds on the population this NFR measures, and the measurement
says why: no 0.1.0 skeleton carries a frontmatter `object:` key, so Quire runs
headings-only validation on it and never assembles or checks a typed record.
That is what makes 0.2.0 additive for the artifacts that exist today, and it
is asserted rather than assumed.

The engine defect behind it is real but differently scoped: once a legacy-form
artifact *does* declare `object:`, quire 0.46.0 assembles its declaration
record as `{}` and validates it against the type schema unconditionally, so it
fails `semantic.record-invalid` at error severity even under
`legacy_forms: warning`. `agent-ix/quire-rs#391` owns that rule. The module
carries that case as an explicit expected failure beside NFR-001-AC-4 rather
than relaxing a schema, so the day the engine changes, the row turns red and
is noticed.

A checked-in copy of the 0.1.0 `body_extraction`, `traceability` and
`allowed_links` blocks, and of all twenty-three 0.1.0 skeletons, is compared
against the 0.2.0 manifest and validated under it.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-001-AC-1 | Every 0.1.0 `body_extraction` locator is present in 0.2.0 with identical facets (0 changed). | Test |
| NFR-001-AC-2 | The `traceability` block, the `lexicon`, and every object type's `allowed_links` and `roles` are equal to the frozen 0.1.0 baseline (0 changed). | Test |
| NFR-001-AC-3 | Every skeleton of the checked-in 0.1.0 set validates under 0.2.0 with 0 error findings. | Test |
| NFR-001-AC-4 | No skeleton of the checked-in 0.1.0 set yields a `semantic.record-invalid` finding under 0.2.0. | Test |

## Dependencies

- **Upstream**: [FR-003](../functional/FR-003-semantic-manifest-contract.md), [FR-005](../functional/FR-005-executable-skeletons.md); quoin FR-074 (`ix://agent-ix/quoin/FR-074`)
- **Downstream**: corpus promotion (`agent-ix/quoin#291` sweep), outside this module; `agent-ix/spec-objects-safety` hazard coverage, unaffected by design
