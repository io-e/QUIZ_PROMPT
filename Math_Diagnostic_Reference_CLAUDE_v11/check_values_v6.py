"""Recompute keys and wrong-answer signatures of the v6 rows (numeric ones); shipped with v7 (TS-AN-04 checks follow its v7 seed).

Each check: (row, what, computed value, value written in the reference).
Also checks that every signature differs from its key (no masking) and that
the MCQ signatures of a row are pairwise distinct.
"""
from fractions import Fraction as F
from math import comb, perm, sqrt, e, log, atan, degrees, cos, pi, isclose, exp, factorial
import sympy as sp

x, t, n, h, X = sp.symbols('x t n h X')
fails = []
run = [0]
APPROX_ATOL = 1e-12  # v11: absolute tolerance for approximate values near 0
records = []  # v10: (row, what, computed, written, ok) so that the validator can link each check to the current CSV


def _is_approx(v):
    return isinstance(v, float) or (isinstance(v, sp.Basic) and v.is_number and v.atoms(sp.Float) != set())


def same(a, b, tol=1e-9):
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k], tol) for k in a)
    if isinstance(a, (set, frozenset)) or isinstance(b, (set, frozenset)):
        a, b = sorted(map(sp.sympify, a), key=sp.default_sort_key), sorted(map(sp.sympify, b), key=sp.default_sort_key)
    if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(same(u, v, tol) for u, v in zip(a, b))
    if isinstance(a, sp.MatrixBase) or isinstance(b, sp.MatrixBase):
        return sp.simplify(sp.Matrix(a) - sp.Matrix(b)) == sp.zeros(*sp.Matrix(a).shape)
    if _is_approx(a) or _is_approx(b):
        # v10: a floating-point value is an approximation: relative tolerance, never exact equality (M2-SF-04, one ulp).
        # v11: absolute tolerance APPROX_ATOL (1e-12) only near 0, so that 0 and 5e-10 differ.
        return isclose(float(sp.N(a)), float(sp.N(b)), rel_tol=tol, abs_tol=APPROX_ATOL)
    if isinstance(a, sp.Basic) or isinstance(b, sp.Basic):
        return sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0
    if isinstance(a, (int, F)) and isinstance(b, (int, F)) and not isinstance(a, bool) and not isinstance(b, bool):
        return F(a) == F(b)  # v11: exact integers and fractions are compared exactly (10**18 and 10**18 + 1 differ)
    return isclose(float(a), float(b), rel_tol=tol, abs_tol=APPROX_ATOL)


def ck(row, what, got, want, tol=1e-9):
    run[0] += 1
    ok = same(got, want, tol)
    records.append((row, what, got, want, ok))
    if not ok:
        fails.append((row, what, got, want))


def distinct(row, key, sigs):
    vals = [key] + sigs
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            a, b = vals[i], vals[j]
            if isinstance(a, sp.Basic) or isinstance(b, sp.Basic):
                same = sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0
            else:
                same = isclose(float(a), float(b), rel_tol=1e-12, abs_tol=1e-12)
            if same:
                fails.append((row, 'collision', a, b))


# ---------------- BREVET
ck('BR-NC-01', 'key', F(-3, 4) + F(1, 2), F(-1, 4))
ck('BR-NC-01', 'E1', F(-3 + 1, 4 + 2), F(-1, 3))
ck('BR-NC-01', 'E2', F(3, 4) + F(1, 2), F(5, 4))
ck('BR-NC-01', 'E3', -(F(3, 4) + F(1, 2)), F(-5, 4))
distinct('BR-NC-01', F(-1, 4), [F(-1, 3), F(5, 4), F(-5, 4)])
ck('BR-NC-02', 'E2 equal value', 42e-5, 0.00042)
ck('BR-NC-03', 'key', 2**2 * 3 * 7, 84)
ck('BR-NC-03', 'E1 lcm', sp.ilcm(84, 36), 252)
ck('BR-NC-03', 'E2 open', 2 * 3, 6)
ck('BR-NC-03', 'gcd', sp.igcd(84, 36), 12)
ck('BR-NC-04', 'key', sp.expand((3*x - 5)*(3*x + 5)), 9*x**2 - 25)
for wrong in [(x - 5)*(x + 5), (3*x + 5)**2, (3*x - 5)**2]:
    assert sp.expand(wrong) != 9*x**2 - 25
