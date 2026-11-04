"""Independent recomputation of Terminale spécialité v7 values (keys K, open targets A, signatures E1..)."""
from fractions import Fraction as F
import math
import sympy as sp

x, n, t, s, u, l, m, C = sp.symbols('x n t s u l m C')
pi, E, oo = sp.pi, sp.E, sp.oo
binom, fact = sp.binomial, sp.factorial


def first(pred, start=0, stop=10 ** 6):
    k = start
    while not pred(k):
        k += 1
        if k > stop:
            raise ValueError('no rank found')
    return k


def dot(a, b):
    return sum(p * q for p, q in zip(a, b))


def trapz(f, a, b, k):
    hh = F(b - a, k)
    pts = [a + i * hh for i in range(k + 1)]
    return hh * (F(f(pts[0]) + f(pts[-1]), 2) + sum(f(p) for p in pts[1:-1]))


def lake(n_):
    v = 2000
    for _ in range(n_):
        v = 0.9 * v + 300
    return v


def trace_while(cond, step):
    k, v = 0, 100
    while cond(v):
        v, k = step(v), k + 1
    return k, v


uu, vv, ww = (1, 2, 0), (0, 1, 1), (2, 5, 1)
a1, b1 = sp.symbols('a1 b1')
ab = sp.solve([a1 * p + b1 * q - r for p, q, r in zip(uu, vv, ww)], [a1, b1])
d_pt = lambda tt: (1 + 2 * tt, -1 + tt, 3 - tt)
f27 = x ** 3 - 6 * x ** 2 + 5
binP = lambda k, nn=5, p=F(1, 5): binom(nn, k) * p ** k * (1 - p) ** (nn - k)
seq_list = [1]
for _ in range(4):
    seq_list.append(2 * seq_list[-1] + 1)
seq2 = [1.0]
for _ in range(3):
    seq2.append(0.5 * seq2[-1] + 3)

