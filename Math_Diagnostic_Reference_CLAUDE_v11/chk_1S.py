"""Independent recomputation of Première spécialité v7 values (keys K, open targets A, signatures E1..)."""
from fractions import Fraction as F
from math import exp as fexp
import sympy as sp

x, n, h, t, m, y = sp.symbols('x n h t m y')
pi = sp.pi


def first(pred, start=0, stop=10 ** 6):
    k = start
    while not pred(k):
        k += 1
        if k > stop:
            raise ValueError('no rank found')
    return k


def seq_rec(u0, f, k):
    u = u0
    for _ in range(k):
        u = f(u)
    return u


def euler(h_, steps):
    yv = 1.0
    for _ in range(steps):
        yv = yv + h_ * yv
    return round(yv, 6)


L0 = [5, 8, 2]
L1 = L0 + [7]
L_front = [7] + L0

f_an06 = lambda v: v ** 2 - 3 * v
f_an07 = lambda v: 2 / v
g_ge11 = lambda v: 2 * v ** 2 - 8 * v + 3

CHECKS = {
 '1S-AU-05': dict(K=(1 / F(125, 100) - 1) * 100, A=(F(9, 10) ** 2 - 1) * 100, E1=-25, E2=-F(4, 5) * 100, E3=-(1 / F(125, 100) - 1) * 100),
 '1S-AU-06': dict(K=set(sp.solve((2 * x + 6) * (x - 4))), A=set(sp.solve(x * (x - 2) - 3)), E1={3, -4}, E2={-6, 4}, E3={4}),
 '1S-AU-07': dict(K=sp.expand((x - 3) ** 2 - (x + 1) * (x - 1)), A=sp.expand((n + 1) ** 2 - n ** 2),
                  E1=(x ** 2 - 9) - (x ** 2 - 1), E2=sp.expand((x - 3) ** 2) - x ** 2 - 1, E3=sp.expand((x + 3) ** 2 - (x ** 2 - 1))),
 '1S-AU-08': dict(K=F(-2 - 4, 3 - (-1)), A=F(-3, 2) * x + (4 - F(-3, 2) * (-1)), E1=F(3 - (-1), -2 - 4), E2=F(-2 - 4, 2), E3=-2 - 4),
 '1S-AU-09': dict(K=F(12 + 15 + 9 + 14, 4) + 2, A=F(20 * 11 + 32, 21), E1=F(50, 4), E2=F(50, 4) + 4 * 2, E3=2 * F(50, 4)),
 '1S-AU-10': dict(K=F(30, 60), A=F(30, 80), E1=F(30, 120), E2=F(30, 200), E3=F(120, 200)),
 '1S-AL-06': dict(K=seq_rec(2, lambda u: 3 * u - 1, 3), A=sp.expand(2 * (n + 1) ** 2 - 1 - (2 * n ** 2 - 1)),
                  E1=seq_rec(2, lambda u: 3 * u - 1, 2), E2=3 * 3 - 1, E3=2 * 3 ** 3 - 1),
 '1S-AL-07': dict(K=17 - 5 * F(29 - 17, 3), A=first(lambda k: 1200 + 75 * k > 3000), E1=17 - 5 * 12, E2=17 - 4 * F(12, 3), E3=17 - F(12, 3)),
 '1S-AL-08': dict(K=5 * 3 ** 4, A=round(2000 * 1.03 ** 10, 2), E1=5 + 4 * 3, E2=5 * 3 ** 3, E3=(5 * 3) ** 4),
 '1S-AL-09': dict(K=sum(range(1, 51)), A=sum(7 + 4 * k for k in range(15)), E1=50 * 49 // 2, E2=F(50 ** 2, 2), E3=50 * 51),
 '1S-AL-10': dict(K=round(30 * 1.04 ** 3, 2), A=first(lambda k: 1000 * 1.05 ** k > 1000 + 60 * k, start=1),
                  E1=30 + 3 * F(30 * 4, 100), E2=round(30 * 1.04 ** 4, 2), E3=round(30 * 1.4 ** 3, 2)),
 '1S-AL-11': dict(A=sp.expand((n + 1) ** 2 - 6 * (n + 1) - (n ** 2 - 6 * n))),
 '1S-AL-12': dict(K=sp.limit(1000 * sp.Rational(9, 10) ** n, n, sp.oo), A=first(lambda k: 0.9 ** k < 0.01),
                  E1=F(9, 10), E2='−∞', E3=1000),
 '1S-AL-13': dict(K=(set(sp.solve(x ** 2 - 7 * x + 10)) - {2}).pop(), A=set(sp.solve(x ** 2 - 10 * x + 21)),
                  E1=F(-10, 1) / 2, E2=-7 - 2, E3=10 - 2),
 '1S-AL-14': dict(K=2 * (x + 1) * (x - 3), E1=2 * (x - 1) * (x + 3), E2=(x + 1) * (x - 3), E3=2 * x ** 2 - 4 * x + 6),
 '1S-AL-15': dict(A=set(sp.solve(m ** 2 - 4 * 9, m))),
 '1S-AN-06': dict(K=F(f_an06(4) - f_an06(1), 3), A=F(2 * 3 ** 2 - 2 * 1 ** 2, 2), E1=f_an06(4) - f_an06(1),
                  E2=F(3, f_an06(4) - f_an06(1)), E3=F(f_an06(4) - f_an06(1), 5)),
 '1S-AN-07': dict(K=sp.simplify((f_an07(1 + h) - f_an07(1)) / h),
                  A=sp.diff(2 / x, x).subs(x, 1) * (x - 1) + 2, E1=2 / (1 + h - 1) / h, E2=1, E3=2 / (1 + h)),
 '1S-AN-08': dict(K=3 + F(1, 6) * F(3, 10), A=1 + 5 * F(2, 1000), E1=3 + F(1, 3) * F(3, 10), E2=3 + F(1, 6), E3=3 + F(1, 6) * F(93, 10)),
 '1S-AN-09': dict(K=sp.diff(x ** 4 - 3 * x ** 2 + 1 / x, x), A=sp.simplify(sp.diff((2 * x + 1) / (x - 3), x)),
                  E1=4 * x ** 3 - 6 * x + 1 / x ** 2, E2=x ** 3 - 3 * x + 1 / x ** 2, E3=4 * x ** 3 - 6 * x - 1 / x),
 '1S-AN-10': dict(K=sp.diff((3 * x - 1) * sp.sqrt(x), x), E1=3 / (2 * sp.sqrt(x)), E2=3 * sp.sqrt(x),
                  E3=3 * sp.sqrt(x) + (3 * x - 1) / sp.sqrt(x)),
 '1S-AN-12': dict(K=sp.maximum(x * (10 - x), x, sp.Interval(0, 10)), A=sp.maximum(x * (10 - x), x, sp.Interval(0, 10)),
                  E1=10 ** 2, E2=20, E3=6 * 4),
 '1S-AN-13': dict(K=x ** 3 - (3 * x - 2), E1=x ** 3 + 3 * x - 2, E2=x ** 3 - 3 * x - 2, E3=sp.diff(x ** 3, x) - sp.diff(3 * x - 2, x)),
 '1S-AN-15': dict(K=sp.simplify(sp.exp(2 * x + 1) * sp.exp(-x)), A=sp.solve(3 * x - 2 - (x + 4))[0],
                  E1=sp.exp(sp.expand((2 * x + 1) * (-x))), E2=sp.exp(2 * x + 1 + x), E3=-sp.exp(3 * x + 1)),
 '1S-AN-16': dict(K=sp.diff(5 * sp.exp(-t / 5), t), A=F(first(lambda k: 20 * fexp(-0.5 * k / 10) < 5), 10),
                  E1=5 * sp.exp(-t / 5), E2=sp.exp(-t / 5), E3=5 * (-t / 5) * sp.exp(-t / 5 - 1)),
 '1S-AN-17': dict(K=3 * 2 * pi / 3, A=150 * pi / 180, E1=3 * 120, E2=2 * pi / 3, E3=sp.Rational(1, 2) * 3 ** 2 * 2 * pi / 3),
 '1S-AN-18': dict(K=sp.sin(5 * pi / 6), A=set(sp.solveset(sp.cos(x) + sp.Rational(1, 2), x, sp.Interval.Lopen(-pi, pi))),
                  E1=-sp.sin(5 * pi / 6), E2=sp.cos(pi / 6), E3=sp.cos(5 * pi / 6)),
 '1S-AN-19': dict(K=sp.simplify(sp.cos(x + 2 * pi) - sp.cos(-x)), A=sp.simplify(sp.sin(pi - x) + sp.cos(pi + x) + sp.sin(-x)),
                  E1=sp.cos(x) + sp.cos(x), E2=2 * pi, E3=1),
 '1S-GE-05': dict(K=6 * 2, A=4 * 4 + 0 * 4, E1=6 * (6 - 2), E2=6 + 2, E3=-6 * 2),
 '1S-GE-06': dict(K=9 + 4 + 2 * (-1), E1=9 + 4, E2=(3 + 2) ** 2, E3=9 + 4 + (-1)),
 '1S-GE-07': dict(K=sp.sqrt(25 + 64 - 2 * 5 * 8 * sp.cos(pi / 3)), A=F(16 + 25 - 36, 2 * 4 * 5),
                  E1=sp.sqrt(25 + 64), E2=sp.sqrt(25 + 64 + 2 * 5 * 8 * sp.cos(pi / 3)), E3=sp.sqrt(25 + 64 - 5 * 8 * sp.cos(pi / 3))),
 '1S-GE-09': dict(K=(F(3 * 1 + 1 * 1, 2), F(3 * 1 + 1 * 1, 2)), A=sp.sqrt((3 - 2) ** 2 + (1 - 2) ** 2), E1=(1, 3), E2=(3, 3),
                  E3=(3 * 1 + 1 * 1, 3 * 1 + 1 * 1)),
 '1S-GE-11': dict(K=(2, g_ge11(2)), A=(3, -3 ** 2 + 6 * 3 - 5), E1=(-2, g_ge11(-2)), E2=(4, g_ge11(4)), E3=(2, g_ge11(0))),
 '1S-PS-05': dict(K=F(1, 10) / F(1, 2), A=F(4, 10) * F(1, 4) + F(6, 10) * F(2, 3), E1=F(1, 10) / F(4, 10), E2=F(1, 10), E3=F(4, 10) / F(5, 10)),
 '1S-PS-06': dict(K=F(3, 10) * F(4, 100) + F(7, 10) * F(1, 100), A=(F(3, 10) * F(4, 100)) / (F(3, 10) * F(4, 100) + F(7, 10) * F(1, 100)),
                  E1=F(4, 100) + F(1, 100), E2=(F(4, 100) + F(1, 100)) / 2, E3=F(3, 10) * F(4, 100)),
 '1S-PS-07': dict(K=F(3, 10) + F(5, 10) - F(3, 10) * F(5, 10), E1=F(3, 10) + F(5, 10), E2=F(3, 10) * F(5, 10), E3=F(7, 10) * F(5, 10)),
 '1S-PS-08': dict(K=3 * F(2, 10) * F(8, 10) ** 2, A=1 - F(7, 10) ** 4, E1=F(2, 10) * F(8, 10) ** 2, E2=F(2, 10), E3=3 * F(2, 10)),
 '1S-PS-09': dict(K=(2 * 3 - 5, 2 ** 2 * 2), A=F(1, 10) * 10 - F(9, 10) * 1, E1=(2 * 3 - 5, 2 * 2), E2=(2 * 3 - 5, 2 * 2 - 5), E3=(2 * 3, 2 ** 2 * 2)),
 '1S-PS-10': dict(K=2 * 4 / sp.sqrt(64), A=first(lambda k: k > 0 and 8 / sp.sqrt(k) <= sp.Rational(1, 2), start=1),
                  E1=F(2 * 4, 64), E2=2 * 4, E3=4 / sp.sqrt(64)),
 '1S-AP-05': dict(K=str([k ** 2 for k in range(1, 5)]), A=sum(range(0, 21, 2)), E1=str([k ** 2 for k in range(0, 5)]),
                  E2=str([k ** 2 for k in range(1, 6)]), E3=str([k * 2 for k in range(1, 5)])),
 '1S-AP-06': dict(K='%d %d %d' % (L1[1], L1[-1], len(L1)), A=max([3, -1, 9, 4]), E1='%d %d %d' % (L1[0], L1[-1], len(L1)),
                  E2='%d %d %d' % (L0[1], L0[-1], len(L0)), E3='%d %d %d' % (L_front[1], L_front[-1], len(L_front))),
 '1S-AP-07': dict(K=euler(0.1, 2), A=round(1.01 ** 100, 4), E1=1 + 2 * 0.1, E2=euler(0.1, 1), E3=round(fexp(0.2), 4)),
 '1S-LO-05': dict(K=']1 ; 5[', E1='[−2 ; 7]', E2='[1 ; 5]', E3=']1 ; 5]'),
}


def extra():
    out = []
    b = 4 - F(-3, 2) * (-1)
    out.append(('1S-AU-05/A', abs(1 / 0.81 - 1 - 0.235) < 0.0005, 'recovery +23.5 %'))
    out.append(('1S-AU-08/A', F(-3, 2) * 5 + b == -5, 'C(5 ; −5) on (AB)'))
    out.append(('1S-AL-11', sp.simplify((5 - 3 / (n + 2)) - (5 - 3 / (n + 1)) - 3 / ((n + 1) * (n + 2))) == 0, 'key difference'))
    out.append(('1S-AL-11/A', first(lambda k: 2 * k - 5 > 0) == 3, 'increasing from rank 3'))
    out.append(('1S-AL-14/A', (-(0 - 2) * (0 + 5)) > 0 and sp.expand(2 * (x + 1) * (x - 3)) != 2 * x ** 2 - 4 * x + 6, 'sign between the roots; E3 is a wrong expansion'))
    out.append(('1S-AL-15', (-2) ** 2 - 4 * 3 * 5 == -56 and (-2) ** 2 + 4 * 3 * 5 == 64, 'Δ = −56; sign error gives 64'))
    out.append(('1S-AN-10', sp.simplify(sp.diff((3 * x - 1) * sp.sqrt(x), x) - (9 * x - 1) / (2 * sp.sqrt(x))) == 0, 'simplified derivative'))
    out.append(('1S-AN-11/A', sp.limit(sp.sqrt(h) / h, h, 0, '+') == sp.oo, 'rate of √x at 0'))
    g = x ** 3 - 3 * x + 2
    out.append(('1S-AN-13/A', sp.expand(sp.diff(g, x) - 3 * (x - 1) * (x + 1)) == 0 and g.subs(x, 1) == 0 and g.subs(x, 0) > 0, 'minimum 0 at x = 1'))
    f = x ** 3 - 2 * x
    out.append(('1S-AN-14', sp.expand(f.subs(x, -x) + f) == 0 and sp.expand((x ** 4 - 3 * x ** 2 + 1).subs(x, -x) - (x ** 4 - 3 * x ** 2 + 1)) == 0, 'odd; g even'))
    out.append(('1S-AN-16/A', 20 * fexp(-0.5 * 2.7) > 5 > 20 * fexp(-0.5 * 2.8), 'threshold between 2.7 and 2.8'))
    out.append(('1S-GE-05/A', (4 * (-4) + 0 * 4) == -16, 'AB·BD = −16'))
    mab = (x + 1) * (x - 3) + (y - 2) * (y - 4)
    out.append(('1S-GE-08', sp.expand(mab - ((x - 1) ** 2 + (y - 3) ** 2 - 5)) == 0 and (-1 - 1) ** 2 + (2 - 3) ** 2 == 5, 'circle centre (1 ; 3), r² = 5; A on it'))
    out.append(('1S-GE-10', sp.expand((x - 3) ** 2 + (y + 2) ** 2 - 16 - (x ** 2 + y ** 2 - 6 * x + 4 * y - 3)) == 0 and (7 - 3) ** 2 + (1 + 2) ** 2 > 16, 'centre (3 ; −2), r = 4; P outside'))
    out.append(('1S-GE-11/A', set(sp.solve(-x ** 2 + 6 * x - 5)) == {1, 5}, 'roots 1 and 5'))
    out.append(('1S-PS-09/A', sp.solve(F(1, 10) * x - F(9, 10))[0] == 9, 'fair with a 9 € prize'))
    out.append(('1S-LO-05', sp.Interval.Ropen(-2, 5).intersect(sp.Interval.Lopen(1, 7)) == sp.Interval.open(1, 5), 'intersection ]1 ; 5['))
    out.append(('1S-LO-05/A', sp.Interval(1, 5) == sp.solve_univariate_inequality(sp.Abs(x - 3) <= 2, x, relational=False), '|x − 3| ≤ 2'))
    out.append(('1S-LO-06', all((k * (k + 1)) % 2 == 0 for k in range(-50, 50)), 'n(n + 1) even (sanity)'))
    return out
