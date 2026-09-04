"""The three security rules the schemas encode rather than describe.

The `default`-refusal rule is **defence in depth, not the primary gate**. The
pinned engine's typed-table reader refuses a `default:` constraint cell with
`semantic.unknown-constraint-keyword` (semantic-core's `ConstraintKeyword` is a
closed set with no `default` member), so no *extracted* record can carry
`FieldDecl.default` at all. The schema rule exists for the records that reach a
consumer without passing the Markdown reader — a generated-language fixture, a
frontend, a hand-built record — and that population is what the tests below
build.
"""

from __future__ import annotations

import json
import re

import pytest

from tests.conftest import (
    CLAUSE,
    DEFAULT_REFUSING,
    MODEL_OF,
    OBJECT_TYPES,
    REPO_ROOT,
    SCHEMAS_DIR,
    SEMANTIC_CORE_DIR,
    VOCABULARIES,
    field,
)

# The minimal valid record per type, before a default is added. Reused from the
# role-schema suite so the two cannot drift.
from tests.test_role_schemas import MINIMAL as BASE_RECORD  # noqa: E402

# Where a vocabulary is carried, so an invented member can be shown to fail.
VOCABULARY_CARRIER = {
    "Severity": (
        "Vulnerability",
        "severity",
        {"fields": [field("id", "UUID", identity=True), field("severity")]},
    ),
    "Likelihood": (
        "Risk",
        "likelihood",
        {
            "fields": [
                field("id", "UUID", identity=True),
                field("likelihood"),
                field("impact"),
            ]
        },
    ),
    "Impact": (
        "Risk",
        "impact",
        {
            "fields": [
                field("id", "UUID", identity=True),
                field("likelihood"),
                field("impact"),
            ]
        },
    ),
    "StrideCategory": (
        "Threat",
        "stride_category",
        {"fields": [field("id", "UUID", identity=True), field("stride_category")]},
    ),
    "ControlEffectiveness": (
        "Control",
        "effectiveness",
        {"clauses": [CLAUSE], "fields": [field("effectiveness")]},
    ),
    "FindingStatus": (
        "AuditFinding",
        "status",
        {"fields": [field("id", "UUID", identity=True), field("status")]},
    ),
    "ConfidentialityLevel": (
        "DataClassification",
        "level",
        {"fields": [field("id", "UUID", identity=True), field("level")]},
    ),
    "TrustLevel": (
        "TrustBoundary",
        "trust_level",
        {
            "clauses": [CLAUSE],
            "fields": [field("id", "UUID", identity=True), field("trust_level")],
        },
    ),
    "SecretLifecycle": (
        "Secret",
        "lifecycle",
        {"fields": [field("id", "UUID", identity=True)]},
    ),
    "MfaFactorKind": (
        "MfaMethod",
        "factor_kind",
        {"fields": [field("id", "UUID", identity=True)]},
    ),
}


def schema(model: str) -> dict:
    return json.loads((SCHEMAS_DIR / f"{model}.json").read_text())


def default_keywords(node, path=("#",)) -> list[str]:
    """Every `default` in **schema position**.

    The discriminator matters: semantic-core's `FieldDecl` and this module's
    `DefaultedField.json` both declare a *property* literally named `default`,
    which is a key of a `properties` object and not a JSON Schema keyword. A
    naive substring or key scan reports those as violations and the criterion
    then means nothing. Keyword containers whose keys are names, not schema
    keywords, are descended into by value only; `enum` and `const` subtrees are
    not schemas at all and are skipped.
    """
    found: list[str] = []
    if isinstance(node, list):
        for index, item in enumerate(node):
            found += default_keywords(item, path + (str(index),))
        return found
    if not isinstance(node, dict):
        return found
    if "default" in node:
        found.append("/".join(path))
    for key, value in node.items():
        if key in ("enum", "const"):
            continue
        if key in ("properties", "$defs", "patternProperties", "dependentSchemas"):
            if isinstance(value, dict):
                for name, sub in value.items():
                    found += default_keywords(sub, path + (key, name))
            continue
        if key == "required":
            continue
        found += default_keywords(value, path + (key,))
    return found


