---
id: FR-030
title: "A requirement a SOUP record serves is asked for the requirements placed on that SOUP"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-security/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-security/FR-010"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-013"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-058"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-086"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-041"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-161"
    type: "references"
---
# FR-030: A requirement a SOUP record serves is asked for the requirements placed on that SOUP

## Description

A third-party component that a requirement relies on needs its own stated requirements: the functions and
performance the product expects of it. Quoin FR-161 has an activity kind `soup-requirements` that reads a
**design relation** by name, one row per requirement. No default module declared such a relation, so a class
policy that asked for the activity was refused. This requirement declares it.

### Why the relation is per requirement and not per record

[FR-013](./FR-013-soup-record-serves-requirement.md) reads the `serves` list from the `soup_record` end
(`from: soup_record`). The design-element join (`agent-ix/quire-rs` FR-086) and the class report (quoin FR-161) are
per requirement, so a relation whose `from` is a `soup_record` can never give a requirement a row. A separate
requirement that merely constrains a SOUP record, with an edge to the record, would also give no per-requirement
row: the record is the target, and the requirement a class policy asks about has no edge of its own to read. The
relation here therefore has an `FR` or `NFR` as `from`.

### The statement

A person states the requirements placed on a SOUP item as ordinary `FR` or `NFR` documents. A requirement that
a SOUP record references (an incoming `references` edge from a `soup_record`) is asked for at least one such
statement: an `FR` or `NFR` that authors the new verb `soup_requirement_for` toward it. The tool never writes the
edge, never judges the statement, and assigns no score, class or acceptability; a person decides whether the stated
requirements are right.

The verb is **new**, because no verb of the `spec-artifacts-iso` registry means this. `references` and `satisfies`
mean other facts and would make the relation satisfiable by an unrelated link. The verbs `constrains` (an FR or NFR imposes a
constraint on the target) and `specifies` (an object FR specifies a behavioral FR) are already allowed on `FR`, and `constrains` on
`NFR`, but each states a different fact: a constraint on, or a specification of, the target requirement itself, not a requirement
placed on the SOUP item that serves it. Counting either as the statement would let an unrelated constraint satisfy the relation, and
widening their meaning would change every existing use. The module declares it in its own
`edge_types`, as it declares `scopes` and `considers`, so it relies on no other module for the verb. The verb is
authored on the requirement that states the SOUP requirements and targets the requirement the SOUP serves. Its inverse
`has_soup_requirement` lets the served requirement author the same fact toward the statement without editing it
(`agent-ix/quire-rs` FR-041).

### Scope

A requirement is in scope when any incoming `references` edge from a resolved `soup_record` reaches it. The scope is the
`when_any` of `agent-ix/quire-rs` FR-058: `when_any: [{verb: references, direction: incoming, other: [soup_record]}]`. The
`serves` list of FR-013 is one source of such an edge, and the engine harvests the same verb from body links (FR-013), so a
record that body-links a requirement it does not serve also puts that requirement in scope, and it is then asked for the
statement. That is the consequence of reading the verb as authored; a person who does not want it removes the body link or
maps the finding key `off`. A requirement no `soup_record` references yields no row and no finding. Unscoped, the relations
would report every requirement in the corpus, so the Behavior section requires the scope.

### Effect on the other readers of `design_relations`

Naming the two relations in `design_relations` makes the join of `agent-ix/quire-rs` FR-086 carry them, in module order after the
relations of other modules (FR-086-CON-1). The readers below take the join as it is; this module owns only the declaration:

- The quire design matrix gate (`agent-ix/quire-cli` FR-043, `quire matrix --strict`) and the quoin matrix design column
  (quoin FR-165) read the join verbatim. A missing SOUP-requirements edge is a design gap there only for a requirement in the scope above, and for no other.
