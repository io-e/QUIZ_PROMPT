"""Independent recomputation of Brevet v7 values (keys K, open targets A, signatures E1..)."""
from fractions import Fraction as F
from math import gcd, lcm, degrees, acos, asin, atan, tan, radians, sqrt as fsqrt
import sympy as sp
x = sp.Symbol('x')
pi = sp.pi

CHECKS = {
 'BR-NC-06': dict(K=-7 + 3 - (-5), A=-3 - (-8) + (-2) * 4, E1=-(7 + 3) - (-5), E2=(-7 + 3) - 5, E3=abs(-7 + 3) + 5),
 'BR-NC-07': dict(K=F(-12, 4) * (-3), E1=-(F(12, 4) * 3), E2=F(-12, 4 * (-3)), E3=(-12) * 4 * (-3)),
 'BR-NC-08': dict(K=20 - 4 * (3 - 5) ** 2, E1=(20 - 4) * (3 - 5) ** 2, E2=20 - 4 * (-4), E3=20 - 4 * (3 ** 2 - 5 ** 2)),
 'BR-NC-10': dict(K=F(2, 3) - F(1, 4), A=F(3, 8) + F(5, 12) - F(1, 6), E1=F(2 - 1, 3 - 4), E2=F(2 - 1, 12), E3=F(2 * 1, 3 * 4)),
 'BR-NC-11': dict(K=F(5, 6) / F(2, 9), E1=F(5, 6) * F(2, 9), E2=F(6, 5) * F(2, 9), E3=F(5 * 9, 6)),
 'BR-NC-12': dict(K=gcd(72, 108), A=F(72, 108), E1=lcm(72, 108), E2=2 * 3, E3=2 ** 2),
 'BR-NC-13': dict(K=(240 - 240 * 3 // 8) - (240 - 240 * 3 // 8) // 3, A=(200 - 80) - (200 - 80) // 4,
                  E1=240 - 90 - 240 // 3, E2=(240 - 240 // 8) - (240 - 240 // 8) // 3, E3=240 - 90),
 'BR-NC-14': dict(K=F(10) ** (5 - 2 - 4), A=5000, E1=F(10) ** (5 * -2 - 4), E2=F(10) ** (3 + 4), E3=F(10) ** (5 + 2 - 4)),
 'BR-NC-15': dict(K=F(1, 8), E1=-8, E2=2 * (-3), E3=F(1, 2 * 3)),
 'BR-NC-16': dict(K=F(3) ** (8 - 5), E1=F(3) ** (4 + 2 - 5), E2=F(3) ** (8 * -5), E3=-(3 ** 13)),
 'BR-NC-17': dict(K=F(15, 1000), A=500, E1=F(15, 10 ** 5), E2=F(15, 10 ** 28), E3=F(8, 1000)),
 'BR-NC-18': dict(K=5, E1=4 + 3, E2=F(25, 2), E3=25),
 'BR-NC-19': dict(K={-7, 7}, E1={7}, E2={F(49, 2)}, E3={-49, 49}),
 'BR-NC-20': dict(K=lcm(12, 18), E1=gcd(12, 18), E2=12 * 18, E3=12 + 18),
 'BR-NC-21': dict(K=59, E1=51, E2=91, E3=1),
 'BR-NC-22': dict(K=sp.expand(5 - 3 * (2 * x - 4)), E1=5 - 6 * x - 12, E2=5 - 6 * x - 4, E3=sp.expand((5 - 3) * (2 * x - 4))),
 'BR-NC-23': dict(K=sp.expand((2 * x - 3) * (x + 4)), A=sp.expand((x + 5) * (x - 2) - x * (x + 1)),
                  E1=2 * x ** 2 - 12, E2=2 * x ** 2 + 8 * x + 3 * x - 12, E3=2 * (2 * x) + 8 * x - 3 * x - 12),
 'BR-NC-24': dict(K=sp.expand((3 * x - 5) ** 2), E1=9 * x ** 2 - 25, E2=3 * x ** 2 - 30 * x + 25, E3=9 * x ** 2 - 30 * x - 25),
 'BR-NC-25': dict(K=sp.expand((x + 2) * (3 * x - 1) - (x + 2) * (x + 4)), E1=(x + 2) * (3 * x - 1 - x + 4),
                  E2=(x + 2) * (3 * x - 1) * (x + 4), E3=(3 * x - 1) - (x + 4)),
 'BR-NC-26': dict(K=sp.solve(5 * x - 7 - (2 * x + 8))[0], A=sp.solve(3 * (x - 2) - (5 * x + 4))[0],
                  E1=F(8 - 7, 3), E2=15 - 3, E3=F(15, 5 + 2)),
 'BR-NC-27': dict(K=sp.solve(41 + x - 3 * (9 + x))[0], E1=sp.solve(41 + x - 27)[0], E2=sp.solve(41 - x - 3 * (9 - x))[0], E3=41 - 27),
 'BR-NC-29': dict(K=set(sp.solve(x ** 2 - 5 * x)), E1={5}, E2={sp.sqrt(5)}, E3={0, -5}),
 'BR-DF-06': dict(K=F(54, 360) * 100, E1=54, E2=F(54, 180) * 100, E3=F(54, 360)),
 'BR-DF-07': dict(K=F(12, 80) * 100, E1=F(80, 12), E2=12, E3=F(68, 80) * 100),
 'BR-DF-08': dict(K=F(10 * 3 + 14 * 5 + 18 * 2, 10), A=sp.solve((2 * 12 + 3 * 15 + 9 + 2 * x) / 8 - 13)[0],
                  E1=F(10 + 14 + 18, 3), E2=F(136, 3), E3=F(3 + 5 + 2, 3)),
 'BR-DF-09': dict(K=F(7 + 9, 2), E1=F(12 + 9, 2), E2=F(46, 6), E3=7),
 'BR-DF-10': dict(K=sorted([2, 4, 5, 7, 8, 10, 11, 13, 15, 20, 21])[2], E1=4, E2=10, E3=F(21, 4)),
 'BR-DF-11': dict(K=10 + 25, E1=25, E2=50, E3=25 + 15),
 'BR-DF-12': dict(K=F(2, 5) ** 2, A=2 * F(2, 5) * F(3, 5), E1=F(2, 5) * F(1, 4), E2=F(2, 5) + F(2, 5), E3=F(1, 4)),
 'BR-DF-13': dict(K=F(65, 100), A=1 - F(5, 6) ** 2, E1=F(75, 100), E2=F(9965, 100), E3=F(-35, 100)),
 'BR-DF-15': dict(K=F(5, 10) + F(4, 10) - F(15, 100), E1=F(9, 10), E2=F(105, 100), E3=F(5, 10) * F(4, 10)),
 'BR-DF-16': dict(K=F(92, 10) / 4 * 7, E1=F(92, 10) + 3, E2=F(round(28 / 9.2, 2)).limit_denominator(1000), E3=F(92, 10) * 7),
 'BR-DF-17': dict(K=F(35, 100) * 240, E1=240 - 35, E2=F(240, 35), E3=F(35, 1000) * 240),
 'BR-DF-18': dict(K=F(330) / F(12, 10), E1=F(330) * F(8, 10), E2=310, E3=F(round(330 / 1.02, 2)).limit_denominator(1000)),
 'BR-DF-21': dict(K=sp.solve(2 * x + 1 - (-x + 7))[0], E1=2 * 2 + 1, E2=F(7 + 1, 3), E3=3),
 'BR-DF-22': dict(K=(-3) ** 2, E1=-(3 ** 2), E2=-3 * 2, E3=3 * 2),
 'BR-GM-05': dict(K=pi * 5 ** 2, E1=pi * 10 ** 2, E2=pi * 10, E3=pi * 5),
 'BR-GM-06': dict(K=F(6 * 4 * 9, 3), E1=6 * 4 * 9, E2=F(6 * 4 * 9, 2), E3=F(2 * (6 + 4) * 9, 3)),
 'BR-GM-07': dict(K=sp.Rational(4, 3) * pi * 6 ** 3, A=(sp.Rational(4, 3) * pi * 27) / (pi * 9 * 6),
                  E1=4 * pi * 6 ** 2, E2=sp.Rational(4, 3) * pi * 12 ** 3, E3=pi * 6 ** 3),
 'BR-GM-08': dict(K=2 * 60 + 24, E1=2 * 60 + 40, E2=2 * 60 + 4, E3=1 * 60 + 44),
 'BR-GM-09': dict(K=F(450, 150), E1=F(450, 230), E2=F(450, 150) * 60, E3=F(150, 450)),
 'BR-GM-10': dict(K=F(6 * 25000, 100000), E1=15, E2=F(6, 25000), E3=150),
 'BR-GM-11': dict(K=F(72, 1) / F(36, 10), E1=F(72) * F(36, 10), E2=F(72, 60), E3=72000),
 'BR-EG-17': dict(K=sp.sqrt(13 ** 2 - 5 ** 2), E1=sp.sqrt(13 ** 2 + 5 ** 2), E2=13 - 5, E3=13 ** 2 - 5 ** 2),
 'BR-EG-18': dict(K=4 * F(75, 10) / 3, E1=4 * 3 / F(75, 10), E2=4 + (F(75, 10) - 3), E3=4 * F(105, 10) / 3),
 'BR-EG-19': dict(K=round(degrees(acos(0.8))), E1=round(degrees(asin(0.8))), E2=round(degrees(atan(0.8))), E3=F(round(acos(0.8), 2)).limit_denominator(100)),
 'BR-EG-20': dict(K=(0, 2), E1=(0, -2), E2=(-2, 0), E3=(2, 2)),
 'BR-EG-22': dict(K=sp.sqrt(5 ** 2 - 3 ** 2), E1=5 - 3, E2=sp.sqrt(5 ** 2 + 3 ** 2), E3=5),
 'BR-EG-25': dict(K=sp.sqrt(3 ** 2 + 4 ** 2 + 12 ** 2), E1=sp.sqrt(3 ** 2 + 4 ** 2), E2=3 + 4 + 12, E3=5 + 12),
 'BR-AP-05': dict(K=4 * 3, E1=3 * 3, E2=5 * 3, E3=3),
 'BR-AP-07': dict(K=27, E1=9, E2=81, E3=3),
 'BR-AP-08': dict(K=sp.expand(2 * (x + 3) - 6), E1=2 * x + 3 - 6, E2=x + 3 * 2 - 6, E3=2 * (x + 3)),
}


def extra():
    """Checks that are not value comparisons; return list of (id, ok, note)."""
    out = []
    out.append(('BR-NC-09', sorted([-0.4, -0.35, -0.5]) == [-0.5, -0.4, -0.35], 'order of −0.4, −0.35, −1/2'))
    out.append(('BR-NC-21', sp.isprime(59) and not sp.isprime(51) and not sp.isprime(91) and not sp.isprime(1), 'only 59 prime'))
    sol = sp.solve_univariate_inequality(-3 * x + 4 > 19, x, relational=False)
    out.append(('BR-NC-28', sol == sp.Interval.open(-sp.oo, -5), 'x < −5'))
    out.append(('BR-NC-28/A', sp.solve_univariate_inequality(2 * (x - 3) <= 5 * x + 6, x, relational=False) == sp.Interval(-4, sp.oo), 'x ≥ −4'))
    out.append(('BR-DF-20', (5 - (-1)) / 2 == 3, 'slope 3, intercept −1'))
    out.append(('BR-EG-25/A', (10 ** 2 + 8 ** 2, 10 ** 2 + 8 ** 2 + 6 ** 2) == (164, 200), 'face and space diagonals'))
    out.append(('BR-EG-19/A', abs(30 * tan(radians(40)) - 25.17) < 0.01, 'tower height'))
    return out
