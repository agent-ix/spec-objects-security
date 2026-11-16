"""The closed safeguards vocabulary and control links (FR-025)."""

from __future__ import annotations

import re

import pytest

from tests.conftest import CLAUSE, PACKAGE_ROOT, SKELETONS_DIR, field, frontmatter
from tests.test_regulated_categories import _extract, _schema
from tests.test_threat_model import errors, target_doc, validate


def _declared_safeguards() -> list[str]:
    source = (PACKAGE_ROOT.parent / "typespec" / "main.tsp").read_text()
    declaration = re.search(r"enum Safeguard\s*\{([^}]*)\}", source, re.DOTALL)
    assert declaration is not None
    return [
        literal or identifier
        for literal, identifier in re.findall(
            r"^\s*(?:`([^`]+)`|([A-Za-z_][A-Za-z0-9_]*))\s*,\s*$",
            declaration.group(1),
            re.MULTILINE,
        )
    ]


def _control_record(**extra) -> dict:
    return {
        "clauses": [CLAUSE],
        "fields": [field("effectiveness")],
        **extra,
    }


@pytest.mark.trace("TC-244", "FR-025-AC-8", "FR-025-AC-11")
def test_safeguard_and_frontmatter_schemas_are_closed_where_required(
    schema_registry,
):
    safeguard = _schema("Safeguard")
    assert safeguard["enum"] == _declared_safeguards()

    control = _schema("Control")
    safeguards = control["properties"]["safeguards"]
    assert safeguards["type"] == "array"
    assert safeguards["items"]["$ref"].endswith("/Safeguard.json")
    assert safeguards["minItems"] == 1
    assert safeguards["uniqueItems"] is True
    assert "default" not in safeguards
    assert "safeguards" not in control.get("required", [])

    record_schema = schema_registry("Control")
    assert record_schema.is_valid(_control_record(safeguards=["encrypt-in-transit"]))
    for invalid in (
        ["shield"],
        ["remove-from-sink"],
        [],
        [_declared_safeguards()[0], _declared_safeguards()[0]],
        "encrypt-in-transit",
    ):
        assert not record_schema.is_valid(_control_record(safeguards=invalid)), invalid

    control_frontmatter = _schema("ControlFrontmatter")
    assert (
        control_frontmatter["properties"]["safeguards"]["items"]["enum"]
        == safeguard["enum"]
    )
    assert "required" not in control_frontmatter
    assert schema_registry("ControlFrontmatter").is_valid(
        {"id": "CTRL-1", "safeguards": ["encrypt-in-transit"], "owner": "Ada"}
    )

    classification_frontmatter = _schema("DataClassificationFrontmatter")
    assert (
        classification_frontmatter["properties"]["regulated_categories"]["items"][
            "enum"
        ]
        == _schema("RegulatedDataCategory")["enum"]
    )
    assert schema_registry("DataClassificationFrontmatter").is_valid(
        {"id": "CLASS-1", "regulated_categories": ["health"], "owner": "Ada"}
    )
    assert not schema_registry("DataClassificationFrontmatter").is_valid(
        {"regulated_categories": ["medical"]}
    )


@pytest.mark.trace("TC-245", "FR-025-AC-8", "FR-025-AC-9")
def test_safeguards_are_optional_authored_frontmatter_and_the_skeleton_validates(
    tmp_path,
    quire_engine,
    semantic_block,
    semantic_module,
    bundle_index,
    schema_registry,
):
    skeleton = (SKELETONS_DIR / "control.md").read_text()
    result = validate(tmp_path, {"control.md": skeleton})
    assert result.returncode == 0 and not errors(result), result.stderr

    extracted = _extract(
        quire_engine,
        semantic_block,
        semantic_module,
        "control.md",
        skeleton,
        kind="control",
        bundle=bundle_index,
    )
    assert extracted["record"]["safeguards"] == ["encrypt-in-transit"]

    omitted = skeleton.replace("safeguards: [encrypt-in-transit]\n", "")
    omitted_result = validate(tmp_path, {"control.md": omitted})
    assert omitted_result.returncode == 0 and not errors(
        omitted_result
    ), omitted_result.stderr
    absent = _extract(
        quire_engine,
        semantic_block,
        semantic_module,
        "control-without-safeguards.md",
        omitted,
        kind="control",
        bundle=bundle_index,
    )
    assert "safeguards" not in absent["record"]

    invalid_values = (
        ("shield", ["shield"]),
        ("remove-from-sink", ["remove-from-sink"]),
        ("[]", []),
        (
            "duplicate",
            [_declared_safeguards()[0], _declared_safeguards()[0]],
        ),
    )
    frontmatter_validator = schema_registry("ControlFrontmatter")
    for label, value in invalid_values:
        document = skeleton.replace(
            "safeguards: [encrypt-in-transit]", f"safeguards: {value}"
        )
        diagnostics = list(frontmatter_validator.iter_errors(frontmatter(document)))
        assert diagnostics, label
        assert any(
            tuple(diagnostic.absolute_path)[:1] == ("safeguards",)
            for diagnostic in diagnostics
        ), diagnostics


@pytest.mark.trace("TC-246", "FR-025-AC-9")
@pytest.mark.parametrize(
    ("kind", "identifier"),
    [("connection", "CONN-1"), ("data_sink", "SINK-1")],
)
def test_control_protects_connections_and_sinks(tmp_path, kind, identifier):
    control = (
        (SKELETONS_DIR / "control.md")
        .read_text()
        .replace(
            "object: control\n",
            "object: control\n"
            f"relationships:\n  - target: {identifier}\n    type: protects\n",
            1,
        )
    )
    result = validate(
        tmp_path,
        {
            "control.md": control,
            "target.md": target_doc(kind, identifier),
        },
        extra_object_types=("connection", "data_sink"),
    )
    assert result.returncode == 0 and not errors(result), result.stderr


@pytest.mark.trace("TC-247", "FR-025-AC-9", "FR-025-AC-11")
def test_manifest_declares_safeguard_and_classification_frontmatter():
    import yaml

    manifest = yaml.safe_load((PACKAGE_ROOT / "manifest.yaml").read_text())
    object_types = {item["name"]: item for item in manifest["object_types"]}
    control = object_types["control"]
    classification = object_types["data_classification"]

    assert control["frontmatter_schema_ref"] == "schemas/ControlFrontmatter.json"
    assert control["allowed_links"]["protects"] == [
        "externally-exposed",
        "asset",
        "connection",
        "data_sink",
    ]
    assert control["body_extraction"]["yield_pattern"]["match"]["safeguards"] == {
        "from": "frontmatter_field",
        "path": ["safeguards"],
        "required": False,
    }
    assert classification["frontmatter_schema_ref"] == (
        "schemas/DataClassificationFrontmatter.json"
    )
    assert classification["body_extraction"]["yield_pattern"]["match"][
        "regulatedCategories"
    ] == {
        "from": "frontmatter_field",
        "path": ["regulated_categories"],
        "required": False,
    }