- A quoin class policy (quoin FR-161) entry `design-trace` with no `relation`, and a `detailed-design` entry with no `relation`, read these
  relations like any other design relation. Once the `design-trace` `relation` key of quoin FR-161 exists (quoin PR #1042; today FR-161 refuses a `design-trace` entry that names a relation), a policy can pin `design-trace` to one relation by naming it. A `soup-requirements` entry
  names one of the two relations.
- The dossier readers (quoin FR-193, FR-194) read the join verbatim.

The `design-trace` `relation` key is quoin FR-161's, so it is a stated dependency (see Dependencies) and not behavior of this module.

### Consistency with the module's declared dependencies (PLAT-1852)

The scope uses `references` and the relation names `FR` and `NFR`, all declared by `spec-artifacts-iso`, as FR-013
already does. This requirement adds no import of its own: the module's declaration of the edge-type modules it uses
is PLAT-1852's. This requirement only ensures it introduces no further unregistered verb, because its one new verb is
declared in this module's `edge_types`. In a corpus where no loaded module declares `FR` or `NFR` and none exists, the
relations report `trace:undeclared-relation-vocabulary` as `agent-ix/quire-rs` FR-058 states.

## Inputs

- Documents of type `FR` and `NFR`, and `soup_record` documents whose `serves` entries name them.
- The `spec-artifacts-iso` and `spec-objects-security` manifests loaded together.

## Outputs

- Edge verb `soup_requirement_for` (category `traceability`) with `inverse: has_soup_requirement` in `edge_types`.
- Two `required_relations` entries and two names in `traceability.design_relations`.
- Advisory findings `fr-without-soup-requirements` and `nfr-without-soup-requirements`.

## Behavior

- The manifest SHALL declare `soup_requirement_for` with `inverse: has_soup_requirement` and `category: traceability` in `edge_types`.
- The manifest SHALL declare the relation `fr-has-soup-requirements` with `from: FR`, `edges: [soup_requirement_for]`, `to: [FR, NFR]`, `direction: incoming`, `check: fr-without-soup-requirements` and `when_any: [{verb: references, direction: incoming, other: [soup_record]}]`.
- The manifest SHALL declare the relation `nfr-has-soup-requirements` with the same fields and `from: NFR`, `check: nfr-without-soup-requirements`.
- The manifest SHALL list `fr-has-soup-requirements` and `nfr-has-soup-requirements`, in that order, in `traceability.design_relations`.
- Quire SHALL report a requirement that a resolved `soup_record` references and that has no incoming `soup_requirement_for` edge, or `has_soup_requirement` edge it authors itself, to or from a resolved `FR` or `NFR`.
- Quire SHALL report nothing for a requirement no resolved `soup_record` references.
- Quire SHALL report nothing for a served requirement with such an edge, whether the edge is authored by the statement or as `has_soup_requirement` by the served requirement.
- Each finding SHALL be a warning, tunable on `trace:fr-without-soup-requirements` and `trace:nfr-without-soup-requirements`.
- The relations SHALL NOT read, set or require a score, class, acceptability or approval value.
- The manifest SHALL declare each relation of this requirement with the `when_any` above and no relation without it.
- The manifest SHALL keep FR-013's `soup-record-serves-requirement` relation out of `design_relations`.
- The manifest SHALL leave FR-013's `soup-record-serves-requirement` declaration unchanged.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-030-AC-1 | The manifest declares `soup_requirement_for` with inverse `has_soup_requirement` and category `traceability`, the two relations with the fields and `when_any` stated above, and `design_relations` listing exactly those two names in that order; the module loads without a declaration error. | Test |
| FR-030-AC-2 | Over a fixture where a `soup_record` serves an `FR` and no document states SOUP requirements for it, `quire relations --json` reports that `FR` `uncovered` in `fr-has-soup-requirements` and `quire validate --okf` yields one `fr-without-soup-requirements` finding naming it. | Test |
| FR-030-AC-3 | Adding an `FR` that authors `soup_requirement_for` toward the served `FR` makes it `covered` with that `FR` linked and removes the finding; authoring `has_soup_requirement` from the served `FR` toward the statement gives the same result and no `disallowed-edge-type` warning. | Test |
| FR-030-AC-4 | An `FR` and an `NFR` that no `soup_record` serves yield no row and no finding in either relation. | Test |
| FR-030-AC-5 | A `references` edge, a `satisfies` edge or an edge from a document of another kind toward the served requirement leaves it `uncovered`; an edge authored by an `NFR` statement toward a served `FR` satisfies `fr-has-soup-requirements`, because `to` names both kinds. | Test |
| FR-030-AC-6 | `--severity trace:fr-without-soup-requirements=error` promotes the finding and the run exits non-zero; mapping the key `off` drops it. | Test |
| FR-030-AC-7 | The `soup-record-serves-requirement` relation of FR-013 keeps its declaration and is absent from `design_relations`; the `soup_record` type still declares no `allowed_links`. | Test |
| FR-030-AC-8 | Over the same fixture, `quoin class obligations` with a `soup-requirements` entry naming `relation: fr-has-soup-requirements` reads the `FR` row `unmet` before the statement and `met` after it, and reports `not-available` for an `FR` no record serves. | Demonstration |
| FR-030-AC-9 | Over a fixture where a `soup_record` serves an `NFR` and no document states SOUP requirements for it, the `NFR` is `uncovered` in `nfr-has-soup-requirements` with one `nfr-without-soup-requirements` finding; an `FR` or `NFR` authoring `soup_requirement_for` toward it makes it `covered` and removes the finding; `--severity trace:nfr-without-soup-requirements=error` promotes it and mapping the key `off` drops it. | Test |
| FR-030-AC-10 | A `soup_record` whose body links an `FR` it does not list in `serves` puts that `FR` in scope, so it is `uncovered` until a statement exists. | Test |
| FR-030-AC-11 | Over a corpus loading this module and spec-objects-architecture, the join of `agent-ix/quire-rs` FR-086 lists the two relations of this module in `design_relations` order after the relations of the modules loaded before it. Over the fixture of AC-2, `quire matrix --strict` (`agent-ix/quire-cli` FR-043) exits 1 with a stderr line naming the document and `fr-without-soup-requirements`; for a requirement outside the scope, no `fr-has-soup-requirements` or `nfr-has-soup-requirements` block or gap appears (blocks of other relations are unaffected). | Test |

## Constraints

| ID | Constraint | Type | Validation |
|----|-----------|------|------------|
| FR-030-CON-1 | The declaration SHALL add no object type and no engine behavior: it is `edge_types` and `traceability` data only. | Scope | Inspection |
| FR-030-CON-2 | The module SHALL NOT write or infer a `soup_requirement_for` edge. | Design | Inspection |
| FR-030-CON-3 | A finding SHALL name only the absence of a stated requirement. | Design | Inspection |

## Dependencies

- **Upstream**: [FR-013](./FR-013-soup-record-serves-requirement.md); `agent-ix/quire-rs` FR-058 (`when_any`), FR-086 (design join; a design relation is read over the same population as the finding), FR-041 (inverse labels); quoin FR-161 (the `soup-requirements` kind, which names the relation, and the `design-trace` `relation` key, which lands with quoin PR #1042).
- **Cross-repository**: `spec-artifacts-iso` does not list `soup_requirement_for` or `has_soup_requirement` in the `allowed_links` of `FR` and `NFR`; until it does, authoring the verb draws the advisory `disallowed-edge-type` and the relation counts the edge regardless, being verb-based. Authoring the inverse from the served requirement avoids the warning. PLAT-1852 owns the module's declaration of the edge-type modules it uses.
- **Downstream**: quoin FR-161 (the class policy), quoin FR-165 and the dossier, which read the new design relations.
