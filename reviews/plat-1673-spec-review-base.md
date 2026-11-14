---
id: SR-060
title: "Base spec review — FR-008 test matrix"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-security; spec_objects_security/manifest.yaml, tests/test_reverse_mitigates.py, spec/tests.md, spec/functional/FR-008-security-nfr-needs-mitigation-target.md"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-008
    type: reviews
---
# SR-060: Base spec review — FR-008 test matrix

## Summary

Ticket: PLAT-1673; PR agent-ix/spec-objects-security#58 at frozen head `253c8cb26b0d87312131babf5132fb41ca2ce94a`. Reviewed unchanged FR-008 requirements, the changed TC-116..TC-120 and TC-146..TC-149 rows, and their test bindings. Requirement statements are owned by main; this PR changes evidence status only.

## Verdict

**CONDITIONAL** — FR-008-AC-5 is tagged and marked complete, but its test does not assert the specified strict exit code or promoted error severity.

## Coverage

Base review only: identifiers, acceptance-criterion coverage, test matrix status, and verification evidence. FR-008-AC-1..10 are present and each has a matching `Trace` binding in a non-ignored test. TC-116..TC-120 and TC-146..TC-149 each name the intended criterion. The manifest test verifies both incoming `to: []` relations. The FR-008 behavior, outputs, severity rules, and acceptance criteria were read as context; no requirement statement changed in this PR. No applicable AssuranceProfile document exists in the repository.

Examined requirement units:

- `FR-008-AC-1` (role: examined): The manifest declares one `required_relations` entry with `from: NFR`, `where` over `quality_attribute` with `values: [security]`, `edges: [mitigates]`, `to: [threat, risk]`, `direction: outgoing` and `check: unjustified-security-nfr`.
- `FR-008-AC-2` (role: examined): Over a bundle holding a `security` NFR with no `mitigates` edge, `quire validate --okf` exits 0 and yields exactly one `unjustified-security-nfr` finding, naming the NFR and the value `security`.
- `FR-008-AC-3` (role: examined): Giving that NFR a `mitigates` edge to a `threat` in the same repository removes the finding.
- `FR-008-AC-4` (role: examined): An NFR whose `quality_attribute` is not `security` and which has no `mitigates` edge yields no `unjustified-security-nfr` finding.
- `FR-008-AC-5` (role: examined): Under `--okf --strict` the finding is a warning and never an error; strict still exits 3 on warnings by design. `--severity trace:unjustified-security-nfr=error` promotes it and the run exits non-zero.
- `FR-008-AC-6` (role: examined): `threat-has-control` and `risk-has-treatment` still declare `to: []` in the manifest.
- `FR-008-AC-7` (role: examined): Giving that NFR a `mitigates` edge to a `risk` in the same repository removes the finding.
- `FR-008-AC-8` (role: examined): `quire validate --okf --repo o/a=<A> --repo o/b=<B> --module $M` over a fixture where the NFR in `o/a` has a `mitigates` edge to a `threat` in `o/b` yields no `unjustified-security-nfr` finding.
- `FR-008-AC-9` (role: examined): An NFR whose only `mitigates` edges target a `hazard` in the same repository still yields the `unjustified-security-nfr` finding.
- `FR-008-AC-10` (role: examined): An NFR whose only `mitigates` edges target a `threat` in a repository not named by any `--repo` still yields the finding.

The FR-008 TC rows all changed to `✅`; TC-119's complete evidence is incomplete because the assertion checks warning text and nonzero promotion, but not the two explicit outcomes in AC-5.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | medium | TC-119 does not assert the strict-mode exit code 3 or that explicit severity promotion produces an error. | tests/test_reverse_mitigates.py:207-215 | correct-requirement-no-evidence |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | The test now checks strict-mode status 3 and the promoted error summary and severity. |
| FND-001 | fixed | Rechecked on head `2808f4385a2cbcef56b3d39668f1213b457f6183`; both severity assertions remain in the test. |

After excerpt (verbatim):

```python
assert strict.returncode == 3, strict.stderr
assert "1 OKF bundle validation error(s)" in promoted.stderr, promoted.stderr
assert not promoted_findings[0].startswith("warning:"), promoted.stderr
```

After excerpt (round 2, verbatim):

```python
assert strict.returncode == 3, strict.stderr
assert "1 OKF bundle validation error(s)" in promoted.stderr, promoted.stderr
assert not promoted_findings[0].startswith("warning:"), promoted.stderr
```
