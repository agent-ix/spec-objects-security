---
id: SR-058
title: "Code review — FR-008 mitigation target constraint"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-security; spec_objects_security/manifest.yaml, tests/test_reverse_mitigates.py, spec/tests.md, spec/functional/FR-008-security-nfr-needs-mitigation-target.md"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-008
    type: reviews
---
# SR-058: Code review — FR-008 mitigation target constraint

## Summary

Ticket: PLAT-1673; PR agent-ix/spec-objects-security#58 at frozen head `253c8cb26b0d87312131babf5132fb41ca2ce94a`. Reviewed the manifest constraint, changed reverse-mitigation tests, and FR-008 matrix rows against FR-008-AC-1..10. The allowed target kinds and both loaded/unloaded cross-repository cases are covered; the severity test omits required exit/severity assertions.

## Verdict

**CONDITIONAL** — one medium test-evidence gap remains for FR-008-AC-5.

## Assurance Context

No applicable AssuranceProfile document exists in the repository.

## Coverage

Review set: subset. Python test review, duplication, integrity, test/spec alignment, and the changed declarative manifest behavior were examined. No Rust or React files are in the diff. Quoin matrix coverage for FR-008 shows all ten criteria tagged. The full matrix also reports unrelated untagged criteria outside this PR's scope; they are not findings against PR #58. No aggregate gate was run.

Examined requirement units (each is in the scope reviewed):

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

Other examined units: `spec_objects_security/manifest.yaml` (the exact `security-nfr-has-mitigation-target` relation and its explanatory comments); `spec/tests.md` rows TC-116..TC-120 and TC-146..TC-149; `tests/test_reverse_mitigates.py` tests bound to those rows.

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
