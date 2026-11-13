---
id: FR-021
title: "Default source profiles list only publishable clause sets and degrade while a pack is missing"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/FR-020"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-181"
    type: "depends_on"
---
# FR-021: Default source profiles list only publishable clause sets and degrade while a pack is missing

## Description

The module ships three default profiles. Each lists only clause sets whose sources are free to publish: NIST and OWASP
publications and public law.

| Profile `name` | Intended sources |
|----------------|------------------|
| `us-device-cybersecurity-hipaa` | US device cybersecurity statute and FDA guidance, and the HIPAA Security Rule |
| `eu-device-gdpr-ai-act` | EU device regulation cybersecurity, GDPR, and the AI Act |
| `web-app-baseline` | NIST and OWASP application security |

The packs these profiles draw on are specified and published by other tickets: the US pack by PLAT-1593 and PLAT-1612,
the GDPR set by PLAT-1627, and the NIST and OWASP sets by their own pack work. This requirement authors no pack. A
profile lists a set's key in the same change that publishes the set, taking the key from the pack, so no profile names
a key that no pack declares. Until then the profile is shipped with the sets that exist, or not shipped, and
[quoin FR-181](ix://agent-ix/quoin/FR-181) reports any listed set a machine lacks as `unavailable`.

A profile's `context` states only facts the profile name itself implies (for example that the product is a medical
device in the named market). It SHALL NOT state a fact about the particular product, such as its safety class or
whether it processes patient data; the repository supplies those in its selection file
([quoin FR-180](ix://agent-ix/quoin/FR-180)).

## Behavior

- The module SHALL ship profiles named `us-device-cybersecurity-hipaa`, `eu-device-gdpr-ai-act` and `web-app-baseline` once at least one publishable set is available for each.
- A shipped profile SHALL list only clause sets that declare rights allowing their text to be published, or that carry no text.
- A shipped profile SHALL list a key only if some published module declares that key.
- A shipped profile SHALL NOT name a pack whose standard text is licensed.
- A shipped profile's `context` SHALL hold no entry that describes a particular product.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-021-AC-1 | Every shipped profile validates under [FR-020](./FR-020-source-profile-format.md). | Test |
| FR-021-AC-2 | For every key in every shipped profile, a module in the reference module set declares that key; a profile listing an undeclared key fails the test. | Test |
| FR-021-AC-3 | For every key in every shipped profile, the declaring set's rights permit publication (`text` is `none` or `original`, `structure` is `original` or `citation_only`). | Test |
| FR-021-AC-4 | Each `context` entry of a shipped profile states a market or product-kind fact implied by the profile name; none states a fact about a particular product (safety class, data processed). | Inspection |
| FR-021-AC-5 | Evaluating each shipped profile with only part of its sets installed reports the missing sets `unavailable` and evaluates the rest. | Test |
| FR-021-AC-6 | The module's published files contain no name of a licensed pack. | Inspection |

## Dependencies

- **Upstream**: [FR-020](./FR-020-source-profile-format.md); `agent-ix/quoin` FR-181; pack tickets PLAT-1593, PLAT-1612, PLAT-1627 (by id only)
