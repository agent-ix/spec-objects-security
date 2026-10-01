---
id: FR-002
title: "Emit the module's JSON Schemas from a TypeSpec package importing semantic-core"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/filament-core-data/FR-033"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: "depends_on"
---
# FR-002: Emit the module's JSON Schemas from a TypeSpec package importing semantic-core

## Description

The module build SHALL emit one JSON Schema 2020-12 document per security
object type from a TypeSpec source that imports `@agent-ix/semantic-core`,
using the official `@typespec/json-schema` emitter at a pinned
toolchain, into `spec_objects_security/schemas/`, so that the shipped schema
is the compiled one and any drift between source and shipped bytes fails the
build.

## Inputs

- `typespec/main.tsp`: namespace `AgentIx.SpecObjects.Security`, decorated
  `@jsonSchema("https://schemas.agent-ix.org/agent-ix/spec-objects-security/")`.
- `@agent-ix/semantic-core` from GitHub Packages (`FieldDecl`, `TypeRef`,
  `Multiplicity`, `ConstraintDecl`, `DefaultDecl`, `RelationDecl`,
  `OperationDecl`, `ClauseRef`, `EnumValue`, `KernelScalar`, `Identifier`,
  `SemanticId`).
- `@typespec/compiler`, `@typespec/json-schema` and `@agent-ix/semantic-core`
  as `devDependencies` in `package.json`: all three are build inputs of the
  emission step, and the published artifact is Markdown and JSON, so none is a
  runtime dependency of a consumer.
- `scripts/generate-schemas.mjs` (the generator) and `scripts/stage-npm.mjs`
  (the npm staging script), both Node built-ins only.

## Outputs

- `spec_objects_security/schemas/<Model>.json`, one per model of the module
  namespace, rendered as two-space JSON with a trailing newline.

## Behavior

- `make schemas` SHALL run `node scripts/generate-schemas.mjs`.
- The generator SHALL compile `typespec/` with `tsp compile`, keep only the emitted files whose `$id` starts with the module base, and discard the re-emitted semantic-core files.
- If the emitter leaves any `$id` or `$ref` relative, then the generator SHALL rewrite it to `<base><file>` (module models) or `https://schemas.agent-ix.org/semantic-core/0.3.0/<file>` (semantic-core models).
- If `tsp compile` fails or emits no module model, then the generator SHALL exit non-zero without touching the committed output.
- If `node` is older than 20 or `tsp` is not resolvable, then the generator SHALL exit non-zero naming the required Node version or the missing binary.
- In `--check` mode the generator SHALL write no file, neither under `spec_objects_security/schemas/` nor in `manifest.yaml`.
- Every emitted schema SHALL declare `$schema: https://json-schema.org/draft/2020-12/schema` and `$id: https://schemas.agent-ix.org/agent-ix/spec-objects-security/<Model>.json`.
- Every `$ref` in an emitted schema SHALL name either a sibling `https://schemas.agent-ix.org/agent-ix/spec-objects-security/<File>.json` that ships in `schemas/`, or `https://schemas.agent-ix.org/semantic-core/0.3.0/<Model>.json`.
- `make schemas-check` SHALL run the generator with `--check`.
- `make lint` SHALL run `make schemas-check`, so a `typespec/` edit that was never regenerated fails before push rather than at review.
- If any emitted file differs from the committed output, a committed file under `spec_objects_security/schemas/` is stale (it has no emitted counterpart in this run), then the check SHALL exit non-zero naming each such file.
- If nothing differs, then the check SHALL exit zero.
- The generator SHALL write files under `spec_objects_security/schemas/` only.
- The Python package SHALL include `spec_objects_security/schemas/*.json` in the wheel and sdist.
- The repository SHALL mark `*.json`, `*.tsp`, `*.yaml` and `*.md` as `eol=lf` in `.gitattributes`.
- `scripts/stage-npm.mjs` SHALL copy `schemas/` beside `manifest.yaml` at pack time, so the npm tarball ships the schemas the manifest references.
- `scripts/stage-npm.mjs` SHALL remove the staged copies again on `postpack`.
- When `GITHUB_REF_NAME` names a `vX.Y.Z` tag, `scripts/stage-npm.mjs` SHALL stamp that version into `package.json` so the npm tarball is published at the tag version.
- When `GITHUB_REF_NAME` is absent or does not name such a tag, `scripts/stage-npm.mjs` SHALL leave `package.json` untouched.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-002-CON-1 | The build SHALL use the official `@typespec/json-schema` emitter only; no custom emitter and no hand-edited emitted file. | Architecture | Inspection |
| FR-002-CON-2 | The repository SHALL carry no `.npmrc`, no `file:` or `link:` dependency, and no upper version bound on the TypeSpec toolchain. | Packaging | Inspection |
| FR-002-CON-3 | Emission SHALL be deterministic: two runs over one source produce byte-identical files. | Integrity | Test |
| FR-002-CON-4 | `package-lock.json` SHALL resolve every public package from `registry.npmjs.org`; `@agent-ix/semantic-core` resolves from `npm.pkg.github.com`, the real GitHub Packages registry it publishes to (`agent-ix/filament-core-data#11`) and the one CI actually authenticates against, so `make schemas`/`make schemas-check` run identically in the GitHub workflow and on a machine authenticated to GitHub Packages. | Packaging | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-002-AC-2 | Every shipped schema declares the 2020-12 `$schema` and the `$id` `https://schemas.agent-ix.org/agent-ix/spec-objects-security/<Model>.json` matching its file name. | Test |
| FR-002-AC-3 | Every `$ref` across the shipped schemas resolves to a shipped sibling or to semantic-core; a `$ref` to any other host is absent. | Test |
| FR-002-AC-4 | `make schemas-check` on the committed tree exits zero; after one byte of any shipped schema is changed, it exits non-zero naming that file. | Test |
| FR-002-AC-6 | The wheel built by `make build` contains every emitted schema, not only the exported models: a schema whose `$ref` names a sibling that did not ship is unresolvable at the consumer. | Test |
| FR-002-AC-7 | The npm tarball produced by `npm pack` contains `manifest.yaml` and a sibling `schemas/<File>` for every emitted schema, so a manifest-relative `schema:` path and every `$ref` it reaches resolve inside the tarball. | Test |
| FR-002-AC-9 | `make schemas-check` on a committed tree carrying an extra `spec_objects_security/schemas/Stale.json` with no emitted counterpart exits non-zero naming that file, and writes nothing. | Test |
| FR-002-AC-11 | `.gitattributes` marks `*.json`, `*.tsp`, `*.yaml` and `*.md` `eol=lf`, and `npm pack` leaves no staged `manifest.yaml`, `schemas/` or `skeletons/` at the repository root. | Test |

## Dependencies

- **Upstream**: [US-001](../usecase/US-001-declare-security-objects-against-semantic-core.md); semantic-core FR-033 (`ix://agent-ix/filament-core-data/FR-033`); the generation pattern of `agent-ix/spec-objects-business` `scripts/generate-schemas.mjs`
- **Upstream (models)**: [FR-004](./FR-004-role-schemas.md) declares the models this build emits
- **Downstream**: [FR-003](./FR-003-semantic-manifest-contract.md)
