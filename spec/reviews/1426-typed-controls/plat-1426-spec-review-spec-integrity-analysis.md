---
id: SR-041
title: "Spec integrity review of PR #49 control clause references and scope exclusions"
type: SpecReview
analysis: integrity
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-004-role-schemas.md, spec/functional/FR-014..FR-018, spec/non-functional/NFR-003-clause-references-state-and-never-derive.md, spec/functional/index.md, spec/non-functional/index.md (PR #49, git diff origin/main...HEAD at d3658e0)"
---
# SR-041: Spec integrity review of PR #49 control clause references and scope exclusions

## Summary

Ticket: PLAT-1426. Spec-only PR. It adds FR-014 to FR-018 and NFR-003 and edits
the `ControlMapping` bullet of FR-004. The companion is quoin#871 (FR-171 to
FR-174, NFR-038).

What was measured, with quire 0.44.0 (engine 0.59.1) and quoin 0.30.1:

- `quire validate --scope . --summary 'spec/**/*.md'` exits 0, and 71 of 71 docs
  are grammar-clean. `--okf --strict` exits 3, but only on findings that are
  already on main (tests.md dangling traces, unowned quality characteristics,
  the FR-004 `Mystery` example). None of them is in a file this PR adds.
- Id collisions: none. FR-014..FR-018 and NFR-003 are absent on main and in
  spec-objects-security#48, which adds FR-020, FR-021 and NFR-002. quoin
  FR-171..FR-174 and NFR-038 are absent on quoin main and in every other open
  quoin PR. Both PRs append to `spec/functional/index.md` and
  `spec/non-functional/index.md` after the same lines, so whichever lands
  second gets a trivial textual conflict.
- No standard text and no roadmap content. The new files name only the
  synthetic `example.invalid/std@1`.
- The author said FR-015 relies on quire-rs FR-083 for clause-set resolution.
  Checked on quire-rs main, FR-083 exists but does not do this (FND-003).

## Verdict

