"""Resolve package paths for the programs/ layout (v11).

Environment overrides (highest priority):
  EA_EVAL_REFERENTIEL  absolute path to the curriculum/data root
  EA_EVAL_OUTPUT       absolute path to the programs output root
  EA_EVAL_PROGRAMS     absolute path to the programs/ folder

Default layout:
  <package>/                          <- referentiel (data root)
    French_Math_..._v11.md
    Math_Diagnostic_Targets_v11.csv
    ...
    programs/
      config/programs_v11.yaml
      scripts/   <- this file lives here
      output/
      referentiel/README.md
"""
from __future__ import annotations

import os
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_PROGRAMS = _SCRIPTS.parent


def programs_root() -> Path:
    env = os.environ.get("EA_EVAL_PROGRAMS")
    return Path(env).resolve() if env else _PROGRAMS


def data_root() -> Path:
    """Curriculum package root (CSV, MD, eligibility, build inputs)."""
    env = os.environ.get("EA_EVAL_REFERENTIEL")
    if env:
        return Path(env).resolve()
    cfg = _load_yaml_paths()
    rel = (cfg or {}).get("paths", {}).get("referentiel", "..")
    return (programs_root() / rel).resolve()


def scripts_root() -> Path:
    return _SCRIPTS


def output_root() -> Path:
    env = os.environ.get("EA_EVAL_OUTPUT")
    if env:
        return Path(env).resolve()
    cfg = _load_yaml_paths()
    rel = (cfg or {}).get("paths", {}).get("output", "output")
    return (programs_root() / rel).resolve()


def config_path() -> Path:
    return programs_root() / "config" / "programs_v11.yaml"


def _load_config_data():
    """Load programs_v11.yaml, or programs_v11.json if PyYAML is unavailable (e.g. python -I)."""
    import json
    ypath = config_path()
    jpath = ypath.with_suffix(".json")
    if ypath.is_file():
        try:
            import yaml  # type: ignore
            with ypath.open(encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            pass
    if jpath.is_file():
        with jpath.open(encoding="utf-8") as f:
            return json.load(f) or {}
    return None


def _load_yaml_paths():
    return _load_config_data()


def ensure_output_dirs() -> dict[str, Path]:
    root = output_root()
    mapping = {
        "root": root,
        "validation": root / "validation",
        "prompts": root / "prompts",
        "dashboards": root / "dashboards",
        "demos": root / "demos",
        "logs": root / "logs",
        "builds": root / "builds",
    }
    for p in mapping.values():
        p.mkdir(parents=True, exist_ok=True)
    return mapping


def bootstrap_sys_path() -> Path:
    """Put scripts/ on sys.path so chk_*, v7lib, validate_reference import each other."""
    import sys

    s = str(scripts_root())
    if s not in sys.path:
        sys.path.insert(0, s)
    return scripts_root()
