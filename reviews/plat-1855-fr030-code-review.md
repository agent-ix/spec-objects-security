---
id: SR-1627
title: "Code review — FR-030 SOUP-requirements design relation (code step)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-security; spec_objects_security/manifest.yaml, tests/test_soup_requirements.py, tests/test_manifest.py, tests/test_reverse_mitigates.py"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-030
    type: reviews
---
# SR-1627: Code review — FR-030 SOUP-requirements design relation (code step)

## Summary

Ticket: PLAT-1855 (code part); PR agent-ix/spec-objects-security#80 at head `70538ffb3abf22cd28976e0fb40edd8a328828ad`, scoped to `git diff origin/main...HEAD` (4 files: manifest data and Python tests only).

The PR declares `soup_requirement_for` (category `traceability`, inverse `has_soup_requirement`) in the module's own `edge_types`, adds `fr-has-soup-requirements` and `nfr-has-soup-requirements` to `required_relations` with the FR-030 fields and `when_any`, lists both in `traceability.design_relations`, adds `tests/test_soup_requirements.py`, makes `tests/test_manifest.py` a membership check that excludes design relations, and makes `tests/test_reverse_mitigates.py` select its relation by name.

Measured (scratch venv and scratch module copies under the reviewer scratchpad; nothing created in the worktree):

- Relation fields match FR-030 Behavior exactly: names, `from: FR` / `from: NFR`, `edges: [soup_requirement_for]`, `to: [FR, NFR]`, `direction: incoming`, checks `fr-without-soup-requirements` / `nfr-without-soup-requirements`, `when_any: [{verb: references, direction: incoming, other: [soup_record]}]`, no `severity` key (engine default warning), no `where` or score field. `design_relations` is `[fr-has-soup-requirements, nfr-has-soup-requirements]`.
- FR-013's `soup-record-serves-requirement` is unchanged (diff is insert-only around it) and is not in `design_relations`.
- `tests/test_soup_requirements.py` 10/10 pass with iso PR #77 (`5a018fd`) and either architecture `0.14.0` (the `package.json` pin, from `npm pack`) or architecture PR #60 (`beff9a8`). FR-013's tests in `tests/test_soup_record.py` (AC-1..7) pass; the touched `test_manifest.py` and `test_reverse_mitigates.py` pass. The other `test_soup_record.py` errors are the missing quire wheel / semantic-core in the scratch env and are unrelated to the diff.
- Against iso `origin/main` (`9342304`, equivalent to the locked `spec-artifacts-iso` 0.25.0) one test fails: `test_a_statement_or_the_inverse_covers_the_served_fr` at line 183 (`disallowed-edge-type` on the forward verb). See FND-001.
- Mutations of the manifest, each run against the touched test files, all killed: `when_any` removed from either relation (5 and 3 tests fail), verb category changed to `governance`, `design_relations` order swapped (AC-1 and AC-11 tests), FR `to` narrowed to `[FR]`, inverse removed, FR-013's relation added to `design_relations`, `references` added to `edges`, `when_any.other` widened to `threat`.
- Coder's claim verified: directory `quire validate --okf` (and non-okf directory validate) emits no `disallowed-edge-type`; only single-file `quire validate` does. With iso main the inverse `has_soup_requirement` authored by the served FR draws no warning, while the forward verb from an FR or NFR statement does, as FR-030's Dependencies paragraph states.
- Corpus with security and architecture: the design join is `[fr-has-design-element, nfr-has-design-element, fr-has-soup-requirements, nfr-has-soup-requirements]` with architecture 0.14.0, and `[..., fr-has-segregation, nfr-has-segregation, fr-has-soup-requirements, nfr-has-soup-requirements]` with architecture PR #60; with security loaded before architecture its two relations come first. `quire matrix --strict` exits 1 with stderr `design gap: spec/FR-100.md fr-without-soup-requirements`.
- `scripts/generate-schemas.mjs` reads only `typespec/main.tsp` and `package.json`, never the manifest, so manifest-only changes cannot move generated schemas; the `--check` run was correctly skipped and was not run.
- `test_manifest.py`: the exact-set assertions became subset assertions and design relations are excluded from the per-relation loop. Nothing real was lost: every non-design relation still passes the direction / declared-`from` / permitted-verb invariants, and the two design relations' fields and distinct check names are pinned exactly by the FR-030-AC-1 test. No new count or pin assertion was added.
- ruff and black pass on the three test files.

