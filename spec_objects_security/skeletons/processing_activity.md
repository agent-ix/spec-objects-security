---
id: PA-001
title: CustomerSupportProcessing
type: processing_activity
object: processing_activity
role: controller
controller: "Example Services Ltd; privacy@example.invalid"
purposes:
  - "Respond to customer support requests"
data_subject_categories:
  - "Customers"
retention: "Support records are retained for the documented support period."
home_regions:
  - eu
relationships:
  - target: CONN-001
    type: covers
---
<!-- Processing activity authoring skeleton. Choose one role form:

Controller form:
  role: controller
  controller: "name and contact"
  purposes: ["... at least one purpose"]
  data_subject_categories: ["... at least one category"]
  retention: "..."

Processor form (use this form instead of the controller fields above):
  role: processor
  processor: "processor name and contact"
  controller:
    - "controller name and contact"
  # purposes, data_subject_categories and retention may be omitted; categories
  # of processing are read from covered data sinks.

Both forms require at least one home_regions entry and a covers relationship
to a connection, data_sink or part. Region entries follow data_sink.region:
ISO 3166-1 alpha-2, eu or eea. Do not infer any omitted field. -->
# [PA-001] Customer support processing

Describe the person-authored context that is not present in the flow model.
State what the activity covers, how the named purposes apply, and where the
declared relationships begin and end. List facts that are unavailable under
Gaps; do not infer a missing value from code, a sink name, or runtime behavior.
