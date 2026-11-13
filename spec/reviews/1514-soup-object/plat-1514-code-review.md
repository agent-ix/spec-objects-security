---
id: SR-032
title: "Code review of PR #45 soup_record object type"
type: SpecReview
analysis: code-review
review_set: subset
scope: "agent-ix/spec-objects-security; spec_objects_security/manifest.yaml, spec_objects_security/schemas/{SoupRecord,Anomaly,PurlField,SoupSupportStatus}.json, spec_objects_security/skeletons/soup_record.md, typespec/main.tsp, tests/test_soup_record.py, tests/conftest.py, tests/test_manifest_semantic.py, tests/test_role_schemas.py, tests/test_security_rules.py, tests/test_skeletons_semantic.py, spec/tests.md (PR #45, git diff origin/main...HEAD at 07788e5; spec/reviews/1512-soup-record/ excluded)"
---
# SR-032: Code review of PR #45 soup_record object type

## Summary

Ticket: PLAT-1514 (PR #45). The PR adds the `soup_record` object type
(TypeSpec model, emitted `SoupRecord`, `Anomaly`, `PurlField` and
`SoupSupportStatus` schemas, manifest export and `body_extraction`, skeleton),
adds `soup_record` to `vulnerability.allowed_links.affects`, and adds
`tests/test_soup_record.py` (22 tests, TC-121..TC-145 minus TC-123, TC-133, TC-138).

Measured: `tests/test_soup_record.py` plus the five touched test modules give
62 passed, 1 xfailed (the existing FR-003-AC-6 xfail). `node
scripts/generate-schemas.mjs --check` reports 51 schemas matching the committed
output. Engine: `node_modules/.bin/quire` 0.43.0 (engine 0.58.0), and PATH
quire 0.44.0 (engine 0.59.1) for the cross-check. The sealed schema refuses every
key FR-009, FR-011 and FR-012 name, as tested on hand-built records. No digest,
pin, ledger, vendored file or derived score field was added. The count bumps
(exports 23 to 24, role schemas 23 to 24, skeletons 26 to 27, primary skeletons
23 to 24) are correct for one new type plus its skeleton.

Reproduced against the shipped module with `validate_document`: a `soup_record`
document whose frontmatter carries `support_status: bogus_status`,
`end_of_support: soon`, `digest: "sha256:00"` and `severity: high` returns
`is_valid: True` with no errors. Removing the `purl` frontmatter key or the
`purl` Properties row does fail. Directory-mode `quire validate --okf` exits 0 for
all three documents, the broken ones included.

## Verdict

**FAIL**: one high finding. The schema is correct and sealed, but none of its
refusals reach an authored document, so ticket AC-2 ("validates with `quire
validate`") holds for any record at all. Several "emits" assertions check the
test's own input dict. All of it can be fixed in this PR: tests, `spec/tests.md`
status notes, and one engine gap to route.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | An authored soup_record document's record keys are never checked against SoupRecord.json: frontmatter `support_status: bogus_status`, `end_of_support: soon`, `digest` and `severity` validate (validate_document is_valid True). FR-009/010/011/012 refusals exist only for hand-built dicts. No committed fixture carries version/serves/known_anomalies/support_status/end_of_support, so ticket AC-2 is met vacuously. Fix: commit such a fixture and assert it with validate_document; add an `xfail(strict=True)` test showing a bogus authored document must fail (repo precedent tests/test_manifest_semantic.py:88); route the engine gap (frontmatter record keys not projected into, or validated against, the data_schema) to terra:quoin:triage | tests/test_soup_record.py:1-7, spec_objects_security/manifest.yaml:623-641 |
| FND-002 | medium | TC-134 is marked ✅ but its test only checks that the regex matches a canary string and that the skeleton (which has no anomaly statement) is clean. No anomaly statement is scanned or refused, so FR-010-AC-6 is unbacked. Set it to 🚧 with an honest note (no shipped artifact carries an anomaly statement; scanning authored records needs an engine lint), or run the scan over a real negative fixture that carries `known_anomalies` | tests/test_soup_record.py:187-193, spec/tests.md:221 |
| FND-003 | medium | The "emits"/"adds no key" halves assert on the test's own input dicts, which jsonschema never mutates. They cannot fail: TC-125 `absent == before`, TC-130 `"known_anomalies" in empty`/`empty != absent`, TC-136 `absent == before`, TC-139 `stripped == plain`, TC-124 `other["purl"] != record()["purl"]`. Assert over extract_semantic output (as TC-145 does), or mark the emission half 🚧 under FND-001's engine gap | tests/test_soup_record.py:91-110, 158-167, 203-209, 227-233 |
| FND-004 | low | TC-122 drops the top-level purl and the purl row together, so it cannot tell which one is enforced. It never exercises the document path, where a missing `purl` frontmatter key is a real engine error. Add: top-level purl with no purl row fails, and validate_document of the skeleton without `purl:` fails naming `purl` | tests/test_soup_record.py:82-87 |
| FND-005 | low | TC-141/TC-142 use directory-mode `quire validate --okf`, which exits 0 for a soup_record missing its required `purl`. TC-142 ("validates with no finding") therefore also passes for an invalid record. Pair it with validate_document of the same file, or assert on a check that dir mode actually runs | tests/test_soup_record.py:297-312, 359-365 |
| FND-006 | low | The `end_of_support` pattern admits impossible dates such as `2027-02-31`, and FR-010 says "a calendar date" | spec_objects_security/schemas/SoupRecord.json:59-62, typespec/main.tsp:800 |
| FND-007 | low | Hard-coded counts are redundant or inventory-only: `len(exports) == 24` follows an exact list equality with OBJECT_TYPES, and `len(paths) == 27` / `len(primary_skeletons()) == 24` are inventory counts that every new type has to bump. Derive them from OBJECT_TYPES or drop them | tests/test_manifest_semantic.py:46, tests/test_skeletons_semantic.py:74, tests/test_skeletons_semantic.py:224 |
| FND-008 | low | The module docstring names FR-009, FR-012 and NFR-001, and `quire matrix` emits three `trace-id-outside-marker` warnings for it | tests/test_soup_record.py:1 |
