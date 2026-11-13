---
id: SR-045
title: "Code review of PR #50 NIST SP 800-53 Rev 5.2.0 clause set"
type: SpecReview
analysis: code-review
review_set: subset
scope: "agent-ix/spec-objects-security; spec_objects_security/clauses/nist-sp800-53-5.2.0.json, spec_objects_security/manifest.yaml, tests/test_clause_sets.py, package.json, package-lock.json, pyproject.toml, scripts/stage-npm.mjs (PR #50, git diff origin/main...HEAD at 4d92f0a)"
---
# SR-045: Code review of PR #50 NIST SP 800-53 Rev 5.2.0 clause set

## Summary

Ticket: PLAT-1521. The PR changes data, Python tests and packaging. It has no Rust and
no spec change. The tests ran on an exported copy of 4d92f0a, using quire 0.44.0
(engine 0.59.1) and quoin 0.30.1 from `npm ci` against npmjs. `tests/test_clause_sets.py`
gives 10 passed. The full suite, run on a git clone, gives 251 passed and 9 xfailed, with
100% coverage.

The clause data was checked against the official OSCAL content in usnistgov/oscal-content
(`nist.gov/SP800-53/rev5/json`). The catalogue and the LOW, MODERATE, HIGH and PRIVACY
profiles all have metadata version 5.2.0. The catalogue holds 1196 controls and
enhancements, of which 182 are withdrawn. The set has exactly the 1014 that are not
withdrawn, in catalogue order. It contains no withdrawn id and no extra id. Every title
matches OSCAL byte for byte. Every `subjects[0]` is the OSCAL group title of the control.
The 20 family values match the OSCAL group ids. The baselines nest (LOW is inside
MODERATE, which is inside HIGH). Each clause's `at_least` value is the lowest baseline
that selects it, and evaluating the set gives 149, 287 and 370 binding clauses for low,
moderate and high, which match the profiles exactly. The 644 controls in no baseline are
`permitted` with `not(at_least low)`. They are `not_binding` under any baseline and
`unresolved` when no baseline is given. `source.officialUrl` is the CSRC page that
carries the 5.2.0 release notice of 2025-08-27.

The rights are truthful: a US Government work under 17 U.S.C. 105, `text: none`,
`structure: citation_only`, and no clause carries `text`. `quire publish-check --module
spec_objects_security` exits 0 with `no restricted clause sets`. When the copied module's
set is changed to `text: licensed`, the same command exits 2 and names
`nist/sp800-53@5.2.0`, so the check really does load the shipped set.

The bump of `@agent-ix/quire-cli` from 0.43.0 to 0.44.0 is legitimate. `publish-check`
first ships in 0.44.0 (CHANGELOG, PLAT-1421), and FR-017-AC-3 needs it. The lockfile
integrity values match the npmjs registry for the main package and for the linux-x64
package.

The packaging additions work. The wheel built with `poetry build -f wheel` contains
`spec_objects_security/clauses/nist-sp800-53-5.2.0.json`. `npm pack --dry-run` stages
`clauses/`, ships `clauses/nist-sp800-53-5.2.0.json` and removes the staged copy
afterwards.

The PR commits no build artifacts and no generator script. It has no roadmap content
and copies nothing from another repo. The staged clause-only module in the tests is a
temp-dir copy of the committed file.

## Verdict