CHECKS = {
 'TS-AG-05': dict(K=10 ** 4, A=10 ** 4 - 10 * 9 * 8 * 7, E1=10 * 9 * 8 * 7, E2=4 ** 10, E3=10 * 4),
 'TS-AG-06': dict(K=fact(6), A=fact(5) / (fact(2) * fact(2)), E1=sum(range(1, 7)), E2=6 ** 6, E3=fact(5)),
 'TS-AG-07': dict(K=2 ** 5, A=sum(binom(5, k) for k in range(6)), E1=2 ** 5 - 1, E2=5 ** 2, E3=binom(5, 2)),
 'TS-AG-08': dict(K=binom(5, 2) * 4, A=binom(9, 3) - binom(5, 3), E1=binom(5, 2) + 4, E2=5 * 4 * 4, E3=binom(9, 3)),
 'TS-AG-09': dict(K=binom(8, 4), A=binom(10, 2), E1=binom(7, 4) + binom(7, 5), E2=35 * 35, E3=8 * binom(7, 3)),
 'TS-AG-10': dict(K=(ab[a1], ab[b1]), E1=(2, -1), E2=(1, 2), E3=(1, 1)),
 'TS-AG-12': dict(K=dot((2, -1, 3), (1, 4, -2)), A=sp.solve(dot((m, 2, 1), (2, -1, 3)), m)[0], E1=2 - 4 + 6, E2=(2 + 1) + (-1 + 4) + (3 - 2), E3=2 - 4),
 'TS-AG-13': dict(K=sp.sqrt(2 ** 2 + 3 ** 2 + 6 ** 2), E1=2 + 3 + 6, E2=sp.sqrt(2 ** 2 + 3 ** 2), E3=2 ** 2 + 3 ** 2 + 6 ** 2),
 'TS-AG-14': dict(K=(2, 0, -1), E1=(2, -1, 5), E2=(2, 0, 1), E3=(2, 1, -1)),
 'TS-AG-15': dict(K=tuple(2 - F(2 + 2 + 2 - 3, 3) for _ in range(3)), A=sp.Abs(2 + 2 + 2 - 3) / sp.sqrt(3),
                  E1=tuple(2 + F(2 + 2 + 2 - 3, 3) for _ in range(3)), E2=(2, 2, 3 - 2 - 2), E3=tuple(2 - F(6, 3) for _ in range(3))),
 'TS-AG-16': dict(K=d_pt(2), E1=(4, 2, -2), E2=(5, 1, 3), E3=(5, 1, 5)),
 'TS-AG-17': dict(K=(1 + 1, 2 - 1, 3 * 1), E1=(1 - 1, 2 + 1, -3), E2='no intersection point', E3=(1 + 3, 2 - 3, 9)),
 'TS-AG-18': dict(A=tuple(c.subs(t, sp.solve(4 * 2 * t - 2 * (1 - t) + 2 * t + 1, t)[0]) for c in (2 * t, 1 - t, t))),
 'TS-AN-18': dict(A=1),
 'TS-AN-19': dict(K=sp.limit((2 ** n - 5 ** n) / (5 ** n + 3), n, oo), A=sp.limit((1 - sp.Rational(1, 2) ** (n + 1)) / (1 - sp.Rational(1, 2)), n, oo),
                  E1=0, E2=1, E3='−∞'),
 'TS-AN-20': dict(A=2 - 1 / n),
 'TS-AN-21': dict(A=sp.solve(sp.sqrt(2 + x) - x, x)[0]),
 'TS-AN-22': dict(K='+∞', A=sp.limit((2 * x - 1) / (x + 3), x, oo), E1='−∞', E2=0, E3=2 + 1),
 'TS-AN-23': dict(K=sp.limit(x ** 3 * sp.exp(-x), x, oo), A='+∞', E1='+∞', E2='−∞', E3='no limit'),
 'TS-AN-24': dict(K=sp.limit(sp.log(x) / x, x, oo), A=sp.limit(sp.log(x) / sp.sqrt(x), x, oo), E1=1, E2='+∞', E3='no limit'),
 'TS-AN-25': dict(K=sp.diff(sp.exp(x ** 2), x), A=sp.diff((3 * x - 1) ** 5, x), E1=sp.exp(x ** 2), E2=x ** 2 * sp.exp(x ** 2 - 1), E3=sp.exp(2 * x)),
 'TS-AN-26': dict(K=sp.diff(sp.sqrt(x ** 2 + 1), x), A=sp.diff(sp.log(x ** 2 + 1), x), E1=1 / (2 * sp.sqrt(x ** 2 + 1)), E2=1,
                  E3=2 * x / sp.sqrt(x ** 2 + 1)),
 'TS-AN-27': dict(K=sp.solve(sp.diff(f27, x, 2), x)[0], A=sp.solve(sp.diff(x * sp.exp(x), x, 2), x)[0], E1=set(sp.solve(sp.diff(f27, x), x)),
                  E2=sp.solve(6 * x - 6, x)[0], E3=0),
 'TS-AN-29': dict(K=2 ** 2 + 1, A=math.floor(1 - 1 / 10), E1=2, E2='+∞', E3=2 ** 2),
 'TS-AN-30': dict(A=math.floor(10 * sp.nsolve(x ** 3 + x - 3, x, 1.2)) / 10),
 'TS-AN-31': dict(K=sp.solve(l - (l / 2 + 3), l)[0], A=F(1, 2), E1=3, E2=F(3) / F(3, 2), E3=0),
 'TS-AN-32': dict(K=sp.log(12) - sp.log(3) + sp.log(2), A=[r for r in sp.solve(x * (x - 1) - 6, x) if r > 1][0],
                  E1=sp.log(12 - 3) + sp.log(2), E2=sp.log(sp.Rational(12, 3) + 2), E3=sp.log(12) - (sp.log(3) + sp.log(2))),
 'TS-AN-33': dict(K=']1/2 ; 1[', A=first(lambda k: 0.8 ** k < 0.01), E1=']−∞ ; 1[', E2=']−∞ ; 1/2[', E3=']1 ; +∞['),
 'TS-AN-34': dict(K=sp.diff(sp.log(3 * x - 2), x), A=(sp.log(x) / x).subs(x, E), E1=1 / (3 * x - 2), E2=1 / x, E3=3 / (3 * x - 2) ** 2),
 'TS-AN-35': dict(K=sp.diff(sp.cos(3 * x), x), A=set(sp.solveset(sp.sin(x) - sp.sqrt(3) / 2, x, sp.Interval(0, 2 * pi))),
                  E1=3 * sp.sin(3 * x), E2=-sp.sin(3 * x), E3=-3 * sp.sin(x)),
 'TS-AN-36': dict(K=sp.integrate(2 * x * sp.exp(x ** 2), x), A=sp.log(3 * x + 1), E1=sp.diff(2 * x * sp.exp(x ** 2), x),
                  E2=x ** 2 * sp.exp(x ** 2), E3=sp.exp(x ** 3 / 3)),
 'TS-AN-37': dict(K=2 * x ** 3 - 2 * x ** 2 + (3 - (2 * 8 - 2 * 4)), A=sp.exp(2 * x) / 2 + (1 - sp.Rational(1, 2)),
                  E1=2 * x ** 3 - 2 * x ** 2 + 3, E2=6 * x ** 3 - 4 * x ** 2 + (3 - (6 * 8 - 4 * 4)), E3=2 * x ** 3 - 2 * x ** 2),
 'TS-AN-38': dict(K=C * sp.exp(-2 * x) + 3, A=2 * sp.exp(-2 * x) + 3, E1=C * sp.exp(-2 * x) - 3, E2=C * sp.exp(-2 * x) + 6, E3=C * sp.exp(2 * x) + 3),
 'TS-AN-39': dict(K=sp.integrate(3 * x ** 2 + 2 * x, (x, 1, 2)), A=sp.integrate(sp.exp(x) + 1, (x, 0, 1)), E1=-sp.integrate(3 * x ** 2 + 2 * x, (x, 1, 2)),
                  E2=(3 * 4 + 4) - (3 + 2), E3=2 ** 3 + 2 ** 2),
 'TS-AN-40': dict(K=sp.integrate(sp.Abs(x - 1), (x, 0, 2)), A=sp.integrate(x - x ** 2, (x, 0, 1)), E1=sp.integrate(x - 1, (x, 0, 2)),
                  E2=sp.integrate(1 - x, (x, 0, 1)), E3=sp.integrate(x + 1, (x, 0, 2))),
 'TS-AN-41': dict(K=sp.integrate(x ** 2, (x, 0, 3)) / 3, A=sp.integrate(sp.exp(x), (x, 0, 1)), E1=sp.integrate(x ** 2, (x, 0, 3)),
                  E2=F(0 + 9, 2), E3=F(3, 2) ** 2),
 'TS-AN-42': dict(K=sp.integrate(x * sp.sin(x), (x, 0, pi)), A=sp.integrate(sp.log(x), (x, 1, E)), E1=-sp.integrate(x * sp.sin(x), (x, 0, pi)),
                  E2=(-(x ** 2 / 2) * sp.cos(x)).subs(x, pi) - (-(x ** 2 / 2) * sp.cos(x)).subs(x, 0), E3=sp.integrate(sp.cos(x), (x, 0, pi))),
 'TS-AN-43': dict(K=trapz(lambda v: v ** 2, 0, 2, 2), A=trapz(lambda v: v ** 2, 0, 1, 4), E1=F(0 + 1 + 4, 2), E2=0 + 1, E3=0 + 2 * 1 + 4),
 'TS-AN-44': dict(K=sp.Rational(9, 10) * u + 300, A=first(lambda k: lake(k) > 2900), E1=sp.Rational(9, 10) * (u + 300),
                  E2=sp.Rational(1, 10) * u + 300, E3=u - 10 + 300),
 'TS-AN-45': dict(K=sp.limit(4 * sp.Rational(1, 3) ** n + 2, n, oo), A=sp.limit((2 ** n + 3 ** n) / 4 ** n, n, oo), E1=4 * F(1, 3) + 2, E2='+∞', E3=0),
 'TS-PR-05': dict(K=1 - binP(0), A=binP(0) + binP(1) + binP(2), E1=binP(1), E2=1 - binP(5), E3=1 - (binP(0) + binP(1))),
 'TS-PR-06': dict(K=first(lambda k: 1 - 0.95 ** k >= 0.9), A=first(lambda k: 1 - 0.99 ** k >= 0.9), E1=math.floor(math.log(0.1) / math.log(0.95)),
                  E2=math.ceil(F(9, 10) / F(5, 100)), E3=first(lambda k: 1 - 0.05 ** k >= 0.9, start=1)),
 'TS-PR-07': dict(K=2 * 4 - 3 * (-1) + 5, A=2 ** 2 * 2 + 3 ** 2 * 3, E1=2 * 4 - 3 + 5, E2=2 * 4 - 3 * (-1), E3=2 ** 2 * 4 + 3 ** 2 * (-1) + 5),
 'TS-PR-08': dict(K=F(4, 100), A=5, E1=100 * 4, E2=F(2, 100), E3=4),
 'TS-PR-09': dict(K=first(lambda k: F(25, 100) / (k * F(1, 100)) <= F(5, 100), start=1), A=F(25, 100) / (2000 * F(1, 100)),
                  E1=first(lambda k: F(25, 100) / (k * F(1, 10)) <= F(5, 100), start=1),
                  E2=first(lambda k: F(5, 10) / (k * F(1, 100)) <= F(5, 100), start=1),
                  E3=first(lambda k: F(25, 100) / (k * F(1, 100)) <= F(95, 100), start=1)),
 'TS-PR-11': dict(K=0, A=(0, 2 ** 2 * F(10, 4)), E1=F(10, 4) + F(10, 4), E2=F(10, 4), E3=10),
 'TS-LO-05': dict(A=30 - (18 + 12 - 7)),
 'TS-AP-05': dict(K=str(seq_list), A=seq2[-1], E1=str(seq_list[:-1]), E2=str([1, 3, 3, 3, 3]), E3=str([seq_list[-1]])),
 'TS-AP-06': dict(K=trace_while(lambda v: v > 10, lambda v: 0.5 * v)[0], A=first(lambda k: 100 * 0.5 ** k < 1), E1=trace_while(lambda v: v < 10, lambda v: 0.5 * v)[0],
                  E2=trace_while(lambda v: v > 10, lambda v: 0.5 * v)[1], E3=trace_while(lambda v: v > 10, lambda v: 0.5 * v)[0] + 1),
}


