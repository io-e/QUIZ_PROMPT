"""Shared helpers for the v7 build and validator: patch parsing, value parsing, comparison."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, convert_xor)

X, Y, Z, N, T, A, B, K, P, Q, R, U, V, H, LAM = sp.symbols('x y z n t a b k p q r u v h lambda')
LOC = {'x': X, 'y': Y, 'z': Z, 'n': N, 't': T, 'a': A, 'b': B, 'k': K, 'p': P, 'q': Q, 'r': R,
       'u': U, 'v': V, 'h': H, 'lam': LAM, 'pi': sp.pi, 'E': sp.E, 'I': sp.I, 'i': sp.I,
       'sqrt': sp.sqrt, 'exp': sp.exp, 'ln': sp.log, 'log': sp.log, 'sin': sp.sin, 'cos': sp.cos,
       'tan': sp.tan, 'arctan': sp.atan, 'Arctan': sp.atan, 'oo': sp.oo, 'e': sp.E,
       'ch': sp.cosh, 'sh': sp.sinh, 'arcsin': sp.asin, 'arccos': sp.acos}
TRANS = standard_transformations + (implicit_multiplication_application, convert_xor)
SUP = str.maketrans({'⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7',
                     '⁸': '8', '⁹': '9', '⁻': '-', 'ⁿ': 'n', 'ˣ': 'x', '⁺': '+'})
UNITS = r'(?:cm²|cm³|m²|m³|km/h|m/s|L/min|L/h|kWh|kW|cm|mm|km|m|L|€|g|kg|min|s|h|°|%|points?|pupils?|days?|years?|units?)'


def parse_row_header(line):
    m = re.match(r'@(\S+)\s+D(\d)\s*(.*)$', line)
    rid, d, rest = m.group(1), int(m.group(2)), m.group(3)
    meta = {}
    for part in rest.split('|'):
        part = part.strip()
        if '=' in part:
            k, v = part.split('=', 1)
            meta[k.strip()] = v.strip()
    return rid, d, meta


def parse_patch(path):
    rows, cur = [], None
    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        if not line.strip() or line.startswith('#'):
            continue
        if line.startswith('@'):
            rid, d, meta = parse_row_header(line)
            cur = {'id': rid, 'D': d, 'meta': meta, 'errors': [], 'notes': []}
            rows.append(cur)
            continue
        tag, _, body = line.partition(':')
        body = body.strip()
        if tag == 'T':
            cur['target'] = body
        elif tag == 'N':
            cur['notes'].append(body)
        elif tag in ('M', 'O'):
            q, _, ans = body.partition('##')
            ans = ans.strip()
            ans = re.sub(r'^[KA]:\s*', '', ans)
            cur['mcq' if tag == 'M' else 'open'] = q.strip()
            cur['key' if tag == 'M' else 'answer'] = ans
        elif re.fullmatch(r'E\d', tag):
            main, _, tags = body.partition('##')
            label, arrow, sig = main.partition('→')
            if not arrow:
                raise ValueError('missing → in %s %s' % (cur['id'], tag))
            cur['errors'].append({'id': '%s-%s' % (cur['id'], tag), 'label': label.strip(),
                                  'sig': sig.strip(),
                                  'tags': [t.strip() for t in tags.split(';') if t.strip()]})
        else:
            raise ValueError('unknown line in %s: %r' % (cur['id'] if cur else '?', line))
    return rows


def strip_comment(s):
    s = s.strip()
    m = re.search(r'\s+\(((?:[^()]|\([^()]*\))*)\)\s*$', s)
    if m and re.search(r'[A-Za-zéè]{3,}\s+[A-Za-zéè]{2,}', m.group(1)):
        s = s[:m.start()].strip()
    return s


def to_py(s):
    s = s.translate(str.maketrans('', '', '₀₁₂₃₄₅₆₇₈₉ₙ'))  # uₙ, u₃ ... parsed as u
    s = s.replace('−', '-').replace('×', '*').replace('·', '*').replace('÷', '/').replace('π', 'pi')
    s = re.sub(r'√\(', ' sqrt(', s)  # leading space: '2π√2' must not become the name 'pisqrt'
    s = re.sub(r'√(\d+(?:\.\d+)?|[a-z])', r' sqrt(\1)', s)
    s = re.sub(r'e\^\(', 'exp(', s)
    s = re.sub(r'e\^([\-a-z0-9.]+)', r'exp(\1)', s)
    s = re.sub(r'([0-9a-zA-Z)])([⁰¹²³⁴⁵⁶⁷⁸⁹⁻ⁿˣ⁺]+)', lambda m: m.group(1) + '**(' + m.group(2).translate(SUP) + ')', s)
    s = s.replace('^', '**')
    return s


def pv(s):
    """Parse a displayed value. Returns ('num', expr) | ('set', frozenset) | ('tuple', tuple) | ('text', norm)."""
    s0 = strip_comment(s)
    if len(s0.strip()) >= 2 and s0.strip()[0] == '"' and s0.strip()[-1] == '"':
        return ('text', norm_text(s0.strip()[1:-1]))  # a quoted signature is always compared as text
    s1 = s0.strip().strip('"').strip()
    if '⃗' in s1:
        return ('text', norm_text(s1))
    s1 = re.sub(r'(?<=\d)[ \u202f\u00a0](?=\d{3}\b)', '', s1)
    s1 = re.sub(r'\s*\+\s*o\((?:[^()]|\([^()]*\))*\)\s*$', '', s1)  # a trailing + o(...) term is dropped
    if s1.startswith('open:'):
        s1 = s1[5:].strip()
    s1 = re.sub(r'^[a-zA-Z]\s*=\s*(?=[^=]*$)', '', s1) if re.match(r'^[a-zA-Z]\s*=\s*[-−\d(]', s1) else s1
    hm = re.fullmatch(r'(\d+)\s*h\s*(\d+)\s*min', s1)
    if hm:
        return ('num', sp.Integer(int(hm.group(1)) * 60 + int(hm.group(2))))
    unit_tail = r'(?:\s+' + UNITS + r'|(?<=\d)(?:%|°|€|cm²|cm³|m²|m³))\s*$'  # a unit needs a space, except symbols glued to a number
    t = re.sub(unit_tail, '', s1)
    t = re.sub(unit_tail, '', t)
    if re.fullmatch(r'-?\d+(?:\.\d+)?(?:\s+-?\d+(?:\.\d+)?)+', t.replace('−', '-')):
        return ('text', ' '.join(t.replace('−', '-').split()))  # program output such as "8 7 4"
    if t.startswith('{') and t.endswith('}'):
        parts = [p for p in re.split(r'\s*;\s*', t[1:-1]) if p.strip()]
        vals = []
        for p in parts:
            k, v = pv(p)
            if k != 'num':
                return ('text', norm_text(s1))
            vals.append(sp.nsimplify(v) if v.is_number else sp.simplify(v))
        return ('set', frozenset(vals))
    if re.fullmatch(r'\(.*;.*\)', t):
        parts = re.split(r'\s*;\s*', t[1:-1])
        vals = []
        for p in parts:
            k, v = pv(p)
            if k != 'num':
                return ('text', norm_text(s1))
            vals.append(v)
        return ('tuple', tuple(vals))
    bare = re.sub(r'arctan|arcsin|arccos|sqrt|exp|sinh|cosh|sin|cos|tan|ln|log|pi', '', t)  # known function names
    if re.search(r'[<>≤≥⇔⇒]|\bor\b|\band\b|[A-Za-z]{3,}', bare):
        return ('text', norm_text(s1))
    try:
        e = parse_expr(to_py(t), local_dict=LOC, transformations=TRANS, evaluate=True)
        if isinstance(e, sp.Basic):
            return ('num', e)
    except Exception:
        pass
    return ('text', norm_text(s1))


def is_quoted(s):
    s0 = strip_comment(s).strip()
    return len(s0) >= 2 and s0[0] == '"' and s0[-1] == '"'


def norm_text(s):
    s = s.replace('−', '-').replace('’', "'").lower()
    return re.sub(r'\s+', '', s)


def same(a, b):
    """Compare two parsed values."""
    ka, va = a
    kb, vb = b
    if ka != kb:
        return False
    if ka == 'text':
        return va == vb
    if ka == 'set':
        return len(va) == len(vb) and all(any(sp.simplify(x - y) == 0 for y in vb) for x in va)
    if ka == 'tuple':
        return len(va) == len(vb) and all(sp.simplify(x - y) == 0 for x, y in zip(va, vb))
    try:
        d = sp.simplify(sp.expand(va - vb))
        if d == 0:
            return True
        if d.is_number:
            return abs(complex(sp.N(d))) < 1e-9
        d2 = sp.simplify(sp.nsimplify(va) - sp.nsimplify(vb))
        if d2 == 0:
            return True
        return numeric_equal(va, vb)
    except Exception:
        return False


def numeric_equal(a, b, points=((0.37, 1.31), (1.73, 0.59), (2.9, 4.1))):
    """Fallback for symbolic expressions: equal at three generic points (positive values, so roots and logs exist)."""
    syms = sorted((a - b).free_symbols, key=lambda s: s.name)
    if not syms:
        return False
    for pt in points:
        sub = {s: pt[i % len(pt)] + 0.11 * i for i, s in enumerate(syms)}
        try:
            va, vb = complex(sp.N(a.subs(sub))), complex(sp.N(b.subs(sub)))
        except Exception:
            return False
        if abs(va - vb) > 1e-9 * max(1.0, abs(va), abs(vb)):
            return False
    return True


def expected(v):
    """Turn a check value (python/sympy) into a parsed value."""
    if isinstance(v, (set, frozenset)):
        return ('set', frozenset(sp.nsimplify(x) if not isinstance(x, sp.Basic) else x for x in v))
    if isinstance(v, tuple):
        return ('tuple', tuple(sp.nsimplify(x) if not isinstance(x, sp.Basic) else x for x in v))
    if isinstance(v, str):
        got = pv(v)
        return got if got[0] != 'text' else ('text', norm_text(v))
    return ('num', sp.nsimplify(v) if isinstance(v, float) else sp.sympify(v))


# ---------------------------------------------------------------- v7 reference rows (markdown)
MINUTES = {1: 4, 2: 8, 3: 12}
LEVEL_CODES = {'BR': 'BREVET', '1S': 'BAC_1RE_SPE', '1C': 'BAC_1RE_COMMUN', 'TS': 'BAC_TLE_SPE',
               'TE': 'BAC_TLE_EXPERTES', 'TC': 'BAC_TLE_COMPLEMENTAIRES', 'M1': 'MP2I', 'M2': 'MPI'}
ROW_RE = re.compile(r'^\| \*\*`([A-Z0-9]+-[A-Z0-9]+-\d\d)` · D(\d)\*\*')


def esc(s):
    """Escape a cell for a markdown table (| becomes \\|)."""
    return (s or '').replace('\\|', '|').replace('|', '\\|')


def cells(line):
    """Split a markdown table row into its cells (escaped pipes kept inside cells)."""
    parts = re.split(r'(?<!\\)\|', line.strip())
    return [p.strip() for p in parts[1:-1]]


def render_error(e):
    mark = '*(v6)* ' if e.get('v6new') else ''
    tags = ''
    if e.get('tags'):
        tags = ' (' + ', '.join('`%s`' % t for t in e['tags']) + ')'
    amb = ''
    if e.get('ambiguous_with'):
        amb = ' **[ambiguous with %s: log both as `UNDETERMINED`]**' % ', '.join('`%s`' % a for a in e['ambiguous_with'])
    return '`%s` %s%s → %s%s%s' % (e['id'], mark, e['label'], e['sig'], tags, amb)


def render_md_row(t):
    """Markdown table row of a v7-rendered target (new rows and rows revised in v7)."""
    head = '**`%s` · D%d**' % (t['id'], t['D'])
    if t['status'] == 'NEW_V7':
        head += ' *(v7)*'
    head += ' (MCQ/Open %d / %d min)' % (t['D'], MINUTES[t['D']])
    if t['level'] == 'BR' and t.get('edition'):
        head += ' · `%s`' % t['edition']
    if t.get('fmt') == 'REASONED':
        head += ' · `REASONED`'
    if t.get('elig') in ('BRIDGE', 'PREREQUISITE', 'HOLD'):
        head += ' · `%s`' % t['elig']
    head += ' · ref `%s`' % t['ref'].replace(';', '`, `')
    cap = t['capability'] + (' *(%s)*' % t['note'] if t.get('note') else '')
    mcq = '%s **[key seed: %s]**' % (t['mcq'], t['key'])
    opn = '%s **[target: %s]**' % (t['open'], t['answer'])
    errs = '; '.join(render_error(e) for e in t['errors'] if not e.get('retired'))
    return '| ' + ' | '.join(esc(c) for c in (head, cap, mcq, opn, errs)) + ' |'


def compare_value(disp, val):
    """Compare a displayed value with an independently computed one: ('pass'|'fail'|'unparsed', got, expected)."""
    got = pv(disp)
    exp = expected(val)
    if isinstance(val, str) and is_quoted(disp):
        exp = ('text', norm_text(val))
    if got[0] == 'text' and exp[0] != 'text':
        for alt in (disp.split('=')[-1], re.split(r'[,;(]', disp)[0]):
            g2 = pv(alt)
            if g2[0] != 'text':
                got = g2
                break
    if got[0] == 'text' and exp[0] != 'text':
        return 'unparsed', got, exp
    return ('pass' if same(got, exp) else 'fail'), got, exp


def value_part(sig):
    """Value written before an explanatory ' (...)' or a '; open: ...' part (v6 convention)."""
    s = sig.strip()
    if s.startswith('open:'):
        s = s[5:].strip()
    s = s.split('; open:')[0]
    if not s.startswith('"'):
        m = re.match(r'^(.*?\S) \((?:[^()]|\([^()]*\))*\)\s*$', s)
        if m and not re.fullmatch(r'\(.*;.*\)', s):
            s = m.group(1)
    return s.strip()
