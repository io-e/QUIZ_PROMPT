# Math Diagnostic CLAUDE v11 — user testing and HTML guide

**Version:** CODEX support kit, 3 November 2026  
**Audience:** teachers, project maintainers and Windows users.  
**Source:** `Math_Diagnostic_Reference_CLAUDE_v11.zip`, especially `README_v11.md`, `tests_v11.py`, `validate_reference_v11.py`, `build_v11.py`, and their reports.

> **Release warning:** this entire reference is still **HOLD** for both paper and digital. Technical checks passing is **not** permission to release questions to students. The HTML quiz included here is a local *demonstration* only, with hand-authored, unvalidated examples. Error codes are hypotheses, not diagnoses.

## 1. What you can test today

| Test | Command in the v11 folder | What PASS means | What it does **not** mean |
|---|---|---|---|
| Python environment | `py -3 --version` / `py -3 -c "import sympy; print(sympy.__version__)"` | Python and SymPy import correctly | All mathematics is correct |
| Regression tests | `py -3 -I tests_v11.py` | 21 programmed regression scenarios pass | The 600 rows are approved |
| Reproducible build | `py -3 -I build_v11.py --check` | Eight generated files match the packaged copies | A new build is safe to overwrite your reviews |
| Reference validator | `py -3 -I validate_reference_v11.py` | No **blocking structural finding** | Curriculum, pedagogical, pilot or player approval |
| HTML report | `py -3 -I v11_html_dashboard.py` | An HTML page is produced from the current JSON/CSV reports | It has run any of the tests itself |
| HTML quiz demonstration | `py -3 -I make_demo_quiz_html.py` | An HTML prototype is produced from an example JSON | It is compatible with the `alphavalon.eval/v1` player or ready for pupils |

**Independently checked in this session:** Python **3.13.5**, SymPy **1.14.0**; `tests_v11.py` **21/21 PASS**; `build_v11.py --check` **8 files, 0 differ**; validator exit code **0**, **zero structural blockers**. The report still says **paper HOLD / digital HOLD**, with **0 PASS, 594 HOLD, 6 FAIL**.

## 2. Install prerequisites on Windows

1. Install a supported Python 3 interpreter and ensure `py` is available in Windows Terminal or PowerShell. The package has been exercised on Python 3.13.5 and SymPy 1.14.0; other versions should be retested.
2. Extract the supplied **test kit ZIP**. Inside it is the `Math_Diagnostic_Reference_CLAUDE_v11` folder containing the scripts, data, and this guide.
3. In File Explorer, open that extracted folder, click the address bar, type `powershell`, and press Enter.
4. Create an isolated Python environment and install the dependency:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "sympy==1.14.0"
.\.venv\Scripts\python.exe -c "import sympy; print(sympy.__version__)"
```

Using `.venv` avoids `--user` installation problems: Python's `-I` mode does not include user-site packages. If PowerShell does not allow activation of virtual environments, **activation is not required** when you call `.venv\Scripts\python.exe` explicitly as shown.

**Alternative:** if SymPy is already installed for `py -3`, simply use the commands in section 3. You do not need to install another copy.

## 3. Run the checks yourself

### Option A — Windows, one double-click

Double-click **`RUN_TESTS_V11.cmd`** inside the extracted package folder. It uses `.venv\Scripts\python.exe` when the environment exists; otherwise it uses `py -3`. It runs in this order:

1. `tests_v11.py` — 21 regression scenarios.
2. `build_v11.py --check` — read-only rebuild comparison.
3. `validate_reference_v11.py` — structural validator and reports.
4. `v11_html_dashboard.py` — generates the visual HTML report.

Then open `validation_dashboard_v11.html` in your browser. The command window also writes `tests_output_v11.txt` and `validator_output_v11.txt`.

### Option B — Windows, manual commands

In the PowerShell terminal opened in the package folder:

```powershell
.\.venv\Scripts\python.exe -I tests_v11.py
.\.venv\Scripts\python.exe -I build_v11.py --check
.\.venv\Scripts\python.exe -I validate_reference_v11.py
.\.venv\Scripts\python.exe -I v11_html_dashboard.py
Start-Process .\validation_dashboard_v11.html
```

If you did not create a virtual environment, replace `.\.venv\Scripts\python.exe` with `py -3`.

### Option C — Linux / macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install 'sympy==1.14.0'
.venv/bin/python -I tests_v11.py
.venv/bin/python -I build_v11.py --check
.venv/bin/python -I validate_reference_v11.py
.venv/bin/python -I v11_html_dashboard.py
```

Open `validation_dashboard_v11.html` in your browser. These steps do not require a web server.

### Expected exit codes

For the **validator**: `0` = no blocking structural findings; `1` = blocking findings; `2` = could not run (e.g. missing files or SymPy). For the **regression tests**: `0` = all scenarios passed; `1` = at least one failed. For `build_v11.py --check`: `0` = all eight generated files match; `1` = at least one differs.