ck('BR-NC-05', 'key', sp.solve(3*(2*x - 1) - 9, x)[0], 2)
ck('BR-NC-05', 'E2', sp.solve(6*x - 1 - 9, x)[0], F(5, 3))
ck('BR-NC-05', 'E4', sp.solve(6*x - (9 - 3), x)[0], 1)
d = [9, 2, 8, 2, 5]
ck('BR-DF-01', 'key median', sorted(d)[2], 5)
ck('BR-DF-01', 'E1', d[2], 8)
ck('BR-DF-01', 'E4 mean', F(sum(d), 5), F(26, 5))
distinct('BR-DF-01', 5, [8, 2, 5.2])
ck('BR-DF-01', 'open mean', F(1 + 2 + 2 + 3 + 12, 5), 4)
ck('BR-DF-01', 'E2 open', F(20, 4), 5)
ck('BR-DF-03', 'key', 80 * F(125, 100), 100)
ck('BR-DF-03', 'E5', 80 + F(25, 100), F(8025, 100))
ck('BR-DF-03', 'open', 100 * F(11, 10) * F(9, 10), 99)
ck('BR-DF-04', 'key', F(7 + 2, 3), 3)
ck('BR-DF-04', 'E1', 3 * 7 - 2, 19)
ck('BR-DF-04', 'E4', F(7 - 2, 3), F(5, 3))
ck('BR-DF-04', 'open', F(18 - 4, 2), 7)
ck('BR-DF-05', 'key', F(7 - 1, 3 - 0), 2)
ck('BR-DF-05', 'E3', F(3, 6), F(1, 2))
ck('BR-DF-05', 'open b', 4 - 2 * 1, 2)
ck('BR-DF-05', 'open slope', F(8 - 4, 3 - 1), 2)
ck('BR-GM-01', 'key', 1.5 * 10**4, 15000)
ck('BR-GM-01', 'open', 0.25 * 1000, 250)
ck('BR-GM-02', 'key', 3**2 * 4, 36)          # in units of pi
ck('BR-GM-02', 'E2', 6**2 * 4, 144)
ck('BR-GM-02', 'E3 lateral', 2 * 3 * 4, 24)
ck('BR-GM-02', 'E4 cone', F(1, 3) * 9 * 4, 12)
ck('BR-GM-02', 'trap r=2', 2**2 * 3, 2 * 2 * 3)  # pi r^2 h = 2 pi r h when r = 2
ck('BR-GM-03', 'open', (F(3, 2))**2, F(9, 4)); ck('BR-GM-03', 'open3', (F(3, 2))**3, F(27, 8))
ck('BR-GM-04', 'key', 60 * 1.5, 90); ck('BR-GM-04', 'E4', 60 * (1 + 50 / 60), 110)
ck('BR-GM-04', 'open', 2 * 3 * 0.20, 1.20)
ck('BR-EG-01', 'key', sqrt(36 + 64), 10); ck('BR-EG-01', 'E5', sqrt(64 - 36), sqrt(28))
ck('BR-EG-01', 'open', 13**2, 5**2 + 12**2); ck('BR-EG-01', 'E2 open', 5**2 + 13**2, 194)
ck('BR-EG-02', 'key', F(9 * 4, 6), 6); ck('BR-EG-02', 'E1', F(9 * 6, 4), F(27, 2))
ck('BR-EG-02', 'E3', 9 * F(4, 6 - 4), 18); ck('BR-EG-02', 'E4', 9 - (6 - 4), 7)
ck('BR-EG-02', 'open', 4.2 * 5 / 3, 7)
ck('BR-EG-03', 'open angle', degrees(atan(0.75)), 36.8698976, 1e-6); ck('BR-EG-03', 'rad', atan(0.75), 0.6435011, 1e-6)
ck('BR-EG-07', 'key', 9**2, 81); ck('BR-EG-07', 'key2', 6**2 + 7**2, 85); ck('BR-EG-07', 'E2', 6**2 + 9**2, 117)
ck('BR-EG-07', 'open', 17**2, 8**2 + 15**2)
ck('BR-EG-08', 'key', F(3, 5) * 35, 21); ck('BR-EG-08', 'key2', F(4, 7) * 35, 20)
ck('BR-EG-08', 'open', F(24, 60), F(3, F(75, 10)))
ck('BR-EG-09', 'key', 180 - 50 - 65, 65); ck('BR-EG-09', 'E1', 360 - 50 - 65, 245)
ck('BR-EG-11', 'open', 5 * F(6, 4), F(15, 2)); ck('BR-EG-11', 'E1 open', 5 * F(4, 6), F(10, 3))
ck('BR-EG-15', 'key', 5**2 + 12**2, 13**2); ck('BR-EG-15', 'open', degrees(atan(12 / 5)), 67.38, 1e-3)
ck('BR-AP-01', 'key', 3 * (-3) + 4, -5); ck('BR-AP-01', 'E1', (-3 + 4) * 3, 3); ck('BR-AP-01', 'E4', 9 + 4, 13)
ck('BR-AP-01', 'trap fixed point', 3 * (-2) + 4, -2)
distinct('BR-AP-01', -5, [3, -3, 13, -13])
xx = 1
for _ in range(3):
    xx += 2
ck('BR-AP-03', 'key', xx, 7)
xx, seq = 1, [1]
while not xx > 10:
    xx += 3; seq.append(xx)
