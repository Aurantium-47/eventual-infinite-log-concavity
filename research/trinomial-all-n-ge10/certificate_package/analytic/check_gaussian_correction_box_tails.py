if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
from fractions import Fraction as F
from math import prod
import json
from pathlib import Path

def exp_lower(x,N=180):
 term=total=F(1)
 for k in range(1,N+1):term*=x/k;total+=term
 return total
cases=[(225,5,F(2797,160),F(1,1000)),(400,7,F(25081,800),F(1,10**8)),(625,9,F(39609,800),F(1,10**15))]
rows=[]
for V,t,loss,goal in cases:
 const=32*prod(1+F(t*t,m) for m in (2,4,8,16))
 upper=const/exp_lower(loss)
 assert upper<goal
 rows.append({'V_at_least':V,'Chernoff_t':t,'loss_lower':str(loss),'tail_probability_bound':str(goal),'verified_by_positive_exponential_partial_sum_terms':180})
L2=F(7405704307825,1693651716)
assert L2<67**2
assert 2*(F(1,1000)+F(67,225)*F(4,125))<F(11,500)
assert 2*(F(1,10**8)+F(67,400)*F(1,10**4))<F(1,25000)
assert 2*(F(1,10**15)+F(67,625)*F(1,30*10**6))<F(1,10**8)
receipt={'scope':'Gaussian plus first-correction integral outside coordinate saddle box d=2/5; not actual torus tails','L2_constant_squared':str(L2),'cases':rows,'per_saddle_error_bounds':{'V>=225':'11/500','V>=400':'1/25000','V>=625':'1/100000000'},'original_target_solved':False}
Path(__file__).with_name('GAUSSIAN_CORRECTION_BOX_TAIL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('All exact Chernoff and correction-tail bounds PASS')
