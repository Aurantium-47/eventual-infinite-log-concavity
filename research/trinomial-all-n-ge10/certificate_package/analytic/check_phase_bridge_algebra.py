if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
import sympy as S
s,c,d=S.symbols('s c d',real=True);z=s*(c+S.I*d)
def red(x):return S.factor(S.rem(S.Poly(S.expand(x),d),S.Poly(d*d+c*c-1,d)).as_expr())
p=1+z+z*z;q=1+4*z+z*z
ip=red(S.im(z*(1+2*z)*S.conjugate(p)))
iq=red(S.im(z*(4+2*z)*S.conjugate(q)))
iv=red(S.im(z*q*S.conjugate(p)**2))
assert S.expand(ip-s*d*(1+4*s*c+s*s))==0
assert S.expand(iq-4*s*d*(1+s*c+s*s))==0
want=s*d*(1-s*s)*(4*c*c*s*s+8*c*s**3+8*c*s+s**4+5*s*s+1)
assert S.expand(iv-want)==0
assert S.expand(red(S.expand(q*S.conjugate(q)-p*S.conjugate(p)))- (6*s*c*(1+s*s)+15*s*s))==0
pr=1+s+s*s;qr=1+4*s+s*s
v=s*qr/pr**2;m=s*(1+2*s)/pr
assert S.factor(m/v-1)==s*(2*s*s+2*s-1)/qr
assert S.factor(s*S.diff(v,s)-s*(1-s*s)*(1+7*s+s*s)/pr**3)==0
value=v.subs(s,S.Rational(7,20))
assert value==S.Rational(141260,346921)
assert 1001*value>400
assert (2*s*s+2*s-1).subs(s,S.Rational(7,20))==-S.Rational(11,200)
print('PASS: Im mp, Im mq, Im v numerator, modulus gap, m/v, v monotonicity, exact V400 crossing')
print('v(7/20)=',value,'; 1001*v -400=',1001*value-400)
