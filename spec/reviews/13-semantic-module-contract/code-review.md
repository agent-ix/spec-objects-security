---
id: SR-010
title: "Code review of the #13 semantic module contract implementation"
type: SpecReview
analysis: code-review
scope: "tests/, tests/conftest.py, tests/fixtures/, scripts/generate-schemas.mjs, scripts/stage-npm.mjs, typespec/main.tsp, spec_objects_security/manifest.yaml, spec_objects_security/schemas/, spec_objects_security/skeletons/, spec/tests.md"
review_set: all
---
# SR-010: Code review of the #13 semantic module contract implementation

## Summary

Code review of branch `spec/13-semantic-module-contract` against `origin/main`:
the Python suite (`tests/conftest.py` plus nine test modules, 213 collected),
the Node emitter `scripts/generate-schemas.mjs`, `typespec/main.tsp` and its 47
emitted schemas, `manifest.yaml`, 26 skeletons, and the baseline and negative
fixtures. `spec-objects-business` was used as the peer style reference; the two
repositories share a Makefile, a poe task set and a test layout, and this
module's suite is the stricter of the two.

The gates run clean. `make lint` passes (ruff, black, and
`generate-schemas.mjs --check` reporting 47 schemas matching the committed
output). `make test` reports **211 passed, 2 xfailed, 0 skipped** at 100 %
coverage with `filterwarnings = ["error"]`. Both `xfail`s are `strict=True` and
name a live issue (`agent-ix/quire-rs#391`; `agent-ix/quire-rs#221` and
`#394`). No `pytest.skip`, no swallowed exception, and no narrowed gate was
found: the suite deliberately **fails** rather than skips when the Quire wheel
is absent (`tests/conftest.py:require_quire`), which is the disposition of
`agent-ix/spec-objects-security#10` and is honoured everywhere.

Trace-tag binding is clean. All 79 `@pytest.mark.trace` markers are single-line
(black leaves none wrapped), every bare `TC-` id in a docstring sits on a symbol
that already carries the matching marker, and no marker sits on a module
docstring or a plain helper. `quire coverage --scope <worktree>` reports
131/145 rows backed (90 %), `python: 79/79/81 bound/tagged/candidates`, and
emits **no** `tag-on-non-binding-symbol`, `marker-form-mismatch` or
`hollow-denominator` diagnostic. It does emit `status-column-matches-nothing`
(FND-304) and lists eight unbacked Manual/Integration rows (FND-312).

The generator is sound on the two properties that matter: `--check` writes
nothing (`check()` only reads; `write()` is unreachable from the `--check`
branch, and the compile scratch is an `mkdtemp` outside the tree removed in a
`finally`), and emission is deterministic (`readdirSync(...).sort()`, an
insertion-ordered `Map`, a stable two-space render, digests over the rendered
bytes).

**The defaulted-field rule was verified independently**, by building records by
hand against `spec_objects_security/schemas/` with `jsonschema` and
`referencing` rather than by reading the tests. Three results:

1. The schemas are *correct*. All seven declared refusing types (`Secret`,
   `EncryptionKey`, `JwtClaim`, `CsrfToken`, `MfaMethod`, `AuthFlow`,
   `AuditEvent`) reject a well-formed defaulted `FieldDecl`
   (`{"kind": "semantic", "value": …}`) and, where they admit `operations`,
   reject a defaulted `operations[].params[]` entry, while the same record
   without the default validates. No shipped schema carries a `default` in
   schema position at any depth (independent walk, `toolchain.json` excluded).
   FND-160 and FND-161 of SR-009 are genuinely discharged: the encoding is
   `items`/`not` and no file carries `minContains`/`maxContains`.
2. **The test that claims to prove this proves nothing** (FND-300). The record
   `tests/conftest.py:field()` builds is `default: {"kind": "literal", …}`, and
   semantic-core's `DefaultKind` is the closed set
   `["semantic", "representation", "migration"]`. `"literal"` is not a member,
   so the record fails `FieldDecl` inside semantic-core and never reaches the
   module's guard. Removing the entire `allOf` block from `Secret.json` leaves
   every negative assertion of TC-073 passing.
3. **The rule is absent from exactly the types where a default would grant
   something** (FND-301). A `Control` whose `effectiveness` row carries
   `default: effective`, a `TrustBoundary` whose `trust_level` row carries
   `default: trusted`, and a `Role` whose grant row carries a default all
   validate.

## Verdict

**FAIL** — two `high` findings: the acceptance test for the module's central
security rule passes for a reason unrelated to the rule (FND-300), and the
`default`-refusal is not applied to the granting rows the ticket's merge gate
names (FND-301). Everything else is `medium` or below and the toolchain,
generator, schemas and gate discipline are in good order.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-300 | high | TC-073's negative records are rejected by semantic-core `FieldDecl`, never by the module's `not: DefaultedField` guard: `field()` emits `default: {"kind": "literal", …}` and `DefaultKind` admits only `semantic`/`representation`/`migration`, so the record is malformed before the guard is consulted. Verified by deleting the whole `allOf` from `Secret.json` — every assertion of TC-073 still passes. FR-006-AC-4 and FR-006-CON-2 are therefore unverified, and the same defect makes the "clean" halves (`assert validator.is_valid(clean)`) the only assertions that exercise real behaviour. The guard itself is correct when driven with `kind: "semantic"` | tests/conftest.py:401, tests/test_security_rules.py:195, node_modules/@agent-ix/semantic-core/generated/json-schema/DefaultKind.json |
| FND-301 | high | `FieldDecl.default` is unguarded on the sixteen non-sensitive types, including exactly the rows where a default grants something. Independently confirmed against the shipped schemas: `Control` with `fields: [{name: effectiveness, default: {kind: semantic, value: effective}}]` validates; `TrustBoundary` with `trust_level` defaulted to `trusted` validates; `Role`, `Permission` and `Scope` accept defaulted grant rows. Issue #13's merge gate reads "No schema default grants permission, trust, or control effectiveness". SR-009 recorded that gate as met by reading it as the JSON Schema `default` keyword (TC-072); the declaration-level default reaches the same outcome and is unowned by any requirement | typespec/main.tsp:554, typespec/main.tsp:421, typespec/main.tsp:249, spec_objects_security/schemas/Control.json, spec/functional/FR-006-security-safe-declarations.md |
| FND-302 | medium | Vacuous assertion that can never fail: `assert "object:" not in frontmatter(text)` tests membership of the string `"object:"` in a parsed-YAML dict whose keys are `id`, `title`, `type` — `"object:"` with the colon is never a key under any input. The docstring says the property "is asserted here rather than assumed"; it is assumed. NFR-001-AC-4's stated precondition is unverified (the intended `"object" not in …` does hold for all 23 baseline skeletons) | tests/test_additive_compatibility.py:82 |
| FND-303 | medium | A `Manual`/🚧 matrix row reports as backed by an existence check. `TC-110` is authored in tests.md as `Manual`, "Quoin install roundtrip with state restore", yet carries a binding `@pytest.mark.trace("TC-110", "IT-002-SC-01")` on a test that asserts only that `manifest.yaml`, `skeletons/` and `schemas/` exist and that each `$id` ends with its file name. IT-002-SC-01 is "the pre-install `quoin module` listing is captured, including any existing entry" — none of which is exercised. The docstring is honest about being a precondition check; the marker is not, and quire consequently does not list TC-110 beside the other Manual rows it reports as minting no symbol | tests/test_quoin_install_roundtrip.py:26, spec/tests.md:190, spec/integration/IT-002-quoin-module-install.md:41 |
| FND-304 | medium | A coverage gate silently does not run. `quire coverage` reports `status-column-matches-nothing`: the `functional-coverage` declaration's configured status column is `Status`, and the table under "Functional Requirement Coverage" is headed `Coverage Status`. Status classification was skipped, so complete-but-unbacked rows could not be checked at all — the class of defect the sibling `hollow-denominator` rule exists to catch | spec/tests.md:81 |
| FND-305 | medium | The strict `xfail` carrying the second half of TC-103 has no `@pytest.mark.trace`, so the "the `object:`-declaring case is an expected failure" clause of the TC-103 row has no binding symbol. Taken with FND-302, the whole of NFR-001-AC-4 rests on one loop whose distinguishing assertion cannot fail and one untraced expected failure | tests/test_additive_compatibility.py:91 |
| FND-306 | low | `test_the_frozen_baseline_is_the_previous_module_version` is a load-bearing gate — it is what stops every NFR-001 criterion from comparing the manifest against itself, and it pins `version == 0.2.0` — but carries no trace marker and owns no matrix row, so a version bump breaks a test no requirement claims | tests/test_additive_compatibility.py:32 |
| FND-307 | low | Stale docstring contradicting the change's central policy: TC-013 reads "Skips when the installed quire wheel predates the markdown-default validator; quire is intentionally not a dependency of this pack." Nothing in that path skips any more — `_quire_doc_validator` calls `require_quire`, which calls `pytest.fail`. The module docstring twelve lines above and `conftest.py:10` say the opposite | tests/test_skeletons_and_validate.py:243 |
| FND-308 | low | TC-062's first assertion is vacuous when `@agent-ix/semantic-core` is not installed: `glob` over a missing directory yields an empty set, so `not (core & shipped)` holds trivially. Every other test that reads that directory fails loudly instead — `schema_registry` calls `pytest.fail` naming `npm ci` — so this is the one place where a missing toolchain reports green | tests/test_role_schemas.py:231 |
| FND-309 | low | The generator runs `tsp compile` with `stdio: "pipe"` and discards stdout and stderr on success, so any TypeSpec compiler warning is dropped silently. The repository treats warnings as errors on the Python side (`filterwarnings = ["error"]`) and has no equivalent on the emitter side; the diagnostics are only surfaced when the compile exits non-zero | scripts/generate-schemas.mjs:106 |
| FND-310 | low | Argument handling is `process.argv.includes("--check")` with no rejection of anything else, so a mistyped flag (`--chek`, `-check`) falls through to write mode and rewrites `schemas/` and `manifest.yaml` when the caller asked for a check. A CI step that typo'd the flag would report success having mutated the tree | scripts/generate-schemas.mjs:290 |
| FND-311 | low | `manifestWithDigests` leaves `pending` set when a `schema: schemas/<File>` line is not followed by a `digest:` line inside its own entry; the next `digest:` line anywhere later in the file is then rewritten with that schema's digest. Harmless on today's manifest (23 `schema:` lines, 23 `digest:` lines, one-to-one) but unbounded by construction, and the textual-rewrite design is what makes it silent | scripts/generate-schemas.mjs:216 |
| FND-312 | low | Coverage stands at 131/145 rows (90 %). Eight rows have no backing symbol — TC-015..TC-019 (needs a running filament-core), TC-046, TC-112, TC-113 (Manual) — and FR-001-AC-2, FR-001-AC-3, FR-001-AC-4 and FR-003-AC-5 have no verification symbol. All are declared `Manual`/`Integration` and marked 🚧 in tests.md, so this is disclosed rather than hidden; recorded so the gap is carried rather than closed by silence | spec/tests.md:121, spec/tests.md:148, spec/tests.md:190, spec/functional/FR-001-module-manifest-activates.md:35 |

