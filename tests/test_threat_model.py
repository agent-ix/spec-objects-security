"""The `threat_model` object type, wider `threat.threatens` targets, and the
`risk` decision fields (FR-026, FR-004)."""

from __future__ import annotations

import json
import re
import shutil
import subprocess

import pytest
import yaml

from tests.conftest import (
    MANIFEST_PATH,
    PACKAGE_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    engine_tool,
    field,
)


def target_doc(kind: str, ident: str) -> str:
    front = f'id: {ident}\ntitle: "{ident}"\ntype: {kind}\nobject: {kind}\n'
    return f"---\n{front}---\n# {ident}\n"


def edges(*pairs: tuple[str, str]) -> str:
    if not pairs:
        return ""
    lines = "".join(f"  - target: {t}\n    type: {v}\n" for v, t in pairs)
    return f"relationships:\n{lines}"


def threat_model(
    *,
    method: str | None = "stride_per_element",
    reviewed_by: str | None = '"A. Person"',
    relationships: tuple[tuple[str, str], ...] = (("covers", "CONN-1"),),
    sections: tuple[str, ...] = ("Scope", "Assumptions", "Out of scope"),
) -> str:
    front = 'id: TM-1\ntitle: "TM"\ntype: threat_model\nobject: threat_model\n'
    if method is not None:
        front += f"method: {method}\n"
    if reviewed_by is not None:
        front += f"reviewed_by: {reviewed_by}\n"
    front += edges(*relationships)
    body = "".join(f"\n## {name}\n\nText for {name}.\n" for name in sections)
    return (
        f"---\n{front}---\n# [TM-1] TM\n{body}\n## Properties\n\n"
        "| Field | Type | Multiplicity | Constraints |\n|---|---|---|---|\n"
        "| threat_model_id | UUID | 1..1 | identity |\n"
    )


def validate(
    tmp_path, documents: dict[str, str], *, include_queue_type: bool = False
) -> subprocess.CompletedProcess:
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    for name, text in documents.items():
        (bundle / name).write_text(text)
    module = PACKAGE_ROOT
    if include_queue_type:
        module = tmp_path / "modules" / "spec_objects_security"
        shutil.copytree(PACKAGE_ROOT, module)
        manifest_path = module / "manifest.yaml"
        manifest = yaml.safe_load(manifest_path.read_text())
        manifest["semantic"]["exports"].append("queue")
        manifest["object_types"].append(
            {
                "name": "queue",
                "data_schema": {"schema": "schemas/Queue.json"},
                "body_extraction": {"yield_pattern": {"match": {}}},
            }
        )
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))
        (module / "schemas" / "Queue.json").write_text(
            json.dumps(
                {
                    "$id": "https://schemas.agent-ix.org/test/Queue.json",
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "type": "object",
                    "additionalProperties": True,
                }
            )
        )
    return subprocess.run(
        [engine_tool("quire"), "validate", "--okf", "--module", str(module)]
        + [str(bundle)],
        capture_output=True,
        text=True,
    )


def world() -> dict[str, str]:
    return {
        "conn.md": target_doc("connection", "CONN-1"),
        "role.md": target_doc("role", "ROLE-1"),
        "queue.md": target_doc("queue", "QUEUE-1"),
        "threat.md": (SKELETONS_DIR / "threat.md")
        .read_text()
        .replace("THREAT-001", "THREAT-1"),
    }


def errors(result: subprocess.CompletedProcess) -> list[str]:
    return [
        line
        for line in (result.stdout + result.stderr).splitlines()
        if line
        and not line.startswith(("warning:", "UnknownEdgeType:", "UnknownRole:"))
    ]


@pytest.mark.trace("FR-026-AC-1")
def test_threat_model_with_covers_and_considers_validates(tmp_path):
    docs = {
        **world(),
        "tm.md": threat_model(
            relationships=(("covers", "CONN-1"), ("considers", "THREAT-1"))
        ),
    }
    result = validate(tmp_path, docs)
    assert result.returncode == 0 and not errors(result), result.stderr


