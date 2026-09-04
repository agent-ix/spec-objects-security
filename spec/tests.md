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
  - target: "ix://agent-ix/spec-objects-security/NFR-001"
    type: covers
---
# Test Matrix

## Overview

This matrix is the verification contract for the module: the manifest
activation requirement (FR-001, issue #1 era, rows TC-001..TC-014) and the
issue #13 semantic module contract (US-001, FR-002..FR-006, NFR-001, IT-002).
Coverage is complete when every acceptance criterion, named constraint, and
NFR metric maps to at least one test case.

Rows are `🚧` until a tagged test asserts them; the rows that stay `🚧` are the
ones whose evidence needs an environment this repository cannot provision (a
running `filament-core-service`, a Quoin built from main) or a human.

## Test Matrix Rules

1. Every acceptance criterion and named constraint has at least one test case.
2. Both Properties forms (typed table, `sysml` fence) and every one of the
   twenty-three object types are tested.
3. Item-rule boundaries are tested at their allowed and refused edges (zero
   versus one identity field, empty versus one-item `clauses`/`operations`,
   present versus absent graded row).
4. Every named refusal (digest mismatch, unknown key, both forms, dangling
   clause, non-Identifier token, embedded default, invented vocabulary member)
   has a failing fixture.
5. Availability states (`available`, `not_applicable`, `unavailable`) are
   tested per declaration kind.
6. Legacy artifacts and unresolved tokens are covered as edge cases.

## Requirements Traceability

### Stakeholder Requirement Coverage

| Stakeholder Req | Trace to US/FR | Test/Validation | Coverage Status |
|---|---|---|---|
| StR-001 | US-001, FR-001..FR-006 | TC-005, TC-006, TC-111 | 🚧 VC-1/VC-2 need a running filament-core |

### User Story Coverage

| User Story | Acceptance Criteria | Test Cases | Coverage Status |
|---|---|---|---|
| US-001 | US-001-EX-1..3 (illustrative) implemented by FR-002..FR-006 | TC-080, TC-073, TC-110 | 🚧 TC-110 needs a Quoin built from main |

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Coverage Status |
|---|---|---|---|
| FR-001 | FR-001-AC-1..4 | TC-001..TC-014 | 🚧 AC-2..AC-4 need a running filament-core |
| FR-002 | FR-002-AC-1..9, FR-002-CON-1..5 | TC-020..TC-033 | 🚧 pending implementation |
| FR-003 | FR-003-AC-1..7, FR-003-CON-1..3 | TC-040..TC-047 | 🚧 AC-5 is a Demonstration; AC-6's naming half is an expected failure |
| FR-004 | FR-004-AC-1..14, FR-004-CON-1..2 | TC-050..TC-063 | 🚧 pending implementation |
| FR-005 | FR-005-AC-1..9, FR-005-CON-1..3 | TC-080..TC-090 | 🚧 pending implementation |
| FR-006 | FR-006-AC-1..6, FR-006-CON-1..2 | TC-070..TC-076 | 🚧 pending implementation |

### Non-Functional Requirement Coverage

| Non-Functional Req | Verification Method | Evidence/Test Cases | Status |
|---|---|---|---|
| NFR-001 | Test (NFR-001-AC-1..4: locator baseline diff, edge-vocabulary baseline diff, legacy skeleton validation) | TC-100..TC-103 | 🚧 pending implementation |

### Integration Test Coverage

| Integration Test | Success Criteria | Test Cases | Coverage Status |
|---|---|---|---|
| IT-001 | IT-001-AC-1..2 | TC-002..TC-004 | 🚧 needs a running filament-core |
| IT-002 | IT-002-SC-01..06 | TC-110 | 🚧 needs a Quoin built from main |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---|---|---|---|---|---|
| TC-001 | The packaged manifest path resolves to a file that exists | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-002 | The manifest parses as YAML and carries the declared top-level keys | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-003 | Every `object_type` declares a name and a data schema | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-004 | No two `object_type` entries share a name | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-005 | The manifest validates against the FR-035 module-manifest schema imported from spec-artifacts-iso | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-006 | Every lexicon entry carries a whole definition | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-007 | Threat and risk coverage is declared as module data rather than encoded in the engine | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-008 | Every `object_type` ships a skeleton and the skeleton directory carries nothing extra | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-009 | Each skeleton's frontmatter matches the locators its manifest entry declares | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-010 | Each skeleton carries every asserted section and code block | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-011 | No skeleton drifts beyond what its manifest entry asserts | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-012 | Each skeleton supplies substantive body content, not placeholder text | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-013 | A filled skeleton round-trips through `validate_document` | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-014 | A mutated skeleton fails validation with the expected reason | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-020 | Emitted set equals the twenty-three object-type models plus the declared support models; `toolchain.json` records compiler and emitter 1.15.0 | Unit | P0 | FR-002-AC-1 | 🚧 |
| TC-021 | Every shipped schema declares the 2020-12 `$schema` and the `$id` matching its file name under the manifest-version base | Unit | P0 | FR-002-AC-2 | 🚧 |
| TC-022 | Every `$ref` resolves to a shipped sibling or semantic-core 0.1.0 | Unit | P0 | FR-002-AC-3 | 🚧 |
| TC-023 | `make schemas-check` exits zero on the committed tree and non-zero naming a mutated schema or digest | Integration | P1 | FR-002-AC-4 | 🚧 |
| TC-024 | A `@jsonSchema` base version differing from the manifest version fails the generator naming both | Integration | P1 | FR-002-AC-5 | 🚧 |
| TC-025 | The built wheel contains every exported schema file | Integration | P1 | FR-002-AC-6 | 🚧 |
| TC-026 | The packed npm tarball contains `manifest.yaml` and a sibling `schemas/<Model>.json` per export | Integration | P1 | FR-002-AC-7 | 🚧 |
| TC-027 | A coordinated version bump re-emits every `$id`/`$ref` at the new version with matching digests; bumping one half of the pair fails the check | Integration | P1 | FR-002-AC-8, FR-002-CON-5 | 🚧 |
| TC-028 | `make schemas-check` names a stale committed schema with no emitted counterpart and writes nothing | Integration | P1 | FR-002-AC-9 | 🚧 |
| TC-029 | Two generator runs over one source are byte-identical | Integration | P1 | FR-002-CON-3 | 🚧 |
| TC-030 | The build uses the official `@typespec/json-schema` emitter only and no emitted file is hand-edited | Static | P2 | FR-002-CON-1 | 🚧 |
| TC-031 | No `.npmrc`, no `file:`/`link:` dependency, exact toolchain pins in `package.json` | Static | P2 | FR-002-CON-2 | 🚧 |
| TC-032 | `package-lock.json` resolves every package from npmjs except `@agent-ix/semantic-core` (npm.ix) | Unit | P2 | FR-002-CON-4 | 🚧 |
| TC-033 | No acceptance test hard-codes the `$id` version segment; each reads it from the manifest `version` | Static | P2 | FR-002-CON-5 | 🚧 |
| TC-040 | The `semantic` block equals the nine admitted keys and `exports` equals the twenty-three types | Unit | P0 | FR-003-AC-1, FR-003-CON-1 | 🚧 |
| TC-041 | Every exported type's `data_schema` is the reference form whose file hashes to the recorded digest | Unit | P0 | FR-003-AC-2 | 🚧 |
| TC-042 | Every 0.1.0 locator is unchanged against the checked-in baseline | Unit | P0 | FR-003-AC-3 | 🚧 |
| TC-043 | Every added locator is `required: false` | Unit | P1 | FR-003-AC-3, FR-003-CON-2 | 🚧 |
| TC-044 | `quire.Registry.load_from` lists all twenty-three archetypes and `validate_document` reports no `semantic.*` load failure on any skeleton | Integration | P0 | FR-003-AC-4 | 🚧 |
| TC-045 | An unknown `semantic` key and an altered digest are each refused by the loader; the refusal names the key or path | Integration | P1 | FR-003-AC-6 | 🚧 refusal verified; the naming half is an expected failure on quire-rs#221 and quire-rs#394 |
| TC-046 | `quoin module install path:` succeeds, lists the module, and the prior entry is restored | Manual | P1 | FR-003-AC-5 | 🚧 |
| TC-047 | The `traceability` block and every `allowed_links`/`roles` map equal the 0.1.0 baseline | Unit | P0 | FR-003-AC-7, FR-003-CON-3 | 🚧 |
| TC-050 | Each of the twenty-three schemas differs from every other in a required, admitted, or item rule; none is `type: object` only | Unit | P0 | FR-004-AC-1 | 🚧 |
| TC-051 | Asset: identity record validates; identity flag removed fails; no `fields` fails | Integration | P0 | FR-004-AC-2 | 🚧 |
| TC-052 | Role with `operations` fails; permission and scope with `relations` each fail | Integration | P0 | FR-004-AC-3 | 🚧 |
| TC-053 | Threat: `stride_category` row required; an invented STRIDE member fails | Integration | P0 | FR-004-AC-4 | 🚧 |
| TC-054 | Vulnerability needs a `severity` row; risk needs `likelihood` and `impact`; audit finding needs `status` | Integration | P0 | FR-004-AC-5 | 🚧 |
| TC-055 | Control: one clause plus an `effectiveness` row validates; each removal fails | Integration | P0 | FR-004-AC-6 | 🚧 |
| TC-056 | Policy, password policy, cors policy and session config each need one clause and refuse `operations` | Integration | P0 | FR-004-AC-7 | 🚧 |
| TC-057 | Auth flow: one operation validates; empty `operations` fails; `relations` fails | Integration | P0 | FR-004-AC-8 | 🚧 |
| TC-058 | Audit event: `Timestamp` field and no identity validates; missing `Timestamp`, an identity row, or `operations` each fail | Integration | P0 | FR-004-AC-9 | 🚧 |
| TC-059 | Trust boundary: one clause and a `trust_level` row validates; each removal fails; an invented trust level fails | Integration | P1 | FR-004-AC-10 | 🚧 |
| TC-060 | The empty record `{}` fails against all twenty-three schemas | Unit | P0 | FR-004-AC-11, FR-004-CON-2 | 🚧 |
| TC-061 | Placeholder `unresolved` target is accepted by the schema and reported by the extractor; a bare token is refused | Integration | P1 | FR-004-AC-12 | 🚧 |
| TC-062 | No module schema redeclares a semantic-core model; every grammar item is a `$ref` to semantic-core | Unit | P1 | FR-004-AC-13, FR-004-CON-1 | 🚧 |
| TC-063 | Data classification: `level` row required; `relations` refused | Integration | P1 | FR-004-AC-14 | 🚧 |
| TC-070 | Each of the ten vocabularies has exactly its declared members as a closed `enum` | Unit | P0 | FR-006-AC-1 | 🚧 |
| TC-071 | For each vocabulary the unassessed member validates and an invented member fails | Property | P0 | FR-006-AC-2 | 🚧 |
| TC-072 | No shipped schema carries a JSON Schema `default` keyword at any depth | Unit | P0 | FR-006-AC-3 | 🚧 |
| TC-073 | A record of each sensitive type carrying a defaulted field fails; the same record without it validates | Integration | P0 | FR-006-AC-4, FR-006-CON-2 | 🚧 |
| TC-074 | A `default:` constraint cell is refused by the extractor with `semantic.unknown-constraint-keyword` | Integration | P0 | FR-006-AC-5 | 🚧 |
| TC-075 | `ControlEffectiveness` starts at `not_assessed` and `TrustLevel`'s unassessed member is `untrusted` | Unit | P1 | FR-006-AC-6 | 🚧 |
| TC-076 | No vocabulary member expresses "assume the permissive value" | Static | P2 | FR-006-CON-1 | 🚧 |
| TC-080 | Every skeleton (twenty-three plus three alternates) validates with no error | Integration | P0 | FR-005-AC-1 | 🚧 |
| TC-081 | Table and `sysml` skeletons extract to identical normalized fields with the recorded forms | Integration | P0 | FR-005-AC-2, FR-005-CON-2 | 🚧 |
| TC-082 | Under the skeleton bundle index every skeleton extracts with zero errors and zero unresolved tokens | Integration | P0 | FR-005-AC-3 | 🚧 |
| TC-083 | Availability states per skeleton (fields, clauses, operations) match the type's declared set | Integration | P1 | FR-005-AC-4 | 🚧 |
| TC-084 | Every negative fixture produces its `expect:` code and the ten named cases exist | Integration | P0 | FR-005-AC-5 | 🚧 |
| TC-085 | Every skeleton's H2 set is asserted by the manifest and includes every required heading | Unit | P1 | FR-005-AC-6 | 🚧 |
| TC-086 | Every skeleton is placeholder-free with non-empty asserted sections | Unit | P2 | FR-005-AC-7 | 🚧 |
| TC-087 | Skeleton titles are distinct `Identifier`s outside `KernelScalar`, and `object` equals `type` in every skeleton frontmatter | Unit | P1 | FR-005-AC-8 | 🚧 |
| TC-088 | No skeleton or fixture matches a credential-shaped literal | Unit | P0 | FR-005-AC-9, FR-005-CON-3 | 🚧 |
| TC-089 | No corpus repository or vendored fixture is edited by the change (diff over the branch) | Static | P2 | FR-005-CON-1 | 🚧 |
| TC-090 | A Properties section holding both a table and a fence is refused at the second form | Integration | P1 | FR-005-CON-2 | 🚧 |
| TC-100 | Zero 0.1.0 locators changed | Unit | P0 | NFR-001-AC-1 | 🚧 |
| TC-101 | Zero `traceability`/`allowed_links` bytes changed against the 0.1.0 baseline | Unit | P0 | NFR-001-AC-2 | 🚧 |
| TC-102 | Every checked-in 0.1.0 skeleton validates under 0.2.0 with zero errors | Integration | P0 | NFR-001-AC-3 | 🚧 |
| TC-103 | No checked-in 0.1.0 skeleton yields `semantic.record-invalid` under 0.2.0; the `object:`-declaring case is an expected failure | Integration | P0 | NFR-001-AC-4 | 🚧 |
| TC-110 | Quoin install roundtrip with state restore | Manual | P1 | IT-002-SC-01..IT-002-SC-06, FR-003-AC-5 | 🚧 needs a Quoin built from quoin main ≥ `3e842ce` (no release carries it) |
| TC-111 | Every object type ships a typed schema a fixture reader can consume; a secret and a risk record are distinguishable by schema alone | Manual | P2 | StR-001-VC-3 | 🚧 |

## Test Environment

Every `Integration` row that names Quire runs against the Quire wheel FR-005
Inputs pins, provisioned by `make dev-quire`. That wheel is not on any index
this repository may commit a dependency against (`internal-pypi` serves 0.33.0
at most); `agent-ix/quire-rs#392` is the blocking issue. The suite **fails**
rather than skips when `extract_semantic` is absent, so no row here can be
reported green without the engine under test. This is the disposition of
`agent-ix/spec-objects-security#10`.

Rows over the record keys the extractor does not populate (`severity`,
`likelihood`, `impact`, `status`, `level`, `trust_level`, `stride_category`,
`effectiveness`, `lifecycle`, `material_ref`, `relations`, and the
cross-reference lists) are verified against hand-built records, not extracted
ones — TC-053, TC-054, TC-059, TC-063, TC-073 in particular — and their tests
say so; they are schema evidence, not extraction evidence.

## Coverage Gaps

Every criterion, constraint, and metric above has a row. Two evidence-plan
artifacts are absent and are carried by the plan, not by this matrix: no
`SuiteRegistry` document declares a producer for the `Unit`, `Integration`,
`Static`, `Property` and `Manual` evidence kinds, and no `Inspections` document
exists to discharge the `Static`/`Manual` rows (TC-005, TC-006, TC-030,
TC-031, TC-033, TC-046, TC-076, TC-089, TC-110, TC-111). Rows remain `🚧`
until the implementation lands a tagged test for them.
