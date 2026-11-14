---
id: SCOPEX-001
title: "ExampleClauseOutsideComponent"
type: scope_exclusion
object: scope_exclusion
---
<!-- scope_exclusion authoring skeleton (spec-objects-security). Contract
     (manifest body_extraction asserts, each section one inline-code value):
     - Frontmatter MUST carry id, title, type: scope_exclusion,
       object: scope_exclusion.
     - "## Set" (H2, required): the clause set key authority/id@version.
     - "## Clause" (H2, required): the clause id inside that set.
     - "## Responsible" (H2, required): the bare id of the bundle artifact for
       the component, service or document responsible for the clause.
     - "## Rationale" (H2, required): why the clause is outside this component.
     - "## Decision" (H2, required): delegated, accepted_risk or
       temporary_exception.
     - "## Decision owner" and "## Approval ref" (H2, required): the bare id
       of the decision owner artifact and an opaque approval reference.
     - "## Expires at" (H2, required only for temporary_exception): an RFC 3339
       instant with an explicit time zone.
     This declares a boundary and proposed disposition; it is not an approval. -->
# [SCOPEX-001] ExampleClauseOutsideComponent

## Set

`example.invalid/std@1`

## Clause

`EX-1`

## Responsible

`COMP-001`

## Rationale

`The deployment platform owns this clause for every service it hosts.`

## Decision

`temporary_exception`

## Decision owner

`SEC-OWNER-001`

## Approval ref

`APPROVAL-001`

## Expires at

`2026-11-14T12:00:00Z`
