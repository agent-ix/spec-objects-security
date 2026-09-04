---
id: Task-001
title: "FR-002 - TypeSpec toolchain, schema generator and drift gate"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-security/TC-023
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-024
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-028
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-029
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-030
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-031
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-032
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-033
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-034
    type: verifies
  - target: ix://agent-ix/spec-objects-security/TC-035
    type: verifies
---
# Task-001: FR-002 - TypeSpec toolchain, schema generator and drift gate

## Scope

The enablement half of FR-002: everything that turns a TypeSpec source into
shipped schema bytes, and everything that refuses a tree where the two
disagree. The models themselves are Task-002.

## Subtasks

- [x] Pin `@typespec/compiler` 1.15.0, `@typespec/json-schema` 1.15.0 and
      `@agent-ix/semantic-core` 0.1.0 as exact `devDependencies`. No `.npmrc`,
      no `file:`/`link:`, no upper bound; the lockfile resolves every public
      package from npmjs and only `@agent-ix/*` from npm.ix.
- [x] Author the `typespec/main.tsp` shell: namespace
      `AgentIx.SpecObjects.Security`, `@jsonSchema` base carrying the manifest
      version.
- [x] Write `scripts/generate-schemas.mjs` (Node built-ins only): compile, keep
      this namespace, normalize relative `$id`/`$ref`, record every rewrite in
      `toolchain.json`, render two-space JSON with a trailing newline.
- [x] Fail loudly and touch nothing on failure: a compile failure, an empty
      emitted set, Node older than 20, and a `@jsonSchema` base whose version
      differs from the manifest version - naming both values.
- [x] Rewrite `data_schema.digest` textually so the manifest keeps its YAML
      anchors and comments, and write nothing else in it.
- [x] `--check` mode writes no file and names each differing, stale or
      digest-mismatched path.
- [x] Wire `make schemas` / `make schemas-check`; `make lint` runs the gate.
- [x] `.gitattributes` marks `*.json`, `*.tsp`, `*.yaml` and `*.md` `eol=lf`.
- [x] `scripts/stage-npm.mjs` gains the `postpack` clean, so a staged
      `manifest.yaml` cannot make every Filament tool discover the repository
      root as a second module.

## Deliverables

- `typespec/main.tsp` (shell), `typespec/tspconfig.yaml`,
  `scripts/generate-schemas.mjs`, `scripts/stage-npm.mjs`, `.gitattributes`
- `package.json`, `package-lock.json`, `Makefile` and the poe tasks

## Notes

The generator resolves every path from its own location, not from the process
working directory, so a test driving a scratch tree must run that tree's own
copy. Running the repository copy against a scratch working directory silently
checks the repository instead, and every negative case then passes. That trap
is recorded in the test that hit it.