@pytest.mark.trace("TC-070", "FR-006-AC-1")
def test_every_vocabulary_is_closed_over_exactly_its_declared_members():
    assert len(VOCABULARIES) == 10
    for name, (members, _) in VOCABULARIES.items():
        doc = schema(name)
        assert doc["type"] == "string", name
        assert doc["enum"] == members, name
        assert set(doc) <= {"$schema", "$id", "type", "enum", "description"}, name


@pytest.mark.trace("TC-071", "FR-006-AC-2")
def test_the_unassessed_member_validates_and_an_invented_member_fails(
    schema_registry,
):
    """Property-shaped over the ten vocabularies: for every vocabulary, the
    unassessed member is admitted and no value outside the member list is."""
    for name, (members, unassessed) in VOCABULARIES.items():
        model, key, record = VOCABULARY_CARRIER[name]
        validator = schema_registry(model)
        assert unassessed in members, name
        assert validator.is_valid({**record, key: unassessed}), name
        for member in members:
            assert validator.is_valid({**record, key: member}), (name, member)
        for invented in ("assume_ok", "", "UNKNOWN", "definitely_fine"):
            assert not validator.is_valid({**record, key: invented}), (name, invented)


@pytest.mark.trace("TC-072", "FR-006-AC-3")
def test_no_shipped_schema_carries_a_default_keyword():
    offenders = {}
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        if path.name == "toolchain.json":
            continue
        hits = default_keywords(json.loads(path.read_text()))
        if hits:
            offenders[path.name] = hits
    assert not offenders, offenders
    # DefaultedField.json is the case that proves the discriminator works: it
    # declares a *property* named `default` and must not be reported.
    marker = json.loads((SCHEMAS_DIR / "DefaultedField.json").read_text())
    assert "default" in marker["properties"]
    assert default_keywords(marker) == []
    assert default_keywords({"type": "string", "default": "granted"}) == ["#"]


@pytest.mark.trace("TC-073", "FR-006-AC-4", "FR-006-CON-2")
def test_no_declaration_admits_a_defaulted_field_or_param(schema_registry):
    """Every one of the twenty-three types, not only the sensitive four.

    The rule began on `secret`, `encryption_key`, `jwt_claim` and `csrf_token`,
    which left it off exactly the rows that grant: a `Control` whose
    `effectiveness` defaulted to `effective`, a `TrustBoundary` whose
    `trust_level` defaulted to `trusted`, and defaulted grant rows on `role`,
    `permission` and `scope` all validated. The ticket's merge gate reads "No
    schema default grants permission, trust, or control effectiveness".
    """
    assert set(DEFAULT_REFUSING) == set(OBJECT_TYPES)
    for name in DEFAULT_REFUSING:
        model = MODEL_OF[name]
        validator = schema_registry(model)
        base = BASE_RECORD[model]
        properties = schema(model).get("properties", {})
        assert validator.is_valid(base), (name, "minimal record rejected")
        if "fields" in properties:
            embedded = {
                **base,
                "fields": list(base.get("fields", []))
                + [field("material", default="hunter2")],
            }
            assert not validator.is_valid(embedded), name
        if "operations" in properties:
            clean = {
                **base,
                "operations": [{"name": "rotate", "params": [field("reason")]}],
            }
            assert validator.is_valid(clean), name
            leaky = {
                **base,
                "operations": [
                    {"name": "rotate", "params": [field("material", default="hunter2")]}
                ],
            }
            assert not validator.is_valid(leaky), name


@pytest.mark.trace("TC-073", "FR-006-AC-4")
def test_the_defaulted_field_the_guard_refuses_is_valid_semantic_core():
    """The canary the code review earned.

    TC-073 used to pass for a reason unrelated to the rule: the fixture built
    `default: {"kind": "literal"}`, and `literal` is outside semantic-core's
    closed `DefaultKind`, so every "embedded" record was refused by `FieldDecl`
    before the module's own guard was consulted. Deleting the whole `allOf`
    from `Secret.json` left every assertion passing. This asserts the premise
    the rest of TC-073 rests on: the defaulted field is a *valid* `FieldDecl`,
    so the module's guard is what refuses it.
    """
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    resources = []
    for path in sorted(SEMANTIC_CORE_DIR.glob("*.json")):
        schema_doc = json.loads(path.read_text())
        resources.append((schema_doc["$id"], Resource.from_contents(schema_doc)))
    field_decl = Draft202012Validator(
        json.loads((SEMANTIC_CORE_DIR / "FieldDecl.json").read_text()),
        registry=Registry().with_resources(resources),
    )
    defaulted = field("material", default="hunter2")
    assert not [e.message for e in field_decl.iter_errors(defaulted)], defaulted
    assert defaulted["default"]["kind"] in ("semantic", "representation", "migration")


