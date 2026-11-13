---
id: FR-020
title: "A source profile is a module data file naming clause sets and an applicability context"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-180"
    type: "constrains"
---
# FR-020: A source profile is a module data file naming clause sets and an applicability context

## Description

A source profile says which security and compliance sources a kind of product answers to. It is data in this module,
a YAML file under `profiles/`, read by Quoin ([quoin FR-180](ix://agent-ix/quoin/FR-180)). It adds nothing to the
Quire engine and nothing to the module manifest: a profile file is found by its directory, so the manifest declares no
`profiles` key. No user story covers source selection, so this requirement traces to the module's manifest requirement
and to the Quoin requirement that reads it.

A profile file has `schemaVersion: source-profile-v1`, a `name`, a `title`, a `description`, a `clauseSets` list and
an optional `context` map. Each `clauseSets` entry is an exact clause-set key: `authority`, `id` and `version`. The
`context` map gives a value for a classification dimension of the listed sets (for example a statement that the
product is a medical device). It is the base of the effective context Quoin builds, where a repository's own context
values replace it ([quoin FR-180](ix://agent-ix/quoin/FR-180)); the engine then decides each clause's applicability.
The profile decides nothing about a clause.

The rules below are checked in two places: by this repository's profile test over the files it ships, and by Quoin when
it reads a profile (quoin FR-180 refuses a profile that breaks them). The module ships no JSON Schema file for
profiles; the rules in this requirement are the definition.

A profile names sets by key and carries no clause or standard text, so it cannot hold licensed content.

## Inputs

- A `profiles/<name>.yaml` file.

## Outputs

- A profile that Quoin selects and evaluates.

## Behavior

- A profile file SHALL declare `schemaVersion: source-profile-v1`.
- A profile file SHALL declare a non-empty `name` equal to its file stem, and a non-empty `title` and `description`.
- A profile file SHALL list at least one clause-set key, each with a non-empty `authority`, `id` and `version`, and no key twice.
- The `context` of a profile SHALL map non-empty dimension names to non-empty string values.
- A profile file SHALL carry no key other than those named here.
- A profile SHALL NOT carry clause text, a clause title, or a standard's wording.
- The manifest SHALL declare no key for profiles.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-020-AC-1 | A fixture profile with every required key and one set passes this repository's profile test. | Test |
| FR-020-AC-2 | A profile missing `name`, `title`, `description` or `clauseSets` fails the profile test, as does one whose `name` differs from its file stem. | Test |
| FR-020-AC-3 | A profile with an empty `clauseSets`, a key with an empty field, or a repeated key fails the profile test. | Test |
| FR-020-AC-4 | A profile with an unknown top-level key, or a `context` entry with an empty or non-string value, fails the profile test. | Test |
| FR-020-AC-5 | A profile carrying `text` or `title` under a `clauseSets` entry fails the profile test. | Test |
| FR-020-AC-6 | The module manifest has no `profiles` key and still activates against filament-core. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md); `agent-ix/quoin` FR-180
- **Downstream**: [FR-021](./FR-021-default-source-profiles.md)