def extra():
    out = []
    sys_ = [1 + t - s, 2 * t - (1 + s), 3 - 2 * s]
    out.append(('TS-AG-11', sp.solve(sys_, [t, s]) == [] and sp.Matrix([[1, 2, 0], [1, 1, 2]]).rank() == 2, 'directions independent, no common point'))
    out.append(('TS-AG-11/E2', (1 + sp.Rational(1, 2), 2 * sp.Rational(1, 2), 3) == (sp.Rational(3, 2), 1, 3) and (sp.Rational(3, 2), 1 + sp.Rational(3, 2), 3) != (sp.Rational(3, 2), 1, 3), 'the E2 point is on d only'))
    out.append(('TS-AG-11/A', (2, 4, 0) == tuple(2 * c for c in (1, 2, 0)) and sp.solve([1 + t - 0, 2 * t - 0, 3 - 3], t) == [], 'parallel and distinct'))
    out.append(('TS-AG-10/A', tuple(p + q for p, q in zip(uu, vv)) == (1, 3, 1), 't⃗ = u⃗ + v⃗'))
    A_, B_, C_ = (1, -2, 3), (3, 1, -3), (3, -2, 3)
    AC = tuple(c - a for a, c in zip(A_, C_)); BC = tuple(c - b for b, c in zip(B_, C_))
    out.append(('TS-AG-13/A', dot(AC, BC) == 0, 'right angle at C'))
    on_d = lambda P: len(sp.solve([c - pp for c, pp in zip(d_pt(t), P)], t)) == 1
    out.append(('TS-AG-16', on_d((5, 1, 1)) and not any(on_d(P) for P in [(4, 2, -2), (5, 1, 3), (5, 1, 5)]), 'only the key lies on d'))
    out.append(('TS-AG-17', sp.solve((1 + t) + (2 - t) + 3 * t - 6, t) == [1], 't = 1'))
    out.append(('TS-AG-17/A', dot((1, 1, -2), (1, 1, 1)) == 0 and (0 + 1 + 0 - 6) != 0, 'parallel, not contained'))
    out.append(('TS-AG-18', sp.Matrix([[2, -1, 1], [4, -2, 2]]).rank() == 1, 'u⃗ collinear to n⃗'))
    out.append(('TS-AG-15/E2', 2 + 2 + (-1) - 3 == 0, 'vertical projection lies on P but is not orthogonal'))
    out.append(('TS-AN-18', all(2 - 1 / k <= 2 + math.cos(k) / k <= 2 + 1 / k for k in range(1, 200)), 'squeeze bounds'))
    out.append(('TS-AN-18/A', sp.limit((n - 1) / (n + 2), n, oo) == 1 and sp.limit((n + 1) / (n + 2), n, oo) == 1, 'both bounds tend to 1'))
    out.append(('TS-AN-22', sp.limit((x + 1) / (x - 2), x, 2, '+') == oo, 'right limit +∞'))
    out.append(('TS-AN-23/A', sp.limit(sp.exp(x) - x ** 2, x, oo) == oo, '+∞'))
    out.append(('TS-AN-28', all(math.log(v) <= v - 1 + 1e-15 for v in [0.01, 0.5, 1, 2, 10, 100]), 'ln x ≤ x − 1'))
    out.append(('TS-AN-28/A', sp.diff(x ** 3, x, 2).subs(x, 2) > 0 and sp.expand(3 * (x - 1) + 1 - (3 * x - 2)) == 0, 'convex; tangent at 1 is y = 3x − 2'))
    out.append(('TS-AN-21', all(0 <= v <= 2 for v in [1.0, math.sqrt(3), math.sqrt(2 + math.sqrt(3))]), 'first terms within [0 ; 2]'))
    out.append(('TS-AN-30/A', (1.2 ** 3 + 1.2 - 3) < 0 < (1.3 ** 3 + 1.3 - 3), 'α in ]1.2 ; 1.3['))
    out.append(('TS-AN-31/A', sp.simplify(((sp.Rational(1, 2) * (u) + 3) - 6) - sp.Rational(1, 2) * (u - 6)) == 0, 'vₙ₊₁ = 0.5 vₙ'))
    out.append(('TS-AN-32', abs(float(sp.log(12) - sp.log(3) + sp.log(2) - sp.log(8))) < 1e-12, 'ln 8'))
    out.append(('TS-AN-33', sp.solve_univariate_inequality(sp.log(2 * x - 1) < 0, x, relational=False) == sp.Interval.open(sp.Rational(1, 2), 1), ']1/2 ; 1['))
    out.append(('TS-AN-34/A', sp.solve(sp.diff(sp.log(x) / x, x), x) == [E], 'maximum at e'))
    out.append(('TS-AN-36/A', sp.simplify(sp.diff(sp.log(3 * x + 1), x) - 3 / (3 * x + 1)) == 0, 'primitive checked'))
    out.append(('TS-AN-37', (2 * x ** 3 - 2 * x ** 2 - 5).subs(x, 2) == 3 and sp.expand(sp.diff(2 * x ** 3 - 2 * x ** 2 - 5, x) - (6 * x ** 2 - 4 * x)) == 0, 'F′ = f, F(2) = 3'))
    K38 = C * sp.exp(-2 * x) + 3
    out.append(('TS-AN-38', sp.simplify(sp.diff(K38, x) - (-2 * K38 + 6)) == 0 and (2 * sp.exp(-2 * x) + 3).subs(x, 0) == 5, 'solves the equation; y(0) = 5'))
    out.append(('TS-AN-43/A', trapz(lambda v: v ** 2, 0, 1, 4) > F(1, 3), 'over-estimate'))
    out.append(('TS-AN-44/A', abs(lake(21) - (3000 - 1000 * 0.9 ** 21)) < 1e-6 and lake(21) <= 2900 < lake(22), 'closed form and threshold'))
    out.append(('TS-PR-11', all(h_ + (10 - h_) == 10 for h_ in range(11)), 'X + Y = 10 is constant'))
    return out
