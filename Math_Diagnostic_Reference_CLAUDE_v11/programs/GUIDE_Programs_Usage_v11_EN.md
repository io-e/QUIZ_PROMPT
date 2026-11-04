# Math Diagnostic v11 — Programs usage guide

**Version:** 11.0 · 2026-11-04  
**Audience:** maintainers and teachers who run the reference tooling on Windows (PowerShell) or call the Python scripts directly.  
**Related:** `GUIDE_Math_Diagnostic_v11_Testing_and_HTML_EN.md`, `GUIDE_Prompt_Usage_v10_EN.md`, `HANDOFF_CLAUDE_Questionnaire_Usage_v1.md`, `README_v11.md`.

> **Status warning:** of the 600 rows of reference v11, **594 are `HOLD`** and **6 are `FAIL`** (`1C-FN-05`…`10`, never usable); **none is `PASS`**. A structural pass of the validator is **not** pedagogical approval. Anything produced with the diagnostic prompt is a **draft** (`UNVALIDATED — HOLD`).

> **Layout change (v11 programs package):** all Python entry points and check modules live under `programs/scripts/`. PowerShell wrappers live under `programs/wrappers/`. Parameters live in `programs/config/programs_v11.yaml` (with a JSON twin for `python -I`). Thin shims remain at the package root so older commands still work.

---

## 1. What this package is for

| Goal | Use |
|---|---|
| Check that the **curriculum reference** (CSV + Markdown + eligibility) is structurally consistent | `Invoke-ValidateReference.ps1` / `validate_reference_v11.py` |
| Regression-test eligibility rules | `Invoke-Tests.ps1` / `tests_v11.py` |
| Rebuild or diff generated v11 files | `Invoke-Build.ps1` / `build_v11.py` |
| Browse the last validation report in HTML | `Invoke-Dashboard.ps1` / `v11_html_dashboard.py` |
| Build a **local demo** HTML quiz (hand-authored JSON only) | `Invoke-DemoQuiz.ps1` / `make_demo_quiz_html.py` |
| Build a **ready-to-paste prompt request** from YAML defaults/scenarios | `Invoke-MakePrompt.ps1` / `make_prompt_request_v11.py` |
| Run the full technical kit | `Invoke-AllChecks.ps1` or `RUN_TESTS_V11.cmd` |

**Out of scope for these programs**

- Generating a full student assessment from the 600 catalogue rows (that is the LLM + `PROMPT_…` workflow).
- Marking student scripts or writing error logs.
- Approving rows for `PASS` / quiz `VALIDATED` (human + registers).

---

## 2. Directory layout

```text
Math_Diagnostic_Reference_CLAUDE_v11/          ← default REFERENTIEL (data root)
├── French_Math_Diagnostic_Curriculum_Reference_CLAUDE_EN_v11.md
├── Math_Diagnostic_Targets_v11.csv
├── Item_Release_Eligibility_v11.csv
├── Item_Review_Register_v11.csv
├── PROMPT_Diagnostic_Maths_Brevet_Bac_MPI_v9.md
├── build/                                     ← inputs for build_v11.py
├── validation_report_v11.json|.txt            ← written by the validator into the referentiel
├── validation_dashboard_v11.html
├── RUN_TESTS_V11.cmd                          ← calls programs wrappers when present
├── validate_reference_v11.py                  ← thin shim → programs/scripts/
├── tests_v11.py                               ← thin shim
├── build_v11.py                               ← thin shim
├── v11_html_dashboard.py                      ← thin shim
├── make_demo_quiz_html.py                     ← thin shim
└── programs/                                  ← tooling package
    ├── GUIDE_Programs_Usage_v11_EN.md         ← this file
    ├── config/
    │   ├── programs_v11.yaml                  ← source of truth for parameters
    │   └── programs_v11.json                  ← twin for python -I (no user-site PyYAML)
    ├── lib/
    │   └── Common.ps1                         ← shared PowerShell helpers
    ├── wrappers/
    │   ├── Invoke-AllChecks.ps1
    │   ├── Invoke-ValidateReference.ps1
    │   ├── Invoke-Tests.ps1
    │   ├── Invoke-Build.ps1
    │   ├── Invoke-Dashboard.ps1
    │   ├── Invoke-DemoQuiz.ps1
    │   └── Invoke-MakePrompt.ps1
    ├── scripts/
    │   ├── ea_paths.py                        ← resolves referentiel / output / config
    │   ├── validate_reference_v11.py
    │   ├── tests_v11.py
    │   ├── build_v11.py
    │   ├── check_values_v6.py
    │   ├── chk_*.py, v7lib.py, v8lib.py
    │   ├── v11_html_dashboard.py
    │   ├── make_demo_quiz_html.py
    │   └── make_prompt_request_v11.py         ← NEW: builds prompt requests from YAML
    ├── referentiel/
    │   └── README.md                          ← explains default referentiel = parent
    └── output/
        ├── validation/                        ← mirrored reports
        ├── prompts/                           ← generated REQUEST / FULL / vars
        ├── dashboards/
        ├── demos/
        ├── logs/
        └── builds/
```

