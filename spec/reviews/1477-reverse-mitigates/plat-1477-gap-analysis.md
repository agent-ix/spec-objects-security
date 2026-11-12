---
id: SR-025
title: "Gap analysis of PR #43 reverse mitigates rule for security NFRs"
type: SpecReview
analysis: gap-analysis
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-008-security-nfr-needs-mitigation-target.md, spec/tests.md, spec_objects_security/manifest.yaml, tests/test_reverse_mitigates.py, tests/test_manifest.py against PLAT-1477, PLAT-370 and quire-rs FR-058-AC-12..22 (PR #43 diff at 8f26af7)"
---
# SR-025: Gap analysis of PR #43 reverse mitigates rule for security NFRs

## Summary

Ticket: PLAT-1477, which closes PLAT-370. Plan completion: not assessed
(planless). `quire matrix --scope .` reports FR-008-AC-1 to AC-5 as all
tagged, at `tests/test_reverse_mitigates.py` lines 84, 96, 106 (AC-3 and
AC-4) and 122. The FR-007 status correction is accurate:
`tests/test_control_mitigates.py` tags TC-091 to FR-007-AC-1 and TC-092 to
FR-007-AC-2. Each new TC id appears once in `spec/tests.md`.

Measured against intent. The ticket text is treated as data. PLAT-1477 asks
for:

- `from: NFR`, where `quality_attribute` is security, `direction: outgoing`,
  `edges: [mitigates]`, advisory. All present.
- The cross-repo caveat to be handled. It is handled by `to: []`.

FR-058 sanctions `to: []` as "a reading a module opts into deliberately". The
safety counterpart (spec-objects-safety PR #32) makes the same choice.
Probes with real documents and the PR's manifest:

| Bundle | Result |
|---|---|
| security NFR, no edge | 1 finding naming the NFR and `'security'` |
| `mitigates` an in-bundle threat | clean |
| `ix://` edge to another repo | clean |
| `performance_efficiency` NFR | clean |
| `safety` NFR | clean |
| ` Security ` | selected |
| list value | not selected |
| `mitigates` another NFR | clean |
| `mitigates` a typo'd id | clean, with a separate advisory `dangling-reference` |

With `to: [threat, risk]`, the cross-repo NFR and the NFR-to-NFR edge are
both reported. The PR's stated reason for `to: []` is therefore accurate.
SR-026 FND-002 records the trade-off.

Single-file `quire validate` of an NFR with a `mitigates` edge warns that
the edge type "is not in the resolved allowed" set, because iso
`NFR.allowed_links` lacks `mitigates`. OKF bundle mode does not warn. This
matches the PR's known caveat.

## Verdict

PASS with gaps. Every AC is bound and live. One Behavior statement has no AC
and no test.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | medium | FR-008 Behavior says "The module SHALL NOT narrow the `to: []` of `threat-has-control` or `risk-has-treatment`". It has no AC and no test. Mutating `threat-has-control` to `to: [control]` leaves the suite result unchanged (same 175 passed and 6 node_modules-only failures as baseline). Either add an AC with a test asserting both relations keep `to: []`, or delete the statement, since it governs declarations FR-008 does not own. | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:55 |
| FND-002 | low | FR-008 Outputs says the finding names "the NFR, the declaration and the selector". TC-117 asserts only the NFR id and `'security'`. The engine output does name `security-nfr-has-mitigation-target` and `quality_attribute`, but no assertion pins them. | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:45, tests/test_reverse_mitigates.py:95-102 |

## Dispositions

| ID | Disposition |
|----|-------------|
| FND-001 | Fixed in round 1: FR-008-AC-6 and TC-120 assert `threat-has-control` and `risk-has-treatment` keep `to: []`. |
| FND-002 | Fixed in round 1: TC-117 asserts the finding names the declaration and the selector field. |
