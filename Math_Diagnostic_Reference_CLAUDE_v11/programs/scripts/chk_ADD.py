"""Independent recomputation of the v8 errors (add_mcq_v8.txt) and of the TS-AN-14-E1 open-seed signature.

CHECKS: values compared with the signature displayed in Math_Diagnostic_Targets_v8.csv (validate_reference_v8.py).
extra(): checks of signatures that are not single values (pairs, vectors, sets, statements resting on a computation).
"""
import sympy as sp

x, t, n, p = sp.symbols('x t n p')
lam, th = sp.Symbol('λ'), sp.Symbol('θ', real=True)

CHECKS = {
    'BR-NC-05': dict(E5=sp.solve(sp.Eq(2 * x - 1, 9), x)[0]),            # 3(2x − 1) = 9: the 9 is not divided by 3
    '1C-PR-02': dict(E5=sp.Rational(4, 10)),                             # P(A) given for P(A ∩ B)
    'TS-AN-01': dict(E5=0 * 0 + sp.Rational(1, 2)),                       # n(n + 1)/2 read n × n + 1/2, at n = 0
    'TS-AN-03': dict(E5=1 / sp.log(x)),                                  # derivative read as the reciprocal of ln
    'TS-AN-09': dict(E5=sp.Integer(10) ** 6 / 2),                        # square root taken as halving
    'TS-AN-17': dict(E5=sp.Rational(3, 10) / 3),                         # 0.03 read as 0.3 in 0.03/3
    'TS-AP-04': dict(E6=sp.Rational(100, 52)),                           # ratio inverted
    'TE-AR-03': dict(E6=(2 * 10) % 11),                                  # 2^10 computed as 2 × 10
    'TC-ST-02': dict(E4=2 * (3 + 1)),                                    # priority ignored in 2 × 3 + 1
    'TC-PR-02': dict(E4=sp.exp(-t / lam)),                               # λ read as the mean
    'M1-CA-03': dict(E5=sum(1 for _ in range(1, 4))),                    # inner sum only
    'M1-CA-04': dict(E5=1 - sp.sin(x) ** 2),                             # factor 2 lost
    'M1-CX-01': dict(E5=sp.arg(-1 - sp.I)),                              # sign of the imaginary part ignored
    'M1-PO-02': dict(E4=2 + 1),                                          # number of conditions plus one
    'M1-IN-02': dict(E5=sp.limit(n / n ** 2, n, sp.oo)),                 # each term k/n² (k ≤ n) tends to 0
    'M1-PR-04': dict(E5=sp.Rational(1, 6)),                              # probability of one face
    'M1-SN-03': dict(E5=sp.oo),                                          # infinitely many positive terms
    'M2-ST-01': dict(E6=2),                                              # 3 × 2 = 6 ≡ −1 (mod 7)
    'M2-RED-04': dict(E5=n),                                             # determinant taken as the dimension
    'M2-EU-02': dict(E5=0),
    'M2-EVN-01': dict(E5=max(3, 4)),                                     # sup norm of (3, 4)
    'M2-SE-02': dict(E5=sp.limit(n / (n + 1), n, sp.oo)),                # ratio without the power n
    'M2-SEN-01': dict(E5=sp.limit(1 / n, n, sp.oo)),                     # limit of the coefficients 1/n
    'M2-SEN-02': dict(E6=sp.diff(1 / (1 - x), x)),                       # derivative series used
    'M2-IN-04': dict(E5=sp.oo),
    'M2-PR-01': dict(E6=sp.exp(lam)),                                    # sign of the exponent lost
    'M2-PR-02': dict(E5=1 / (1 - p)),                                    # p and 1 − p exchanged
    'M2-PR-03': dict(E6=lam * (t - 1)),                                  # exponential forgotten
    'M2-CD-03': dict(E5=0),
    'M2-CD-04': dict(E5=[r for r in sp.solve(2 * x ** 2 - 1, x) if r > 0][0], E6=0),  # x = y on the circle; top point (0 ; 1)
}


def extra():
    out = []
    out.append(('1C-FN-03/E6', set(sp.solve((x - 1) * (x + 3), x)) == {1, -3} != set(sp.solve((x - 1) * (x - 3), x)), 'one sign changed: roots 1 and −3, not 1 and 3'))
    out.append(('M1-EU-01/E6', (1 + 1, 1 + (-1)) == (2, 0), 'u + v = (2 ; 0) instead of u · v = 0'))
    f = x ** 2 + sp.Symbol('y') ** 2 - 2 * x
    out.append(('M2-CD-01/E5', sp.diff(f, x) == 2 * x - 2, '∂f/∂x = 2x − 2; the ∂f/∂y component replaced by 0'))
    out.append(('M2-ST-04/E5', 6 + 10 == 16 and sp.gcd(6, 10) == 2, 'generators added: 16ℤ instead of 2ℤ'))
    out.append(('TE-CX-02/E6', sp.simplify(sp.re(sp.expand((sp.cos(th) + sp.I * sp.sin(th)) ** 2)) - sp.cos(2 * th)) == 0, 'real part only: cos(2θ)'))
    v_open = 1 + 0.1 * sp.exp(sp.Rational(1, 10))
    v_mcq = 2 + 0.1 / (2 * sp.sqrt(4.1))
    out.append(('TS-AN-14-E1', round(float(v_open), 4) == 1.1105 and abs(float(v_mcq) - 2.025) < 0.001,
                'open seed: 1 + 0.1e^0.1 = 1.1105; MCQ seed: 2.0247, within 0.001 of the key 2.025'))
    out.append(('TS-AN-09/key', min(N for N in range(1, 2000) if all(k * k > 10 ** 6 for k in range(N, N + 50))) == 1001, 'N = 1001; E5 = 10⁶/2'))
    out.append(('1S-PS-02/E6', sp.Rational(2, 10) / sp.Rational(5, 10) == sp.Rational(4, 10) != sp.Rational(5, 10), 'P(B | A) = 0.2/0.5 = 0.4 = P(B), compared with P(A) = 0.5'))
    out.append(('M1-SN-04/E4', all(sp.Rational(1, k * k + 1) <= sp.Rational(1, k * k) for k in range(1, 50)), '1/(n² + 1) ≤ 1/n² is true but does not give the equivalence'))
    out.append(('M2-SE-01/E4', sp.limit((n / (n + 1)) ** 2, n, sp.oo) == 1, 'ratio → 1: the ratio test is inconclusive'))
    out.append(('M2-SE-02/key', sp.limit((n / (n + 1)) ** n, n, sp.oo) == sp.exp(-1), 'key 1/e; E5 drops the power n'))
    return out
