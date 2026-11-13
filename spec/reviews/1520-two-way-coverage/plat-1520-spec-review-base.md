---
id: SR-034
title: "Base spec review of PR #46 FR-008 constrained mitigation target"
type: SpecReview
analysis: base
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-008-security-nfr-needs-mitigation-target.md, spec/tests.md (PR #46 diff, git diff origin/main...HEAD at 60b5bab)"
---
# SR-034: Base spec review of PR #46 FR-008 constrained mitigation target

## Summary

Ticket: PLAT-1520 (PR #46). The PR amends FR-008 so the
`security-nfr-has-mitigation-target` relation declares `to: [threat, risk]`
and relies on quire-rs FR-085 (agent-ix/quire-rs#664, open) for
cross-repository resolution and FR-084 for the reverse coverage view.
Review set: subset (base, ears-conformance, integrity, dependency).
`quire validate --scope . "spec/**/*.md"` (quire 0.44.0, engine 0.59.1)
exits 0. No assurance profile is present in the repo.

Checked: ID formats (FR-008, FR-008-AC-1..6) unchanged and gap-free; no
hash, digest, pin, SHA, ledger or tracking record is introduced; no
paywalled standard text is quoted. The diff is symmetric with the safety
amendment (agent-ix/spec-objects-safety#35, FR-009) and its wording matches
FR-084/FR-085.

Coverage: the PR changes FR-008-AC-1 and FR-008-AC-3 but leaves the test
cases that back them describing the old behaviour, and AC-3 exercises only
one of the two kinds `to` now names.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | TC-116 still states the relation declares `to: []`, contradicting amended FR-008-AC-1 (`to: [threat, risk]`), and is marked passing | spec/tests.md:210 |
| FND-002 | medium | TC-118 still states an edge to any document in another repository yields no finding, contradicting amended FR-008-AC-3 (tests/test_reverse_mitigates.py:116 asserts the old behaviour); no TC covers AC-3's new negative clause (wrong-kind target, unloaded repository) | spec/tests.md:212 |
| FND-003 | medium | `to` names `risk`, but no criterion shows a `mitigates` edge to a `risk` satisfies the obligation; AC-3 covers `threat` only, so `to: [threat]` passes every AC except the literal AC-1 check | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:72 |

## Verdict

Changes requested (3 medium). The FR-008 text is otherwise coherent and
consistent with quire-rs FR-058/FR-084/FR-085.