**FAIL**: four high findings, one medium and one low. The count statements
that FR-017 claims to update are unchanged. FR-014's extraction of the
`## Mappings` table conflicts with FR-003's fixed `mappings` list. The four new
Quire diagnostics in FR-015 and FR-018 have no engine owner. FR-004 is the only
existing requirement this PR edits, and its `ControlMapping` bullet is
consistent with FR-014. FR-016, the NFR-003 statement and the index entries
are clean.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-017 says that `scope_exclusion` is the twenty-fifth type, so "the counts of FR-003 through FR-006 include it" and "it has a role-schema row". The PR amends none of them. FR-003 Behavior still lists exactly twenty-four exports, and FR-003-AC-1/AC-4 still say "twenty-four". FR-004 Outputs say "Twenty-four object-type models", and the role table has no `scope_exclusion` row (no Model, required keys or item rules). FR-004-CON-2, AC-1 and AC-11 say twenty-four. So do FR-005-AC-1 and AC-7, and FR-006 Behavior and AC-4. So do spec.md Scope ("The 24 tier-2 ObjectTypes"), US-001 and IT-002. Implementing FR-017-AC-1 (`scope_exclusion` in `exports`) makes FR-003-AC-1 false. This is the same defect as PLAT-1512 SR FND-001 for `soup_record`, which was fixed by amending each statement | spec/functional/FR-017-scope-exclusion-object.md:27-29, spec/functional/FR-003-semantic-manifest-contract.md:47, spec/functional/FR-003-semantic-manifest-contract.md:68-69, spec/functional/FR-004-role-schemas.md:34, spec/functional/FR-004-role-schemas.md:61-81, spec/functional/FR-004-role-schemas.md:106, spec/functional/FR-004-role-schemas.md:112, spec/functional/FR-004-role-schemas.md:122, spec/functional/FR-005-executable-skeletons.md:81, spec/functional/FR-005-executable-skeletons.md:87, spec/functional/FR-006-security-safe-declarations.md:59, spec/functional/FR-006-security-safe-declarations.md:85, spec/spec.md:28, spec/usecase/US-001-declare-security-objects-against-semantic-core.md:22, spec/integration/IT-002-quoin-module-install.md:60 |
| FND-002 | high | FR-014 requires "The extractor SHALL read the `## Mappings` typed table into `mappings`" (AC-3). The engine reads a section into a record key only under quire-rs FR-081 record-sections, and FR-081 runs only when the module's `semantic.mappings` names `record-sections`. FR-003 Behavior fixes that list as exactly `[typed-table, sysml-fence, ocl-clause]`, and the manifest matches it. FR-004 Behavior still lists `mappings` among the keys "the current extractor does not populate". FR-014 does not cite FR-081 and amends neither FR-003 nor FR-004, so FR-014-AC-3 contradicts FR-003-AC-1 as written | spec/functional/FR-014-control-mappings-are-clause-references.md:43, spec/functional/FR-014-control-mappings-are-clause-references.md:53, spec/functional/FR-003-semantic-manifest-contract.md:46, spec/functional/FR-004-role-schemas.md:94, spec_objects_security/manifest.yaml:36 |
| FND-003 | high | FR-015 states three engine behaviours: "Quire SHALL report" `control-mapping-clause-unresolved` and `control-mapping-duplicate`, and stays silent for a set that is not loaded. No quire-rs requirement owns them, and FR-015 names no module-declarative mechanism. FR-013, by contrast, grounds its finding in quire-rs FR-058 `required_relations`. The `references` edge to quire-rs FR-083 does not supply resolution. Checked on quire-rs main, FR-083 only declares a manifest `clause_sets` list and `check_publishable`, and no quire-rs FR mentions control mappings. "Loaded clause set" is also undefined. It could mean a set declared by any module discovered under `--scope`, or a licensed pack installed in `IX_HOME` (quoin FR-137). These are different populations, and FR-015-AC-1/AC-3 depend on which. Name the owning engine requirement or ticket, or a declarative manifest rule, and define "loaded" | spec/functional/FR-015-mapping-resolution-and-duplicates.md:24-27, spec/functional/FR-015-mapping-resolution-and-duplicates.md:42 |
| FND-004 | high | FR-018 states two cross-document Quire errors, `clause-mapped-and-excluded` and `scope-exclusion-duplicate`, computed over "the same corpus". It names no engine requirement and no manifest mechanism that can express a uniqueness or a mutual-exclusion rule across documents. No quire-rs FR provides one. quoin#871 FR-173 depends on this check, because `facts-from-mappings` exits non-zero "when a clause is both mapped and excluded". The quoin half also has no defined producer for the check | spec/functional/FR-018-mapped-and-excluded-contradiction.md:23-25 |
| FND-005 | medium | The FR-014 key and clause grammar does not match the quoin rule it cites. FR-014 attributes `authority/id@version` to quoin FR-133. FR-133 defines a storage path `discharge/<authority>/<id>/<version>/<clause>.json`, while the key form is stated by quoin FR-137 to FR-140. FR-133 also bounds each of the four ids to 1-64 bytes, refuses ids that fold to the same case (`case-collision`), and refuses ids outside the bound (`invalid-identifier`). FR-014 admits any non-empty part with no length bound. A mapping FR-014 accepts can therefore yield a fact that `record-discharge` refuses, through quoin FR-173. Cite the right requirement, and either bound the parts or state that FR-133's identifier rules apply | spec/functional/FR-014-control-mappings-are-clause-references.md:21, spec/functional/FR-014-control-mappings-are-clause-references.md:40-41 |
| FND-006 | low | FR-006 Behavior still lists `ControlMapping.doc` among the free-text carriers that the FR-005 credential scan gates. FR-014 removes `doc` from `ControlMapping`, so the bullet now names a property that no longer exists | spec/functional/FR-006-security-safe-declarations.md:57, spec/functional/FR-014-control-mappings-are-clause-references.md:42 |

## Dispositions

Round 1, checked against fix commit f61e87f and merge commit aa90516. The PR head is aa90516, which is current main (9d3c9e7) plus the PR. GitHub reports it `MERGEABLE`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Every count is now twenty-five or 25: FR-003 Behavior and FR-003-AC-1/AC-4; FR-004 Outputs, CON-2, AC-1 and AC-11; FR-005-AC-1 and AC-7; FR-006 Behavior and AC-4; spec.md; US-001; IT-002; and tests.md. FR-004 gains a `scope_exclusion` role-table row, and FR-003 `exports` names `scope_exclusion`. |
| FND-002 | fixed | FR-003 now fixes `mappings: [typed-table, sysml-fence, ocl-clause, record-sections]`. FR-014 depends on quire-rs FR-081, and FR-004:94 no longer lists `mappings` or `effectiveness` as unpopulated. Measured with the quire 0.58.0 wheel against a scratch copy of the module, after adding `record-sections` and a `{set, clause}` ControlMapping: `## Mappings` and `## Effectiveness` populate the record. An invalid set raises `semantic.record-invalid` at `mappings[0].set`, and an invalid effectiveness raises it at `effectiveness`. |
| FND-003 | fixed | The original FR-015 (resolution and duplicates) is deleted. FR-014 states that clause existence and repetition are checked by `quoin evidence facts-from-mappings`. quoin#871 FR-173 at 5d1878c2 refuses an unlisted clause and a duplicate mapping. |
| FND-004 | fixed | FR-018 is deleted. quoin#871 FR-173 at 5d1878c2 refuses a duplicate exclusion and a clause that is both mapped and excluded. |
| FND-005 | fixed | FR-014 now cites quoin FR-137 to FR-140 for the key form, bounds every part to 1-64 bytes per FR-133, and leaves case-collision to Quoin (FR-173). |
| FND-006 | fixed | FR-006:57 no longer lists `ControlMapping.doc`. |
