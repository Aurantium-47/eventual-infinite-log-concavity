"""Independent exact checks for the fixed manuscript's Section 6.

No submitted source code, certificate or saved receipt is imported.
Only Python integers and Fractions determine acceptance. The finite tree
check exhausts all 16 one-outer and 120 two-outer choices for the fixed
16-leaf tree. This does not re-run any finite exponent or edge certificate.
"""
if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not run with python -O")

from fractions import Fraction as F
from itertools import combinations
from math import isqrt, prod
from pathlib import Path
import hashlib
import json
import sys

sys.set_int_max_str_digits(0)
OUT = Path(__file__).resolve().parent

def sqrt_bracket(q, denominator=10**6):
    q=F(q)
    lo=isqrt(q.numerator*denominator**2//q.denominator)
    left,right=F(lo,denominator),F(lo+1,denominator)
    assert left**2<=q<right**2
    return left,right

def exp_minus_upper(x, terms=400):
    """e^-x < 1 / sum_(k=0)^terms x^k/k! for x>0."""
    x=F(x)
    assert x>0
    term=total=F(1)
    for k in range(1,terms+1):
        term*=x/k
        total+=term
    return 1/total

def small_upper(q, denominator=10**12):
    q=F(q)
    n=-((-q.numerator*denominator)//q.denominator)
    r=F(n,denominator)
    assert q<=r
    return str(r)

nodes=[]
for size in (2,4,8,16):
    for start in range(0,16,size):
        vector=[0]*16
        for i in range(start,start+size):
            vector[i]=1 if i<start+size//2 else -1
        nodes.append((size,tuple(vector)))
assert len(nodes)==15
assert prod(F(size,2) for size,_ in nodes)==2048
for i,(mi,vi) in enumerate(nodes):
    assert sum(vi)==0 and sum(x*x for x in vi)==mi
    for _,vj in nodes[i+1:]:
        assert sum(x*y for x,y in zip(vi,vj))==0

one_geometry=[]
for outer in range(16):
    intact=[(m,v) for m,v in nodes if v[outer]==0]
    assert len(intact)==11
    assert prod(F(m,2) for m,_ in intact)==32
    assert all(sum(v[i] for i in range(16) if i!=outer)==0 for _,v in intact)
    one_geometry.append(len(intact))

two_geometry=[]
for outer in combinations(range(16),2):
    intact=[(m,v) for m,v in nodes if all(v[i]==0 for i in outer)]
    assert len(intact)>=8
    assert all(m<=8 for m,_ in intact)
    keep=intact[:8]
    assert 2**7*prod(F(m,2) for m,_ in keep)<=2**23
    assert all(sum(v[i] for i in range(16) if i not in outer)==0 for _,v in keep)
    two_geometry.append(len(intact))

winding={}
for q in (0,1,2):
    angular_range=F(q)+F(16-q,3)
    odd=[j for j in range(-17,18,2) if abs(j)<=angular_range]
    assert odd==[-5,-3,-1,1,3,5]
    winding[str(q)]={"range_in_units_of_pi":str(angular_range),"possible_odd_sums":odd}

# Derive rational pi bounds with Machin's identity and alternating series.
def arctan_bracket(x, terms):
    x=F(x)
    assert 0<x<1
    partial=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(terms)),F(0))
    nxt=(-1)**terms*x**(2*terms+1)/F(2*terms+1)
    return min(partial,partial+nxt),max(partial,partial+nxt)

a_lo,a_hi=arctan_bracket(F(1,5),20)
b_lo,b_hi=arctan_bracket(F(1,239),8)
machin_lo,machin_hi=16*a_lo-4*b_hi,16*a_hi-4*b_lo
t2=2*F(1,5)/(1-F(1,5)**2)
t4=2*t2/(1-t2**2)
assert (t4-F(1,239))/(1+t4*F(1,239))==1
assert 0<4*a_lo-b_hi<4*a_hi-b_lo<1
# The angle above lies in (0,1), hence in (-pi/2,pi/2), where tan is injective.
# Its tangent is one, proving pi=16 atan(1/5)-4 atan(1/239).
pi_lo,pi_hi=F(333,106),F(22,7)
assert machin_lo>pi_lo and machin_hi<pi_hi
assert pi_lo**2>F(493,50)
assert pi_hi**2<10
assert F(19,48)*pi_hi<F(5,4)
assert 2*pi_hi/F(15)<F(2,3)**2
assert pi_hi**2*F(3,14)<4
assert 1-(pi_hi/16+F(2,5))**2/2>F(3,4)
assert 1-(3*pi_hi/16)**2/2>F(3,4)
assert (2*pi_hi/45)**2/16<F(1,100)
assert pi_hi**2/(32*(1-pi_hi**2/256))<F(40,123)

