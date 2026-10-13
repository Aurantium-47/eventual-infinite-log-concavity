#!/usr/bin/env python3
"""Exact certificates for eventual infinite log-concavity of polynomial powers.

Python 3.10+, standard library only. Do not use python -O.
  python code/verify.py                   # regenerate and compare the new certificates
  python code/verify.py --write-data      # regenerate the new stored certificates
  python code/verify.py --baseline        # also rerun the complete earlier verifier

The finite Poisson certificate uses a shrinking prefix, NOT zero extension at
its artificial right edge. All comparisons use integers. This program does not
enumerate the enormous exponent interval left open in the research report.
"""
from __future__ import annotations
import argparse, gzip, json, math, pathlib, subprocess, sys, time
from fractions import Fraction
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def ceildiv(a: int, b: int) -> int:
    assert b > 0
    return -(-a // b)


def ceil_log2(a: int) -> int:
    assert a > 0
    return (a - 1).bit_length()


def poisson_init(max_index: int, precision: int) -> tuple[list[int], list[int]]:
    assert max_index >= 1 and precision >= 1
    D = 1 << precision
    lo = [D*k // (k+1) for k in range(max_index+1)]
    hi = [ceildiv(D*k, k+1) for k in range(max_index+1)]
    return lo, hi


def prefix_step(lo: list[int], hi: list[int], D: int) -> tuple[list[int], list[int]]:
    assert len(lo) == len(hi) and len(lo) >= 3
    assert lo[0] == hi[0] == 0
    assert all(0 <= l <= u < D for l, u in zip(lo, hi))
    ll, uu = [0], [0]
    # The previous last index is discarded, not assigned a false zero neighbor.
    for k in range(1, len(lo)-1):
        l, u = lo[k], hi[k]
        ll.append(l*l*(D-hi[k-1])*(D-hi[k+1]) // (D*(D-l)**2))
        uu.append(ceildiv(u*u*(D-lo[k-1])*(D-lo[k+1]), D*(D-u)**2))
    assert all(0 <= l <= u for l, u in zip(ll, uu))
    return ll, uu


def poisson_certificate() -> dict:
    P, M, target, max_depth = 256, 2064, 2047, 16
    D = 1 << P
    lo, hi = poisson_init(M, P)
    hits, layers = {}, []
    for j in range(max_depth+1):
        assert len(lo) == M+1-j and len(lo) > target+1
        assert all(0 <= l <= u < D for l, u in zip(lo, hi))
        for k in range(1, target+1):
            if k not in hits and 3*hi[k] < D:
                assert j <= ceil_log2(8*k)
                hits[k] = {"k": k, "depth": j, "lower": str(lo[k]),
                           "upper": str(hi[k]), "strict_gap_D_minus_3upper": str(D-3*hi[k])}
        layers.append({"depth": j, "retained_max_index": len(lo)-1,
                       "maximum_upper": str(max(hi)),
                       "minimum_positive_index_lower": str(min(lo[1:])),
                       "maximum_interval_width": str(max(u-l for l, u in zip(lo, hi))),
                       "number_of_certified_target_indices": len(hits)})
        if len(hits) == target:
            break
        lo, hi = prefix_step(lo, hi, D)
    assert len(hits) == target and j == 12
    assert [s["number_of_certified_target_indices"] for s in layers] == [
        0, 0, 2, 6, 13, 27, 56, 115, 231, 464, 930, 1862, 2047]
    return {"initial_sequence": "u_k=1/k!, k>=0; u_k=0 for k<0",
            "initial_ratio": "q_k=k/(k+1), including q_0=0",
            "precision_bits": P, "denominator": str(D),
            "initial_max_ratio_index": M, "target_max_index": target,
            "last_depth": j, "layers": layers,
            "certificates": [hits[k] for k in range(1, target+1)]}


def L_prefix(a: list[int]) -> list[int]:
    assert len(a) >= 2
    return [a[k]*a[k] - (a[k-1]*a[k+1] if k else 0)
            for k in range(len(a)-1)]


def independent_integer_crosscheck() -> dict:
    # Integer coefficients of M! / k!, transformed directly by the defining L.
    # Geometric/global scaling does not affect the ratios.
    M, J, P = 64, 8, 256
    S, D = math.factorial(M), 1 << P
    a = [S // math.factorial(k) for k in range(M+1)]
    lo, hi = poisson_init(M, P)
    comparisons = 0
    layer_records = []
    for j in range(J+1):
        assert min(a) > 0
        for k in range(len(a)-1):
            num = a[k-1]*a[k+1] if k else 0
            den = a[k]*a[k]
            assert lo[k]*den <= D*num <= hi[k]*den, (j,k)
            comparisons += 1
        layer_records.append({"depth":j, "max_coefficient_index":len(a)-1,
                              "number_of_ratio_comparisons":len(a)-1,
                              "max_coefficient_bit_length":max(x.bit_length() for x in a)})
        if j < J:
            a = L_prefix(a)
            lo, hi = prefix_step(lo,hi,D)
    assert comparisons == sum(M-j for j in range(J+1))
    return {"initial_scale":str(S), "initial_max_index":M,
            "through_depth":J, "ratio_comparisons":comparisons, "layers":layer_records}


def padd(a: list[int], b: list[int], factor: int=1) -> list[int]:
    c = [0]*max(len(a),len(b))
    for i,x in enumerate(a): c[i] += x
    for i,x in enumerate(b): c[i] += factor*x
    while len(c)>1 and c[-1]==0: c.pop()
    return c


def pmul(a: list[int], b: list[int]) -> list[int]:
    c = [0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j] += x*y
    while len(c)>1 and c[-1]==0: c.pop()
    return c


def peval(a: list[int], x: int) -> int:
    value = 0
    for y in reversed(a): value = value*x+y
    return value


def trinomial_row(n: int) -> list[int]:
    a = [1]
    for _ in range(n):
        b = [0]*(len(a)+2)
        for k,x in enumerate(a):
            b[k] += x; b[k+1] += x; b[k+2] += x
        a = b
    return a


def L_full(a: list[int]) -> list[int]:
    return [x*x-(a[k-1]*a[k+1] if 0<k<len(a)-1 else 0)
            for k,x in enumerate(a)]


def polynomial_crosscheck() -> dict:
    M, J = 12, 4
    S = math.factorial(M)
    falling = [[1]]
    for m in range(1,M+1): falling.append(pmul(falling[-1],[-m+1,1]))
    polys = []
    for m in range(M+1):
        p = [0]
        norm_term_bound = 0
        for j in range(m//2+1):
            d = math.factorial(j)*math.factorial(m-2*j)
            assert S % d == 0
            p = padd(p,[x*(S//d) for x in falling[m-j]])
            norm_term_bound += math.comb(m-j,j)
        assert sum(abs(x) for x in p) <= S*norm_term_bound <= S*2**m
        polys.append(p)
    poisson = [S//math.factorial(k) for k in range(M+1)]
    layers = []
    for r in range(J+1):
        scale = S**(2**r)
        norm_bound = 2**((M+1)*2**r-1)
        assert len(polys)==len(poisson)==M+1-r
        for k,p in enumerate(polys):
            assert len(p)-1 == k*2**r
            assert p[-1] == poisson[k] > 0
            assert sum(abs(x) for x in p) <= scale*norm_bound
        for n in (0,1,5,10,20,50):
            exact = trinomial_row(n)
            for _ in range(r): exact=L_full(exact)
            for k,p in enumerate(polys):
                actual=exact[k] if k<len(exact) else 0
                assert peval(p,n)==scale*actual,(n,r,k)
        layers.append({"depth":r, "polynomials_scaled_by":str(scale),
                       "coefficients_ascending_powers_of_n":[[str(x) for x in p] for p in polys]})
        if r<J:
            polys=[padd(pmul(p,p),pmul(polys[k-1],polys[k+1]) if k else [0],-1)
                   for k,p in enumerate(polys[:-1])]
            poisson=L_prefix(poisson)
    return {"max_initial_index":M, "through_depth":J,
            "description":"Structural cross-checks of the general leading-term and coefficient-norm proof; not a substitute for that proof.",
            "layers":layers}


def constant_checks() -> dict:
    F=Fraction
    assert F(81,16)>4
    assert 16*F(8,9)**2+6*F(8,9)+3<21
    assert F(7,3)/(1-F(8,9))==21
    assert 42/(1-F(1,4))==56
    assert 1-F(56,256)==F(25,32)
    assert F(25,32)*4==F(25,8)>3
    assert F(800,3)>=256
    assert F(2048,8)>=256
    assert 8*24**2+F(24**2,2)==4896
    assert 192<2**8
    assert 10000-2*4896-8==200
    assert 6*F(9,8)<8
    B=1<<20001; J=ceil_log2(8*B); M=B+J+1
    assert J==20004 and M < (1<<20002)
    assert 20003 < (1<<15)
    assert 20018+(J+1)==40023
    assert 40024<40100
    return {"holo_mu_R_squared_minimum":256,
            "holo_error_constant":56,
            "trinomial_variance_threshold":"2^20000",
            "trinomial_initial_scaled_curvature_disk_radius":20,
            "gaussian_relative_error_on_radius_24_upper":"2^-200",
            "bulk_boundary_width":"B=2^20001",
            "finite_boundary_max_depth":J,
            "finite_boundary_initial_max_index":"M=B+20005",
            "symbolic_auxiliary_cutoff":"2*(2^(M+1)*M!)^(2^20005)",
            "proved_convenient_cutoff":"2^(2^40100)",
            "cutoff_evaluated_or_enumerated":False}


def compare_or_write(name: str, data: object, write: bool) -> None:
    path=DATA/name
    if write:
        with gzip.open(path,'wt',encoding='utf-8') as f:
            json.dump(data,f,separators=(',',':'))
    else:
        with gzip.open(path,'rt',encoding='utf-8') as f:
            expected=json.load(f)
        assert data==expected,('data mismatch',name)


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-data',action='store_true')
    parser.add_argument('--baseline',action='store_true')
    args=parser.parse_args()
    if not __debug__:
        raise RuntimeError('Run without -O: assertions are part of the verifier.')
    DATA.mkdir(exist_ok=True)
    start=time.time()
    pc=poisson_certificate()
    compare_or_write('poisson_certificates.json.gz',pc,args.write_data)
    print('PASS: strict local 3-factor certificates at all Poisson indices 1..2047; maximum depth 12.',flush=True)
    ic=independent_integer_crosscheck()
    compare_or_write('poisson_integer_crosscheck.json.gz',ic,args.write_data)
    print(f'PASS: {ic["ratio_comparisons"]} interval comparisons with independent exact integer iterates.',flush=True)
    pp=polynomial_crosscheck()
    compare_or_write('polynomial_crosscheck.json.gz',pp,args.write_data)
    print('PASS: exact polynomial leading coefficients, norm bounds, and evaluation cross-checks.',flush=True)
    cc=constant_checks()
    compare_or_write('constant_checks.json.gz',cc,args.write_data)
    print('PASS: rational constants and symbolic cutoff exponent bounds.',flush=True)
    if args.baseline:
        baseline=ROOT/'baseline'/'verify.py'
        assert baseline.exists(), 'The packaged baseline verifier is missing.'
        proc=subprocess.run([sys.executable,str(baseline),'--full'],capture_output=True,text=True)
        (DATA/'baseline_recheck_current.log').write_text(proc.stdout+proc.stderr)
        assert proc.returncode==0,proc.stdout+proc.stderr
        print('PASS: complete baseline verification, all 994 exponent certificates regenerated.',flush=True)
    summary={"status_for_original_threshold_10_target":"NONE",
             "poisson_target_indices":pc['target_max_index'],"poisson_last_depth":pc['last_depth'],
             "independent_integer_ratio_comparisons":ic['ratio_comparisons'],
             "baseline_rechecked_this_run":args.baseline,
             "cutoff_claim":"Analytical proof, not finite enumeration; see the manuscript.",
             "python":sys.version.split()[0],"elapsed_seconds":round(time.time()-start,3)}
    if args.write_data:
        (DATA/'verification_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
