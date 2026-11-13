---
id: SR-039
title: "Gap analysis of PR #47 SOUP record serves edge"
type: SpecReview
analysis: gap-analysis
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-010-soup-record-fields.md, spec/functional/FR-012-soup-record-relations.md, spec/functional/FR-013-soup-record-serves-requirement.md, spec/tests.md, spec_objects_security/manifest.yaml, tests/test_soup_record.py, tests/test_manifest.py (PR #47, git diff origin/main...HEAD at 6ca3e61)"
---
# SR-039: Gap analysis of PR #47 SOUP record serves edge

## Summary

Ticket: PLAT-1598. Plan completion: not assessed (planless). The computed matrix
(`quoin matrix --repo . --json`, quoin 0.30.1) binds FR-013-AC-1..6 to one test
each. FR-013-AC-7 and FR-010-AC-5 have no binder.

Ticket ACs, measured at 6ca3e61:

- AC-1 (manifest declares the link; the target may be cross-repository) is met.
  `allowed_links.serves: [FR, NFR, StR]` is declared, but `serves` is an
  unregistered verb (SR-038 FND-001).
- AC-2 (a `required_relations` rule as data, no engine change, named check) is
  met. The diff touches no engine code.
- AC-3 (a fixture with the edge validates; one without it is reported) is met by
  TC-151/TC-152. TC-152's "in bundle" claim is weaker than it looks (SR-038 FND-003).
- AC-4 (`quire trace` / `quire matrix` show the edge) is NOT met. The coder's
  claim is verified: `quire trace --id FR-100` and `--id SOUP-011` return
  `resolved: false` on both 0.43.0 and 0.44.0, and `quire matrix` prints "No
  obligations matched this scope". `quire extract` lists the edge (TC-155).
- AC-5 (spec amendment via `quoin:specify`) is met in substance. FR-013 was written
  by hand, but its sections are a subset of the iso `fr.md` skeleton
  (`quoin write . --types FR`), and `quire validate` exits 0 on FR-010, FR-012,
  FR-013 and tests.md.

The coder's claim that `--repo` is missing is verified: neither quire 0.43.0 nor
0.44.0 has `quire validate --repo`. The TC-156 🚧 row is honest status, not
ceremony. The cross-repository case is the usual one, as FR-013's own
Description says.

## Verdict

**FAIL**: three medium dispositioning gaps. Each needs either a fix in this PR or a
properly linked ticket, not a note in the PR body.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | Ticket AC-4 ("`quire trace` / `quire matrix` show the edge from requirement to SOUP record") is unmet. The PR body says "this needs a quire-rs capability (PLAT-1519)", but PLAT-1519 covers frontmatter data_schema validation, purl uniqueness and absent list keys, not document-to-document edges in trace/matrix. PLAT-1598 has no relation to any ticket for it and no comment. FR-013 silently substitutes `quire extract` (AC-6), so the spec drops the ticket's AC. Fix: file the trace/matrix doc-edge capability with the quire-rs/quoin owner and link it to PLAT-1598, and state in FR-013 that trace/matrix display waits on that ticket. Otherwise get the AC explicitly dropped from the ticket | spec/functional/FR-013-soup-record-serves-requirement.md:55,66 |
| FND-002 | medium | FR-013-AC-7 / TC-156 needs `quire validate --repo`, which no shipped quire has (0.43.0, 0.44.0 measured). No ticket owns that capability: PLAT-1598 has no relation, and the 🚧 note names none. Until it exists, every real record whose requirement lives in the product repository warns, which is the usual case per FR-013 Description. The 🚧 row is honest, but it is not dispositioned. Fix: cite an owning engine ticket in the TC-156 note and link it to PLAT-1598 (check PLAT-1556 "Count cross-repo mitigates targets" first), or reword AC-7 to the mechanism that exists | spec/functional/FR-013-soup-record-serves-requirement.md:67, spec/tests.md:124,252 |
| FND-003 | medium | FR-010-AC-5 lost its only binder: the TC-133 strict-xfail test was deleted, and nothing is tagged FR-010-AC-5 or TC-133 (the computed matrix shows `binders: []`). spec/tests.md still marks TC-133 and the FR-010 row ✅ "discharged by TC-151 and TC-152". FR-010-AC-5 and FR-010 Behavior line 45 now restate FR-013-AC-2/3. Fix: delete FR-010-AC-5, its Behavior line and the TC-133 row, and point FR-010 at FR-013. Alternatively, tag TC-151/TC-152 with FR-010-AC-5 | spec/functional/FR-010-soup-record-fields.md:45,63, spec/tests.md:121,233 |
