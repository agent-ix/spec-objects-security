---
id: SR-048
title: "Gap analysis of PR #51 OWASP ASVS 5.0.0 clause set"
type: SpecReview
analysis: gap-analysis
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-017-module-declares-nist-and-asvs-clause-sets.md, spec/tests.md, spec_objects_security/clauses/owasp-asvs-5.0.0.json, spec_objects_security/manifest.yaml, tests/test_clause_sets.py (PR #51, git diff origin/plat-1521-nist-clause-set...HEAD at 117369e)"
---
# SR-048: Gap analysis of PR #51 OWASP ASVS 5.0.0 clause set

## Summary

Ticket: PLAT-1522. Plan completion: not assessed (planless). quoin 0.30.1, quire
0.44.0 (engine 0.59.1).

FR-017 acceptance criteria, measured at 117369e for #51's part:

- FR-017-AC-1 is met. `test_manifest_declares_exactly_the_nist_and_asvs_clause_sets`
  asserts the exact sorted key list.
- FR-017-AC-2 is met for ASVS (`licence` names CC BY-SA 4.0, `text: none`) by
  `test_every_declared_set_names_its_licence_and_a_publishable_text_right` and the
  new ASVS rights test. See SR-047 FND-003 for the raw-JSON-only caveat.
- FR-017-AC-3 is met. `quire publish-check --module spec_objects_security` exits 0.
- FR-017-AC-4 was already met by #50's licensed-fixture test and is unchanged.

Ticket ACs:

- AC-1 (rights record the open licence, attribution and share-alike truthfully;
  text only as the licence allows) is met. No requirement text is carried. A
  licence-URI nit is in SR-047 FND-002.
- AC-2 (levels are an applicability dimension; chapters are a classification
  dimension): levels are met. With `--context level=1/2/3`, `quire clauses`
  binds 70 / 253 / 345 clauses, and without a level every clause is unresolved.
  For chapters, see SR-047 FND-001.
- AC-3 (empty restricted list for the shipping module) is met on the real module.
- AC-4 (`quoin discharge --rmm --pack` renders a matrix over a synthetic corpus)
  is met by a substitute command. See FND-002.

The tests run `quire clauses evaluate` on a staged module that holds only the
clause sets. On the real module, `quire clauses evaluate --module spec_objects_security ...`
exits 3 with `EdgeVocabularyViolation [UnknownEdgeType]: 'references'`, because
the module's edges come from another module. The test helper's docstring
documents this, and it predates #51.

## Verdict

**PASS with findings.** Every behaviour #51 owns is implemented and tested. One
medium traceability gap means the computed matrix cannot see that coverage. One
low finding concerns ticket AC-4's wording.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | `quoin matrix --repo .` reports FR-017-AC-1..4 as `untagged` at 117369e. Every other FR in this repository binds through TC rows in spec/tests.md (`trace("TC-NNN", "FR-...")`), but FR-017 has no TC rows and its tests carry bare `trace("FR-017-AC-n")`. #51's rewritten AC-1 test and its new AC-2 test are therefore invisible to the computed matrix. Adding a TC id to the trace alone did not change the status in a scratch copy, so the TC rows are needed. The gap originates in #50, and the fix belongs to the stack: add FR-017 TC rows to spec/tests.md and tag the tests with them | tests/test_clause_sets.py:93-126, spec/tests.md |
| FND-002 | low | Ticket AC-4 names `quoin discharge --rmm --pack`. That cannot be met for this module. The installed quoin 0.30.1 has no `--pack` flag. On quoin main, `--pack` refuses any module where `is_pack` is false, and `is_pack` is `!restricted_sets(dir).is_empty()`: a pack must hold at least one `licensed` set (rust/crates/quoin-core/src/runtime.rs:334-339). FR-017 forbids licensed sets here. The substitute (`quoin evidence record-discharge`, then `quoin discharge --binding --rmm --repo`) renders the same per-set FR-135 matrix, and I judge it adequate. Fix: amend the ticket AC-4 text to the binding form, or disposition it on the ticket | tests/test_clause_sets.py:234-282,297-306 |
