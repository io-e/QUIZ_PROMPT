"""Independent recomputation of MP2I v7 values (keys K, open targets A, signatures E1..)."""
from fractions import Fraction as F
import math
import sympy as sp

x, y, n, t, k, m, X = sp.symbols('x y n t k m X')
A_, B_, C_ = sp.symbols('A B C')
I, pi, E, oo = sp.I, sp.pi, sp.E, sp.oo
Mx = sp.Matrix


def mstr(M):
    return '[' + ', '.join('[' + ', '.join(str(sp.nsimplify(v)) for v in M.row(i)) + ']' for i in range(M.rows)) + ']'


def cplx(v):
    return sp.nsimplify(sp.expand(v))


def inversions(s):
    return sum(1 for i in range(len(s)) for j in range(i + 1, len(s)) if s[i] > s[j])


def v_p(nn, p):
    c = 0
    while nn % p == 0:
        nn //= p
        c += 1
    return c


joint = {(0, 0): F(1, 10), (0, 1): F(3, 10), (1, 0): F(2, 10), (1, 1): F(4, 10)}
EX = sum(p * a for (a, b), p in joint.items()); EY = sum(p * b for (a, b), p in joint.items())
EXY = sum(p * a * b for (a, b), p in joint.items())
Af = Mx([[2, 3], [1, -1]]); Pb = Mx([[1, 1], [1, -1]])
u1, u2 = Mx([1, 1, 0]), Mx([1, 0, 1])
e1 = u1 / u1.norm(); w2 = u2 - (u2.dot(e1)) * e1; e2 = w2 / w2.norm()
sq = lambda v: sp.sqrt(v)
P7 = X ** 4 - 2 * X ** 3 + 2 * X - 1
f_f2 = x * sp.exp(y) + y ** 2
g_f2 = x ** 2 + x * y + y ** 2 - 3 * x
crit = sp.solve([sp.diff(g_f2, x), sp.diff(g_f2, y)], [x, y])

