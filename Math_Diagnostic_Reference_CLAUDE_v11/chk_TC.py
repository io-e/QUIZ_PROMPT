"""Independent recomputation of Terminale mathématiques complémentaires v7 values."""
from fractions import Fraction as F
import math
import sympy as sp

x, q = sp.symbols('x q')
E = sp.E


def first(pred, start=0, stop=10 ** 6):
    k = start
    while not pred(k):
        k += 1
        if k > stop:
            raise ValueError('no rank found')
    return k


def bisect(f, a, b, steps):
    for _ in range(steps):
        mid = (a + b) / 2
        if f(a) * f(mid) <= 0:
            b = mid
        else:
            a = mid
    return a, b


def fmt_iv(iv):
    return '[%s ; %s]' % tuple(('%g' % v) for v in iv)


g5 = lambda v: v ** 3 + v - 1
fc = x ** 3 - 3 * x ** 2 + 2
CM = (q ** 2 + 2 * q + 36) / q

CHECKS = {
 'TC-SE-05': dict(K=(1 - F(1, 2) ** 10) / (1 - F(1, 2)), A=round(1000 * (1.03 ** 10 - 1) / 0.03, 2), E1=(1 - F(1, 2) ** 9) / (1 - F(1, 2)), E2=2,
                  E3=F(10, 2) * (1 + F(1, 2) ** 9)),
 'TC-SE-06': dict(K=100 - sp.solve(sp.Symbol('l') - (F(8, 10) * sp.Symbol('l') + 50))[0], A=sp.solve(sp.Symbol('l') - (F(8, 10) * sp.Symbol('l') + 50))[0],
                  E1=100 + 250, E2=100, E3=100 - 50),
 'TC-FN-05': dict(K=fmt_iv(bisect(g5, 0, 1, 2)), A=first(lambda k: 1 / 2 ** k < 0.01), E1=sum(bisect(g5, 0, 1, 2)) / 2,
                  E2=fmt_iv(bisect(g5, 0, 1, 1)), E3=fmt_iv((0.75, 1))),
 'TC-FN-06': dict(K=first(lambda k: 3 * 1.05 ** k >= 6), A=E ** 2, E1=math.ceil(math.log(6) / (3 * math.log(1.05))), E2=math.floor(math.log(2) / math.log(1.05)),
                  E3=math.ceil(math.log(6) / math.log(1.05))),
 'TC-FN-07': dict(K=sp.limit((3 * x + 1) / (x - 2), x, sp.oo), A='+∞', E1=1, E2=F(1, -2), E3='+∞'),
 'TC-FN-08': dict(K=[r for r in sp.solve(sp.diff(CM, q), q) if r > 0][0], A=CM.subs(q, 6), E1=sp.solve(sp.diff(q ** 2 + 2 * q + 36, q), q)[0], E2=36, E3=CM.subs(q, 6)),
 'TC-FN-09': dict(K=sp.integrate(4 * x ** 3 - 6 * x + 2, x), A=sp.diff(x * sp.exp(x), x), E1=sp.diff(4 * x ** 3 - 6 * x + 2, x), E2=4 * x ** 4 - 6 * x ** 2 + 2 * x,
                  E3=x ** 4 - 3 * x ** 2 + 2),
 'TC-FN-10': dict(K=sp.solve(F(1, 2) * x - 2, x)[0], A=(6 - 4) * sp.exp(x / 2) + 4, E1=-2, E2=-4, E3=F(1, 2) * (-2)),
 'TC-FN-11': dict(K='[1 ; +∞[', A=(1, fc.subs(x, 1)), E1=']−∞ ; 0] ∪ [2 ; +∞[', E2=']−∞ ; 1]', E3='[1/2 ; +∞['),
 'TC-IN-05': dict(K=7 - 2, A=F(7, 3), E1=7 + 2, E2=-(7 - 2), E3=F(7, 2)),
 'TC-PR-05': dict(K=F(8, 10) ** 2 * F(2, 10), A=1 / F(2, 10), E1=3 * F(2, 10) * F(8, 10) ** 2, E2=F(2, 10) ** 3, E3=F(8, 10) ** 3 * F(2, 10)),
 'TC-PR-06': dict(A=round(0.9 ** 10, 4)),
 'TC-PR-07': dict(K=(100 * F(1, 2), sp.sqrt(100 * F(1, 2) * F(1, 2))), A=(50 - 2 * 5, 50 + 2 * 5), E1=(50, 25), E2=(50, sp.sqrt(50)), E3=(F(1, 2), 5)),
 'TC-PR-08': dict(K=F(5 - 3, 10 - 2), A=F(2 + 10, 2), E1=F(5 - 3, 10), E2=F(1, 10 - 2), E3=F(5 - 3, 10 + 2)),
 'TC-PR-09': dict(K=1 - sp.exp(-sp.Rational(1, 2) * 2), A=1 / sp.Rational(1, 2), E1=sp.exp(-1), E2=sp.Rational(1, 2) * 2, E3=sp.Rational(1, 2) * sp.exp(-1)),
 'TC-ST-05': dict(K=sp.exp(sp.Rational(3, 10) * x + sp.Rational(6, 5)), A=round(math.exp(0.3 * 5 + 1.2), 2), E1=sp.log(sp.Rational(3, 10) * x + sp.Rational(6, 5)),
                  E2=sp.exp(sp.Rational(3, 10) * x) + sp.exp(sp.Rational(6, 5)), E3=sp.Rational(3, 10) * x + sp.Rational(6, 5)),
 'TC-ST-06': dict(K=10 - F(3, 2) * 4, A=F(3, 2) * 10 + (10 - F(3, 2) * 4), E1=10, E2=4 - F(3, 2) * 10, E3=10 - F(3, 2)),
 'TC-LO-01': dict(A=15),
}


