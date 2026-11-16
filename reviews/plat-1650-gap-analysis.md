---
id: SR-1614
title: "Gap analysis of PLAT-1650 PR #66 default US and EU profiles"
type: SpecReview
analysis: gap-analysis
review_set: subset
scope: "agent-ix/spec-objects-security; spec_objects_security/profiles/eu-device-gdpr-ai-act.yaml, spec_objects_security/profiles/us-device-cybersecurity-hipaa.yaml, tests/test_profiles.py and spec/tests.md (PR #66 at ffbf8fe7c7dade4d9d61f8af92300b554419eeb1), against FR-020, FR-021, NFR-002 and PLAT-1650 AC1-7"
---
# SR-1614: Gap analysis of PLAT-1650 PR #66 default US and EU profiles

## Summary

Ticket: PLAT-1650. Quoin's computed Test Matrix binds the applicable profile tests to FR-020-AC-1..6, FR-021-AC-1..3 and AC-5, and NFR-002-AC-1..2 and M-1..2. The new profile keys have direct assertions, and the fixture test changes a key version to ensure an undeclared key is refused with that key named. FR-021-AC-4, AC-6 and AC-7 are inspection criteria: both new profiles omit context, name only the public sources in the requirement, and list the keys declared by the newly released US/EU pack modules.

`quoin matrix --repo . --json` shows all applicable Test criteria tagged. The matrix also reports 43 untagged criteria in FR-022, FR-025, FR-026, FR-027 and NFR-005; the same 43 criteria are untagged on `origin/main` at 82ac619, so this PR introduces no matrix gap.

The ticket's seven acceptance criteria were reviewed: shipped profiles and allowed names (AC1); declared keys and a negative changed-version case (AC2); publish-check for each key (AC3); absent profile context (AC4); CLI evaluation with all packs and with the EU pack omitted (AC5); wheel and npm inclusion through existing glob/list/staging rules (AC6); and public, non-licensed sources (AC7). The focused test files passed, 45 total. CLI evaluation produced 2/2 web, 3/3 US, and 4/4 EU sets evaluated when modules were installed; with the EU module omitted, the EU profile reports 4 unavailable and exits 0.

## Verdict

**PASS**: no findings. All changed Test criteria are tagged and have test binders. The remaining untagged rows reproduce unchanged on clean `origin/main` and do not concern this diff.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |
