---
id: MFA-001
title: "TimeBasedOneTimeCode"
type: mfa_method
object: mfa_method
kind: totp
factor: possession
---
<!-- mfa_method authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: mfa_method, object: mfa_method
       and kind; factor is optional.
     - "## Properties" (H2): the typed declaration. MfaMethod.json admits no
       field carrying a default, so no enrolment value can be embedded. -->
# [MFA-001] TimeBasedOneTimeCode

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| method_id | UUID | 1..1 | identity |
| factor_kind | String | 1..1 | minLength: 1 |
| code_digits | Integer | 1..1 | min: 6, max: 8 |
| step_period | Duration | 1..1 |  |
| seed_locator | String | 1..1 | minLength: 1 |
