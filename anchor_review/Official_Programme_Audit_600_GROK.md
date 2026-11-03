# Official programme audit – 600 targets (Grok Bot) – DRAFT

**Status: PROPOSALS ONLY.** Nothing here is validated. Every conformity value is a proposal for the teacher. No packaged file was modified; `Item_Review_Register_v11.csv` is untouched; no target is PASS; paper and digital release stay **HOLD**. Scope: curriculum alignment only.

## Method
- **Batch 1** (152 PROVISIONAL + 6 NOT_SUPPORTED rows, `map_batch1.py`): I picked each passage by hand, copied it verbatim from the PDF text, and the script checks it automatically against the source (`build_audit.py`).
- **Batch 2** (442 SOURCE_LINKED rows, `match_batch2.py`): each existing citation is checked independently against the official text. The ref's French paraphrase from `Math_Official_Referential_Index_v11.csv` is split into terms. Each term is searched in the official text of the applicable level (accent/case-insensitive, word prefixes), and the evidence is the **exact source line(s)** with their PDF page(s).
  - SUPPORTED = every term found (confidence *medium*: automated, teacher check needed).
  - PARTIALLY_SUPPORTED = some terms missing, or only found in a programme that does not apply to the exam year.
  - UNVERIFIED = nothing found by the matcher.
  - TS-AN-05 and TS-AN-38 (differential equations, formulas the matcher couldn't parse) were checked by hand.
  - Limitation: an automated term match does not prove that the item is pitched at the right depth. The `pedagogical_interpretation` column is kept separate from `official_evidence`.
- **Brevet**: the 3e uses the **2020** cycle 4 programme in 2026-27 and 2027-28 (DNB 2027 and 2028). The 2026 programme reaches 3e only in 2028-29. Each Brevet row is therefore checked against both, and the 2020 text decides conformity for the DNB.
- Page = PDF page of the cited file. All sources were consulted on 2026-11-03.
- `coverage_check.py` proves that exactly 600 unique IDs match `Math_Diagnostic_Targets_v11.csv`.

## Sources
- BO n°14, 2 Apr 2026, full PDF (Première spécialité and Première maths in the enseignement scientifique): https://www.education.gouv.fr/sites/default/files/document/Bulletin%20officiel%20n%C2%B0%2014%20du%202%20avril%202026-515432.pdf
- Cycle 4, 2020 programme (BO n°31, 30 Jul 2020, Éduscol version, maths on PDF pp. 127-139): https://eduscol.education.gouv.fr/sites/default/files/document/programme-d-enseignement-du-cycle-4-67722.pdf
- Cycle 4, 2026 programme (BO n°10, 5 Mar 2026, annexe 2): https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf
- Terminale spécialité 2019 (BO spécial n°8, 25 Jul 2019): https://eduscol.education.gouv.fr/sites/default/files/document/spe246annexe1158907pdf-84159.pdf
- Terminale mathématiques complémentaires 2019: https://eduscol.education.gouv.fr/sites/default/files/document/spe265annexe1159134pdf-84162.pdf
- Terminale mathématiques expertes 2019: https://eduscol.education.gouv.fr/sites/default/files/document/spe264annexe1158825pdf-84165.pdf
- MPSI/MP2I 2021: https://cache.media.education.gouv.fr/file/SPE1-MEN-MESRI-4-2-2021/64/8/spe779_annexe_1373648.pdf
- MP/MPI 2021: https://cache.media.education.gouv.fr/file/31/21/2/ensecsup756_annexes_1417212.pdf

**Not accessible:**
- education.gouv.fr/bo/… HTML pages and education.gouv.fr/media/11546, 11585 and 11588 (Cloudflare 403). The Éduscol mirrors above were used instead.
- The Éduscol 2020 3e summary sheet (R29, TLS error).
- The ac-bordeaux copies (503).
- The BO spécial n°11 of 26 Nov 2015 was not fetched separately. The 2020 Éduscol text is the consolidated version of that programme as amended.

## Summary
Total: {'SUPPORTED': 456, 'PARTIALLY_SUPPORTED': 44, 'NOT_SUPPORTED': 7, 'UNVERIFIED': 93}

| Level | n | SUPPORTED | PARTIALLY_SUPPORTED | NOT_SUPPORTED | UNVERIFIED |
|---|---|---|---|---|---|
| BAC_1RE_COMMUN | 40 | 26 | 8 | 6 | 0 |
| BAC_1RE_SPE | 79 | 73 | 5 | 1 | 0 |
| BAC_TLE_COMPLEMENTAIRES | 42 | 41 | 1 | 0 | 0 |
| BAC_TLE_EXPERTES | 36 | 32 | 4 | 0 | 0 |
| BAC_TLE_SPE | 85 | 83 | 2 | 0 | 0 |
| BREVET | 95 | 72 | 23 | 0 | 0 |
| MP2I | 130 | 129 | 1 | 0 | 0 |
| MPI | 93 | 0 | 0 | 0 | 93 |

UNVERIFIED rows: 93 – M2-ST-01, M2-ST-02, M2-ST-03, M2-ST-04, M2-ST-05, M2-ST-06, M2-ST-07, M2-ST-08, M2-RED-01, M2-RED-02, M2-RED-03, M2-RED-04, M2-RED-05, M2-RED-06, M2-RED-07, M2-RED-08, M2-RED-09, M2-RED-10, M2-RED-11, M2-EU-01, M2-EU-02, M2-EU-03, M2-EU-04, M2-EU-05, M2-EU-06, M2-EU-07, M2-EU-08, M2-EVN-01, M2-EVN-02, M2-EVN-03, M2-EVN-04, M2-EVN-05, M2-EVN-06, M2-EVN-07, M2-EVN-08, M2-EVN-09, M2-SE-01, M2-SE-02, M2-SE-03, M2-SE-04, M2-SE-05, M2-SE-06, M2-SE-07, M2-SF-01, M2-SF-02, M2-SF-03, M2-SF-04, M2-SF-05, M2-SF-06, M2-SF-07, M2-SF-08, M2-SEN-01, M2-SEN-02, M2-SEN-03, M2-SEN-04, M2-SEN-05, M2-SEN-06, M2-SEN-07, M2-SEN-08, M2-FV-01, M2-FV-02, M2-FV-03, M2-FV-04, M2-FV-05, M2-FV-06, M2-IN-01, M2-IN-02, M2-IN-03, M2-IN-04, M2-IN-05, M2-IN-06, M2-IN-07, M2-IN-08, M2-PR-01, M2-PR-02, M2-PR-03, M2-PR-04, M2-PR-05, M2-PR-06, M2-PR-07, M2-PR-08, M2-ED-01, M2-ED-02, M2-ED-03, M2-ED-04, M2-ED-05, M2-ED-06, M2-CD-01, M2-CD-02, M2-CD-03, M2-CD-04, M2-CD-05, M2-CD-06

## How the teacher confirms a row
1. Open `source_url` at `page` and read `verbatim_passage`.
2. If you agree, fill bo_match, bo_reviewer and bo_reviewed_on yourself in `Item_Review_Register_v11.csv`. The bot never fills those fields.
3. Optionally fill `reviewer` / `reviewed_on` here.

The rows to check first are in `Discrepancies_by_level_600_GROK.md`.
