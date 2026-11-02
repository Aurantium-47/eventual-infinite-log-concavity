"""Exact global scalar premises for the analytic-core referee report.

Independently constructs cumulants from p, computes real/imaginary parts in
Q[s,c,w]/(w^2-(1-c^2)), and certifies cleared numerators by tensor Bernstein
coefficients. No author program, saved controls, or receipt is imported.
Requires SymPy; all certificate decisions use rational arithmetic.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import time
import sympy as sp

if not __debug__:
    raise RuntimeError('Assertions are part of the verifier; do not run Python with -O/-OO.')

s,c,z=sp.symbols('s c z')
p=1+z+z*z
ps=1+s+s*s
qs=1+4*s+s*s

def mul(a,b):
    return (sp.expand(a[0]*b[0]-(1-c*c)*a[1]*b[1]),
            sp.expand(a[0]*b[1]+a[1]*b[0]))

def power(a,n):
    out=(sp.Integer(1),sp.Integer(0))
    for _ in range(n): out=mul(out,a)
    return out

def evaluate(poly):
    out=(sp.Integer(0),sp.Integer(0))
    for coefficient in sp.Poly(poly,z).all_coeffs():
        out=mul(out,(s*c,s))
        out=(out[0]+coefficient,out[1])
    return tuple(sp.expand(x) for x in out)

def norm(a):
    return sp.expand(a[0]**2+(1-c*c)*a[1]**2)

pp=evaluate(p)
den=norm(pp)
pbar=(pp[0],-pp[1])
assert sp.expand(den-(1-s*s+s**4+2*s*(1+s*s)*c+4*s*s*c*c))==0
nums={2:z*(1+4*z+z*z)}
for m in range(2,6):
    nums[m+1]=sp.expand(z*(p*sp.diff(nums[m],z)-m*sp.diff(p,z)*nums[m]))
evaluated={m:evaluate(poly) for m,poly in nums.items()}
realimag={m:mul(evaluated[m],power(pbar,m)) for m in nums}

def clean(poly):
    poly=sp.Poly(sp.expand(poly),s,c)
    # s>0 in the theorem. Cancelling a common positive power of s is exact.
    k=min(i for (i,j),a in poly.terms())
    expr=sp.cancel(poly.as_expr()/s**k)
    return sp.Poly(expr,s,c),k

def bernstein(poly,box):
    a,b,d,e=box
    ns,nc=map(int,poly.degree_list())
    coeff=[[F(0) for _ in range(nc+1)] for _ in range(ns+1)]
    for (i,j),v in poly.terms(): coeff[i][j]=F(int(v.p),int(v.q))
    ax=[[sum((coeff[i][j]*comb(i,k)*a**(i-k)*(b-a)**k
              for i in range(k,ns+1)),F(0))
         for j in range(nc+1)] for k in range(ns+1)]
    ay=[[sum((ax[i][j]*comb(j,l)*d**(j-l)*(e-d)**l
              for j in range(l,nc+1)),F(0))
         for l in range(nc+1)] for i in range(ns+1)]
    bx=[[sum((ay[i][j]*F(comb(k,i),comb(ns,i))
              for i in range(k+1)),F(0))
         for j in range(nc+1)] for k in range(ns+1)]
    controls=[[sum((bx[k][j]*F(comb(l,j),comb(nc,j))
                    for j in range(l+1)),F(0))
               for l in range(nc+1)] for k in range(ns+1)]
    return min(min(row) for row in controls)

def certify(name,expr,cmin):
    poly,cancelled=clean(expr)
    queue=[((F(i,4),F(i+1,4),cmin,F(1)),0) for i in range(4)]
    accepted=[]
    while queue:
        box,depth=queue.pop(0)
        minimum=bernstein(poly,box)
        if minimum>=0:
            accepted.append({'box':list(map(str,box)),'minimum':str(minimum)})
        elif depth<8:
            a,b,d,e=box
            # Alternate independent interval bisection in the two variables.
            if depth%2==0:
                mid=(a+b)/2
                queue.extend([((a,mid,d,e),depth+1),((mid,b,d,e),depth+1)])
            else:
                mid=(d+e)/2
                queue.extend([((a,b,d,mid),depth+1),((a,b,mid,e),depth+1)])
        else:
            raise ArithmeticError((name,'not certified',box,minimum))
    result={'name':name,'domain_s':['0','1'],'domain_cos':[str(cmin),'1'],
            'cancelled_positive_s_power':cancelled,
            'numerator_bidegree':list(map(int,poly.degree_list())),
            'cells':accepted,'pass':True}
    print(json.dumps({'name':name,'cells':len(accepted),'pass':True}),flush=True)
    return result

def main():
    started=time.monotonic()
    rv,iv=realimag[2]
    tests=[
      ('central Re(v)>=v0/3',3*rv*ps**2-s*qs*den**2,F(1,2)),
      ('narrow Re(v)>=19v0/20',20*rv*ps**2-19*s*qs*den**2,F(49,50)),
      ('narrow Re(v)<=17v0/16',17*s*qs*den**2-16*rv*ps**2,F(49,50)),
      ('narrow 16(Im(v))^2<=(Re(v))^2',rv**2-16*(1-c*c)*iv**2,F(49,50)),
      ('narrow abs(Im(kappa3))<=v0/4',
       s*s*qs**2*den**6-16*(1-c*c)*realimag[3][1]**2*ps**4,F(49,50)),
      ('wide Re(kappa4)<=3v0/2',
       3*s*qs*den**4-2*realimag[4][0]*ps**2,F(3,4)),
    ]
    for m,bound,cosmin in [(3,F(6,5),F(49,50)),(4,F(4,3),F(49,50)),
                            (5,F(9,4),F(49,50)),(4,F(3),F(3,4)),
                            (6,F(32),F(3,4))]:
        C=sp.Rational(bound.numerator,bound.denominator)
        tests.append((f'abs(kappa{m})<={bound}v0 on cos>={cosmin}',
                      C*C*s*s*qs**2*den**m-norm(evaluated[m])*ps**4,cosmin))
    out=[certify(*t) for t in tests]
    # Exponentiation of positive rational numbers proves the normalization
    # estimates without floating logarithms.
    assert F(17,16)**45 < 2**4
    assert F(285,269)**45 < 16
    assert F(269,300)>F(15,16)**2
    result={'status':'PASS','independent_from_author_code':True,'premises':out,
            'normalization_checks':['(17/16)^(45/4)<2',
                                    '2*(285/269)^(45/2)<8',
                                    '269/300>(15/16)^2'],
            'seconds':time.monotonic()-started}
    target=Path(__file__).with_name('scalar_premises_results.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print('ALL scalar premises certified exactly',flush=True)

if __name__=='__main__': main()
