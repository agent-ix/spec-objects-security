---
id: SR-1626
title: "Gap analysis — FR-030 acceptance criteria against the code step"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-security; spec/functional/FR-030-soup-requirements-design-relation.md, spec/functional/FR-013-soup-record-serves-requirement.md, tests/test_soup_record.py, spec_objects_security/manifest.yaml"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-030
    type: reviews
---
# SR-1626: Gap analysis — FR-030 acceptance criteria against the code step

## Summary

Ticket: PLAT-1855; PR agent-ix/spec-objects-security#79 at head `1a9075387ab1678d9c269b85170454d3d1d30b0d`, scope `git diff origin/main...HEAD`. Spec-only PR: the manifest and tests follow in a later code step, so this audit checks that each FR-030 criterion is testable with the repository's existing harness (`tests/test_soup_record.py` `_validate`, `quire_engine`, the installed iso module) and that the spec leaves no behaviour the code step cannot be held to. No cargo or `make ci` was run (spec-only).

## Verdict

**PASS with two low findings.** Plan completion: not assessed.

`quire matrix --scope .` on the PR head lists FR-030-AC-1..8 as `untagged` and FR-030-CON-1..3 as `method-without-symbol`, which is expected before the code step; FR-013-AC-1..7 stay `tagged` to `tests/test_soup_record.py` and the FR-013-AC-1 test (which selects the relation by `from == soup_record`) still matches the reworded criterion. Each FR-030 AC names an observable outcome a test can fail: AC-1 exact manifest data, AC-2..AC-6 `quire relations --json` and `quire validate --okf` findings over fixtures, AC-7 manifest data, AC-8 a quoin `class obligations` demonstration that quoin origin/main implements. The engine behaviour AC-3 and AC-5 rely on (inverse counterpart reading, no Tier-2 finding for an inverse whose forward verb is absent from `allowed_links`, wrong-kind incoming source leaves a gap) was confirmed in quire-rs origin/main. The design-trace / `--strict` side effect (SR-1625 FND-001) also has no AC; it is recorded there, not duplicated here.

Examined units:

- `FR-030-AC-1..8` (role: examined).
- `FR-030-CON-1..3` (role: examined).
- `FR-030` Outputs (role: examined).
- `FR-013-AC-1` and its test `tests/test_soup_record.py:595-608` (role: examined).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The `nfr-has-soup-requirements` relation has no behavioural criterion: AC-2, AC-3 and AC-6 exercise only a served `FR`, AC-4 only the unserved case, so no AC requires a served `NFR` with no statement to be `uncovered` with an `nfr-without-soup-requirements` finding, to become `covered` by a statement, or `trace:nfr-without-soup-requirements` to be tunable, although Behavior names both keys | spec/functional/FR-030-soup-requirements-design-relation.md:99-103 |
| FND-002 | low | Outputs state the verb's category is `traceability`, but no Behavior SHALL and no AC fixes the category (AC-1 checks only the inverse), so the code step can declare any category and still pass | spec/functional/FR-030-soup-requirements-design-relation.md:76 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | low | FR-030-AC-11's matrix clause does not name the quire-cli FR-043 observable and its negative is ambiguous: "reports a block for the uncovered FR" holds without `--strict` too (the gate is exit 1 with a stderr line naming the document and `fr-without-soup-requirements`), and "none for a requirement outside the scope" is false read literally in the stated corpus, where spec-objects-architecture's relation still gives that requirement its own block; it should say no `fr-has-soup-requirements` block or gap | spec/functional/FR-030-soup-requirements-design-relation.md:130 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Verified in fix commit 3b08c0a (head 3b08c0a3a9a515b5cfb284e0fa37d79ea5ce3180). |
| FND-002 | fixed | Verified in fix commit 3b08c0a (head 3b08c0a3a9a515b5cfb284e0fa37d79ea5ce3180). |
