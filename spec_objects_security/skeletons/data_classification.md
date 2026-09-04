---
id: CLASS-001
title: "DataRestricted"
type: data_classification
object: data_classification
---
<!-- data_classification authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: data_classification,
       object: data_classification.
     - "## Handling" (H2, required): how data of this class is handled.
     - "## Properties" (H2): the typed declaration. DataClassification.json
       requires a `level` row. -->
# [CLASS-001] DataRestricted

## Handling

- Encrypted at rest with TenantDataEncryptionKey and in transit with TLS 1.3.
- Never written to application logs, traces, or error payloads.
- Exported only under ExportTenantData, and only to the owning tenant.
- Deleted within the retention period once the tenant contract ends.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| classification_id | UUID | 1..1 | identity |
| level | String | 1..1 | minLength: 1 |
| retention | Duration | 1..1 |  |
| logging_permitted | Boolean | 1..1 |  |
