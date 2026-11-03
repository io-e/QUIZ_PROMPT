"""v8 row model shared by build_v8.py and validate_reference_v8.py: signatures per seed and the markdown rendering of a row.

An error carries one signature per seed: sig_mcq (wrong answer on the MCQ seed) and sig_open (wrong answer or trace on the
open seed). mode = mcq | open | mcq+open. The v7 single string `signature` is kept: "<mcq>", "open: <open>" or "<mcq>; open: <open>".
Rule R1: a signature is compared only with its own seed.
"""
from v7lib import esc, value_part, norm_text


def split_sig(s):
    s = s.strip()
    if s.startswith('open:'):
        return '', s[5:].strip()
    if '; open:' in s:
        a, b = s.split('; open:', 1)
        return a.strip(), b.strip()
    return s, ''


def join_sig(m, o):
    if m and o:
        return '%s; open: %s' % (m, o)
    return 'open: ' + o if o else m


def mode_of(m, o):
    return 'mcq+open' if (m and o) else ('open' if o else 'mcq')


def active(errors):
    return [e for e in errors if e['status'] == 'ACTIVE']


def mcq_distinct(errors):
    """Number of distinct MCQ-seed signatures among the active errors (REASONED rows: distinct wrong reasons)."""
    return len({norm_text(value_part(e['sig_mcq'])) for e in active(errors) if e['sig_mcq']})


def render_error(e, seed):
    sig = e['sig_mcq'] if seed == 'mcq' else e['sig_open']
    if seed == 'open' and e['sig_mcq']:
        return '`%s` (same rule) → %s' % (e['id'], sig)
    mark = {'v6': '*(v6)* ', 'v8': '*(v8)* '}.get(e['origin'], '')
    tags = ' (' + ', '.join('`%s`' % t for t in e['tags']) + ')' if e['tags'] else ''
    form = ' **[same value as the key in another form: the stem asks for that form]**' if (seed == 'mcq' and e['form_distinct']) else ''
    return '`%s` %s%s → %s%s%s' % (e['id'], mark, e['label'], sig, tags, form)


def render_errors(errors):
    groups = []
    m = [render_error(e, 'mcq') for e in active(errors) if e['sig_mcq']]
    o = [render_error(e, 'open') for e in active(errors) if e['sig_open']]
    if m:
        groups.append('**MCQ seed:** ' + '; '.join(m))
    if o:
        groups.append('**Open seed:** ' + '; '.join(o))
    return ' <br>'.join(groups)


def head_markers(anchor_status, ref_verified, allowed_items):
    out = ''
    if anchor_status == 'PROVISIONAL':
        out += ' · anchor `%s` (provisional)' % ref_verified
    elif anchor_status == 'NOT_SUPPORTED':
        out += ' · anchor `NOT_SUPPORTED` (excluded, `HOLD`)'
    if allowed_items == 'OPEN_ONLY':
        out += ' · `OPEN_ONLY`'
    return out


def body_cells(capability, note, mcq, key, open_seed, target, errors):
    """Cells 2–5 of a row, escaped, from the data."""
    cap = capability + (' *(%s)*' % note if note else '')
    return [esc(cap), esc('%s **[key seed: %s]**' % (mcq, key)), esc('%s **[target: %s]**' % (open_seed, target)), esc(render_errors(errors))]


def render_line(head, capability, note, mcq, key, open_seed, target, errors):
    return '| ' + ' | '.join([head] + body_cells(capability, note, mcq, key, open_seed, target, errors)) + ' |'
