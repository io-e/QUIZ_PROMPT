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

## Programme versioning (draft, `programme-versioning-v1`)
`quiz_eval/` is a shared, stdlib-only engine that selects the official programme by **subject + grade + track + school year**. Exam rules are selected **separately by session**. The engine writes a version manifest that records four versions: curriculum edition, reference version, exam session and software version.

```bash
python3 -I tests/test_versioning.py          # 29 tests, including the 12 Codex golden cases
python3 -I -c "import sys; sys.path.insert(0,'.'); from quiz_eval import programme_resolver as P; \
  print(P.manifest_bytes(P.resolve('HISTORICAL_EXAM','mathematics','3e','general',assessment='DNB_MATH',exam_session=2025)).decode())"
```

Brevet examples:
- DNB 2025, 2027 and 2028 → `MATH_C4_2020`
- DNB 2029 → `MATH_C4_2026`
- 5e in 2026-27 → `MATH_C4_2026`, and physics-chemistry 5e in 2026-27 → `PHYS_C4_2020`

All links are proposals with approval=PENDING; release stays HOLD.

See:
- `docs/VALIDATION_RESULTS.md`
- `docs/MIGRATION_PLAN.md`
- `docs/REVIEW_WORKLIST.csv`
- `docs/codex/` (Codex's specification and prompt)
