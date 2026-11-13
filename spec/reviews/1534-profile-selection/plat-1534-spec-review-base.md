---
id: SR-041
title: "Base spec review of PR #48 source profile format and default profiles"
type: SpecReview
analysis: base
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-020-source-profile-format.md, spec/functional/FR-021-default-source-profiles.md, spec/non-functional/NFR-002-profiles-never-name-or-carry-licensed-content.md, spec/functional/index.md, spec/non-functional/index.md (PR #48, git diff origin/main...HEAD at 3f39621)"
---
# SR-041: Base spec review of PR #48 source profile format and default profiles

## Summary

Ticket: PLAT-1534. This is a spec-only PR that adds FR-020, FR-021 and NFR-002.
`quire validate` (quire 0.44.0, engine 0.59.1) exits 0 on all five changed files.
The only output is two warnings that predate this PR (a `spec-artifacts-app`
unused import, and a `DuplicateModuleName` from the second local checkout).
Applicability: the repo has no `AssuranceProfile` document, so no review policy
applies, and this subset was chosen by the dispatching brief.

All four ticket scope items are decided across this PR and quoin #870:

- format: FR-020
- location and selection: FR-020 and quoin FR-180
- defaults: FR-021
- licensed-pack join: quoin FR-182 and NFR-002

No paywalled standard text appears, and no file names a licensed pack.

The clause-set key shape (`authority`, `id`, `version`) and the context type
(string to string) match the engine's `ClauseSet::evaluate(&BTreeMap<String, String>)`
in quire-rs `src/clauses.rs`. The `profiles/` directory discovery matches quoin
FR-180.

The defects are below. The two high findings are an ID collision with the
parallel PLAT-1426 lane, and a rights rule that contradicts the engine's
publishability rule.

## Verdict

**FAIL**: two high, four medium and four low findings. All can be fixed in this PR.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | ID collision with the PLAT-1426 lane. Open PR agent-ix/spec-objects-security#49 (PLAT-1426, opened 2026-11-13T13:57:22Z, one minute after this PR) adds FR-020..FR-024: `FR-020-control-mappings-are-clause-references`, `FR-021-mapping-resolution-and-duplicates`, and so on. This PR adds FR-020 and FR-021, so whichever PR merges second produces duplicate ids. The companion ids collide too. quoin#871 (PLAT-1426) adds quoin FR-180..FR-183 while quoin#870 adds FR-180..FR-182. So this PR's `ix://agent-ix/quoin/FR-180` / `FR-181` relationship targets and NFR-002's FR-182 link will resolve to PLAT-1426 documents if #871 lands first. #49's FR-023 already cites "quoin FR-182" for a different meaning. The PR body's claim that it chose "a high range to avoid the parallel PLAT-1426 lane" is not true of the measured state. Fix: renumber to ids neither lane uses, for example FR-025/FR-026 here (or a block agreed with PLAT-1426) and quoin FR-184+ there, and update every cross-reference | spec/functional/FR-020-source-profile-format.md:2, spec/functional/FR-021-default-source-profiles.md:2, spec/functional/FR-020-source-profile-format.md:8, spec/functional/FR-021-default-source-profiles.md:8 | wrong-requirement |
| FND-002 | high | FR-021-AC-3 hard-codes a rights rule that contradicts the engine. quire-rs FR-083 makes a set publishable iff `rights.text` is not `licensed`, so `none`, `original` and `explicitly_cleared` all qualify. It also says "Structure rights do not change the verdict" (FR-083-AC-5) and that consumers hold no rights policy. AC-3 excludes `text: explicitly_cleared` and adds a `structure` condition, which also excludes `structure: explicitly_cleared`. A cleared, publishable set would therefore fail this module's test. AC-3 also exceeds its Behavior line (text only). Fix: state publication as "the engine's publishability check (`check_publishable` / `quire publish-check`) reports no set of the profile" and drop the enumerated values | spec/functional/FR-021-default-source-profiles.md:49, spec/functional/FR-021-default-source-profiles.md:38 | wrong-requirement |
| FND-003 | medium | NFR-002-AC-2 adds a second licence signal: a hand-kept allow-list of "publishable authorities" in the test. quire-rs FR-083 says rights are the only licence signal. An allow-list passes a licensed set from an allowed authority and rejects a publishable set from a new one, so it can be green while the profile lists a licensed pack. NFR-002's own second metric is already rights-based. Fix: drop AC-2 and verify NFR-002's second statement with the engine publishability check (FND-002) | spec/non-functional/NFR-002-profiles-never-name-or-carry-licensed-content.md:42 | wrong-requirement |
| FND-004 | medium | FR-021's first Behavior line (ship the three named profiles) has no acceptance criterion. AC-1, AC-2, AC-3 and AC-5 are all "for every shipped profile". Today no publishable set exists to list: PLAT-1593, PLAT-1612 and PLAT-1627 are Backlog, and no NIST or OWASP clause set was found in the local reference modules. So the module can ship zero profiles and every AC passes vacuously. Fix: add an AC that, for each named profile, the profile exists exactly when at least one of its intended sets is declared by a published module, and is absent otherwise | spec/functional/FR-021-default-source-profiles.md:37 | missing-requirement |
| FND-005 | medium | FR-021-AC-2 tests against "the reference module set", which is defined nowhere. Behavior says "some published module". Two implementers would load different module sets: installed modules, the quoin default catalog, or a fixture list. Fix: name the set, for example the modules `quoin module ensure-defaults` installs plus this module | spec/functional/FR-021-default-source-profiles.md:48, spec/functional/FR-021-default-source-profiles.md:39 | wrong-requirement |
| FND-006 | medium | The PR adds 14 ACs and 2 NFR metrics but no test-case rows in `spec/tests.md`, and no `covers` relationships for FR-020, FR-021 or NFR-002. The repo convention is that a spec PR adds its TC rows in the same change (PR #44 added TC rows and `covers` edges for FR-009..FR-012). Fix: add TC rows (status 🚧 until implemented) and the three `covers` edges | spec/tests.md | missing-requirement |
| FND-007 | low | FR-021-AC-5 asserts Quoin evaluation behavior: partial install yields `unavailable`, and the rest is evaluated. That is quoin FR-181-AC-3. No FR-021 Behavior line states it, and this module's tests cannot run it without Quoin. Fix: drop AC-5 and keep the quoin FR-181 reference in the Description | spec/functional/FR-021-default-source-profiles.md:51 | wrong-requirement |
| FND-008 | low | FR-020 `implements` US-001, "Declare security object types against semantic-core". A source profile is module data, not an object type, so the trace is to an unrelated story. Fix: trace to a story or StR that covers source selection (add one if none exists), or drop the edge | spec/functional/FR-020-source-profile-format.md:6-7 | wrong-requirement |
| FND-009 | low | `spec/spec.md` In Scope lists the manifest, object types, templates, schemas and grammars. The new `profiles/` data and its schema are not in scope there, so the module's scope statement no longer covers what FR-020 and FR-021 ship. Fix: add one In Scope bullet for source profiles | spec/spec.md:25-36 | missing-requirement |
| FND-010 | low | FR-021's Description lists cross-repo delivery order: which tickets will publish which packs, and "until then" shipping behavior. The rule in the same paragraph (a key is listed in the change that publishes its set) already says what is needed, without the ticket schedule. Fix: drop the ticket list and the "until then" sentence, and keep the rule | spec/functional/FR-021-default-source-profiles.md:24-28 | wrong-requirement |
