#!/usr/bin/env python3
"""Exact verifiers for the partial trinomial results; Python 3.10+, standard library.

python verify.py --quick       # finite algebraic certificates and small ratio checks
python verify.py --full        # also regenerate every dyadic certificate, n up to 100000
python verify.py --full --write-data  # regenerate the stored data

No floating-point arithmetic or numerical root finding is used. Assertions are
part of the verifier: do not run Python with -O. Data files are compared with
freshly computed values, not treated as trusted mathematical assertions.
"""
from __future__ import annotations
import argparse, csv, gzip, io, itertools, json, math, pathlib, sys, time
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)
ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / 'data'


def row(n: int) -> list[int]:
    assert n >= 0
    a = [1]
    for _ in range(n):
        b = [0] * (len(a) + 2)
        for k, x in enumerate(a):
            b[k] += x; b[k+1] += x; b[k+2] += x
        a = b
    return a


def L(a: list[int]) -> list[int]:
    return [x*x - (a[k-1]*a[k+1] if 0 < k < len(a)-1 else 0)
            for k, x in enumerate(a)]


def det_bareiss(matrix: list[list[int]]) -> int:
    a = [r[:] for r in matrix]
    n = len(a)
    if n == 0: return 1
    old, sign = 1, 1
    for k in range(n-1):
        if a[k][k] == 0:
            p = next((p for p in range(k+1, n) if a[p][k]), None)
            if p is None: return 0
            a[k], a[p] = a[p], a[k]; sign = -sign
        pivot = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                z = a[i][j]*pivot - a[i][k]*a[k][j]
                assert z % old == 0
                a[i][j] = z // old
            a[i][k] = 0
        old = pivot
    return sign*a[-1][-1]


PERMS4 = [(p, (-1)**sum(p[i] > p[j] for i in range(4) for j in range(i+1,4)))
          for p in itertools.permutations(range(4))]
def det4_independent(a: list[list[int]]) -> int:
    return sum(sign*a[0][p[0]]*a[1][p[1]]*a[2][p[2]]*a[3][p[3]]
               for p, sign in PERMS4)


def json_data(name: str, value, write: bool) -> None:
    path = DATA / name
    if write:
        if name.endswith('.gz'):
            with gzip.open(path, 'wt', encoding='utf-8') as f:
                json.dump(value, f, separators=(',', ':'))
        else:
            path.write_text(json.dumps(value, indent=2)+'\n')
    else:
        if name.endswith('.gz'):
            with gzip.open(path, 'rt', encoding='utf-8') as f: expected = json.load(f)
        else: expected = json.loads(path.read_text())
        assert expected == value, ('stored data mismatch', name)


def pf4_certificates(write: bool) -> list[dict]:
    summaries = []
    for n in (8, 9):
        a = row(n); records = []; smallest = None
        for u0 in itertools.combinations_with_replacement(range(2*n+1), 4):
            u = u0[::-1]
            M = [[a[t] if 0 <= t < len(a) else 0
                  for t in (u[i]-i+j for j in range(4))] for i in range(4)]
            b = det_bareiss(M); c = det4_independent(M)
            assert b == c and b > 0, (n, u, b, c)
            records.append(list(u)+[b])
            smallest = b if smallest is None else min(smallest, b)
        assert len(records) == math.comb(2*n+4, 4)
        path = DATA / f'pf4_n{n}.csv.gz'
        if write:
            with gzip.open(path, 'wt', newline='') as f:
                w = csv.writer(f); w.writerow(['u1','u2','u3','u4','determinant']); w.writerows(records)
        else:
            with gzip.open(path, 'rt', newline='') as f:
                r = csv.reader(f); assert next(r) == ['u1','u2','u3','u4','determinant']
                assert [[int(x) for x in line] for line in r] == records
        summaries.append({'n': n, 'determinants': len(records), 'minimum': smallest})
    return summaries


def finite_exact(write: bool) -> dict:
    failures = []
    for n in range(1, 10):
        a = row(n); chain = [a]
        for j in range(1, 10):
            a = L(a); chain.append(a)
            if min(a) < 0:
                k = next(k for k, x in enumerate(a) if x < 0)
                failures.append({'n': n, 'first_negative_depth': j,
                                 'first_negative_index': k, 'value': str(a[k]),
                                 'chain': [[str(x) for x in layer] for layer in chain]})
                break
        else: raise AssertionError(('no expected failure', n))
    assert [f['first_negative_depth'] for f in failures] == [2,2,2,3,3,3,4,5,6]
    positive = []
    for n in range(4, 56):
        bound = 2 if n < 7 else 3
        a = row(n); chain = [a]
        for _ in range(bound):
            a = L(a); assert min(a) >= 0; chain.append(a)
        positive.append({'n': n, 'through_depth': bound,
                         'chain': [[str(x) for x in layer] for layer in chain]})
    assert L([1]) == [1]
    json_data('small_failures.json.gz', failures, write)
    json_data('finite_positive_chains.json.gz', positive, write)
    return {'failure_witnesses': [{k:v for k,v in f.items() if k != 'chain'} for f in failures],
            'positive_n4_to6_depth': 2, 'positive_n7_to55_depth': 3}