@pytest.mark.trace("FR-026-AC-1", "FR-026-AC-10")
def test_the_skeleton_validates(tmp_path):
    result = validate(
        tmp_path, {"tm.md": (SKELETONS_DIR / "threat_model.md").read_text()}
    )
    assert not errors(result), result.stderr


def validate_doc(quire_engine, object_type: str, text: str) -> dict:
    return quire_engine.validate_document(object_type, str(PACKAGE_ROOT), text)


def messages(result: dict) -> str:
    return "\n".join(e["message"] for e in result["errors"])


@pytest.mark.trace("FR-026-AC-2")
def test_method_guesswork_fails_naming_method(quire_engine):
    result = validate_doc(
        quire_engine, "threat_model", threat_model(method="guesswork")
    )
    assert not result["is_valid"]
    assert "method" in messages(result), result["errors"]


@pytest.mark.trace("FR-026-AC-3")
def test_missing_or_empty_reviewed_by_fails_naming_it(quire_engine):
    for value in (None, '""'):
        result = validate_doc(
            quire_engine, "threat_model", threat_model(reviewed_by=value)
        )
        assert not result["is_valid"], value
        assert "reviewed_by" in messages(result), result["errors"]


@pytest.mark.parametrize("missing", ["Scope", "Assumptions", "Out of scope"])
@pytest.mark.trace("FR-026-AC-6")
def test_a_missing_body_section_fails_naming_it(quire_engine, missing):
    sections = tuple(
        n for n in ("Scope", "Assumptions", "Out of scope") if n != missing
    )
    result = validate_doc(quire_engine, "threat_model", threat_model(sections=sections))
    assert not result["is_valid"]
    assert missing in messages(result), result["errors"]


@pytest.mark.trace("FR-026-AC-4")
def test_no_covers_edge_fails(tmp_path):
    result = validate(tmp_path, {**world(), "tm.md": threat_model(relationships=())})
    out = result.stdout + result.stderr
    assert "threat-model-covers-nothing" in out, out


@pytest.mark.trace("FR-026-AC-5")
def test_covers_to_a_role_is_a_wrong_kind_link(tmp_path):
    result = validate(
        tmp_path,
        {**world(), "tm.md": threat_model(relationships=(("covers", "ROLE-1"),))},
    )
    out = result.stdout + result.stderr
    assert "disallowed-edge-target" in out and "covers" in out, out


@pytest.mark.trace("FR-026-AC-5")
def test_considers_to_a_missing_id_is_dangling(tmp_path):
    result = validate(
        tmp_path,
        {
            **world(),
            "tm.md": threat_model(
                relationships=(("covers", "CONN-1"), ("considers", "THREAT-404"))
            ),
        },
    )
    out = result.stdout + result.stderr
    assert "THREAT-404" in out, out


def threat_threatening(target: str) -> str:
    threat = (SKELETONS_DIR / "threat.md").read_text().replace("THREAT-001", "THREAT-2")
    return threat.replace(
        "object: threat\n", "object: threat\n" + edges(("threatens", target)), 1
    )


@pytest.mark.trace("FR-027-AC-7")
def test_threatens_a_connection_validates(tmp_path):
    ok = validate(
        tmp_path,
        {
            "conn.md": target_doc("connection", "CONN-1"),
            "threat.md": threat_threatening("CONN-1"),
        },
    )
    assert "disallowed-edge-target" not in ok.stdout + ok.stderr, ok.stderr


@pytest.mark.trace("FR-027-AC-7")
def test_threatens_does_not_allow_a_queue_target(tmp_path):
    result = validate(
        tmp_path,
        {
            "queue.md": target_doc("queue", "QUEUE-1"),
            "threat.md": threat_threatening("QUEUE-1"),
        },
        include_queue_type=True,
    )
    out = result.stdout + result.stderr
    assert "disallowed-edge-target" in out and "threatens" in out, out


