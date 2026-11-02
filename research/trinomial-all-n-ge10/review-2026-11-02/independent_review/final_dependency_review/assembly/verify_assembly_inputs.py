"""Independent small exact checks for the edge-to-root assembly.

Reads only the frozen rational node table and the list of 63 bypass indices.
Does not import author code, read saved jets, or regenerate coefficient jets.
Uses power-basis polynomials followed by a direct Bernstein conversion, rather
than the submitted Bernstein-product implementation.  All arithmetic is exact.
"""
if not __debug__:
    raise RuntimeError('Run without -O/-OO; assertions must be enabled.')

from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
import argparse
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('edge', type=Path, help='Frozen certificate_package/edge directory')
SOURCE = parser.parse_args().edge


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and not poly[-1]:
        poly.pop()
    return poly


def add(*polys):
    out = [F(0)] * max(map(len, polys))
    for poly in polys:
        for i, coefficient in enumerate(poly):
            out[i] += coefficient
    return trim(out)


def scale(coefficient, poly):
    return trim([coefficient * value for value in poly])


def mul(left, right):
    out = [F(0)] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            out[i + j] += left_value * right_value
    return trim(out)


def power(poly, exponent):
    out = [F(1)]
    for _ in range(exponent):
        out = mul(out, poly)
    return out


def controls(poly):
    degree = len(poly) - 1
    return [sum((poly[j] * F(comb(k, j), comb(degree, j))
                 for j in range(k + 1)), F(0))
            for k in range(degree + 1)]


def positive_record(name, poly, require=True):
    values = controls(poly)
    minimum = min(values)
    if require and minimum <= 0:
        raise ArithmeticError((name, minimum))
    return {'name': name, 'degree': len(poly) - 1,
            'minimum_control': str(minimum), 'positive': minimum > 0}


def alternating_atan(x, count):
    partial = sum((F((-1)**k, 2*k + 1) * x**(2*k + 1)
                   for k in range(count)), F(0))
    successor = partial + F((-1)**count, 2*count + 1) * x**(2*count + 1)
    return min(partial, successor), max(partial, successor)


