"""Backward-compatible shim — real script lives in programs/scripts/. """
from __future__ import annotations
import os, runpy, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROGRAMS = ROOT / "programs"
SCRIPTS = PROGRAMS / "scripts"
os.environ.setdefault("EA_EVAL_REFERENTIEL", str(ROOT))
os.environ.setdefault("EA_EVAL_PROGRAMS", str(PROGRAMS))
os.environ.setdefault("EA_EVAL_OUTPUT", str(PROGRAMS / "output"))
sys.path.insert(0, str(SCRIPTS))
TARGET = SCRIPTS / "make_demo_quiz_html.py"
if not TARGET.is_file():
    raise SystemExit(f"Missing migrated script: {TARGET}")
runpy.run_path(str(TARGET), run_name="__main__")