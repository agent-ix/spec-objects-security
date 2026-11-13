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

## New findings (disposition pass 1)

Checked at c6ee512. `quire validate --scope . "spec/**/*.md"` now exits 3.

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-004 | high | `spec/tests.md` fails `quire validate` (exit 3): the Status cell of TC-116, TC-118, TC-120 and TC-146..TC-149 is empty, and the TestMatrix schema requires one of ✅ ❌ 🚧 ⛔ | spec/tests.md:210,212,214-218 |
| FND-005 | medium | FR-008-AC-6 is reused with a new meaning (a `risk` edge clears the finding) instead of a new id; `tests/test_reverse_mitigates.py:142` still tags TC-120 (exposure-end `to: []`) to FR-008-AC-6, so the matrix credits the risk-edge criterion to a test that does not assert it | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:85; tests/test_reverse_mitigates.py:142 |
| FND-006 | low | TC-149 (threat in a repository not named by `--repo`) lists FR-008-AC-10 (exposure-end `to: []`), which it does not test; TC-120 already backs AC-10 | spec/tests.md:218 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | TC-116 now reads `to: [threat, risk]` (c6ee512) |
| FND-002 | fixed | TC-118 now covers a same-repository threat; TC-147..TC-149 cover the cross-repo, wrong-kind and unloaded cases (c6ee512) |
| FND-003 | fixed | New FR-008-AC-6 and TC-146 cover a `risk` edge (c6ee512) |
