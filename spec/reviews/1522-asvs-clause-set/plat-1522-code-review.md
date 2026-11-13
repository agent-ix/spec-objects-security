---
id: SR-047
title: "Code review of PR #51 OWASP ASVS 5.0.0 clause set"
type: SpecReview
analysis: code-review
review_set: subset
scope: "agent-ix/spec-objects-security; spec_objects_security/clauses/owasp-asvs-5.0.0.json, spec_objects_security/manifest.yaml, tests/test_clause_sets.py (PR #51, git diff origin/plat-1521-nist-clause-set...HEAD at 117369e)"
---
# SR-047: Code review of PR #51 OWASP ASVS 5.0.0 clause set

## Summary

Ticket: PLAT-1522. Stacked on PR #50 (PLAT-1521). This review covers only #51's
own diff: the new ASVS clause-set file, one manifest line and the test additions.

What was measured at 117369e:

- **Data against the official release.** The PR file was compared with OWASP/ASVS
  tag `v5.0.0_release`, `5.0/docs_en/..._5.0.0_en.json`, and the 5.0.0 CSV. Both
  have 345 requirements. The id sets are equal and in the same order. All 17
  chapters V1-V17 match, and every clause's `subjects` equals its official
  chapter name. Every `applicability` is `at_least level <L>` with the official
  `L`. The cumulative binding counts are 70 / 253 / 345. There are no mismatches
  against either the JSON or the CSV.
- **No requirement text.** Every clause has exactly the keys `id, force, subjects,
  obligatedActors, approvalRoles, styles, applicability, expectedOutputs`. There
  are no `title` or `text` keys. No 40-character prefix of any official
  requirement description appears in the file. No section name appears either,
  apart from two substrings of chapter names.
- **Rights.** `rights.text: none` and `structure: citation_only`. The engine
  rejects clause text under `text: none` (quire-rs `ClauseSet::validate`).
  `quire publish-check --module spec_objects_security` prints "No restricted
  clause sets" and exits 0 on quire 0.44.0 (engine 0.59.1). A copy with ASVS
  `rights.text: licensed` exits 2 and names `owasp/asvs@5.0.0`, so the check
  really reads the new file.
- **Consistency with quoin PR #873** (merged, `skills/spec-security-analysis/references/owasp-asvs/`).
  The 17 chapter headings equal the official names. The 345 requirement ids in its
  tables equal this set's ids, and the lowest-ticked level of every row equals
  the set's `at_least` value. The three `V`-prefixed ids cited elsewhere in the
  skill all exist.
- **Packaging.** No new packaging change is needed, because #50's
  `clauses/*.json` globs already cover the file. A `poetry build -f wheel` holds
  `spec_objects_security/clauses/owasp-asvs-5.0.0.json`. `stage-npm.mjs` and
  `package.json` `files` already ship `clauses/`.
- **Tests.** The `tests/test_clause_sets.py` suite has 15 tests and all pass.
  `ruff check` and `ruff format --check` are clean.
- **Hygiene.** One commit. No build artifacts, no generator script, no roadmap
  text, and no vendored copy of the ASVS release are committed.

## Verdict

**PASS with findings.** The data is correct against the official release, and the
licensing posture is truthful. Because the set carries only ids and 17 short
chapter names, CC BY-SA share-alike is not triggered, and the `share_alike`
statement says so honestly. One medium finding: the `chapter` dimension
classifies nothing. There are three low findings.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The `chapter` classification dimension (values V1-V17) is inert. No clause references it: every `applicability` uses only `level`, and the clause carries its chapter only as a `subjects` name ("Encoding and Sanitization"), a different vocabulary from the dimension's values. In clause-set-v1, dimensions are consumed only by applicability, so a context of `chapter=V6` changes nothing, and no data links a clause to a chapter value except by parsing the id prefix. The ticket AC "chapters are a classification dimension" is met by declaration only. `test_chapters_classify_and_levels_are_an_ordered_applicability_dimension` checks that the 17 values are declared and that the subjects are distinct, but never checks clause-to-chapter membership. Fix: carry the chapter id per clause in a field the model preserves (for example `styles: {"chapter": "V1"}`) and test that every clause's chapter value is a declared value that matches its id prefix. Alternatively, drop the unused dimension, make `subjects` the stated chapter classification, and amend the ticket AC. PR #50's `family` dimension has the same shape; that is not reviewed here | spec_objects_security/clauses/owasp-asvs-5.0.0.json:20-40, tests/test_clause_sets.py:212-220 |
| FND-002 | low | The attribution names the work, the author, the licence name and the source repository, but not the licence URI. CC BY-SA 4.0 s.3(a)(1)(C) requires a URI or hyperlink to the licence. Fix: append `https://creativecommons.org/licenses/by-sa/4.0/` to `rights.attribution` (or to `licence`) | spec_objects_security/clauses/owasp-asvs-5.0.0.json:12 |
| FND-003 | low | The `licence`, `attribution` and `share_alike` keys are not fields of quire-rs `ClauseSetRights`, which declares only `structure`, `text` and `clearance_ref`. serde drops unknown keys at load, so the engine, `quire clauses` and quoin never see the licence. FR-017-AC-2 ("rights metadata naming its source licence") holds only in the raw JSON that the test reads, and a misspelt key (`license`) would load silently. This does not conflict with quire-rs FR-083: "Rights remain the only licence signal" governs publishability through `rights.text`, which these keys do not affect. It is a schema gap shared with #50. Fix: the owning ticket should add typed optional licence and attribution fields in quire-rs, or this PR accepts the gap as is | spec_objects_security/clauses/owasp-asvs-5.0.0.json:11-13 |
| FND-004 | low | `test_quoin_renders_an_asvs_requirements_matrix_over_a_synthetic_corpus` asserts a Compliant row (V1.2.1) and a Not-applicable row (V1.2.6), but no row that is applicable but undischarged, unlike its NIST counterpart (`AC-2 \| Applicable \| Not compliant - undischarged`). A renderer that marked every applicable ASVS clause Compliant would pass. Fix: also assert `\| V1.2.2 \| Applicable \| Not compliant - undischarged` | tests/test_clause_sets.py:297-306 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1, head 0db79e8. Every clause's `subjects` is now its chapter id (`["V1"]` .. `["V17"]`), equal to a declared `chapter` value and to its id prefix. `test_each_asvs_clause_names_its_chapter_dimension_value` (TC-184, FR-017-AC-6) asserts this for all 345 clauses |
| FND-002 | fixed | Round 1, head 0db79e8. `licence` and `attribution` both carry `https://creativecommons.org/licenses/by-sa/4.0/`, asserted by `test_every_set_names_its_licence_and_the_nist_set_is_public_domain` |
| FND-003 | deferred: the gap is in quire-rs `ClauseSetRights`, not in this module. The keys do not affect publishability, and FR-017-AC-5 now states them normatively in the module's raw JSON. Typed fields need a quire-rs change, which is outside this PR. There is no owning ticket; the lead decides whether to file one | - |
| FND-004 | fixed | Round 1, head 0db79e8. The ASVS matrix test also asserts `\| V1.2.2 \| Applicable \| Not compliant - undischarged` |
