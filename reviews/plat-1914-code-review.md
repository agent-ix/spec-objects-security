---
id: SR-20261116045026
title: "Code review — authored threat judgments"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-security; PLAT-1914; tests/test_threat_model.py; tests/test_threat_model_rules.py; NFR-005"
review_set: subset
---

## Summary

Reviewed PR #84 at 6ef2accb12530065b0a82e0fd1a4413bdebc4e61 for PLAT-1914. Three medium test-evidence gaps remain despite the focused nine-test run passing. Tests pin schema defaults and missing-decision validation, but do not fully check absence of generated records, edges or scores.

## Verdict

**CONDITIONAL** — add assertions over complete output records, facts and edges before claiming all five criteria closed.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The crossing test checks input filenames and denials, but never asserts the absence of threat/risk facts or considers edges in the returned report. Injecting invented threat and risk facts plus a considers edge into real Quire output leaves all nine focused tests passing. Assert the returned fact populations and threat-model edges, not only unchanged source files. | tests/test_threat_model_rules.py:401 |
| FND-002 | medium | The extraction test inspects records[0] only. Appending an invented risk record containing likelihood, impact, decision and decided_by to real extraction output leaves the test passing. Check the complete record population and assert that no unauthored records or judgment fields appear. | tests/test_threat_model_rules.py:454 |
| FND-003 | medium | The no-score test checks only schema property names and rule input fields; it never examines an actual output. Injecting score=999 into the extracted record and a risk fact leaves all nine focused tests passing. Exercise risk output and assert the absence of computed scores; keeping score out of the schema alone does not establish the output obligation. | tests/test_threat_model_rules.py:416 |

## Reviewed units and bindings

```yaml
scope:
- id: NFR-005-AC-1
  path: spec/non-functional/NFR-005-threats-ratings-and-acceptance-are-person-authored.md
  role: examined
  excerpt: '`ThreatModel.json`, `Threat.json` and `Risk.json` carry no `default` for
    `method`, `reviewed_by`, `decision`, `decided_by`, `likelihood` or `impact`, and
    no manifest entry has an `assert` or default value for any of them.'
- id: NFR-005-AC-2
  path: spec/non-functional/NFR-005-threats-ratings-and-acceptance-are-person-authored.md
  role: examined
  excerpt: A corpus in which a `connection` that carries a `data_classification` and
    crosses a `trust_boundary` is covered by a `threat_model` that considers no threat
    produces no `threat`, no `considers` edge and no `risk` record; of the three threat-model
    checks the only finding is `trace:crossing-without-threat` (starter rules of FR-025
    are not counted).
- id: NFR-005-AC-3
  path: spec/non-functional/NFR-005-threats-ratings-and-acceptance-are-person-authored.md
  role: examined
  excerpt: A `risk` with `likelihood` and `impact` stated and no `decision` fails
    validation; no rule reads `likelihood` or `impact`, and no output carries a computed
    score.
- id: NFR-005-M-1
  path: spec/non-functional/NFR-005-threats-ratings-and-acceptance-are-person-authored.md
  role: examined
  excerpt: '`default` keywords for `method`, `reviewed_by`, `decision`, `decided_by`,
    `likelihood` or `impact` in emitted schemas; target 0, threshold 0; method Test.'
- id: NFR-005-M-2
  path: spec/non-functional/NFR-005-threats-ratings-and-acceptance-are-person-authored.md
  role: examined
  excerpt: Threat, `considers`, rating, `decision` or `decided_by` keys in an extracted
    record that the author did not write; target 0, threshold 0; method Test.
bindings:
- test_id: test_threat_and_risk_fields_have_no_schema_or_manifest_defaults
  ac_id: NFR-005-AC-1
  trace: correct
- test_id: test_threat_and_risk_fields_have_no_schema_or_manifest_defaults
  ac_id: NFR-005-M-1
  trace: correct
- test_id: test_risk_document_decision_rules
  ac_id: NFR-005-AC-3
  trace: correct
```

## Evidence

