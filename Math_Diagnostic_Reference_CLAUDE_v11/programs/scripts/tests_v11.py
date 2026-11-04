"""Regression tests for the v11 release logic (consolidated CODEX + Grok audit of v10, §4).

Usage (from the package folder): python3 -I tests_v11.py     Windows: py -3 -I tests_v11.py
Exit 0 when every scenario gives the expected result.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import contextlib
import io
import math
import os
import sys

import ea_paths  # noqa: E402
ea_paths.bootstrap_sys_path()
HERE = str(ea_paths.data_root())
import sympy as sp  # noqa: E402
import validate_reference_v11 as V  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    import check_values_v6 as C  # noqa: E402

ROW = {'id': 'T-01', 'anchor_status': 'SOURCE_LINKED', 'eligibility': 'IN-PROG',
       'errors': [{'id': 'T-01-E1', 'status': 'ACTIVE', 'research_status': 'PILOT_SUPPORTED'}]}
FULL = {'bo_match': 'SUPPORTED', 'bo_page': 'p. 5', 'bo_passage': 'Capacités attendues …', 'bo_reviewer': 'ALF', 'bo_reviewed_on': '2026-11-03',
        'teacher_item_review': 'APPROVED', 'teacher_reviewer': 'ALF', 'teacher_reviewed_on': '2026-11-03',
        'text_signatures_reviewed': 'YES', 'text_reviewer': 'ALF', 'text_reviewed_on': '2026-11-03', 'text_review_note': 'E1 wording checked',
        'pilot_status': 'PILOTED', 'pilot_evidence_id': 'PILOT-2026-01', 'pilot_reviewed_on': '2026-11-03'}
CALC_OK = (True, 2, 2, 1)
NO_PLAYER = ('UNVERIFIED', 'no record')
PLAYER_OK = ('PASS', '')


def elig(row=ROW, g=None, calc=CALC_OK, player=NO_PLAYER, structure_ok=True):
    return V.row_eligibility(row, dict(FULL, **(g or {})), structure_ok, calc, player)


CASES = [
    ('SUPPORTED with blank page and passage -> curriculum HOLD', lambda: elig(g={'bo_page': '', 'bo_passage': ''})['curriculum'] == 'HOLD'),
    ('SUPPORTED with all evidence -> curriculum PASS', lambda: elig()['curriculum'] == 'PASS'),
    ('SOURCE_LINKED without review -> curriculum HOLD', lambda: elig(g={'bo_match': 'PENDING'})['curriculum'] == 'HOLD'),
    ('teacher APPROVED, reviewer, no date -> teacher HOLD', lambda: elig(g={'teacher_reviewed_on': ''})['teacher_review'] == 'HOLD'),
    ('teacher APPROVED with a malformed date -> teacher HOLD', lambda: elig(g={'teacher_reviewed_on': '3/11/26'})['teacher_review'] == 'HOLD'),
    ('text YES with reviewer, date, note -> text cleared, calculation PASS', lambda: elig()['calculation'] == 'PASS'),
    ('text YES without reviewer -> calculation PARTIAL', lambda: elig(g={'text_reviewer': ''})['calculation'] == 'PARTIAL'),
    ('text cleared but a numeric signature unchecked -> calculation PARTIAL', lambda: elig(calc=(True, 1, 2, 1))['calculation'] == 'PARTIAL'),
    ('NOT_PILOTED with an arbitrary research_status -> diagnostic HOLD',
     lambda: elig(row=dict(ROW, errors=[{'id': 'T-01-E1', 'status': 'ACTIVE', 'research_status': 'WHATEVER'}]), g={'pilot_status': 'NOT_PILOTED'})['diagnostic_validity'] == 'HOLD'),
    ('blank research_status -> diagnostic HOLD', lambda: elig(row=dict(ROW, errors=[{'id': 'T-01-E1', 'status': 'ACTIVE', 'research_status': ''}]))['diagnostic_validity'] == 'HOLD'),
    ('all paper checks pass, no player record -> paper PASS, digital HOLD', lambda: (lambda d: d['eligibility_paper'] == 'PASS' and d['eligibility_digital'] == 'HOLD')(elig())),
    ('schema and player smoke test pass -> digital PASS', lambda: elig(player=PLAYER_OK)['eligibility_digital'] == 'PASS'),
    ('NOT_SUPPORTED row -> FAIL on paper and digital', lambda: (lambda d: d['eligibility_paper'] == d['eligibility_digital'] == 'FAIL')(elig(row=dict(ROW, anchor_status='NOT_SUPPORTED', eligibility='HOLD')))),
    ('row in a blocking finding -> FAIL', lambda: elig(structure_ok=False)['eligibility_paper'] == 'FAIL'),
    ('exact integers 10**18 and 10**18 + 1 -> distinct', lambda: not C.same(10 ** 18, 10 ** 18 + 1)),
    ('0 and 5e-10 -> distinct', lambda: not C.same(0, 5e-10)),
    ('one-ulp difference of an approximate value -> equal', lambda: C.same(sp.Float(2 * math.log(2)), sp.Float(math.nextafter(2 * math.log(2), 3)))),
    ('exact symbolic log 4 = 2 log 2 -> equal; log 4 vs log 5 -> distinct', lambda: C.same(sp.log(4), 2 * sp.log(2)) and not C.same(sp.log(4), sp.log(5))),
    ('fractions 1/3 and 2/6 -> equal', lambda: C.same(C.F(1, 3), C.F(2, 6))),
    ('no player record -> player UNVERIFIED', lambda: V.player_status()[0] == 'UNVERIFIED' if not os.path.exists(V.path(V.PLAYER)) else True),
    ('generated Markdown holds no runtime environment (deterministic across Python patch releases)',
     lambda: 'Environment: Python' not in open(V.path(V.MD), encoding='utf-8').read()),
]


def main():
    bad = 0
    for name, test in CASES:
        try:
            ok = bool(test())
        except Exception as exc:  # a crash is a failure
            ok, name = False, '%s [%s]' % (name, exc)
        bad += not ok
        print('%s  %s' % ('PASS' if ok else 'FAIL', name))
    print('scenarios: %d, failed: %d' % (len(CASES), bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