### Path resolution order

1. Environment variables (highest priority):
   - `EA_EVAL_REFERENTIEL` — curriculum/data root  
   - `EA_EVAL_OUTPUT` — programs output root  
   - `EA_EVAL_PROGRAMS` — `programs/` folder  
2. `programs/config/programs_v11.yaml` → `paths.referentiel` / `paths.output`  
3. Defaults: referentiel = parent of `programs/`, output = `programs/output/`

Wrappers set the three environment variables before calling Python.

---

## 3. Configuration (`programs_v11.yaml`)

Edit the YAML; then regenerate the JSON twin so `python -I` keeps working:

```powershell
py -3 -c "import yaml,json; from pathlib import Path; p=Path('programs/config/programs_v11.yaml'); Path('programs/config/programs_v11.json').write_text(json.dumps(yaml.safe_load(p.read_text(encoding='utf-8')), ensure_ascii=False, indent=2), encoding='utf-8')"
```

(Requires PyYAML in a non-isolated interpreter. The twin is already shipped.)

### 3.1 `python` block

| Key | Meaning |
|---|---|
| `launcher` / `version_arg` | Default `py` / `-3` on Windows |
| `venv_candidates` | Checked first (programs `.venv`, then referentiel `.venv`) |
| `isolated` | Wrappers pass `-I` so user-site packages are ignored |
| `pip_packages` | Recommended: `sympy==1.14.0`, `PyYAML>=6.0` |

**Important:** under `-I`, packages installed with `pip install --user` are invisible. Prefer a venv:

```powershell
cd Math_Diagnostic_Reference_CLAUDE_v11\programs
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "sympy==1.14.0" "PyYAML>=6.0"
```

Then wrappers pick `programs\.venv\Scripts\python.exe` automatically.

### 3.2 `prompt_defaults`

Defaults for `make_prompt_request_v11.py` (PROMPT §0 variables):

| Variable | Default in YAML | Notes |
|---|---|---|
| `LEVEL` | `BREVET` | Required for a complete request |
| `SUBJECT` | `ALL` | Or comma-separated catalogue codes |
| `PURPOSE` | `Entry diagnostic` | |
| `ASSESSMENT_MODE` | `DIAGNOSTIC` | `EXAM_SIMULATION` · `TRAINING` |
| `LEARNER_PROFILE` | _(empty → derived)_ | e.g. `Tle → MP2I entry` |
| `EXAM_SESSION` | `2028` | |
| `DURATION` | `55` | minutes |
| `NB_MCQ` / `NB_OPEN` | `12` / `3` | v9 defaults |
| `TEST_LENGTH` | `FULL` | **Handoff / expected PROMPT v10** (`FULL`\|`SHORT`); still marked preview while v10 is missing |
| `CALCULATOR` | `Not allowed` | |
| `DELIVERY` | `Paper` | |
| `ADAPTATIONS` | `None` | |
| `OUTPUT_LANGUAGE` | `French` | |
| `REFERENCE` | `French_Math_…_v11.md` | |
| `TARGET_CODES` | `AUTO` | |
| `DIAGNOSTIC_OPTIONS` | `NSP, CONFIDENCE` | Clear for exam simulation |
| `OUTPUT_FORMAT` | `MARKDOWN` | `YAML` · `BOTH` |

### 3.3 `prompt_scenarios`

Named presets merged over defaults:

| Scenario | Intent |
|---|---|
| `quick_brevet_entry` | `SHORT`, 20 min, 5 MCQ + 2 open |
| `full_brevet_entry` | Full defaults |
| `exam_simulation_brevet` | Exam mode, no diagnostic options |
| `premiere_spe_midyear` | `BAC_1RE_SPE` mid-year |
| `mp2i_entry` | MP2I entry profile |
| `mpi_with_prereq` | MPI (prompt still enforces ≥ 20 % `M1-*`) |