@pytest.mark.trace("FR-026-AC-4", "FR-026-AC-5", "FR-026-AC-9", "FR-027-AC-7")
def test_manifest_declares_the_verbs_and_the_link_targets():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert {"covers", "considers"} <= set(manifest["edge_types"])
    assert manifest["edge_types"]["considers"]["category"] == "governance"
    types = {o["name"]: o for o in manifest["object_types"]}
    assert types["threat_model"]["allowed_links"] == {
        "covers": ["part", "connection", "data_sink", "trust_boundary"],
        "considers": ["threat"],
    }
    assert types["threat"]["allowed_links"]["threatens"] == [
        "asset",
        "attack_surface",
        "connection",
        "data_sink",
        "trust_boundary",
    ]
    assert "threat_model" in manifest["semantic"]["exports"]


@pytest.mark.trace("FR-026-AC-2")
def test_method_enum_is_exactly_the_two_members():
    schema = json.loads((SCHEMAS_DIR / "ThreatModelMethod.json").read_text())
    assert schema["enum"] == ["stride_per_element", "stride_per_interaction"]


@pytest.mark.trace("FR-026-AC-7", "FR-026-AC-10")
def test_threat_model_schema_requires_method_and_reviewed_by_and_has_no_default(
    schema_registry,
):
    text = (SCHEMAS_DIR / "ThreatModel.json").read_text()
    assert '"default"' not in text
    validator = schema_registry("ThreatModel")
    record = {
        "fields": [field("a", "UUID", identity=True)],
        "method": "stride_per_interaction",
        "reviewed_by": "A. Person",
    }
    assert validator.is_valid(record)
    assert not validator.is_valid({})
    assert not validator.is_valid({**record, "method": "guesswork"})
    assert not validator.is_valid({**record, "reviewed_by": ""})
    assert not validator.is_valid(
        {k: v for k, v in record.items() if k != "reviewed_by"}
    )


@pytest.mark.trace("FR-027-AC-6")
@pytest.mark.parametrize(
    ("extra", "valid"),
    [
        ({"decision": "accepted", "decided_by": "A. Person"}, True),
        ({"decision": "not_accepted", "decided_by": "A. Person"}, True),
        ({"decision": "undecided"}, True),
        ({"decision": "accepted"}, False),
        ({"decision": "undecided", "decided_by": "A. Person"}, False),
        ({"decision": "maybe"}, False),
        ({}, False),
    ],
)
def test_risk_decision_rules(schema_registry, extra, valid):
    record = {
        "fields": [
            field("a", "UUID", identity=True),
            field("likelihood"),
            field("impact"),
        ],
        **extra,
    }
    assert schema_registry("Risk").is_valid(record) is valid


def risk_doc(**front) -> str:
    text = (SKELETONS_DIR / "risk.md").read_text()
    text = re.sub(r"^decision: .*\n", "", text, flags=re.M)
    extra = "".join(f"{k}: {v}\n" for k, v in front.items())
    return text.replace("\n---\n<!--", f"\n{extra}---\n<!--", 1)


@pytest.mark.trace("FR-027-AC-6")
@pytest.mark.parametrize(
    ("front", "valid"),
    [
        ({"decision": "accepted", "decided_by": '"A. Person"'}, True),
        ({"decision": "accepted"}, False),
        ({"decision": "undecided", "decided_by": '"A. Person"'}, False),
        ({"decision": "maybe"}, False),
        ({}, False),
    ],
)
def test_risk_document_decision_rules(quire_engine, front, valid):
    result = validate_doc(quire_engine, "risk", risk_doc(**front))
    assert result["is_valid"] is valid, result["errors"]


@pytest.mark.trace("FR-027-AC-6")
def test_risk_skeleton_states_a_decision():
    text = (SKELETONS_DIR / "risk.md").read_text()
    assert re.search(r"^decision: undecided$", text, re.M)
