---
id: SR-037
title: "Dependency review of PR #46 FR-008 constrained mitigation target"
type: SpecReview
analysis: dependency
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-008-security-nfr-needs-mitigation-target.md against agent-ix/quire-rs FR-058, FR-084, FR-085 (quire-rs#664) and agent-ix/quire-cli FR-030 (quire-cli#180) (PR #46 diff at 60b5bab)"
---
# SR-037: Dependency review of PR #46 FR-008 constrained mitigation target

## Summary

Ticket: PLAT-1520 (PR #46). FR-008 now depends on quire-rs FR-085 for
cross-repository resolution and kind mismatch, and is read by FR-084 as the
reverse view. Checked against the quire-rs#664 branch: FR-085 resolves an
`ix://<org>/<repo>/<ID>` edge to a loaded member, keeps an unloaded
repository `Dangling`, and reports a resolved target outside a non-empty
`to` as `trace:target-kind-mismatch`; FR-084's reverse view is a
`direction: outgoing` relation with `where`. FR-008's use of both matches,
and the new FR-058 paragraph agrees. `threat` and `risk` match the `from:`
of this module's own `threat-has-control` and `risk-has-treatment`.

Gaps: only `quire relations` (quire-cli FR-030 `--repo`) can load several
repositories, while FR-008's ACs run `quire validate --okf`; FR-085-AC-10's
single-member lexical resolution contradicts one FR-008 sentence; the
dependency edges are incomplete; and no implementation ticket covers this
repository (PLAT-1554 lists quire-rs and quire-cli, PLAT-1556 quire-rs).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | AC-3's "threat in another repository loaded into the corpus" has no `quire validate` surface: only `quire relations --repo` (quire-cli FR-030) loads several members, so under the `quire validate --okf` run AC-2/AC-5 use, the cross-repo arm cannot be exercised and every correct NFR whose threat is in a sibling repo warns with no way to clear it | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:72; tests/test_reverse_mitigates.py:116 |
| FND-002 | low | "An edge to a repository that is not loaded stays dangling" is false for a single-member corpus without identity: FR-085-AC-10 keeps FR-026 lexical `ix://` resolution, so `ix://agent-ix/other-repo/THREAT-001` resolves to a local THREAT-001 | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:35 |
| FND-003 | low | Dependency edges are incomplete and misdirected: FR-085 is depended on in the body but not declared `depends_on` in frontmatter (only FR-058 is), and FR-084 is listed as Upstream although it reads FR-008's declaration (Description line 37), making it downstream | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:12-13,37,79 |
| FND-004 | medium | No implementation ticket owns this repository's change: the `to: [threat, risk]` SHALL, the manifest entry and comment at spec_objects_security/manifest.yaml:684-691, and TC-116/TC-118 have no owner, since PLAT-1554 and PLAT-1556 list only quire-rs/quire-cli | spec/functional/FR-008-security-nfr-needs-mitigation-target.md:57 |

## Verdict

Changes requested (1 high, 1 medium, 2 low).
