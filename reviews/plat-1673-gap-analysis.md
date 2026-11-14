---
id: SR-059
title: "Gap analysis — FR-008 mitigation target constraint"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-security; spec_objects_security/manifest.yaml, tests/test_reverse_mitigates.py, spec/tests.md, spec/functional/FR-008-security-nfr-needs-mitigation-target.md"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-008
    type: reviews
---
# SR-059: Gap analysis — FR-008 mitigation target constraint

## Summary

Ticket: PLAT-1673; PR agent-ix/spec-objects-security#58 at frozen head `253c8cb26b0d87312131babf5132fb41ca2ce94a`. The computed matrix binds every FR-008 criterion to a test, and the changed tests exercise the manifest relation and the requested same-repository, cross-repository, wrong-kind, unresolved-target, alternate-quality-attribute, and severity paths.

## Verdict

**PASS** — no uncovered FR-008 criteria were found in the changed scope.

## Coverage

Plan completion: not assessed.

The changed manifest relation is owned by FR-008. Computed matrix records bind FR-008-AC-1..10 to tests in `tests/test_reverse_mitigates.py`; no criterion in this PR's scope is untagged or bound only to an ignored test. Tests execute the real `quire validate` path with installed ISO and security modules. No new stubs, skipped tests, or coverage threshold changes were found in the diff.

`quire matrix --strict` reports untagged criteria elsewhere in the repository, outside the PR diff and the requested review scope; those existing rows were not attributed to this PR. The strict matrix command exits 1 for those out-of-scope gaps. The optional semantic review was not requested and was skipped. No plan was supplied.

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

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |
