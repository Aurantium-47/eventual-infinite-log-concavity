"""Shared floating-exponent interval Taylor jets.
Each coefficient lies in 2^(e-p)*(m_i+[-rad,rad]). No implicit float arithmetic.
Exact convolution backend is pluggable; default is independently audited bytes.
"""
from fractions import Fraction as F
from integer_polynomial import convolution as byte_convolution

def near(n,d):
 q,r=divmod(n,d)
 return q+int(2*r>=d)
def ceildiv(n,d):return -((-n)//d)
def pow2(e):return F(1<<e) if e>=0 else F(1,1<<(-e))
def rational_exponent(q):
 q=abs(F(q));assert q
 n,d=q.numerator,q.denominator;e=n.bit_length()-d.bit_length()
 if (n < d<<e) if e>=0 else (n<<(-e) < d):e-=1
 assert pow2(e)<=q<2*pow2(e)
 return e

def trimmed_byte_convolution(a,b,d):
 a=a[:];b=b[:]
 while len(a)>1 and a[-1]==0:a.pop()
 while len(b)>1 and b[-1]==0:b.pop()
 return byte_convolution(a,b,d)
CONV=trimmed_byte_convolution
BACKEND='byte-packed'
MUL_COUNT=0

def set_backend(function,name):
 global CONV,BACKEND
 CONV=function;BACKEND=name

class Jet:
 __slots__=('m','rad','e','p')
 def __init__(self,m,rad=0,e=0,p=2048):
  assert m and rad>=0 and p>=2
  self.m=list(m);self.rad=int(rad);self.e=int(e);self.p=int(p)
 @property
 def d(self):return len(self.m)-1
 def exact_zero(self):return self.rad==0 and not any(self.m)
 @classmethod
 def zero(cls,d,p):return cls([0]*(d+1),0,0,p)
 @classmethod
 def rational(cls,q,d,p):
  q=F(q)
  if not q:return cls.zero(d,p)
  e=rational_exponent(q);v=q/pow2(e);n=v.numerator*(1<<p);den=v.denominator
  mid=near(n,den);err=abs(den*mid-n)
  return cls([mid]+[0]*d,ceildiv(err,den),e,p).normalize()
 def normalize(self):
  M=max(self.rad,max(map(abs,self.m)))
  if not M:return Jet.zero(self.d,self.p)
  shift=M.bit_length()-self.p
  if shift<=0:
   return Jet([x<<(-shift) for x in self.m],self.rad<<(-shift),self.e+shift,self.p)
  den=1<<shift;mid=[near(x,den) for x in self.m]
  err=max(abs(den*y-x) for x,y in zip(self.m,mid))
  return Jet(mid,ceildiv(self.rad+err,den),self.e+shift,self.p)
 def align(self,E):
  assert E>=self.e
  if E==self.e:return self
  den=1<<(E-self.e);mid=[near(x,den) for x in self.m]
  err=max(abs(den*y-x) for x,y in zip(self.m,mid))
  return Jet(mid,ceildiv(self.rad+err,den),E,self.p)
 def negative(self):return Jet([-x for x in self.m],self.rad,self.e,self.p)
 def add(self,b,sign=1):
  assert self.p==b.p and self.d==b.d and sign in(-1,1)
  if self.exact_zero():return b if sign==1 else b.negative()
  if b.exact_zero():return self
  E=max(self.e,b.e);a=self.align(E);b=b.align(E)
  return Jet([x+sign*y for x,y in zip(a.m,b.m)],a.rad+b.rad,E,self.p).normalize()
 def scalar(self,q):
  q=F(q)
  if not q or self.exact_zero():return Jet.zero(self.d,self.p)
  qe=rational_exponent(q);q=q/pow2(qe);num,den=q.numerator,q.denominator
  mid=[near(num*x,den) for x in self.m]
  err=max(abs(den*y-num*x) for x,y in zip(self.m,mid))
  return Jet(mid,ceildiv(abs(num)*self.rad+err,den),self.e+qe,self.p).normalize()
 def shift(self,k):
  assert k>=0
  if k>self.d:return Jet.zero(self.d,self.p)
  return Jet(([0]*k+self.m)[:self.d+1],self.rad,self.e,self.p).normalize()
 def rational_poly(self,coefficients):
  out=Jet.zero(self.d,self.p)
  for i,v in enumerate(coefficients):
   if v and i<=self.d:out=out.add(self.scalar(v).shift(i))
  return out
 def mul(self,b):
  global MUL_COUNT
  assert self.p==b.p and self.d==b.d
  if self.exact_zero() or b.exact_zero():return Jet.zero(self.d,self.p)
  MUL_COUNT+=1
  mid=CONV(self.m,b.m,self.d);mid=mid[:self.d+1]+[0]*max(0,self.d+1-len(mid))
  err=b.rad*sum(map(abs,self.m))+self.rad*sum(map(abs,b.m))+(self.d+1)*self.rad*b.rad
  return Jet(mid,err,self.e+b.e-self.p,self.p).normalize()
 def truncate(self,d):
  assert 0<=d<=self.d
  return Jet(self.m[:d+1],self.rad,self.e,self.p).normalize()
 def reprecision(self,p):
  assert p>=2
  if p>=self.p:
   sh=p-self.p;return Jet([x<<sh for x in self.m],self.rad<<sh,self.e,p).normalize()
  den=1<<(self.p-p);mid=[near(x,den) for x in self.m]
  err=max(abs(den*y-x) for x,y in zip(self.m,mid))
  return Jet(mid,ceildiv(self.rad+err,den),self.e,p).normalize()
 def contains(self,coefficients):
  scale=pow2(self.e-self.p)
  return len(coefficients)==len(self.m) and all(scale*(m-self.rad)<=x<=scale*(m+self.rad) for m,x in zip(self.m,coefficients))
 def record(self):return {'m':self.m,'rad':self.rad,'e':self.e,'p':self.p}
 @classmethod
 def from_record(cls,r):return cls(r['m'],r['rad'],r['e'],r['p'])