d=F(2,5)
g_at_d=F(19,40)*d**2-d**3/24-d**4/16
gp_at_d=F(19,20)*d-d**2/8-d**3/4
assert g_at_d==F(269,3750) and gp_at_d==F(43,125)
assert F(19,20)-d/12-d**2/8==F(269,300)

def gamma(r):
    return F(1,3)+F(158,375)/r-F(49,625)/r**2

assert gamma(d)==F(269,300)
assert F(98,625)-F(158,375)*d<0
assert gamma(F(5,4))>0

slabs=[]
slab_total=F(0)
V=F(250)
for j in range(17):
    ell=d+F(j,20)
    radius=ell+F(1,20)
    gam=gamma(radius)
    assert F(17,16)/gam>1
    root_lo,_=sqrt_bracket(V*gam,1000)
    t=max(1,(ell*root_lo).numerator//(ell*root_lo).denominator-1)
    loss=t*ell*root_lo-F(15,32)*t*t
    upper=64*(F(17,16)/gam)**23*prod(1+F(t*t,m) for m in (2,4,8,16))*exp_minus_upper(loss)
    slabs.append({"j":j,"ell":str(ell),"R":str(radius),"gamma":str(gam),"sqrt_lower":str(root_lo),"Chernoff_t":t,"loss_lower":str(loss),"certified_upper":small_upper(upper)})
    slab_total+=upper
assert slab_total<F(9,80)

# A theta-dependent lower bound sufficient for the nonprincipal sector gap.
# t -> 4t-10t^2 is increasing over the theta^2 interval used here.
theta2_lo=(pi_lo/16)**2
theta2_hi=(pi_hi/16)**2
assert theta2_hi<F(1,5)
assert 4*theta2_lo-10*theta2_lo**2>F(1,8)
nonprincipal=8*F(51,16)**23*exp_minus_upper(2*V)
assert nonprincipal<F(1,10**10)

# The one-outer angular loss: its minimum occurs at a=pi/3.
assert F(49,750)<F(1,6)
assert F(1,3)-F(49,4500)*pi_hi**2>0
assert F(2,3)>F(5,12)+F(49,3375)*pi_hi**2
delta1=F(5,12)+F(49,3375)*F(493,50)-F(40,123)
assert delta1==F(3246499,13837500)
_,sqrtV_upper=sqrt_bracket(V)
one_outer=128*3**18*F(17,16)**23*V**4*sqrtV_upper*exp_minus_upper(delta1*V)
assert one_outer<F(1,2000)
assert F(9,2)/V<delta1

delta2=2*F(5,12)-F(40,123)
assert delta2==F(125,246)
two_outer=720*2**17*3**14*F(17,16)**23*V**8*exp_minus_upper(delta2*V)
assert two_outer<F(1,10**10)
assert 8/V<delta2

delta3=3*F(5,12)-F(40,123)
assert delta3==F(455,492)
three_outer=128*F(44,7)**8*F(17,16)**23*V**23*exp_minus_upper(delta3*V)
assert three_outer<F(1,10**10)
assert 23/V<delta3

torus_claimed_cap=F(9,40)+F(1,2000)+F(3,10**10)
actual_exact_bound=2*slab_total+nonprincipal+one_outer+two_outer+three_outer
assert actual_exact_bound<torus_claimed_cap
out={
    "status":"PASS",
    "source_code_imported":False,
    "finite_exponents_checked":False,
    "saved_edge_certificates_replayed":False,
    "one_outer_cases":len(one_geometry),
    "two_outer_cases":len(two_geometry),
    "two_outer_intact_count_range":[min(two_geometry),max(two_geometry)],
    "winding_sector_bounds":winding,
    "slabs":slabs,
    "certified_rational_upper_bounds_at_V250":{
        "one_principal_sector":small_upper(slab_total),
        "four_nonprincipal_sectors":small_upper(nonprincipal,10**30),
        "one_outer_total":small_upper(one_outer),
        "two_outer_total":small_upper(two_outer,10**30),
        "three_or_more_outer_total":small_upper(three_outer,10**50),
        "whole_torus_complement_relative_one_saddle":small_upper(actual_exact_bound),
    },
    "advertised_torus_cap_relative_one_saddle":str(torus_claimed_cap),
    "scalar_estimates_3_4_3_5_3_7_are_mathematical_inputs":True,
    "all_V_ge250_extension":"Each Chernoff term decreases in V; each V^a exp(-delta V) has a/V-delta<0 at250 and thereafter.",
    "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(OUT/'torus_exact_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='slabs'},indent=2))