ck('BR-AP-03', 'open', xx, 13)
# ---------------- PREMIERE
ck('1S-AU-01', 'key', F(3, 4) * F(8, 9), F(2, 3)); ck('1S-AU-01', 'E3', F(27, 32), F(3 * 9, 4 * 8))
ck('1S-AU-01', 'E4', F(3 + 8, 4 + 9), F(11, 13)); ck('1S-AU-01', 'E5', F(24, 9), F(8, 3))
ck('1S-AU-01', 'open', F(2)**-3 * 2**5, 4); ck('1S-AU-01', 'E2 open', -8 * 32, -256)
distinct('1S-AU-01', F(2, 3), [F(27, 32), F(11, 13), F(8, 3)])
ck('1S-AU-02', 'key', F(12, 10) * F(8, 10) - 1, F(-4, 100))
ck('1S-AU-02', 'open', F(126) / F(105, 100), 120); ck('1S-AU-02', 'E3', 126 * 0.95, 119.7); ck('1S-AU-02', 'E2', 126 / 0.05, 2520)
ck('1S-AU-04', 'open', sp.solve(-2*x + 3 - 5, x)[0], -1); ck('1S-AU-04', 'E2', -2*5 + 3, -7)
ck('1S-AL-01', 'key', set(sp.solve(x**2 - 5*x + 6, x)), {2, 3})
ck('1S-AL-01', 'E4', set([(5 + 7) / 2, (5 - 7) / 2]), {6, -1})
ck('1S-AL-01', 'open', set(sp.solve(2*x**2 - 3*x - 2, x)), {2, sp.Rational(-1, 2)})
ck('1S-AL-02', 'open', sp.expand((x - 2)**2 - 3), x**2 - 4*x + 1)
ck('1S-AL-04', 'key', 3 + 3 * 4, 15); ck('1S-AL-04', 'E2', 3 * 4**3, 192); ck('1S-AL-04', 'E3', 3 + 7 + 11 + 15, 36)
ck('1S-AL-04', 'trap r=2', 3 + 5 + 7 + 9, 3 * 2**3)
ck('1S-AL-04', 'open', sum(3 + 2 * k for k in range(5)), 35)
ck('1S-AL-05', 'key', sum(2**k for k in range(6)), 63); ck('1S-AL-05', 'E1', 2**5 - 1, 31)
ck('1S-AL-05', 'open', F(1 - 2**4, 1 - 2), 15)
ck('1S-AN-01', 'key', sp.diff(x*sp.exp(x), x), (x + 1)*sp.exp(x))
ck('1S-AN-01', 'open', sp.diff((x**2 + 1)*sp.exp(x), x), (x + 1)**2*sp.exp(x))
ck('1S-AN-01', 'E3 variant', sp.diff(x*sp.exp(2*x), x), (1 + 2*x)*sp.exp(2*x))
ck('1S-AN-02', 'key', sp.diff(x**2, x).subs(x, 3), 6)
ck('1S-AN-02', 'open', sp.expand(-2*(x + 1) + 1), -2*x - 1)
ck('1S-AN-02', 'E5 secant', 16 - 9, 7)
ck('1S-AN-03', 'key', sp.solve(sp.diff(-x**2 + 4*x, x), x)[0], 2)
ck('1S-AN-03', 'open', (x**2 - 4*x + 1).subs(x, 2), -3)
ck('1S-AN-04', 'key', sp.simplify(sp.exp(x + 1) / sp.exp(x)), sp.E)
ck('1S-AN-05', 'E1', cos(pi / 3 * pi / 180), 0.99983, 1e-4)
ck('1S-GE-01', 'key', 2 * 1 + (-1) * 2, 0); ck('1S-GE-01', 'E1', 2 * 2 + (-1) * 1, 3); ck('1S-GE-01', 'E2', 2 * 2 - (-1) * 1, 5)
ck('1S-GE-02', 'key', 2 * 3 * 0.5, 3); ck('1S-GE-02', 'E2', 2 * 3 * sqrt(3) / 2, 3 * sqrt(3))
ck('1S-GE-02', 'open', 1 / sqrt(2), 1 / sqrt(2))
ck('1S-GE-03', 'key', 2 * 1 + 3 * 0 - 2, 0); ck('1S-GE-03', 'E1', 3 * 1 - 2 * 0 - 3, 0)
ck('1S-GE-03', 'open', 1 + 3 * 2 - 7, 0); ck('1S-GE-03', 'open normal', 3 * 1 + (-1) * 3, 0)
ck('1S-PS-01', 'open', 0.4 * 0.5 + 0.6 * 0.25, 0.35)
ck('1S-PS-02', 'key', 0.5 * 0.4, 0.2)
ck('1S-PS-02', 'open', F(8, 100) / (F(8, 100) + F(9, 100)), F(8, 17))
ck('1S-PS-02', 'E2', F(8, 10) / (F(8, 10) + F(1, 10)), F(8, 9))
ck('1S-PS-02', 'old trap', F(8, 10) / (F(8, 10) + F(2, 10)), F(8, 10))
ck('1S-PS-03', 'key', 0 * 0.6 + 5 * 0.4, 2); ck('1S-PS-03', 'E4', 5 * 0.6, 3)
ck('1S-PS-03', 'open', -1 * 0.75 + 3 * 0.25, 0)
ck('1S-PS-04', 'key', F(1 + 25, 2) - F(1 + 5, 2)**2, 4); ck('1S-PS-04', 'E1', F(26, 2), 13)
ck('1S-PS-04', 'E3', (1 - 3)**2 + (5 - 3)**2, 8)
distinct('1S-PS-04', 4, [13, 2, 8, -4])
nn, u = 0, 1.0
while u <= 2:
    nn += 1; u *= 1.1
