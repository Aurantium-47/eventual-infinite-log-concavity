if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
"""Independent exact certificate reconstruction and scalar bounds. No author code imported."""
from fractions import Fraction as F
from math import comb,isqrt,prod
from pathlib import Path
import json
import sympy as S
root=Path(__file__).parent
# Derive curvature numerator and reconstruct all Bernstein coefficients.
u,y,t,c=S.symbols('u y t c')
a=t*c+1;b2=(t*t-4)*(1-c*c)
D=a*a+b2;R=(a+3)*a*a+(a-3)*b2
poly=S.Poly(S.expand((3*R*(t+1)**2-(t+4)*D**2).subs({t:u+2,c:(1+y)/2})),u,y)
minimums={}
for i in range(poly.degree(u)+1):
 f=S.Poly(sum(coeff*y**j for (ii,j),coeff in poly.terms() if ii==i),y)
 n=f.degree();bs=[sum(f.nth(k)*S.Rational(comb(j,k),comb(n,k)) for k in range(j+1)) for j in range(n+1)]
 assert min(bs)>0
 back=S.expand(sum(bs[j]*comb(n,j)*y**j*(1-y)**(n-j) for j in range(n+1)))
 assert S.expand(back-f.as_expr())==0
 minimums[i]=str(min(bs)/3)
assert list(minimums.values())==['148','347/3','65/3','1/2','2/3','1/6']
# Extra wide bound |kappa4|<=3v: independently derive numerator and convert each rectangle.
z,s,x=S.symbols('z s x');p=1+z+z*z;ps=1+s+s*s
vv=z*(1+4*z+z*z)/p**2
k4=S.cancel(z*S.diff(z*S.diff(vv,z),z))
P4=S.Poly(S.cancel(k4*p**4/z),z)
Pterms=P4.terms();norm=S.expand(sum(ai*aj*s**(i+j)*S.chebyshevt(abs(i-j),c) for (i,),ai in Pterms for (j,),aj in Pterms))
modp=1-s*s+s**4+2*s*(1+s*s)*c+4*s*s*c*c
cert=S.expand(9*(1+4*s+s*s)**2*modp**4-norm*ps**4)
wide=[]
for lo in range(4):
 q=S.Poly(S.expand(cert.subs({s:(lo+x)/4,c:(3+y)/4})),x,y);nx,ny=q.degree(x),q.degree(y)
 terms=dict(q.terms());table=[]
 for i in range(nx+1):
  row=[]
  for j in range(ny+1):
   v=sum(co*S.Rational(comb(i,ii),comb(nx,ii))*S.Rational(comb(j,jj),comb(ny,jj)) for (ii,jj),co in terms.items() if ii<=i and jj<=j)
   row.append(v)
  table.append(row)
 assert min(map(min,table))>0
 # Invert the two Bernstein transforms explicitly, verifying the ENTIRE power array.
 for ii in range(nx+1):
  for jj in range(ny+1):
   back=sum(table[i][j]*comb(nx,i)*comb(nx-i,ii-i)*(-1)**(ii-i)*comb(ny,j)*comb(ny-j,jj-j)*(-1)**(jj-j) for i in range(ii+1) for j in range(jj+1))
   assert back==terms.get((ii,jj),0)
 wide.append(str(min(map(min,table))))

def expneg(x):
 assert x>0
 term=den=F(1)
 for j in range(1,221):term=term*x/j;den+=term
 return 1/den

def sqrtlower(q):
 return F(isqrt(q.numerator*10000**2//q.denominator),10000)
V=400
slabs=[];total=F(0)
for j in range(17):
 lo=F(2,5)+F(j,20);hi=lo+F(1,20)
 curvature=F(1,3)+F(158,375)/hi-F(49,625)/hi**2
 assert 0<curvature<F(17,16)
 h=lo*sqrtlower(curvature*V);tt=max(1,int(h)-1)
 loss=tt*h-F(15,32)*tt*tt
 momentpref=32*prod(1+F(tt*tt,k) for k in (2,4,8,16))
 value=2*(F(17,16)/curvature)**23*momentpref*expneg(loss)
 total+=value
 slabs.append({'lo':str(lo),'hi':str(hi),'curvature':str(curvature),'t':tt,'bound_diagnostic':float(value)})
assert total<F(1,10000)
central=8*F(51,16)**23*expneg(F(V,8))
one=192*3**18*F(17,16)**23*V**4*20*expneg(F(4*V,25))
two=128*F(44,7)**8*F(17,16)**23*V**23*expneg(F(125*V,246))
assert central<F(1,10**8) and one<F(1,1000) and two<F(1,10**18)
# All subsidiary rational comparisons, including radial monotonicity and gap.
assert F(19,48)*F(22,7)<F(5,4)
assert F(3,2)*F(10,256)<F(1,16)
assert F(4*9,256)-F(10*100,256**2)>F(1,8)
gap=F(5,12)+F(49,5*135)-F(40,123)
assert gap==F(18161,110700) and gap>F(4,25)
assert F(2*49,625)<F(158,375)*F(2,5)
assert F(269,300)<F(17,16)
assert F(9,2)/400<F(4,25) and F(23,400)<F(125,246)
assert 2*F(1,10000)+F(1,10**8)+F(1,1000)+F(1,10**18)<F(1201,10**6)
out={'status':'PASS','curvature_Bernstein_minima':minimums,'wide_kappa4_Bernstein_minima':wide,'central_principal_per_branch_diagnostic':float(total),'nonprincipal_central_total_diagnostic':float(central),'one_outer_total_diagnostic':float(one),'two_or_more_outer_total_diagnostic':float(two),'independent_exp_partial_sum_terms':220,'independent_sqrt_denominator':10000,'rigorous_total_cap':'1201/1000000','slabs':slabs,'original_target_solved':False}
(root/'ACTUAL_TORUS_INDEPENDENT_CERTIFICATES.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='slabs'},indent=2))
# Supplement: lower threshold 320, independently checked after the main proof.
V=300;slab300=F(0)
for j in range(17):
 lo=F(2,5)+F(j,20);hi=lo+F(1,20)
 cv=F(1,3)+F(158,375)/hi-F(49,625)/hi**2
 h=lo*sqrtlower(cv*V);tt=max(1,int(h)-1)
 slab300+=2*(F(17,16)/cv)**23*32*prod(1+F(tt*tt,k) for k in (2,4,8,16))*expneg(tt*h-F(15,32)*tt*tt)
assert slab300<F(1,100)
V=320
assert 320<18**2 and 2*F(22,7)/15<F(2,3)**2
one320=128*3**18*F(17,16)**23*V**4*18*expneg(F(18161*V,110700))
nonprincipal320=8*F(51,16)**23*expneg(F(V,8))
two320=128*F(44,7)**8*F(17,16)**23*V**23*expneg(F(125*V,246))
assert one320<F(3,5) and nonprincipal320<F(1,10000) and two320<F(1,5000)
b=F(19,20)
b1cap=16/b+F(1685,128)*F(4,3)/b**2+F(315,32)*F(36,25)/b**3
assert b1cap<53
budget=F(36821,320**2)+F(53,320)+F(11,500)+F(6203,20000)
assert budget==F(2194829,2560000) and budget<F(43,50)
assert F(9,640)<F(18161,110700) and F(23,320)<F(125,246)
supp={'status':'PASS for phase-node sign budget; no phase-node count or edge theorem','principal_branch_at300_diagnostic':float(slab300),'one_outer_at320_diagnostic':float(one320),'nonprincipal_at320_diagnostic':float(nonprincipal320),'two_or_more_outer_at320_diagnostic':float(two320),'B1_V_bound_exact':str(b1cap),'total_320_error_relative_2A':str(budget),'upper':'43/50'}
(root/'BULK_THRESHOLD_320_INDEPENDENT_RECEIPT.json').write_text(json.dumps(supp,indent=2)+'\n')
print(json.dumps(supp,indent=2))