**FAIL, fixable in this PR.** One high finding: FR-015 says the module carries no title
of any standard, and the PR adds 1014 control titles and 20 family titles. There are
three medium findings and two low ones. The data itself is correct against OSCAL 5.2.0.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-015 Behavior says "The `control` skeleton and the module SHALL contain no clause text, title or summary of any standard". The module now ships 1014 NIST control titles and 20 family titles (in `subjects`), plus the publication title. FR-015 is contradicted as written, though the titles are lawful: public domain, and quire-rs FR-073 lets a citation-only set keep titles. FR-017 only bounds text "beyond what its source licence allows", so the two FRs now disagree. Fix in this PR (PR #51 ASVS has the same problem): narrow the FR-015 bullet to the control skeleton and `ControlMapping`, plus "no clause text, title or summary of a licence-restricted standard", and cross-reference FR-017 | spec/functional/FR-015-mappings-carry-no-standard-text.md:25, spec_objects_security/clauses/nist-sp800-53-5.2.0.json:71 |
| FND-002 | medium | The PR adds three keys to `rights`: `licence`, `attribution` and `share_alike`. quire-rs `ClauseSetRights` is `{structure, text, clearance_ref}` without `deny_unknown_fields`, so serde drops the three keys silently at load. The loader is not strict, and no engine schema or spec (quire-rs FR-073 or FR-083) defines them. This does not breach FR-083: the engine never reads these keys, and `rights.text` stays the only licence signal. But FR-017 and quoin FR-172 require only that the rights "state the licence". `attribution` and `share_alike` are new, unspecified keys, and the FR-017-AC-2 test asserts them, which binds the suite to a contract no spec states. Fix: name the keys and their meaning in FR-017, keeping `share_alike` and `attribution` only where a licence imposes them (ASVS, CC BY-SA), and drop them from the NIST set and test otherwise. If the licence is meant to be engine data, route a quire-rs ticket to add it to `ClauseSetRights` | spec_objects_security/clauses/nist-sp800-53-5.2.0.json:7-14, tests/test_clause_sets.py:98-111 |
| FND-003 | medium | The `family` classification dimension is not connected to any clause. Its values are codes (`ac` … `sr`), each clause's `subjects` holds the family title ("Access Control"), and no applicability refers to `family`. Nothing in the data joins a clause to its dimension value except parsing the id prefix. The test checks 20 distinct subjects, not that each subject is a declared family value, so a set whose subjects match no dimension value still passes. Fix: make `subjects` carry the dimension value (for example `ac`), which also removes 20 titles (FND-001), and assert that every clause's subject is in `classificationDimensions.family.values` and equals its id prefix | spec_objects_security/clauses/nist-sp800-53-5.2.0.json:21-44, tests/test_clause_sets.py:152-166 |
| FND-004 | medium | All 37 PM (Program Management) controls and all 21 PT controls are `permitted` with `not(at_least low)`, so an RMM over any baseline shows them as "Not applicable". SP 800-53B does not place PM controls in the security baselines because they apply organisation-wide whatever the impact level. The OSCAL PRIVACY profile (96 controls, 53 of them outside HIGH, every PT control among them) is the fifth profile, and the set does not model it. A profile cannot bind the privacy baseline, and PM-1 can never bind. Fix: add a privacy-baseline dimension (for example `privacy: selected`, used with `eq`) and decide how PM applies (binding with no applicability, or its own dimension). Otherwise state the low/moderate/high-only scope and the PM treatment in FR-017 and the ticket | spec_objects_security/clauses/nist-sp800-53-5.2.0.json:612, spec_objects_security/clauses/nist-sp800-53-5.2.0.json:666 |
| FND-005 | low | `stage-npm.mjs` now stages `clauses/` at the repository root, and its header says "the staged copies are gitignored". `.gitignore` lists `/manifest.yaml`, `/schemas/` and `/skeletons/` but not `/clauses/`. If `postpack` fails, the root `clauses/` is left untracked, and `git add -A` would commit a second 336 kB copy. Fix: add `/clauses/` to `.gitignore` | scripts/stage-npm.mjs:8, scripts/stage-npm.mjs:36, .gitignore:16-18 |
| FND-006 | low | No test checks that the clause file is in the built wheel or the npm tarball. `test_the_built_wheel_contains_every_exported_schema` covers schemas only. Both were measured by hand and both include the file, but a regression in `pyproject.toml` `include` or `package.json` `files` would pass the suite, and the installed module would then fail to load `clause_sets`. Fix: extend the wheel test to cover every path in `manifest.clause_sets` | pyproject.toml:16, package.json:18, tests/test_schema_emission.py |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | 0291192 narrows FR-015: the skeleton carries no title of any standard, the module no title of a `licensed` set, and a publishable set carries titles as its rights allow |
| FND-002 | fixed | FR-017 now specifies `licence`, `attribution` and `share_alike` as informational keys that the engine ignores; the NIST set drops `attribution` and `share_alike`, and TC-179 asserts they are absent |
| FND-003 | fixed | Every NIST clause's `subjects` is now its family code; TC-180 asserts that it equals the id prefix and is a declared `family` value. Re-measured against OSCAL: 0 mismatches |
| FND-004 | fixed | Lead decision: the low/moderate/high-only scope and the PM/PT/privacy treatment are written into FR-017; the data is unchanged and stays correct against OSCAL |
| FND-005 | fixed | `.gitignore` now lists `/clauses/` |
| FND-006 | fixed | TC-182 builds the wheel and runs `npm pack`, asserts that every `clause_sets` path ships, and checks that no staged `clauses/` is left behind; it passes |
