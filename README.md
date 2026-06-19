# spec-objects-security

> Filament Module: tier-2 security and identity ObjectTypes (threats, controls, auth flows, secrets, policies)

`spec-objects-security` is an **Agent-IX Filament module**: a `manifest.yaml` plus per-kind authoring **skeletons** (and frontmatter schemas) that teach the spec tooling a vocabulary of object kinds. It is not a standalone app — it is loaded by [`quire-cli`](https://github.com/agent-ix/quire-cli) and [`quoin`](https://github.com/agent-ix/quoin) to author and validate Markdown spec artifacts.

## Installing quire-cli

This module is consumed by the `quire` binary from [`quire-cli`](https://github.com/agent-ix/quire-cli). Install the prebuilt binary from GitHub Packages — point the `@agent-ix` scope at GitHub Packages in `.npmrc`:

```
@agent-ix:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

```bash
npm install -g @agent-ix/quire-cli   # or: npx @agent-ix/quire-cli --help
quire --help
```

Prebuilt targets: linux-x64, linux-arm64, darwin-arm64, win32-x64. See the [quire-cli install docs](https://github.com/agent-ix/quire-cli#install) for tarball and from-source options.

## Object types provided

This module adds the following object kinds (frontmatter `type:` value in parentheses). All kinds are tier-2 embedded ObjectTypes — they require `id`, `title` and `type` in frontmatter plus the kind-specific contract below.

| Object | `type:` | Description |
|--------|---------|-------------|
| Auth flow | `auth_flow` | An authentication/login flow, with a `Flow` section carrying a mermaid diagram of the sequence (e.g. OIDC authorization code flow). |
| Permission | `permission` | A single grantable permission, naming the protected `resource` kind and the `verb` (action) it grants on it. |
| Scope | `scope` | An OAuth/authorization scope, with a `Grants` section listing the permissions the scope confers. |
| Role | `role` | A named role, with a `Permissions` section listing the permissions bound to it. |
| Secret | `secret` | A managed secret (e.g. client secret), with a `Rotation` section describing how and how often it rotates. |
| Encryption key | `encryption_key` | An encryption key, with frontmatter `algorithm` (cipher) and optional `rotation` cadence. |
| Session config | `session_config` | A session configuration, with a `Settings` section enumerating the effective session parameters (cookies, timeouts, limits). |
| Data classification | `data_classification` | A data sensitivity class, with a `Handling` section stating the handling requirements for that class. |
| Trust boundary | `trust_boundary` | A trust boundary between security zones, with a `Boundary` section carrying a mermaid diagram of the zones. |
| Audit event | `audit_event` | An emitted audit/log event, with an `Event Schema` section carrying a JSON code block of its payload schema. |
| CSRF token | `csrf_token` | A CSRF-protection token, with frontmatter `rotation_window` (how often a fresh token is issued). |
| CORS policy | `cors_policy` | A browser cross-origin policy, with an `Origins` section enumerating the allowed origins and their rules. |
| Password policy | `password_policy` | A password policy, with a `Rules` section enumerating the enforced password rules. |
| MFA method | `mfa_method` | A multi-factor authentication method, with frontmatter `kind` (method kind) and optional `factor` (auth factor class). |
| JWT claim | `jwt_claim` | A JWT/token claim, with a `Schema` section carrying a JSON code block of the claim's JSON Schema. |
| Threat | `threat` | A threat, with frontmatter `stride_category` (STRIDE class) and `vector` (the attack vector). |
| Control | `control` | A security control, with a `Mappings` section mapping it to the threats, risks and standards it addresses. |
| Risk | `risk` | A risk-register entry, with frontmatter `likelihood` and `impact` qualitative ratings driving its score. |
| Vulnerability | `vulnerability` | A vulnerability, with frontmatter `severity` and optional `cve_id` linking the public advisory. |
| Asset | `asset` | A protected asset, with a `Description` section describing the asset and why it matters. |
| Attack surface | `attack_surface` | An attack surface, with an `Entry Points` section enumerating the externally reachable entry points. |
| Policy | `policy` | A normative security policy, with a `Policy` section stating the policy text. |
| Audit finding | `audit_finding` | A security-audit finding, with a `Recommendation` section stating the remediation recommendation. |

## How this module is used

### With quoin (recommended)

[`quoin`](https://github.com/agent-ix/quoin) is the spec-domain authoring CLI. Install the module as a plugin, then author and validate:

```bash
quoin plugin install path:../spec-objects-security
quoin catalog list                      # list the kinds this module adds
quoin write . --types threat,control    # scaffold artifacts of these kinds
quoin review                            # validate authored files
```

### With quire-cli directly

Point `quire` at this module (the package directory holds `manifest.yaml` and `skeletons/`):

```bash
quire schema threat --module ./spec_objects_security                 # a kind's extraction contract
quire validate spec/**/*.md --module ./spec_objects_security         # structural validation
quire extract <DOC> --module ./spec_objects_security                 # extract structured data
```

See the [quire-cli usage docs](https://github.com/agent-ix/quire-cli#usage-instructions) for all commands.

## Development

This module is a flat-layout Python package (`spec_objects_security`, Python 3.13+) managed with [Poetry](https://python-poetry.org/) and built/published via GitHub Actions to Google Artifact Registry (PyPI-compatible).

```bash
make install          # install dependencies in the Poetry venv
make test             # run pytest
make lint             # ruff + black --check
make format           # auto-format (ruff --fix + black)
make build            # build wheel + sdist under dist/
make local-publish    # publish to the local pypi.ix registry
make update-lock      # update poetry.lock
make use-local p=<name> / make use-upstream p=<name>   # swap a dep source
```

**CI:** GitHub Actions runs on `push`, `pull_request`, and `v*.*.*` tags — it tests, lints, builds with `poetry build`, and on tags publishes via `twine upload -r internal-pypi`. Versioning is dynamic from the Git tag. Required CI config: `GCP_SERVICE_ACCOUNT_KEY` (secret) plus `GCP_REGION`, `GCP_PROJECT_NAME`, `GCP_PYPI` (variables).

## License

MIT — see [LICENSE](./LICENSE).