CHECKS = {
 'M1-LO-05': dict(K='[−2 ; −1] ∪ [1 ; 2]', E1='[1 ; 2]', E2='[1 ; 16]', E3='[1/4 ; 1]'),
 'M1-LO-07': dict(K='n = 0 and n = 1', A=sp.expand(3 * (2 ** (n + 1) + 1) - 2 * (2 ** n + 1)), E1='n = 0 only', E2='n = 1 and n = 2', E3='n = 2, computed from the recurrence'),
 'M1-CA-05': dict(K=sp.log(n + 1), E1=sp.log((n + 1) / n), E2=n * sp.log(2), E3=sp.log(n)),
 'M1-CA-06': dict(K=sp.summation(sp.summation(1, (sp.Symbol('i'), 1, sp.Symbol('j') - 1)), (sp.Symbol('j'), 1, n)),
                  A=sp.factor(sp.summation(sp.summation(sp.Symbol('i'), (sp.Symbol('i'), 1, sp.Symbol('j'))), (sp.Symbol('j'), 1, n))),
                  E1=n * (n + 1) / 2, E2=n ** 2, E3=n - 1),
 'M1-CA-07': dict(K='[−1 ; 4]', A=(math.floor(-2.5), math.floor(2.5)), E1=']−∞ ; 4]', E2=']−∞ ; −1] ∪ [4 ; +∞[', E3='[−2 ; 8]'),
 'M1-CX-05': dict(K=set(sp.solve(x ** 2 - (3 + 4 * I), x)), A=set(sp.solve(x ** 2 - 3 * x + 3 - I, x)), E1={sq(3) + 2 * I, -sq(3) - 2 * I}, E2={2 - I, -2 + I},
                  E3={sq(5), -sq(5)}),
 'M1-CX-06': dict(K=2 * sp.cos(t - pi / 3), A=set(sp.solveset(sp.cos(t) + sq(3) * sp.sin(t) - 1, t, sp.Interval.Ropen(0, 2 * pi))),
                  E1=(1 + sq(3)) * sp.cos(t - pi / 3), E2=2 * sp.cos(t - pi / 6), E3=2 * sp.cos(t + pi / 3)),
 'M1-CX-07': dict(K='iπ + 2ikπ, k ∈ ℤ', E1='iπ only', E2='π + 2kπ, k ∈ ℤ', E3='no solution, because eˣ > 0'),
 'M1-CX-08': dict(K=sp.solve(x - ((1 + I) * x + 1), x)[0], A=(sp.Abs(1 + I), sp.arg(1 + I)), E1=-sp.solve(x - ((1 + I) * x + 1), x)[0],
                  E2=cplx(-1 / (1 + I)), E3=1),
 'M1-TA-05': dict(K=sp.diff(sp.atan(2 * x), x), A=sp.simplify(sp.atan(3) + sp.atan(sp.Rational(1, 3))), E1=1 / (1 + 4 * x ** 2), E2=2 / (1 + 2 * x ** 2), E3=2 / (1 - 4 * x ** 2)),
 'M1-TA-06': dict(K=(sp.diff(sp.sinh(x), x), sp.diff(sp.cosh(x), x)), A=set(sp.solve(sp.cosh(x) - 2, x)), E1=(sp.cosh(x), -sp.sinh(x)), E2=(sp.sinh(x), sp.cosh(x)),
                  E3=(-sp.cosh(x), sp.sinh(x))),
 'M1-TA-07': dict(K=sp.integrate(x / (1 + x ** 2), (x, 0, 1)), A=sp.integrate(sp.sin(x) * sp.cos(x) ** 2, (x, 0, pi / 2)), E1=sp.log(2), E2=pi / 4,
                  E3=sp.integrate(x, (x, 0, 1)) * sp.integrate(1 / (1 + x ** 2), (x, 0, 1))),
 'M1-TA-08': dict(K=A_ * sp.exp(x) + B_ * sp.exp(2 * x), A=C_ * sp.exp(-x) + x - 1, E1=A_ * sp.exp(-x) + B_ * sp.exp(-2 * x), E2=A_ * sp.exp(2 * x),
                  E3=A_ * sp.exp(3 * x) + B_ * sp.exp(2 * x)),
 'M1-SU-06': dict(K=A_ * 2 ** n + B_ * 3 ** n, A=3 ** n - 2 ** n, E1=A_ * (-2) ** n + B_ * (-3) ** n, E2=A_ + B_ * (-6) ** n, E3=A_ * 5 ** n + B_ * 6 ** n),
 'M1-SU-07': dict(K=max((-1) ** j + F(1, j) for j in range(1, 200)), A=-1, E1=1, E2=(-1) ** 1 + 1, E3=1 + 1),
 'M1-SU-08': dict(K=0, A='+∞', E1=1, E2='+∞', E3=F(1, 2) ** 2),
 'M1-LC-05': dict(K=sp.limit(sp.sin(x) / x, x, 0), A=sp.limit(x * sp.log(x), x, 0, '+'), E1=sp.sin(0), E2='not extendable', E3='+∞'),
 'M1-LC-06': dict(K=1 + 3 * 2, E1=3 * 2, E2=1 + 3, E3=3 * 2 ** 2),
 'M1-LC-07': dict(K=1 / sp.diff(x ** 3 + x, x).subs(x, 1), A=sp.diff(sp.asin(x), x).subs(x, sp.Rational(1, 2)), E1=1 / sp.diff(x ** 3 + x, x).subs(x, 2),
                  E2=sp.diff(x ** 3 + x, x).subs(x, 1), E3=F(1, 2)),
 'M1-AA-05': dict(K=sp.series(sp.sqrt(1 + x), x, 0, 3).removeO(), A=sp.limit((sp.sqrt(1 + x) - 1 - x / 2) / x ** 2, x, 0), E1=1 + x / 2 - x ** 2 / 4,
                  E2=1 + x / 2 + x ** 2 / 8, E3=1 + x),
 'M1-AA-06': dict(K=sp.limit((sp.log(1 + 1 / n) - 1 / n) * n ** 2, n, oo) / n ** 2, A=sp.limit((sp.sin(1 / n) - sp.tan(1 / n)) * n ** 3, n, oo) / n ** 3,
                  E1=0, E2=1 / (2 * n ** 2), E3=-1 / n ** 2),
 'M1-AR-05': dict(K=v_p(math.factorial(10), 2), A=v_p(math.factorial(100), 5), E1=10 // 2, E2=v_p(10, 2), E3=10 // 2 + 10 // 4),
 'M1-AR-06': dict(K=pow(7, -1, 26), A=(pow(7, -1, 26) * 3) % 26, E1=(-7) % 26, E2='no inverse', E3=(1 - 7 * pow(7, -1, 26)) // 26),
 'M1-ST-05': dict(K='3ℤ', E1='ℕ', E2='the odd integers', E3='{0 ; 1}'),
 'M1-ST-06': dict(A={-1, 1}),
 'M1-PO-05': dict(K=(2, 5), A=2 ** 2 - 2 * 3, E1=(-2, -5), E2=(2, -5), E3=(2, 3)),
 'M1-PO-06': dict(K=sp.interpolate([(0, 1), (1, 2), (2, 5)], X), A=sp.expand((X - 1) * (X - 2) / ((0 - 1) * (0 - 2))), E1=X + 1, E2=-X ** 2 + 2 * X + 1,
                  E3=5 * X ** 2 + 2 * X + 1),
 'M1-PO-07': dict(K=sp.roots(sp.Poly(P7, X))[1], A=sp.factor(P7), E1=1, E2=2, E3=4),
 'M1-AL-05': dict(K='BᵀAᵀ', E1='AᵀBᵀ', E2='AB', E3='BA'),
 'M1-AL-06': dict(K=mstr(Mx([[1, 2], [0, 1]]).inv()), A='[[1, 2n], [0, 1]]', E1='[[1, 1/2], [0, 1]]', E2=mstr(Mx([[1, 2], [0, 1]]).T), E3=mstr(Mx([[1, 2], [0, 1]]))),
 'M1-AL-07': dict(K=sp.solve(Mx([[1, 1], [1, m]]).det(), m)[0], A=tuple(sp.simplify(v) for v in Mx([[1, 1], [1, m]]).inv() * Mx([1, 2])), E1=0, E2=2, E3='no value'),
 'M1-AL-09': dict(A=Mx([[1, 2, 3], [2, 4, 6], [1, 0, 1]]).rank()),
 'M1-AL-10': dict(K=(2 - Mx([[1, -1], [2, -2]]).rank(), Mx([[1, -1], [2, -2]]).rank()), E1=(0, 2), E2=(1, 2), E3=(2, 0)),
 'M1-AL-11': dict(K=set(sp.solve(m ** 2 - m, m)), E1={1}, E2={-1, 1}, E3={0}),
 'M1-AL-12': dict(K=4 - 1, E1=1, E2=4, E3=0),
 'M1-AL-13': dict(K=mstr(Af), A=mstr(Pb.inv() * Af * Pb), E1=mstr(Af.T), E2=mstr(Mx([[3, 2], [-1, 1]])), E3=mstr(Mx([[2, 3], [1, 1]]))),
 'M1-AL-14': dict(A=(Mx([[1, 2], [3, 4]]) * Mx([[0, 1], [1, 0]])).trace()),
 'M1-DT-05': dict(K=inversions((3, 1, 4, 2)), A=(-1) ** inversions((3, 1, 4, 2)), E1=2 * inversions((3, 1, 4, 2)),
                  E2=sum(1 for i in range(3) if (3, 1, 4, 2)[i] > (3, 1, 4, 2)[i + 1]), E3=sum(1 for i, v in enumerate((3, 1, 4, 2), 1) if v != i)),
 'M1-DT-06': dict(K=2 ** 3 * 5, A=(F(1, 5), 5), E1=2 * 5, E2=2 ** 2 * 5, E3=5 + 2),
 'M1-DT-07': dict(K=Mx([[1, 1, 1], [1, 2, 3], [1, 4, 9]]).det(), A=Mx([[1, 1, 1], [1, 2, 4], [1, 4, 16]]).det(), E1=1 * 2 * 9, E2=-Mx([[1, 1, 1], [1, 2, 3], [1, 4, 9]]).det(),
                  E3=(2 - 1) + (3 - 1) + (3 - 2)),
 'M1-IN-05': dict(K=sp.integrate(1 / (1 + x), (x, 0, 1)), A=sp.integrate(1 / (1 + x ** 2), (x, 0, 1)), E1=1, E2=sp.integrate(1 / (1 + x ** 2), (x, 0, 1)), E3='+∞'),
 'M1-IN-06': dict(K='[2 ; 6]', A=sp.integrate(x ** 3, (x, 0, 2)) / 2, E1='[1 ; 3]', E2='[0 ; 6]', E3='[2 ; 3]'),
 'M1-IN-07': dict(K=2 * sp.exp((2 * x) ** 2) - sp.exp(x ** 2), A=(2 * sp.exp((2 * x) ** 2) - sp.exp(x ** 2)).subs(x, 0), E1=sp.exp(4 * x ** 2) - sp.exp(x ** 2),
                  E2=2 * sp.exp(4 * x ** 2), E3=sp.exp(x ** 2)),
 'M1-IN-08': dict(K=sp.exp(sp.Rational(1, 2)) * sp.Rational(1, 2) ** 2 / 2, A=F(1, 10) ** 3 / 6, E1=sp.exp(sp.Rational(1, 2)) * sp.Rational(1, 2) ** 2,
                  E2=sp.Rational(1, 2) ** 2 / 2, E3=sp.exp(sp.Rational(1, 2)) / 2),
 'M1-PR-05': dict(K=math.factorial(11) // (math.factorial(4) ** 2 * 2), A=math.factorial(6) // (math.factorial(3) * math.factorial(2)),
                  E1=math.factorial(11), E2=math.factorial(11) // math.factorial(4), E3=1 * 4 * 4 * 2),
 'M1-PR-06': dict(K=5 * 4 * 3, A=2 ** 3 - 2, E1=5 ** 3, E2=sp.binomial(5, 3), E3=3 ** 5),
 'M1-PR-07': dict(K=(F(1, 100) * F(95, 100)) / (F(1, 100) * F(95, 100) + F(99, 100) * F(5, 100)),
                  A=(F(99, 100) * F(95, 100)) / (F(99, 100) * F(95, 100) + F(1, 100) * F(5, 100)), E1=F(95, 100), E2=F(1, 100) * F(95, 100), E3=1),
 'M1-PR-08': dict(K=joint[(0, 1)] + joint[(1, 1)], E1=joint[(1, 1)], E2=joint[(1, 1)] / (joint[(1, 0)] + joint[(1, 1)]), E3=joint[(1, 0)] + joint[(1, 1)]),
 'M1-PR-09': dict(K=EXY - EX * EY, A=EX * (1 - EX) + EY * (1 - EY) + 2 * (EXY - EX * EY), E1=EXY, E2=EX * EY, E3=-(EXY - EX * EY)),
 'M1-PR-10': dict(K=F(2, 10), A=F(1, 9), E1=2 * 10, E2=1 - F(2, 10), E3=F(2, 100)),
 'M1-EU-05': dict(K=Mx([1, 2, 2]).norm() * Mx([3, 0, 4]).norm(), A=Mx([1, 2, 2]).norm(), E1=Mx([1, 2, 2]).norm() ** 2 * Mx([3, 0, 4]).norm() ** 2,
                  E2=Mx([1, 2, 2]).norm() + Mx([3, 0, 4]).norm(), E3=Mx([1, 2, 2]).dot(Mx([3, 0, 4]))),
 'M1-EU-06': dict(K=tuple(e2), A=tuple(Mx([0, 0, 1]).dot(e1) * e1 + Mx([0, 0, 1]).dot(e2) * e2), E1=tuple((u2 - u2.dot(u1) * u1) / (u2 - u2.dot(u1) * u1).norm()),
                  E2=tuple(w2), E3=tuple(u2 / u2.norm())),
 'M1-SN-07': dict(K=sp.summation(1 / (n * (n + 2)), (n, 1, oo)), A=sp.log(sp.limit(sp.product((n - 1) * (n + 1) / n ** 2, (n, 2, sp.Symbol('N'))), sp.Symbol('N'), oo)),
                  E1=F(1, 2), E2=F(3, 2), E3=F(1, 2) * (1 - F(1, 2))),
 'M1-F2-05': dict(K=(sp.diff(f_f2, x).subs({x: 2, y: 0}), sp.diff(f_f2, y).subs({x: 2, y: 0})),
                  A=sp.diff(f_f2, x).subs({x: 2, y: 0}) * F(3, 5) + sp.diff(f_f2, y).subs({x: 2, y: 0}) * F(4, 5), E1=(1, 0), E2=(2, 1), E3=(1, (sp.exp(y) + 2 * y).subs(y, 0))),
 'M1-F2-06': dict(K=3 * 2 * 1 + 2 * 3 * 1 ** 2, E1=3 + 2, E2=3 * 3 + 2 * 2, E3=3 * 2),
 'M1-F2-07': dict(K=(crit[x], crit[y]), E1=(-crit[x], -crit[y]), E2=(F(3, 2), -F(3, 4)), E3=(F(3, 2), 0)),
}


def extra():
    out = []
    out.append(('M1-LO-05', sp.solve_univariate_inequality(x ** 2 >= 1, x, relational=False).intersect(sp.solve_univariate_inequality(x ** 2 <= 4, x, relational=False)) == sp.Union(sp.Interval(-2, -1), sp.Interval(1, 2)), 'preimage'))
    u_ = [2, 3]
    for _ in range(10):
        u_.append(3 * u_[-1] - 2 * u_[-2])
    out.append(('M1-LO-07', all(u_[j] == 2 ** j + 1 for j in range(len(u_))), 'uₙ = 2ⁿ + 1'))
    out.append(('M1-CA-05/A', all(sum(j * math.factorial(j) for j in range(1, N + 1)) == math.factorial(N + 1) - 1 for N in range(1, 12)), 'Σ k·k! = (n + 1)! − 1'))
    out.append(('M1-CA-05', all(abs(sum(math.log((j + 1) / j) for j in range(1, N + 1)) - math.log(N + 1)) < 1e-12 for N in range(1, 30)), 'telescoping'))
    out.append(('M1-CA-07', sp.solve_univariate_inequality(sp.Abs(2 * x - 3) <= 5, x, relational=False) == sp.Interval(-1, 4), '[−1 ; 4]'))
    out.append(('M1-CX-07', sp.exp(I * pi) == -1 and sp.exp(I * pi + 2 * I * pi) == -1, 'e^(iπ) = −1, period 2iπ'))
    zA = sp.log(sp.sqrt(2)) + I * pi / 4
    out.append(('M1-CX-07/A', abs(complex(sp.N(sp.exp(zA) - (1 + I)))) < 1e-12, 'e^z = 1 + i'))
    out.append(('M1-LC-08', all(math.log((a + b) / 2) >= (math.log(a) + math.log(b)) / 2 for a in [0.1, 1, 3, 10] for b in [0.5, 2, 7]), 'concavity inequality'))
    out.append(('M1-SU-05', all((1 - 1 / j) < (1 - 1 / (j + 1)) and (1 + 1 / j ** 2) > (1 + 1 / (j + 1) ** 2) for j in range(1, 100)), 'monotonicity'))
    out.append(('M1-SU-07/A', all((-1) ** j + 1 / j > -1 for j in range(1, 500)), 'inf −1 not attained'))
    out.append(('M1-ST-06', Mx([[0, 1], [0, 0]]) ** 2 == sp.zeros(2), 'nilpotent example'))
    out.append(('M1-AL-08/A', Mx([[1, 2, -1]]) * Mx([1, 0, 1]) == Mx([0]) and Mx([[1, 2, -1]]) * Mx([0, 1, 2]) == Mx([0]), 'basis vectors in F'))
    out.append(('M1-AL-10/A', Mx([[1, -1], [2, -2]]) * Mx([1, 1]) == sp.zeros(2, 1), 'kernel (1, 1)'))
    out.append(('M1-AL-12/A', Mx([1, 0, 1]).cross(Mx([0, 1, 1])) == Mx([-1, -1, 1]), 'normal (−1, −1, 1)'))
    out.append(('M1-AL-14', Mx([[1, 2], [0, 3]]).trace() == 4 == Mx([[2, 0], [0, 2]]).trace(), 'same trace, yet not similar'))
    out.append(('M1-SN-06', sp.summation(1 / n ** sp.Rational(3, 2), (n, 1, oo)).is_finite, 'α = 3/2 converges'))
    gq = g_f2.subs({x: 2 + sp.Symbol('h'), y: -1 + sp.Symbol('kk')}) - g_f2.subs({x: 2, y: -1})
    out.append(('M1-F2-07/A', sp.expand(gq - (sp.Symbol('h') ** 2 + sp.Symbol('h') * sp.Symbol('kk') + sp.Symbol('kk') ** 2)) == 0, 'quadratic difference'))
    return out
