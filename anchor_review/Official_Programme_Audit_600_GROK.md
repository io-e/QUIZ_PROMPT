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
Total: {'SUPPORTED': 539, 'PARTIALLY_SUPPORTED': 54, 'NOT_SUPPORTED': 7}

| Level | n | SUPPORTED | PARTIALLY_SUPPORTED | NOT_SUPPORTED | UNVERIFIED |
|---|---|---|---|---|---|
| BAC_1RE_COMMUN | 40 | 26 | 8 | 6 | 0 |
| BAC_1RE_SPE | 79 | 73 | 5 | 1 | 0 |
| BAC_TLE_COMPLEMENTAIRES | 42 | 41 | 1 | 0 | 0 |
| BAC_TLE_EXPERTES | 36 | 32 | 4 | 0 | 0 |
| BAC_TLE_SPE | 85 | 83 | 2 | 0 | 0 |
| BREVET | 95 | 70 | 25 | 0 | 0 |
| MP2I | 130 | 129 | 1 | 0 | 0 |
| MPI | 93 | 85 | 8 | 0 | 0 |

UNVERIFIED rows: 0

## Brevet: both curriculum editions (decision of the teacher, 2026-11-03)
Every BREVET row carries per-edition columns: `conformity_2020` / `source_url_2020` / `page_2020` / `passage_2020` (cycle 4 2020 programme, DNB 2027 and 2028) and `conformity_2026` / `source_url_2026` / `page_2026` / `passage_2026` (2026 programme, reaches 3e in 2028-29, DNB from 2029), plus `edition_flag`:
- BOTH: SUPPORTED in both editions.
- 2020_ONLY: SUPPORTED in 2020 only (outgoing notion).
- 2026_ONLY: SUPPORTED in 2026 only (new notion).
- NEITHER: fully SUPPORTED in neither edition.

Non-Brevet rows have `N/A` in these columns.

**How these relate to the overall `conformity` column.** The overall column measures conformity with the edition that applies to the next exams (DNB 2027-2028), which is the 2020 programme:
- overall = `conformity_2020` when that value is SUPPORTED or PARTIALLY_SUPPORTED;
- if 2020 gives nothing but 2026 does, overall = PARTIALLY_SUPPORTED;
- if a notion is absent from 2020 and present in 2026 (2026_ONLY), overall is never higher than PARTIALLY_SUPPORTED.

To read the status for DNB 2029 and later, use `conformity_2026`.

| edition_flag | rows |
|---|---|
| BOTH | 59 |
| 2020_ONLY | 11 |
| 2026_ONLY | 16 |
| NEITHER | 9 |

- 2026_ONLY: BR-NC-04 (BR.NC.8), BR-NC-05 (BR.NC.9;BR.NC.10), BR-NC-24 (BR.NC.8), BR-NC-28 (BR.NC.10), BR-DF-10 (BR.DF.3), BR-DF-11 (BR.DF.3), BR-DF-22 (BR.DF.12), BR-EG-05 (BR.EG.1), BR-EG-21 (BR.EG.7), BR-EG-22 (BR.EG.1), BR-EG-23 (BR.EG.1), BR-EG-25 (BR.EG.2;BR.EG.1), BR-EG-14 (BR.EG.9), BR-EG-16 (BR.EG.7), BR-AP-06 (BR.AP.2), BR-AP-07 (BR.AP.2)
- 2020_ONLY: BR-DF-04 (BR.DF.9), BR-GM-01 (BR.GM.1), BR-GM-02 (BR.GM.1), BR-GM-03 (BR.GM.3), BR-GM-05 (BR.GM.1), BR-GM-06 (BR.GM.1), BR-GM-10 (BR.GM.3), BR-EG-04 (BR.EG.5), BR-EG-20 (BR.EG.6), BR-EG-11 (BR.EG.5), BR-EG-13 (BR.EG.5)
- NEITHER: BR-DF-02 (BR.DF.4), BR-DF-12 (BR.DF.4), BR-DF-13 (BR.DF.4), BR-DF-14 (BR.DF.5), BR-DF-21 (BR.DF.9;BR.DF.12), BR-GM-04 (BR.GM.2), BR-GM-08 (BR.GM.2), BR-GM-09 (BR.GM.2), BR-GM-11 (BR.GM.2)

**BR.DF.12 (square function, graphical solving), checked by hand.** The index flag NEW is **confirmed**. The 2020 hit that batch 2 reported was a matcher false positive: the word prefix "carre" matched "carreaux" on p.128. The 2020 maths pages 127-139 contain no passage on the square function. The 2026 text has "Représenter la fonction carré." (p.20) and "Résoudre analytiquement et graphiquement des équations de la forme 𝑥2 = a." (p.11).

**Known limitation.** Matching on word prefixes can produce false positives like this one, so every automated SUPPORTED stays at confidence *medium* until the teacher confirms it.

## How the teacher confirms a row
1. Open `source_url` at `page` and read `verbatim_passage`.
2. If you agree, fill bo_match, bo_reviewer and bo_reviewed_on yourself in `Item_Review_Register_v11.csv`. The bot never fills those fields.
3. Optionally fill `reviewer` / `reviewed_on` here.

The rows to check first are in `Discrepancies_by_level_600_GROK.md`.
