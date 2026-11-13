---
id: SR-051
title: "Code review of PR #53 typed controls and scope_exclusion"
type: SpecReview
analysis: code-review
review_set: subset
scope: "agent-ix/spec-objects-security; spec_objects_security/schemas/ControlMapping.json, spec_objects_security/schemas/ScopeExclusion.json, typespec/main.tsp, spec_objects_security/manifest.yaml, spec_objects_security/skeletons/control.md, spec_objects_security/skeletons/scope_exclusion.md, tests/, spec/tests.md (PR #53, git diff origin/main...HEAD at bc6eba1)"
---
# SR-051: Code review of PR #53 typed controls and scope_exclusion

## Summary

Ticket: PLAT-1427. One commit, bc6eba1. quoin 0.30.1, quire wheel from the
repo's Poetry environment.

What was measured:

- `poe test`: 296 passed, 3 skipped, 9 xfailed, 100% coverage. `poe lint`
  (ruff, black, schema drift gate with 52 schemas) is clean.
- `ControlMapping` is sealed `{set, clause}`. The old `framework`, `control_id`
  and `doc` keys are refused. TypeSpec and the emitted JSON agree (drift gate).
- The `scope_exclusion` type has a schema, a skeleton, a manifest entry with four
  required `section_body` locators, and an export. It is counted in the 25-type
  helpers.
- The engine reads `## Mappings` and `## Effectiveness` through
  `record-sections`. A probe showed that removing each exclusion section gives both
  the required-locator error and `semantic.record-invalid` at that key. A prose
  (non-inline-code) `## Rationale` or `## Effectiveness` is refused with
  `semantic.feature-not-extractable`. A third `Title` column gives
  `semantic.invalid-model-cell` at the header line, and the column value does
  not appear in the `extract_semantic` output.
- No standard text, no vendored content, no build artifacts and no digest or pin
  were added.

## Verdict

**PASS with findings.** The schemas, the manifest and the skeletons do what
FR-014, FR-015 and FR-016 describe on the ASCII path. There is one medium
finding: identifier length is measured in characters, not bytes. There is one
low finding about a hand-maintained test table.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-014 bounds each part of `set` and the `clause` id to 1 to 64 bytes, so that a mapping this module accepts is never refused on length by `quoin evidence record-discharge` (quoin FR-133 refuses an id over 64 bytes). The schemas count characters instead: `[^/@]{1,64}` and `maxLength: 64`. A probe validated a control whose clause was 64 copies of `é` (128 bytes), and another whose set authority was the same 128-byte string. Both were `is_valid: true`, which is exactly the length refusal FR-014 says cannot happen. The same bound appears in `ScopeExclusion.json` and in both TypeSpec models. Fix: restrict each part to printable ASCII without `/` and `@` (for example `[!-.0-?A-~]{1,64}`), so that characters equal bytes. Then add a non-ASCII case to TC-188. Alternatively, amend FR-014 to state the ASCII alphabet | spec_objects_security/schemas/ControlMapping.json:6-13, spec_objects_security/schemas/ScopeExclusion.json:6-14, typespec/main.tsp:156-157, typespec/main.tsp:814-815 |
| FND-002 | low | `spec/tests.md` is a hand-maintained test matrix (TC id to AC to status). It repeats what `quoin matrix` computes from the `@pytest.mark.trace` tags, and this PR grows it by 20 rows. Its ✅ status column is a claim that nothing checks. This is file-tracking ceremony: the computed matrix already holds the same data. Fix: stop extending the table, and drop it repo-wide under its own ticket. The trace tags remain the record | spec/tests.md:137-139, spec/tests.md:294-310 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1, head 33521a3. `ControlMapping.json` and `ScopeExclusion.json` now pattern `set` as `^[!-.0-?A-~]{1,64}/[!-.0-?A-~]{1,64}@[!-.0-?A-~]{1,64}$` and `clause` as `^[!-~]{1,64}$`, so the character limits are the byte limits |
| FND-002 | rejected | The finding was wrong. `spec/tests.md` is TM-001, a typed TestMatrix; quire's traceability model backs a trace tag only through a declared TC row, so the table is load-bearing, not ceremony. Removing its 20 rows in round 1 unbound all 17 FR-014/015/016 criteria (SR-052 FND-003) |
