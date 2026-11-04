"""Independent recomputation of Première « maths intégré à l'enseignement scientifique » v7 values."""
from fractions import Fraction as F
import math
import sympy as sp

x, h, t = sp.symbols('x h t')


def first(pred, start=0, stop=10 ** 6):
    k = start
    while not pred(k):
        k += 1
        if k > stop:
            raise ValueError('no rank found')
    return k


pts = [(1, 4), (2, 7), (4, 8), (5, 13)]
G = (F(sum(p[0] for p in pts), 4), F(sum(p[1] for p in pts), 4))
fd = 2 * x ** 3 - 5 * x ** 2 + 4 * x - 7
B = -2 * x ** 2 + 40 * x - 150
f11 = -2 * (x + 1) * (x - 4)
d10 = 5 * t ** 2

CHECKS = {
 '1C-AU-05': dict(K=-2 * x + 3, A=sp.solve(-2 * x + 3 - 7)[0], E1=3 * x - 2, E2=2 * x + 3, E3=-x / 2 + 3),
 '1C-AU-06': dict(K=F(3 * 10 ** 4) * 5 / 10 ** 6, A=F(42, 10 ** 6) * 3000000, E1=F(15, 10 ** 24), E2=15 * 10 ** 10, E3=F(8, 100)),
 '1C-SD-05': dict(K=G, A=2 * 7 + (G[1] - 2 * G[0]), E1=(G[1], G[0]), E2=(3, F(7 + 8, 2)), E3=(F(1 + 5, 2), F(4 + 13, 2))),
 '1C-SD-06': dict(K=F(15, 10) * (2023 - 2015) + 20, A=2015 + sp.solve(sp.Rational(3, 2) * x + 20 - 50)[0],
                  E1=F(15, 10) * 2023 + 20, E2=F(15, 10) * 9 + 20, E3=20 * 8 + F(15, 10)),
 '1C-SD-07': dict(K=F(110, 200), A=F(180 - 110, 300 - 200), E1=F(110, 180), E2=F(110, 300), E3=F(180, 300)),
 '1C-SE-05': dict(K=first(lambda k: 500 + 35 * k > 1000), A=first(lambda k: 500 * 1.05 ** k > 1000),
                  E1=math.floor(F(500, 35)), E2=math.ceil(F(1000, 35)), E3=first(lambda k: 500 + 35 * k > 1000) + 1),
 '1C-SE-06': dict(K=(sp.sqrt(sp.Rational(121, 100)) - 1) * 100, A=round((1.5 ** 0.1 - 1) * 100, 2),
                  E1=F(21, 2), E2=21, E3=round(math.sqrt(21), 2)),
 '1C-SE-07': dict(A=round(200 * 1.1 ** 10, 2)),
 '1C-FN-05': dict(K=F(7 - 3, 3 - 1), A=sp.diff(x ** 2, x).subs(x, 1), E1=F(3 - 1, 7 - 3), E2=3, E3=F(7, 3)),
 '1C-FN-06': dict(K=sp.diff(fd, x), A=fd.subs(x, 1), E1=sp.diff(fd, x) - 7, E2=2 * x ** 2 - 5 * x + 4, E3=6 * x ** 3 - 10 * x ** 2 + 4 * x),
 '1C-FN-07': dict(K='[−1 ; 1]', E1='[−2 ; −1] and [1 ; 2]', E2='[−2 ; 1]', E3='[0 ; 1]',
                  A=max((-x ** 3 + 3 * x ** 2).subs(x, v) for v in [-1, 0, 2, 3])),
 '1C-FN-08': dict(K=sp.solve(sp.diff(B, x))[0], A=B.subs(x, sp.solve(sp.diff(B, x))[0]), E1=sp.solve(-2 * x + 40)[0],
                  E2=min(sp.solve(B)), E3=B.subs(x, 10)),
 '1C-FN-09': dict(K=5 + (-3) * (3 - 2), A=3 - (3 ** 2 - 4 * 3) / sp.diff(x ** 2 - 4 * x, x).subs(x, 3),
                  E1=5 + 3 * (3 - 2), E2=-3, E3=5 + (-3) * 3),
 '1C-FN-10': dict(K=sp.diff(d10, t).subs(t, 3), A=sp.simplify((d10.subs(t, 3 + h) - d10.subs(t, 3)) / h),
                  E1=d10.subs(t, 3) / 3, E2=d10.subs(t, 3), E3=(10 * t ** 2).subs(t, 3)),
 '1C-FN-11': dict(K=f11.subs(x, F(-1 + 4, 2)), A=((x - 2) * (x + 6)).subs(x, -2), E1=f11.subs(x, F(-3, 2)), E2=f11.subs(x, 0),
                  E3=((x + 1) * (x - 4)).subs(x, F(3, 2))),
 '1C-FN-12': dict(A=sp.Integer(2) ** sp.Rational(1, 2) * sp.Integer(2) ** sp.Rational(3, 2)),
 '1C-FN-13': dict(K=300 * F(360, 300) ** 3, A=first(lambda k: 300 * 1.2 ** k > 1000), E1=300 + 3 * 60, E2=300 * F(6, 5) ** 2, E3=F(6, 5) ** 3),
 '1C-PR-05': dict(A=F(20, 50)),
 '1C-PR-06': dict(K=1 - F(9, 10) ** 3, A=first(lambda k: 1 - 0.9 ** k > 0.5, start=1), E1=3 * F(1, 10), E2=F(1, 10) ** 3, E3=1 - F(1, 10) ** 3),
 '1C-SD-08': dict(K='=A3*1.05', E1='=A2*1.05', E2='=B2*1.05', E3='=A3*1.06'),
}


