"""Build v11 of the reference from the shipped v10 files (consolidated CODEX + Grok audit of v10).

    python -I build_v11.py           write the v11 files into this folder
    python -I build_v11.py --check   rebuild into a temporary folder and compare SHA-256 with the published files
Inputs: build/inputs_v10/ (the v10 reference, CSVs, register, legacy IDs). Data rows are unchanged from v9; v11 extends the review
register and documents the evidence rules (the corrections of v11 are in validate_reference_v11.py and check_values_v6.py).
"""
import csv
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
IN9 = os.path.join(HERE, 'build', 'inputs_v10')
COPY = {'Math_Diagnostic_Targets_v10.csv': 'Math_Diagnostic_Targets_v11.csv', 'Math_Official_Referential_Index_v10.csv': 'Math_Official_Referential_Index_v11.csv',
        'Math_ID_Migration_to_v10.csv': 'Math_ID_Migration_to_v11.csv', 'Anchor_Verification_Worklist_v10.csv': 'Anchor_Verification_Worklist_v11.csv',
        'Legacy_EC_Codes_CODEX_v5.csv': 'Legacy_EC_Codes_CODEX_v5.csv', 'legacy_ids_v10.json': 'legacy_ids_v11.json'}
MD9 = 'French_Math_Diagnostic_Curriculum_Reference_CLAUDE_EN_v10.md'
MD10 = 'French_Math_Diagnostic_Curriculum_Reference_CLAUDE_EN_v11.md'
REG = 'Item_Review_Register_v11.csv'
REG10 = 'Item_Review_Register_v10.csv'
OUTS = list(COPY.values()) + [MD10, REG]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def build(out):
    for a, b in COPY.items():
        shutil.copyfile(os.path.join(IN9, a), os.path.join(out, b))
    old = list(csv.DictReader(open(os.path.join(IN9, REG10), encoding='utf-8')))
    cols = ['target_id', 'anchor_status', 'official_ref', 'bo_match', 'bo_page', 'bo_passage', 'bo_reviewer', 'bo_reviewed_on',
            'teacher_item_review', 'teacher_reviewer', 'teacher_reviewed_on', 'text_signatures_reviewed', 'text_reviewer', 'text_reviewed_on',
            'text_review_note', 'pilot_status', 'pilot_evidence_id', 'pilot_reviewed_on', 'comment']
    with open(os.path.join(out, REG), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(cols)
        for r in old:
            w.writerow([r.get(c, '') for c in cols])
    s = open(os.path.join(IN9, MD9), encoding='utf-8').read()
    s = edit(s)
    open(os.path.join(out, MD10), 'w', encoding='utf-8', newline='\n').write(s)


OLD_STATEMENT = ('Zero blocking findings establishes only a structural pass. It does not validate programme coverage, student-error mechanisms or player integration. '
                 'The 158 provisional targets require official BO checks, and teacher review is mandatory before release labelled "validated".')
NEW_STATEMENT = ('Zero blocking findings establishes only a structural pass. Programme passages, mathematical coverage and teacher review remain required for any release '
                 'labelled "validated". Today 152 rows are `PROVISIONAL` and 6 `NOT_SUPPORTED` (158 not source-linked).')


def edit(s):
    def rep(a, b):
        nonlocal s
        assert a in s, 'missing: ' + a[:80]
        s = s.replace(a, b, 1)
    rep('Expanded Question-Generation Reference (v10.0)', 'Expanded Question-Generation Reference (v11.0)')
    rep('consolidated Claude + Codex + Grok audit of v9 applied on 3 November 2026 (v10).', 'consolidated Claude + Codex + Grok audit of v9 applied on 3 November 2026 (v10); consolidated CODEX + Grok audit of v10 applied on 3 November 2026 (v11).')
    rep('companion prompt `PROMPT_Diagnostic_Maths_Brevet_Bac_MPI_v8.md`.', 'audit of v10 (R40); companion prompt `PROMPT_Diagnostic_Maths_Brevet_Bac_MPI_v9.md`.')
    rep('Data rows are unchanged from v9.\n', 'Data rows are unchanged from v9.\n**What v11 changes (audit of v10):** every PASS needs complete, dated evidence (BO page and passage; teacher date; text-signature review; pilot evidence); paper and digital readiness are separate; exact integers are compared exactly; `Coverage_Gaps_v11.csv` lists every unchecked key and signature; the generated Markdown holds no runtime environment, so the rebuild is identical across Python patch releases; `tests_v11.py` runs the audit\'s regression scenarios (§1.2 items 44–50). Data rows are unchanged from v9.\n')
    rep('**Companion files (v10):**', '**Companion files (v11):** `Math_Diagnostic_Targets_v11.csv`, `Item_Review_Register_v11.csv`, `Item_Release_Eligibility_v11.csv`, `Coverage_Gaps_v11.csv`, `validate_reference_v11.py`, `tests_v11.py`, `build_v11.py`. *(v10:)*')
    i = s.index('43. **Seventh gate (v10; A08):**')
    j = s.index('\n', i)
    s = s[:j + 1] + ITEMS + s[j + 1:]
    rep('| R39 |', '| R40 | Consolidated CODEX + Grok audit of v10, 3 November 2026 — internal | work folder `XX-OUTILS_EVAL` |\n| R39 |')
    i = s.index('## 15. End-of-build QA summary')
    j = s.index('## 16. Changelog')
    s = s[:i] + qa() + '\n' + s[j:]
    rep('## 16. Changelog\n', '## 16. Changelog\n\n' + CHANGELOG + '\n')
    s = s.replace(OLD_STATEMENT, NEW_STATEMENT)
    return s


ITEMS = """44. **Curriculum evidence enforced (v11; CODEX + Grok P0-01):** a row passes the curriculum gate only with `bo_match` = `SUPPORTED`, a non-empty `bo_page` (or stable section) and `bo_passage`, a reviewer, and a `bo_reviewed_on` date written YYYY-MM-DD; the reason lists each missing field.
45. **Text signatures (v11; P0-02):** a row's text signatures are cleared only by `text_signatures_reviewed` = `YES` with `text_reviewer`, `text_reviewed_on` and `text_review_note`; this clears the text part only — an unchecked key or numeric signature still holds the row.
46. **Diagnostic validity (v11; P0-03):** positive evidence only: every active error must be `PILOT_SUPPORTED` or `RESEARCH_DOCUMENTED`, and the register must give `pilot_status` = `PILOTED`, `pilot_evidence_id` and `pilot_reviewed_on`. A blank or unknown status never passes.
47. **Paper and digital readiness (v11; P0-04):** `eligibility_paper` ignores the player; `eligibility_digital` needs `Player_Validation_Record_v11.json` (schema file and SHA-256, sample quiz, schema valid, player smoke test PASS, tester, date). `release_status` is given for paper and digital separately, with its scope (all 600 rows).
48. **Teacher review (v11; P0-05):** `APPROVED` needs a reviewer and a `teacher_reviewed_on` date.
49. **Rebuild across Python versions (v11; P0-06):** the v10 Markdown embedded the Python version of the run, so a rebuild on Python 3.13.5 differed from the published file (3.13.18). Runtime provenance now goes to `validation_report_v11.json` only; the generated Markdown is deterministic. Grok's validation on Python 3.10.21 / SymPy 1.14.0 and CODEX's on 3.13.5 are recorded as independent runs.
50. **Exact numbers and coverage (v11; P1-1 to P1-4):** in `check_values_v6.py`, integers and fractions are compared exactly (10¹⁸ and 10¹⁸ + 1 differ), approximate values with a relative tolerance of 10⁻⁹ and an absolute tolerance of 10⁻¹² (0 and 5 × 10⁻¹⁰ differ); unreachable code was removed. `Coverage_Gaps_v11.csv` lists each unchecked key, numeric signature, infinity and text signature, and the v6 checks of intermediate values. Counts are stated as 152 `PROVISIONAL` + 6 `NOT_SUPPORTED` (158 not source-linked). The 301 CODEX v5 IDs and their source are inside the package: what remains is their review, not the file.
"""

CHANGELOG = """### v10 → v11

| Change | Detail |
|---|---|
| Evidence | BO page and passage, dated teacher review, text-signature review, positive pilot evidence (items 44–46, 48) |
| Readiness | paper and digital computed separately; player record file (item 47) |
| Reproducibility | no runtime environment in the Markdown (item 49) |
| Numbers | exact integers and fractions; tolerances stated; dead code removed (item 50) |
| Coverage | `Coverage_Gaps_v11.csv` (item 50) |
| Tests | `tests_v11.py`: the audit's regression scenarios |
| Prompt | companion prompt v9 |
"""


def qa():
    p = os.path.join(HERE, 'qa_v11.json')
    qa = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    g = qa.get('gates', {})
    e = qa.get('item_eligibility', {})
    ep, ed = e.get('paper', {}), e.get('digital', {})
    rs = qa.get('release_status', {})
    return '\n'.join(['## 15. End-of-build QA summary', '',
                      '- **v11 validation (`validate_reference_v11.py`):** %s' % qa.get('summary', 'run the validator to fill this line.'),
                      '- **Item eligibility:** paper PASS %s, HOLD %s, FAIL %s; digital PASS %s, HOLD %s, FAIL %s.' % (
                          ep.get('PASS', '—'), ep.get('HOLD', '—'), ep.get('FAIL', '—'), ed.get('PASS', '—'), ed.get('HOLD', '—'), ed.get('FAIL', '—')),
                      '- **Release gates:** %s; `release_status`: paper %s, digital %s (scope: %s).' % (
                          ', '.join('`%s` %s' % kv for kv in g.items()) or '—', rs.get('paper', 'HOLD'), rs.get('digital', 'HOLD'), rs.get('scope', 'all rows')),
                      '- ' + NEW_STATEMENT, ''])


def main():
    if '--check' in sys.argv:
        tmp = tempfile.mkdtemp()
        try:
            build(tmp)
            bad = [n for n in OUTS if not os.path.exists(os.path.join(HERE, n)) or sha(os.path.join(tmp, n)) != sha(os.path.join(HERE, n))]
            print('rebuild check: %d files, %d differ %s' % (len(OUTS), len(bad), bad))
            return 1 if bad else 0
        finally:
            shutil.rmtree(tmp)
    build(HERE)
    print('v11 files written to', HERE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
