"""Independent recomputation of MPI v7 values (keys K, open targets A, signatures E1..)."""
from fractions import Fraction as F
import math
import sympy as sp

x, y, n, t, p, X = sp.symbols('x y n t p X')
I, pi, E, oo = sp.I, sp.pi, sp.E, sp.oo
Mx = sp.Matrix


def mstr(M, factor=None):
    body = '[' + ', '.join('[' + ', '.join(str(sp.nsimplify(v)) for v in M.row(i)) + ']' for i in range(M.rows)) + ']'
    return body if factor is None else '(%s)%s' % (factor, body)


def order_mod(a, nmod):
    k = 1
    while (k * a) % nmod != 0:
        k += 1
    return k


A5 = Mx([[2, 1], [1, 2]])
A10 = Mx([[1, 2], [3, 4]])
u = Mx([1, 2]); Pproj = u * u.T / (u.T * u)[0]
G = (sp.Rational(1, 4) + 3 * t / 4) ** 2
Jf = Mx([x * y, x + y ** 2]).jacobian([x, y]).subs({x: 2, y: 1})
Fv = Mx([sp.cos(t), sp.sin(t), t])

CHECKS = {
 'M2-ST-05': dict(K=order_mod(4, 10), A={g for g in range(10) if math.gcd(g, 10) == 1}, E1=math.gcd(4, 10), E2=10, E3=(-4) % 10),
 'M2-ST-06': dict(K='ℤ/7ℤ', A=pow(3, -1, 11), E1='ℤ/9ℤ', E2='ℤ/8ℤ', E3='ℤ'),
 'M2-ST-07': dict(K=sp.totient(27), A=pow(7, 42, 100), E1=27 - 1, E2=sp.totient(3) ** 3, E3=27 // 3),
 'M2-ST-08': dict(K=sp.gcd(X ** 2 - 1, X ** 2 - 3 * X + 2), A=sp.gcd(X ** 2 - 1, X ** 2 - 3 * X + 2), E1=sp.lcm(X ** 2 - 1, X ** 2 - 3 * X + 2), E2=1, E3=X + 1),
 'M2-RED-05': dict(K=set(A5.eigenvals()), E1={2}, E2=set(sp.solve(X ** 2 - 4 * X - 3, X)), E3={A5.trace(), A5.det()}),
 'M2-RED-07': dict(K=(1 - 3) * (2 - 3) * (4 - 3), A=(1 + 2 + 4, 1 * 2 * 4), E1=1 * 2 * 4 - 3, E2=1 * 2 * 4 - 3 ** 3, E3=(3 - 1) * (3 - 2) * (3 - 4)),
 'M2-RED-08': dict(K=(X - 2) * (X - 5), A=(X - 1) ** 2, E1=(X - 2) ** 2 * (X - 5), E2=X - 2, E3=(X + 2) * (X + 5)),
 'M2-RED-09': dict(A=2),
 'M2-RED-10': dict(K='(A − 5I)/2', A=mstr(A10.inv()), E1='(5I − A)/2', E2='A − 5I', E3='(A + 5I)/2'),
 'M2-RED-11': dict(K='N⁴ = 0', A=next(k for k in range(1, 5) if Mx([[0, 1, 0], [0, 0, 1], [0, 0, 0]]) ** k == sp.zeros(3)),
                   E1='N² = 0', E2='N = 0', E3='N¹⁶ = 0, and no smaller power in general'),
 'M2-EU-05': dict(K='(1/√2)[[1, −1], [1, 1]]', A=sp.atan2(1, 1), E1='[[1, 1], [0, 1]]', E2='[[1, −1], [1, 1]]', E3='(1/2)[[1, −1], [1, 1]]'),
 'M2-EU-06': dict(K=sp.Rational(0 - 1, 2), E1=sp.Rational(0, 2), E2=sp.Rational(0 + 1, 2), E3=0 - 1),
 'M2-EU-07': dict(A=min(Mx([[2, -1], [-1, 2]]).eigenvals())),
 'M2-EU-08': dict(K=mstr(Pproj * 5, '1/5'), A=mstr((2 * Pproj - sp.eye(2)) * 5, '1/5'), E1=mstr(u * u.T), E2=mstr(u * u.T, '1/√5'),
                  E3=mstr((sp.eye(2) - Pproj) * 5, '1/5')),
 'M2-EVN-05': dict(K=(3 + 4 + 1, 4), A=2 * 2, E1=(3 - 4 + 1, 4), E2=(8, 3), E3=(sp.sqrt(9 + 16 + 1), 4)),
 'M2-EVN-06': dict(K='neither open nor closed', E1='closed', E2='open', E3='both open and closed'),
 'M2-EVN-07': dict(K=max(2, 3), A=max(2, 3), E1=2 + 3, E2=2, E3=sp.sqrt(2 ** 2 + 3 ** 2)),
 'M2-EVN-08': dict(K='{(x, y) : x² + y² ≤ 1}', E1='{(x, y) : x² + y² < 1}', E2='{(x, y) : y = x²}', E3='{(1/n ; 0) : n ≥ 1}'),
 'M2-SE-05': dict(K=sp.log(n), A=sp.Rational(2, 3) * n ** sp.Rational(3, 2), E1=1 / n, E2=n, E3=1),
 'M2-SE-06': dict(K=sp.limit((2 ** (n + 1) / sp.factorial(n + 1)) / (2 ** n / sp.factorial(n)), n, oo), A=sp.summation(2 ** n / sp.factorial(n), (n, 0, oo)),
                  E1=2, E2='+∞', E3=1),
 'M2-SE-07': dict(K='Σ_{k≤n} uₖ ~ Σ_{k≤n} vₖ', A=sp.log(n), E1='Σ uₙ converges', E2='Σ_{k≤n} uₖ − Σ_{k≤n} vₖ → 0', E3='nothing can be said'),
 'M2-SF-05': dict(K=sp.limit(n * F(1, 3) / (1 + n ** 2 * F(1, 9)), n, oo), A=(n * x / (1 + n ** 2 * x ** 2)).subs(x, 1 / n), E1=F(1, 2), E2='+∞', E3=1 / x),
 'M2-SF-06': dict(K=1 / n, E1=1, E2=0, E3=sp.sin(n) / n),
 'M2-SF-07': dict(K=sp.exp(-n * sp.Symbol('a')), E1=0, E2=1, E3=sp.exp(-sp.Symbol('a'))),
 'M2-SF-08': dict(K=(0, 1), E1=(1, 1), E2=(0, 0), E3=(1, 0)),  # inner limits checked in extra()
 'M2-SEN-05': dict(K=1 / sp.limit(((n + 1) ** 2 / 3 ** (n + 1)) / (n ** 2 / 3 ** n), n, oo), A='+∞', E1=sp.Rational(1, 3), E2=1, E3='+∞'),
 'M2-SEN-06': dict(K='Σ_{n≥1} (−1)^(n+1) xⁿ/n', E1='Σ_{n≥1} xⁿ/n', E2='Σ_{n≥1} (−1)^(n+1) xⁿ/n!', E3='Σ_{n≥1} (−1)ⁿ xⁿ/n'),
 'M2-SEN-07': dict(K=sp.simplify(x * sp.diff(x * sp.diff(1 / (1 - x), x), x)), A=sp.summation(n ** 2 / 2 ** n, (n, 1, oo)), E1=x / (1 - x) ** 2,
                   E2=(1 + x) / (1 - x) ** 3, E3=x * (1 + x) / (1 - x) ** 2),
 'M2-SEN-08': dict(K='at least 2', A=1 / (1 - x) ** 2, E1='exactly 2', E2='6', E3='3'),
 'M2-FV-05': dict(K='2⟨F(t), F′(t)⟩', E1='⟨F(t), F′(t)⟩', E2='2‖F(t)‖‖F′(t)‖', E3='‖F′(t)‖²'),
 'M2-FV-06': dict(K=sp.simplify(sp.sqrt(sum(c ** 2 for c in Fv.diff(t)))), A=sp.integrate(sp.sqrt(2), (t, 0, 2 * pi)), E1=1, E2=2, E3=sp.sqrt(1 + t ** 2)),
 'M2-IN-05': dict(K='α < 1', A=sp.integrate(sp.log(t), (t, 0, 1)), E1='α > 1', E2='α ≤ 1', E3='α > 0'),
 'M2-IN-07': dict(K=sp.integrate(t ** 2 * sp.exp(-t), (t, 0, oo)), E1=sp.integrate(t * sp.exp(-t), (t, 0, oo)), E2='diverges', E3=sp.factorial(3)),
 'M2-IN-08': dict(K=sp.integrate(sp.diff(sp.exp(-x * t ** 2), x).subs(x, 0), (t, 0, 1)), E1=0, E2=-sp.integrate(sp.diff(sp.exp(-x * t ** 2), x).subs(x, 0), (t, 0, 1)),
                  E3=sp.integrate(sp.exp(-0 * t ** 2), (t, 0, 1))),
 'M2-PR-05': dict(K=(1 - p) ** n, E1=p ** n, E2=(1 - p) ** (n - 1), E3=1 - (1 - p) ** n),
 'M2-PR-06': dict(K=sp.exp(-5), A=(5, 5), E1=sp.exp(-6), E2=sp.exp(-2) + sp.exp(-3), E3=5 * sp.exp(-5)),
 'M2-PR-07': dict(K=sp.diff(G, t).subs(t, 1), A=sp.diff(G, t, 2).subs(t, 1) + sp.diff(G, t).subs(t, 1) - sp.diff(G, t).subs(t, 1) ** 2, E1=G.subs(t, 1),
                  E2=sp.diff(G, t, 2).subs(t, 1), E3=sp.diff(G, t).subs(t, 0)),
 'M2-PR-08': dict(K='ℚ', E1='ℝ, because ℚ is dense in ℝ', E2='the set of subsets of ℕ', E3='[0 ; 1]'),
 'M2-ED-05': dict(K='[[1, t], [0, 1]]', E1='[[1, e^t], [1, 1]]', E2='[[1, 0], [0, 1]]', E3='[[0, t], [0, 0]]'),
 'M2-ED-06': dict(K=sp.simplify(Mx([[sp.cos(t), sp.sin(t)], [-sp.sin(t), sp.cos(t)]]).det()), A=sp.cos(t) * sp.log(sp.cos(t)) + t * sp.sin(t),
                  E1=0, E2=sp.cos(t) ** 2 - sp.sin(t) ** 2, E3=2 * sp.cos(t) * sp.sin(t)),
 'M2-CD-05': dict(K=mstr(Jf), A=tuple(Jf * Mx([1, -1])), E1=mstr(Jf.T), E2=mstr(Mx([[2, 1], [1, 2]])), E3=mstr(Mx([[1, 2], [1, 1]]))),
}


def extra():
    out = []
    out.append(('M2-ST-06', sp.isprime(7) and not sp.isprime(9) and not sp.isprime(8), 'ℤ/nℤ is a field iff n is prime'))
    out.append(('M2-RED-05/A', A5 * Mx([1, -1]) == Mx([1, -1]) and A5 * Mx([1, 1]) == 3 * Mx([1, 1]), 'eigenvectors'))
    Ar = Mx([[1, 0, 0], [0, 2, 1], [0, 0, 2]])
    out.append(('M2-RED-06', (Ar - 2 * sp.eye(3)).nullspace().__len__() == 1 and not Ar.is_diagonalizable(), 'dim E₂ = 1'))
    out.append(('M2-RED-06/A', all(Mx([[1, a], [0, 2]]).is_diagonalizable() for a in [-3, 0, 1, 5]), 'always diagonalisable'))
    out.append(('M2-RED-08/A', (Mx([[1, 1], [0, 1]]) - sp.eye(2)) != sp.zeros(2) and (Mx([[1, 1], [0, 1]]) - sp.eye(2)) ** 2 == sp.zeros(2), 'minimal (X − 1)²'))
    out.append(('M2-RED-09', sp.factor(X ** 3 - X) == X * (X - 1) * (X + 1), 'X³ − X has simple roots'))
    out.append(('M2-RED-10', A10 ** 2 - 5 * A10 - 2 * sp.eye(2) == sp.zeros(2) and (A10 - 5 * sp.eye(2)) / 2 == A10.inv(), 'Cayley–Hamilton inverse'))
    Q = Mx([[1, -1], [1, 1]]) / sp.sqrt(2)
    out.append(('M2-EU-05', Q.T * Q == sp.eye(2) and Mx([[1, 1], [0, 1]]).det() == 1 and (Mx([[1, 1], [0, 1]]).T * Mx([[1, 1], [0, 1]])) != sp.eye(2), 'Q orthogonal; det 1 not sufficient'))
    R = Mx([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    out.append(('M2-EU-06/A', R * Mx([1, 1, 1]) == Mx([1, 1, 1]) and R.trace() == 0, 'axis (1, 1, 1), trace 0'))
    out.append(('M2-EU-07', set(Mx([[2, -1], [-1, 2]]).eigenvals()) == {1, 3}, 'eigenvalues 1 and 3'))
    out.append(('M2-SE-06/A', sp.simplify(sp.summation(2 ** n / sp.factorial(n), (n, 0, oo)) - E ** 2) == 0, 'e²'))
    out.append(('M2-SF-05/A', sp.maximum(5 * x / (1 + 25 * x ** 2), x, sp.Interval(0, 1)) == sp.Rational(1, 2), 'sup 1/2 (n = 5)'))
    out.append(('M2-SF-08', sp.limit(sp.Rational(999, 1000) ** n, n, oo) == 0 and all(sp.limit(x ** k, x, 1) == 1 for k in (1, 10, 1000)), 'lim_n xⁿ = 0 on [0 ; 1[, lim_{x→1} xⁿ = 1'))
    out.append(('M2-ED-05', sp.exp(t * Mx([[0, 1], [0, 0]])) == Mx([[1, t], [0, 1]]) or (sp.eye(2) + t * Mx([[0, 1], [0, 0]])) == Mx([[1, t], [0, 1]]), 'I + tN'))
    yp = sp.cos(t) * sp.log(sp.cos(t)) + t * sp.sin(t)
    out.append(('M2-ED-06/A', sp.simplify(sp.diff(yp, t, 2) + yp - 1 / sp.cos(t)) == 0, 'particular solution checked'))
    H = sp.hessian(x ** 2 + 4 * x * y + y ** 2, (x, y))
    out.append(('M2-CD-06', H.det() == -12, 'det H < 0: saddle'))
    out.append(('M2-PR-08/A', len({2 ** a * (2 * b + 1) - 1 for a in range(8) for b in range(40)}) == 8 * 40, 'pairing injective on a sample'))
    return out
