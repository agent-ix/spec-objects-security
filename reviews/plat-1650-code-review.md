---
id: SR-1613
title: "Code review of PLAT-1650 PR #66 default US and EU profiles"
type: SpecReview
analysis: code-review
review_set: subset
scope: "agent-ix/spec-objects-security; spec_objects_security/profiles/eu-device-gdpr-ai-act.yaml, spec_objects_security/profiles/us-device-cybersecurity-hipaa.yaml, tests/test_profiles.py (PR #66 at ffbf8fe7c7dade4d9d61f8af92300b554419eeb1), reviewed against FR-020, FR-021, NFR-002 and PLAT-1650 AC1-7"
---
# SR-1613: Code review of PLAT-1650 PR #66 default US and EU profiles

## Summary

Ticket: PLAT-1650. The change adds the two profile YAML files and extends the profile tests. The exact keys and versions match the released US and EU GitHub module tags. Both profiles omit `context`, so the profile does not bind product-specific dimensions. The tests install those modules through Quoin's supported `github:` source at their release tags, resolve each profile key against installed module manifests, and run `quire publish-check` against each declaring module. No upstream corpus or source module declaration is copied into this repository.

The focused suite passed: `poetry run pytest -o addopts= tests/test_profiles.py tests/test_clause_sets.py -q` → 45 passed. The repository's default pytest addopts could not run in this environment because pytest-cov and pytest-json-report options were unavailable; clearing those addopts allowed the focused test files to run successfully.

CLI review used Quoin 0.35.0 with a fresh module config, the released US/EU pack tags, and this PR's module tree. `quoin profile evaluate` exited 0 for web-app-baseline (2 evaluated, 0 unavailable), US (3 evaluated, 0 unavailable), and EU (4 evaluated, 0 unavailable). With the EU module omitted, selecting the EU profile still exited 0 and reported all four EU keys unavailable (0 evaluated, 4 unavailable). Missing product dimensions remain unresolved, as expected. Packaging configuration already includes every `profiles/*.yaml` file in wheel and sdist, and npm's package file list and staging script include `profiles/`; the new files therefore follow the existing package paths.

## Verdict

**PASS**: no findings. The profile names are among the three allowed names; keys use only authority, id and version; the US and EU profiles carry no product facts; and the selected public sources match FR-021's intended source table. The PR does not change the module manifest, source-module declarations, publish-check implementation, or packaging scripts.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |
