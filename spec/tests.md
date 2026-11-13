---
id: TM-001
title: "spec-objects-security Test Matrix"
type: TestMatrix
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-001"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-002"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-003"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-004"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-005"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-006"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-007"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-008"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-009"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-010"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-011"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-012"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-013"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/NFR-001"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-020"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-021"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/NFR-002"
    type: covers
  - target: "ix://agent-ix/spec-objects-security/FR-017"
    type: covers
---
# Test Matrix

## Overview

This matrix is the verification contract for the module: the manifest
activation requirement (FR-001, issue #1 era, rows TC-001..TC-014) and the
issue #13 semantic module contract (US-001, FR-002..FR-006, IT-002).
Coverage is complete when every acceptance criterion, named constraint, and
NFR metric maps to at least one test case.

Rows are `🚧` until a tagged test asserts them. The rows that stay `🚧` are the
ones whose evidence needs an environment this repository cannot provision — a
running `filament-core-service`, a Quoin with the module installer — a human, or
an engine check that does not exist yet; every one of them says which.

`quire coverage --scope .` reports a backed-row count. That count is not
the rows of `## Test Case Summary`: a row there is one trace
target, and so is every acceptance criterion, constraint and validation
criterion a requirement document mints on its own, so the two numbers count
different populations and neither is a test count. Backed means at least one
source symbol outside `spec/` carries a matching tag; on its own it does not
say the tagged test asserts the row, which is what the code review and the gap
analysis are for.

The targets it cannot back are exactly those below that read `🚧`: the
nine rows TC-015..TC-019, TC-046, TC-110, TC-112 and TC-113, and the six
criteria FR-001-AC-2..4, FR-003-AC-5 and StR-001-VC-1..2. Every one needs a
running `filament-core-service`, a Quoin with the module installer, or a human.
The SOUP record adds the rows TC-123, TC-125, TC-130, TC-138 and TC-139.
TC-123 (duplicate purl, FR-009-AC-3) needs an engine check that does not exist: an
identity-uniqueness check over a frontmatter key. The
emission halves of TC-125, TC-130 and TC-139 need the engine to project authored
frontmatter record keys into the extracted record. TC-138, with FR-011-AC-4 and
FR-011-CON-1, needs a human reviewer. Each engine-gap row has a strict expected
failure that turns red when the engine supplies the check.

`make test` counts pytest functions, not matrix rows, and the two numbers are not
comparable. The 100% figure `make test` also prints is statement coverage over
`spec_objects_security/__init__.py` — four statements — and is evidence about
the Python package only: neither Node script is measured by it.

## Test Matrix Rules

1. Every acceptance criterion and named constraint has at least one test case.
2. Both Properties forms (typed table, `sysml` fence) and every one of the
   twenty-five object types are tested.
3. Item-rule boundaries are tested at their allowed and refused edges (zero
   versus one identity field, empty versus one-item `clauses`/`operations`,
   present versus absent graded row).
4. Every named refusal (unknown key, both forms, dangling
   clause, non-Identifier token, embedded default, invented vocabulary member)
   has a failing fixture.
5. Availability states are tested per declaration kind, at the two states this
   module's fixtures produce: `available` where the type declares the section
   and `not_applicable` where it does not. `unavailable` is the engine's
   row-error state; a skeleton that produced it would already have failed
   TC-080, so no row asserts it.
6. Legacy artifacts and unresolved tokens are covered as edge cases.

## Requirements Traceability

### Stakeholder Requirement Coverage

| Stakeholder Req | Trace to US/FR | Test/Validation | Status |
|---|---|---|---|
| StR-001 | US-001, FR-001..FR-012, NFR-001 | TC-111, TC-112, TC-113 | 🚧 VC-1 needs a running filament-core; VC-2 needs a generator run |

### User Story Coverage

| User Story | Acceptance Criteria | Test Cases | Status |
|---|---|---|---|
| US-001 | US-001-EX-1..3 (illustrative) implemented by FR-002..FR-012 | TC-080, TC-073, TC-110 | 🚧 TC-110 needs a Quoin with the module installer |

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Status |
|---|---|---|---|
| FR-001 | FR-001-AC-1..4 | TC-001..TC-004, TC-006..TC-014, TC-015..TC-017 | 🚧 AC-2..AC-4 need a running filament-core |
| FR-002 | FR-002-AC-1..4, FR-002-AC-6..11, FR-002-CON-1..4 | TC-020..TC-035 | ✅ |
| FR-003 | FR-003-AC-1, FR-003-AC-4..7, FR-003-CON-1 | TC-040, TC-041, TC-044..TC-046, TC-115 | ✅ AC-5 is a Demonstration (listing and restoring the real install) that nothing here discharges; AC-7 runs the install in a temporary HOME; AC-6's naming half is an expected failure |
| FR-004 | FR-004-AC-1..14, FR-004-CON-1..2 | TC-050..TC-063 | ✅ |
| FR-005 | FR-005-AC-1..9, FR-005-CON-1..3 | TC-080..TC-090 | ✅ |
| FR-006 | FR-006-AC-1..7, FR-006-CON-1..2 | TC-070..TC-077 | ✅ |
| FR-007 | FR-007-AC-1..2 | TC-091, TC-092 | ✅ |
| FR-008 | FR-008-AC-1..10 | TC-116..TC-120, TC-146..TC-149 | 🚧 |
| FR-009 | FR-009-AC-1..8, FR-009-CON-1..2 | TC-121..TC-128 | ✅ AC-3 is an engine gap (TC-123); AC-8 and CON-2 are inspections |
| FR-010 | FR-010-AC-1..4, FR-010-AC-6, FR-010-CON-1 | TC-129..TC-132, TC-134 | ✅ |
| FR-011 | FR-011-AC-1..5, FR-011-CON-1 | TC-135..TC-139 | ✅ AC-4 and CON-1 need a human reviewer (TC-138) |
| FR-012 | FR-012-AC-1..4 | TC-140..TC-143 | ✅ |
| FR-013 | FR-013-AC-1..7 | TC-150..TC-156 | 🚧 AC-7 needs `quire validate --repo` (PLAT-1519); `quire trace`/`quire matrix` show no document edges (PLAT-1519), so AC-6 reads the edge with `quire extract` |
| NFR-001 | NFR-001-AC-1..2, NFR-001-M-1..2 | TC-144, TC-145 | ✅ |
| FR-020 | FR-020-AC-1..6 | TC-160..TC-165 | 🚧 not yet implemented |
| FR-021 | FR-021-AC-1..7 | TC-166..TC-172 | 🚧 not yet implemented; AC-4, AC-6 and AC-7 are inspections; AC-2 and AC-3 are vacuous until a profile ships |
| NFR-002 | NFR-002-AC-1..2, NFR-002-M-1..2 | TC-173, TC-174 | 🚧 not yet implemented |
| FR-017 | FR-017-AC-1..7 | TC-175..TC-186 | ✅ `quire clauses` loads strictly and cannot load the real module (the object-type edges come from another module), so TC-181, TC-183, TC-185 and TC-186 evaluate a module that holds only the set files |

### Integration Test Coverage

| Integration Test | Success Criteria | Test Cases | Status |
|---|---|---|---|
| IT-001 | IT-001-AC-1..2 | TC-018, TC-019 | 🚧 needs a running filament-core |
| IT-002 | IT-002-SC-01..06 | TC-110 | 🚧 needs a Quoin with the module installer |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---|---|---|---|---|---|
| TC-001 | The packaged manifest path resolves to a file that exists | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-002 | The manifest parses as YAML and carries the declared top-level keys | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-003 | Every `object_type` declares a name and a data schema | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-004 | No two `object_type` entries share a name | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-006 | Every lexicon entry carries a whole definition | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-007 | Threat and risk coverage is declared as module data rather than encoded in the engine | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-008 | Every `object_type` ships a skeleton and the skeleton directory carries nothing extra | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-009 | Each skeleton's frontmatter matches the locators its manifest entry declares | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-010 | Each skeleton carries every asserted section and code block | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-011 | No skeleton drifts beyond what its manifest entry asserts | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-012 | Each skeleton supplies substantive body content, not placeholder text | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-013 | A filled skeleton round-trips through `validate_document` | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-014 | A mutated skeleton fails validation with the expected reason | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-015 | Activation against a clean filament-core returns 200 and creates a `modules` row | Integration | P1 | FR-001-AC-2 | 🚧 needs a running filament-core |
| TC-016 | Re-activation is a content-hash no-op | Integration | P1 | FR-001-AC-3 | 🚧 needs a running filament-core |
| TC-017 | Every declared contribution appears in the corresponding filament-core table | Integration | P1 | FR-001-AC-4 | 🚧 needs a running filament-core |
| TC-018 | The activation roundtrip's steps 3-6 all pass | Integration | P1 | IT-001-AC-1 | 🚧 needs a running filament-core |
| TC-019 | Re-activation produces the same SHA-256 content hash | Integration | P1 | IT-001-AC-2 | 🚧 needs a running filament-core |
| TC-021 | Every shipped schema declares the 2020-12 `$schema` and the `$id` matching its file name | Unit | P0 | FR-002-AC-2 | ✅ |
| TC-022 | Every `$ref` resolves to a shipped sibling or semantic-core | Unit | P0 | FR-002-AC-3 | ✅ |
| TC-023 | `make schemas-check` exits zero on the committed tree and non-zero naming a mutated schema | Integration | P1 | FR-002-AC-4 | ✅ |
| TC-025 | The built wheel contains every exported schema file | Integration | P1 | FR-002-AC-6 | ✅ |
| TC-026 | The packed npm tarball contains `manifest.yaml` and a sibling `schemas/<Model>.json` per export | Integration | P1 | FR-002-AC-7 | ✅ |
| TC-028 | `make schemas-check` names a stale committed schema with no emitted counterpart and writes nothing | Integration | P1 | FR-002-AC-9 | ✅ |
| TC-029 | Two generator runs over one source are byte-identical | Integration | P1 | FR-002-CON-3 | ✅ |
| TC-030 | The build uses the official `@typespec/json-schema` emitter only and no emitted file is hand-edited | Static | P2 | FR-002-CON-1 | ✅ |
| TC-031 | No `.npmrc`, no `file:`/`link:` dependency | Static | P2 | FR-002-CON-2 | ✅ |
| TC-032 | `package-lock.json` resolves every package, `@agent-ix/semantic-core` included, from npmjs | Unit | P2 | FR-002-CON-4 | ✅ |
| TC-035 | `.gitattributes` pins `eol=lf` and `npm pack` leaves nothing staged at the repository root | Unit | P1 | FR-002-AC-11 | ✅ |
| TC-040 | The `semantic` block equals the eight admitted keys and `exports` equals the twenty-five types | Unit | P0 | FR-003-AC-1, FR-003-CON-1 | ✅ |
| TC-044 | `quire.Registry.load_from` lists all twenty-five archetypes and `validate_document` reports no `semantic.*` load failure on any skeleton | Integration | P0 | FR-003-AC-4 | ✅ |
| TC-045 | An unknown `semantic` key is refused by the loader; the refusal names the key or path | Integration | P1 | FR-003-AC-6 | ✅ refusal verified; the naming half is a strict expected failure on quire-rs#221 and quire-rs#394 |
| TC-046 | `quoin module install path:` succeeds, lists the module, and the prior entry is restored | Manual | P1 | FR-003-AC-5 | 🚧 |
| TC-050 | Each of the twenty-five schemas differs from every other in a required, admitted, or item rule; none is `type: object` only | Unit | P0 | FR-004-AC-1 | ✅ |
| TC-051 | Asset: identity record validates; identity flag removed fails; no `fields` fails | Integration | P0 | FR-004-AC-2 | ✅ |
| TC-052 | Role with `operations` fails; permission and scope with `relations` each fail | Integration | P0 | FR-004-AC-3 | ✅ |
| TC-053 | Threat: `stride_category` row required; an invented STRIDE member fails | Integration | P0 | FR-004-AC-4 | ✅ |
| TC-054 | Vulnerability needs a `severity` row; risk needs `likelihood` and `impact`; audit finding needs `status` | Integration | P0 | FR-004-AC-5 | ✅ |
| TC-055 | Control: one clause plus an `effectiveness` row validates; each removal fails | Integration | P0 | FR-004-AC-6 | ✅ |
| TC-056 | Policy, password policy, cors policy and session config each need one clause and refuse `operations` | Integration | P0 | FR-004-AC-7 | ✅ |
| TC-057 | Auth flow: one operation validates; empty `operations` fails; `relations` fails | Integration | P0 | FR-004-AC-8 | ✅ |
| TC-058 | Audit event: `Timestamp` field and no identity validates; missing `Timestamp`, an identity row, or `operations` each fail | Integration | P0 | FR-004-AC-9 | ✅ |
| TC-059 | Trust boundary: one clause and a `trust_level` row validates; each removal fails; an invented trust level fails | Integration | P1 | FR-004-AC-10 | ✅ |
| TC-060 | The empty record `{}` fails against all twenty-five schemas | Unit | P0 | FR-004-AC-11, FR-004-CON-2 | ✅ |
| TC-061 | Placeholder `unresolved` target is accepted by the schema and reported by the extractor; a bare token is refused | Integration | P1 | FR-004-AC-12 | ✅ |
| TC-062 | No module schema redeclares a semantic-core model; every grammar item is a `$ref` to semantic-core | Unit | P1 | FR-004-AC-13, FR-004-CON-1 | ✅ |
| TC-063 | Data classification: `level` row required; `relations` refused | Integration | P1 | FR-004-AC-14 | ✅ |
| TC-070 | Each of the ten vocabularies has exactly its declared members as a closed `enum` | Unit | P0 | FR-006-AC-1 | ✅ |
| TC-071 | For each vocabulary the unassessed member validates and an invented member fails | Unit | P0 | FR-006-AC-2 | ✅ |
| TC-072 | No shipped schema carries a JSON Schema `default` keyword at any depth | Unit | P0 | FR-006-AC-3 | ✅ |
| TC-073 | A record of each sensitive type carrying a defaulted field fails; the same record without it validates | Integration | P0 | FR-006-AC-4, FR-006-CON-2 | ✅ |
| TC-074 | A `default:` constraint cell is refused by the extractor with `semantic.unknown-constraint-keyword` | Integration | P0 | FR-006-AC-5 | ✅ |
| TC-075 | `ControlEffectiveness` starts at `not_assessed` and `TrustLevel`'s unassessed member is `untrusted` | Unit | P1 | FR-006-AC-6 | ✅ |
| TC-076 | No shipped schema uses `minContains` or `maxContains`, so no negative rule can invert | Unit | P0 | FR-006-AC-7 | ✅ |
| TC-077 | No vocabulary member expresses "assume the permissive value" | Static | P2 | FR-006-CON-1 | ✅ |
| TC-080 | Every skeleton (twenty-five plus three alternates) validates with no error | Integration | P0 | FR-005-AC-1 | ✅ |
| TC-081 | Table and `sysml` skeletons extract to identical normalized fields with the recorded forms | Integration | P0 | FR-005-AC-2, FR-005-CON-2 | ✅ |
| TC-082 | Under the skeleton bundle index every skeleton extracts with zero errors and zero unresolved tokens | Integration | P0 | FR-005-AC-3 | ✅ |
| TC-083 | Availability states per skeleton (fields, clauses, operations) match the type's declared set | Integration | P1 | FR-005-AC-4 | ✅ |
| TC-084 | Every negative fixture produces its `expect:` code and the ten named cases exist | Integration | P0 | FR-005-AC-5 | ✅ |
| TC-085 | Every skeleton's H2 set is asserted by the manifest and includes every required heading | Unit | P1 | FR-005-AC-6 | ✅ |
| TC-086 | Every skeleton is placeholder-free with non-empty asserted sections | Unit | P2 | FR-005-AC-7 | ✅ |
| TC-087 | Skeleton titles are distinct `Identifier`s outside `KernelScalar`, and `object` equals `type` in every skeleton frontmatter | Unit | P1 | FR-005-AC-8 | ✅ |
| TC-091 | The loaded `control` type lists exactly `threat`, `risk`, `vulnerability`, `hazard`, `failure_mode` under `allowed_links.mitigates` | Unit | P0 | FR-007-AC-1 | ✅ |
| TC-092 | A `control` `mitigates` edge to an `asset` fixture is reported `disallowed-edge-target` naming `asset` | Integration | P0 | FR-007-AC-2 | ✅ |
| TC-088 | No skeleton or fixture matches a credential-shaped literal | Unit | P0 | FR-005-AC-9, FR-005-CON-3 | ✅ |
| TC-089 | No corpus repository or vendored fixture is tracked (tree assertion over `git ls-files`) | Static | P2 | FR-005-CON-1 | ✅ |
| TC-090 | A Properties section holding both a table and a fence is refused at the second form | Integration | P1 | FR-005-CON-2 | ✅ |
| TC-110 | Quoin install roundtrip with state restore | Manual | P1 | IT-002-SC-01..IT-002-SC-06, FR-003-AC-5 | 🚧 needs a Quoin with the module installer |
| TC-111 | Every object type ships a typed schema a fixture reader can consume; a secret and a risk record are distinguishable by schema alone | Unit | P2 | StR-001-VC-3 | ✅ |
| TC-112 | A module activation against filament-core registers every declared contribution | Manual | P2 | StR-001-VC-1 | 🚧 needs a running filament-core |
| TC-113 | A generator run (minijinja-cli) produces a valid artifact from a shipped skeleton and schema | Manual | P2 | StR-001-VC-2 | 🚧 needs a generator run against a released module |
| TC-114 | The module directory a Quoin install would consume is complete and self-consistent: every export's schema file exists and carries its own `$id` | Unit | P1 | IT-002-SC-01 | ✅ precondition only; the install roundtrip itself is TC-110 |
| TC-115 | The shipped manifest is accepted by `quire validate --module` and `quoin module install` (`HOME` pointed at a temporary directory); an unknown top-level key is refused by quire naming it, an unknown `semantic` key is refused by quoin naming `semantic.foo` | Integration | P0 | FR-003-AC-7 | ✅ |
| TC-116 | The manifest declares the `NFR` required relation with `where` on `quality_attribute` = `security`, `mitigates`, `to: [threat, risk]`, outgoing, `unjustified-security-nfr` | Unit | P0 | FR-008-AC-1 | 🚧 |
| TC-117 | A `security` NFR with no `mitigates` edge yields exactly one `unjustified-security-nfr` finding naming the NFR, the declaration, the selector field and `security`, exit 0 | Integration | P0 | FR-008-AC-2 | ✅ |
| TC-118 | The same NFR with a `mitigates` edge to a threat in the same repository yields no finding; an NFR with another `quality_attribute` and no edge yields none | Integration | P0 | FR-008-AC-3, FR-008-AC-4 | 🚧 |
| TC-119 | Under `--okf --strict` the finding stays a `warning:`, and `--severity trace:unjustified-security-nfr=error` exits non-zero | Integration | P1 | FR-008-AC-5 | ✅ |
| TC-120 | `threat-has-control` and `risk-has-treatment` still declare `to: []` | Unit | P1 | FR-008-AC-6 | ✅ |
| TC-146 | A security NFR with a `mitigates` edge to a risk in the same repository yields no finding | Integration | P0 | FR-008-AC-7 | 🚧 |
| TC-147 | `quire validate --okf --repo o/a=… --repo o/b=…` with the NFR in `o/a` mitigating a threat in `o/b` yields no finding | Integration | P0 | FR-008-AC-8 | 🚧 |
| TC-148 | An NFR whose only `mitigates` edge targets a hazard yields the finding | Integration | P0 | FR-008-AC-9 | 🚧 |
| TC-149 | An NFR whose only `mitigates` edge targets a threat in a repository not named by `--repo` yields the finding | Integration | P0 | FR-008-AC-10 | 🚧 |
| TC-121 | The loaded manifest exports `soup_record` with a shipped schema, and its skeleton validates | Unit | P0 | FR-009-AC-1 | ✅ |
| TC-122 | A `soup_record` document without its `purl` frontmatter key fails naming `purl`; a declaration record without a `purl` field row fails its schema | Unit | P0 | FR-009-AC-2 | ✅ |
| TC-123 | Two `soup_record` documents with one purl yield one duplicate-identity report naming both | Integration | P0 | FR-009-AC-3 | 🚧 the engine has no identity-uniqueness check over a frontmatter key; strict expected failure |
| TC-124 | A record with an added `digest` key fails; a record with a different purl is a distinct component | Unit | P0 | FR-009-AC-4, FR-009-CON-1 | ✅ schema half; the authored-document half is a strict expected failure (the frontmatter record keys of an authored document are neither validated against the data schema nor projected into the extracted record) |
| TC-125 | `supplier: unknown` validates, an omitted `supplier` adds no key, and the schema has no `default` keyword | Unit | P0 | FR-009-AC-5 | 🚧 schema half asserted; the emission half is a strict expected failure (the frontmatter record keys of an authored document are neither validated against the data schema nor projected into the extracted record) |
| TC-126 | A record carrying both `license` and `license_fact_ref` fails; either alone validates | Unit | P0 | FR-009-AC-6 | ✅ |
| TC-127 | `finding_refs` and `license_fact_ref` ids validate; a `finding_text` key fails | Unit | P1 | FR-009-AC-7 | ✅ |
| TC-128 | The module declares no `--discharges` option, binding key or SBOM reader | Static | P2 | FR-009-AC-8, FR-009-CON-2 | ✅ |
| TC-129 | `SoupSupportStatus` has exactly four members; `unknown` validates and an invented member fails | Unit | P0 | FR-010-AC-1, FR-010-CON-1 | ✅ schema half; the authored-document half is a strict expected failure (the frontmatter record keys of an authored document are neither validated against the data schema nor projected into the extracted record) |
| TC-130 | An empty `known_anomalies` and an absent one both validate and emit different records | Unit | P0 | FR-010-AC-2 | 🚧 both forms validate; the emission half is a strict expected failure (the frontmatter record keys of an authored document are neither validated against the data schema nor projected into the extracted record) |
| TC-131 | `end_of_support` accepts a date or `unknown` and refuses any other string | Unit | P0 | FR-010-AC-3 | ✅ schema half; the authored-document half is a strict expected failure (the frontmatter record keys of an authored document are neither validated against the data schema nor projected into the extracted record) |
| TC-132 | The `soup_record` schema carries no `default` keyword at any depth | Unit | P0 | FR-010-AC-4 | ✅ |
| TC-134 | An anomaly statement with a credential-shaped string is refused by the FR-005 scan | Unit | P1 | FR-010-AC-6 | ✅ |
| TC-135 | A non-empty `disposition_clause` validates; an empty or whitespace-only one fails | Unit | P0 | FR-011-AC-1 | ✅ |
| TC-136 | A record with no `disposition_clause` validates and carries no such key | Unit | P0 | FR-011-AC-2 | ✅ |
| TC-137 | A record embedding `decision`, `rationale`, `approvalRef`, `attestation`, `approver` or `expires` fails | Unit | P0 | FR-011-AC-3 | ✅ |
| TC-138 | A worked disposition fact of the quoin FR-046 shape names a person in `attestedBy` and `authority` | Manual | P1 | FR-011-AC-4, FR-011-CON-1 | 🚧 the worked example is committed at `tests/fixtures/soup/disposition-example.md` and awaits a human reviewer |
| TC-139 | A `disposition_clause` changes no other emitted key of the record | Unit | P1 | FR-011-AC-5 | 🚧 both documents validate; the emission half is a strict expected failure (the frontmatter record keys of an authored document are neither validated against the data schema nor projected into the extracted record) |
| TC-140 | The loaded `vulnerability` type lists `asset`, `attack_surface`, `soup_record` under `affects`; `soup_record` declares no `allowed_links` | Unit | P0 | FR-012-AC-1 | ✅ |
| TC-141 | A `vulnerability` `affects` edge to a `soup_record` validates with no `UnknownEdgeType`; to a `threat` it is `disallowed-edge-target` | Integration | P0 | FR-012-AC-2 | ✅ |
| TC-142 | A `soup_record` that no vulnerability affects validates with no finding | Integration | P1 | FR-012-AC-3 | ✅ |
| TC-143 | A `soup_record` carrying `severity`, `cve_id` or an advisory list fails | Unit | P0 | FR-012-AC-4 | ✅ schema half; the authored-document half is a strict expected failure (the frontmatter record keys of an authored document are neither validated against the data schema nor projected into the extracted record) |
| TC-144 | The `soup_record` schema has no score, rating, class, tier or level property and reuses no graded vocabulary | Unit | P0 | NFR-001-AC-1, NFR-001-M-1 | ✅ |
| TC-145 | A validated fixture emits exactly the keys the author wrote | Unit | P0 | NFR-001-AC-2, NFR-001-M-2 | ✅ |
| TC-150 | The manifest declares `soup-record-serves-requirement` relation reading `references`, and `soup_record` declares no `allowed_links` | Unit | P0 | FR-013-AC-1 | ✅ |
| TC-151 | A record whose `serves` is absent yields exactly one `soup-serves-no-requirement` finding naming it | Integration | P0 | FR-013-AC-2 | ✅ |
| TC-152 | A record whose `serves` names an `FR` in the bundle yields no finding | Integration | P0 | FR-013-AC-3 | ✅ |
| TC-153 | A `serves` entry naming a document of another kind, or nothing, still yields the finding | Integration | P1 | FR-013-AC-4 | ✅ |
| TC-154 | The finding is a warning and `--severity trace:soup-serves-no-requirement=error` promotes it | Integration | P1 | FR-013-AC-5 | ✅ |
| TC-155 | The skeleton carries no `serves`; `quire extract` lists each `serves` entry as a `references` edge | Integration | P1 | FR-013-AC-6 | ✅ |
| TC-156 | `quire validate --okf --repo o/a=… --repo o/b=…` with the record in `o/a` serving an `FR` in `o/b` yields no finding | Integration | P1 | FR-013-AC-7 | 🚧 the pinned CLI has no `--repo`; engine gap tracked in PLAT-1519 |
| TC-160 | A fixture profile with every required key passes the profile test | Unit | P1 | FR-020-AC-1 | 🚧 |
| TC-161 | A profile missing a required key, or named differently from its file stem, fails | Unit | P1 | FR-020-AC-2 | 🚧 |
| TC-162 | A profile with an empty or repeated clause-set key fails | Unit | P1 | FR-020-AC-3 | 🚧 |
| TC-163 | A profile with an unknown key or a non-string context value fails | Unit | P1 | FR-020-AC-4 | 🚧 |
| TC-164 | A profile carrying clause text or title fails | Unit | P1 | FR-020-AC-5 | 🚧 |
| TC-165 | The manifest has no `profiles` key and still activates | Unit | P1 | FR-020-AC-6 | 🚧 |
| TC-166 | Every shipped profile passes the profile test | Unit | P1 | FR-021-AC-1 | 🚧 |
| TC-167 | Every shipped key is declared by a module in the reference module set | Integration | P1 | FR-021-AC-2 | 🚧 |
| TC-168 | `quire publish-check` accepts the declaring module of every shipped key | Integration | P1 | FR-021-AC-3 | 🚧 |
| TC-169 | Profile context entries state only market or product-kind facts | Manual | P2 | FR-021-AC-4 | 🚧 human reviewer |
| TC-170 | Shipped profile names are a subset of the three named profiles | Unit | P1 | FR-021-AC-5 | 🚧 |
| TC-171 | Published files name no licensed pack | Manual | P2 | FR-021-AC-6 | 🚧 human reviewer |
| TC-172 | A published module's set for an intended source is listed in the matching profile | Manual | P2 | FR-021-AC-7 | 🚧 human reviewer |
| TC-173 | Every shipped profile has only the six top-level keys and the three key fields | Unit | P1 | NFR-002-AC-1, NFR-002-M-1 | 🚧 |
| TC-174 | `quire publish-check` accepts every declaring module, with no authority list | Integration | P1 | NFR-002-AC-2, NFR-002-M-2 | 🚧 |
| TC-175 | The manifest `clause_sets` names exactly `nist/sp800-53@5.2.0` and `owasp/asvs@5.0.0` | Unit | P0 | FR-017-AC-1 | ✅ |
| TC-176 | Every declared set's `rights.text` is `none`, `original` or `explicitly_cleared` | Unit | P0 | FR-017-AC-2 | ✅ |
| TC-177 | `quire publish-check --module` over this module exits 0 | Integration | P0 | FR-017-AC-3 | ✅ |
| TC-178 | A set with `rights.text: licensed` makes `quire publish-check` exit non-zero without echoing its text | Integration | P0 | FR-017-AC-4 | ✅ |
| TC-179 | Every set names its licence; the NIST licence states the public-domain status and carries no attribution or share-alike key | Unit | P0 | FR-017-AC-5 | ✅ |
| TC-180 | Each NIST clause's `subjects` is its official family code, declared in the `family` dimension | Unit | P0 | FR-017-AC-6 | ✅ |
| TC-181 | `quire clauses evaluate` binds 149, 287 and 370 NIST clauses at low, moderate and high, a control in no baseline is `not_binding`, and no baseline leaves every clause `unresolved` | Integration | P0 | FR-017-AC-7 | ✅ |
| TC-182 | The wheel and the npm tarball ship every file named by `clause_sets` | Integration | P1 | FR-017-AC-1 | ✅ |
| TC-183 | `quoin discharge --binding --rmm --repo` renders a requirements matrix for the NIST set over a synthetic corpus | Integration | P1 | FR-017 | ✅ |
| TC-184 | Each ASVS clause's `subjects` is its chapter id, declared in the `chapter` dimension | Unit | P0 | FR-017-AC-6 | ✅ |
| TC-185 | `quire clauses evaluate` binds 70, 253 and 345 ASVS clauses at level 1, 2 and 3, and no level leaves every clause `unresolved` | Integration | P0 | FR-017-AC-7 | ✅ |
| TC-186 | `quoin discharge --binding --rmm --repo` renders a requirements matrix for the ASVS set over a synthetic corpus, with compliant, undischarged and not-applicable rows | Integration | P1 | FR-017 | ✅ |

## Test Environment

Every `Integration` row that names Quire runs against the Quire wheel FR-005
Inputs pins, a dev dependency resolved from `internal-pypi` by `poetry install`.
The suite **fails** rather than skips when `extract_semantic` is absent, so no
row here can be reported green without the engine under test. This is the
disposition of `agent-ix/spec-objects-security#10`.

Rows over the record keys the extractor does not populate (`severity`,
`likelihood`, `impact`, `status`, `level`, `trust_level`, `stride_category`,
`effectiveness`, `lifecycle`, `material_ref`, `relations`, and the
cross-reference lists) are verified against hand-built records, not extracted
ones — TC-053, TC-054, TC-059, TC-063, TC-073 in particular — and their tests
say so; they are schema evidence, not extraction evidence.

## Coverage Gaps

Every acceptance criterion, named constraint and NFR metric of FR-001..FR-006,
IT-001, IT-002 and StR-001 now has at least one row. Nine rows cannot
be discharged in this repository and are `🚧` with the reason on the row:
TC-015..TC-019 and TC-112 need a running `filament-core-service`, TC-046 and
TC-110 need a Quoin with the module installer, and TC-113
needs a generator run against a released module.

TC-114 is deliberately a row of its own rather than a tag on TC-110. A test
that only checks the module directory is complete cannot back "the pre-install
listing is captured", and tagging it `TC-110` made a blocked row report backed
— which the gap analysis caught. Splitting it left TC-110 correctly unbacked, which is a truer number rather
than a better one.

`quire coverage` additionally reports `status-column-matches-nothing` on the
Functional Requirement Coverage table: the `TestMatrix` archetype asserts the
header `Coverage Status` while `traceability.status.column` names `Status`, so
status classification is skipped there and a complete-but-unbacked row cannot
be caught. Renaming the column here fails structural validation, so the header
stays as the archetype asserts and the defect is upstream —
`agent-ix/spec-artifacts-process#81` and `#82` own it. The `Test Case Summary`
table, which does use `Status`, is classified normally.

Two evidence-plan artifacts are absent and are carried by the plan, not by this
matrix: no `SuiteRegistry` document declares a producer for the `Unit`,
`Integration`, `Static` and `Manual` evidence kinds, and no `Inspections`
document exists to discharge the `Static` and `Manual` rows. `quire coverage`
reports both as `archetype-matches-nothing` against the
`spec-artifacts-process` declarations, not against this bundle.