@pytest.mark.trace("TC-076", "FR-006-AC-7")
def test_no_negative_rule_depends_on_a_counting_keyword():
    """A negative item rule is `items: {not: …}`, never
    `contains` + `minContains: 0` + `maxContains: 0`.

    The counting form is the dangerous one: a validator that does not implement
    `minContains`/`maxContains` — which is exactly the generated-fixture and
    frontend population these rules exist for — reads the remaining `contains`
    as "at least one item MUST match", inverting "no defaulted field" into
    "must carry a defaulted field". `items`/`not` cannot invert.
    """
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        if path.name == "toolchain.json":
            continue
        text = path.read_text()
        assert "minContains" not in text, path.name
        assert "maxContains" not in text, path.name


@pytest.mark.trace("TC-075", "FR-006-AC-6")
def test_the_ordered_vocabularies_start_at_their_least_granting_member():
    """Two of the ten vocabularies are ordered by how much they grant, and for
    those the unassessed member is also the least-granting one. The other eight
    are unordered and their `unknown` member states only that nobody assessed
    it; no schema turns that into a grant."""
    effectiveness = schema("ControlEffectiveness")["enum"]
    assert effectiveness[0] == "not_assessed"
    assert "unknown" not in effectiveness
    trust = schema("TrustLevel")["enum"]
    assert trust[0] == "untrusted"
    for name, (members, unassessed) in VOCABULARIES.items():
        if name in ("ControlEffectiveness", "TrustLevel"):
            assert members[0] == unassessed, name
        else:
            assert unassessed == "unknown", name
    granting = {"allow", "granted", "trusted_by_default", "assume_effective"}
    for name in VOCABULARIES:
        assert not (set(schema(name)["enum"]) & granting), name


@pytest.mark.trace("TC-077", "FR-006-CON-1")
def test_no_vocabulary_member_expresses_assume_the_permissive_value():
    permissive = {
        "allow",
        "allowed",
        "granted",
        "grant",
        "permit",
        "permitted",
        "assume_effective",
        "assume_trusted",
        "trusted_by_default",
        "default",
        "any",
    }
    for name, (members, unassessed) in VOCABULARIES.items():
        assert not (set(members) & permissive), name
        assert unassessed in members, name


@pytest.mark.trace("TC-078", "FR-006-AC-8")
def test_the_change_carries_a_recorded_security_review():
    """The merge gate's "security review is required before release" as an
    artifact rather than a promise: a SpecReview document exists for this
    change and every finding it *owns* has a disposition.

    A finding is owned when it opens a row of the review's own Findings table.
    An id merely cited in prose belongs to another review and is dispositioned
    there; requiring a disposition for it here would make cross-referencing a
    sibling review impossible.
    """
    reviews = sorted((REPO_ROOT / "spec" / "reviews").rglob("*.md"))
    assert reviews, "no SpecReview was recorded for this change"
    assert [p for p in reviews if p.name == "security.md"], [p.name for p in reviews]
    for path in reviews:
        text = path.read_text()
        assert "## Dispositions" in text, path.name
        owned = set(re.findall(r"^\|\s*(FND-\d+)\s*\|", text, re.MULTILINE))
        assert owned, path.name
        tail = text.split("## Dispositions")[-1]
        cited = set(re.findall(r"FND-\d+", tail))
        ranges = [
            (int(a), int(b))
            for a, b in re.findall(r"FND-(\d+)\s*\.\.\s*(?:FND-)?(\d+)", tail)
        ]
        missing = set()
        for finding in owned:
            number = int(finding.split("-")[1])
            if finding in cited:
                continue
            if any(low <= number <= high for low, high in ranges):
                continue
            missing.add(finding)
        assert not missing, (path.name, sorted(missing))