def extra():
    out = []
    out.append(('TC-SE-05/A', abs(sum(1000 * 1.03 ** j for j in range(10)) - 11463.88) < 0.006, 'sum of the 10 payments'))
    l = sp.Symbol('l')
    out.append(('TC-SE-06/A', sp.solve(l - (sp.Rational(4, 5) * l + 50), l) == [250], 'fixed point 250'))
    a, b = bisect(g5, 0, 1, 2)
    out.append(('TC-FN-05', (a, b) == (0.5, 0.75) and g5(a) < 0 < g5(b), 'sign change kept'))
    out.append(('TC-FN-06', 3 * 1.05 ** 14 < 6 <= 3 * 1.05 ** 15, 'threshold 15'))
    out.append(('TC-FN-06/A', sp.solve_univariate_inequality(sp.log(x) < -1, x, relational=False) == sp.Interval.open(0, sp.exp(-1)), ']0 ; 1/e['))
    out.append(('TC-FN-07/A', sp.limit((3 * x + 1) / (x - 2), x, 2, '+') == sp.oo, '+∞ at 2⁺'))
    out.append(('TC-FN-08/A', sp.diff(q ** 2 + 2 * q + 36, q).subs(q, 6) == 14, 'marginal cost = average cost = 14'))
    out.append(('TC-FN-10/A', sp.simplify(sp.diff(2 * sp.exp(x / 2) + 4, x) - (sp.Rational(1, 2) * (2 * sp.exp(x / 2) + 4) - 2)) == 0, 'solves y′ = 0.5y − 2'))
    conv = sp.solve_univariate_inequality(sp.diff(fc, x, 2) >= 0, x, relational=False)
    out.append(('TC-FN-11', conv == sp.Interval(1, sp.oo), 'f″ ≥ 0 on [1 ; +∞['))
    out.append(('TC-FN-11/E1', sp.solve_univariate_inequality(sp.diff(fc, x) >= 0, x, relational=False) == sp.Union(sp.Interval(-sp.oo, 0), sp.Interval(2, sp.oo)), 'f′ ≥ 0 set'))
    out.append(('TC-PR-09/A', sp.simplify(sp.solve(sp.exp(-x / 2) - sp.Rational(1, 2), x)[0] - 2 * sp.log(2)) == 0, 'median 2 ln 2'))
    out.append(('TC-LO-01/A', 15 % 5 == 0 and 15 % 10 != 0, '15 is a counterexample'))
    return out
