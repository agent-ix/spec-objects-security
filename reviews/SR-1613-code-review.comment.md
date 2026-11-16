<!-- reviewer repo=agent-ix/spec-objects-security visibility=public quoin=0.35.0 module=spec-objects-security@9bf425fc id=SR-1613 method=code-review lang=py pr=spec-objects-security#65 model=gpt-6.1-sol run=3548c9d2-949f-427a-9f73-a76ca26647b9 -->

| FND | Severity | Check | Summary |
| --- | --- | --- | --- |
| FND-001 | high | soundness | The new _extract helper duplicates tests/test_regulated_categories.py::_extract: it loads schema documents, composes module mappings and source identity, then invokes extract_semantic with dataSchema and bodyExtraction. This creates two implementations that can drift; reuse or generalize the existing helper. |

+++ [reviewer data]

```yaml
clean: false
scope:
- id: tests/test_trust_boundary.py::_extract
  path: tests/test_trust_boundary.py
  role: examined
  excerpt: Semantic extraction helper loads schemas and invokes extract_semantic with
    the module mappings, source identity, data schema, and body extraction.
- id: tests/test_regulated_categories.py::_extract
  path: tests/test_regulated_categories.py
  role: context_only
  excerpt: Existing helper performs the same semantic extraction setup with schema
    documents, module mappings, source identity, and bodyExtraction.
findings:
- fnd: FND-001
  severity: high
  confidence: high
  method: code-review
  check: soundness
  artifact_id: tests/test_trust_boundary.py::_extract
  related_ids:
  - tests/test_regulated_categories.py::_extract
  path: tests/test_trust_boundary.py
  lines: 20-42
  excerpt: The trust_level frontmatter extraction path has separate coverage in test_trust_boundary.py.
  finding: 'The new _extract helper duplicates tests/test_regulated_categories.py::_extract:
    it loads schema documents, composes module mappings and source identity, then
    invokes extract_semantic with dataSchema and bodyExtraction. This creates two
    implementations that can drift; reuse or generalize the existing helper.'
bindings: []
```

+++