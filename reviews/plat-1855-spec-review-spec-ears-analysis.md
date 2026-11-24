---
id: SR-1624
title: "EARS analysis — FR-030 SOUP-requirements design relation and FR-013 wording"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-objects-security; spec/functional/FR-030-soup-requirements-design-relation.md, spec/functional/FR-013-soup-record-serves-requirement.md, spec/functional/index.md"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-objects-security/FR-030
    type: reviews
  - target: ix://agent-ix/spec-objects-security/FR-013
    type: reviews
---
# SR-1624: EARS analysis — FR-030 SOUP-requirements design relation and FR-013 wording

## Summary

Ticket: PLAT-1855; PR agent-ix/spec-objects-security#79 at head `1a9075387ab1678d9c269b85170454d3d1d30b0d`, scope `git diff origin/main...HEAD` (FR-030 new, FR-013 three wording edits, index line).

## Verdict

**PASS with two low findings.** Every FR-030 Behavior bullet and constraint carries one SHALL or SHALL NOT with a single subject (the manifest, Quire, the relations, the module). The three FR-013 edits are wording only and keep the one-obligation form. No acceptance criterion assigns a score, class or acceptability; FR-030 states the tool assigns none. No standard text is quoted; the diff carries no pins, SHAs or counts. `quire validate --scope .` on FR-030 and FR-013 exits 0; the only output, `DuplicateModuleName: 'spec-objects-security' declared at 2 path(s); first-wins`, is environmental (it appears equally for the unchanged FR-029 on this checkout and for `spec-objects-architecture` validated in its own checkout: the repo's own manifest plus the installed module).

Examined units:

- `FR-030` Behavior bullets 1-11 (role: examined): each one SHALL / SHALL NOT.
- `FR-030-CON-1..3` (role: examined): single obligations, Inspection.
- `FR-013` statement edit "this requirement introduces no link verb" (role: examined).
- `FR-013` Outputs edit and `FR-013-AC-1` edit "a `required_relations` entry named `soup-record-serves-requirement`" (role: examined).
- `FR-013` Dependencies downstream edit (role: examined).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | Behavior bullet "Quire SHALL report a requirement served by a `soup_record` that has no incoming `soup_requirement_for` edge from a resolved `FR` or `NFR`" has an ambiguous relative clause (the record or the requirement has no edge) and names only the forward verb, while the next bullet and FR-058 counterpart reading also accept `has_soup_requirement` authored by the served requirement | spec/functional/FR-030-soup-requirements-design-relation.md:86 |
| FND-002 | low | A normative SHALL NOT sits in Description prose ("the relations SHALL NOT be declared without that scope"), outside Behavior and with no AC of its own; it duplicates the `when_any` field already fixed by the Behavior bullets and AC-1 | spec/functional/FR-030-soup-requirements-design-relation.md:57-59 |
