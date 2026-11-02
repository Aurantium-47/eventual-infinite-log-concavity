"""Independent rational closure of the model tail and two-saddle budget.

Uses the NEW independent subtree moment implementation, not submitted code.
Mathematical use of the estimates is explained in the referee report.
"""
if not __debug__:
    raise RuntimeError('Assertions are required; do not use -O/-OO.')
from fractions import Fraction as F
from math import factorial,prod
from pathlib import Path
import importlib.util,json

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('referee_tree_moments',ROOT/'local/rederive_local.py')
tree=importlib.util.module_from_spec(spec)
spec.loader.exec_module(tree)

def atan_sum(x,N):
    return sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(N)),F(0))

def exp_lower(x,N):
    assert x>=0
    term,total=F(1),F(1)
    for k in range(1,N+1):
        term*=x/k;total+=term
    return total

# Machin's identity: the alternating sums provide actual bounds, not samples.
pi_lo=16*atan_sum(F(1,5),10)-4*atan_sum(F(1,239),11)
pi_hi=16*atan_sum(F(1,5),11)-4*atan_sum(F(1,239),10)
assert pi_lo*pi_lo>F(493,50)
assert pi_hi<F(22,7)
assert 1-(pi_hi/16)**2/2>F(49,50)
assert 1-(pi_hi/16+F(2,5))**2/2>F(3,4)
assert 1-(3*pi_hi/16)**2/2>F(3,4)
assert 4*(pi_lo/16)**2-10*(pi_hi/16)**4>F(1,8)
assert pi_hi*pi_hi/(32*(1-pi_hi*pi_hi/256))<F(40,123)

moments={k:tree.moment(k) for k in [
 (0,0,0,0,1),(0,1,0,0,0),(2,0,0,0,0),
 (0,0,0,0,2),(0,2,0,0,0),(4,0,0,0,0),
 (0,1,0,0,1),(2,0,0,0,1),(2,1,0,0,0)]}
first=[-moments[(0,0,0,0,1)]/12,
       moments[(0,1,0,0,0)]/24,
       -moments[(2,0,0,0,0)]/72]
assert first==[-F(16),F(1685,128),-F(315,32)]
cfirst=16*F(20,19)+F(1685,128)*F(4,3)*F(20,19)**2+F(315,32)*F(6,5)**2*F(20,19)**3
assert cfirst==F(2173895,41154) and cfirst<53
a,b,d=F(20,19)/12,F(20,19)**2/18,F(20,19)**3/50
l2=(a*a*moments[(0,0,0,0,2)]+b*b*moments[(0,2,0,0,0)]
    +d*d*moments[(4,0,0,0,0)]+2*a*b*moments[(0,1,0,0,1)]
    +2*a*d*moments[(2,0,0,0,1)]+2*b*d*moments[(2,1,0,0,0)])
assert l2==F(7405704307825,1693651716) and l2<67**2

# At V=225, sqrt(19V/20)>731/50. With t=5 and d=2/5 this
# turns the negative exponential into a certified rational upper bound.
sqrt_lo=F(731,50)
assert sqrt_lo**2 < F(19,20)*225
x=2*sqrt_lo-F(375,32)
P_upper=32*prod(1+F(25,m) for m in [2,4,8,16])/exp_lower(x,80)
assert P_upper<F(1,1000)
# sqrt(P)<4/125 follows from P<1/1000 < (4/125)^2.
assert F(1,1000)<F(4,125)**2
model_tail_upper=2*(F(1,1000)+F(67,225)*F(4,125))
assert model_tail_upper<F(11,500)

budget=F(36821,250**2)+F(53,250)+F(11,500)+F(1,2)*(F(9,40)+F(1,2000)+F(3,10**10))
assert budget==F(18717720003,20000000000) and budget<F(47,50)

# Parameter bridge uses this exact evaluation and the sign of 2s^2+2s-1.
sst=F(7,20)
vst=sst*(1+4*sst+sst*sst)/(1+sst+sst*sst)**2
assert vst==F(141260,346921) and 1001*vst>250
assert 2*sst*sst+2*sst-1<0

out={'status':'PASS','source':'new independent formulas; no author imports or receipts',
     'pi_interval':[str(pi_lo),str(pi_hi)],
     'first_correction_coefficients':list(map(str,first)),
     'first_correction_absolute_constant':str(cfirst),
     'weighted_model_tail_L2_squared':str(l2),
     'chernoff_P_upper_at_V225':str(P_upper),
     'chernoff_P_below_1_over_1000':True,
     'model_tail_upper':str(model_tail_upper),
     'model_tail_below_11_over_500':True,
     'bulk_relative_error_budget':str(budget),
     'margin_below_47_over_50':str(F(47,50)-budget),
     'sstar_bridge_value_at_7_over_20':str(vst)}
Path(__file__).with_name('model_and_assembly_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='chernoff_P_upper_at_V225'},indent=2))
