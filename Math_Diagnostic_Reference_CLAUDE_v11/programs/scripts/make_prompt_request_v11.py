#!/usr/bin/env python3
"""Build a ready-to-paste diagnostic prompt request from programs_v11.yaml.

Writes:
  - output/prompts/<stamp>_<scenario>_REQUEST.md   (variables + instructions)
  - output/prompts/<stamp>_<scenario>_FULL.md      (optional: prompt file + request)
  - output/prompts/<stamp>_<scenario>_vars.json     (resolved values)

Usage (from anywhere; paths come from ea_paths / YAML):
  py -3 -I make_prompt_request_v11.py
  py -3 -I make_prompt_request_v11.py --scenario quick_brevet_entry
  py -3 -I make_prompt_request_v11.py --set LEVEL=MP2I --set DURATION=40
  py -3 -I make_prompt_request_v11.py --full --scenario full_brevet_entry

This does NOT call an LLM and does NOT generate a quiz.
"""
from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import ea_paths

ea_paths.bootstrap_sys_path()
HERE = ea_paths.data_root()
OUTPUT = ea_paths.ensure_output_dirs()
CONFIG = ea_paths.config_path()


def load_config() -> dict:
    data = ea_paths._load_config_data()
    if not data:
        raise SystemExit(
            f"Config not found. Expected {CONFIG} or {CONFIG.with_suffix('.json')}. "
            "Install PyYAML (py -3 -m pip install PyYAML) or keep the JSON twin in sync."
        )
    return data


def derive_learner_profile(level: str) -> str:
    mapping = {
        "BREVET": "incoming 2nde / DNB entry",
        "BAC_1RE_SPE": "1re spé maths",
        "BAC_1RE_COMMUN": "1re maths enseignement scientifique",
        "BAC_TLE_SPE": "Tle spé maths",
        "BAC_TLE_EXPERTES": "Tle maths expertes (with spé)",
        "BAC_TLE_COMPLEMENTAIRES": "Tle maths complémentaires",
        "MP2I": "Tle → MP2I entry",
        "MPI": "MP2I → MPI",
    }
    return mapping.get(level, level)


def resolve_vars(cfg: dict, scenario: str | None, overrides: dict) -> dict:
    values = dict(cfg.get("prompt_defaults") or {})
    if scenario:
        scenarios = cfg.get("prompt_scenarios") or {}
        if scenario not in scenarios:
            known = ", ".join(sorted(scenarios)) or "(none)"
            raise SystemExit(f"Unknown scenario '{scenario}'. Known: {known}")
        values.update(scenarios[scenario] or {})
    values.update(overrides)
    if not str(values.get("LEARNER_PROFILE") or "").strip():
        values["LEARNER_PROFILE"] = derive_learner_profile(str(values.get("LEVEL") or ""))
    # SHORT convenience: align NB_* when TEST_LENGTH is SHORT and still at FULL defaults
    if str(values.get("TEST_LENGTH", "")).upper() == "SHORT":
        if int(values.get("NB_MCQ") or 0) >= 12 and int(values.get("DURATION") or 0) >= 55:
            values["NB_MCQ"] = 5
            values["NB_OPEN"] = 2
            values["DURATION"] = 20
    return values


