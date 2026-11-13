---
id: FR-021
title: "Default source profiles list only publishable clause sets"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-020"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-181"
    type: "depends_on"
---
# FR-021: Default source profiles list only publishable clause sets

## Description

The module ships up to three default profiles, under these names and no others. Each lists only clause sets whose
sources are free to publish: NIST and OWASP publications and public law.

| Profile `name` | Intended sources |
|----------------|------------------|
| `us-device-cybersecurity-hipaa` | US device cybersecurity statute and FDA guidance, and the HIPAA Security Rule |
| `eu-device-gdpr-ai-act` | EU device regulation cybersecurity, GDPR, and the AI Act |
| `web-app-baseline` | NIST and OWASP application security |

The clause sets these profiles draw on are specified and published by other work (PLAT-1593, PLAT-1612, PLAT-1627,
PLAT-1521, PLAT-1522). This requirement authors no set. A change that publishes a set for an intended source also adds
that set's key to the matching profile, creating the profile if it does not exist, and takes the key from the set. A
profile is therefore never shipped listing a key that no module declares. A machine that lacks a listed set is handled
by [quoin FR-181](ix://agent-ix/quoin/FR-181), not here.

The reference module set used by the tests is the modules that `quoin module ensure-defaults` installs, together with
this module.

A profile's `context` states only a market or product-kind fact the profile name implies (for example that the product
is a medical device in the named market). It states no fact about the particular product, such as its safety class or
whether it processes patient data. For `web-app-baseline` the NIST baseline and the ASVS level, which PLAT-1521 and
PLAT-1522 make applicability dimensions, are product facts: the profile binds neither, and the repository supplies them
in its selection `context` ([quoin FR-180](ix://agent-ix/quoin/FR-180)). Until it does, the clauses that need them are
reported `unresolved`.

## Behavior

- The `profiles/` directory SHALL contain no profile whose `name` is not in the table above.
- When a change publishes a clause set for an intended source in the table, that change SHALL list the set's key in the matching profile.
- A shipped profile SHALL list only keys that a module in the reference module set declares.
- A shipped profile SHALL list only keys whose declaring module the engine's publishability check (`check_publishable`, run by `quire publish-check`) accepts, with no further rights test of its own.
- A shipped profile SHALL NOT name a pack whose standard text is licensed.
- A shipped profile's `context` SHALL hold no entry that describes a particular product.
- A shipped profile SHALL bind no NIST baseline or ASVS level.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-021-AC-1 | Every shipped profile passes the FR-020 profile test. | Test |
| FR-021-AC-2 | For every key in every shipped profile, a module in the reference module set declares that key; a profile listing an undeclared key fails the test. | Test |
| FR-021-AC-3 | For every key in every shipped profile, `quire publish-check --module <declaring module>` exits 0. | Test |
| FR-021-AC-4 | Each `context` entry of a shipped profile states a market or product-kind fact implied by the profile name; none states a fact about a particular product (safety class, data processed). | Inspection |
| FR-021-AC-5 | The set of `name` values in `profiles/` is a subset of the three names in the table; an extra profile fails the test. | Test |
| FR-021-AC-6 | The module's published files contain no name of a licensed pack. | Inspection |
| FR-021-AC-7 | `web-app-baseline`, if shipped, has no `context` entry for the NIST baseline or the ASVS level dimension. | Test |
| FR-021-AC-8 | A change that adds a clause set for an intended source and does not list its key in the matching profile is rejected at review. | Inspection |

## Dependencies

- **Upstream**: [FR-020](./FR-020-source-profile-format.md); `agent-ix/quoin` FR-181; clause-set work tracked as PLAT-1593, PLAT-1612, PLAT-1627, PLAT-1521, PLAT-1522
