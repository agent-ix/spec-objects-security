---
id: SR-046
title: "Gap analysis of PR #50 NIST SP 800-53 Rev 5.2.0 clause set"
type: SpecReview
analysis: gap-analysis
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-017-module-declares-nist-and-asvs-clause-sets.md, spec/tests.md, spec_objects_security/clauses/nist-sp800-53-5.2.0.json, spec_objects_security/manifest.yaml, tests/test_clause_sets.py (PR #50, git diff origin/main...HEAD at 4d92f0a); PLAT-1521 acceptance criteria"
---
# SR-046: Gap analysis of PR #50 NIST SP 800-53 Rev 5.2.0 clause set

## Summary

Ticket: PLAT-1521. Plan completion: not assessed. This gap analysis covers FR-017
AC-1 to AC-4 and the four acceptance criteria of the ticket. The coverage data comes
from `quire matrix --scope .` (quire 0.44.0) run on a clone of 4d92f0a. The outcomes
come from running the tests and the CLIs directly.

Each criterion was traced to evidence:

- **FR-017-AC-1.** `test_manifest_declares_the_nist_clause_set` covers it, but only
  partly (FND-003).
- **FR-017-AC-2.** Two tests cover it, and both pass.
- **FR-017-AC-3.** `test_publish_check_accepts_the_module` covers it. It runs on the
  real module and exits 0.
- **FR-017-AC-4.** `test_publish_check_refuses_a_licensed_set` covers it. The test
  exits non-zero, and the sentinel is absent from the output.

The ticket's acceptance criteria were checked the same way:

- **Ticket AC 1 (loads and validates).** The set validates through
  `quire clauses evaluate`, but only from a staged module (FND-002).
- **Ticket AC 2 (dimensions).** Both dimensions are present. The family dimension
  is not linked to the clauses (SR-045 FND-003).
- **Ticket AC 3 (publish-check).** Met.
- **Ticket AC 4 (`--pack` matrix).** Cannot be met as written (FND-004). The
  PR's FR-135 single-set run (`quoin discharge --rmm --binding --repo`) is the
  right test, and it renders a matrix over a synthetic corpus.

The `quire matrix` run produced no backing for FR-017: every FR-017 criterion shows
`untagged` (FND-001).

## Verdict

**FAIL, fixable in this PR.** The behaviour is implemented and tested, but the computed
matrix gives FR-017 no backing (FND-001). One ticket AC can be met only through a staged
copy, because of an engine limit (FND-002). Another ticket AC needs its text corrected
(FND-004).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | `quire matrix` reports FR-017-AC-1 to AC-4 as `untagged`. Each `@pytest.mark.trace("FR-017-AC-n")` emits `criterion-tagged-outside-row … This tag does not provide backing`. This repo's convention is that each FR has a coverage row and TC rows in `spec/tests.md`, and each test tags its TC id with the AC (for example `trace("TC-121", "FR-009-AC-1")`). `spec/tests.md` has no FR-017 row and no TC rows. Fix: add the FR-017 coverage row and one TC row per test to `spec/tests.md`, and tag each test with its TC id | spec/tests.md:126-133, tests/test_clause_sets.py:92-130 |
| FND-002 | medium | `quire clauses evaluate --module spec_objects_security --authority nist --set sp800-53 --version 5.2.0` exits 3 with `loading clause-set module: EdgeVocabularyViolation [UnknownEdgeType]: 'references'`. The `quire clauses` loader is strict and does not merge the edge vocabulary of the installed modules, so the shipped module cannot be evaluated where it lives. Ticket AC 1 and the RMM test are met only through `_stage_clause_only_module`, a temp module that holds the set alone. Anyone binding the installed NIST set has to repeat that workaround. The data is fine; the gap is in the engine. Fix: send it to the quire-rs owner (terra:quoin:triage) so `quire clauses` resolves edge types the way `quire validate` does. Then point the test at `PACKAGE_ROOT` | tests/test_clause_sets.py:44-60, tests/test_clause_sets.py:138-146 |
| FND-003 | low | FR-017-AC-1 requires `clause_sets` to name exactly `nist/sp800-53@5.2.0` and `owasp/asvs@5.0.0`. The test asserts `"nist/sp800-53@5.2.0" in keys`, which passes with ASVS absent and with any extra set present, so its AC-1 trace cannot fail on the AC's real condition. PR #51, stacked on this one, replaces it with an exact-equality test. Disposition: deferred to PR #51, provided the two merge together | tests/test_clause_sets.py:92-94, spec/functional/FR-017-module-declares-nist-and-asvs-clause-sets.md:39 |
| FND-004 | low | Ticket AC 4, "`quoin discharge --rmm --pack` renders a matrix for the set", cannot be met for this module. The installed quoin 0.30.1 has no `--pack` flag (`quoin discharge --help`). On quoin main, `pack_matrix` refuses any module that is not a pack (`module … is not a pack`), and FR-137 defines a pack as a module with at least one restricted (`licensed`) clause set. spec-objects-security is publishable by design (FR-017), so it can never be a `--pack` target. The right test is the FR-135 single-set path, which the PR uses: `quoin discharge --binding <quire clauses evaluate output> --rmm --repo`. Fix: amend the ticket AC to the FR-135 form; the code needs no change | tests/test_clause_sets.py:183-245 |