def extra():
    out = []
    fdec = sp.solve_univariate_inequality(sp.diff(x ** 3 - 3 * x, x) <= 0, x, relational=False)
    out.append(('1C-FN-07', fdec == sp.Interval(-1, 1), 'f′ ≤ 0 exactly on [−1 ; 1]'))
    wrong = sp.solve_univariate_inequality(3 * x ** 2 - 3 * x <= 0, x, relational=False)
    out.append(('1C-FN-07/E3', wrong == sp.Interval(0, 1), 'with (−3x)′ = −3x, f′ ≤ 0 on [0 ; 1]'))
    out.append(('1C-FN-07/A', sp.expand(sp.diff(-x ** 3 + 3 * x ** 2, x) + 3 * x * (x - 2)) == 0, 'f′ = −3x(x − 2)'))
    out.append(('1C-FN-06/A', sp.diff(fd, x).subs(x, 1) == 0 and fd.subs(x, 1) == -6, 'horizontal tangent y = −6'))
    out.append(('1C-SD-05/A', G[1] - 2 * G[0] == 2, 'line y = 2x + 2 through G'))
    out.append(('1C-SE-05', 500 + 35 * 14 <= 1000 < 500 + 35 * 15, 'threshold 15'))
    out.append(('1C-SE-07', all(abs(b / a - 1.1) < 1e-12 for a, b in zip([200, 220, 242], [220, 242, 266.2])), 'ratio 1.1'))
    out.append(('1C-SE-07/A', 200 + 20 * 10 == 400, 'u(10) = 400'))
    out.append(('1C-FN-12', abs(0.8 ** 2 - 0.64) < 1e-12 and 0.5 ** -2 == 4, '0.8² = 0.64, not 1.6; 0.5^(−2) = 4'))
    out.append(('1C-FN-13/A', 300 * 1.2 ** 6 <= 1000 < 300 * 1.2 ** 7, 'threshold 7'))
    out.append(('1C-PR-05', F(80, 200) * F(50, 200) == F(20, 200), 'P(A)P(B) = P(A ∩ B) = 0.1'))
    out.append(('1C-PR-06/A', 0.9 ** 6 > 0.5 > 0.9 ** 7, 'threshold 7'))
    return out
