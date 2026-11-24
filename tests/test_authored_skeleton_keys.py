"""The four optional string keys the skeletons author in frontmatter.

`kind`, `vector`, `rotation` and `rotation_window` reach the record because the
engine projects every authored frontmatter key into the record the closed
schema validates. Each is declared, typed and optional.
"""

from __future__ import annotations

import pytest

from tests.conftest import PACKAGE_ROOT, SKELETONS_DIR, field

MODELS = {
    "MfaMethod": "kind",
    "Threat": "vector",
    "EncryptionKey": "rotation",
    "CsrfToken": "rotation_window",
}


def _record(model: str, **extra) -> dict:
    fields = [field("subject_id", "UUID", identity=True)]
    if model == "Threat":
        fields.append(field("stride_category"))
    return {"fields": fields, **extra}


def _errors(validator_for, model: str, record: dict) -> list:
    return list(validator_for(model).iter_errors(record))


@pytest.mark.trace("FR-004-AC-15")
@pytest.mark.parametrize(("model", "key"), MODELS.items())
def test_the_key_is_optional_and_absence_validates(schema_registry, model, key):
    assert not _errors(schema_registry, model, _record(model))


@pytest.mark.trace("FR-004-AC-15")
@pytest.mark.parametrize(
    ("model", "key", "value"),
    [
        ("MfaMethod", "kind", "totp"),
        ("Threat", "vector", "exfiltrated refresh token replayed"),
        ("EncryptionKey", "rotation", "P90D"),
        ("EncryptionKey", "rotation", "P1Y2M"),
        ("CsrfToken", "rotation_window", "PT30M"),
        ("CsrfToken", "rotation_window", "P1DT12H"),
        ("CsrfToken", "rotation_window", "PT15M"),
        ("EncryptionKey", "rotation", "P1Y2M3DT4H5M6S"),
        ("EncryptionKey", "rotation", "P2W"),
        ("EncryptionKey", "rotation", "P1Y2M3D"),
    ],
)
def test_accepted_values(schema_registry, model, key, value):
    assert not _errors(schema_registry, model, _record(model, **{key: value}))


@pytest.mark.trace("FR-004-AC-15")
@pytest.mark.parametrize(
    ("model", "key", "value"),
    [
        ("MfaMethod", "kind", ""),
        ("MfaMethod", "kind", 7),
        ("Threat", "vector", ""),
        ("EncryptionKey", "rotation", "ninety days"),
        ("EncryptionKey", "rotation", "P"),
        ("EncryptionKey", "rotation", "90D"),
        ("CsrfToken", "rotation_window", "30 minutes"),
        ("CsrfToken", "rotation_window", "PT"),
        ("CsrfToken", "rotation_window", 30),
        ("EncryptionKey", "rotation", "P1D1Y"),
        ("EncryptionKey", "rotation", "P1Y2W"),
        ("EncryptionKey", "rotation", "P2W3D"),
        ("EncryptionKey", "rotation", "P1Y1M1W1D"),
        ("EncryptionKey", "rotation", "P1W1W"),
        ("EncryptionKey", "rotation", "P0.5D"),
        ("CsrfToken", "rotation_window", "PT0.5S"),
        ("EncryptionKey", "rotation", "P1D2D"),
        ("EncryptionKey", "rotation", "P1Y1Y"),
        ("EncryptionKey", "rotation", "P1DT"),
        ("CsrfToken", "rotation_window", "PT5M1H"),
        ("CsrfToken", "rotation_window", "PT1H1H"),
        ("CsrfToken", "rotation_window", "P1DT5S3M"),
    ],
)
def test_rejected_values(schema_registry, model, key, value):
    assert _errors(schema_registry, model, _record(model, **{key: value}))


@pytest.mark.trace("FR-004-AC-15")
@pytest.mark.parametrize(
    ("kind", "old", "new"),
    [
        ("csrf_token", "rotation_window: PT30M", "rotation_window: soon"),
        ("encryption_key", "rotation: P90D", "rotation: quarterly"),
    ],
)
def test_a_malformed_duration_fails_an_authored_document(quire_engine, kind, old, new):
    text = (SKELETONS_DIR / f"{kind}.md").read_text()
    assert old in text
    result = quire_engine.validate_document(
        kind, str(PACKAGE_ROOT), text.replace(old, new)
    )
    assert not result["is_valid"]
    assert any("semantic.record-invalid" in e["message"] for e in result["errors"])