---

## 4. PowerShell wrappers

Open PowerShell in the package (or use absolute paths). Execution policy for the current process only:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
cd C:\ALF_ZGit\EA-EVAL_TOOLS\Math_Diagnostic_Reference_CLAUDE_v11
```

### 4.1 Full technical kit

```powershell
pwsh -NoProfile -File .\programs\wrappers\Invoke-AllChecks.ps1 -ContinueOnBuildDiff
```

Order: tests → `build_v11.py --check` → validate → dashboard → mirror reports to `programs/output/validation/`.  
On Windows, pass `-ContinueOnBuildDiff` when the build step fails only because of CRLF vs LF (see §5.4).

### 4.2 Individual actions

```powershell
pwsh -NoProfile -File .\programs\wrappers\Invoke-Tests.ps1
pwsh -NoProfile -File .\programs\wrappers\Invoke-Build.ps1              # --check (safe)
pwsh -NoProfile -File .\programs\wrappers\Invoke-Build.ps1 -Apply       # writes files (confirm)
pwsh -NoProfile -File .\programs\wrappers\Invoke-ValidateReference.ps1
pwsh -NoProfile -File .\programs\wrappers\Invoke-Dashboard.ps1
pwsh -NoProfile -File .\programs\wrappers\Invoke-DemoQuiz.ps1
```

Optional: `-PythonExe 'C:\path\to\python.exe'` on any wrapper.  
Optional: `-WhatIf` on wrappers that support `SupportsShouldProcess` to print resolved paths.

### 4.3 Prompt request builder

```powershell
# List scenarios
pwsh -NoProfile -File .\programs\wrappers\Invoke-MakePrompt.ps1 -ListScenarios

# Quick Brevet entry (SHORT)
pwsh -NoProfile -File .\programs\wrappers\Invoke-MakePrompt.ps1 -Scenario quick_brevet_entry

# Full paste file = PROMPT v9 body + request block
pwsh -NoProfile -File .\programs\wrappers\Invoke-MakePrompt.ps1 -Scenario full_brevet_entry -Full

