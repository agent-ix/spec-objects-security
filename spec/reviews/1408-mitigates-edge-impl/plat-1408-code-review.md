---
id: SR-017
title: "Code review of PR #40 control mitigates admits hazard and failure_mode"
type: SpecReview
analysis: code-review
review_set: subset
scope: "agent-ix/spec-objects-security; spec_objects_security/manifest.yaml, tests/test_control_mitigates.py, spec/tests.md (PR #40 diff, git diff origin/main...HEAD at 75e7e48)"
---
# SR-017: Code review of PR #40 control mitigates admits hazard and failure_mode

## Summary

Ticket: PLAT-1408. Reviewed the one-line manifest widening of
`control.allowed_links.mitigates`, the new test module carrying TC-091 and
TC-092, and the TC-091/TC-092 status flip in `spec/tests.md`.

Focused run (Python 3.10 venv, quire CLI 0.40.0, engine 0.56.0): TC-091
passes. TC-092 fails with "spec-artifacts-iso is not installed and
SPEC_ARTIFACTS_ISO_MODULE names no checkout". It passes once
`SPEC_ARTIFACTS_ISO_MODULE` points at a local `spec_artifacts_iso/` package
dir. Running `quire validate --okf` by hand showed that the
`[disallowed-edge-target]` diagnostic naming `'asset'` is emitted with
`--module <package root>` alone. It is also emitted when the iso path is the
checkout root, which loads no edge vocabulary at all. So the iso module is not
load-bearing for FR-007-AC-2.

On the other reviewer's dependency question: `quire validate --module`
replaces ambient module discovery, so the test does not depend on installed
modules. The widened list comes from this repo's manifest via
`--module PACKAGE_ROOT`, not from the CLI. The reusable
`semantic-module-ci.yml` puts `@agent-ix/quire-cli@latest` on PATH, which is
enough.

## Verdict

FAIL: TC-092 fails in the repo's own CI environment, and its naming assertion
is not bound to the diagnostic it is meant to check.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | high | TC-092 hard-fails under CI. `_iso_module()` needs `spec_artifacts_iso` installed or `SPEC_ARTIFACTS_ISO_MODULE` set. `pyproject.toml` declares no spec-artifacts-iso (it was removed in PLAT-902 #19, in line with FR-003 Inputs), and `semantic-module-ci.yml` sets no such variable, so `poetry run pytest` fails TC-092 while `spec/tests.md` marks it done. The iso module is not needed, because the diagnostic fires with `--module PACKAGE_ROOT` alone. Fix: drop `_iso_module` and the iso `--module`. Do not re-add the dependency. | tests/test_control_mitigates.py:19-30, tests/test_control_mitigates.py:62-67, pyproject.toml:22-34 |
| FND-002 | medium | The naming half of FR-007-AC-2 checks `"'asset'" in result.stderr` anywhere in stderr. It is not tied to the `[disallowed-edge-target]` line. Without the iso module, an `UnknownEdgeType: archetype 'asset' allowed_links uses 'references'` load line satisfies it on its own, so a diagnostic that named the wrong type would still pass. Fix: select the `[disallowed-edge-target]` line and assert that it contains `(object type 'asset')`. | tests/test_control_mitigates.py:75-76 |
