from fractions import Fraction as F
from math import comb
import interval_jets as fj
def ceilq(x):return -((-x.numerator)//x.denominator)

def ipow2(n):return F(1<<n) if n>=0 else F(1,1<<(-n))

def log_upper(x,L=16):
 w=(x-1)/(x+1)
 assert 0<=w<1
 return 2*sum((w**(2*j+1)/F(2*j+1) for j in range(L)),F(0))+2*w**(2*L+1)/((2*L+1)*(1-w*w))

def analytic_errors(c,h,r,t,a,B,K,d,Treal,umax):
 assert abs(a)*r<1
 T=t/(1-abs(a)*r);R=T+1;q=(c+r)*R
 assert q<1
 H=sum((F((2 if l%3==0 else 1)*(l-1),l)*q**(l-2) for l in range(2,33)),F(0))+2*q**31/(1-q)
 E=(log_upper(1+c*R+(c*R)**2)/c if c else R)+r*R*R*H
 # Positive atanh partial sum is a rigorous lower bound on log(2).
 log2lower=2*sum((F(1,(2*j+1)*3**(2*j+1)) for j in range(10)),F(0))
 upper=ipow2(15+ceilq(16*E/log2lower)-16*B)/(1-(T/R)**16)
 jeterr=upper*(h/r)**(d+1)/(1-h/r)
 Rt=2*Treal;assert umax*Rt<1
 Et=Rt+umax*Rt*Rt/2
 tail=ipow2(15+ceilq(16*Et/log2lower)-16*B-16*(K+1))/(1-F(1,2**16))
 return jeterr,tail,{'q':str(q),'log2_exponent_bound':ceilq(16*E/log2lower),'normalization_binary_exponent':B}
def bernstein(jet):
 d=jet.d;Q=[jet.m[-1]]
 for j in range(d-1,-1,-1):
  out=[0]*(len(Q)+1)
  for i,x in enumerate(Q):out[i]-=x;out[i+1]+=2*x
  out[0]+=jet.m[j];Q=out
 C=[Q[-1]]
 for j in range(d-1,-1,-1):
  degree=d-j;C=[0]+C
  for i in range(degree+1):C[i]+=Q[j]*comb(degree,i)
 controls=[F(C[i],comb(d,i)) for i in range(d+1)];scale=fj.pow2(jet.e-jet.p)
 roundoff=(d+1)*jet.rad*scale
 return min(controls)*scale-roundoff,max(controls)*scale+roundoff,roundoff
