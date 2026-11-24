---
id: SR-1625
title: "Integrity analysis — FR-030 SOUP-requirements design relation and FR-013 wording"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-objects-security; spec/functional/FR-030-soup-requirements-design-relation.md, spec/functional/FR-013-soup-record-serves-requirement.md, spec/functional/index.md"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-030
    type: reviews
  - target: ix://agent-ix/spec-objects-security/FR-013
    type: reviews
---
# SR-1625: Integrity analysis — FR-030 SOUP-requirements design relation and FR-013 wording

## Summary

Ticket: PLAT-1855; PR agent-ix/spec-objects-security#79 at head `1a9075387ab1678d9c269b85170454d3d1d30b0d`, scope `git diff origin/main...HEAD`. Engine and consumer claims were re-measured on origin/main of quire-rs, quire-cli, quoin, spec-artifacts-iso and spec-objects-architecture, not taken from the PR text or the ticket.

## Verdict

**FAIL (one medium finding) — not mergeable until FND-001 is settled in the spec.** The rest is consistent and verified:

- Manifest shape (origin/main `spec_objects_security/manifest.yaml`): no top-level `relations` or `checks`; relations live under `traceability.required_relations`; no `design_relations` key exists yet; FR-013's `soup-record-serves-requirement` is therefore outside `design_relations`, and FR-030 keeps it there (Behavior, AC-7). The existing FR-013-AC-1 test selects the relation by `from == soup_record`, so the two new `from: FR`/`from: NFR` relations do not disturb it.
- quire-rs FR-086 / `src/loader/mod.rs`: `design_relations` merge across modules in module order without duplicates (FR-086-CON-1), so security's two names append after spec-objects-architecture's `fr-has-design-element`, `nfr-has-design-element`.
- quire-rs FR-058 / `src/corpus/required_relations.rs` `in_scope_by_edge`: a `when_any` condition matches `e.edge_type == c.verb()` as authored against a resolved document of an `other` kind, with no inverse normalisation; `references` incoming from a `soup_record` is the authored harvest of `serves`. Rows are per `from` document (per requirement).
- quire-rs FR-058 CR-416 (AC-23) and FR-086: a relation listing `soup_requirement_for` also accepts its declared inverse `has_soup_requirement` authored by the served requirement.
- quire-rs FR-041 / `src/corpus/validate.rs`: an inverse label is type-allowed at Tier-1; at Tier-2 the normalised forward verb absent from the source's `allowed_links` is skipped, so the inverse spelling draws no `disallowed-edge-type` and no `disallowed-edge-target`. AC-3's claim holds; the forward spelling does draw the advisory Tier-1 warning, as the Cross-repository note says.
- spec-artifacts-iso origin/main: neither `soup_requirement_for` nor `has_soup_requirement` is in the `allowed_links` of `FR` or `NFR`, and neither name exists anywhere in the iso `edge_types` or any sibling module manifest (no FR-041 precedence collision). The stated dependency is accurate.
- PLAT-1852: FR-030 adds no new undeclared dependency. Its new verb is declared in this module's own `edge_types` (beside `scopes` and `considers`); `references`, `FR` and `NFR` are already used by FR-013 and `security-nfr-has-mitigation-target`.
- quoin FR-161 and `class_obligations.rs` on origin/main implement `soup-requirements` with a required `relation:` and the met / unmet / not-available reading AC-8 relies on.

Examined units:

- `FR-030` statement and Description sections (role: examined).
- `FR-030` Behavior bullets 1-11 and `FR-030-CON-1..3` (role: examined).
- `FR-030-AC-1..8` (role: examined).
- `FR-030` Dependencies, incl. Cross-repository note (role: examined).
- `FR-013` edited statement, Outputs, `FR-013-AC-1`, Dependencies (role: examined).
- `spec/functional/index.md` FR-030 line (role: examined).
- quire-rs FR-041, FR-058, FR-086; quire-cli FR-043; quoin FR-161, FR-165 (role: context_only).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | Listing the two relations in `traceability.design_relations` also feeds every consumer of the design join, and FR-030 neither states nor decides that: quoin FR-161 `design-trace` reads every design relation and is `unmet` if any row is `uncovered`, so a served FR that has a design element but no SOUP statement turns `unmet` (and gates under `gate: true`); a `detailed-design` entry with no `relation` reads them too; quire-cli FR-043 `quire matrix --strict` exits 1 on any live requirement with an `uncovered` design block; and the quoin FR-165 / quire-rs FR-092 design column lists the SOUP-statement FR/NFR as design elements of the served requirement. FR-030 calls the finding a warning but does not say that design-relation membership makes it a `--strict` matrix gate. The ticket's scope item 3 asks the spec to settle this | spec/functional/FR-030-soup-requirements-design-relation.md:85 |
| FND-002 | low | The scope is any incoming `references` edge from a resolved `soup_record`, which FR-013 says includes a body link from the record, but the Description says the requirement is in scope when it has "an incoming `serves` edge of FR-013"; a record's body link to an FR it does not serve puts that FR in scope | spec/functional/FR-030-soup-requirements-design-relation.md:42 |
| FND-003 | low | The rationale for a new verb rules out `references` and `satisfies` only; iso `constrains` ("Imposes a constraint on the target", inverse `constrained_by`) and `specifies` are already in the `FR` (and, for `constrains`, `NFR`) `allowed_links` and would avoid the advisory warning, so the FR should say why they do not mean this fact | spec/functional/FR-030-soup-requirements-design-relation.md:47-49 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-004 | low | The Effect section states as current fact that "A policy pins `design-trace` to one relation by naming it", but quoin origin/main FR-161-AC-12 refuses a `design-trace` entry naming a relation; that becomes true only when quoin PR #1042 (open) lands. The next line calls it "a stated dependency", yet Dependencies lists quoin FR-161 only for the `soup-requirements` kind, so the dependency is not stated. No contradiction with PR #1042's text | spec/functional/FR-030-soup-requirements-design-relation.md:76-80 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Verified in fix commit 3b08c0a (head 3b08c0a3a9a515b5cfb284e0fa37d79ea5ce3180). |
| FND-002 | fixed | Verified in fix commit 3b08c0a (head 3b08c0a3a9a515b5cfb284e0fa37d79ea5ce3180). |
| FND-003 | fixed | Verified in fix commit 3b08c0a (head 3b08c0a3a9a515b5cfb284e0fa37d79ea5ce3180). |
| FND-004 | fixed | Verified in fix commit 4eebba1 (head 4eebba194c163d1a1ddea3e6808a84a990c31d75). |
