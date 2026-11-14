"""Activation acceptance test against an isolated filament-core and database."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import pathlib
import subprocess
import time
import uuid

import httpx
import pytest
import yaml
from platform_test_kit.integration.postgres_stack import PostgresStack
from platform_test_kit.integration.rabbitmq_stack import RabbitMQStack
from platform_test_kit.integration.service_deployer import IsolatedServiceDeployer
from platform_test_kit.k8s.engine import ApplicationEngine
from platform_test_kit.k8s.primitives import RolloutWaiter

from tests.conftest import MANIFEST_PATH

TENANT_ID = "00000000-0000-0000-0000-000000000000"
ISSUER = "https://plat-1650-test.invalid"
KUBECTL_CONTEXT = "kind-platform"
CORE_IMAGE = "ghcr.io/agent-ix/filament-core-service:latest"
PGVECTOR_IMAGE = "pgvector/pgvector:pg15"


@pytest.fixture
def isolated_deployer():
    run_id = f"it-{uuid.uuid4().hex[:8]}"
    engine = ApplicationEngine()
    deployer = IsolatedServiceDeployer(
        engine=engine,
        waiter=RolloutWaiter(engine),
        run_id=run_id,
        namespace="apps",
    )
    try:
        yield deployer
    finally:
        deployer.halt_all()


@pytest.fixture
def unique_run_id(isolated_deployer):
    return isolated_deployer.run_id


def _b64url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _rsa_test_key(tmp_path: pathlib.Path) -> tuple[pathlib.Path, dict[str, str]]:
    private_key = tmp_path / "integration-rsa.pem"
    subprocess.run(
        [
            "openssl",
            "genpkey",
            "-algorithm",
            "RSA",
            "-pkeyopt",
            "rsa_keygen_bits:2048",
            "-out",
            str(private_key),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    modulus_result = subprocess.run(
        ["openssl", "rsa", "-in", str(private_key), "-noout", "-modulus"],
        check=True,
        capture_output=True,
        text=True,
    )
    modulus = bytes.fromhex(modulus_result.stdout.strip().split("=", maxsplit=1)[1])
    modulus = modulus.lstrip(b"\x00")
    return private_key, {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "kid": "plat-1650-integration-key",
        "n": _b64url(modulus),
        "e": "AQAB",
    }


def _system_token(private_key: pathlib.Path) -> str:
    now = int(time.time())
    header = {
        "alg": "RS256",
        "typ": "JWT",
        "kid": "plat-1650-integration-key",
    }
    claims = {
        "iss": ISSUER,
        "sub": "plat-1650-integration-system",
        "aud": "filament",
        "tenant_id": TENANT_ID,
        "roles": ["system"],
        "iat": now,
        "exp": now + 300,
    }
    signing_input = (
        f"{_b64url(json.dumps(header, separators=(',', ':')).encode())}."
        f"{_b64url(json.dumps(claims, separators=(',', ':')).encode())}"
    )
    signed = subprocess.run(
        ["openssl", "dgst", "-sha256", "-sign", str(private_key)],
        input=signing_input.encode("ascii"),
        check=True,
        capture_output=True,
    ).stdout
    return f"{signing_input}.{_b64url(signed)}"


def _deploy_jwks(isolated_deployer, run_id: str, jwk: dict[str, str]) -> None:
    config_map_name = f"activation-jwks-{run_id}"
    labels = {"app": "activation-jwks"}
    isolated_deployer.deploy_from_manifests(
        [
            {
                "apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {"name": "activation-jwks", "namespace": "apps"},
                "data": {"jwks.json": json.dumps({"keys": [jwk]})},
            },
            {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {"name": "activation-jwks", "namespace": "apps"},
                "spec": {
                    "replicas": 1,
                    "selector": {"matchLabels": labels},
                    "template": {
                        "metadata": {"labels": labels},
                        "spec": {
                            "containers": [
                                {
                                    "name": "jwks",
                                    "image": "nginx:alpine",
                                    "ports": [{"containerPort": 80}],
                                    "volumeMounts": [
                                        {
                                            "name": "jwks",
                                            "mountPath": "/usr/share/nginx/html",
                                            "readOnly": True,
                                        }
                                    ],
                                }
                            ],
                            "volumes": [
                                {
                                    "name": "jwks",
                                    "configMap": {
                                        "name": config_map_name,
                                        "items": [
                                            {"key": "jwks.json", "path": "jwks.json"}
                                        ],
                                    },
                                }
                            ],
                        },
                    },
                },
            },
            {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {"name": "activation-jwks", "namespace": "apps"},
                "spec": {
                    "selector": labels,
                    "ports": [{"port": 80, "targetPort": 80}],
                },
            },
        ]
    )
    isolated_deployer.wait_for_ready("Deployment", "activation-jwks", timeout=120)


def _psql_json(isolated_deployer, run_id: str, query: str) -> dict:
    pod = isolated_deployer.wait_for_ready("Pod", "postgres", timeout=60)
    result = subprocess.run(
        [
            "kubectl",
            "exec",
            "-n",
            isolated_deployer.namespace,
            "--context",
            KUBECTL_CONTEXT,
            pod["metadata"]["name"],
            "--",
            "psql",
            "-U",
            "postgres",
            "-d",
            "filament",
            "-tA",
            "-c",
            query,
        ],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PGPASSWORD": f"test-{run_id}"},
    )
    assert result.returncode == 0, result.stderr + result.stdout
    return json.loads(result.stdout.strip())


def _prepare_filament_roles(isolated_deployer, run_id: str) -> None:
    pod = isolated_deployer.wait_for_ready("Pod", "postgres", timeout=60)
    subprocess.run(
        [
            "kubectl",
            "exec",
            "-n",
            isolated_deployer.namespace,
            "--context",
            KUBECTL_CONTEXT,
            pod["metadata"]["name"],
            "--",
            "psql",
            "-U",
            "postgres",
            "-d",
            "postgres",
            "-c",
            "CREATE ROLE filament_app NOLOGIN; "
            "CREATE ROLE filament_platform_operator NOLOGIN BYPASSRLS;",
        ],
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ, "PGPASSWORD": f"test-{run_id}"},
    )


def _assert_core_jwks_route(isolated_deployer, jwks_url: str) -> None:
    pod = isolated_deployer.wait_for_ready(
        "Pod", "activation-filament-core", timeout=60
    )
    script = (
        "import urllib.request; "
        "import json; "
        "from filament_core_service.config import settings; "
        "print(json.dumps(settings.auth.model_dump())); "
        f"print(urllib.request.urlopen({jwks_url!r}, timeout=10).read().decode())"
    )
    result = subprocess.run(
        [
            "kubectl",
            "exec",
            "-n",
            isolated_deployer.namespace,
            "--context",
            KUBECTL_CONTEXT,
            pod["metadata"]["name"],
            "--",
            "python",
            "-c",
            script,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    auth_settings = json.loads(result.stdout.splitlines()[0])
    assert auth_settings["AUTH_JWKS_URL"] == jwks_url, auth_settings
    assert auth_settings["AUTH_ISSUER"] == ISSUER, auth_settings


@pytest.mark.integration
@pytest.mark.trace("TC-015", "FR-001-AC-2")
@pytest.mark.trace("TC-016", "FR-001-AC-3")
@pytest.mark.trace("TC-017", "FR-001-AC-4")
def test_activation_noop_hash_and_contribution_tables(
    isolated_deployer, unique_run_id, tmp_path
):
    """Deploy clean dependencies, activate twice, and inspect persisted rows."""
    db = PostgresStack(
        deployer=isolated_deployer,
        db_name="filament",
        user="postgres",
        password=f"test-{unique_run_id}",
    )
    db.DEFAULT_IMAGE = PGVECTOR_IMAGE
    db_info = db.deploy(timeout=180)
    _prepare_filament_roles(isolated_deployer, unique_run_id)
    rabbitmq = RabbitMQStack(deployer=isolated_deployer)
    rabbitmq_info = rabbitmq.deploy(timeout=180)

    private_key, jwk = _rsa_test_key(tmp_path)
    _deploy_jwks(isolated_deployer, unique_run_id, jwk)
    jwks_url = (
        f"http://activation-jwks-{unique_run_id}.{isolated_deployer.namespace}"
        ".svc.cluster.local/jwks.json"
    )
    core_url = isolated_deployer.deploy_service(
        name="activation-filament-core",
        image=CORE_IMAGE,
        port=8000,
        env={
            "ENV": "test",
            "DEBUG": "false",
            "POSTGRES_HOST": f"postgres-{unique_run_id}",
            "POSTGRES_PORT": str(db_info["port"]),
            "POSTGRES_USER": db_info["user"],
            "POSTGRES_PASSWORD": db_info["password"],
            "POSTGRES_DB": db_info["database"],
            "EVENT_BUS_URL": rabbitmq_info["amqp_url"],
            "AUTH": json.dumps(
                {
                    "AUTH_JWKS_URL": jwks_url,
                    "AUTH_ISSUER": ISSUER,
                    "AUTH_AUDIENCE": "filament",
                }
            ),
        },
        wait_for_http=180,
    )
    _assert_core_jwks_route(isolated_deployer, jwks_url)

    module_manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    activation_manifest = {
        key: module_manifest[key]
        for key in (
            "manifest_version",
            "name",
            "version",
            "description",
            "archetypes",
            "grammars",
            "artifact_types",
            "object_types",
            "lint_rules",
        )
        if key in module_manifest
    }
    headers = {
        "Authorization": f"Bearer {_system_token(private_key)}",
        "X-Tenant-ID": TENANT_ID,
        "X-Actor-Roles": "system",
    }
    with httpx.Client(timeout=60.0) as client:
        first = client.post(
            f"{core_url}/api/v1/modules/activate",
            json=activation_manifest,
            headers=headers,
        )
        assert first.status_code == 200, first.text
        first_body = first.json()
        assert first_body["skipped"] is False, first_body
        first_hash = first_body["module"]["manifest"]["_content_hash"]
        assert len(first_hash) == hashlib.sha256().digest_size * 2

        second = client.post(
            f"{core_url}/api/v1/modules/activate",
            json=activation_manifest,
            headers=headers,
        )
        assert second.status_code == 200, second.text
        second_body = second.json()
        assert second_body["skipped"] is True, second_body
        assert second_body["module"]["manifest"]["_content_hash"] == first_hash

    module_name = activation_manifest["name"].replace("'", "''")
    query = f"""
        SELECT json_build_object(
            'module_count', (
                SELECT count(*) FROM modules WHERE name = '{module_name}'
            ),
            'hash', (
                SELECT manifest->>'_content_hash' FROM modules
                WHERE name = '{module_name}'
            ),
            'archetypes', COALESCE((
                SELECT json_agg(kind ORDER BY kind) FROM archetypes
                WHERE module_id = (SELECT id FROM modules WHERE name = '{module_name}')
            ), '[]'::json),
            'object_types', COALESCE((
                SELECT json_agg(name ORDER BY name) FROM object_types
                WHERE module_id = (SELECT id FROM modules WHERE name = '{module_name}')
            ), '[]'::json),
            'artifact_types', COALESCE((
                SELECT json_agg(d.name ORDER BY d.name)
                FROM artifact_type_definitions d
                JOIN grammars g ON g.id = d.grammar_id
                WHERE g.module_id = (
                    SELECT id FROM modules WHERE name = '{module_name}'
                )
            ), '[]'::json)
        )::text
    """
    rows = _psql_json(isolated_deployer, unique_run_id, query)
    assert rows["module_count"] == 1, rows
    assert rows["hash"] == first_hash, rows
    assert set(rows["archetypes"]) == {
        item["kind"] for item in activation_manifest.get("archetypes", [])
    }, rows
    assert set(rows["object_types"]) == {
        item["name"] for item in activation_manifest.get("object_types", [])
    }, rows
    assert set(rows["artifact_types"]) == {
        item["name"] for item in activation_manifest.get("artifact_types", [])
    }, rows
