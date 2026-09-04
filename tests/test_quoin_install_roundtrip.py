"""The Quoin install roundtrip.

The row is `Manual` in the Test Matrix and stays `🚧`: it needs a Quoin built
from `agent-ix/quoin` main at or after `3e842ce`, and no release tag carries
the semantic module installer. What is automated here is the *precondition
check* — the module directory this test would hand to Quoin is complete and
self-consistent — so the manual step has a machine-checked starting point
rather than a claim.
"""

from __future__ import annotations

import json

import pytest

from tests.conftest import (
    MODEL_OF,
    OBJECT_TYPES,
    PACKAGE_ROOT,
    SCHEMAS_DIR,
    sha256_of,
)


@pytest.mark.trace("TC-110", "IT-002-SC-01")
def test_the_module_directory_quoin_would_install_is_complete():
    assert (PACKAGE_ROOT / "manifest.yaml").is_file()
    assert (PACKAGE_ROOT / "skeletons").is_dir()
    assert SCHEMAS_DIR.is_dir()
    for name in OBJECT_TYPES:
        path = SCHEMAS_DIR / f"{MODEL_OF[name]}.json"
        assert path.is_file(), name
        schema = json.loads(path.read_text())
        assert schema["$id"].endswith(f"/{MODEL_OF[name]}.json"), name
        assert sha256_of(path).startswith("sha256:")