**Critical:** Do **not** run `build_v11.py` without `--check` once reviews have been entered: its normal build mode rewrites the generated reference, target CSV, and `Item_Review_Register_v11.csv` from the bundled baseline. Back up all edited files first.

## 4. Read the validation outputs

| File | Purpose | Can you edit it manually? |
|---|---|---|
| `validation_report_v11.json` | Machine-readable findings, seven gates, release status, environment | **No**: generated by validator |
| `validation_report_v11.txt` | Human-readable validation summary | No |
| `qa_v11.json` | Concise QA summary for the reference | No |
| `Item_Release_Eligibility_v11.csv` | Per-item PASS/HOLD/FAIL and reasons, separate paper/digital | **No**: generated |
| `Coverage_Gaps_v11.csv` | Unchecked keys, numeric/text/infinity signatures, intermediate checks | **No**: generated |
| `Item_Review_Register_v11.csv` | BO evidence, teacher review, text review and pilot records | **Yes**, with real evidence and backups |
| `Anchor_Verification_Worklist_v11.csv` | List of 152 provisional anchors to check against official BO passages | Yes, record actual evidence |
| `Math_ID_Migration_to_v11.csv` | Cross-version legacy mappings, including 301 CODEX v5 targets | Yes, but only after carefully verifying mappings |
| `Math_Diagnostic_Targets_v11.csv` | Core reference data including proposed error patterns | Only through a coordinated source/reference update; direct edits will break structural consistency |

Seven gates in the JSON report: `STRUCTURE_PASS`, `CALCULATION_PASS`, `CURRICULUM_PASS`, `LEGACY_MIGRATION_PASS`, `PLAYER_SCHEMA_PASS`, `TEACHER_REVIEW_PASS`, `DIAGNOSTIC_VALIDITY_PASS`. Paper release does not require the player gate; digital release does. **No gate should be marked PASS merely to produce an all-green dashboard.**

**Current baseline gaps from v11:** 249 unchecked answer keys; 458 unchecked numeric wrong-answer signatures and 5 unchecked infinity signatures; 901 text signatures needing review; 58 legacy checks concerning intermediate values. Programme work: 152 provisional anchors and six unsupported rows (`1C-FN-05`…`1C-FN-10`, excluded). Legacy migrations: 301 to review. The player schema and real pilot evidence are not supplied.

## 5. How to review one target (teacher workflow)

Example: **`BR-NC-01`**. This is a *procedure*, not a claim that the item already passes.

1. Open `Math_Diagnostic_Targets_v11.csv` and find `BR-NC-01`. Inspect `capability`, `official_ref`, `mcq_seed`, `mcq_key`, `open_seed`, `open_target`, and `errors_json`.
2. Open the actual, applicable official programme and locate the **page or stable section and the supporting passage**. Check the school year and track. If it does not support the capability, mark it unsupported rather than forcing a match.
3. In `Anchor_Verification_Worklist_v11.csv` (when the row is listed), record the actual page, passage, teacher, date and supporting evidence. **This worklist alone does not update the release gate.**
4. In the corresponding row of `Item_Review_Register_v11.csv`, fill `bo_match=SUPPORTED`, `bo_page`, `bo_passage`, `bo_reviewer`, `bo_reviewed_on`. Only enter `SUPPORTED` when the official source genuinely supports the exact capacity.
5. Independently recompute the student answer and every relevant distractor on the **correct seed** (MCQ vs open). Add missing checks to the matching `chk_*.py` through a reviewed code change. The CSV log cannot replace a missing numeric check.
6. For every text signature, review the mathematical meaning and wording. Only then set `text_signatures_reviewed=YES` with `text_reviewer`, `text_reviewed_on` and `text_review_note`.
7. Perform a real teaching review and record `teacher_item_review=APPROVED`, `teacher_reviewer` and `teacher_reviewed_on`, once ready.
8. Collect genuinely independent pilot evidence and a documented interpretation of the error signatures. Only verified evidence justifies setting `research_status=PILOT_SUPPORTED` or `RESEARCH_DOCUMENTED` for each active error (requires a coordinated data/reference rebuild). Enter `pilot_status=PILOTED`, `pilot_evidence_id`, and `pilot_reviewed_on` **only after** the corresponding pilot.
9. Review the 301 legacy mappings separately. `review_status=REVIEWED` in the migration table must represent an actual checked equivalence, not a bulk change.
10. Rerun the tests, validator and dashboard. Check the row in `Item_Release_Eligibility_v11.csv` for **each** remaining HOLD reason.

Dates must be written `YYYY-MM-DD`. The current validator checks the **date shape**, but this alone does not prove the date or the signed review is genuine. Maintain evidence files separately.

## 6. Build an HTML dashboard (technical checks)