def format_request_block(values: dict, cfg: dict, scenario: str | None) -> str:
    meta = cfg.get("meta") or {}
    warning = (cfg.get("status_warning") or "").strip()
    lines = [
        "# Diagnostic prompt request (generated)",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Config: `{CONFIG.name}` v{meta.get('version', '?')}",
        f"- Prompt on disk: `{meta.get('prompt_on_disk')}`",
        f"- Prompt v10 status: {meta.get('prompt_v10_status', 'unknown')}",
        f"- Scenario: {scenario or '(defaults)'}",
        "",
        "> **Status:** " + warning.replace("\n", " "),
        "",
        "## How to use",
        "",
        "1. Open a new chat with your LLM tool.",
        "2. Paste the **entire** prompt file named above (from the referentiel).",
        "3. Attach the reference files listed under Attachments.",
        "4. Paste the variable block below.",
        "5. Read the one-sentence restatement (RaR). Correct it if needed, then continue.",
        "",
        "## Attachments (referentiel)",
        "",
    ]
    for name in (cfg.get("attachments") or {}).get("always") or []:
        path = HERE / name
        mark = "found" if path.is_file() else "MISSING"
        lines.append(f"- `{name}` — {mark}")
    prompt_name = (cfg.get("attachments") or {}).get("prompt_file")
    if prompt_name:
        p = HERE / prompt_name
        lines.append(f"- Prompt file `{prompt_name}` — {'found' if p.is_file() else 'MISSING'}")
    lines.extend(["", "## Variable block", "", "```text"])
    order = [
        "LEVEL", "SUBJECT", "PURPOSE", "ASSESSMENT_MODE", "LEARNER_PROFILE",
        "EXAM_SESSION", "DURATION", "NB_MCQ", "NB_OPEN", "TEST_LENGTH",
        "CALCULATOR", "DELIVERY", "ADAPTATIONS", "OUTPUT_LANGUAGE",
        "REFERENCE", "TARGET_CODES", "DIAGNOSTIC_OPTIONS", "OUTPUT_FORMAT",
    ]
    seen = set()
    for key in order:
        if key in values:
            lines.append(f"{{{key}}} = {values[key]}")
            seen.add(key)
    for key in sorted(values):
        if key not in seen:
            lines.append(f"{{{key}}} = {values[key]}")
    lines.append("```")
    if str(values.get("TEST_LENGTH", "")).upper() == "SHORT":
        lines.extend([
            "",
            "> **Note:** `TEST_LENGTH=SHORT` comes from the handoff / expected PROMPT v10.",
            "> On PROMPT v9, the equivalent is NB_MCQ / NB_OPEN / DURATION as written above.",
        ])
    lines.extend([
        "",
        "## Operator reminders",
        "",
        "- Do not use FAIL rows (`1C-FN-05`…`10`).",
        "- HOLD rows yield draft items only.",
        "- `validate_reference_v11.py` checks the **reference package**, not this quiz.",
        "- Quiz status stays `UNVALIDATED — HOLD` until every item is from a PASS row and a teacher approves it.",
        "",
    ])
    return "\n".join(lines)


def build_full_document(request_md: str, cfg: dict) -> str:
    prompt_name = (cfg.get("attachments") or {}).get("prompt_file")
    if not prompt_name:
        return request_md
    path = HERE / prompt_name
    if not path.is_file():
        return request_md + f"\n\n<!-- PROMPT FILE MISSING: {path} -->\n"
    body = path.read_text(encoding="utf-8")
    return (
        "<!-- FULL PASTE: prompt file then request block -->\n\n"
        + body
        + "\n\n---\n\n"
        + request_md
    )


def parse_set_args(items: list[str]) -> dict:
    out = {}
    for raw in items:
        if "=" not in raw:
            raise SystemExit(f"--set expects KEY=VALUE, got: {raw}")
        key, value = raw.split("=", 1)
        key = key.strip().lstrip("{").rstrip("}").strip()
        # coerce ints when obvious
        if value.isdigit():
            out[key] = int(value)
        else:
            out[key] = value
    return out


def main(argv: list[str] | None = None) -> int:
    cfg = load_config()
    scenarios = sorted((cfg.get("prompt_scenarios") or {}).keys())
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scenario", choices=scenarios, help="Named scenario from YAML")
    ap.add_argument("--set", dest="sets", action="append", default=[], metavar="KEY=VALUE",
                    help="Override a prompt variable (repeatable)")
    ap.add_argument("--full", action="store_true",
                    help="Also write FULL.md = prompt file + request block")
    ap.add_argument("--stdout", action="store_true", help="Print the request block to stdout")
    ap.add_argument("--list-scenarios", action="store_true", help="List scenarios and exit")
    args = ap.parse_args(argv)

    if args.list_scenarios:
        for name in scenarios:
            print(name)
        return 0

    overrides = parse_set_args(args.sets)
    values = resolve_vars(cfg, args.scenario, overrides)
    if not values.get("LEVEL"):
        raise SystemExit("LEVEL is required. Set it in YAML or pass --set LEVEL=BREVET")

    request_md = format_request_block(values, cfg, args.scenario)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tag = args.scenario or "defaults"
    prompts_dir = OUTPUT["prompts"]
    base = prompts_dir / f"{stamp}_{tag}"
    req_path = Path(str(base) + "_REQUEST.md")
    vars_path = Path(str(base) + "_vars.json")
    req_path.write_text(request_md, encoding="utf-8", newline="\n")
    vars_path.write_text(
        json.dumps(
            {
                "generated": datetime.now().isoformat(timespec="seconds"),
                "scenario": args.scenario,
                "values": values,
                "referentiel": str(HERE),
                "config": str(CONFIG),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {req_path}")
    print(f"Wrote {vars_path}")
    if args.full:
        full_path = Path(str(base) + "_FULL.md")
        full_path.write_text(build_full_document(request_md, cfg), encoding="utf-8", newline="\n")
        print(f"Wrote {full_path}")
    if args.stdout:
        print("\n" + request_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