def outward(pair, denominator=10**15):
    lo, hi = pair
    lower = (lo * denominator).numerator // (lo * denominator).denominator
    upper_fraction = hi * denominator
    upper = -((-upper_fraction.numerator) // upper_fraction.denominator)
    return F(lower, denominator), F(upper, denominator)


def trig_at_rational(x, cosine):
    offset = 0 if cosine else 1
    count = 12
    partial = sum((F((-1)**k, factorial(2*k + offset)) * x**(2*k + offset)
                   for k in range(count)), F(0))
    successor = partial + F((-1)**count, factorial(2*count + offset)) * x**(2*count + offset)
    return min(partial, successor), max(partial, successor)


def constants():
    a = alternating_atan(F(1, 5), 24)
    b = alternating_atan(F(1, 239), 8)
    pi = outward((16*a[0] - 4*b[1], 16*a[1] - 4*b[0]), 10**18)
    bounds = {}
    for label, divisor, cosine in [('c', 16, True), ('d', 16, False),
                                   ('c2', 8, True), ('d2', 8, False)]:
        if cosine:
            raw = (trig_at_rational(pi[1]/divisor, True)[0],
                   trig_at_rational(pi[0]/divisor, True)[1])
        else:
            raw = (trig_at_rational(pi[0]/divisor, False)[0],
                   trig_at_rational(pi[1]/divisor, False)[1])
        bounds[label] = outward(raw)
        if not 0 < bounds[label][0] < bounds[label][1] < 1:
            raise ArithmeticError((label, bounds[label]))
    return pi, bounds


PI, TRIG = constants()


def atan_rational(numerator, denominator, u, order, divide_u):
    """Exact rational polynomial for T_order(u*N/D), optionally divided by u."""
    if order == 3:
        num = add(mul(numerator, power(denominator, 2)),
                  scale(-F(1, 3), mul(power(u, 2), power(numerator, 3))))
        den = power(denominator, 3)
    elif order == 5:
        num = add(mul(numerator, power(denominator, 4)),
                  scale(-F(1, 3), mul(mul(power(u, 2), power(numerator, 3)),
                                      power(denominator, 2))),
                  scale(F(1, 5), mul(power(u, 4), power(numerator, 5))))
        den = power(denominator, 5)
    else:
        raise ValueError(order)
    if not divide_u:
        num = mul(u, num)
    return num, den


def panel_forms(left_node, right_node, left_u, right_u):
    # Local power variable x lies in [0,1]. Normalize harmonic t=A/B to A=1.
    u = [left_u, right_u - left_u]
    B = [1/left_node, 1/right_node - 1/left_node]
    B2, uB, u2 = power(B, 2), mul(u, B), power(u, 2)

    def ratio(weight, upper):
        index_n = 1 if upper else 0
        index_d = 0 if upper else 1
        N = add(scale(weight*TRIG['d'][index_n], B),
                scale(TRIG['d2'][index_n], u))
        D = add(B2, scale(weight*TRIG['c'][index_d], uB),
                scale(TRIG['c2'][index_d], u2))
        return N, D

    pairs = {'p_lower': ratio(1, False), 'p_upper': ratio(1, True),
             'q_lower': ratio(4, False), 'q_upper': ratio(4, True)}
    domain = [positive_record('harmonic_denominator', B),
              positive_record('s_below_one', add(B, scale(-1, u)))]
    for name, (N, D) in pairs.items():
        domain += [positive_record(name + '_numerator', N),
                   positive_record(name + '_denominator', D),
                   positive_record(name + '_atan_argument_below_one',
                                   add(D, scale(-1, mul(u, N))))]
    variance_den = add(B2, uB, u2)
    variance_gap = add(mul(B, add(B2, scale(4, uB), u2)),
                       scale(-250, power(variance_den, 2)))
    return u, B, pairs, domain, variance_gap


def phase_expression(p_ratio, q_ratio, u, lower):
    # Returns N/D bounding Psi + 45*pi/32. The apparent 1/u is eliminated.
    pn, pd = atan_rational(*p_ratio, u, 3 if lower else 5, True)
    qn, qd = atan_rational(*q_ratio, u, 5 if lower else 3, False)
    numerator = add(mul(mul(add([F(16)], scale(45, u)), pn), qd),
                    scale(-F(45, 2), mul(qn, pd)))
    return numerator, mul(pd, qd)


def main():
    node_data = json.loads((SOURCE / 'nodes.json').read_text())
    manifest = json.loads((SOURCE / 'data_manifest.json').read_text())
    grid = list(map(F, node_data['u_endpoints']))
    if grid != [F(i, 32032) for i in range(9)] or grid[-1] != F(1, 4004):
        raise ArithmeticError('Parameter grid does not match the stated closed cover.')
    if [row['node'] for row in node_data['nodes']] != list(range(1, 250)):
        raise ArithmeticError('Node labels are not exactly 1,...,249.')
    nodes = {row['node']: list(map(F, row['endpoints'])) for row in node_data['nodes']}
    if not all(len(values) == 9 and min(values) > 0 for values in nodes.values()):
        raise ArithmeticError('Invalid or nonpositive endpoint row.')
    gaps = [(nodes[j+1][k] - nodes[j][k], j, k)
            for j in range(1, 249) for k in range(9)]
    minimum_gap = min(gaps)
    if minimum_gap[0] <= 0:
        raise ArithmeticError(('Endpoint ordering failed', minimum_gap))
    maximum_node = max(value for values in nodes.values() for value in values)
    if not maximum_node < 253 or not grid[-1] * maximum_node < 1:
        raise ArithmeticError('The simple global positive-radius bound failed.')

    bypass_pairs = [tuple(pair) for pair in manifest['bypasses']]
    if len(bypass_pairs) != 63 or len(set(bypass_pairs)) != 63:
        raise ArithmeticError('Bypass list is not 63 distinct pairs.')
    if not all(0 <= panel < 8 and 1 <= node <= 249 for panel, node in bypass_pairs):
        raise ArithmeticError('Bypass pair outside required index domain.')
    per_panel = [sum(panel == p for panel, node in bypass_pairs) for p in range(8)]
    if per_panel != [3, 4, 6, 8, 9, 10, 11, 12]:
        raise ArithmeticError(('Unexpected bypass coverage', per_panel))

    bypasses = []
    for panel, node in sorted(bypass_pairs):
        u, B, pairs, domain, variance_gap = panel_forms(
            nodes[node][panel], nodes[node][panel+1], grid[panel], grid[panel+1])
        ln, ld = phase_expression(pairs['p_lower'], pairs['q_upper'], u, True)
        un, ud = phase_expression(pairs['p_upper'], pairs['q_lower'], u, False)
        phase_factor = F(node) + F(45, 32)
        lower_gap = add(ln, scale(F(1, 3) - phase_factor*PI[1], ld))
        upper_gap = add(scale(phase_factor*PI[0] + F(1, 3), ud), scale(-1, un))
        checks = [positive_record('variance_above_250', variance_gap),
                  positive_record('phase_above_node_pi_minus_one_third', lower_gap),
                  positive_record('phase_below_node_pi_plus_one_third', upper_gap)]
        bypasses.append({'panel': panel, 'node': node,
                         'parameter_interval': [str(grid[panel]), str(grid[panel+1])],
                         'domain': domain, 'margins': checks})
        print(f'bypass panel={panel} node={node}: exact positive controls', flush=True)

    joins = []
    for panel in range(8):
        u, B, pairs, domain, _ = panel_forms(
            nodes[249][panel], nodes[249][panel+1], grid[panel], grid[panel+1])
        un, ud = phase_expression(pairs['p_upper'], pairs['q_lower'], u, False)
        gap = add(scale((F(250) + F(45, 32))*PI[0], ud), scale(-1, un))
        joins.append({'panel': panel, 'node': 249,
                      'parameter_interval': [str(grid[panel]), str(grid[panel+1])],
                      'domain': domain, 'margin': positive_record('phase_below_250_pi', gap)})
        print(f'join panel={panel}: exact positive controls', flush=True)

    result = {
        'status': 'PASS',
        'method': 'independent power-basis arithmetic and power-to-Bernstein conversion',
        'inputs_read': ['fixed nodes.json', 'fixed data_manifest.json bypass indices only'],
        'not_performed': ['jet replay', 'jet regeneration', 'finite-exponent verification'],
        'pi_interval': list(map(str, PI)),
        'trigonometric_intervals': {key: list(map(str, value)) for key, value in TRIG.items()},
        'grid': list(map(str, grid)),
        'node_rows': len(nodes), 'positive_endpoint_values': 249*9,
        'strict_adjacent_endpoint_comparisons': len(gaps),
        'minimum_adjacent_endpoint_gap': {'value': str(minimum_gap[0]),
                                         'left_node': minimum_gap[1], 'endpoint': minimum_gap[2]},
        'maximum_node_endpoint': str(maximum_node),
        'uniform_ut_upper_bound': str(grid[-1] * maximum_node),
        'bypasses_per_panel': per_panel, 'bypasses': bypasses, 'joins': joins,
        'zero_endpoint_sign_margin': '2*|A_0|/225 > 0; proved analytically in ASSEMBLY_REVIEW.txt'}
    (HERE / 'assembly_input_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print('PASS: 2241 positive endpoints; 2232 strict adjacent comparisons; 63 bypasses; 8 joins.', flush=True)


if __name__ == '__main__':
    main()
