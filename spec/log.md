---
type: log
title: "Update Log"
description: "Chronological log of structural changes to this bundle."
---
# Update Log

## History

* **2026-06-15** — Adopted OKF-compatible bundle structure with directory indexes.
* **2026-09-04** — Added `usecase/` and `non-functional/` for the issue #13 semantic-module contract (US-001, FR-002..FR-006, NFR-001, IT-002).
* **2026-09-22** — the quire 0.47.1 wheel is published to `internal-pypi`: FR-005 declares `quire` as a dev dependency pinned to the `internal-pypi` source and drops the `make dev-quire` target and every `pypi.ix` reference; this leaves spec.md Out of Scope. semantic-core resolves from GitHub Packages (US-001), installed by `make semantic-install`. The `agent-ix/quire-rs#487` semantic-core-acceptance xfail machinery (`semantic_core_engine_xfail`, `engine_accepts_module_semantic_core`) is removed from `tests/conftest.py` and every test that carried it: quire 0.47.1 vendors semantic-core 0.3.0, so the probe now always reports acceptance and the strict xfail would never fire.
