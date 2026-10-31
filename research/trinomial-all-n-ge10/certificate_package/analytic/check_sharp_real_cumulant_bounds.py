if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
# Exact rational Bernstein certificates for real saddle-remainder bounds.
import sympy as S
import json
from pathlib import Path
t,c,d,h=S.symbols('t c d h',real=True)
w=t*c-S.I*d*h
D=t*t+2*t*c-3+4*c*c

def reduce_even(expr):
 out=0
 for (ed,eh),coef in S.Poly(S.expand(expr),d,h).terms():
  assert ed%2==eh%2==0
  out+=coef*(t*t-4)**(ed//2)*(1-c*c)**(eh//2)
 return S.expand(out)
I3=reduce_even(S.im(S.expand(-(-d*c+S.I*t*h)*(w+7)*(t*c+1+S.I*d*h)**3))/h)
R4=reduce_even(S.re(S.expand((w**3+12*w*w-15*w-80)*(t*c+1+S.I*d*h)**4)))
P3=S.expand((t+4)**2*D**6-16*(1-c*c)*I3**2*(t+1)**4)
P4=S.expand(S.Rational(3,2)*(t+4)*D**4-R4*(t+1)**2)
u,z=S.symbols('u z')

def certificate(poly,lo,hi,c0,c1):
 q=S.Poly(S.expand(poly.subs({t:lo+(hi-lo)*u if hi is not None else lo+u,c:c0+(c1-c0)*z})),u,z)
 du,dz=q.degree_list(); bs=[]
 for i in range(du+1):
  row=[]
  for j in range(dz+1):
   val=sum(q.nth(k,l)*(S.binomial(i,k)/S.binomial(du,k) if hi is not None else (1 if i==k else 0))*S.binomial(j,l)/S.binomial(dz,l) for k in range(i+1) for l in range(j+1))
   assert val>0
   row.append(val)
  bs.append(row)
 # Two exact evaluation checks supplement the algebraic basis formula.
 for uu,zz in [(S.Rational(1,3),S.Rational(2,5)),(S.Rational(4,5),S.Rational(1,7))]:
  reconstructed=sum(bs[i][j]*(S.binomial(du,i)*uu**i*(1-uu)**(du-i) if hi is not None else uu**i)*S.binomial(dz,j)*zz**j*(1-zz)**(dz-j) for i in range(du+1) for j in range(dz+1))
  assert reconstructed==q.eval({u:uu,z:zz})
 return {'t_interval':[str(lo),str(hi)],'c_interval':[str(c0),str(c1)],'basis_t':'Bernstein' if hi is not None else 'powers of t-lo','degrees':[du,dz],'coefficients':[[str(v) for v in row] for row in bs],'minimum':str(min(v for row in bs for v in row))}
cert3=certificate(P3,S.Integer(2),None,S.Rational(49,50),S.Integer(1))
cert4=[certificate(P4,S.Integer(lo),S.Integer(hi) if hi else None,S.Rational(3,4),S.Integer(1)) for lo,hi in [(2,4),(4,8),(8,None)]]
assert 251**2*16*400>256**2*17*19**2
assert 2**2*285**45 < 8**2*269**45
assert 2**2*456**45 < 13**2*421**45
out={'Im_kappa3_bound':'abs(Im kappa3)<=v/4 when cos(theta)>=49/50','Re_kappa4_bound':'Re kappa4<=3v/2 when cos(alpha)>=3/4','Im_kappa3_certificate':cert3,'Re_kappa4_certificates':cert4,'variance_lower_bound':'Re v(zeta)>=19v(s)/20','coordinate_box_gaussian_losses':{'d=2/5':'<8','d=1/2':'<13'},'full_target_solved':False}
Path(__file__).with_name('SHARP_REAL_CUMULANT_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS minima',cert3['minimum'],[q['minimum'] for q in cert4])
