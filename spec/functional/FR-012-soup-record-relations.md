---
id: FR-012
title: "A SOUP record relates to vulnerability, asset and requirements, and leaves the advisory join open"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-009"
    type: "depends_on"
---
# FR-012: A SOUP record relates to vulnerability, asset and requirements, and leaves the advisory join open

## Description

The module already declares `vulnerability` and `asset`. A `soup_record` reuses them instead of
copying their content. It states which vulnerabilities a reviewer has linked to the component, and
nothing more: matching advisories to components is a separate capability and is not specified here.

## Inputs

- The `soup_record`, `vulnerability` and `asset` entries of the module manifest.

## Outputs

- `soup_record.allowed_links` in the module manifest.

## Behavior

- The manifest SHALL declare `soup_record.allowed_links.affected_by` equal to `[vulnerability]`.
- The manifest SHALL declare `soup_record.allowed_links.part_of` equal to `[asset]`.
- The manifest SHALL declare `soup_record.allowed_links.references` equal to `[soup_record]`.
- A `soup_record` SHALL NOT carry advisory text, an advisory identifier list, or a severity; those belong to the `vulnerability` it links to.
- Quire SHALL report a `soup_record` edge whose target type is outside the declared list as `disallowed-edge-target`, naming the target's type.
- The module SHALL NOT populate `affected_by` from an advisory feed or match.
- An `affected_by` edge SHALL exist only when an author wrote it.
- The module SHALL leave `vulnerability.affects` unchanged, so a `vulnerability` still names `asset` and `attack_surface` targets only.
- The module SHALL NOT declare a required relation that obliges a `soup_record` to have an `affected_by` edge, because a component with no linked vulnerability is a valid state.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-012-AC-1 | The loaded `soup_record` type lists exactly `affected_by: [vulnerability]`, `part_of: [asset]` and `references: [soup_record]` under `allowed_links`. | Test |
| FR-012-AC-2 | A fixture `soup_record` with an `affected_by` edge to a fixture `threat` is reported `disallowed-edge-target`, and the diagnostic names the type `threat`. | Test |
| FR-012-AC-3 | A fixture `soup_record` with an `affected_by` edge to a fixture `vulnerability`, and a fixture with no such edge, both validate with no finding. | Test |
| FR-012-AC-4 | The `soup_record` schema declares no `severity`, `cve_id` or advisory-list key. | Test |
| FR-012-AC-5 | The loaded `vulnerability` type still lists exactly `asset` and `attack_surface` under `allowed_links.affects`, and the manifest's required relations are unchanged apart from any added for other requirements. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-009](./FR-009-soup-record-identity-and-promotion.md)
- **Downstream**: none; the advisory join is a later requirement of the owning project.
