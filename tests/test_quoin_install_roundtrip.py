"""The Quoin install roundtrip.

The IT-002 success criteria need a Quoin that provides the module installer,
so this file does not cover them: a test that only checks files exist cannot
claim "the pre-install listing is captured". It checks only that the module
directory the roundtrip would hand to Quoin is complete and self-consistent,
which gives the manual install step a machine-checked starting point.
"""

from __future__ import annotations

import json

from tests.conftest import (
    MODEL_OF,
    OBJECT_TYPES,
    PACKAGE_ROOT,
    SCHEMAS_DIR,
)


def test_the_module_directory_quoin_would_install_is_complete():
    assert (PACKAGE_ROOT / "manifest.yaml").is_file()
    assert (PACKAGE_ROOT / "skeletons").is_dir()
    assert SCHEMAS_DIR.is_dir()
    for name in OBJECT_TYPES:
        path = SCHEMAS_DIR / f"{MODEL_OF[name]}.json"
        assert path.is_file(), name
        schema = json.loads(path.read_text())
        assert schema["$id"].endswith(f"/{MODEL_OF[name]}.json"), name