The supplied `v11_html_dashboard.py` reads the current `validation_report_v11.json`, `Item_Release_Eligibility_v11.csv`, and `Coverage_Gaps_v11.csv` and writes **`validation_dashboard_v11.html`**.

```powershell
.\.venv\Scripts\python.exe -I validate_reference_v11.py
.\.venv\Scripts\python.exe -I v11_html_dashboard.py
Start-Process .\validation_dashboard_v11.html
```

It displays gates, counts, per-target status/reasons, and filterable open gaps; filtered tables can be saved as CSV. It is a **static read-only report**: the browser cannot run the Python validator itself. Re-run both commands to refresh the page after changing input files. The HTML works offline and contains no external resources or network calls.

## 7. Create an interactive HTML question page

**There are two different workflows:**

- **Prototype only:** `make_demo_quiz_html.py` converts the included **hand-reviewed demonstration JSON** to one standalone HTML file (`diagnostic_prototype_v11.html`). You can open it directly in a browser. It contains three MCQs with an optional « Je ne sais pas » response and confidence choice, plus an open Brevet geometry demonstration that explicitly needs manual grading. Distractor codes shown after answering are **hypotheses**, not validated student diagnoses.
- **Production route:** choose eligible `PASS` rows → have the prompt generate complete student/teacher questions → produce the required `alphavalon.eval/v1` YAML → validate it with the **actual player schema** (`alphavalon-eval-v1.schema.json`) → run the player smoke test → record the test evidence (`Player_Validation_Record_v11.json`) → release only after the digital and content gates pass. The player's schema is **not in v11**, and this kit does not invent or bypass it.

### Generate the prototype

```powershell
.\.venv\Scripts\python.exe -I make_demo_quiz_html.py
Start-Process .\diagnostic_prototype_v11.html
```

### Change the prototype questions

Edit `quiz_demo_v11.json` in VS Code, preserving this simple *demonstration-only* structure:

```json
{
  "title": "Diagnostic de calcul — démonstrateur v11",
  "items": [
    {
      "id": "DEMO-01",
      "type": "mcq",
      "skill_id": "BR-NC-06",
      "question": "Calculer : −5 − (−8)",
      "options": [
        {"text": "−13", "correct": false, "error_code": "CB-SGN-02", "why": "Erreur de signe possible"},
        {"text": "3", "correct": true},
        {"text": "−3", "correct": false, "error_code": "LOCAL", "why": "Signe inversé possible"},
        {"text": "13", "correct": false, "error_code": "LOCAL", "why": "Valeurs absolues additionnées"}
      ],
      "solution": "−5 − (−8) = −5 + 8 = 3."
    }
  ]
}
```

The prototype generator checks that each MCQ has **four distinct options, one correct option, and explanations for all distractors**. An `open` item needs an `id`, `type`, `skill_id`, `question` and `solution`. It **does not** mathematically verify the answers or check BO eligibility.

### Important implementation limits

- An HTML file cannot directly execute local Python scripts without a separately built and secured backend. Use the `.cmd` file or terminal for testing; open the generated report in a browser.
- An offline HTML quiz is **not** an `alphavalon.eval/v1` schema-validation test. It does not create `Player_Validation_Record_v11.json`.
- Open answers are not automatically marked, and no student scores are transmitted or stored remotely.
- Do not use the prototype as a real diagnostic until the curriculum, mathematics, distractor hypotheses, privacy and teacher gates have been met.

## 8. Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| `ModuleNotFoundError: No module named sympy` | Wrong Python environment; a `--user` install is hidden by `-I` | Install SymPy inside `.venv` and run its Python executable |
| `NOT RUN: missing file ...` | Working folder or extraction incomplete | Extract the entire ZIP and run from the folder containing `validate_reference_v11.py` |
| `rebuild check: 8 files, 1 differ` | Files were changed, or input/source is out of sync | Compare filenames/hashes; **do not** rebuild over a review register without a backup |
| `STRUCTURAL_PASS` but HOLD | Expected: structural checks ≠ release gates | Inspect `Item_Release_Eligibility_v11.csv` and open gaps |
| Dashboard seems outdated | It was generated from an older report | Re-run validator then `v11_html_dashboard.py` |
| Unicode characters wrong in Excel | CSV encoding mishandled | Import CSV as UTF-8, do not silently change separators or IDs |
| `PLAYER_SCHEMA_PASS` unverified | Actual player schema and smoke-test record unavailable | Test against the real schema and real player, then preserve the evidence |
| Generated quiz opens but no questions | Edited JSON invalid or generator failed | Run `make_demo_quiz_html.py` and read its validation error |

## 9. First useful acceptance test

On your machine, first confirm **regression 21/21**, **rebuild 8/8**, **structural findings 0**, and **overall paper/digital HOLD**. Open the HTML dashboard, filter `BR-NC-01`, and inspect its specific missing evidence. Then generate the demonstration quiz and answer the sign and parentheses MCQs. This validates your local **technical workflow**, not the pedagogical release.