# Integer polynomial operations, coefficients in ascending powers of u.
def padd(a: list[int], b: list[int], factor: int = 1) -> list[int]:
    c = [0]*max(len(a),len(b))
    for i,x in enumerate(a): c[i] += x
    for i,x in enumerate(b): c[i] += factor*x
    while len(c)>1 and c[-1] == 0: c.pop()
    return c


def pmul(a: list[int], b: list[int]) -> list[int]:
    c = [0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j] += x*y
    while len(c)>1 and c[-1] == 0: c.pop()
    return c


def peval(a: list[int], u: int) -> int:
    result = 0
    for x in reversed(a): result = result*u+x
    return result


def boundary_certificates(write: bool) -> dict:
    N, K, J, M = 10, 8, 4, 13
    scale = math.factorial(M)
    falling = [[1]]
    for m in range(1,M+1): falling.append(pmul(falling[-1], [N-m+1,1]))
    a = []
    for k in range(M+1):
        p = [0]
        for j in range(k//2+1):
            denominator = math.factorial(j)*math.factorial(k-2*j)
            assert scale % denominator == 0
            p = padd(p, [x*(scale//denominator) for x in falling[k-j]])
        a.append(p)
    layers = []
    for r in range(J+1):
        assert len(a) == M+1-r
        assert all(p[0] > 0 and min(p) >= 0 for p in a)
        layers.append([p[:] for p in a])
        if r < J:
            a = [padd(pmul(a[k],a[k]), pmul(a[k-1],a[k+1]) if k else [0], -1)
                 for k in range(len(a)-1)]
    gaps = [padd(pmul(a[k],a[k]),pmul(a[k-1],a[k+1]),-3) for k in range(1,K+1)]
    assert all(g[0] > 0 and min(g) >= 0 for g in gaps)
    assert [len(g)-1 for g in gaps] == [32*k for k in range(1,K+1)]
    # Compare all retained polynomial entries with a separate integer-row construction.
    for u in (0,1,2,10):
        exact = row(N+u)
        for r, polys in enumerate(layers):
            assert all(peval(p,u) == scale**(2**r)*exact[k] for k,p in enumerate(polys))
            if r < J: exact = L(exact)
    obj = {'shift_n': N, 'initial_max_index': M, 'base_scale': str(scale),
           'scale_at_stage_r': 'base_scale ** (2 ** r)',
           'coefficient_order': 'ascending powers of u=n-10',
           'layers': [[[str(x) for x in p] for p in layer] for layer in layers],
           'stage4_3factor_gaps_k1_to8': [[str(x) for x in g] for g in gaps]}
    json_data('boundary_polynomials.json.gz', obj, write)
    return {'stage': J, 'indices': [1,K], 'degrees': [len(g)-1 for g in gaps],
            'layer_lengths': [len(x) for x in layers],
            'gap_coefficient_counts': [len(x) for x in gaps],
            'all_coefficients_nonnegative': True, 'all_constant_terms_positive': True}


def ceildiv(a: int, b: int) -> int:
    assert b > 0
    return -(-a//b)


def ratio_init(n: int, P: int) -> tuple[list[int],list[int]]:
    assert n >= 1 and P >= 1
    D = 1 << P; lo = [0]; hi = [0]; tl = tu = n*D
    for k in range(1,n):
        A, B = n-k, 2*n-k+1
        assert tl > 0
        lo.append(D*D*(A*tu+B*D)//((k+1)*tu*tu))
        hi.append(ceildiv(D*D*(A*tl+B*D),(k+1)*tl*tl))
        tl,tu = (D*(A*tu+B*D)//((k+1)*tu),
                 ceildiv(D*(A*tl+B*D),(k+1)*tl))
    assert tl > 0
    lo.append(D**3//(tu*tu)); hi.append(ceildiv(D**3,tl*tl))
    assert all(0 <= x <= y for x,y in zip(lo,hi))
    return lo,hi


def ratio_step(lo: list[int], hi: list[int], D: int) -> tuple[list[int],list[int]]:
    assert len(lo) == len(hi) and all(0 <= x <= y < D for x,y in zip(lo,hi))
    n = len(lo)-1; ll = [0]; uu = [0]
    for k in range(1,n+1):
        right = k+1 if k<n else k-1
        l,u = lo[k],hi[k]
        ll.append(l*l*(D-hi[k-1])*(D-hi[right])//(D*(D-l)**2))
        uu.append(ceildiv(u*u*(D-lo[k-1])*(D-lo[right]),D*(D-u)**2))
    assert all(0 <= x <= y for x,y in zip(ll,uu))
    return ll,uu


def ratio_certificate(n: int, P: int, max_depth: int = 30) -> dict:
    D = 1 << P; lo,hi = ratio_init(n,P); stats = []
    for j in range(max_depth+1):
        U = max(hi)
        stats.append({'j':j,'max_upper':str(U), 'min_lower_interior':str(min(lo[1:])),
                      'max_interval_width':str(max(y-x for x,y in zip(lo,hi)))})
        assert U < D, ('positivity not certified',n,j)
        if 3*U <= D:
            return {'n':n,'precision_bits':P,'depth':j,'stages':stats}
        lo,hi = ratio_step(lo,hi,D)
    raise AssertionError(('no stopping certificate',n,max_depth))


def ratio_crosschecks() -> int:
    # Bounds are compared with independently constructed, exact integer iterates.
    tests = list(range(10,41)) + [50,64,80,100,128]
    for n in tests:
        a = row(n); D = 1 << 256; lo,hi = ratio_init(n,256)
        for j in range(20):
            assert min(a) > 0
            for k in range(n+1):
                numerator = a[k-1]*a[k+1] if k else 0
                assert lo[k]*a[k]**2 <= D*numerator <= hi[k]*a[k]**2, (n,j,k)
            assert max(hi) < D
            if 3*max(hi) <= D: break
            a = L(a); lo,hi = ratio_step(lo,hi,D)
        else: raise AssertionError(n)
    return len(tests)


def interval_certificates(full: bool, write: bool) -> dict:
    path = DATA / 'interval_certificates.json'
    ns = list(range(10,1001)) + [2000,10000,100000]
    if full:
        results = [ratio_certificate(n,256 if n <= 10000 else 512) for n in ns]
        json_data('interval_certificates.json',results,write)
    else:
        results = json.loads(path.read_text())
        for n in [10,19,20,40,80,100,160,320,501,1000]:
            expected = next(r for r in results if r['n'] == n)
            assert expected == ratio_certificate(n,expected['precision_bits'])
    assert [r['n'] for r in results] == ns
    bounds = {10:(27,100),501:(11,50),1000:(11,50),2000:(11,50),10000:(3,10),100000:(3,20)}
    table = []
    for r in results:
        n = r['n']; D = 1 << r['precision_bits']
        assert r['depth'] == len(r['stages'])-1
        assert all(int(s['max_upper']) < D for s in r['stages'])
        U = int(r['stages'][-1]['max_upper']); assert 3*U <= D
        if n in bounds:
            p,q = bounds[n]; assert q*U <= p*D
            table.append({'n':n,'depth':r['depth'],'max_q_upper':f'{p}/{q}'})
    return {'number_of_certified_exponents':len(results),'representative_certificates':table,
            'full_interval_regeneration_performed':full}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--quick',action='store_true')
    group.add_argument('--full',action='store_true')
    parser.add_argument('--write-data',action='store_true')
    args = parser.parse_args()
    assert __debug__, 'Assertions must be enabled.'
    DATA.mkdir(exist_ok=True)
    t = time.time(); report = {'status':'NONE', 'python':sys.version.split()[0]}
    report['pf4'] = pf4_certificates(args.write_data)
    print('PASS: all 12,160 PF4 determinants, two independent algorithms.',flush=True)
    report['finite_exact'] = finite_exact(args.write_data)
    print('PASS: exact small failures and uniform-proof finite base range.',flush=True)
    report['boundary'] = boundary_certificates(args.write_data)
    print('PASS: integer polynomial coefficient certificates for the boundary strip.',flush=True)
    report['ratio_crosscheck_count'] = ratio_crosschecks()
    print('PASS: dyadic bounds checked against full exact integer rows/iterates.',flush=True)
    report['interval'] = interval_certificates(args.full,args.write_data)
    print('PASS: interval certificates ('+('all 994 regenerated' if args.full else 'selected regenerated; use --full for all')+').',flush=True)
    report['elapsed_seconds'] = round(time.time()-t,3)
    if args.write_data:
        (DATA/'verification_summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__ == '__main__': main()
