---
id: SR-033
title: "Gap analysis of PR #45 soup_record object type"
type: SpecReview
analysis: gap-analysis
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-004-role-schemas.md, spec/functional/FR-009..FR-012, spec/non-functional/NFR-001-soup-records-state-and-never-derive.md, spec/tests.md TC-121..TC-145, tests/test_soup_record.py, spec_objects_security/ (PR #45, git diff origin/main...HEAD at 07788e5)"
---
# SR-033: Gap analysis of PR #45 soup_record object type

## Summary

Ticket: PLAT-1514. Plan completion: not assessed (planless). `quire matrix
--strict --scope .` reports 8 untagged criteria. Four of them predate this PR
(FR-001-AC-2..4 and FR-003-AC-5, which need filament-core or a Quoin
installer). The four this PR adds are FR-009-AC-3, FR-010-AC-5, NFR-001-M-1 and
NFR-001-M-2. FR-009-AC-8, FR-009-CON-2, FR-011-AC-4 and FR-011-CON-1 are
Inspection (`method-without-symbol`). Every other FR-009..FR-012 and NFR-001
criterion is tagged. The semantic review was done inline at the brief's request,
not fanned out. Its results for test strength are in SR-032 (FND-001..FND-003).

Ticket ACs: AC-1 (type and emitted schema follow the module conventions) is met.
The purl handling follows the `vulnerability`/`severity` convention: a required
frontmatter key plus a required marker field row. AC-2 is met only vacuously; see
SR-032 FND-001. AC-3 ("a risk disposition requires an approval ref; no derived
score") is met as FR-011 refines it: the record holds `disposition_clause` only,
and the approval ref lives in the quoin FR-046 fact. No score, class or level
field exists (TC-144).

## Verdict

**FAIL**: the spec and code disagree on purl (high), and two NFR metrics are
untagged. Everything can be fixed in this PR. The two engine-gap criteria should
stay 🚧 with the target design kept in the spec.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | Spec says purl is a required top-level schema key; the code makes it a required `fields` row (PurlField) plus a required frontmatter key, with top-level `purl` optional. Amend in this PR: FR-004 soup_record row moves `purl: string` to Optional keys and adds "≥ 1 `purl` field" to Item rules; FR-009 Behavior replaces "The `soup_record` schema SHALL require `purl`..." with "A `soup_record` document SHALL carry `purl`, the component's package URL, as a required frontmatter key; it is the component identity." and "The `soup_record` schema SHALL require a `purl` field row in `fields`."; FR-009-AC-2 becomes "A fixture `soup_record` with a purl validates; the same document without its `purl` frontmatter key fails naming `purl`, and a declaration record without a `purl` field row fails its schema." | spec/functional/FR-004-role-schemas.md:67, spec/functional/FR-009-soup-record-identity-and-promotion.md:56,82, spec_objects_security/schemas/SoupRecord.json:16-19,72-80 |
| FND-002 | medium | NFR-001-M-1 and NFR-001-M-2 are untagged, so `quire matrix --strict` fails on them. Both are already asserted: tag TC-144 with NFR-001-M-1 and TC-145 with NFR-001-M-2 | spec/non-functional/NFR-001-soup-records-state-and-never-derive.md:37-38, tests/test_soup_record.py:246,257 |
| FND-003 | medium | FR-009-AC-3 (duplicate purl) and FR-010-AC-5 (empty or absent `serves`) cannot be enforced by the engine (no cross-document identity on a frontmatter key; no presence check on a record list key). Leaving TC-123/TC-133 🚧 with honest notes is right, and the spec keeps the target design. Add: one engine-gap ticket routed to terra:quoin:triage, cited in both notes; `xfail(strict=True)` tests tagged FR-009-AC-3 and FR-010-AC-5 that reproduce the gap (precedent tests/test_manifest_semantic.py:88), so the rows flip when the engine lands. Fix TC-133's note wording, "engine cannot read a record list", to name the actual missing check | spec/tests.md:210, spec/tests.md:220 |
| FND-004 | medium | FR-011-AC-4 / TC-138 is a manual inspection of a worked example pairing a record with a quoin FR-046 disposition fact, but the PR ships no such example, so no reviewer can perform the inspection. Add the worked example (for example in the skeleton comment or a doc), keep TC-138 🚧 until it is inspected, and say so in the note | spec/functional/FR-011-soup-risk-disposition.md:68, spec/tests.md:225 |
| FND-005 | low | spec/tests.md requirement-coverage rows FR-009..NFR-001 still read "🚧 specified by PLAT-1512; the tests land with the schema and manifest work". The "targets it cannot back are exactly..." paragraph does not list TC-123/TC-133/TC-138 or FR-009-AC-3, FR-010-AC-5, FR-011-AC-4, FR-011-CON-1. The "rows that stay 🚧 need an environment or a human" paragraph does not cover engine gaps | spec/tests.md:43-60, spec/tests.md:111-115 |
