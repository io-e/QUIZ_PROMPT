"""Independent recomputation of Terminale mathématiques expertes v7 values."""
from fractions import Fraction as F
import sympy as sp

I, pi, E = sp.I, sp.pi, sp.E
z, k, th = sp.symbols('z k θ')
Mx = sp.Matrix


def mstr(M):
    return '[' + ', '.join('[' + ', '.join(str(sp.nsimplify(v)) for v in M.row(i)) + ']' for i in range(M.rows)) + ']'


def cplx(v):
    return sp.nsimplify(sp.expand(v))


def euclid(a, b):
    q = a // b
    return (q, a - b * q)


P = (z ** 3 - 3 * z ** 2 + 4 * z - 2)
A7 = Mx([[1, 2], [3, 4]]); B7 = Mx([[0, 1], [1, 0]])
A8 = Mx([[2, 1], [5, 3]])
A9 = Mx([[F(1, 2), 0], [0, F(1, 2)]]); C9 = Mx([1, 2])
K3 = Mx([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
P11 = Mx([[sp.Rational(7, 10), sp.Rational(3, 10)], [sp.Rational(4, 10), sp.Rational(6, 10)]])
P12 = Mx([[sp.Rational(1, 2), sp.Rational(1, 2), 0], [sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(1, 4)], [0, sp.Rational(1, 2), sp.Rational(1, 2)]])
p1, p2, p3 = sp.symbols('p1 p2 p3')
pi12 = sp.solve(list(Mx([[p1, p2, p3]]) * P12 - Mx([[p1, p2, p3]])) + [p1 + p2 + p3 - 1], [p1, p2, p3])
path4 = Mx([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]])

CHECKS = {
 'TE-CX-05': dict(K=cplx((3 + I) / (1 - I)), A=cplx((3 + 4 * I) / (2 - I)), E1=3 / 1 + 1 / (-1), E2=cplx((3 + I) * (1 + I)),
                  E3=cplx((3 + 3 * I + I + 1) / 2)),
 'TE-CX-06': dict(K=cplx((2 - 3 * I) * (2 + 3 * I)), A=(sp.Abs(1 + I * sp.sqrt(3)), sp.arg(1 + I * sp.sqrt(3))), E1=4 - 9,
                  E2=cplx((2 - 3 * I) ** 2), E3=sp.sqrt(13)),
 'TE-CX-07': dict(K=sp.Abs(-2 + 2 * I) * sp.exp(I * sp.arg(-2 + 2 * I)), A=cplx(4 * sp.exp(-I * pi / 3)),
                  E1=2 * sp.sqrt(2) * sp.exp(I * sp.atan(sp.Rational(2, -2))), E2=4 * sp.exp(I * 3 * pi / 4), E3=2 * sp.sqrt(2) * sp.exp(I * pi / 4)),
 'TE-CX-08': dict(K=cplx((1 + I) ** 8), A=next(nn for nn in range(1, 20) if sp.im(cplx((1 + I) ** nn)) == 0 and sp.re(cplx((1 + I) ** nn)) > 0),
                  E1=1 + I ** 8, E2=16 * sp.exp(I * pi / 4), E3=8 * sp.sqrt(2)),
 'TE-CX-09': dict(K=(1 + sp.cos(2 * th)) / 2, A=(3 * sp.sin(th) - sp.sin(3 * th)) / 4, E1=(1 - sp.cos(2 * th)) / 2, E2=sp.cos(2 * th) / 2, E3=sp.cos(2 * th)),
 'TE-CX-10': dict(K=set(sp.solve(z ** 2 - 4 * z + 13, z)), A=sp.Abs(sp.solve(z ** 2 + 2 * z + 5, z)[0]), E1=set(sp.solve(z ** 2 - 4 * z - 5, z)),
                  E2={2 - 6 * I, 2 + 6 * I}, E3={-s for s in sp.solve(z ** 2 - 4 * z + 13, z)}),
 'TE-CX-11': dict(K=sp.div(P, z - 1, z)[0], A=set(sp.solve(P, z)), E1=z ** 2 + 2 * z + 2, E2=z ** 2 - 2 * z - 2, E3=sp.div(P, z + 1, z)[0]),
 'TE-CX-12': dict(K=cplx((3 * I - (1 + I)) / ((3 + 2 * I) - (1 + I))), E1=cplx(((3 + 2 * I) - (1 + I)) / (3 * I - (1 + I))),
                  E2=sp.Rational(-4, 5) + I, E3=sp.Rational(-1, 2) + 2),
 'TE-CX-13': dict(K=set(sp.solve(z ** 4 - 16, z)), A=(2 * sp.sqrt(2)) ** 2, E1={-2, 2}, E2={4},
                  E3={cplx(2 * sp.exp(I * j * pi / 4)) for j in range(4)}),
 'TE-AR-05': dict(K=euclid(-17, 5), A={nn for nn in range(21) if nn % 5 == 3}, E1=(-3, -2), E2=(-(17 // 5), 17 % 5), E3=tuple(reversed(euclid(-17, 5)))),
 'TE-AR-06': dict(K=pow(5, 100, 7), E1=pow(5, 100 % 7, 7), E2=pow(5, 100 % 3, 7), E3=(5 * 100) % 7),
 'TE-AR-07': dict(K=(-2, 7), A=(-2 + 5 * k, 7 - 17 * k), E1=(2, -7), E2=(7, -2), E3=(17 // 5, 5 // (17 % 5))),
 'TE-AR-08': dict(A=(7 * k, 4 * k)),
 'TE-AR-09': dict(K=(2 + 5 * k, -1 - 3 * k), A={xx for xx in range(21) if (1 - 3 * xx) % 5 == 0}, E1=(2 + 3 * k, -1 - 5 * k), E2=(2 + 5 * k, -1 + 3 * k), E3=(2 * k, -k)),
 'TE-AR-10': dict(K=sp.divisor_count(360), A=sp.gcd(1000, 1080), E1=3 * 2 * 1, E2=4 + 3 + 2, E3=len(sp.factorint(360))),
 'TE-AR-11': dict(K=pow(7, 22, 11), E1=pow(7, 22 % 11, 11), E2=7 ** 2, E3=22 % 10),
 'TE-GM-05': dict(K=F(3 + 3 + 2 + 2 + 2 + 4, 2), E1=3 + 3 + 2 + 2 + 2 + 4, E2=6, E3=F(16, 6)),
 'TE-GM-06': dict(K=sp.binomial(6, 2), A=(7, 6), E1=6 ** 2, E2=6 * 5, E3=5),
 'TE-GM-07': dict(K=mstr(A7 * B7), E1=mstr(B7 * A7), E2=mstr(A7.multiply_elementwise(B7)), E3=mstr(A7.T * B7)),
 'TE-GM-08': dict(K=mstr(A8.inv()), A=tuple(A8.inv() * Mx([4, 11])), E1=mstr(Mx([[2, -1], [-5, 3]])), E2=mstr(-A8),
                  E3=mstr(A8.applyfunc(lambda v: sp.Rational(1, v)))),
 'TE-GM-09': dict(K=tuple((sp.eye(2) - A9).inv() * C9), A=tuple((sp.eye(2) - A9).inv() * C9), E1=tuple(C9), E2=tuple((sp.eye(2) + A9).inv() * C9),
                  E3=tuple(A9 * C9 + C9)),
 'TE-GM-10': dict(K=(K3 ** 3)[0, 1], A=(path4 ** 2)[0, 2], E1=(K3 ** 2)[0, 1], E2=(K3 ** 3)[0, 0], E3=(K3 ** 4)[0, 1]),
 'TE-GM-11': dict(K='[[0.7, 0.3], [0.4, 0.6]]', A=(P11 ** 2)[0, 0], E1='[[0.7, 0.4], [0.3, 0.6]]', E2='[[0.3, 0.7], [0.6, 0.4]]', E3='[[0.4, 0.6], [0.7, 0.3]]'),
 'TE-GM-12': dict(K=(pi12[p1], pi12[p2], pi12[p3]), A=tuple(Mx([[1, 0, 0]]) * P12 ** 2), E1=(F(1, 3),) * 3, E2=tuple(P12[i, i] for i in range(3)),
                  E3=tuple(v / pi12[p1] for v in (pi12[p1], pi12[p2], pi12[p3]))),
}


def extra():
    out = []
    out.append(('TE-CX-07/K', sp.simplify(sp.arg(-2 + 2 * I) - 3 * pi / 4) == 0 and sp.Abs(-2 + 2 * I) == 2 * sp.sqrt(2), 'modulus 2√2, argument 3π/4'))
    out.append(('TE-CX-09', sp.simplify(sp.cos(th) ** 2 - (1 + sp.cos(2 * th)) / 2) == 0, 'cos² linearised'))
    out.append(('TE-CX-09/A', sp.simplify(sp.sin(th) ** 3 - (3 * sp.sin(th) - sp.sin(3 * th)) / 4) == 0, 'sin³ linearised'))
    out.append(('TE-CX-11', sp.expand((z - 1) * (z ** 2 - 2 * z + 2) - P) == 0 and sp.div(P, z + 1, z)[1] != 0, 'P = (z − 1)Q; E3 leaves a remainder'))
    out.append(('TE-CX-12/A', sp.Abs(I) == 1 and sp.arg(I) == pi / 2, 'right isosceles at A'))
    out.append(('TE-AR-05', -17 == 5 * (-4) + 3, '−17 = 5 × (−4) + 3'))
    out.append(('TE-AR-06/A', all((2 ** (3 * nn) - 1) % 7 == 0 for nn in range(30)), '7 divides 2^(3n) − 1'))
    out.append(('TE-AR-07', 17 * (-2) + 5 * 7 == 1 and all(17 * (-2 + 5 * j) + 5 * (7 - 17 * j) == 1 for j in range(-5, 6)), 'Bézout and general solution'))
    t1 = all((3 * nn) % 5 != 0 or nn % 5 == 0 for nn in range(-100, 100))
    f1 = any((4 * nn) % 6 == 0 and nn % 6 != 0 for nn in range(-100, 100))
    f2 = any((nn * nn) % 4 == 0 and nn % 4 != 0 for nn in range(-100, 100))
    f3 = any((nn + 2) % 3 == 0 and nn % 3 != 0 for nn in range(-100, 100))
    out.append(('TE-AR-08', t1 and f1 and f2 and f3, 'key true; the three distractors have counterexamples'))
    out.append(('TE-AR-08/A', all(4 * 7 * j == 7 * 4 * j for j in range(-5, 6)), '4 × 7k = 7 × 4k'))
    out.append(('TE-AR-09', all(3 * (2 + 5 * j) + 5 * (-1 - 3 * j) == 1 for j in range(-5, 6)), 'general solution valid'))
    out.append(('TE-AR-11/A', all((nn ** 11 - nn) % 11 == 0 for nn in range(-50, 50)), 'Fermat'))
    out.append(('TE-GM-05/A', (5 * 3) % 2 == 1, 'odd degree sum is impossible'))
    out.append(('TE-GM-07/A', A7 * B7 != B7 * A7, 'AB ≠ BA'))
    out.append(('TE-GM-08', A8 * A8.inv() == sp.eye(2), 'A A⁻¹ = I'))
    out.append(('TE-GM-09/A', all(abs(v) < 1e-12 for v in (A9 ** 60) * Mx([1, 1])), 'Aⁿ → 0'))
    out.append(('TE-GM-11', P11 == Mx([[0.7, 0.3], [0.4, 0.6]]).applyfunc(sp.nsimplify), 'transition matrix'))
    pi_v = Mx([[pi12[p1], pi12[p2], pi12[p3]]])
    out.append(('TE-GM-12', pi_v * P12 == pi_v, 'πP = π'))
    return out
