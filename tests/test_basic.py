from spec_objects_security import MANIFEST_PATH, PACK_ROOT


def test_manifest_path_points_to_packaged_manifest():
    """TC-001: FR-001-AC-1."""
    assert MANIFEST_PATH == PACK_ROOT / "manifest.yaml"
    assert MANIFEST_PATH.is_file()
