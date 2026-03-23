"""
Detect the best Python environment for running the Bloomberg MCP server.

Checks (in order):
1. Active conda environment with blpapi already installed
2. Any conda environment with blpapi installed
3. System Python with blpapi installed
4. Active conda environment (blpapi not yet installed)
5. System Python (fallback)

Outputs JSON with:
  - python_path: full path to python executable
  - env_type: "conda" | "system"
  - env_name: conda environment name (or "system")
  - blpapi_installed: bool
  - fastmcp_installed: bool
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], timeout: int = 10) -> str | None:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def _check_package(python_path: str, package: str) -> bool:
    return _run([python_path, "-c", f"import {package}"]) is not None


def _get_conda_envs() -> list[dict]:
    """List all conda environments with their Python paths."""
    raw = _run(["conda", "env", "list", "--json"])
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []

    envs = []
    for env_path in data.get("envs", []):
        env_path = Path(env_path)
        # Windows: python.exe is directly in the env folder
        py = env_path / "python.exe"
        if not py.exists():
            py = env_path / "bin" / "python"
        if not py.exists():
            continue

        name = env_path.name
        if str(env_path).endswith(("anaconda3", "miniconda3", "miniforge3")):
            name = "base"

        envs.append({
            "name": name,
            "python_path": str(py),
            "env_path": str(env_path),
        })
    return envs


def detect() -> dict:
    # Check active conda env first
    active_conda = os.environ.get("CONDA_DEFAULT_ENV")
    active_prefix = os.environ.get("CONDA_PREFIX")

    candidates = []

    # 1. Active conda environment
    if active_prefix:
        py = Path(active_prefix) / "python.exe"
        if not py.exists():
            py = Path(active_prefix) / "bin" / "python"
        if py.exists():
            has_blpapi = _check_package(str(py), "blpapi")
            has_fastmcp = _check_package(str(py), "fastmcp")
            candidates.append({
                "python_path": str(py),
                "env_type": "conda",
                "env_name": active_conda or "unknown",
                "blpapi_installed": has_blpapi,
                "fastmcp_installed": has_fastmcp,
                "priority": 10 if has_blpapi else 3,
            })

    # 2. All conda environments
    for env in _get_conda_envs():
        # Skip if already added as active
        if active_prefix and str(Path(active_prefix)) == env["env_path"]:
            continue
        has_blpapi = _check_package(env["python_path"], "blpapi")
        has_fastmcp = _check_package(env["python_path"], "fastmcp")
        candidates.append({
            "python_path": env["python_path"],
            "env_type": "conda",
            "env_name": env["name"],
            "blpapi_installed": has_blpapi,
            "fastmcp_installed": has_fastmcp,
            "priority": 8 if has_blpapi else 1,
        })

    # 3. System Python
    sys_python = sys.executable
    if sys_python:
        has_blpapi = _check_package(sys_python, "blpapi")
        has_fastmcp = _check_package(sys_python, "fastmcp")
        candidates.append({
            "python_path": sys_python,
            "env_type": "system",
            "env_name": "system",
            "blpapi_installed": has_blpapi,
            "fastmcp_installed": has_fastmcp,
            "priority": 9 if has_blpapi else 2,
        })

    # Sort by priority (highest first)
    candidates.sort(key=lambda c: c["priority"], reverse=True)

    if not candidates:
        return {
            "python_path": "python",
            "env_type": "system",
            "env_name": "system",
            "blpapi_installed": False,
            "fastmcp_installed": False,
            "all_environments": [],
        }

    best = candidates[0]
    best.pop("priority", None)
    for c in candidates:
        c.pop("priority", None)
    best["all_environments"] = candidates

    return best


if __name__ == "__main__":
    result = detect()
    print(json.dumps(result, indent=2))