## Dispositions

| ID | Disposition |
|----|-------------|
| FND-300 | Fix `tests/conftest.py:field()` to emit a `DefaultDecl` semantic-core accepts — `{"kind": "semantic", "value": …}` — so TC-073's negative records reach the module's guard. Add the canary the criterion needs: assert that the *base* record plus a well-formed default is refused **and** that the same record validates against a copy of the schema with its `allOf` removed, so the assertion cannot pass again for a reason unrelated to the rule. This is the same class of defect FND-161 named in SR-009 (a rule that reports green while a consumer reads it backwards); here it is the test rather than the schema. Belongs to #13 — reopen it rather than filing a new ticket |
| FND-301 | Decide and record which reading of the merge gate the module holds itself to. Either extend the `items`/`not` `DefaultedField` refusal to the granting rows — at minimum `Control.fields` (`effectiveness`), `TrustBoundary.fields` (`trust_level`) and the `Role`/`Permission`/`Scope` grant rows — as a marker model over the named row, with an FR-006 sentence and acceptance criterion; or state explicitly in FR-006 that a declaration-level `FieldDecl.default` on a graded row is admitted, why it does not constitute a grant, and which consumer obligation covers it. Do not leave FR-006 reading as though the seven sensitive types were the whole surface — that is precisely the shape SR-009's FND-160 disposition warned against |
| FND-302 | Change the assertion to `assert "object" not in frontmatter(text)`. The property holds for all 23 baseline skeletons today, so the fix is green immediately; it is the assertion, not the data, that is wrong. Add a canary so the check cannot silently become vacuous again — e.g. assert the mutated text used by the sibling `xfail` *does* carry the key |
| FND-303 | Either drop the `TC-110` marker so the row reads as Manual and unbacked, matching TC-046/TC-112/TC-113, and retag the test as its own precondition row; or rewrite tests.md so TC-110 is split into an automated precondition row and a Manual roundtrip row, and bind the marker to the precondition row only. Keep the `IT-002-SC-01` reference on whichever row actually captures the pre-install listing |
| FND-304 | Rename the `Coverage Status` header to `Status` in spec/tests.md, or align `traceability.status.column` with the authored header — the engine will not guess between those two change targets. Then re-run `quire coverage` and confirm the classification actually runs; a status gate that was skipped is worth nothing until it reports |
| FND-305 | Add `@pytest.mark.trace("TC-103", "NFR-001-AC-4")` to the strict `xfail`, so the expected-failure half the TC-103 row describes has a binding symbol and turns red visibly the day `agent-ix/quire-rs#391` ships |
| FND-306 | Mint a matrix row for the baseline-freeze gate (it verifies a deliverable NFR-001 depends on) and tag the test with it, or fold its assertions into TC-100 and delete the untagged function. Either way no gate in this suite should be untraced |
| FND-307 | Delete the two stale sentences from the TC-013 docstring and replace them with the fail-not-skip statement the module docstring already carries. A docstring that describes a skip in a change whose whole point is the removal of skips is the one place a future reader will look for permission to reintroduce one |
| FND-308 | Route TC-062 through the same `pytest.fail` path `schema_registry` uses when `SEMANTIC_CORE_DIR` is absent, or assert `core` is non-empty before intersecting. A one-line guard turns the only silent-green path in the suite into a loud one |
| FND-309 | Surface the compiler output. Capture stdout/stderr from the successful `tsp compile` and fail when it is non-empty (or when it matches a warning marker), so the emitter side matches the Python side's warnings-as-errors posture. If TypeSpec emits benign chatter, allow-list it explicitly rather than discarding the stream |
| FND-310 | Parse the argument list strictly: accept `--check` and nothing else, and exit non-zero naming the unknown flag. The failure mode being closed is "asked for a check, got a write", which no test can catch after the fact |
| FND-311 | Reset `pending` on any non-`digest:` line after a `schema:` line, and fail when a `schema: schemas/<File>` line has no `digest:` line in its own entry. Assert it: a fixture manifest with a `schema:` line and no following `digest:` must make the generator exit non-zero, not silently rewrite a later digest |
| FND-312 | No code change. Recorded and carried: every unbacked row is declared `Manual` or `Integration`, marked 🚧, and names its blocking dependency (a running filament-core; a Quoin built from `agent-ix/quoin` main at or after `3e842ce`). Re-check when those land, and keep the 90 % figure in the report rather than rounding it away |

### Round record (2026-09-04)

Applied in the fix round: FND-300 (the fixture built an invalid `DefaultKind`, so semantic-core refused the record before the module guard ran — `kind` is now `semantic`, and a canary asserts the defaulted `FieldDecl` is itself valid semantic-core, so the guard is what refuses it; falsified by deleting `Secret.json`'s `allOf`, which now fails the suite), FND-301 (the guard is now on all twenty-three types and their operation parameters, not the sensitive four — a `Control` with `effectiveness` defaulted to `effective` and a `TrustBoundary` with `trust_level` defaulted to `trusted` are now refused), FND-302 (`"object:" not in frontmatter(...)` could not fail; it tests the parsed key now), FND-303 (the precondition test no longer binds TC-110 or IT-002-SC-01; it has its own row, TC-114, and TC-110 is correctly unbacked again), FND-305 (the strict xfail carrying TC-103's second half now carries its marker).

Recorded without change, and carried into the report rather than silently closed: FND-304 (upstream: agent-ix/spec-artifacts-process#81 and #82), FND-306..FND-312.
