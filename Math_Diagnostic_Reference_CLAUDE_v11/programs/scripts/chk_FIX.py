"""Independent recomputation for the five v6 rows revised in v7 (TS-AN-04, BR-DF-03, 1C-AU-04, M1-F2-02, BR-AP-01)."""
import sympy as sp

x, y = sp.symbols('x y')
E = sp.E
I01 = lambda f: sp.integrate(f, (x, 0, 1))

CHECKS = {
 'TS-AN-04': dict(K=I01(x * sp.exp(2 * x)), A=I01(x * sp.exp(x)),
                  E1=(x * sp.exp(2 * x) / 2).subs(x, 1) + I01(sp.exp(2 * x) / 2),
                  E2=-I01(sp.exp(2 * x) / 2),
                  E3=((1 + 2 * x) * sp.exp(2 * x)).subs(x, 1) - ((1 + 2 * x) * sp.exp(2 * x)).subs(x, 0),
                  E4=I01(x) * I01(sp.exp(2 * x)), E5=(x * sp.exp(2 * x)).subs(x, 1) - (x * sp.exp(2 * x)).subs(x, 0)),
 'BR-DF-03': dict(K=sp.Rational(125, 100) * 80, A=100 * sp.Rational(11, 10), E2=80 + 25, E4=sp.Rational(25, 100) * 80, E5=80 + sp.Rational(25, 100)),
 'BR-AP-01': dict(K=3 * (-3) + 4, E1=(-3 + 4) * 3, E2=-3, E3=(-3 + 4) * 3, E4=9 + 4, E5=-9 - 4),
}


def extra():
    out = []
    out.append(('BR-DF-03/A', 100 * sp.Rational(11, 10) * sp.Rational(9, 10) == 99 and 110 - 11 == 99, '110, then −11, final 99'))
    out.append(('BR-DF-03/E1-E3', 100 * (1 + sp.Rational(10, 100) - sp.Rational(10, 100)) == 110 - 10 == 100, 'E1 and E3 share the final value 100; the staged answer separates them'))
    out.append(('1C-AU-04', 80 * sp.Rational(125, 100) * sp.Rational(9, 10) == 90 and 80 + 25 - 10 == 95 and 80 * sp.Rational(25, 100) * sp.Rational(9, 10) == 18
                and 80 * sp.Rational(125, 100) - 8 == 92 == 80 * sp.Rational(115, 100), 'key 90; E1 95; E2 18; E3 92 equals "percentages added"'))
    g = x ** 2 + y ** 2
    out.append(('M1-F2-02', sp.solve([sp.diff(g, x), sp.diff(g, y)], [x, y]) == {x: 0, y: 0} and g.subs({x: 0, y: 0}) == 0, 'critical point (0 ; 0)'))
    h = x ** 2 + y ** 2 - 2 * x
    out.append(('M1-F2-02/A', sp.solve([sp.diff(h, x), sp.diff(h, y)], [x, y]) == {x: 1, y: 0}, 'open target (1 ; 0)'))
    return out

CHECKS['M1-AA-03'] = dict(A=sp.limit((sp.exp(x) - 1 - x) / x ** 2, x, 0))
_extra0 = extra


def extra():
    out = _extra0()
    out.append(('M1-AA-03', sp.limit((1 - sp.cos(x)) / x ** 2, x, 0) == sp.Rational(1, 2) and sp.limit((1 - sp.cos(x)) / x ** 2, x, sp.oo) == 0
                and sp.limit(x ** 2 / (1 - sp.cos(x)), x, 0) == 2, 'key 1/2; E3 limit at +∞ is 0; E4 inverse gives 2'))
    return out
