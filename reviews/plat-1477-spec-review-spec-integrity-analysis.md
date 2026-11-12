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
