"""Independent log-series reconstruction and whole-panel check for (7,22).

No submitted code or supplement program is imported. The initial coefficients
come from exp(sum_l c_l u^(l-1) z^l), not the published three-term recurrence
or the supplement's generalized multinomial formula. Exact rational polynomial
arithmetic uses python-flint==0.9.0. Bounds and acceptance use exact rationals.
"""
if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
from pathlib import Path
from fractions import Fraction as F
from math import comb
import argparse, gzip, hashlib, json, sys, time
import flint
from flint import fmpq, fmpq_poly

sys.set_int_max_str_digits(0)
assert flint.__version__ == "0.9.0"
parser=argparse.ArgumentParser()
parser.add_argument("edge",type=Path)
parser.add_argument("--minimum-receipt",type=Path)
args=parser.parse_args()
start=time.monotonic()
panel,node=7,22
record=next(json.loads(line) for line in gzip.open(args.edge/"jets_panel7.jsonl.gz","rt") if json.loads(line)["node"]==node)
assert record["panel"]==panel and record["K"]==108 and record["d"]==86
K,D=record["K"],record["d"]
table=json.loads((args.edge/"nodes.json").read_text())
ends=list(map(F,table["u_endpoints"]))
assert ends==[F(i,32032) for i in range(9)]
c,h=(ends[7]+ends[8])/2,(ends[8]-ends[7])/2
assert c==F(15,64064) and h==F(1,64064)
nd=next(row for row in table["nodes"] if row["node"]==node)
left,right=map(F,nd["endpoints"][7:9])
assert left>0 and right>0
fq=lambda x:fmpq(str(x))
zero=fmpq_poly([])
one=fmpq_poly([1])
u=fmpq_poly([fq(c),fq(h)])
def mul(a,b):
    return (a*b).truncate(D+1)
powers=[one]
for j in range(K+4):
    powers.append(mul(powers[-1],u))
coeff=[one]
# z*g'_u(z)=g_u(z)*sum_l (l*c_l)*u^(l-1)*z^l,
# where l*c_l = 1 unless 3 divides l, then -2.
for k in range(1,K+5):
    val=fmpq_poly([])
    for ell in range(1,k+1):
        val=val+mul(powers[ell-1],coeff[k-ell])*(-2 if ell%3==0 else 1)
    coeff.append(val/k)
for level in range(4):
    coeff=[mul(v,v)-mul(coeff[k-1] if k else zero,coeff[k+1]) for k,v in enumerate(coeff[:-1])]
assert len(coeff)==K+1
tc=2/(1/left+1/right)
beta=(1/right-1/left)*tc/2
x=fmpq_poly([fq(-tc**16*comb(15+j,j)*(-beta)**j) for j in range(D+1)])
evaluated=zero
for v in reversed(coeff):
    evaluated=mul(evaluated,x)+v

unit=fmpq(2)**(record["exponent"]-record["precision"])
checks=[]
claimed={}
if args.minimum_receipt:
    old=json.loads(args.minimum_receipt.read_text())["case"]
    assert (old["panel"],old["node"],old["K"])==(panel,node,K)
    claimed={r["order"]:r["exact_value_sha256"] for r in old["orders"]}
    assert set(claimed)==set(range(D+1))
for j in range(D+1):
    exact=evaluated[j]
    assert (record["m"][j]-record["radius"])*unit<=exact<=(record["m"][j]+record["radius"])*unit
    digest=hashlib.sha256(str(exact).encode()).hexdigest()
    if claimed:
        assert digest==claimed[j]
    checks.append({"order":j,"contained":True,"exact_value_sha256":digest,
                   "numerator_bits":exact.numerator.bit_length(),
                   "denominator_bits":exact.denominator.bit_length()})

# Independent direct power-to-Bernstein conversion of the ACTUAL rational
# Taylor polynomial, with no interval roundoff term needed.
power=fmpq_poly([])
affine=fmpq_poly([-1,2])
for j in reversed(range(D+1)):
    power=power*affine+fmpq_poly([evaluated[j]])
controls=[]
for i in range(D+1):
    controls.append(sum((power[k]*fmpq(comb(i,k),comb(D,k)) for k in range(i+1)),fmpq(0)))
signed_bound=min(controls) if node%2==0 else -max(controls)
assert signed_bound>0

# Independent analytic majorant. At the real center we use the elementary
# log p(q)<=q+q^2/2, rather than the submitted 16-term logarithm routine.
radius=4*h
a=beta/h
assert abs(a)*radius<1
T=tc/(1-abs(a)*radius)
R=T+1
q=(c+radius)*R
assert 0<q<1 and 0<h<radius and R>T
H=sum((F((2 if ell%3==0 else 1)*(ell-1),ell)*q**(ell-2) for ell in range(2,33)),F(0))+2*q**31/(1-q)
E=R+c*R*R/2+radius*R*R*H
log2_lower=2*sum((F(1,(2*j+1)*3**(2*j+1)) for j in range(10)),F(0))
ceil=lambda z:-((-z.numerator)//z.denominator)
pow2=lambda e:F(1<<e) if e>=0 else F(1,1<<(-e))
M=pow2(15+ceil(16*E/log2_lower))/(1-(T/R)**16)
taylor_error=M*(h/radius)**(D+1)/(1-h/radius)
T0=max(left,right)
R0=2*T0
U=c+h
assert 0<=c-h and U*R0<1
E0=R0+U*R0*R0/2
coefficient_tail=pow2(15+ceil(16*E0/log2_lower)-16*(K+1))/(1-F(1,2**16))
errors=fq(taylor_error+coefficient_tail)
assert signed_bound>errors
relative=(signed_bound-errors)/signed_bound
rel=F(str(relative))
rel_floor=F((rel.numerator*10**12)//rel.denominator,10**12)
assert rel_floor>0

result={
 "status":"PASS",
 "method":"independent logarithmic-series coefficient recurrence, exact rational four L maps, actual Taylor Bernstein controls, separate Cauchy/coefficient tails",
 "imports_author_or_supplement_code":False,
 "shared_exact_arithmetic_library":"python-flint 0.9.0",
 "panel":panel,"node":node,"K":K,"d":D,
 "all_retained_taylor_coefficients_recomputed":D+1,
 "all_87_match_supplement_exact_value_hashes":bool(claimed),
 "whole_closed_panel_sign_independently_certified":True,
 "whole_panel_interval":[str(c-h),str(c+h)],
 "required_sign":1 if node%2==0 else -1,
 "relative_sign_margin_certified_lower":str(rel_floor),
 "complex_disk_q":str(q),
 "real_tail_domain_U_R0":str(U*R0),
 "elapsed_seconds":time.monotonic()-start,
 "checks":checks,
 "source_data_sha256":{
  "nodes.json":hashlib.sha256((args.edge/"nodes.json").read_bytes()).hexdigest(),
  "jets_panel7.jsonl.gz":hashlib.sha256((args.edge/"jets_panel7.jsonl.gz").read_bytes()).hexdigest()},
 "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 "scope":"one whole panel/node only; not all1929, no bypass or full theorem by this computation"}
out=Path(__file__).with_name("independent_minimum_result.json")
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="checks"},indent=2))