ck('1S-AP-02', 'open', nn, 8)
nn = 0
while 2**nn <= 1000:
    nn += 1
ck('1S-AP-02', 'key', nn, 10)
ck('1S-AP-03', 'open f(1.5)', 1.5**2 - 2, 0.25); ck('1S-AP-03', 'open f(1.25)', 1.25**2 - 2, -0.4375)
ck('1C-AU-01', 'open', 1 / 8, 0.125)
ck('1C-AU-02', 'E2', 49 * 201, 9849); ck('1C-AU-02', 'open', 5 * 1.9e3, 9.5e3)
ck('1C-AU-04', 'key', 80 * 1.25 * 0.9, 90); ck('1C-AU-04', 'E3', 100 - 8, 92); ck('1C-AU-04', 'E2', 80 * 0.25 * 0.9, 18)
ck('1C-AU-04', 'open', 50 * 0.9, 45)
ck('1C-FN-01', 'key', 2 * 3 + 1, 7); ck('1C-FN-01', 'E2', 1 * 3 + 2, 5)
ck('1C-FN-04', 'key', 2**3, 8)
ck('1C-SE-02', 'key', 5 + 4 * 2, 13); ck('1C-SE-02', 'open', 7 + 5 * 3, 22)
ck('1C-SE-03', 'key', 100 * F(1, 2)**3, F(25, 2)); ck('1C-SE-03', 'E4', F(100, 6), F(50, 3))
ck('1C-SE-04', 'key', 100 * 1.2**2, 144); ck('1C-SE-04', 'open', 100 * 1.2**3, 172.8)
ck('1C-PR-01', 'key', F(150, 200), F(3, 4)); ck('1C-PR-01', 'E1', F(150, 160), F(15, 16))
ck('1C-PR-03', 'open', 0.25 * 0.4 + 0.75 * 0.6, 0.55)
ck('1C-PR-04', 'key', 0.3**2, 0.09); ck('1C-PR-04', 'E5', 0.7**2, 0.49)
ck('1C-PR-04', 'open', 3 * 0.4**2 * 0.6, 0.288); ck('1C-PR-04', 'E2', 0.4**2 * 0.6, 0.096)
# ---------------- TERMINALE
ck('TS-AG-01', 'key', perm(5, 3), 60); ck('TS-AG-01', 'E1', comb(5, 3), 10)
ck('TS-AG-02', 'key', comb(6, 2), 15); ck('TS-AG-02', 'E2', perm(6, 2), 30); ck('TS-AG-02', 'E5', factorial(6) // factorial(2), 360)
ck('TS-AG-02', 'trap', comb(5, 2), 5 * 2)
for a in range(1, 7):
    for b in range(0, a):
        assert comb(a, b) + comb(a, b + 1) == comb(a + 1, b + 1)
ck('TS-AG-04', 'key', 2 - 2 * 1 + 3 * 1 - 3, 0); ck('TS-AG-04', 'E1', 2 * 1 + (-2) + 3 - 3, 0)
ck('TS-AG-04', 'open A', 2 * 1 - 0 + 2 - 4, 0); ck('TS-AG-04', 'open B', 2 * 2 - 1 + 1 - 4, 0)
ck('TS-AN-02', 'key', sp.limit((2*n**2 + 1) / (n**2 - 3), n, sp.oo), 2)
ck('TS-AN-02', 'open', sp.limit((3*x**2 - x) / (x**2 + 1), x, sp.oo), 3)
ck('TS-AN-04', 'key (v7 seed)', sp.integrate(x*sp.exp(2*x), (x, 0, 1)), (sp.E**2 + 1)/4)
ck('TS-AN-04', 'E1 (v7 seed)', sp.E**2/2 + (sp.E**2 - 1)/4, (3*sp.E**2 - 1)/4)
ck('TS-AN-04', 'E3 (v7 seed)', ((1 + 2*x)*sp.exp(2*x)).subs(x, 1) - ((1 + 2*x)*sp.exp(2*x)).subs(x, 0), 3*sp.E**2 - 1)
ck('TS-AN-04', 'E4 (v7 seed)', sp.integrate(x, (x, 0, 1)) * sp.integrate(sp.exp(2*x), (x, 0, 1)), (sp.E**2 - 1)/4)
ck('TS-AN-04', 'open', sp.integrate(x*sp.exp(x), (x, 0, 1)), 1)
distinct('TS-AN-04', (sp.E**2 + 1)/4, [(3*sp.E**2 - 1)/4, (1 - sp.E**2)/4, 3*sp.E**2 - 1, (sp.E**2 - 1)/4, sp.E**2])
y = sp.Function('y')
ck('TS-AN-05', 'open', sp.dsolve(sp.Eq(y(x).diff(x) + y(x), 2), y(x), ics={y(0): 0}).rhs, 2 - 2*sp.exp(-x))
ck('TS-AN-08', 'open eps=1e-2', int(1 / sqrt(1e-2)) + 1, 11)
ck('TS-AN-08', 'open eps=1e-4', int(round(1 / sqrt(1e-4))) + 1, 101)
ck('TS-AN-09', 'key', 1001, int(sqrt(10**6)) + 1)
ck('TS-AN-13', 'key', sp.expand(((3 + h)**2 - 9) / h), 6 + h)
ck('TS-AN-13', 'open', sp.simplify((1 / (x + h) - 1 / x) / h), -1 / (x*(x + h)))
ck('TS-AN-14', 'key', 2 + 0.25 * 0.1, 2.025); ck('TS-AN-14', 'E1', 2 + 0.1 / (2 * sqrt(4.1)), 2.0247, 1e-4)
ck('TS-AN-14', 'E2', 2 + 0.25, 2.25); ck('TS-AN-14', 'E6', 2 + 0.5 * 0.1, 2.05)
ck('TS-AN-15', 'key', sum(F(k, 4)**2 for k in range(4)) / 4, F(7, 32))
ck('TS-AN-15', 'E1', sum(F(k, 4)**2 for k in range(4)), F(7, 8))
ck('TS-AN-15', 'E2', sum(F(k, 4)**2 for k in range(1, 5)) / 4, F(15, 32))
ck('TS-AN-16', 'key', sp.limit((sp.exp(x) - 1) / x, x, 0), 1)
ck('TS-AN-16', 'open', sp.limit(sp.log(1 + x) / x, x, 0), 1)
ck('TS-PR-01', 'key', comb(4, 1) * 0.3 * 0.7**3, 0.4116); ck('TS-PR-01', 'E2', 0.3 * 0.7**3, 0.1029)
ck('TS-PR-01', 'open', 3 * 0.2 * 0.8**2, 0.384)
ck('TS-PR-02', 'key', 10 * 0.3 * 0.7, 2.1); ck('TS-PR-02', 'E1', 10 * 0.3**2, 0.9); ck('TS-PR-02', 'E3', sqrt(2.1), 1.449, 1e-3)
ck('TS-PR-02', 'trap p=.5', 10 * 0.5**2, 10 * 0.5 * 0.5)
ck('TS-PR-02', 'open', 20 * 0.25 * 0.75, 3.75)
ck('TS-PR-03', 'open', 4 * 2 + 3, 11); ck('TS-PR-03', 'E1', sqrt(2) + sqrt(3), 3.146, 1e-3)
ck('TS-PR-04', 'key', F(4, 16), F(1, 4)); ck('TS-PR-04', 'open', 4 / (100 * 0.25), 0.16)
ck('TS-AP-01', 'open', sum(k**2 for k in range(1, 4)), 14)
ck('TS-AP-03', 'key', 0.5 * sum([0, 0.5, 1, 1.5]), 1.5); ck('TS-AP-03', 'E2', 0.5 * sum([0.5, 1, 1.5, 2]), 2.5)
ck('TS-AP-03', 'E1', sum([0, 0.5, 1, 1.5]), 3)
ck('TS-AP-03', 'open', (0 + 0.25 + 0.5 + 0.75) / 4, 3 / 8); ck('TS-AP-03', 'open R', (0.25 + 0.5 + 0.75 + 1) / 4, 5 / 8)
ck('TE-CX-02', 'open', sp.expand((1 + sp.I)**4), -4)
zs = [sp.exp(sp.I*(sp.pi/4 + k*sp.pi/2)) for k in range(4)]
for z in zs:
    ck('TE-CX-03', 'open root', sp.simplify(z**4), -1)
ck('TE-CX-04', 'open', sp.simplify((4 + 2*sp.I) / (2 + sp.I)), 2)
ck('TE-AR-01', 'open', 84 - 2 * 36, 12)
ck('TE-AR-02', 'key', (3 * 5) % 7, 1)
ck('TE-AR-02', 'open', sorted(x0 for x0 in range(6) if (4 * x0) % 6 == 2), [2, 5])
ck('TE-AR-03', 'key', pow(2, 10, 11), 1)
ck('TE-AR-04', 'key', 7**4 % 10, 1); ck('TE-AR-04', 'open', (1 + 2 * 2 + 3 * 3) % 11, 3)
for digits in [(1, 2, 3), (4, 0, 9)]:
    c = (digits[0] + 2 * digits[1] + 3 * digits[2]) % 11
    for pos in range(3):
        for nd in range(10):
            if nd != digits[pos]:
                dd = list(digits); dd[pos] = nd
                assert (dd[0] + 2 * dd[1] + 3 * dd[2]) % 11 != c
A = sp.Matrix([[1, 1], [0, 1]])
ck('TE-GM-01', 'key', A**2, sp.Matrix([[1, 2], [0, 1]])); ck('TE-GM-01', 'open', A.inv(), sp.Matrix([[1, -1], [0, 1]]))
Pth = sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
ck('TE-GM-02', 'open', Pth**2, sp.Matrix([[1, 0, 1], [0, 2, 0], [1, 0, 1]]))
Pm = sp.Matrix([[sp.Rational(8, 10), sp.Rational(2, 10)], [sp.Rational(3, 10), sp.Rational(7, 10)]])
ck('TE-GM-03', 'key', sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2)]]) * Pm, sp.Matrix([[sp.Rational(55, 100), sp.Rational(45, 100)]]))
ck('TE-GM-03', 'E1', Pm * sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)]), sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)]))
ck('TE-GM-03', 'open', sp.Matrix([[1, 0]]) * Pm**2, sp.Matrix([[sp.Rational(7, 10), sp.Rational(3, 10)]]))
ck('TE-GM-04', 'open', sp.Matrix([[sp.Rational(6, 10), sp.Rational(4, 10)]]) * Pm, sp.Matrix([[sp.Rational(6, 10), sp.Rational(4, 10)]]))
ck('TC-SE-01', 'open', 1000 * 1.03**3, 1092.727)
u1 = 10000 * 1.005 - 500; u2 = u1 * 1.005 - 500
ck('TC-SE-03', 'open u1', u1, 9550); ck('TC-SE-03', 'open u2', u2, 9097.75)
ck('TC-FN-03', 'open', 5 * log(2), -log(0.5) / 0.2)
ck('TC-FN-04', 'open', (-x**2 + 6*x).subs(x, 2), 8)
ck('TC-IN-01', 'open', sp.integrate(2*t, (t, 0, 3)), 9)
ck('TC-IN-02', 'open L', 1 * (0**2 + 1**2), 1); ck('TC-IN-02', 'open R', 1 * (1**2 + 2**2), 5)
ck('TC-IN-03', 'key', sp.integrate(x**2, (x, 1, 3)) / 2, sp.Rational(13, 3)); ck('TC-IN-03', 'E2', (1 + 9) / 2, 5)
ck('TC-IN-03', 'open', sp.integrate(x**2, (x, 0, 3)) / 3, 3)
ck('TC-IN-04', 'key', 1 - 2 * sp.integrate(x**3, (x, 0, 1)), sp.Rational(1, 2))
ck('TC-IN-04', 'trap', sp.integrate(x**2, (x, 0, 1)), 1 - 2 * sp.integrate(x**2, (x, 0, 1)))
ck('TC-PR-01', 'key', 0.8**3, 0.512); ck('TC-PR-01', 'E1', 3 * 0.2 * 0.8**2, 0.384); ck('TC-PR-01', 'open', 0.8**2 * 0.2, 0.128)
ck('TC-PR-02', 'open', exp(-0.5 * 5) / exp(-0.5 * 2), exp(-1.5))
ck('TC-PR-03', 'open', 200 * 0.02, 4)
ck('TC-ST-02', 'open', 1.5 * 4 + 2, 8)
ck('TC-ST-04', 'open', [4 - (2 * 1 + 1), 4 - (2 * 2 + 1), 8 - (2 * 3 + 1)], [1, -1, 1])
ck('TC-BA-01', 'key', (0.01 * 0.99) / (0.01 * 0.99 + 0.99 * 0.01), 0.5)
ck('TC-BA-03', 'open p=.1', 0.9 * 0.1 / (0.9 * 0.1 + 0.1 * 0.9), 0.5)
ck('TC-BA-03', 'open p=.01', 0.9 * 0.01 / (0.9 * 0.01 + 0.1 * 0.99), 0.0833, 1e-3)
# ---------------- MP2I
ck('M1-CA-01', 'open', sp.summation(n + 1, (n, 1, x)).expand(), (x*(x + 3) / 2).expand())
ck('M1-CA-02', 'key', sp.expand((1 + x)**4).coeff(x, 2), 6)
ck('M1-CA-03', 'open', sp.summation(sp.summation(1, (t, 1, n)), (n, 1, x)).expand(), (x*(x + 1) / 2).expand())
ck('M1-CA-04', 'open', set(sp.solve(2*X**2 + X - 1, X)), {sp.Rational(1, 2), -1})
ck('M1-CX-01', 'open', sp.expand_complex(sp.sqrt(2)*sp.exp(3*sp.I*sp.pi/4)), -1 + sp.I)
ck('M1-CX-03', 'open', set(sp.solve(x**2 - 2*x + 2, x)), {1 + sp.I, 1 - sp.I})
ck('M1-TA-01', 'open', sp.diff(sp.exp(x**2), x), 2*x*sp.exp(x**2))
ck('M1-TA-02', 'open', sp.dsolve(sp.Eq(y(x).diff(x) + 2*y(x), 4), y(x), ics={y(0): 0}).rhs, 2 - 2*sp.exp(-2*x))
ck('M1-TA-03', 'open', sp.dsolve(y(x).diff(x, 2) - 3*y(x).diff(x) + 2*y(x), y(x), ics={y(0): 1, y(x).diff(x).subs(x, 0): 0}).rhs, 2*sp.exp(x) - sp.exp(2*x))
ck('M1-AA-03', 'key', sp.limit((1 - sp.cos(x)) / x**2, x, 0), sp.Rational(1, 2))
ck('M1-AA-03', 'open', sp.limit((sp.exp(x) - 1 - x) / x**2, x, 0), sp.Rational(1, 2))
ck('M1-AR-02', 'key', 7**2 % 5, 4)
ck('M1-AR-03', 'key', sp.multiplicity(2, 40), 3); ck('M1-AR-03', 'open', (sp.multiplicity(3, 72), sp.multiplicity(2, 72)), (2, 3))
for k in range(-3, 4):
    assert 6 * (-1 + 3 * k) + 9 * (1 - 2 * k) == 3
