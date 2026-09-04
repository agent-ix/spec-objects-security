"""Shared fixtures for the module's test suite.

Two policies are enforced here and nowhere else:

* **The engine is a hard dependency of the semantic rows.** ``quire`` is not
  declared in ``pyproject.toml`` — no index a repository may commit against
  carries 0.46.0 (``internal-pypi`` serves 0.33.0 at most and no ``quire-rs``
  tag carries the semantic layer), so the wheel is provisioned by
  ``make dev-quire`` and ``agent-ix/quire-rs#392`` is the blocking issue. When
  it is absent the semantic tests **fail**; they never skip, because a skipped
  row is not coverage (FR-005). This is the disposition of
  ``agent-ix/spec-objects-security#10``.
* **The emitted schemas are read from the committed tree**, and every ``$ref``
  to semantic-core resolves against the package the toolchain installs, so a
  record test validates against the real bytes.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
from typing import Any

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGE_ROOT = REPO_ROOT / "spec_objects_security"
MANIFEST_PATH = PACKAGE_ROOT / "manifest.yaml"
SCHEMAS_DIR = PACKAGE_ROOT / "schemas"
SKELETONS_DIR = PACKAGE_ROOT / "skeletons"
NEGATIVE_DIR = REPO_ROOT / "tests" / "fixtures" / "negative"
BASELINE_DIR = REPO_ROOT / "tests" / "fixtures" / "baseline-0.1.0"
SEMANTIC_CORE_DIR = (
    REPO_ROOT
    / "node_modules"
    / "@agent-ix"
    / "semantic-core"
    / "generated"
    / "json-schema"
)

SEMANTIC_CORE_BASE = "https://schemas.agent-ix.org/semantic-core/0.1.0/"

QUIRE_MISSING = (
    "the Quire wheel exposing `extract_semantic` is not installed in this "
    "environment. Run `make dev-quire` (agent-ix/quire-rs#392 tracks publishing "
    "0.46.0 to an index this repository may depend on). The semantic tests fail "
    "rather than skip, because a skipped row is not coverage."
)

OBJECT_TYPES = (
    "auth_flow",
    "permission",
    "scope",
    "role",
    "secret",
    "encryption_key",
    "session_config",
    "data_classification",
    "trust_boundary",
    "audit_event",
    "csrf_token",
    "cors_policy",
    "password_policy",
    "mfa_method",
    "jwt_claim",
    "threat",
    "control",
    "risk",
    "vulnerability",
    "asset",
    "attack_surface",
    "policy",
    "audit_finding",
)

MODEL_OF = {
    "auth_flow": "AuthFlow",
    "permission": "Permission",
    "scope": "Scope",
    "role": "Role",
    "secret": "Secret",
    "encryption_key": "EncryptionKey",
    "session_config": "SessionConfig",
    "data_classification": "DataClassification",
    "trust_boundary": "TrustBoundary",
    "audit_event": "AuditEvent",
    "csrf_token": "CsrfToken",
    "cors_policy": "CorsPolicy",
    "password_policy": "PasswordPolicy",
    "mfa_method": "MfaMethod",
    "jwt_claim": "JwtClaim",
    "threat": "Threat",
    "control": "Control",
    "risk": "Risk",
    "vulnerability": "Vulnerability",
    "asset": "Asset",
    "attack_surface": "AttackSurface",
    "policy": "Policy",
    "audit_finding": "AuditFinding",
}

MARKER_MODELS = (
    "IdentityField",
    "DefaultedField",
    "OccurrenceField",
    "OccurrenceTypeRef",
    "StrideCategoryField",
    "SeverityField",
    "LikelihoodField",
    "ImpactField",
    "StatusField",
    "LevelField",
    "TrustLevelField",
    "EffectivenessField",
)

RECORD_MODELS = ("ControlMapping", "FlowStep")

VOCABULARIES = {
    "Severity": (
        ["none", "low", "medium", "high", "critical", "unknown"],
        "unknown",
    ),
    "Likelihood": (
        ["rare", "unlikely", "possible", "likely", "almost_certain", "unknown"],
        "unknown",
    ),
    "Impact": (
        ["negligible", "minor", "moderate", "major", "severe", "unknown"],
        "unknown",
    ),
    "StrideCategory": (
        [
            "spoofing",
            "tampering",
            "repudiation",
            "information_disclosure",
            "denial_of_service",
            "elevation_of_privilege",
            "unknown",
        ],
        "unknown",
    ),
    "ControlEffectiveness": (
        ["not_assessed", "ineffective", "partially_effective", "effective"],
        "not_assessed",
    ),
    "FindingStatus": (
        [
            "open",
            "in_remediation",
            "remediated",
            "risk_accepted",
            "false_positive",
            "unknown",
        ],
        "unknown",
    ),
    "ConfidentialityLevel": (
        ["public", "internal", "confidential", "restricted", "unknown"],
        "unknown",
    ),
    "TrustLevel": (["untrusted", "semi_trusted", "trusted", "unknown"], "untrusted"),
    "SecretLifecycle": (
        ["proposed", "active", "rotating", "revoked", "compromised", "unknown"],
        "unknown",
    ),
    "MfaFactorKind": (["knowledge", "possession", "inherence", "unknown"], "unknown"),
}

# The types whose schema admits no `FieldDecl` carrying a `default` (FR-006).
DEFAULT_REFUSING = (
    "secret",
    "encryption_key",
    "jwt_claim",
    "csrf_token",
    "mfa_method",
    "auth_flow",
    "audit_event",
)

FIELD_BEARING = (
    "asset",
    "role",
    "permission",
    "scope",
    "mfa_method",
    "threat",
    "vulnerability",
    "risk",
    "audit_finding",
    "data_classification",
    "attack_surface",
    "trust_boundary",
    "secret",
    "encryption_key",
    "jwt_claim",
    "csrf_token",
    "control",
    "audit_event",
)

CLAUSE_BEARING = (
    "trust_boundary",
    "policy",
    "control",
    "password_policy",
    "cors_policy",
    "session_config",
)

OPERATION_BEARING = ("auth_flow",)

ALTERNATES = ("asset", "secret", "threat")

KERNEL_SCALARS = frozenset(
    {
        "UUID",
        "Boolean",
        "Integer",
        "Decimal",
        "String",
        "Timestamp",
        "Duration",
        "Bytes",
        "JsonObject",
    }
)

IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def load_manifest() -> dict[str, Any]:
    return yaml.safe_load(MANIFEST_PATH.read_text())


def manifest_version() -> str:
    return load_manifest()["version"]


def module_base() -> str:
    """The `$id` base, read from the manifest version — never hard-coded
    (FR-002-CON-5)."""
    return (
        "https://schemas.agent-ix.org/agent-ix/spec-objects-security/"
        f"{manifest_version()}/"
    )


def object_types() -> list[dict[str, Any]]:
    return load_manifest()["object_types"]


def object_type(name: str) -> dict[str, Any]:
    return next(ot for ot in object_types() if ot["name"] == name)


def locators(ot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    body = ot.get("body_extraction") or {}
    return ((body.get("yield_pattern") or {}).get("match")) or {}


def frontmatter(markdown: str) -> dict[str, Any]:
    match = re.match(r"---\n(.*?)\n---\n", markdown, re.DOTALL)
    assert match, "document has no frontmatter"
    return yaml.safe_load(match.group(1))


def sha256_of(path: pathlib.Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def require_quire():
    """Import quire, or fail the test naming the provisioning path."""
    try:
        import quire
    except ImportError as error:
        pytest.fail(f"{QUIRE_MISSING} (import error: {error})")
    if not hasattr(quire, "extract_semantic"):
        pytest.fail(
            f"`extract_semantic` is missing from the installed quire: {QUIRE_MISSING}"
        )
    return quire


@pytest.fixture(scope="session")
def quire_engine():
    return require_quire()


@pytest.fixture(scope="session")
def manifest() -> dict[str, Any]:
    return load_manifest()


@pytest.fixture(scope="session")
def semantic_block(manifest: dict[str, Any]) -> dict[str, Any]:
    return manifest["semantic"]


@pytest.fixture(scope="session")
def semantic_module(semantic_block: dict[str, Any]) -> dict[str, Any]:
    """The `module` block `extract_semantic` takes, derived from the manifest."""
    return {
        "contractVersion": semantic_block["contract_version"],
        "semanticCore": semantic_block["semantic_core"],
        "package": semantic_block["package"],
        "exports": semantic_block["exports"],
        "imports": semantic_block["imports"],
        "compatibilityPosture": semantic_block["compatibility_posture"],
        "legacyForms": semantic_block["legacy_forms"],
    }


@pytest.fixture(scope="session")
def skeletons() -> list[pathlib.Path]:
    return sorted(SKELETONS_DIR.glob("*.md"))


@pytest.fixture(scope="session")
def bundle_index(semantic_block: dict[str, Any]) -> dict[str, Any]:
    """A bundle index built from the skeleton frontmatter (FR-005-AC-3)."""
    objects: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in sorted(SKELETONS_DIR.glob("*.md")):
        front = frontmatter(path.read_text())
        if front["id"] in seen:
            continue
        seen.add(front["id"])
        objects.append({"id": front["id"], "names": [front["id"], front["title"]]})
    return {
        "package": semantic_block["package"],
        "objects": objects,
        "enumerations": [],
        "imports": {},
    }


@pytest.fixture(scope="session")
def schema_registry():
    """A 2020-12 validator factory over the shipped schemas plus semantic-core.

    Every `$ref` resolves locally: module models from the committed `schemas/`
    directory, grammar models from the semantic-core package the pinned
    toolchain installs.
    """
    from referencing import Registry, Resource

    if not SEMANTIC_CORE_DIR.is_dir():
        pytest.fail(
            "@agent-ix/semantic-core is not installed, so `$ref`s to the grammar "
            "cannot resolve. Run `npm ci` (FR-002-CON-4: `@agent-ix` resolves "
            "from npm.ix through the user-level npm config)."
        )
    resources = []
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        if path.name == "toolchain.json":
            continue
        schema = json.loads(path.read_text())
        resources.append((schema["$id"], Resource.from_contents(schema)))
    for path in sorted(SEMANTIC_CORE_DIR.glob("*.json")):
        schema = json.loads(path.read_text())
        uri = schema.get("$id") or f"{SEMANTIC_CORE_BASE}{path.name}"
        resources.append((uri, Resource.from_contents(schema)))
    registry = Registry().with_resources(resources)

    def validator_for(model: str):
        from jsonschema import Draft202012Validator

        schema = json.loads((SCHEMAS_DIR / f"{model}.json").read_text())
        return Draft202012Validator(schema, registry=registry)

    return validator_for


def field(
    name: str,
    target: str = "String",
    lower: int = 1,
    upper: int = 1,
    identity: bool = False,
    default: Any = None,
) -> dict[str, Any]:
    """Build one `FieldDecl` by hand.

    Hand-built records are how every criterion over a key the extractor does
    not populate is verified (FR-004): they are schema evidence, never
    extraction evidence, and the tests that use them say so.
    """
    decl: dict[str, Any] = {
        "name": name,
        "type": {"target": target, "multiplicity": {"lower": lower, "upper": upper}},
    }
    if identity:
        decl["identity"] = True
    if default is not None:
        decl["default"] = {"kind": "literal", "value": default}
    return decl


CLAUSE = {"language": "ocl", "clauseId": "SomeClause"}
OPERATION = {"name": "some_operation", "params": []}
