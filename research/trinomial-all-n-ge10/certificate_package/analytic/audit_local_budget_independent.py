if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
"""Independent stdlib positive-polynomial assembly, using independently regenerated moments."""
from fractions import Fraction as R
from collections import defaultdict
from pathlib import Path
from math import isqrt,prod
import ast,json
root=Path(__file__).parent
mom={ast.literal_eval(k):R(v) for k,v in json.loads((root/'LOCAL_HOMOTOPY_INDEPENDENT_MOMENTS.json').read_text()).items()}
Z=(0,)*7

def const(c):return {Z:R(c)}
def var(i):
 key=list(Z);key[i]=1
 return {tuple(key):R(1)}
def add(*polys):
 p=defaultdict(R)
 for q in polys:
  for k,c in q.items():p[k]+=c
 return dict(p)
def mul(*polys):
 p=const(1)
 for q in polys:
  out=defaultdict(R)
  for k,c in p.items():
   for l,d in q.items():out[tuple(a+b for a,b in zip(k,l))]+=c*d
  p=dict(out)
 return p
def scale(c,p):return {k:R(c)*v for k,v in p.items()}
def pw(p,n):return mul(*([p]*n))
A,B,C,D,Q,V,T=map(var,range(7));d=R(2,5)
e1=mul(V,add(scale(R(1,5),A),mul(B,add(scale(R(1,9),T),scale(9*d/160,pw(T,2)),scale(8*d*d/45,pw(T,3))))))
e2=mul(V,B,add(const(R(1,9)),scale(9*d/80,T),scale(8*d*d/15,pw(T,2))))
e3=mul(V,add(scale(R(9,80),C),scale(R(16,15),mul(T,D))))
e4=scale(R(16,15),mul(V,D))
f1=scale(R(1,6),mul(T,Q));f2=scale(R(1,6),Q);f3=scale(R(1,12),mul(T,Q,Q));f4=scale(R(1,12),mul(Q,Q))
# Derivative polynomials for exp(E): recursively Bell factors explicitly.
bell2=add(e2,pw(e1,2))
bell3=add(e3,scale(3,mul(e1,e2)),pw(e1,3))
bell4=add(e4,scale(4,mul(e1,e3)),scale(3,pw(e2,2)),scale(6,mul(e1,e1,e2)),pw(e1,4))
P=add(f4,scale(4,mul(f3,e1)),scale(6,mul(f2,bell2)),scale(4,mul(f1,bell3)),bell4)

def ceil_sqrt(q):
 k=isqrt(q.numerator//q.denominator)
 return R(k if k*k>=q else k+1)
def absbound(key):
 a,b,c,d,q=key
 if a%2==c%2==0:return mom[key]
 lo=list(key);hi=list(key)
 if a%2:
  lo[0]-=1;hi[0]+=1
 if c%2:
  if a%2:lo[2]+=1;hi[2]-=1
  else:lo[2]-=1;hi[2]+=1
 return ceil_sqrt(mom[tuple(lo)]*mom[tuple(hi)])
receipt=json.loads((root/'LOCAL_HOMOTOPY_TAU_BUDGET_RECEIPT.json').read_text())
rows={tuple(t['powers']):t for t in receipt['terms']}
assert set(rows)==set(P)
total=R(0);values={n:R(0) for n in (10,15,20,25)}
for exps,coeff in P.items():
 assert coeff>0
 idx=exps[:5];vp,tp=exps[5:];degree=sum(a*b for a,b in zip(idx,(3,4,5,6,2)))
 assert degree-2*vp>=4
 bound=absbound(idx);weight=R(1,prod(range(tp+1,tp+5)))
 base=8*weight*coeff*bound*R(16,15)**degree
 term=base*R(10)**(2*vp-degree+4);total+=term
 assert str(bound)==rows[exps]['moment_bound']
 assert str(weight)==rows[exps]['tauweight']
 assert str(term)==rows[exps]['C100_contribution']
 for n in values:values[n]+=base*R(n)**(2*vp-degree)
assert str(total)==receipt['C100'] and total<36821
for n,q in values.items():assert str(q)==receipt['one_saddle_bounds_at_square_V'][str(n*n)]
# Independently derive tail norm from six moments, then scalar Chernoff bounds.
b=R(19,20);aa,bb,cc=1/(12*b),1/(18*b*b),1/(50*b*b*b)
l2=aa*aa*mom[(0,0,0,0,2)]+bb*bb*mom[(0,2,0,0,0)]+cc*cc*mom[(4,0,0,0,0)]+2*aa*bb*mom[(0,1,0,0,1)]+2*aa*cc*mom[(2,0,0,0,1)]+2*bb*cc*mom[(2,1,0,0,0)]
assert l2==R(7405704307825,1693651716) and l2<67**2
cases=[(225,5,R(73,5),R(1,1000),R(4,125),R(11,500)),(400,7,R(97,5),R(1,10**8),R(1,10**4),R(1,25000)),(625,9,R(243,10),R(1,10**15),R(1,30*10**6),R(1,10**8))]
for vv,t,lower,goal,sqrtgoal,tailgoal in cases:
 assert lower*lower<R(19,20)*vv
 loss=t*R(2,5)*lower-R(15,32)*t*t
 term=den=R(1)
 for k in range(1,181):term*=loss/k;den+=term
 pref=32*prod(1+R(t*t,m) for m in (2,4,8,16))
 assert pref/den<goal and sqrtgoal*sqrtgoal>=goal
 assert 2*(goal+R(67,vv)*sqrtgoal)<tailgoal
assert R(269,300)>R(15,16)**2 and R(285,269)**45<16
out={'status':'PASS','moments_independently_regenerated':len(mom),'positive_terms_independently_assembled':len(P),'C100':str(total),'local_errors':{n*n:str(q) for n,q in values.items()},'tail_L2_squared':str(l2),'combined_bounds':{'225':'651/1000','400':'185/1000','625':'73/1000'},'actual_torus_complement_included':False}
assert values[15]+R(11,500)<R(651,1000)
assert values[20]+R(1,25000)<R(185,1000)
assert values[25]+R(1,10**8)<R(73,1000)
(root/'LOCAL_HOMOTOPY_INDEPENDENT_BUDGET_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
