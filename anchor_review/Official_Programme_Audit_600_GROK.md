# Official programme audit – 600 targets (Grok Bot) – DRAFT, batch 1

**Status: PROPOSALS ONLY.** Nothing here is validated. Every conformity value is a proposal for the teacher. No packaged file was modified; `Item_Review_Register_v11.csv` is untouched; no target is PASS; paper and digital release stay **HOLD**. Scope: curriculum alignment only.

## Method
1. Official PDFs downloaded on 2026-11-03 and converted with `pdftotext -layout`.
2. For each audited row, a passage was chosen by hand and copied from the extracted text. `build_audit.py` checks automatically that each fragment (split on `[...]`) is present in the extracted text. Any row that fails the check becomes UNVERIFIED.
3. Page = PDF page of the cited file. For BO n°14, the PDF page equals the printed BO page.
4. Separate columns: `official_evidence` (quote) / `pedagogical_interpretation` (my reading).
5. Track/edition contradictions (CONTRADICTS) are recorded as NOT_SUPPORTED, with "CONTRADICTS" in the discrepancy column.
6. Rows not yet checked against a fetched official text are **UNVERIFIED**. A link alone is not treated as evidence.
7. `coverage_check.py` proves that exactly 600 unique IDs match `Math_Diagnostic_Targets_v11.csv` (output: `coverage_report.txt`).

## Sources consulted (2026-11-03)
- BO n°14 du 2 avril 2026 (full PDF, 438 p.): https://www.education.gouv.fr/sites/default/files/document/Bulletin%20officiel%20n%C2%B0%2014%20du%202%20avril%202026-515432.pdf, with MENE2602916A pp. 346–353 (Première, maths in the enseignement scientifique) and MENE2602917A pp. 354–365 (Première spécialité).
- MPSI/MP2I programme, annexe 1 (2021): https://cache.media.education.gouv.fr/file/SPE1-MEN-MESRI-4-2-2021/64/8/spe779_annexe_1373648.pdf
- **Not accessible:** education.gouv.fr/bo/... HTML pages (Cloudflare 403), education.gouv.fr/media/11546/download (Terminale spécialité, 403), and the ac-bordeaux copies (503).

## Summary
Total: {'UNVERIFIED': 442, 'PARTIALLY_SUPPORTED': 14, 'SUPPORTED': 137, 'NOT_SUPPORTED': 7}

| Level | SUPPORTED | PARTIALLY_SUPPORTED | NOT_SUPPORTED | UNVERIFIED |
|---|---|---|---|---|
| BAC_1RE_COMMUN | 26 | 8 | 6 | 0 |
| BAC_1RE_SPE | 73 | 5 | 1 | 0 |
| BAC_TLE_COMPLEMENTAIRES | 0 | 0 | 0 | 42 |
| BAC_TLE_EXPERTES | 0 | 0 | 0 | 36 |
| BAC_TLE_SPE | 0 | 1 | 0 | 84 |
| BREVET | 0 | 0 | 0 | 95 |
| MP2I | 38 | 0 | 0 | 92 |
| MPI | 0 | 0 | 0 | 93 |

## Batch status
- Batch 1 (done): the 152 PROVISIONAL rows and the 6 NOT_SUPPORTED rows (= the 158 rows of the v11 worklist).
- Batch 2 (to do): the **442 SOURCE_LINKED rows**, all still UNVERIFIED. By level: BREVET 95, MPI 93, MP2I 92, BAC_TLE_SPE 84, BAC_TLE_COMPLEMENTAIRES 42, BAC_TLE_EXPERTES 36. They need the cycle 4 programme (R15/R29), the Terminale spécialité/complémentaires/expertes programmes, MPI 2nd year and the rest of the MP2I programme.

## How the teacher confirms a row
1. Open `source_url` at `page` and compare it with `verbatim_passage`.
2. If you agree, write the conformity in your own words in `Item_Review_Register_v11.csv` (bo_match, bo_reviewer, bo_reviewed_on, page/passage). The bot never fills those fields.
3. Fill `reviewer` / `reviewed_on` in this CSV if you want a trace.

See `Discrepancies_by_level_600_GROK.md` for the rows to look at first.