# Overrides
pwsh -NoProfile -File .\programs\wrappers\Invoke-MakePrompt.ps1 -Scenario mp2i_entry -Set LEVEL=MP2I -Set DURATION=40
```

**Outputs** (under `programs/output/prompts/`):

| File | Content |
|---|---|
| `*_REQUEST.md` | Instructions, attachment checklist, `{VAR} = value` block |
| `*_vars.json` | Machine-readable resolved values + paths |
| `*_FULL.md` | Entire prompt file + request (with `-Full`) |

Paste workflow: open a new LLM chat → paste prompt (or use `*_FULL.md`) → attach reference CSV/MD → paste variable block → check RaR → generate.

---

## 5. Python programs (detailed)

### 5.1 `ea_paths.py`

Shared path bootstrap. Functions: `programs_root()`, `data_root()`, `scripts_root()`, `output_root()`, `config_path()`, `ensure_output_dirs()`, `bootstrap_sys_path()`, `_load_config_data()`.

Every entry script inserts its own directory on `sys.path` before importing `ea_paths` (required because `python -I` does not put the script directory first in this environment).

### 5.2 `validate_reference_v11.py`

**Purpose:** structural validation of the **reference package**, not of a generated quiz.

**Reads (referentiel):** targets CSV, curriculum Markdown, official index, migration table, legacy IDs, review register, optional player validation record, and loads `chk_*.py` / `check_values_v6.py` from `programs/scripts/`.

**Writes (referentiel):** `validation_report_v11.json`, `validation_report_v11.txt`, `qa_v11.json`, `Item_Release_Eligibility_v11.csv`, `Coverage_Gaps_v11.csv`.

**Exit codes:** `0` = no blocking finding (structural pass only); `1` = blockers; `2` = could not run (e.g. missing SymPy).

**Gates reported:** STRUCTURE, CALCULATION, CURRICULUM, LEGACY_MIGRATION, PLAYER_SCHEMA, TEACHER_REVIEW, DIAGNOSTIC_VALIDITY. Paper and digital eligibility are separate.

### 5.3 `tests_v11.py`

**Purpose:** 21 regression scenarios for `row_eligibility()` and related helpers inside the validator module.

**Does not** re-validate all 600 rows end-to-end (that is the validator’s job).

### 5.4 `build_v11.py`

**Purpose:** rebuild selected v11 artefacts from `build/inputs_v10/`.

| Mode | Command | Effect |
|---|---|---|
| Check | `build_v11.py --check` | Compare generated temp outputs to packaged files; no overwrite |
| Apply | `build_v11.py` (wrapper `-Apply`) | Write into the referentiel |

**Windows line endings (CRLF):** on Windows checkouts, `--check` often reports **8 files, 2 differ** even when the content is the same. The two files are typically the reference Markdown and `Item_Review_Register_v11.csv`: they are stored with **CRLF** in git, while the builder writes **LF**. This is independent of the `programs/` migration. A “0 differ” result was verified on Debian/LF environments. Do **not** treat a CRLF-only diff as a curriculum regression.

To finish the rest of the kit on Windows after a CRLF-only build diff:

```powershell
pwsh -NoProfile -File .\programs\wrappers\Invoke-AllChecks.ps1 -ContinueOnBuildDiff
```

### 5.5 `check_values_v6.py` and `chk_*.py`

**Purpose:** independent recomputation of keys and wrong-answer signatures (Brevet, Première, Terminale tracks, MP2I, MPI, v7 fixes, v8 additions). Invoked **in-process** by the validator. Not meant as day-to-day CLI tools for teachers.

Supporting libraries: `v7lib.py`, `v8lib.py`.

### 5.6 `v11_html_dashboard.py`

**Purpose:** static HTML dashboard from the latest JSON/CSV reports. Read-only; does not run validation. Writes `validation_dashboard_v11.html` into the referentiel and mirrors a copy under `programs/output/dashboards/`.

### 5.7 `make_demo_quiz_html.py`

**Purpose:** HTML prototype from `quiz_demo_v11.json` (hand-reviewed demo items only). **Not** a converter from the 600-row catalogue. Mirrors HTML to `programs/output/demos/`.

### 5.8 `make_prompt_request_v11.py` (new)

**Purpose:** turn YAML defaults/scenarios into a paste-ready request for the diagnostic prompt.

```text
py -3 -I programs\scripts\make_prompt_request_v11.py --scenario quick_brevet_entry
py -3 -I programs\scripts\make_prompt_request_v11.py --full --set LEVEL=MPI
py -3 -I programs\scripts\make_prompt_request_v11.py --list-scenarios
```

Does **not** call an LLM and does **not** generate items.

---

## 6. Environment setup (Windows)

1. Install Python 3. Ensure `py -3` works. This programs package has been exercised on **Python 3.12.10** (current Windows machine) and earlier kit notes mention **3.13.x / SymPy 1.14**. Re-check SymPy after changing interpreters.
2. Create a venv under `programs/` (recommended) or under the referentiel root.
3. Install SymPy (required for validator/tests). Install PyYAML if you edit YAML and regenerate the JSON twin (needed when the non-isolated interpreter lacks PyYAML; `python -I` uses the JSON twin).
4. From the package root:

```powershell
pwsh -NoProfile -File .\programs\wrappers\Invoke-AllChecks.ps1 -ContinueOnBuildDiff
```

5. Open `validation_dashboard_v11.html` (referentiel or `programs/output/dashboards/`).

**Double-click alternative:** `RUN_TESTS_V11.cmd` (delegates to `Invoke-AllChecks.ps1 -ContinueOnBuildDiff` when present).

### Wrapper exit codes

`Invoke-ProgramsPython` in `lib/Common.ps1` must return **only** the integer exit code. Logging goes to the host via `Out-Host` (and to `output/logs/`). An earlier Tee-Object pipeline made wrappers return log lines plus the code, so `Invoke-AllChecks` / `Invoke-Tests` / `Invoke-ValidateReference` reported failure even when Python succeeded.

---

## 7. Typical workflows

### A. After editing the curriculum Markdown or targets CSV

1. `Invoke-ValidateReference.ps1`  
2. Read `validation_report_v11.txt` and eligibility counts (expect 594 HOLD / 6 FAIL until reviews land).  
3. `Invoke-Dashboard.ps1`  
4. Optional: copy mirrored files from `programs/output/validation/` into a review bundle.

### B. Prepare a classroom diagnostic request (draft)

1. Edit `prompt_defaults` or pick a `prompt_scenarios` entry.  
2. `Invoke-MakePrompt.ps1 -Scenario quick_brevet_entry -Full`  
3. Paste into the LLM with attachments.  
4. Treat the result as `UNVALIDATED — HOLD`. Follow `GUIDE_Prompt_Usage_v10_EN.md` Part B for marking and follow-up.

### C. Safe rebuild check after pulling package updates

```powershell
pwsh -NoProfile -File .\programs\wrappers\Invoke-Build.ps1
```

Use `-Apply` only when you intend to overwrite generated files and understand the impact on the review register.

---

## 8. Mapping to the prompt / guide ecosystem

| Concern | Document / tool |
|---|---|
| How to fill `{LEVEL}`, interpret T1–T10, evidence states | `GUIDE_Prompt_Usage_v10_EN.md` |
| Corrections from the questionnaire handoff | `HANDOFF_CLAUDE_Questionnaire_Usage_v1.md` |
| Filling defaults without hand-editing each chat | `make_prompt_request_v11.py` + YAML |
| Structural truth of the 600 rows | `validate_reference_v11.py` |
| Human release to `VALIDATED` | Review register + eligibility `PASS` + teacher approval (not automated here) |

`PROMPT_Diagnostic_Maths_Brevet_Bac_MPI_v10.md` is **not** in the repository. YAML still carries `TEST_LENGTH` for forward compatibility; the generated request notes the v9 equivalent (`NB_MCQ` / `NB_OPEN` / `DURATION`).

---

## 9. Exit codes and logs

| Source | 0 | Non-zero |
|---|---|---|
| Validator | No blocking finding | `1` blockers / `2` cannot run |
| Tests | All scenarios pass | One or more failed |
| Build `--check` | Packaged files match | Drift detected |
| Make-prompt | Files written | Config/scenario error |

Logs: `programs/output/logs/*.log` when using wrappers.

---

## 10. Compatibility shims

Root-level `validate_reference_v11.py`, `tests_v11.py`, `build_v11.py`, `v11_html_dashboard.py`, and `make_demo_quiz_html.py` are **shims**. They set `EA_EVAL_*` and `runpy` the real scripts under `programs/scripts/`. Prefer the PowerShell wrappers for new work.

---

## 11. Known limits

- Validator ≠ quiz checker.  
- Demo HTML ≠ catalogue assessment.  
- `TEST_LENGTH` awaits PROMPT v10.  
- JSON twin must be regenerated after YAML edits if you rely on `python -I` without a venv PyYAML.  
- Eligibility remains HOLD/FAIL until human BO review, teacher review, and pilot evidence move rows.  
- `build_v11.py --check` may fail on Windows because of CRLF vs LF (see §5.4); use `-ContinueOnBuildDiff` when that is the only issue.  
- Root shims exist only for the five entry points (validate, tests, build, dashboard, demo). `chk_*`, `v7lib`, and `v8lib` live under `programs/scripts/` only.  
- Validator runs rewrite generated reports under the referentiel; `programs/output/` mirrors copies. `SHA256SUMS.txt` may be stale after a re-run.  
- Nothing in this package commits or pushes git state.

## 12. Verification notes (honest status)

| Check | Status on Windows (programs package) |
|---|---|
| `tests_v11.py` (direct + shim + wrapper) | PASS 21/21 when wrappers return a pure exit code |
| `validate_reference_v11.py` | Exit 0, `STRUCTURAL_PASS`, 594 HOLD / 6 FAIL |
| `Invoke-MakePrompt.ps1 -Scenario quick_brevet_entry` | Writes REQUEST / vars (and FULL with `-Full`) |
| `build_v11.py --check` | Often **2 differ** on Windows (CRLF); not a migration regression |
| Dashboard / demo via wrappers | Run after the exit-code fix; confirm locally |
| Release posture | Unchanged: no PASS rows, drafts stay HOLD |

---

## 13. Quick command card

```powershell
# One-shot technical kit (Windows: allow CRLF-only build diff)
pwsh -NoProfile -File .\programs\wrappers\Invoke-AllChecks.ps1 -ContinueOnBuildDiff

# Prompt pack for a short Brevet entry test
pwsh -NoProfile -File .\programs\wrappers\Invoke-MakePrompt.ps1 -Scenario quick_brevet_entry -Full

# Validator only
pwsh -NoProfile -File .\programs\wrappers\Invoke-ValidateReference.ps1
```

```text
programs/output/prompts/   ← paste-ready requests
programs/output/validation/← mirrored reports
programs/output/logs/      ← wrapper logs
```
