if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
# Exact Bernstein positivity certificate, not a sampled numerical inequality.
import sympy as S
import json
from pathlib import Path
u,z=S.symbols('u z')
t=u+2;c=S.Rational(49,50)+z/50
b2=(t*t-4)*(1-c*c);a=t*c+1
R=(a+3)*a*a+(a-3)*b2;T=a*a+6*a+b2
P=S.Poly(S.expand(R**2-16*b2*T**2),u)
rows=[]
for m in range(P.degree()+1):
 q=S.Poly(P.nth(m),z);d=q.degree()
 bern=[S.factor(sum(q.nth(i)*S.binomial(k,i)/S.binomial(d,i) for i in range(k+1))) for k in range(d+1)]
 assert all(b>0 for b in bern)
 # Independently reconstruct each polynomial from its Bernstein coefficients.
 assert S.expand(sum(bern[k]*S.binomial(d,k)*z**k*(1-z)**(d-k) for k in range(d+1))-q.as_expr())==0
 rows.append({'power_u':m,'bernstein_degree':int(d),'coefficients':[str(b) for b in bern],'minimum':str(min(bern))})
assert 17**45 < 2**184
receipt={'statement':'R^2-16B^2T^2>0 for t>=2,49/50<=c<=1','rows':rows,'gaussian_conditioning_bound':'(17/16)^(45/4)<2','finite_n_root_conclusion':False}
p=Path(__file__).with_name('COMPLEX_VARIANCE_CONDITIONING_RECEIPT.json')
p.write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS; minimum Bernstein coefficient',min(S.Rational(v) for r in rows for v in r['coefficients']))
