---
id: SR-040
title: "Spec review of PR #47 FR-013 and FR-010/FR-012 amendments"
type: SpecReview
analysis: base
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-013-soup-record-serves-requirement.md, spec/functional/FR-010-soup-record-fields.md (Behavior, AC-5), spec/functional/FR-012-soup-record-relations.md (Description, Behavior, AC-1, AC-3), spec/functional/index.md (PR #47, git diff origin/main...HEAD at 6ca3e61)"
---
# SR-040: Spec review of PR #47 FR-013 and FR-010/FR-012 amendments

## Summary

Ticket: PLAT-1598. This review covers the base review, EARS conformance and
integrity, inline, over the new FR-013 and the FR-010-AC-5 and FR-012 amendments.
`quire validate --scope .` exits 0 on all of them. FR-013 has the iso `fr.md`
skeleton's sections (Description, Inputs, Outputs, Behavior, Acceptance Criteria,
Dependencies), and its Behavior statements are EARS-conformant SHALL clauses.
Each one maps to an AC. The FR-012 amendments are consistent with FR-013:
`serves` is the record's only link, and the one required relation is outgoing.
The index entry is present.

Findings from other methods are not repeated here:

- the unregistered `serves` verb that contradicts FR-012 Behavior and FR-013
  Description (SR-038 FND-001)
- AC-7's missing `--repo`, the dropped trace/matrix AC and the FR-010-AC-5
  duplication (SR-039 FND-001..003)

## Verdict

**PASS with findings**: one medium and one low, both fixable in this PR.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | Two authorities now state which requirements a component serves. One is the FR-010 `serves` record field, which quoin's `soup report` (FR-144) reads. The other is the FR-013 `serves` relationship, which the completeness rule reads. FR-010 says only that the check does not read the field, and no requirement relates the two. The worked fixture served.md carries both, so they can drift silently: a record lists FR-100 in `serves:` and edges to FR-200, or lists nothing and has an edge. Fix: either make the relationship the single source (drop or derive the record field) or state the rule that relates them, and say which one the report shows | spec/functional/FR-010-soup-record-fields.md:24,45, spec/functional/FR-013-soup-record-serves-requirement.md:21-24, tests/fixtures/soup/served.md:10-20 |
| FND-002 | low | FR-013 Dependencies cites `agent-ix/quire-rs` FR-085 (cross-repository resolution), but the frontmatter `relationships` has no `depends_on` to it. FR-008, the precedent it follows, carries both FR-058 and FR-085 | spec/functional/FR-013-soup-record-serves-requirement.md:5-15,71 |