ck('M1-PO-04', 'key', sp.apart((3*X + 5) / ((X + 1)*(X + 2))), 2 / (X + 1) + 1 / (X + 2))
ck('M1-PO-04', 'open', sp.apart((X + 7) / ((X - 1)*(X + 3))), 2 / (X - 1) - 1 / (X + 3))
ck('M1-PO-04', 'old trap', sp.apart((2*X + 3) / ((X + 1)*(X + 2))), 1 / (X + 1) + 1 / (X + 2))
ck('M1-PO-03', 'key', sp.factor(X**4 - 1), (X - 1)*(X + 1)*(X**2 + 1))
ck('M1-AL-02', 'key', sp.solve([x + 2*y(0) - 5, 3*x - y(0) - 1], [x, y(0)]), {x: 1, y(0): 2})
ck('M1-AL-02', 'E1', sp.Rational(-1, 7), sp.Rational(-1, 7))
ck('M1-AL-03', 'open', sp.Matrix([[1, 1], [1, -1]]) * sp.Matrix([2, 1]), sp.Matrix([3, 1]))
Md = sp.Matrix([[1, 2, 3], [0, 1, 4], [5, 6, 0]])
ck('M1-DT-02', 'key', Md.det(), 1)
ck('M1-DT-02', 'E3', 1 * (1 * 0 - 4 * 6) + 2 * (0 * 0 - 4 * 5) + 3 * (0 * 6 - 1 * 5), -79)
m = sp.symbols('m')
ck('M1-DT-04', 'open', set(sp.solve(sp.Matrix([[m, 2], [3, m - 1]]).det(), m)), {3, -2})
ck('M1-IN-03', 'open', sp.integrate(1 + t**2, (t, 1, 1)), 0)
ck('M1-PR-01', 'key', comb(6, 2), 15); ck('M1-PR-01', 'E3', comb(6 + 1, 2), 21); ck('M1-PR-01', 'trap', comb(5, 2), 5 * 2)
ck('M1-PR-02', 'key', F(6, 36), F(1, 6)); ck('M1-PR-02', 'open', F(3, 36), F(1, 12))
ck('M1-PR-03', 'open', F(3, 5) * F(2, 4), F(3, 10))
ck('M1-EU-02', 'open', sp.Matrix([1, 1]) - (sp.Matrix([1, 1]).dot(sp.Matrix([1, 0]))) * sp.Matrix([1, 0]), sp.Matrix([0, 1]))
ck('M1-EU-03', 'open', (sp.Matrix([2, 1]).dot(sp.Matrix([1, 1])) / 2) * sp.Matrix([1, 1]), sp.Matrix([sp.Rational(3, 2), sp.Rational(3, 2)]))
ck('M1-EU-04', 'open', (sp.Matrix([2, 1]) - sp.Matrix([sp.Rational(3, 2), sp.Rational(3, 2)])).norm(), sp.sqrt(2) / 2)
ck('M1-SN-02', 'open', sp.summation(1 / (n*(n + 1)), (n, 1, sp.oo)), 1)
ck('M1-F2-01', 'open', (sp.diff(x**2*t + x*t**2, x), sp.diff(x**2*t + x*t**2, t)), (2*x*t + t**2, x**2 + 2*x*t))
# ---------------- MPI
ck('M2-ST-01', 'key', (3 * 5) % 7, 1)
ck('M2-ST-01', 'open', [a for a in range(8) if sp.igcd(a, 8) == 1], [1, 3, 5, 7])
ck('M2-ST-02', 'key', [a for a in range(15) if a % 3 == 1 and a % 5 == 2], [7])
ck('M2-ST-02', 'open', [a for a in range(15) if a % 3 == 2 and a % 5 == 3], [8])
ck('M2-ST-03', 'key', sp.totient(12), 4); ck('M2-ST-03', 'open', (sp.totient(15), pow(2, 8, 15)), (8, 1))
ck('M2-ST-04', 'key', sp.igcd(6, 10), 2)
ck('M2-RED-01', 'open', sp.Matrix([[2, 1], [0, 3]]).charpoly(X).as_expr(), sp.expand((X - 2)*(X - 3)))
J = sp.Matrix([[1, 1], [0, 1]])
ck('M2-RED-02', 'open', (J - sp.eye(2)).nullspace()[0], sp.Matrix([1, 0])); assert len((J - sp.eye(2)).nullspace()) == 1
S = sp.Matrix([[2, 1], [1, 2]]); Q = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
ck('M2-EU-03', 'open', sp.simplify(Q.T * S * Q), sp.diag(3, 1))
ck('M2-SE-02', 'key', sp.limit((n / (n + 1))**n, n, sp.oo), sp.exp(-1))
ck('M2-SF-04', 'open', sp.integrate(2 / (2 - x), (x, 0, 1)), 2*sp.log(2))
# v10: exact rational partial sum and a proven bound, instead of comparing two floats
# 2 ln 2 = Σ_{k≥0} 1/((k+1)2^k); tail after 80 terms < Σ_{k≥80} 2^-k/81 = 2^-79/81 ≈ 2.04e-26 < 3e-26
_S80 = sum(sp.Rational(1, (k + 1) * 2**k) for k in range(80))
ck('M2-SF-04', 'open series', int(bool(abs(sp.N(2*sp.log(2) - _S80, 60)) < sp.Rational(3, 10**26))), 1)
ck('M2-SEN-02', 'open', sp.diff(1 / (1 - x), x), 1 / (1 - x)**2)
ck('M2-SEN-03', 'open', sp.diff(-sp.log(1 - x), x), 1 / (1 - x))
ck('M2-FV-02', 'key', (sp.integrate(t, (t, 0, 1)), sp.integrate(t**2, (t, 0, 1))), (sp.Rational(1, 2), sp.Rational(1, 3)))
ck('M2-FV-02', 'open', (sp.integrate(2*t, (t, 0, 1)), sp.integrate(sp.exp(t), (t, 0, 1))), (1, sp.E - 1))
ck('M2-FV-03', 'open', (sp.series(sp.exp(t), t, 0, 3).removeO(), sp.series(sp.cos(t), t, 0, 3).removeO()), (1 + t + t**2/2, 1 - t**2/2))
ck('M2-IN-01', 'open', sp.integrate(1 / t**2, (t, 1, sp.oo)), 1)
npos = sp.symbols('npos', positive=True)
ck('M2-IN-03', 'open', sp.integrate(sp.exp(-npos*t), (t, 0, 1)), (1 - sp.exp(-npos)) / npos)
ck('M2-IN-04', 'key', sp.integrate(t*sp.exp(-t), (t, 0, sp.oo)), 1)
lam, mu = sp.symbols('lambda mu', positive=True)
k = sp.symbols('k', integer=True, nonnegative=True)
ck('M2-PR-01', 'open', sp.summation(sp.exp(-lam)*lam**k/sp.factorial(k), (k, 0, sp.oo)).simplify(), 1)
ck('M2-PR-02', 'open E', sp.summation(k*sp.exp(-lam)*lam**k/sp.factorial(k), (k, 0, sp.oo)).simplify(), lam)
ck('M2-ED-01', 'open', sp.dsolve(sp.Eq(y(t).diff(t) - 2*y(t), 0), y(t), ics={y(1): sp.E**2}).rhs, sp.exp(2*t))
Aed = sp.Matrix([[1, 2], [2, 1]])
Xt = sp.Rational(1, 2)*sp.exp(3*t)*sp.Matrix([1, 1]) + sp.Rational(1, 2)*sp.exp(-t)*sp.Matrix([1, -1])
ck('M2-ED-03', 'open ode', sp.simplify(Xt.diff(t) - Aed*Xt), sp.zeros(2, 1)); ck('M2-ED-03', 'open init', Xt.subs(t, 0), sp.Matrix([1, 0]))
ck('M2-ED-04', 'key', sp.dsolve(sp.Eq(y(t).diff(t) + y(t), 1), y(t), ics={y(0): 0}).rhs, 1 - sp.exp(-t))
ck('M2-CD-02', 'key', sp.diff(t**2 + t**4, t).subs(t, 1), 6)
ck('M2-CD-04', 'max', sp.sqrt(2)/2 + sp.sqrt(2)/2, sp.sqrt(2))

print('checks run:', run[0])
print('checks failed:', len(fails))
for f in fails:
    print('  ', f)
