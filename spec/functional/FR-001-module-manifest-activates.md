---
id: FR-001
title: "Module manifest activates against filament-core"
type: FR
---
# FR-001: Module manifest activates against filament-core

## Description

The system **SHALL** publish a Filament Module manifest (`spec_objects_security/manifest.yaml`) that conforms to the module-manifest schema owned by `filament-core-data` and activates idempotently against `POST /api/v1/modules/activate`.


## Inputs

- `manifest.yaml` (this repo's package)
- Activation endpoint: `POST /api/v1/modules/activate`

## Outputs

- Module row in `modules` table
- Contributed archetypes, object_types, grammars, artifact_types per the manifest

## Behavior

The manifest **SHALL** conform to the module-manifest schema owned by `filament-core-data`; this module holds no copy of it. Conformance is judged by the engines that apply that schema when they load a module (FR-003-AC-7) and by activation at `POST /api/v1/modules/activate` (FR-001-AC-2), which needs a running filament-core and is `🚧` in this repository's matrix. Re-activation **SHALL** be a no-op (idempotent by content hash per FR-026-AC-1).

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-001-AC-1 | The module is well-formed against its own declarations: the packaged manifest resolves and parses, every `object_type` declares a name and a `data_schema`, no two share a name, every lexicon entry carries a whole definition, threat and risk coverage is declared as module data, every `object_type` ships a skeleton whose frontmatter matches its declared locators and which carries every asserted section, no skeleton drifts beyond what its manifest entry asserts, every skeleton supplies substantive body content rather than placeholder text, and a filled skeleton round-trips through `validate_document` while a mutated one fails. | Test |
| FR-001-AC-2 | Activation against clean filament-core succeeds with 200 | Test |
| FR-001-AC-3 | Re-activation returns no-op (same content hash) | Test |
| FR-001-AC-4 | Each declared archetype/object_type/artifact_type appears in the corresponding filament-core table after activation | Test |

## Dependencies

- **Upstream**: `filament-core-data` (module-manifest schema), filament-core-service FR-026, FR-034
- **Downstream**: consumer agents/editors discovering this module's contributions
