"""Exact independent algebra for the phase appendix; Python standard library.

No author code, symbolic-algebra library, certificate, or saved answer is read.
The sparse integer ring Z[s,c] is paired with iw, where w^2=1-c^2.
Six cleared polynomial identities and three rational threshold comparisons
are regenerated.  Their sign/branch use is proved in PHASE_AND_REAL_EXPONENT.txt.
"""
if not __debug__:
    raise RuntimeError('Run with assertions enabled, without -O/-OO.')

from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import json


def add(*polys):
    out = defaultdict(int)
    for poly in polys:
        for powers, coefficient in poly.items():
            out[powers] += coefficient
    return {powers: coefficient for powers, coefficient in out.items()
            if coefficient}


def scale(coefficient, poly):
    return {powers: coefficient * value for powers, value in poly.items()
            if coefficient * value}


def sub(left, right):
    return add(left, scale(-1, right))


def mul(left, right):
    out = defaultdict(int)
    for (ls, lc), left_value in left.items():
        for (rs, rc), right_value in right.items():
            out[(ls + rs, lc + rc)] += left_value * right_value
    return {powers: coefficient for powers, coefficient in out.items()
            if coefficient}


def power(poly, exponent):
    out = {(0, 0): 1}
    for _ in range(exponent):
        out = mul(out, poly)
    return out


ONE = {(0, 0): 1}
ZERO = {}
S = {(1, 0): 1}
C = {(0, 1): 1}
W_SQUARED = sub(ONE, power(C, 2))


def complex_mul(left, right):
    # A pair (a,b) means a+i*w*b, not a+i*b.
    return (sub(mul(left[0], right[0]),
                mul(W_SQUARED, mul(left[1], right[1]))),
            add(mul(left[0], right[1]), mul(left[1], right[0])))


def complex_add(*pairs):
    return (add(*(pair[0] for pair in pairs)),
            add(*(pair[1] for pair in pairs)))


def complex_scale(coefficient, pair):
    return scale(coefficient, pair[0]), scale(coefficient, pair[1])


def norm_squared(pair):
    return add(power(pair[0], 2), mul(W_SQUARED, power(pair[1], 2)))


def imaginary_numerator(numerator, denominator):
    # Imag(numerator/denominator) = w*this / |denominator|^2.
    return sub(mul(numerator[1], denominator[0]),
               mul(numerator[0], denominator[1]))


def serialize(poly):
    return [{'s_power': powers[0], 'c_power': powers[1],
             'coefficient': coefficient}
            for powers, coefficient in sorted(poly.items())]


def main():
    identities = []

    def identity(name, equation, left, right):
        residual = sub(left, right)
        if residual:
            raise ArithmeticError((name, serialize(residual)))
        identities.append({
            'name': name, 'equation': equation,
            'cleared_left': serialize(left), 'cleared_right': serialize(right),
            'residual': serialize(residual), 'equal': not residual})

    # z=s(c+iw); w^2=1-c^2. Everything below is integer polynomial algebra.
    z = mul(S, C), S
    z_squared = complex_mul(z, z)
    p = complex_add((ONE, ZERO), z, z_squared)
    q = complex_add((ONE, ZERO), complex_scale(4, z), z_squared)
    m_numerator = complex_add(z, complex_scale(2, z_squared))
    mq_numerator = complex_add(complex_scale(4, z),
                               complex_scale(2, z_squared))

    identity(
        'imaginary_part_of_m',
        'Im(z*pprime/p)=s*w*(1+4*s*c+s^2)/|p|^2',
        imaginary_numerator(m_numerator, p),
        mul(S, add(ONE, scale(4, mul(S, C)), power(S, 2))))
    identity(
        'imaginary_part_of_mq',
        'Im(z*qprime/q)=4*s*w*(1+s*c+s^2)/|q|^2',
        imaginary_numerator(mq_numerator, q),
        scale(4, mul(S, add(ONE, mul(S, C), power(S, 2)))))
    identity(
        'q_minus_p_squared_modulus',
        '|q|^2-|p|^2=6*s*c*(1+s^2)+15*s^2',
        sub(norm_squared(q), norm_squared(p)),
        add(scale(6, mul(mul(S, C), add(ONE, power(S, 2)))),
            scale(15, power(S, 2))))

    n2 = complex_mul(z, q)
    p_squared = complex_mul(p, p)
    positive_factor = add(
        scale(4, mul(power(S, 2), power(C, 2))),
        scale(8, mul(power(S, 3), C)), scale(8, mul(S, C)),
        power(S, 4), scale(5, power(S, 2)), ONE)
    identity(
        'imaginary_part_of_v',
        'Im(v)=s*w*(1-s^2)*(4*s^2*c^2+8*s^3*c+8*s*c+s^4+5*s^2+1)/|p|^4',
        imaginary_numerator(n2, p_squared),
        mul(mul(S, sub(ONE, power(S, 2))), positive_factor))

    ps = add(ONE, S, power(S, 2))
    qs = add(ONE, scale(4, S), power(S, 2))
    pprime = add(ONE, scale(2, S))
    qprime = add(scale(4, ONE), scale(2, S))
    identity(
        'real_variance_derivative',
        's*vprime(s)=s*(1-s^2)*(1+7*s+s^2)/p(s)^3',
        sub(mul(add(qs, mul(S, qprime)), ps),
            scale(2, mul(mul(S, qs), pprime))),
        mul(sub(ONE, power(S, 2)), add(ONE, scale(7, S), power(S, 2))))
    identity(
        'm_over_v_minus_one',
        'm(s)/v(s)-1=s*(2*s^2+2*s-1)/(1+4*s+s^2)',
        sub(mul(add(ONE, scale(2, S)), ps), qs),
        mul(S, add(scale(2, power(S, 2)), scale(2, S), scale(-1, ONE))))

    endpoint = F(7, 20)
    endpoint_variance = (endpoint * (1 + 4 * endpoint + endpoint**2)
                         / (1 + endpoint + endpoint**2)**2)
    bridge_margin = 1001 * endpoint_variance - 250
    curvature_polynomial = 2 * endpoint**2 + 2 * endpoint - 1
    comparisons = [
        {'name': 'variance_at_7_over_20', 'left': str(endpoint_variance),
         'right': '141260/346921', 'relation': '=',
         'pass': endpoint_variance == F(141260, 346921)},
        {'name': 'n1001_variance_bridge', 'left': str(bridge_margin),
         'right': '0', 'relation': '>', 'pass': bridge_margin > 0,
         'cleared_integer_margin': 1001 * 141260 - 250 * 346921},
        {'name': 'm_below_v_endpoint_polynomial', 'left': str(curvature_polynomial),
         'right': '-11/200', 'relation': '=',
         'pass': curvature_polynomial == F(-11, 200) and curvature_polynomial < 0}]
    if not all(item['pass'] for item in comparisons):
        raise ArithmeticError(comparisons)

    result = {
        'status': 'PASS',
        'method': 'sparse integer polynomials in s,c and pairs a+i*w*b with w^2=1-c^2',
        'dependencies': 'Python standard library only; no submitted programs or data read',
        'identity_count': len(identities), 'identities': identities,
        'rational_comparison_count': len(comparisons), 'comparisons': comparisons,
        'scope': 'Algebra only; branch, sign, domain, and convergence arguments are in PHASE_AND_REAL_EXPONENT.txt.'}
    target = Path(__file__).with_name('phase_identity_results.json')
    target.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'identities': len(identities),
                      'rational_comparisons': len(comparisons),
                      'output': str(target)}, indent=2))


if __name__ == '__main__':
    main()
