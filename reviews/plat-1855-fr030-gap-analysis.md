---
id: SR-1628
title: "Gap analysis — FR-030 acceptance criteria against the code step"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-security; spec/functional/FR-030-soup-requirements-design-relation.md, spec_objects_security/manifest.yaml, tests/test_soup_requirements.py, tests/test_manifest.py, tests/test_reverse_mitigates.py, tests/test_soup_record.py"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-030
    type: reviews
---
# SR-1628: Gap analysis — FR-030 acceptance criteria against the code step

## Summary

Ticket: PLAT-1855 (code part); PR agent-ix/spec-objects-security#80 at head `70538ffb3abf22cd28976e0fb40edd8a328828ad`, scope `git diff origin/main...HEAD`. Planless audit: plan completion was not assessed.

`quire matrix --scope .` at the PR head shows FR-030-AC-1..7 and AC-9..11 `tagged` to `tests/test_soup_requirements.py`, AC-8 `untagged`, and CON-1..3 `method-without-symbol`. The CONs are Inspection constraints, and inspection of the diff satisfies them: it adds only `edge_types` and `traceability` data, adds no object type and no Python production code, writes or infers no edge, and every finding is the engine's relation finding naming its check. No production code is left without an owning requirement. The diff has no stubs.

Each tagged test was run with iso PR #77 and architecture 0.14.0 or PR #60 (10/10 pass). A manifest mutation was run against each criterion's manifest clause (see SR-1627): every mutation fails at least one test, including removal of `when_any`, a change of the verb category and a swap of the `design_relations` order. FR-013-AC-1..7 still pass.

Per-AC trace (all bindings correct):

- AC-1: exact dict equality for both relations, the verb's `inverse` and `category`, an exact `design_relations` list, and an engine load beside iso and architecture.
- AC-2: `uncovered` row with nothing linked, and exactly one `--okf` finding naming FR-100 at exit 0.
- AC-3: forward statement and inverse each `covered`, linked to FR-200, with no finding; no `disallowed-edge-type` on the inverse, with a `blocks` control. The extra forward assertion is SR-1627 FND-001.
- AC-4: no row or finding for an unserved FR or NFR, with a served-FR control.
- AC-5: `references`, `satisfies` and a `threat` source stay `uncovered`; an NFR statement covers a served FR.
- AC-6: `warning:` prefix, `=error` exits non-zero, `=off` drops the finding.
- AC-7: exact FR-013 declaration, not in `design_relations`, no `allowed_links`.
- AC-9: an NFR row is `uncovered` with one finding, `=error` and `=off` work, and FR and NFR statements cover it.
- AC-10: a body link puts the FR in scope and a statement covers it, with a no-link control.
- AC-11: join order and `matrix --strict` exit 1 with a gap line; an out-of-scope FR gets no soup block. The weaknesses are SR-1627 FND-002.

Examined units:

- `FR-030-AC-1` .. `FR-030-AC-11` (role: examined), text as in spec/functional/FR-030-soup-requirements-design-relation.md lines 120-130.
- `FR-030-AC-8` (role: examined): Over the same fixture, `quoin class obligations` with a `soup-requirements` entry naming `relation: fr-has-soup-requirements` reads the `FR` row `unmet` before the statement and `met` after it, and reports `not-available` for an `FR` no record serves. (Demonstration)
- `FR-030` Behavior "Each finding SHALL be a warning, tunable on `trace:fr-without-soup-requirements` and `trace:nfr-without-soup-requirements`." (role: examined)
- `FR-030-CON-1` .. `FR-030-CON-3` (role: examined, Inspection).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | FR-030-AC-8 (Demonstration) has no recorded demonstration, and none can be run against the released quoin: `quoin class obligations` with installed quoin 0.36.8 refuses the policy with `unknown field relation, expected one of id, kind, method`, and the `soup-requirements` kind (quoin #1032) is on quoin main but absent from tag v0.36.10, the `package.json` pin. The spec's Demonstration method is right, because the behaviour is quoin's and quoin's tc_plat1836_003 tests the kind generically, so no test belongs in this repository. The demonstration should be recorded on the ticket once a quoin release carries #1032. It does not wait on quoin #1042, which only adds the `design-trace` `relation` key. | spec/functional/FR-030-soup-requirements-design-relation.md:127 |
| FND-002 | low | The Behavior "Each finding SHALL be a warning" is asserted only for the FR finding (AC-6 test, `startswith("warning:")`). The AC-9 test checks promotion and `off` for `nfr-without-soup-requirements` but never asserts that the plain finding is a warning or that the plain run exits 0. | tests/test_soup_requirements.py:276-278 |

## Verdict

**PASS with two low findings.** Every Test-method criterion has a tagged test that can fail, and the manifest mutations prove it. The only untagged criterion, AC-8, is a Demonstration whose method is correct and which cannot be performed until a quoin release ships the `soup-requirements` kind (FND-001; suggested disposition: deferred to the ticket). FND-002 is a one-line test addition.
