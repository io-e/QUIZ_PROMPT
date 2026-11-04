"""Validate the v11 reference package; write validation_report_v11.json (+ .txt), qa_v11.json and Item_Release_Eligibility_v11.csv.

Automatic gates (a failure is a blocking finding):
 (1) structure: every markdown row is re-rendered from Math_Diagnostic_Targets_v8.csv (cells 2-5 exactly; head cell:
     ID, difficulty, anchors, REASONED / OPEN_ONLY / provisional-anchor markers); same rows in the same order;
 (2) identifiers: grammar, uniqueness, reserved patterns unused, continuous E-numbering, statuses, merges;
 (3) error fields: mode, sig_mcq, sig_open and signature agree; origin;
 (4) transversal codes used are defined in §2A;
 (5) anchors: every ref is in the index; ref_verified is the weakest status; anchor_status is VERIFIED only if every anchor is OFFICIAL;
 (6) migration covers every v5/v6/v7 ID and every current ID; merged and retired IDs are recorded;
 (7) allowed_items: MCQ+OPEN only with three or more distinct MCQ-seed signatures;
 (8) masking and collisions on each seed (rule R1: a signature is compared with its own seed only);
 (9) numeric recomputation: chk_*.py (incl. chk_ADD.py) against the displayed values, check_values_v6.py for v6 rows.
Reported, not blocking: declared form-distinct errors, OPEN_ONLY rows, PROVISIONAL anchors, unparsed values.
Not checked (manual review): pedagogical plausibility, BO support of COPY/TOC anchors, empirical validity, player JSON schema.
v9: six release gates (STRUCTURE, CALCULATION, CURRICULUM, LEGACY_MIGRATION, PLAYER_SCHEMA, TEACHER_REVIEW), coverage of rows and
errors by the configured checks, symbolic signatures, the 301 CODEX v5 IDs, anchor statuses SOURCE_LINKED / PROVISIONAL / NOT_SUPPORTED.
v11: evidence fields enforced (BO page and passage, dated reviews, text-signature review, pilot evidence); paper and digital
readiness computed separately (digital needs Player_Validation_Record_v11.json); Coverage_Gaps_v11.csv; environment kept out of
the Markdown (runtime provenance only in the JSON report); eligibility rules in row_eligibility() (tested by tests_v11.py).
v10: the v6 checks run in-process and are linked to the current CSV; item-level release eligibility; seven gates (adds DIAGNOSTIC_VALIDITY);
the curriculum gate needs a recorded capability review (SOURCE_LINKED is not enough); the environment is recorded.
Usage (from the package folder): python3 -I validate_reference_v11.py     Windows: py -3 -I validate_reference_v11.py
Exit code: 0 = no blocking finding (structural pass, not a release); 1 = blocking findings; 2 = could not run.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import csv
import importlib.util
import json
import os
import re
import platform
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except (AttributeError, ValueError):
    pass
import ea_paths  # noqa: E402
SCRIPTS = str(ea_paths.bootstrap_sys_path())
HERE = str(ea_paths.data_root())  # referentiel root (CSV/MD/reports)
ea_paths.ensure_output_dirs()
try:
    import sympy  # noqa: F401
except ImportError:
    print('NOT RUN: sympy is required for this interpreter. Install it with: python -m pip install sympy '
          '(Windows: py -3 -m pip install sympy). With -I, packages installed with --user are not visible.')
    sys.exit(2)
import sympy as sp  # noqa: E402
from v7lib import cells, ROW_RE, pv, same, compare_value, value_part, is_quoted, norm_text  # noqa: E402
from v8lib import body_cells, head_markers, mode_of, join_sig, mcq_distinct  # noqa: E402

MD = 'French_Math_Diagnostic_Curriculum_Reference_CLAUDE_EN_v11.md'
TARGETS = 'Math_Diagnostic_Targets_v11.csv'
INDEX = 'Math_Official_Referential_Index_v11.csv'
MIGRATION = 'Math_ID_Migration_to_v11.csv'
LEGACY = 'legacy_ids_v11.json'
REGISTER = 'Item_Review_Register_v11.csv'
ELIG = 'Item_Release_Eligibility_v11.csv'
PLAYER = 'Player_Validation_Record_v11.json'
GAPS = 'Coverage_Gaps_v11.csv'
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
EVIDENCE_OK = ('PILOT_SUPPORTED', 'RESEARCH_DOCUMENTED')
LEVEL_PREFIX = ['BR', '1S', '1C', 'TS', 'TE', 'TC', 'M1', 'M2']
CHK = ['BR', '1S', '1C', 'TS', 'TE', 'TC', 'M1', 'M2', 'FIX', 'ADD']
ID_RE = re.compile(r'^(BR|1S|1C|TS|TE|TC|M1|M2)-[A-Z0-9]{2,3}-\d\d$')
SCOPE = {
    'automatic_gates': ['markdown rows re-rendered from the CSV', 'ID grammar, uniqueness, reserved patterns, E-numbering, statuses',
                        'mode / sig_mcq / sig_open consistency', 'transversal codes defined in §2A', 'anchor presence and status consistency',
                        'migration coverage (v5, v6, v7 and current IDs; merged and retired IDs)', 'MCQ allowed only with three distinct MCQ-seed signatures',
                        'masking and collisions on each seed (rule R1)', 'numeric recomputation of keys and signatures (chk_*.py, check_values_v6.py)'],
    'not_checked': ['pedagogical plausibility of each signature (teacher review)', 'that a BO paraphrase supports the capability (PROVISIONAL anchors need a BO check)',
                    'empirical diagnostic validity (no pilot data: signatures are hypotheses)', 'YAML compatibility with the player JSON schema (schema file not in this package)',
                    'wording and French student-facing text of generated items'],
    'release_rule': 'Zero blocking findings establishes only a structural pass. Programme passages, mathematical coverage and teacher review remain required for any release labelled "validated". Today 152 rows are PROVISIONAL and 6 NOT_SUPPORTED (158 not source-linked).',
}


def path(name):
    return os.path.join(HERE, name)


def load_targets():
    rows = []
    with open(path(TARGETS), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            r['errors'] = json.loads(r['errors_json'])
            r['D'] = int(r['difficulty'])
            rows.append(r)
    return rows


def equal_values(a, b, as_text=False):
    if norm_text(a) == norm_text(b):
        return True
    if as_text or is_quoted(a) or is_quoted(b):
        return False
    pa, pb = pv(a), pv(b)
    return pa[0] != 'text' and pb[0] != 'text' and same(pa, pb)


def displayed(r, fld):
    if fld == 'K':
        return r['mcq_key']
    if fld == 'A':
        return r['open_target']
    for e in r['errors']:
        if e['id'].endswith('-' + fld):
            sig = e['sig_mcq'] or e['sig_open']
            return sig if sig.startswith('"') else value_part(sig)
    return None


def load(p):
    spec = importlib.util.spec_from_file_location(os.path.basename(p)[:-3], p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def player_status():
    """PASS only with a record of a real schema validation and player smoke test; otherwise UNVERIFIED."""
    p = path(PLAYER)
    if not os.path.exists(p):
        return 'UNVERIFIED', 'no %s' % PLAYER
    try:
        rec = json.load(open(p, encoding='utf-8'))
    except ValueError as exc:
        return 'UNVERIFIED', 'unreadable record: %s' % exc
    need = ('schema_file', 'schema_sha256', 'sample_quiz', 'tested_by', 'tested_on')
    miss = [k for k in need if not rec.get(k)]
    if miss or rec.get('schema_valid') is not True or rec.get('player_smoke_test') != 'PASS' or not DATE_RE.match(str(rec.get('tested_on', ''))):
        return 'UNVERIFIED', 'incomplete record: missing %s' % (', '.join(miss) or 'a passing schema test or smoke test')
    return 'PASS', ''


def row_eligibility(r, g, structure_ok, calc, player):
    """Eligibility of one row. r: CSV row (with errors); g: its register line; calc: (key_checked, n_num_ok, n_num, n_txt); player: (status, why).
    Returns dict with the per-gate statuses, paper and digital eligibility and the reasons. Every PASS needs positive, complete evidence."""
    def dated(k):
        return bool(DATE_RE.match(g.get(k, '') or ''))
    reasons = []
    st = 'PASS' if structure_ok else 'FAIL'
    if not structure_ok:
        reasons.append('structure: listed in a blocking finding')
    key_ok, n_ok, n_num, n_txt = calc
    txt_ok = n_txt == 0 or (g.get('text_signatures_reviewed') == 'YES' and g.get('text_reviewer') and dated('text_reviewed_on') and g.get('text_review_note'))
    if key_ok and n_ok == n_num and txt_ok:
        cal = 'PASS'
    else:
        cal = 'PARTIAL'
        if not key_ok:
            reasons.append('calc: key not checked')
        if n_ok != n_num:
            reasons.append('calc: %d/%d numeric signatures checked' % (n_ok, n_num))
        if not txt_ok:
            reasons.append('calc: %d text signatures without a complete review (YES, reviewer, date, note)' % n_txt)
    if r['anchor_status'] == 'NOT_SUPPORTED' or r['eligibility'] == 'HOLD':
        cur = 'FAIL'
        reasons.append('curriculum: %s / eligibility %s' % (r['anchor_status'], r['eligibility']))
    elif g.get('bo_match') == 'SUPPORTED':
        miss = [k for k in ('bo_page', 'bo_passage', 'bo_reviewer') if not (g.get(k) or '').strip()] + ([] if dated('bo_reviewed_on') else ['bo_reviewed_on (YYYY-MM-DD)'])
        cur = 'PASS' if not miss else 'HOLD'
        if miss:
            reasons.append('curriculum: SUPPORTED but missing %s' % ', '.join(miss))
    else:
        cur = 'HOLD'
        reasons.append('curriculum: %s, capability not reviewed against the official passage' % r['anchor_status'])
    if g.get('teacher_item_review') == 'APPROVED' and (g.get('teacher_reviewer') or '').strip() and dated('teacher_reviewed_on'):
        teach = 'PASS'
    else:
        teach = 'HOLD'
        if g.get('teacher_item_review') == 'APPROVED':
            reasons.append('teacher review: APPROVED but missing %s' % ('reviewer' if not (g.get('teacher_reviewer') or '').strip() else 'teacher_reviewed_on (YYYY-MM-DD)'))
        else:
            reasons.append('teacher review: %s' % (g.get('teacher_item_review') or 'PENDING'))
    act = [e for e in r['errors'] if e['status'] == 'ACTIVE']
    if all(e.get('research_status') in EVIDENCE_OK for e in act) and g.get('pilot_status') == 'PILOTED' and (g.get('pilot_evidence_id') or '').strip() and dated('pilot_reviewed_on'):
        diag = 'PASS'
    else:
        diag = 'HOLD'
        reasons.append('diagnostic validity: needs every error PILOT_SUPPORTED or RESEARCH_DOCUMENTED, pilot_status PILOTED, evidence ID and date')
    parts = [st, cal, cur, teach, diag]
    paper = 'FAIL' if 'FAIL' in parts else ('PASS' if all(p == 'PASS' for p in parts) else 'HOLD')
    if paper == 'PASS' and player[0] != 'PASS':
        reasons.append('digital: player %s (%s)' % (player[0], player[1]))
    digital = paper if paper != 'PASS' else ('PASS' if player[0] == 'PASS' else 'HOLD')
    return dict(structure=st, calculation=cal, curriculum=cur, player_schema=player[0], teacher_review=teach, diagnostic_validity=diag,
                eligibility_paper=paper, eligibility_digital=digital, reasons='; '.join(reasons))


def main():
    for name in (MD, TARGETS, INDEX, MIGRATION, LEGACY):
        if not os.path.exists(path(name)):
            print('NOT RUN: missing file %s (run from the package folder)' % name)
            return 2
    rep = {'file': MD, 'scope': SCOPE, 'findings': {}, 'counts': {}}
    F = rep['findings']

    def add(k, v):
        F.setdefault(k, []).append(v)
    s = open(path(MD), encoding='utf-8').read()
    lines = s.split('\n')
    targets = load_targets()
    byid = {r['id']: r for r in targets}
    # (1) structure
    md_ids, md_lines = [], {}
    for i, line in enumerate(lines, 1):
        m = ROW_RE.match(line)
        if m:
            md_ids.append(m.group(1))
            md_lines[m.group(1)] = line
            if len(cells(line)) != 5:
                add('table_cells', [i, m.group(1), len(cells(line))])
    rep['counts']['md_rows'] = len(md_ids)
    rep['counts']['csv_rows'] = len(targets)
    if md_ids != [r['id'] for r in targets]:
        add('md_csv_order_or_set', 'markdown rows and CSV rows differ')
    for r in targets:
        line = md_lines.get(r['id'])
        if line is None:
            continue
        c = cells(line)
        if len(c) != 5:
            continue
        want = body_cells(r['capability'], r['note'], r['mcq_seed'], r['mcq_key'], r['open_seed'], r['open_target'], r['errors'])
        for k, name in enumerate(('capability', 'mcq', 'open', 'errors')):
            if c[k + 1] != want[k]:
                add('md_cell_differs_from_csv', [r['id'], name])
        head, refs_r = c[0], r['official_ref'].split(';')
        if not head.startswith('**`%s` · D%d**' % (r['id'], r['D'])):
            add('md_head_id_or_difficulty', r['id'])
        if 'ref `%s`' % refs_r[0] not in head or any('`%s`' % x not in head for x in refs_r):
            add('md_head_missing_ref', r['id'])
        if (r['format'] == 'REASONED') != ('`REASONED`' in head):
            add('md_head_reasoned_marker', r['id'])
        if not head.endswith(head_markers(r['anchor_status'], r['ref_verified'], r['allowed_items']) or head[-1:]):
            add('md_head_v8_markers', r['id'])
        if ('(provisional)' in head) != (r['anchor_status'] == 'PROVISIONAL') or ('`OPEN_ONLY`' in head) != (r['allowed_items'] == 'OPEN_ONLY') \
                or ('`NOT_SUPPORTED`' in head) != (r['anchor_status'] == 'NOT_SUPPORTED'):
            add('md_head_v8_markers', r['id'])
    # (2) identifiers and statuses
    if len(set(md_ids)) != len(md_ids):
        add('duplicate_ids', sorted({x for x in md_ids if md_ids.count(x) > 1}))
    all_eids = []
    for r in targets:
        if not ID_RE.match(r['id']):
            add('id_grammar', r['id'])
        if re.search(r'-[FS]\d\d$', r['id']):
            add('reserved_pattern_used', r['id'])
        nums = [int(e['id'].rsplit('-E', 1)[1]) for e in r['errors']]
        if nums != list(range(1, len(nums) + 1)) or any(not e['id'].startswith(r['id'] + '-E') for e in r['errors']):
            add('error_numbering', r['id'])
        act = [e for e in r['errors'] if e['status'] == 'ACTIVE']
        if len(act) < 3:
            add('fewer_than_3_errors', r['id'])
        for e in r['errors']:
            all_eids.append(e['id'])
            if e['status'] not in ('ACTIVE', 'RETIRED', 'MERGED'):
                add('bad_error_status', e['id'])
            if e['status'] == 'MERGED':
                into = [x for x in act if x['id'] == e.get('merged_into')]
                if not into:
                    add('merged_into_not_active_in_row', e['id'])
            elif e.get('merged_into'):
                add('merged_into_on_unmerged_error', e['id'])
            if len(e['tags']) > 2:
                add('more_than_2_tags', e['id'])
            # (3) error fields
            if e['mode'] != mode_of(e['sig_mcq'], e['sig_open']) or e['signature'] != join_sig(e['sig_mcq'], e['sig_open']):
                add('mode_or_signature_inconsistent', e['id'])
            if e['sig_mcq'].startswith('open:') or 'open:' in e['sig_open'][:6]:
                add('seed_prefix_left_in_signature', e['id'])
            if e.get('origin') not in ('v5', 'v6', 'v7', 'v8'):
                add('bad_origin', e['id'])
            if e.get('research_status') not in ('HYPOTHESIS', 'PILOT_SUPPORTED', 'RESEARCH_DOCUMENTED'):
                add('bad_research_status', e['id'])
            if e['status'] == 'ACTIVE' and e['ambiguous_with']:
                add('declared_ambiguous_pair_left', e['id'])
    if len(set(all_eids)) != len(all_eids):
        add('duplicate_error_ids', len(all_eids) - len(set(all_eids)))
    act_all = [e for r in targets for e in r['errors'] if e['status'] == 'ACTIVE']
    rep['counts']['active_error_ids'] = len(act_all)
    rep['counts']['active_by_mode'] = {m: sum(e['mode'] == m for e in act_all) for m in ('mcq', 'open', 'mcq+open')}
    rep['counts']['active_by_origin'] = {o: sum(e['origin'] == o for e in act_all) for o in ('v5', 'v6', 'v7', 'v8')}
    rep['counts']['retired_error_ids'] = sum(1 for r in targets for e in r['errors'] if e['status'] == 'RETIRED')
    rep['counts']['merged_error_ids'] = sum(1 for r in targets for e in r['errors'] if e['status'] == 'MERGED')
    rep['counts']['by_level'] = {lv: sum(r['id'].startswith(lv + '-') for r in targets) for lv in LEVEL_PREFIX}
    rep['counts']['by_status'] = {}
    for r in targets:
        rep['counts']['by_status'][r['status']] = rep['counts']['by_status'].get(r['status'], 0) + 1
    rep['counts']['reasoned_rows'] = sum(r['format'] == 'REASONED' for r in targets)
    rep['counts']['rows_changed_in_v8'] = sum(bool(r['v8_change']) for r in targets)
    # (4) codes
    defined = set(re.findall(r'^\| `((?:CB-[A-Z]+-\d\d|RP-\d\d))` \|', s.split('### 2A.4')[0], re.M))
    used = {tg for r in targets for e in r['errors'] for tg in e['tags']}
    used |= set(re.findall(r'`((?:CB-[A-Z]+-\d\d|RP-\d\d))`', s))
    for c in sorted(used - defined):
        add('undefined_code', c)
    rep['counts']['codes_defined'] = len(defined)
    # (5) anchors
    refs = {}
    with open(path(INDEX), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            refs[r['ref']] = r
    order = {'OFFICIAL': 0, 'COPY': 1, 'TOC': 2, 'NOT_SUPPORTED': 3}
    for r in targets:
        ids = r['official_ref'].split(';')
        if any(x not in refs for x in ids):
            add('unknown_ref', [r['id'], r['official_ref']])
            continue
        weakest = max((refs[x]['verified'] for x in ids), key=lambda v: order.get(v, 3))
        if weakest != r['ref_verified']:
            add('ref_verified_mismatch', r['id'])
        want = 'NOT_SUPPORTED' if weakest == 'NOT_SUPPORTED' else ('SOURCE_LINKED' if weakest == 'OFFICIAL' else 'PROVISIONAL')
        if r['anchor_status'] != want:
            add('anchor_status_gate', r['id'])
        if want == 'NOT_SUPPORTED' and r['eligibility'] != 'HOLD':
            add('not_supported_row_not_on_hold', r['id'])
        for x in ids:
            if r['id'] not in refs[x]['targets'].split():
                add('ref_index_missing_target', [x, r['id']])
    for x, rr in refs.items():
        if rr['verified'] not in order:
            add('ref_bad_verified_status', [x, rr['verified']])
    rep['counts']['ref_entries'] = len(refs)
    rep['counts']['ref_entries_by_status'] = {v: sum(rr['verified'] == v for rr in refs.values()) for v in order}
    rep['counts']['rows_by_anchor_status'] = {a: sum(r['anchor_status'] == a for r in targets) for a in ('SOURCE_LINKED', 'PROVISIONAL', 'NOT_SUPPORTED')}
    rep['counts']['rows_by_weakest_anchor'] = {v: sum(r['ref_verified'] == v for r in targets) for v in order}
    # (6) migration
    mig = list(csv.DictReader(open(path(MIGRATION), encoding='utf-8')))
    legacy = {}
    for m in mig:
        if m['legacy_id']:
            legacy.setdefault(m['legacy_id'], []).append(m)
    current = {m['current_id'] for m in mig if m['current_id']}
    old = json.load(open(path(LEGACY), encoding='utf-8'))
    old_ids = set(old['v6']) | set(old['v7']) | set(old.get('v8', []))
    for x in sorted(old_ids):
        if x not in legacy and x not in current:
            add('migration_missing_legacy', x)
    for r in targets:
        if r['id'] not in current:
            add('migration_missing_current', r['id'])
        for e in r['errors']:
            if e['status'] == 'ACTIVE' and e['id'] not in current:
                add('migration_missing_current', e['id'])
            if e['status'] == 'RETIRED' and not any(m['relation'] == 'RETIRED' for m in legacy.get(e['id'], [])):
                add('retired_not_in_migration', e['id'])
            if e['status'] == 'MERGED' and not any(m['relation'] == 'MERGED' and m['current_id'] == e['merged_into'] for m in legacy.get(e['id'], [])):
                add('merged_not_in_migration', e['id'])
            if e['origin'] == 'v8' and not any(m['relation'] == 'NEW_V8' and m['current_id'] == e['id'] for m in mig):
                add('new_v8_not_in_migration', e['id'])
    codex = {m['legacy_id']: m for m in mig if m['legacy_version'] == 'CODEX_v5_301'}
    for x in old.get('codex_v5_301', []):
        if x not in codex:
            add('codex_v5_301_id_not_enumerated', x)
        elif codex[x]['relation'] not in ('EXACT', 'PARTIAL', 'SPLIT', 'MERGE', 'NOT_EQUIVALENT', 'UNMAPPED'):
            add('codex_v5_301_bad_relation', x)
        elif codex[x]['current_id'] and codex[x]['current_id'] not in byid:
            add('codex_v5_301_unknown_current_id', x)
    if len(old.get('codex_v5_301', [])) != 301:
        add('codex_v5_301_inventory_size', len(old.get('codex_v5_301', [])))
    leg_review = {k: sum(1 for x in old.get('codex_v5_301', []) if codex.get(x, {}).get('review_status') == k) for k in ('PROPOSED_UNREVIEWED', 'REVIEWED')}
    rep['counts']['codex_v5_301'] = {'enumerated': sum(1 for x in old.get('codex_v5_301', []) if x in codex), 'review_status': leg_review,
                                     'relations': {k: sum(1 for x in codex.values() if x['relation'] == k and x['legacy_id'] in set(old['codex_v5_301'])) for k in ('EXACT', 'PARTIAL', 'UNMAPPED')}}
    for need in ('BR-NC-F\\d\\d', 'SUBDOMAIN-S\\d\\d', 'SUBDOMAIN-F\\d\\d'):
        if need not in legacy or legacy[need][0]['relation'] != 'RESERVED':
            add('reserved_pattern_missing', need)
    rep['counts']['migration_rows'] = len(mig)
    rep['counts']['migration_relations'] = {}
    for m in mig:
        rep['counts']['migration_relations'][m['relation']] = rep['counts']['migration_relations'].get(m['relation'], 0) + 1
    rep['counts']['legacy_ids_checked'] = len(old_ids)
    # (7) allowed items
    for r in targets:
        n = mcq_distinct(r['errors'])
        if r['allowed_items'] not in ('MCQ+OPEN', 'OPEN_ONLY'):
            add('allowed_items_value', r['id'])
        elif r['allowed_items'] == 'MCQ+OPEN' and n < 3:
            add('mcq_allowed_with_fewer_than_3_signatures', [r['id'], n])
        elif r['allowed_items'] == 'OPEN_ONLY' and not r['allowed_items_reason']:
            add('open_only_without_reason', r['id'])
    rep['counts']['allowed_items'] = {a: sum(r['allowed_items'] == a for r in targets) for a in ('MCQ+OPEN', 'OPEN_ONLY')}
    # (8) scan on each seed (rule R1)
    scan = {'masking_mcq': [], 'masking_open': [], 'collision_mcq': [], 'collision_open': [], 'declared_form_distinct': [], 'open_only_rows': []}
    for r in targets:
        as_text = r['compare'] == 'text'
        act = [e for e in r['errors'] if e['status'] == 'ACTIVE']
        groups = {'mcq': [(e, value_part(e['sig_mcq'])) for e in act if e['sig_mcq']],
                  'open': [(e, value_part(e['sig_open'])) for e in act if e['sig_open']]}
        refv = {'mcq': value_part(r['mcq_key']), 'open': value_part(r['open_target'])}
        for g, vals in groups.items():
            for e, v in vals:
                if v and refv[g] and equal_values(v, refv[g], as_text):
                    if g == 'mcq' and e.get('form_distinct'):
                        scan['declared_form_distinct'].append([r['id'], e['id'], e['form_distinct']])
                    else:
                        scan['masking_' + g].append([r['id'], e['id']])
            for i in range(len(vals)):
                for j in range(i + 1, len(vals)):
                    (a, va), (b, vb) = vals[i], vals[j]
                    if va and vb and equal_values(va, vb, as_text):
                        scan['collision_' + g].append([r['id'], a['id'], b['id']])
        if r['allowed_items'] == 'OPEN_ONLY':
            scan['open_only_rows'].append([r['id'], r['allowed_items_reason']])
    rep['scan'] = scan
    # (9) numeric recomputation
    num = {'checked': 0, 'passed': 0, 'failed': [], 'unparsed': [], 'extra_ok': 0, 'extra_failed': [], 'rows_with_checks': 0}
    for lv in CHK:
        mod = load(os.path.join(SCRIPTS, 'chk_%s.py' % lv))
        for rid, fields in mod.CHECKS.items():
            r = byid.get(rid)
            if r is None:
                num['failed'].append([rid, '*', 'row not found'])
                continue
            num['rows_with_checks'] += 1
            for fld, val in fields.items():
                disp = displayed(r, fld)
                if disp is None:
                    num['failed'].append([rid, fld, 'field not found'])
                    continue
                num['checked'] += 1
                res, got, exp = compare_value(disp, val)
                if res == 'pass':
                    num['passed'] += 1
                elif res == 'fail':
                    num['failed'].append([rid, fld, disp, str(exp[1])])
                else:
                    num['unparsed'].append([rid, fld, disp])
        if hasattr(mod, 'extra'):
            for rid, ok, note in mod.extra():
                if ok:
                    num['extra_ok'] += 1
                else:
                    num['extra_failed'].append([rid, note])
    # v6 checks, in-process, linked to the current CSV (v10)
    import contextlib
    import io
    from fractions import Fraction
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        v6 = load(os.path.join(SCRIPTS, 'check_values_v6.py'))
    num['v6_checks_run'] = v6.run[0]
    num['v6_checks_failed'] = len(v6.fails)
    num['v6_failures'] = [[str(x) for x in f] for f in v6.fails]
    fmap = {'key': 'K', 'open': 'A'}
    linked, link_mismatch, unlinkable = set(), [], 0
    for row, what, got, want, ok in v6.records:
        fld = fmap.get(what, what if re.fullmatch(r'E\d', what) else None)
        if not ok or fld is None or row not in byid:
            unlinkable += 1
            continue
        if isinstance(want, Fraction):
            want = sp.Rational(want.numerator, want.denominator)
        if isinstance(want, bool) or not isinstance(want, (int, float, sp.Basic)) or isinstance(want, sp.MatrixBase):
            unlinkable += 1
            continue
        disp = displayed(byid[row], fld)
        if disp is None:
            unlinkable += 1
            continue
        res = compare_value(disp, want)[0]
        if res == 'pass':
            linked.add((row, fld))
        else:
            link_mismatch.append([row, fld, disp, str(want)])
    num['v6_label'] = 'v6 checks: recomputed in-process; a check counts as coverage only when its written value equals the value shown in the current CSV'
    num['v6_linked_to_csv'] = len(linked)
    num['v6_link_mismatch_for_review'] = link_mismatch
    num['v6_unlinkable'] = unlinkable
    # coverage (v9, extended in v10 with the linked v6 checks)
    checked = {(rid, f) for lv in CHK for rid, fields in load(os.path.join(SCRIPTS, 'chk_%s.py' % lv)).CHECKS.items() for f in fields} | linked
    cov = {'rows_total': len(targets), 'rows_with_key_check': len({rid for rid, f in checked if f == 'K'}),
           'rows_with_any_check': len({rid for rid, f in checked}), 'errors_active': len(act_all), 'errors_with_signature_check': 0,
           'numeric_signatures_total': 0, 'numeric_signatures_checked': 0, 'text_signatures_for_review': 0, 'symbolic_infinity': []}
    row_calc = {}
    for r in targets:
        n_num = n_ok = n_txt = 0
        for e in r['errors']:
            if e['status'] != 'ACTIVE':
                continue
            suf = e['id'].rsplit('-', 1)[1]
            ok = (r['id'], suf) in checked
            cov['errors_with_signature_check'] += ok
            for sig in (e['sig_mcq'], e['sig_open']):
                if not sig:
                    continue
                v = value_part(sig)
                if '∞' in v:
                    cov['symbolic_infinity'].append([e['id'], v, 'CHECKED' if ok else 'NOT_CHECKED'])
                if is_quoted(v) or pv(v)[0] == 'text':
                    n_txt += 1
                else:
                    n_num += 1
                    n_ok += ok
        cov['text_signatures_for_review'] += n_txt
        cov['numeric_signatures_total'] += n_num
        cov['numeric_signatures_checked'] += n_ok
        row_calc[r['id']] = (( r['id'], 'K') in checked, n_ok, n_num, n_txt)
    cov['form_distinct_review'] = len(scan['declared_form_distinct'])
    rep['coverage'] = cov
    rep['numeric'] = num
    # summary
    blocking = sum(len(v) for v in F.values()) + len(scan['masking_mcq']) + len(scan['masking_open']) + len(scan['collision_mcq']) \
        + len(scan['collision_open']) + len(num['failed']) + len(num['extra_failed']) + (num['v6_checks_failed'] or 0)
    rep['blocking_findings'] = blocking
    rep['non_blocking'] = {'declared_form_distinct': len(scan['declared_form_distinct']), 'open_only_rows': len(scan['open_only_rows']),
                           'provisional_anchor_rows': rep['counts']['rows_by_anchor_status']['PROVISIONAL'], 'unparsed_values': len(num['unparsed'])}
    rep['status'] = 'STRUCTURAL_PASS (not a release: see scope)' if blocking == 0 else 'BLOCKING_FINDINGS'
    ac = rep['counts']['rows_by_anchor_status']
    # item-level release eligibility (v10)
    reg = {r['target_id']: r for r in csv.DictReader(open(path(REGISTER), encoding='utf-8'))}
    flagged = set()
    for v in list(F.values()) + [scan['masking_mcq'], scan['masking_open'], scan['collision_mcq'], scan['collision_open'], num['failed'], num['extra_failed']]:
        for item in v:
            for rid in byid:
                if rid in str(item):
                    flagged.add(rid)
    player = player_status()
    elig_rows, gap_rows = [], []
    for r in targets:
        d = row_eligibility(r, reg.get(r['id'], {}), r['id'] not in flagged, row_calc[r['id']], player)
        elig_rows.append([r['id'], d['structure'], d['calculation'], d['curriculum'], d['player_schema'], d['teacher_review'], d['diagnostic_validity'],
                          d['eligibility_paper'], d['eligibility_digital'], d['reasons']])
    for r in targets:
        if (r['id'], 'K') not in checked:
            gap_rows.append([r['id'], 'K', 'mcq', r['mcq_key'], 'KEY_NOT_CHECKED'])
        for e in r['errors']:
            if e['status'] != 'ACTIVE':
                continue
            suf = e['id'].rsplit('-', 1)[1]
            for seed, sig in (('mcq', e['sig_mcq']), ('open', e['sig_open'])):
                if not sig:
                    continue
                v = value_part(sig)
                if is_quoted(v) or pv(v)[0] == 'text':
                    gap_rows.append([e['id'], suf, seed, v, 'TEXT_REVIEW'])
                elif (r['id'], suf) not in checked:
                    gap_rows.append([e['id'], suf, seed, v, 'INFINITY_NOT_CHECKED' if '∞' in v else 'NUMERIC_NOT_CHECKED'])
    for row, fld, disp, want in num['v6_link_mismatch_for_review']:
        gap_rows.append([row, fld, '', disp, 'V6_CHECKS_AN_INTERMEDIATE_VALUE (checked: %s)' % want])
    with open(path(GAPS), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['id', 'field', 'seed', 'value', 'gap'])
        w.writerows(gap_rows)
    rep['coverage']['gaps'] = {k: sum(1 for x in gap_rows if x[4].startswith(k)) for k in ('KEY_NOT_CHECKED', 'NUMERIC_NOT_CHECKED', 'INFINITY_NOT_CHECKED', 'TEXT_REVIEW', 'V6_CHECKS')}
    with open(path(ELIG), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['target_id', 'structure', 'calculation', 'curriculum', 'player_schema', 'teacher_review', 'diagnostic_validity',
                    'eligibility_paper', 'eligibility_digital', 'reasons'])
        w.writerows(elig_rows)
    ec = {k: sum(x[7] == k for x in elig_rows) for k in ('PASS', 'HOLD', 'FAIL')}
    ecd = {k: sum(x[8] == k for x in elig_rows) for k in ('PASS', 'HOLD', 'FAIL')}
    rep['item_eligibility'] = {'paper': ec, 'digital': ecd}
    in_scope = [x for x in elig_rows if x[3] != 'FAIL']
    gates = {'STRUCTURE_PASS': 'PASS' if blocking == 0 else 'FAIL',
             'CALCULATION_PASS': 'PASS' if all(x[2] == 'PASS' for x in in_scope) else 'PARTIAL',
             'CURRICULUM_PASS': 'PASS' if all(x[3] == 'PASS' for x in in_scope) else 'HOLD',
             'LEGACY_MIGRATION_PASS': 'PASS' if leg_review['REVIEWED'] == 301 else 'HOLD',
             'PLAYER_SCHEMA_PASS': player[0],
             'TEACHER_REVIEW_PASS': 'PASS' if all(x[5] == 'PASS' for x in in_scope) else 'HOLD',
             'DIAGNOSTIC_VALIDITY_PASS': 'PASS' if all(x[6] == 'PASS' for x in in_scope) else 'HOLD'}
    rep['gates'] = gates
    paper_gates = {k: v for k, v in gates.items() if k != 'PLAYER_SCHEMA_PASS'}
    rep['release_status'] = {'scope': 'all %d rows' % len(targets),
                             'paper': 'RELEASE_READY' if all(v == 'PASS' for v in paper_gates.values()) else 'HOLD',
                             'digital': 'RELEASE_READY' if all(v == 'PASS' for v in gates.values()) else 'HOLD'}
    rep['environment'] = {'python': platform.python_version(), 'implementation': platform.python_implementation(), 'sympy': sp.__version__,
                          'platform': platform.platform(), 'command': ' '.join([os.path.basename(sys.executable)] + sys.argv)}
    am = rep['counts']['active_by_mode']
    summary0 = ('%d rows (%s); %d active error IDs (MCQ seed %d, open seed %d, both %d; %d added in v8), %d retired, %d merged; '
               'structure, IDs, fields, codes, anchors, migration and allowed items: %d findings; scan on each seed: %d masking, %d collisions, '
               '%d declared form-distinct; MCQ+OPEN %d rows, OPEN_ONLY %d; anchors VERIFIED %d, PROVISIONAL %d; numeric: %d/%d values, %d/%d extra checks, '
               'v6 checks %s/%s; blocking findings: %d.') % (
        len(targets), ', '.join('%s %d' % kv for kv in rep['counts']['by_level'].items()), len(act_all), am['mcq'], am['open'], am['mcq+open'],
        rep['counts']['active_by_origin']['v8'], rep['counts']['retired_error_ids'], rep['counts']['merged_error_ids'],
        sum(len(v) for v in F.values()), len(scan['masking_mcq']) + len(scan['masking_open']), len(scan['collision_mcq']) + len(scan['collision_open']),
        len(scan['declared_form_distinct']), rep['counts']['allowed_items']['MCQ+OPEN'], rep['counts']['allowed_items']['OPEN_ONLY'],
        rep['counts']['rows_by_anchor_status']['SOURCE_LINKED'], rep['counts']['rows_by_anchor_status']['PROVISIONAL'],
        num['passed'], num['checked'], num['extra_ok'], num['extra_ok'] + len(num['extra_failed']),
        (num['v6_checks_run'] or 0) - (num['v6_checks_failed'] or 0), num['v6_checks_run'], blocking)
    summary = summary0.replace('anchors VERIFIED', 'anchors SOURCE_LINKED') + (
        ' Coverage: %d/%d rows with a key check, %d/%d active errors with a signature check, %d/%d numeric signatures checked, %d text signatures for review, '
        '%d symbolic infinities (%d checked); v6 checks linked to the CSV %d; NOT_SUPPORTED rows %d; CODEX v5 301 IDs enumerated %d (reviewed %d); items (paper) PASS %d, HOLD %d, FAIL %d. Gates: %s. release_status: paper %s, digital %s (scope: all rows).') % (
        cov['rows_with_key_check'], cov['rows_total'], cov['errors_with_signature_check'], cov['errors_active'], cov['numeric_signatures_checked'],
        cov['numeric_signatures_total'], cov['text_signatures_for_review'], len(cov['symbolic_infinity']), sum(x[2] == 'CHECKED' for x in cov['symbolic_infinity']),
        num['v6_linked_to_csv'], ac['NOT_SUPPORTED'], rep['counts']['codex_v5_301']['enumerated'], leg_review['REVIEWED'], ec['PASS'], ec['HOLD'], ec['FAIL'],
        ', '.join('%s %s' % kv for kv in gates.items()), rep['release_status']['paper'], rep['release_status']['digital'])
    rep['summary'] = summary
    json.dump(rep, open(path('validation_report_v11.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(path('validation_report_v11.txt'), 'w', encoding='utf-8') as f:
        f.write(summary + '\n' + rep['status'] + '\n')
        f.write('Scope: ' + SCOPE['release_rule'] + '\nNot checked: ' + '; '.join(SCOPE['not_checked']) + '\n')
        for k, v in F.items():
            f.write('%s (%d): %s\n' % (k, len(v), v[:20]))
        for k, v in scan.items():
            if v:
                f.write('scan %s (%d): %s\n' % (k, len(v), v[:30]))
        f.write('environment: %s\n' % rep['environment'])
        if num['v6_link_mismatch_for_review']:
            f.write('v6 link mismatches for review (%d): %s\n' % (len(num['v6_link_mismatch_for_review']), num['v6_link_mismatch_for_review'][:30]))
        for k in ('failed', 'unparsed', 'extra_failed'):
            if num[k]:
                f.write('numeric %s (%d): %s\n' % (k, len(num[k]), num[k][:30]))
    json.dump({'summary': summary, 'status': rep['status'], 'item_eligibility': rep['item_eligibility'], 'gates': gates, 'release_status': rep['release_status'], 'active_error_ids': len(act_all), 'values': '%d/%d' % (num['passed'], num['checked']),
               'extra': '%d/%d' % (num['extra_ok'], num['extra_ok'] + len(num['extra_failed'])),
               'v6_checks': '%s/%s' % ((num['v6_checks_run'] or 0) - (num['v6_checks_failed'] or 0), num['v6_checks_run'])},
              open(path('qa_v11.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(summary)
    print(rep['status'], '| release_status:', rep['release_status'], '| environment:', rep['environment']['python'], 'SymPy', rep['environment']['sympy'])
    return 0 if blocking == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
