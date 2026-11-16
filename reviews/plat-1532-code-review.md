---
id: SR-1613
title: "code-review review — PLAT-1532 spec-objects-security"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-security; tests/test_trust_boundary.py; tests/test_role_schemas.py"
review_set: subset
---

## Summary

The new _extract helper repeats the semantic extraction setup already implemented by tests/test_regulated_categories.py::_extract: loading all schema documents, composing module mappings, setting source identity, and calling extract_semantic with dataSchema/bodyExtraction. This creates two implementations that can drift. Reuse or generalize the existing extraction helper.

## Verdict

**FAIL** — a high-severity defect is present.

## Scope

- Examined: tests/test_trust_boundary.py; tests/test_role_schemas.py.
- Ticket: PLAT-1532; PR #65; reviewed head `9bf425fc3047401cccaa5fe45adfb76c0af75811`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The new _extract helper repeats the semantic extraction setup already implemented by tests/test_regulated_categories.py::_extract: loading all schema documents, composing module mappings, setting source identity, and calling extract_semantic with dataSchema/bodyExtraction | tests/test_trust_boundary.py:20-42 |

## Evidence

The `trust_level` extraction path has separate coverage in `test_trust_boundary.py`.

Observed finding: The new _extract helper repeats the semantic extraction setup already implemented by tests/test_regulated_categories.py::_extract: loading all schema documents, composing module mappings, setting source identity, and calling extract_semantic with dataSchema/bodyExtraction. This creates two implementations that can drift. Reuse or generalize the existing extraction helper.

## Examined Units

- `tests/test_trust_boundary.py::_extract` (examined): “Semantic extraction helper loads schemas and invokes extract_semantic with the module mappings, source identity, data schema, and body extraction.”
- `tests/test_regulated_categories.py::_extract` (context_only): “Existing helper performs the same semantic extraction setup with schema documents, module mappings, source identity, and bodyExtraction.”

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | The trust-boundary test now reuses the generalized `_extract` helper from `test_regulated_categories.py`. |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | The extraction logic is generalized in `test_regulated_categories.py::_extract`, and `test_trust_boundary.py` now reuses it with the trust_boundary schema and bundle. |
