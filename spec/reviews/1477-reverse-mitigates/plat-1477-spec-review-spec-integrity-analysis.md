---
id: SR-026
title: "Spec integrity review of PR #43 FR-008 reverse mitigates"
type: SpecReview
analysis: integrity
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-008-security-nfr-needs-mitigation-target.md, spec/functional/index.md, spec/tests.md (PR #43 diff at 8f26af7)"
---
# SR-026: Spec integrity review of PR #43 FR-008 reverse mitigates

## Summary

Ticket: PLAT-1477 (PR #43). `quire validate --scope .` on the three changed
spec files exits 0. A whole-`spec/` OKF run, compared between origin/main and
the head, shows no new warning, only line shifts in `spec/tests.md`.

FR-008 is structured and atomic for AC-1 to AC-4. It agrees with quire-rs
FR-058 (read-only, origin/main) on four points:

- `where` narrows only the obliged side.
- Matching uses trim and case folding.
- A dangling edge does not satisfy a constrained `to`.
- The finding is advisory under both postures.

The index entry and the TC-116 to TC-119 rows are consistent with the AC
table. US-001 and StR-001 traces are extended to FR-008.

## Verdict

CHANGES REQUESTED on FND-001. The rest is sound.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | high | FR-008-AC-5 claims "without it `--okf --strict` still exits 0", and `spec/tests.md` marks TC-119 ✅. Measured with quire 0.43.0 (engine 0.58.0), both the test's fixture and a properly loaded iso exit 3 under `--okf --strict`. The first fails on an `unknown-type` NFR error. The second fails on iso's own `unowned-quality-characteristic` errors. The `unjustified-security-nfr` finding itself stays a warning, which is what FR-058-AC-18 promises. Restate the AC as "under `--okf --strict` the finding is reported as a warning", and assert that (SR-024 FND-001). | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:65, spec/tests.md:191 |
| FND-002 | low | The Description justifies `to: []` (a cross-repo threat cannot satisfy a constrained `to`) but does not state its cost. Any `mitigates` target satisfies the rule: measured, an NFR mitigating another NFR and an NFR mitigating a typo'd id (which only gets an advisory `dangling-reference`) both come back clean. iso `NFR.allowed_links` has no `mitigates`, so nothing constrains the target kind. The choice is defensible (FR-058 sanctions it, and the PLAT-1477 caveat anticipates it). Record the trade-off so a reader does not take a clean run as "traces to a threat or risk". | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:27-31 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-003 | low | Restated FR-008-AC-5 adds "a bundle whose only faults are these findings stays valid". No test checks that clause, and at the CLI it reads as exit 0, which is false. `quire validate --help` says `--okf --strict` "exits 3 on any finding". Measured with quire 0.43.0 (engine 0.58.0) and iso 0.25.0, the bundle exits 3 ("1 OKF bundle warning(s) (--strict)") even with iso's unrelated check switched off, so that this finding is the only fault. The sibling `uncontrolled-threat` behaves the same way. Either drop the clause or say what it means: the finding is not an error, and `--strict` still exits 3 on warnings. | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:69 |

## Dispositions

| FND | outcome | reason |
|-----|---------|--------|
| FND-001 | fixed | Verified on 1b45548. The false "`--okf --strict` still exits 0" claim is gone. FR-008-AC-5 and the TC-119 row state that the finding stays a warning under strict, and TC-119 asserts it. The remaining "stays valid" clause is recorded separately as FND-003. |
| FND-002 | fixed | Verified on 1b45548. FR-008 has a "What `to: []` lets through" section. It covers NFR-to-NFR edges, mistyped ids, cross-repo edges and iso's unconstrained `allowed_links`, and states that a clean run does not prove a threat or risk trace. |
