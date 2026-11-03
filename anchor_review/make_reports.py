import csv,collections
r=list(csv.DictReader(open('Official_Programme_Audit_600_GROK.csv')))
S=['SUPPORTED','PARTIALLY_SUPPORTED','NOT_SUPPORTED','UNVERIFIED']
c=collections.Counter(x['conformity'] for x in r); L=collections.Counter((x['level'],x['conformity']) for x in r)
levels=sorted({x['level'] for x in r})
tab="| Level | n | "+" | ".join(S)+" |\n|---|---|"+"---|"*4+"\n"+"".join(f"| {l} | {sum(1 for x in r if x['level']==l)} | "+" | ".join(str(L[(l,s)]) for s in S)+" |\n" for l in levels)
unv=[x for x in r if x['conformity']=='UNVERIFIED']
open('Official_Programme_Audit_600_GROK.md','w').write(f"""# Official programme audit – 600 targets (Grok Bot) – DRAFT

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
Total: {dict(c)}

{tab}
UNVERIFIED rows: {len(unv)}{(' – '+', '.join(x['target_id'] for x in unv)) if unv else ''}

## How the teacher confirms a row
1. Open `source_url` at `page` and read `verbatim_passage`.
2. If you agree, fill bo_match, bo_reviewer and bo_reviewed_on yourself in `Item_Review_Register_v11.csv`. The bot never fills those fields.
3. Optionally fill `reviewer` / `reviewed_on` here.

The rows to check first are in `Discrepancies_by_level_600_GROK.md`.
""")
o="# Discrepancies by level (proposals, not validated)\n\nCheck these rows first: NOT_SUPPORTED, then PARTIALLY_SUPPORTED, then UNVERIFIED.\n"
for l in levels:
  rows=[x for x in r if x['level']==l and x['conformity']!='SUPPORTED']
  o+=f"\n## {l} ({len(rows)} rows)\n"
  for x in sorted(rows,key=lambda x:S.index(x['conformity'])*-1):
    o+=f"- **{x['target_id']}** ({x['current_official_ref']}) – {x['conformity']} – {x['capability']}. {x['discrepancy_and_proposed_correction']} [{x['page']}]\n"
open('Discrepancies_by_level_600_GROK.md','w').write(o)
print(tab, 'UNVERIFIED', len(unv))
