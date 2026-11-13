---
id: SOUP-001
title: "ExampleHttpClient"
type: soup_record
object: soup_record
purl: "pkg:cargo/example-http-client@1.4.2"
---
<!-- soup_record authoring skeleton (spec-objects-security). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: soup_record,
       object: soup_record and purl, the component's package URL, which is
       its identity. name, version, supplier and license are optional
       and take the SBOM's value or the literal `unknown`; a value nobody has stated is
       left out, never defaulted.
     - "## Properties" (H2): the typed declaration. SoupRecord.json requires
       an identity field and a `purl` row, and refuses a defaulted field. -->
# [SOUP-001] ExampleHttpClient

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| component_id | UUID | 1..1 | identity |
| purl | String | 1..1 | minLength: 1 |
| supplier | String | 0..1 |  |
