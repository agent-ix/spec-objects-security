---
id: SR-044
title: "Gap analysis of PR #49 control clause references and scope exclusions"
type: SpecReview
analysis: gap-analysis
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-014..FR-018, spec/non-functional/NFR-003-clause-references-state-and-never-derive.md, spec/functional/FR-004-role-schemas.md (PR #49, git diff origin/main...HEAD at d3658e0)"
---
# SR-044: Gap analysis of PR #49 control clause references and scope exclusions

## Summary

Ticket: PLAT-1426. Plan completion: not assessed (planless). This PR changes
only the spec; it changes no source or test file.

`quoin matrix --repo . --json` (quoin 0.30.1) lists all 24 new criteria as
`untagged` with no run evidence. That is 5 for FR-014, 5 for FR-015, 3 for
FR-016, 5 for FR-017, 4 for FR-018 and 2 for NFR-003. This is expected for a
spec-first ticket. The implementation is PLAT-1427, whose Repo(s) names
spec-objects-security as well as quoin. The shipped code diverges from FR-014
as expected. `typespec/main.tsp:150-153` and `schemas/ControlMapping.json`
still declare `framework`, `control_id` and `doc`. The control skeleton's
`## Mappings` is still prose bullets. No `scope_exclusion` model, schema or
skeleton exists yet. None of this is a defect of this PR; PLAT-1427 is
blocked by PLAT-1426 for exactly this work.

No code exists that has no owning requirement, because the PR adds no code.
The engine-side owner gap for the FR-015 and FR-018 diagnostics is recorded in
SR-041 FND-003 and FND-004. PLAT-1427's implementation scope is quoin plus this
module, and it names no quire-rs work.

## Verdict

**PASS** for a spec-only PR: no stubs, no coverage inflation, and no
mis-tagged tests. The untagged criteria are the planned implementation backlog.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |
