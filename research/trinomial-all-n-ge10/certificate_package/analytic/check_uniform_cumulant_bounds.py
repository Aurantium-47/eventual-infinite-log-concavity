if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
import sympy as S
from math import comb
import json,time
z,s,c,x,y=S.symbols('z s c x y');p=1+z+z*z;ps=1+s+s*s;qs=1+4*s+s*s
v=z*(1+4*z+z*z)/p**2
D=1-s*s+s**4+2*s*(1+s*s)*c+4*s*s*c*c

def norm2(P):
 a=S.Poly(P,z);terms=a.terms();out=0
 for (i,),ai in terms:
  for (j,),aj in terms:
   out+=ai*aj*s**(i+j)*S.chebyshevt(abs(i-j),c)
 return S.expand(out)
def bernstein_min(expr):
 poly=S.Poly(expr,x,y);ds,dc=poly.degree(x),poly.degree(y)
 a=[[S.Rational(0)]*(dc+1) for _ in range(ds+1)]
 for (i,j),q in poly.terms():a[i][j]=q
 b=[[sum(a[p][j]*S.Rational(comb(i,p),comb(ds,p)) for p in range(i+1)) for j in range(dc+1)] for i in range(ds+1)]
 out=[sum(b[i][q]*S.Rational(comb(j,q),comb(dc,q)) for q in range(j+1)) for i in range(ds+1) for j in range(dc+1)]
 return min(out),ds,dc
bounds={3:S.Rational(6,5),4:S.Rational(4,3),5:S.Rational(9,4),6:S.Rational(6),7:S.Rational(16),8:S.Rational(64)}
k=v;out=[]
for m in range(3,9):
 k=S.factor(z*S.diff(k,z));P=S.cancel(k*p**m/z);assert S.denom(P)==1
 A=S.expand(qs**2*D**m);B=S.expand(norm2(P)*ps**4)
 C=bounds[m];mins=[]
 for lo in range(4):
  E=S.Poly(S.expand((C*C*A-B).subs({s:(lo+x)/4,c:(49+y)/50},simultaneous=True)),x,y).as_expr()
  mn,ds,dc=bernstein_min(E);mins.append(mn)
 ok=min(mins)>=0
 assert ok, (m, mins)
 r={'m':m,'bound':str(C),'bernstein_minima':list(map(str,mins)),'degrees':[ds,dc],'pass':bool(ok)}
 out.append(r);print(json.dumps(r),flush=True)
print(json.dumps({'scope':'all s in[0,1], cos angle in[49/50,1]; exact Bernstein certificates only for PASS rows','results':out},indent=2))