Examined units:

- `FR-030-AC-1` (role: examined): The manifest declares `soup_requirement_for` with inverse `has_soup_requirement` and category `traceability`, the two relations with the fields and `when_any` stated above, and `design_relations` listing exactly those two names in that order; the module loads without a declaration error.
- `FR-030-AC-3` (role: examined): Adding an `FR` that authors `soup_requirement_for` toward the served `FR` makes it `covered` with that `FR` linked and removes the finding; authoring `has_soup_requirement` from the served `FR` toward the statement gives the same result and no `disallowed-edge-type` warning.
- `FR-030-AC-7` (role: examined): The `soup-record-serves-requirement` relation of FR-013 keeps its declaration and is absent from `design_relations`; the `soup_record` type still declares no `allowed_links`.
- `FR-030-AC-11` (role: examined): Over a corpus loading this module and spec-objects-architecture, the join lists the two relations of this module in `design_relations` order after the relations of the modules loaded before it; `quire matrix --strict` exits 1 with a stderr line naming the document and `fr-without-soup-requirements`.
- `FR-013-AC-1` (role: examined): the manifest declares `soup-record-serves-requirement` with its stated fields.
- `FR-030` Dependencies, Cross-repository paragraph (role: context_only): until iso lists the verbs, authoring the verb draws the advisory `disallowed-edge-type`; authoring the inverse from the served requirement avoids it.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The FR-030-AC-3 test also asserts that the forward verb `soup_requirement_for` authored by a statement draws no `disallowed-edge-type`. AC-3 asks that only of the inverse; the forward case is iso FR-004-AC-9, which iso PR #77 tests itself, and FR-030 states the forward verb draws the warning until iso lists it. Against iso main and the locked `spec-artifacts-iso` 0.25.0 the test fails (measured 1 failed, 9 passed), so `make test` is red after merge until iso #77 is merged, released and the lock is bumped. Merge order alone does not fix it. Drop the line-183 assertion, or bump the iso lock in this PR once iso is released. | tests/test_soup_requirements.py:183 |
| FND-002 | low | The FR-030-AC-11 test is weaker than the AC in two ways. (1) "After the relations of earlier modules" is checked only against names ending `-has-design-element`, so with architecture PR #60 a join that put this module's relations between `nfr-has-design-element` and `fr-has-segregation` would still pass. Assert `names[-2:] == [FR_RELATION, NFR_RELATION]`, or take the max over all of `earlier`. (2) The AC asks for a stderr line, but the gap search also reads stdout, which carries `Design gap: no design element (fr-without-soup-requirements)` too. | tests/test_soup_requirements.py:320-332 |

## Verdict

**PASS with one medium and one low finding; mergeable after FND-001 is fixed or the iso lock is bumped.** The manifest data matches FR-030 field for field. FR-013's relation is untouched and stays out of `design_relations`. Every manifest mutation tried was killed by a test. The membership rewrite of `test_manifest.py` loses no real invariant, and selecting the relation by name in `test_reverse_mitigates.py` is the right repair. FND-001 is the only blocker: a test asserts a property owned by another repository, so this repository's own suite goes red against its locked dependency.

Observation for the lead, not a defect of this PR: quire-cli's `quire matrix` stdout labels every design-relation gap "no design element", which reads oddly for a SOUP-requirements gap. That wording belongs to quire-cli.
