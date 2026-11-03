# QUIZ_PROMPT

Testing the French math diagnostic prompt (Brevet / Bac / MPI) against the CLAUDE v11 reference.

> **Status:** structural PASS, paper **HOLD**, digital **HOLD** (0 PASS, 594 HOLD, 6 FAIL). Nothing here is approved for student assessment. Error codes are hypotheses.

## Contents

- `Math_Diagnostic_Reference_CLAUDE_v11/`: the v11 reference package and test kit, including the prompt (`PROMPT_Diagnostic_Maths_Brevet_Bac_MPI_v9.md`), agent rules (`AGENT_RULES_v11.md`), validator, regression tests, testing guide (`GUIDE_Math_Diagnostic_v11_Testing_and_HTML_EN.md`), dashboard and demo quiz.
- `test_runs/2026-11-03_BR-NC/`: a short Brevet BR-NC diagnostic generated from prompt v9, checked with SymPy, with student and teacher HTML pages and a checklist report (`BR-NC_check.md`).

## Run the checks (Linux / Debian)

```bash
cd Math_Diagnostic_Reference_CLAUDE_v11
python3 -m venv .venv
.venv/bin/python -m pip install 'sympy==1.14.0'
.venv/bin/python -I tests_v11.py              # expect 21/21
.venv/bin/python -I build_v11.py --check      # expect 8 files, 0 differ (never run without --check)
.venv/bin/python -I validate_reference_v11.py # expect STRUCTURAL_PASS, paper/digital HOLD
.venv/bin/python -I v11_html_dashboard.py
```

On Windows, use `RUN_TESTS_V11.cmd` (see the guide).

Verified on Debian 13, Python 3.13.5, SymPy 1.14.0 (2026-11-03).
