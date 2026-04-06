"""Single source of truth for the package version.

Resolution order:
  1. importlib.metadata  — works when package is installed (pip install -e .)
  2. pyproject.toml      — fallback for uninstalled dev environments (Python 3.11+)
  3. "0.0.0+dev"         — last resort so imports never fail
"""
from __future__ import annotations


def _read_version() -> str:
    # 1. Installed package metadata
    try:
        from importlib.metadata import version as _pkg_version

        return _pkg_version("claude-code-max")
    except Exception:
        pass

    # 2. Direct pyproject.toml parse (tomllib is stdlib since Python 3.11)
    try:
        import tomllib
        from pathlib import Path

        _toml = Path(__file__).parent.parent / "pyproject.toml"
        with _toml.open("rb") as fh:
            return tomllib.load(fh)["project"]["version"]
    except Exception:
        pass

    return "0.0.0+dev"


__version__: str = _read_version()

# 4-tuple (major, minor, patch, pre) for runtime comparisons
_parts = __version__.split("+")[0].split(".")
_nums = [int(p) for p in _parts if p.isdigit()]
VERSION_INFO: tuple[int, int, int, str] = (_nums[0], _nums[1], _nums[2], "") if len(_nums) >= 3 else (0, 0, 0, "")


def version_string() -> str:
    """Return the canonical version string e.g. '1.0.7'."""
    return __version__
