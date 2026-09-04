---
id: AUDIT-001
title: "TokenReuseDetected"
type: audit_event
object: audit_event
---
<!-- audit_event authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: audit_event,
       object: audit_event.
     - "## Properties" (H2): the declared payload as typed rows. An audit
       event declaration carries NO identity field (occurrence identity
       belongs to the runtime record) and at least one `Timestamp`
       occurrence field; no row carries a default.
     - "## Event Schema" (H2, required) holds a fenced `json` block. It is a
       derived, human-facing view; the typed table is the authority. -->
# [AUDIT-001] TokenReuseDetected

TokenReuseDetected is emitted when an already-rotated refresh token is
presented. The whole grant family is revoked and the session terminated.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| occurred_at | Timestamp | 1..1 |  |
| actor_reference | String | 1..1 | minLength: 1 |
| grant_family_reference | String | 1..1 | minLength: 1 |
| source_address | String | 0..1 | minLength: 1 |

## Event Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://specs.agent-ix.dev/audit/token-reuse-detected.schema.json",
  "title": "TokenReuseDetected",
  "type": "object",
  "required": ["occurred_at", "actor_reference", "grant_family_reference"],
  "properties": {
    "occurred_at": { "type": "string", "format": "date-time" },
    "actor_reference": { "type": "string", "minLength": 1 },
    "grant_family_reference": { "type": "string", "minLength": 1 },
    "source_address": { "type": "string", "minLength": 1 }
  }
}
```
