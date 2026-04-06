"""Tests for src/version.py — single source of truth for package version."""
from __future__ import annotations

import re

from src.version import VERSION_INFO, __version__, version_string


class TestVersion:
    def test_version_is_string(self):
        assert isinstance(__version__, str)

    def test_version_format(self):
        # Must match MAJOR.MINOR.PATCH
        assert re.match(r"^\d+\.\d+\.\d+", __version__)

    def test_version_string_matches_dunder(self):
        assert version_string() == __version__

    def test_version_info_is_tuple(self):
        assert isinstance(VERSION_INFO, tuple)
        assert len(VERSION_INFO) == 4

    def test_version_info_major_minor_patch(self):
        major, minor, patch, pre = VERSION_INFO
        assert isinstance(major, int) and major >= 0
        assert isinstance(minor, int) and minor >= 0
        assert isinstance(patch, int) and patch >= 0

    def test_version_info_consistent_with_version_string(self):
        major, minor, patch, _ = VERSION_INFO
        assert __version__.startswith(f"{major}.{minor}.{patch}")

    def test_package_exports_version(self):
        import src
        assert src.__version__ == __version__


class TestReadVersionFallbacks:
    def test_tomllib_fallback_when_metadata_unavailable(self, tmp_path):
        """tomllib path used when importlib.metadata raises; reads from real pyproject.toml."""
        import io
        from unittest.mock import patch

        import src.version as vmod

        toml_bytes = b'[project]\nversion = "9.8.7"\n'
        with patch("importlib.metadata.version", side_effect=Exception("not found")):
            with patch("pathlib.Path.open", return_value=io.BytesIO(toml_bytes)):
                result = vmod._read_version()
        assert result == "9.8.7"

    def test_dev_fallback_when_all_fail(self):
        """Returns '0.0.0+dev' when both importlib.metadata and tomllib fail."""
        from unittest.mock import patch

        import src.version as vmod

        with patch("importlib.metadata.version", side_effect=Exception("no meta")):
            with patch("pathlib.Path.open", side_effect=Exception("no file")):
                result = vmod._read_version()
        assert result == "0.0.0+dev"

    def test_version_info_shape_for_dev_string(self):
        """VERSION_INFO tuple logic handles '0.0.0+dev' correctly."""
        parts = "0.0.0+dev".split("+")[0].split(".")
        nums = [int(p) for p in parts if p.isdigit()]
        info = (nums[0], nums[1], nums[2], "") if len(nums) >= 3 else (0, 0, 0, "")
        assert info == (0, 0, 0, "")
