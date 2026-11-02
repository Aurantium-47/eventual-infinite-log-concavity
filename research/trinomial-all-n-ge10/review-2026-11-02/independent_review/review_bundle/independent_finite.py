"""Independent finite-range audit for trinomial infinite log-concavity.

Uses exact coefficient rows (not the author's rounded successive-ratio
initializer), a full row (not a mirrored half-row), and 160-bit directed
intervals. No author module or saved certificate is imported.
The stopping condition proves all subsequent iterates via q <= 1/3.
It does NOT prove anything about untested exponents.
"""
import argparse
import hashlib
import json
from math import factorial
from pathlib import Path
import time


def coeffs(n):
    a = [1, n]
    for k in range(1, n):
        numerator = (n-k)*a[k] + (2*n-k+1)*a[k-1]
        nxt, remainder = divmod(numerator, k+1)
        if remainder:
            raise ArithmeticError((n, k, 'nonintegral coefficient'))
        a.append(nxt)
    return a + a[-2::-1]


def direct_coeff(n, k):
    return sum(factorial(n)//(factorial(j)*factorial(k-2*j)*factorial(n-k+j))
               for j in range(max(0, k-n), k//2+1))


def transform(a):
    p = [0] + a + [0]
    return [p[k+1]**2-p[k]*p[k+2] for k in range(len(a))]


def ceil_div(n, d):
    if n < 0 or d <= 0:
        raise ArithmeticError('invalid directed division')
    return (n+d-1)//d


def certify(n, bits):
    S = 1 << bits
    a = coeffs(n)
    lo, hi = [0], [0]
    for k in range(1, len(a)-1):
        num = S*a[k-1]*a[k+1]
        den = a[k]*a[k]
        lo.append(num//den)
        hi.append(ceil_div(num, den))
    lo.append(0)
    hi.append(0)
    for depth in range(31):
        if not all(0 <= x <= y < S for x, y in zip(lo, hi)):
            raise ArithmeticError((n, depth, 'positivity not certified'))
        if 3*max(hi) <= S:
            return depth
        lnext, unext = [0], [0]
        for k in range(1, len(lo)-1):
            lnext.append(lo[k]**2*(S-hi[k-1])*(S-hi[k+1])//(S*(S-lo[k])**2))
            unext.append(ceil_div(hi[k]**2*(S-lo[k-1])*(S-lo[k+1]), S*(S-hi[k])**2))
        lo, hi = lnext+[0], unext+[0]
    raise ArithmeticError((n, 'cone not certified by iteration 30'))


def small_exact_oracle():
    # Closed multinomial formula independently checks the differential recurrence.
    for n in range(1, 41):
        row = coeffs(n)
        if row != [direct_coeff(n, k) for k in range(2*n+1)]:
            raise ArithmeticError((n, 'coefficient oracle mismatch'))
    failures = []
    for n in range(1, 10):
        a = coeffs(n)
        for depth in range(1, 12):
            a = transform(a)
            bad = [(k, v) for k, v in enumerate(a) if v < 0]
            if bad:
                k, value = bad[0]
                failures.append({'n': n, 'first_negative_layer': depth, 'index': k,
                                 'negative_entry': str(value)})
                break
        else:
            raise ArithmeticError((n, 'expected small-exponent witness not found'))
    exact_depths = {}
    for n in [10, 11, 12, 20, 31, 40]:
        a = coeffs(n)
        for depth in range(15):
            if min(a) <= 0:
                raise ArithmeticError((n, depth, 'nonpositive exact iterate'))
            if all(a[k]**2 >= 3*a[k-1]*a[k+1] for k in range(1, len(a)-1)):
                exact_depths[str(n)] = depth
                break
            a = transform(a)
        if exact_depths[str(n)] != certify(n, 160):
            raise ArithmeticError((n, 'exact/interval cone depth mismatch'))
    return {'multinomial_oracle_exponents': [1, 40],
            'small_negative_witnesses': failures, 'exact_integer_cone_depths': exact_depths}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-n', type=int, default=4003)
    ap.add_argument('--bits', type=int, default=160)
    ap.add_argument('--output', type=Path, default=Path(__file__).with_name('independent_finite_result.json'))
    args = ap.parse_args()
    started = time.monotonic()
    oracle = small_exact_oracle()
    depths = []
    for n in range(10, args.max_n+1):
        depths.append(certify(n, args.bits))
        if n % 250 == 0:
            print(json.dumps({'completed_through': n, 'seconds': round(time.monotonic()-started, 2)}), flush=True)
    canonical = json.dumps(depths, separators=(',', ':')).encode()
    out = {'status': 'PASS', 'range_inclusive': [10, args.max_n], 'count': len(depths),
           'precision_bits': args.bits, 'maximum_cone_depth': max(depths),
           'depth_counts': {str(d): depths.count(d) for d in sorted(set(depths))},
           'depths_sha256': hashlib.sha256(canonical).hexdigest(),
           'depths_in_exponent_order': depths, 'seconds': time.monotonic()-started,
           'oracle': oracle,
           'scope': 'Only the listed finite exponent range is certified; no analytic n>=4004 proof is inferred.'}
    args.output.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['depths_in_exponent_order', 'oracle']}, indent=2))


if __name__ == '__main__':
    main()
