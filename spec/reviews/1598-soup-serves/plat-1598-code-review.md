---
id: SR-038
title: "Code review of PR #47 SOUP record serves edge"
type: SpecReview
analysis: code-review
review_set: subset
scope: "agent-ix/spec-objects-security; spec_objects_security/manifest.yaml, tests/fixtures/soup/served.md, tests/test_manifest.py, tests/test_soup_record.py (PR #47, git diff origin/main...HEAD at 6ca3e61)"
---
# SR-038: Code review of PR #47 SOUP record serves edge

## Summary

Ticket: PLAT-1598. Python and manifest data only, no Rust. `make test` gives 241
passed and 9 xfailed. `make schemas-check` reports 51 schemas matching. Both ran at
6ca3e61 with the pinned quire 0.43.0 (engine 0.58.0) from node_modules.

The manifest change is pure data with no engine change. It adds
`soup_record.allowed_links.serves: [FR, NFR, StR]` and the `required_relations`
entry `soup-record-serves-requirement`, which is outgoing and uses check
`soup-serves-no-requirement`. The finding is a warning by default, and
`--severity trace:soup-serves-no-requirement=error` promotes it. A warning is a
sensible default: a freshly promoted record is reported until a person states
what it serves, as FR-008 does. Quoin promotion writes no edge: quoin main
`rust/crates/quoin-cli/src/soup.rs` and `soup/plan.rs` contain neither
`relationships` nor `serves`.

Measured defects:

1. `serves` is not a registered edge type. Every load prints
   `UnknownEdgeType: archetype 'soup_record' allowed_links uses 'serves' which is not in any edge_types registry`.
   This happens on quire 0.43.0 and 0.44.0.
2. TC-153's "another kind" half rewrites nothing, so it never exercises a threat
   target. A mutation that admits `threat` in `to` survives the test.
3. TC-152 passes only because the engine resolves an `ix://` target by bare id. It
   ignores the repository segment.

## Verdict

**FAIL**: two high findings and one medium. All three can be fixed in this PR.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | `serves` is in no `edge_types` registry (iso or this module), so every validate, trace or matrix load emits `UnknownEdgeType: archetype 'soup_record' allowed_links uses 'serves'`. This contradicts FR-012 Behavior ("SHALL introduce no link verb that the engine does not already know") and FR-013 Description ("adds no link verb the engine does not know"). PLAT-1519 item 3 already says this route "needs a new link verb". No test catches it: TC-141 only checks `UnknownEdgeType: archetype 'vulnerability'`. Fix one of two ways. Declare `serves` (with an inverse, for example `served_by`) in this module's `edge_types`, as spec-objects-business does, and amend FR-012/FR-013 to say so. Or reuse a registered verb (`satisfies`, `supports`, `traces_to`). Either way, add an assertion that loading the module emits no `UnknownEdgeType: archetype 'soup_record'` | spec_objects_security/manifest.yaml:627-628, spec/functional/FR-012-soup-record-relations.md:41, spec/functional/FR-013-soup-record-serves-requirement.md:33, tests/test_soup_record.py:420 |
| FND-002 | high | TC-153's replace string `"example-product/FR-100\n    type: serves"` never matches, because the fixture line is `.../FR-100"` with a closing quote. The "document of another kind" half therefore validates the unmodified served.md, which has an unresolved FR-100, and asserts the "resolves to nothing" case twice. Measured: with `to` and `allowed_links.serves` mutated to admit `threat`, the test-as-written bundle still yields 1 finding, and a correct replacement yields 0. FR-013-AC-4's other-kind branch is unverified. Fix: include the quote in the pattern, and assert the rewritten text differs from the fixture (or build the relationship explicitly) | tests/test_soup_record.py:608-620, tests/fixtures/soup/served.md:18-20 |
| FND-003 | medium | TC-152 (FR-013-AC-3, "a `serves` relationship to an `FR` in the bundle") uses served.md, whose target is `ix://agent-ix/example-product/FR-100`, a different repository. It passes only because the engine matches the bare id `FR-100` against the bundle's FR-100. Measured: `ix://agent-ix/other-repo/FR-100` plus a local FR-100 yields no finding. The test does not state the in-bundle case it claims. It also relies on an engine hole: a record serving another repository's requirement is satisfied by any same-id local document. Fix: point the AC-3 fixture at `ix://agent-ix/spec-objects-security/FR-100`, and route the bare-id resolution to the engine owner | tests/test_soup_record.py:599-605, tests/fixtures/soup/served.md:19 |
