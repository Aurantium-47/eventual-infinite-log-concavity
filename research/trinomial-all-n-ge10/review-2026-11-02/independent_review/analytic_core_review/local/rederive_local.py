"""Independent audit of the local saddle remainder (standard library only).

This program does not import any submitted code, log, moment list or receipt.
It derives the required moments from the fourth-derivative majorant.  Moments
are evaluated by a recursive split of the balanced binary tree, integrating
the root contrast and independent left/right subtrees.  Thus the evaluator
does not use the submission's 15-variable, bit-encoded expansion algorithm.

The eventual comparison with submitted numbers is a separate optional step;
none of those numbers is a mathematical premise in this calculation.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb, factorial, isqrt, prod
from pathlib import Path
import json
import time

HERE = Path(__file__).resolve().parent
if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled, without -O/-OO.')


def add(*polys):
    out = defaultdict(F)
    for p in polys:
        for e, c in p.items():
            out[e] += c
    return {e: c for e, c in out.items() if c}


def scale(c, p):
    return {e: c * v for e, v in p.items() if c * v}


def mul(p, q):
    out = defaultdict(F)
    for a, c in p.items():
        for b, d in q.items():
            out[tuple(x + y for x, y in zip(a, b))] += c * d
    return {e: c for e, c in out.items() if c}


def power(p, k):
    out = {(0,) * len(next(iter(p))): F(1)}
    for _ in range(k):
        out = mul(out, p)
    return out


def variable(i, n=7):
    e = [0] * n
    e[i] = 1
    return {tuple(e): F(1)}


def const(x, n=7):
    return {(0,) * n: F(x)}


# Nonnegative variables: A=|S3|, B=S4, C=|S5|, D=S6, Q, V, tau.
A, B, C, D, Q, V, T = [variable(i) for i in range(7)]
d = F(2, 5)
e1 = mul(V, add(scale(F(1, 5), A), mul(B, add(
    scale(F(1, 9), T), scale(F(9, 160) * d, power(T, 2)),
    scale(F(8, 45) * d * d, power(T, 3))))))
e2 = mul(mul(V, B), add(const(F(1, 9)),
    scale(F(9, 80) * d, T), scale(F(8, 15) * d * d, power(T, 2))))
e3 = mul(V, add(scale(F(9, 80), C), scale(F(16, 15), mul(T, D))))
e4 = scale(F(16, 15), mul(V, D))
e = [None, e1, e2, e3, e4]
f = [const(1), scale(F(1, 6), mul(T, Q)), scale(F(1, 6), Q),
     scale(F(1, 12), mul(T, power(Q, 2))), scale(F(1, 12), power(Q, 2))]

# Build complete exponential Bell polynomials by the recurrence
# B_(n+1) = sum_(k=0)^n binom(n,k) B_(n-k) E^(k+1).
bell = [const(1)]
for n in range(4):
    bell.append(add(*(scale(comb(n, k), mul(bell[n-k], e[k+1]))
                      for k in range(n+1))))
P = add(*(scale(comb(4, k), mul(f[k], bell[4-k])) for k in range(5)))


def cs_pair(key):
    """Return two polynomial-moment exponents whose geometric mean bounds key."""
    a, b, c, d6, q = key
    if a % 2 == 0 and c % 2 == 0:
        return key, key
    low, high = list(key), list(key)
    if a % 2:
        low[0] -= 1
        high[0] += 1
    if c % 2:
        low[2] += 1 if a % 2 else -1
        high[2] += -1 if a % 2 else 1
    assert all(x >= 0 for x in low + high)
    assert low[0] % 2 == low[2] % 2 == high[0] % 2 == high[2] % 2 == 0
    assert all(x + y == 2 * z for x, y, z in zip(low, high, key))
    return tuple(low), tuple(high)


required = set()
for exps, coeff in P.items():
    assert coeff > 0
    key = exps[:5]
    degree = sum(x*y for x, y in zip(key, (3, 4, 5, 6, 2)))
    assert degree - 2 * exps[5] >= 4
    required.update(cs_pair(key))
# Model first correction and the six terms of its L2 norm are also checked.
extra = {(0, 0, 0, 0, 1), (0, 1, 0, 0, 0), (2, 0, 0, 0, 0),
         (0, 0, 0, 0, 2), (0, 2, 0, 0, 0), (4, 0, 0, 0, 0),
         (0, 1, 0, 0, 1), (2, 0, 0, 0, 1), (2, 1, 0, 0, 0)}
remainder_required = required.copy()
required |= extra


@lru_cache(None)
def dfact(k):
    assert k % 2 == 1 and k >= 1
    return prod(range(1, k + 1, 2))


# Tree moment evaluator.  Each node of size m has contrast D with
# E[D^(2r)] = (2r+1)!! m^r.  All contrasts are independent.
# Child power sums here use scaled leaf coordinates X_i=16 eta_i, so all
# coefficients are integers.  At a split, X_i = Y_i +/- (16/m)D.
# Exponents represent (sum X^2, sum X^3, sum X^4, sum X^5, sum X^6, Q).
WEIGHTS = (2, 3, 4, 5, 6, 2)


def integer_multiply(a, b):
    out = defaultdict(int)
    for x, c in a.items():
        for y, d0 in b.items():
            out[tuple(i+j for i, j in zip(x, y))] += c*d0
    return {x: c for x, c in out.items() if c}


@lru_cache(None)
def root_forms(m):
    # 13 coordinates: D, left's six statistics, right's six statistics.
    z = (0,) * 13
    forms = []
    shift = 16 // m
    for k in range(2, 7):
        out = defaultdict(int)
        if k % 2 == 0:
            e0 = list(z); e0[0] = k
            out[tuple(e0)] += m * shift**k
        for j in range(2, k + 1):
            # Child odd power sums vanish identically when child size is two.
            if m == 4 and j % 2:
                continue
            for side in (0, 1):
                ek = list(z)
                ek[0] = k-j
                ek[1 + side*6 + (j-2)] = 1
                out[tuple(ek)] += comb(k, j)*shift**(k-j)*((-1)**(k-j) if side else 1)
        forms.append(dict(out))
    out = {}
    for i, power0 in ((0, 2), (6, 1), (12, 1)):
        ek = list(z); ek[i] = power0; out[tuple(ek)] = 1
    forms.append(out)
    return tuple(forms)


calls = defaultdict(int)


@lru_cache(None)
def tree_moment(m, exps):
    calls[m] += 1
    degree = sum(x*y for x, y in zip(exps, WEIGHTS))
    if degree % 2:
        return 0
    if not any(exps):
        return 1
    if m == 2:
        # Leaves have coordinates +/- 8D.  Odd power sums are identically 0.
        if exps[1] or exps[3]:
            return 0
        dp = 2*exps[0] + 4*exps[2] + 6*exps[4] + 2*exps[5]
        coeff = 2**(exps[0]+exps[2]+exps[4]) * 8**(dp-2*exps[5])
        return coeff * dfact(dp+1) * 2**(dp//2)
    polynomial = {(0,)*13: 1}
    forms = root_forms(m)
    for i, k in enumerate(exps):
        for _ in range(k):
            polynomial = integer_multiply(polynomial, forms[i])
    ans = 0
    for powers, coeff in polynomial.items():
        p0, left, right = powers[0], powers[1:7], powers[7:13]
        if p0 % 2:
            continue
        if sum(a*b for a,b in zip(left, WEIGHTS)) % 2:
            continue
        if sum(a*b for a,b in zip(right, WEIGHTS)) % 2:
            continue
        lv = tree_moment(m//2, left)
        if not lv:
            continue
        rv = tree_moment(m//2, right)
        if rv:
            ans += coeff * dfact(p0+1) * m**(p0//2) * lv * rv
    return ans


def moment(key):
    a,b,c,d6,q = key
    numerator = tree_moment(16, (0,a,b,c,d6,q))
    return F(numerator, 16**(3*a+4*b+5*c+6*d6))


def ceil_sqrt(x):
    k = isqrt(x.numerator // x.denominator)
    return k if F(k*k) == x else k+1


if __name__ == '__main__':
    started = time.time()
    # Independent coordinate normalization checks, not taken from a receipt.
    contrast = []
    sizes = []
    for m in (2, 4, 8, 16):
        for start in range(0, 16, m):
            row = [0]*16
            for i in range(start, start+m):
                row[i] = 1 if i < start+m//2 else -1
            contrast.append(row); sizes.append(m)
    assert len(contrast) == 15
    assert all(sum(row) == 0 for row in contrast)
    for i, row in enumerate(contrast):
        for j, col in enumerate(contrast):
            assert sum(a*b for a,b in zip(row,col)) == (sizes[i] if i == j else 0)
    assert prod(m//2 for m in sizes) == 2048
    assert F(tree_moment(16,(1,0,0,0,0,0)),16**2) == 45
    assert F(269,300) > F(15,16)**2
    assert F(285,269)**45 < 16
    assert 1-F(167,280)**2/2 > F(3,4)
    correction_bound = (16*F(20,19) + F(1685,128)*F(4,3)*F(20,19)**2
                        + F(315,32)*F(6,5)**2*F(20,19)**3)
    assert correction_bound == F(2173895,41154) and correction_bound < 53
    print('Derived positive terms:',len(P),'remainder moment requirements:',len(remainder_required),
          'including correction/tail requirements:',len(required),flush=True)
    moments = {}
    for key in sorted(required, key=lambda k:(sum(x*y for x,y in zip(k,(3,4,5,6,2))),k)):
        t0=time.time(); moments[key]=moment(key)
        print('moment',key,str(moments[key]),'seconds',round(time.time()-t0,3),flush=True)
    terms=[];total=F(0)
    for exps, coeff in sorted(P.items()):
        key=exps[:5]; lo,hi=cs_pair(key)
        bound=moments[key] if lo==hi else F(ceil_sqrt(moments[lo]*moments[hi]))
        degree=sum(x*y for x,y in zip(key,(3,4,5,6,2)))
        vp,tp=exps[5:]
        tau_weight=F(factorial(tp),factorial(tp+4))
        contribution=8*coeff*tau_weight*bound*F(16,15)**degree*F(10)**(2*vp-degree+4)
        total+=contribution
        terms.append({'powers':exps,'coefficient':str(coeff),'angular_degree':degree,
          'cs_moments':[lo,hi],'moment_bound':str(bound),'tau_weight':str(tau_weight),
          'C100_contribution':str(contribution)})
    alpha,beta,gamma=F(20,19)/12,F(20,19)**2/18,F(20,19)**3/50
    l2=(alpha**2*moments[(0,0,0,0,2)]+beta**2*moments[(0,2,0,0,0)]
        +gamma**2*moments[(4,0,0,0,0)]+2*alpha*beta*moments[(0,1,0,0,1)]
        +2*alpha*gamma*moments[(2,0,0,0,1)]+2*beta*gamma*moments[(2,1,0,0,0)])
    assert total < 36821
    assert l2 < 67**2
    result={'source_inputs':'Equations (5.4)-(5.6); no imported submitted receipts or code',
      'method':'balanced subtree moment recursion with independent root contrast integration',
      'positive_terms':len(P),'required_remainder_moments':len(remainder_required),
      'required_moments_with_correction_and_tail':len(required),
      'moments':{str(k):str(v) for k,v in moments.items()},'terms':terms,
      'C100':str(total),'C100_less_than_36821':total<36821,
      'model_tail_L2_squared':str(l2),'model_tail_L2_below_67_squared':l2<67**2,
      'geometry_checks':'15 orthogonal mean-zero contrasts, H constant 2048, E S2=45',
      'first_correction_absolute_bound':str(correction_bound),
      'tree_moment_cache':str(tree_moment.cache_info()),'calls_by_size':dict(calls),
      'seconds':round(time.time()-started,3)}
    (HERE/'local_independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('C100',total,'<36821:',total<36821,flush=True)
    print('L2 squared',l2,'<4489:',l2<67**2,flush=True)
    print('seconds',result['seconds'],'calls',dict(calls),flush=True)
