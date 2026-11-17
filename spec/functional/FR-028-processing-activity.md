---
id: FR-028
title: "A processing_activity states the person-authored context for records of processing"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-023"
    type: depends_on
  - target: "ix://agent-ix/spec-objects-architecture/FR-015"
    type: depends_on
---
# FR-028: A processing_activity states the person-authored context for records of processing

## Description

The security module SHALL let a person describe one processing activity and identify the connections, sinks and parts it covers. The authored fields state contextual facts that the data-flow model cannot supply. The module SHALL NOT derive them from names, code, runtime observations, a purpose field on a sink, or any source outside this requirement.

## Inputs

- A Markdown object with `type: processing_activity` and `object: processing_activity`.
- The `ProcessingActivity` TypeSpec model and its generated frontmatter schema.
- `covers` relationships to `connection`, `data_sink` or `part` objects.

## Outputs

- A `processing_activity` object type exported in `semantic.exports`.
- `ProcessingActivity.json`, `ProcessingActivityFrontmatter.json`, `ProcessingRole.json`, a manifest entry and an authoring skeleton.
- A required-relation declaration that reports an activity with no `covers` edge.

## Behavior

### Frontmatter

- `ProcessingActivity` SHALL require `role`, `controller` and a non-empty `home_regions` list.
- `role` SHALL be exactly `controller` or `processor`.
- When `role` is `controller`, `controller` SHALL be one non-empty name-and-contact string; `purposes`, `data_subject_categories` and `retention` SHALL each be present and non-empty.
- When `role` is `processor`, `processor` SHALL be a non-empty name-and-contact string for the processor itself, and `controller` SHALL be a non-empty list of non-empty name-and-contact strings, one for each controller it acts for. `purposes`, `data_subject_categories` and `retention` MAY be absent; the dossier takes categories of processing from covered sinks.
- `joint_controllers` SHALL be an optional list of non-empty name-and-contact strings for a controller activity. `representative` and `dpo_contact` SHALL be optional non-empty text.
- Each `home_regions` member SHALL be an ISO 3166-1 alpha-2 country code or `eu` or `eea`, using the same vocabulary as `data_sink.region`.
- The schema SHALL NOT provide a default for any authored field or derive a value from another field.

### Coverage edges

- The module manifest SHALL declare the `processing_activity` object type and allow `covers` targets of `connection`, `data_sink` and `part`.
- The manifest SHALL declare a required-relation check for outgoing `covers` edges to those types. When an activity has no such edge, Quire SHALL emit a located warning naming the activity and the declared check; the warning is advisory and does not make `quire validate` exit non-zero.
- A `covers` edge to any other object type or to a missing target SHALL fail validation with a located edge diagnostic.
- A `covers` edge to a `queue` SHALL fail as a wrong-kind edge.

### Skeleton

- The `processing_activity` skeleton SHALL show both role forms, the required fields for each form and a valid `covers` edge.
- The skeleton SHALL validate with `quire validate`.

### Dossier flow facts

- The module SHALL select authored `role`, `controller` and `home_regions` fields on `processing_activity`, and any authored `processor`, `joint_controllers`, `representative`, `dpo_contact`, `purposes`, `data_subject_categories` and `retention` fields, in `traceability.flow_rules`.
- The module SHALL select outgoing `covers` targets on `processing_activity` and outgoing `delivers_to` targets on `part` in `traceability.flow_rules`, so FR-096 facts can carry those authored edges.
- The module SHALL select `processor`, `audience_roles`, `region` and `purpose` on `data_sink`, and `title` on `data_classification`, so a downstream dossier can report these authored facts.
- These selectors SHALL NOT emit a finding for a source document with an authored `id`; they expose facts without judging the data-flow model.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-028-AC-1 | A controller activity with controller details, purposes, data-subject categories, retention, home regions and a valid `covers` edge validates. | Test |
| FR-028-AC-2 | A processor activity with a processor name and contact, a non-empty controller list and home regions validates without `purposes`, `data_subject_categories` or `retention`. | Test |
| FR-028-AC-3 | A controller activity without `retention`, `purposes` or `data_subject_categories`, and a processor activity without its own `processor` identity/contact or with an empty controller list, each fail with a diagnostic naming the missing or invalid field. | Test |
| FR-028-AC-4 | An unknown role, an empty home-region list, or a home-region value outside the stated vocabulary fails validation. | Test |
| FR-028-AC-5 | A `processing_activity` with no `covers` edge emits a located warning naming the activity and declared check; an edge to a `connection`, `data_sink` or `part` validates. | Test |
| FR-028-AC-6 | A `covers` edge to a `queue` fails with a wrong-kind diagnostic, and an edge to an absent target fails with a dangling-target diagnostic. | Test |
| FR-028-AC-7 | The module exports `processing_activity`; its generated schema and skeleton pass the module schema-drift and `quire validate` checks. | Test |
| FR-028-AC-8 | Omitting any optional authored field leaves it absent in the extracted record; no omitted value is populated from another field, artifact, code or runtime source. | Test |
| FR-028-AC-9 | FR-096 flow rules expose activity `role`, `controller`, `home_regions`, and any authored `processor`, `joint_controllers`, `representative`, `dpo_contact`, `purposes`, `data_subject_categories` and `retention`; activity `covers` and part `delivers_to` edges; sink `processor`, `audience_roles`, `region` and `purpose`; and classification `title`, without a finding on documents with an authored `id`. | Test |

## Dependencies

- **Upstream**: spec-objects-architecture `data_sink` and `connection` (PLAT-1532, PLAT-1535); spec-objects-security FR-023.
- **Downstream**: quoin FR-207, which reads this object to generate records of processing.
