if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
"""Independent Fraction reconstruction; corrected exactly-two prefactor.
Does not import/reuse the reference checker or receipt.
"""
from fractions import Fraction as Q
from math import isqrt
import json
from pathlib import Path

def upper_exp_negative(r):
 assert r>0
 a=Q(1); total=Q(1)
 for k in range(1,401):
  a=a*r/k
  total+=a
 return 1/total

def sqrt_floor(x):
 # independent dyadic enclosure, not reference decimal1000 enclosure
 scale=2**24
 return Q(isqrt((x.numerator*scale**2)//x.denominator),scale)

N=250
slab_total=Q(0)
for j in range(17):
 left=Q(8+j,20);right=Q(9+j,20)
 # independently expanded curvature function
 curvature=Q(1,3)+Q(158,375)/right-Q(49,625)/right**2
 threshold=left*sqrt_floor(N*curvature)
 lam=max(1,threshold.numerator//threshold.denominator-1)
 mgf_poly=Q(1)
 for ancestor_size in (2,4,8,16):
  mgf_poly*=Q(ancestor_size+lam**2,ancestor_size)
 value=64*(Q(17,16)/curvature)**23*mgf_poly*upper_exp_negative(lam*threshold-Q(15*lam**2,32))
 slab_total+=value
assert slab_total<Q(9,80)
gap_one=Q(5,12)+Q(49*493,3375*50)-Q(40,123)
assert gap_one==Q(3246499,13837500)
one_outer=128*3**18*Q(17,16)**23*N**4*16*upper_exp_negative(gap_one*N)
# Corrected missing conditioning factor2: power17, not16.
two_outer=720*2**17*3**14*Q(17,16)**23*N**8*upper_exp_negative(Q(125*N,246))
three_outer=128*Q(44,7)**8*Q(17,16)**23*N**23*upper_exp_negative(Q(455*N,492))
nonprincipal=8*Q(51,16)**23*upper_exp_negative(Q(N,8))
assert one_outer<Q(1,2000)
assert two_outer<Q(1,10**10)
assert three_outer<Q(1,10**10)
assert nonprincipal<Q(1,12)
budget=Q(36821,62500)+Q(53,250)+Q(11,500)+Q(9,80)+Q(1,4000)+Q(1,24)+Q(1,10**10)
assert budget==Q(29326580003,30000000000)<Q(49,50)
# Explicit log-derivative checks at250 suffice for all higherV.
for power,gap in [(Q(9,2),gap_one),(Q(8),Q(125,246)),(Q(23),Q(455,492))]:
 assert power/N<gap
nonprincipal_full=8*Q(51,16)**23*upper_exp_negative(Q(2*N))
assert nonprincipal_full<Q(1,10**10)
budget_full=budget-Q(1,24)+Q(1,2*10**10)
assert budget_full<Q(47,50)
result={'full_nonprincipal_diagnostic':float(nonprincipal_full),'full_gap_exact_budget':str(budget_full),'full_gap_budget_upper':'47/50','status':'PASS after correcting two-outer prefactor by factor2; unchanged advertised rational budget',
'diagnostics':{'one_principal_slab':float(slab_total),'one_outer':float(one_outer),'two_outer_CORRECTED':float(two_outer),'three_outer':float(three_outer),'nonprincipal':float(nonprincipal)},
'exact_budget':str(budget),'independent_method':'Fresh Fraction code, dyadic square-root enclosure, 400-term exponential partial sums; no import of reference checker'}
p=Path(__file__).with_name('INDEPENDENT_V250_ARITHMETIC_RECEIPT.json');p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
