---
id: CSRF-001
title: "SessionAntiForgeryToken"
type: csrf_token
object: csrf_token
rotation_window: PT30M
---
<!-- csrf_token authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: csrf_token, object: csrf_token
       and rotation_window.
     - "## Properties" (H2): CsrfToken.json admits no field carrying a
       default, so no token value appears in the declaration. -->
# [CSRF-001] SessionAntiForgeryToken

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| token_id | UUID | 1..1 | identity |
| locator | String | 1..1 | minLength: 1 |
| bound_session_attribute | String | 1..1 | minLength: 1 |
| rotation_window | Duration | 1..1 |  |
