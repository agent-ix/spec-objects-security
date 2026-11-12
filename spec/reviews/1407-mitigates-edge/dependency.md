---
id: SR-015
title: "Dependency review of FR-007 control mitigates hazard and failure_mode"
type: SpecReview
analysis: dependency
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-007-control-mitigates-safety-objects.md (PR #39 diff)"
---
# SR-015: Dependency review of FR-007 control mitigates hazard and failure_mode

## Summary

Ticket: PLAT-1407. Checked FR-007's new `relationships` edges (implements
US-001, depends_on FR-006) and its Dependencies line (FR-006; safety FR-007,
FR-008) against what the requirement needs.

Measured with quire 0.40.0 (engine 0.56.0) in the PR worktree: a document whose
frontmatter relationship targets a non-existent id (`FR-999`) passes
`quire validate --scope . <file>` with exit 0 and no diagnostic; `quire
validate --okf` reports it only as `warning: ... dangling reference 'FR-999'
... [dangling-reference]`. The repository declares no dependency on
`spec-objects-safety` in `pyproject.toml`, `package.json`, `Makefile` or `tests/`.

Clean units: the safety FR-007/FR-008 upstream, and its reciprocal on the
safety side (safety FR-007 names security FR-007 upstream), are consistent.

## Verdict

FAIL: FR-007-AC-3 depends on Quire behaviour that no current release provides
and FR-007 names no owner for it.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | high | FR-007-AC-3 (and its Behavior bullet) requires `quire validate` to exit non-zero, naming file path, verb and id, on a `mitigates` target no loaded document declares. Measured: current Quire exits 0 on a dangling relationship target (warning only under `--okf`). Nothing in this module can make that test pass, and FR-007 names no `agent-ix/quire-cli` / `agent-ix/quire-rs` upstream requirement for it. Cite the quire requirement that owns an exit-failing dangling-reference mode, or drop the AC. Safety FR-007-AC-3 has the same gap. | spec/functional/FR-007-control-mitigates-safety-objects.md:40, spec/functional/FR-007-control-mitigates-safety-objects.md:55 |
| FND-002 | medium | Frontmatter `depends_on` FR-006 (refuse embedded material, explicit grades) is not what FR-007 builds on. The upstreams are FR-003 (the manifest `allowed_links` contract FR-007 changes) and FR-004 (the `Control` model with `mitigates`). The Dependencies line repeats FR-006. | spec/functional/FR-007-control-mitigates-safety-objects.md:8-9, spec/functional/FR-007-control-mitigates-safety-objects.md:61 |
| FND-003 | medium | FR-007-AC-2, AC-3 and AC-4 validate "with both modules loaded", but FR-007 does not say where the `spec-objects-safety` module comes from in this repository's tests (installed module root, git dependency, `--module` path), and the repository declares no dependency on it. | spec/functional/FR-007-control-mitigates-safety-objects.md:25-28, spec/functional/FR-007-control-mitigates-safety-objects.md:54 |

## Dispositions

| FND | outcome | reason |
|-----|---------|--------|
| FND-001 | fixed | fixed in c667d46 |
| FND-002 | fixed | fixed in c667d46 |
| FND-003 | fixed | fixed in c667d46 |
