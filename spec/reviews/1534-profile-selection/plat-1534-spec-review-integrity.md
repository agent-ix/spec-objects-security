---
id: SR-042
title: "Integrity review of PR #48 against companion quoin PR #870"
type: SpecReview
analysis: integrity
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-020-source-profile-format.md, spec/functional/FR-021-default-source-profiles.md, spec/non-functional/NFR-002-profiles-never-name-or-carry-licensed-content.md (PR #48 at 3f39621), read against agent-ix/quoin#870 FR-180, FR-181, FR-182, NFR-037"
---
# SR-042: Integrity review of PR #48 against companion quoin PR #870

## Summary

Ticket: PLAT-1534. This review checks that the module-side spec is internally
consistent and matches the companion quoin PR #870 (FR-180..182, NFR-037).

These parts are consistent:

- The `clauseSets` key shape matches FR-180 `add`.
- The `profiles/` directory discovery and the absent manifest key match FR-180.
- `unavailable` for an undeclared set matches FR-181.
- A licensed pack joins only through `add` in a local `source-profile.yaml`, per FR-182.
- The string-to-string context matches the engine's `ClauseSet::evaluate`.

The ID collision of the quoin companion ids is recorded in SR-041 FND-001. It is
not repeated here.

## Verdict

**FAIL (medium)**: one medium and two low consistency findings.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | medium | FR-020-AC-2 (and AC-3, AC-4 and AC-5) say a bad profile "fails validation" without naming the validator. A JSON Schema cannot compare `name` with the file stem, so AC-2's second half cannot be checked the way AC-1 is ("the profile JSON Schema"). No Behavior line requires the module to ship that schema, or says where it is. On the Quoin side, FR-180 reads profiles but has no requirement to validate one or refuse a malformed one. So nothing at use time enforces FR-020. Fix: add a Behavior line that the module ships `schemas/source-profile-v1.schema.json`, say that the stem check is a module test, and have quoin FR-180 refuse a profile that fails the schema or whose name differs from its stem | spec/functional/FR-020-source-profile-format.md:51, spec/functional/FR-020-source-profile-format.md:50 | missing-requirement |
| FND-002 | low | FR-020 Outputs says "A profile that Quoin lists, selects and evaluates". quoin FR-180..182 specify selection and evaluation but no listing command or output. Fix: drop "lists", or add a listing requirement to quoin #870 | spec/functional/FR-020-source-profile-format.md:34 | wrong-requirement |
| FND-003 | low | FR-020 says the profile `context` "is passed unchanged to the engine's clause-set evaluation". quoin FR-180 instead merges the repository `context` over it, and FR-181 passes that effective context. Fix: say the profile context is the base of the effective context (quoin FR-180) that the engine receives | spec/functional/FR-020-source-profile-format.md:22-24 | wrong-requirement |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | FR-020 now says the rules are checked by this repo's profile test and by Quoin on read, and that no JSON Schema ships. The ACs say "fails the profile test". quoin#870 FR-180 adds the matching refusal (Behavior line and FR-180-AC-8) |
| FND-002 | fixed | FR-020 Outputs now reads "A profile that Quoin selects and evaluates." |
| FND-003 | fixed | FR-020 now calls the profile context the base of the effective context, which a repository's values replace (quoin FR-180) |
