# Math Diagnostic Reference — CLAUDE v11 (package README)

**Date:** 3 November 2026 · **Author:** Claude
**Basis:** CLAUDE v10 and the consolidated CODEX + Grok audit of v10.
**Release status:** **HOLD**, on paper and in digital form (scope: all 600 rows).

> Zero blocking findings establishes only a structural pass. Programme passages, mathematical coverage and teacher review remain required for any release labelled "validated". Today 152 rows are `PROVISIONAL` and 6 are `NOT_SUPPORTED` (158 not source-linked).

## 1. Gates (last run)

| Gate | Status | Detail |
|---|---|---|
| `STRUCTURE_PASS` | **PASS** | 0 blocking findings |
| `CALCULATION_PASS` | **PARTIAL** | Gaps listed in `Coverage_Gaps_v11.csv`:<br>• 249 keys and 458 numeric signatures unchecked;<br>• 5 infinities unchecked;<br>• 901 text signatures to review;<br>• 58 v6 checks of intermediate values. |
| `CURRICULUM_PASS` | **HOLD** | No review with BO page and passage recorded yet |
| `LEGACY_MIGRATION_PASS` | **HOLD** | 0 of 301 reviewed. The CODEX v5 source is already in `build/inputs_legacy/`. |
| `PLAYER_SCHEMA_PASS` | **UNVERIFIED** | No `Player_Validation_Record_v11.json` |
| `TEACHER_REVIEW_PASS` | **HOLD** | No dated approval |
| `DIAGNOSTIC_VALIDITY_PASS` | **HOLD** | No pilot evidence |

**Items:** paper 0 `PASS`, 594 `HOLD`, 6 `FAIL`; digital the same.

## 2. What v11 changes

| Audit item | Action |
|---|---|
| P0-01 — Curriculum evidence | `SUPPORTED` passes only with `bo_page`, `bo_passage`, a reviewer and a `YYYY-MM-DD` date. The reason names each missing field. |
| P0-02 — Text signatures | Cleared only with `YES`, a reviewer, a date and a note. This clears the text part only. |
| P0-03 — Diagnostic validity | Positive allowlist (`PILOT_SUPPORTED` / `RESEARCH_DOCUMENTED`), plus `pilot_status = PILOTED`, an evidence ID and a date. |
| P0-04 — Paper vs digital | Computed separately. Digital needs `Player_Validation_Record_v11.json` with: schema file and SHA-256, sample quiz, `schema_valid: true`, smoke test `PASS`, tester, date. |
| P0-05 — Teacher review | `APPROVED` needs a reviewer and a date. |
| P0-06 — Cross-version rebuild | Cause: the v10 Markdown embedded "Python 3.13.18". The environment now goes to the JSON report only, and the generated Markdown is deterministic. |
| P1-2 / P1-3 — Exact numbers | `10**18 ≠ 10**18 + 1` and `0 ≠ 5e-10`. A one-ulp difference between floats is still equal. Dead code removed. |
| P1-1 — Coverage | `Coverage_Gaps_v11.csv` (1 671 lines) |
| P1-4 / P1-8 — Wording | "152 provisional + 6 unsupported". Earlier prompt versions are labelled historical. |
| §4 — Regression tests | `tests_v11.py`: 21 scenarios, all pass |

## 3. Commands

```text
py -3 -I validate_reference_v11.py    # about 30 s; writes eligibility, gaps, report
py -3 -I tests_v11.py                 # regression scenarios
py -3 -I build_v11.py --check         # rebuild from build/inputs_v10 and compare hashes
```

## 4. Making a row PASS

Fill its line in `Item_Review_Register_v11.csv`, with every date written `YYYY-MM-DD`:

1. **Curriculum:** `bo_match = SUPPORTED`, with `bo_page`, `bo_passage`, `bo_reviewer` and `bo_reviewed_on`.
2. **Teacher review:** `teacher_item_review = APPROVED`, with `teacher_reviewer` and `teacher_reviewed_on`.
3. **Text signatures:** `text_signatures_reviewed = YES`, with `text_reviewer`, `text_reviewed_on` and `text_review_note`.
4. **Pilot:** `pilot_status = PILOTED`, with `pilot_evidence_id` and `pilot_reviewed_on`. The row's errors must also be `PILOT_SUPPORTED` in the targets CSV.
5. **Calculation:** add the missing checks to `chk_*.py`.

Then re-run the validator.
