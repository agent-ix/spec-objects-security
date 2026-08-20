---
id: TM-001
title: "Test Matrix"
type: TestMatrix
---
# Test Matrix

## Overview

Maps every acceptance criterion to the test that backs it.

This document was a **three-line stub until 2026-08-19** — an `FR | IT | Status`
table with one row, no `## Test Case Summary`, and no acceptance-criterion
coverage at all. The consequence is the one agent-ix/quire-rs#72 counts across
the ecosystem: the module minted **zero `test-case` targets**, so no test in this
repository could ever be reported as backing anything.

**[RAN]** `quire coverage --scope .` here, before: **0 of 4 criteria backed.**
The tests existed the whole time; nothing connected them.

FR-001-AC-2, AC-3 and AC-4 are **activation** criteria — they need a running
filament-core, which this package's suite does not start. They are listed as
pending rather than claimed.

## Requirements Traceability

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Coverage Status |
|----------------|---------------------|------------|-----------------|
| FR-001 | FR-001-AC-1 | TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014 | ✅ Complete |
| FR-001 | FR-001-AC-2 | — | 🚧 Pending |
| FR-001 | FR-001-AC-3 | — | 🚧 Pending |
| FR-001 | FR-001-AC-4 | — | 🚧 Pending |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---------|-------|------|----------|-----------|--------|
| TC-001 | The packaged manifest path resolves to a file that exists (`test_manifest_path_points_to_packaged_manifest`) | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-002 | The manifest parses as YAML and carries the declared top-level keys (`test_manifest_loads`) | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-003 | Every `object_type` declares a name and a data schema (`test_object_type_has_name_and_data_schema`) | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-004 | No two `object_type` entries share a name — a duplicate resolves first-wins and silently shadows the other (`test_no_duplicate_object_type_names`) | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-005 | The manifest validates against the FR-035 module-manifest schema imported from spec-artifacts-iso (`test_manifest_validates_against_fr035_schema`) | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-006 | Every lexicon entry carries a whole definition — a truncated one reads as declared and defines nothing (`test_lexicon_entries_are_whole`) | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-007 | Threat and risk coverage is declared as module data rather than encoded in the engine (`test_threat_and_risk_coverage_is_declared_not_coded`) | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-008 | Every `object_type` ships a skeleton and the skeleton directory carries nothing extra (`test_every_object_type_ships_a_skeleton_and_nothing_extra`) | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-009 | Each skeleton's frontmatter matches the locators its manifest entry declares (`test_frontmatter_matches_manifest_locators`) | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-010 | Each skeleton carries every asserted section and code block (`test_asserted_sections_and_code_blocks_present`) | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-011 | No skeleton drifts beyond what its manifest entry asserts (`test_no_skeleton_drift_beyond_manifest`) | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-012 | Each skeleton supplies substantive body content, not placeholder text (`test_skeleton_is_substantive`) | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-013 | A filled skeleton round-trips through `validate_document` (`test_roundtrip_skeleton_validates`) | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-014 | A mutated skeleton fails validation with the expected reason — the negative half, without which TC-013 passes vacuously (`test_roundtrip_mutation_fails`) | Unit | P0 | FR-001-AC-1 | ✅ |
