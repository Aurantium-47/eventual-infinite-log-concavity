if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
# Exact symbolic identity audit, supplementary to the handwritten all-s proof.
import sympy as S
s,c=S.symbols('s c')
P=1+s+s*s; A=2*s*(1+s*s); B=4*s*s; C=s**4-s*s+1
E=C+A*c+B*c*c
N=S.expand((2*B-A*c-4*B*c*c)*E-(1-c*c)*(A+2*B*c)**2)
expected=(-8*s**5-8*s**3)*c**3+(-16*s**6-16*s**4-16*s*s)*c*c+(-2*s**7-16*s**5-16*s**3-2*s)*c+4*s**6-16*s**4+4*s*s
assert S.expand(N-expected)==0
NN=s**7+9*s**5+20*s**4+9*s**3+s
assert S.expand(N.subs(c,S.Rational(1,2))+NN)==0
rhs=s/S.Integer(4)*(3*s**4*(s-1)**2+21*s**4+64*s**3+21*s*s+3*(s-1)**2)
assert S.expand(NN-S.Rational(1,4)*s*(1+4*s+s*s)*P**2-rhs)==0
assert S.Rational(5,12)-S.Rational(40,123)==S.Rational(15,164)
print('Exact algebraic identities PASS; no finite-n real-root conclusion.')