- Independent focused pytest: all four new test functions and the five `test_risk_document_decision_rules` parameter cases passed (9/9). Python 3.13 environment `/home/peter/.cache/pypoetry/virtualenvs/spec-objects-security-T3mNusng-py3.13/bin/pytest`; `-o addopts='' -q` selects focused checks without whole-project coverage/report artifacts.
- Negative-control probe: temporary external CLI wrapper `/tmp/reviewsecurity84/bin/quire` delegates to real Quire 0.52.0 and then injects a threat fact, risk fact, considers edge, computed score, and an additional extracted risk record with invented judgment fields. The identical focused nine-test selection still passed (9/9). No repository source or tests were edited. This is a reviewer oracle-strength probe, not production evidence.
- Independent Ruff and Black checks passed on both changed files; diff whitespace check passed.
- Explicit released `/tmp/regfinish-quoin-v0.37.0/quoin matrix --repo . --json` passed. All five target criteria are statically tagged; tags do not remove the behavioral gaps above.
- Authoring contract fetched with explicit Quoin 0.37.0; module spec-artifacts-process@v0.36.0; validator `/home/peter/.npm-global/bin/quire` 0.52.0 (engine 0.62.2).
- Related implementation inspected: emitted ThreatModel/Threat/Risk schemas and rating refs; manifest extraction declarations and flow rules; risk skeleton with authored likelihood and impact; validation and isolated-flow helpers.
- No production, spec, plan or dependency changes occur. Only code-review applies; Rust/React lanes, gap-analysis and spec-review do not apply.
- No applicable AssuranceProfile was found under spec/. Exact model identifier is not exposed by the harness; marker uses model=unknown.

## Environment limits

The focused run uses the local architecture fixture at `/home/peter/dev/worktrees/regfinish-matrix-spec-objects-architecture/spec_objects_architecture`, configured through PLAT1658_ARCHITECTURE_MODULE and an ignored node_modules symlink for the flow helper's hard-coded path. The cached semantic-core symlink is 0.4.3 whereas committed schema refs name 0.4.4; none of these nine tests uses schema_registry, so this does not invalidate this focused result and does not establish schema-registry compatibility. Quire CLI tests use PATH because no local CLI exists. No full-suite result is claimed.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Returned facts now assert empty threat/risk lists and absence of considers edges across every returned record. |
| FND-002 | fixed | Extraction now requires exactly one record and exactly the authored scopes edge. |
| FND-003 | fixed | A real Risk skeleton extraction checks literal likelihood, impact and decision, and rejects a score key. |

## Disposition pass 1

**PASS; mergeable=yes** at f2b186aa2afc7380fccbecfa8ac8bbd8e012d7c3. Inspected every change since the reviewed head, including the copied original SR artifact and the new criterion-tagged risk extraction test. All three findings are fixed; no new findings.

Independent focused Python 3.13 run: 10 passed. Replaying the original external-output mutation probe against the three affected tests now fails all three, as expected. A separate score-only wrapper confirms the new risk extraction test fails specifically on the injected score key. These probes modify only temporary wrapper files, never repository source. Ruff and Black passed for both changed test files; diff whitespace check passed. Tool selection remains explicit Quoin 0.37.0 and Quire 0.52.0 (engine 0.62.2); fixture and dependency limitations remain as documented above. The five examined units now have meaningful coverage for the reviewed obligations.

Fixed excerpt FND-001:

```python
    facts = report["facts"]
    assert facts["threat"] == []
    assert facts["risk"] == []
    assert not any(
        edge["edge"] == "considers"
        for records in facts.values()
        for record in records
        for edge in record["edges"]
    )
```

Fixed excerpt FND-002:

```python
    assert len(extraction_output["extraction"]["records"]) == 1
    assert extraction_output["edges"] == [{"target": "CONN-1", "type": "scopes"}]
```

Fixed excerpt FND-003:

```python
    assert len(payload["records"]) == 1
    record = payload["records"][0]
    assert record["likelihood"] == "possible"
    assert record["impact"] == "major"
    assert record["decision"] == "undecided"
    assert "score" not in record
```
