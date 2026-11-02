"""Fixed-point jets for one node/panel. No full-chain assertion. Every retained coefficient is enclosed by
(m_i +/- rad)/2^P; rad is a conservative common integer radius.
"""
from fractions import Fraction as F
from math import comb
from collections import deque
from pathlib import Path
import json,time,argparse,sys,resource
from byte_packed_convolution import convolution as byte_convolution
sys.set_int_max_str_digits(0)
DATA=Path(__file__).parent/'data'
OUTPUT=Path('results')
def ceilq(x):return -((-x.numerator)//x.denominator)
def ipow2(n):return F(1<<n) if n>=0 else F(1,1<<(-n))
def iconv(a,b,degree):
 # Trim only midpoint zeros. Full formal-degree uncertainty remains in J.mul.
 a=a[:];b=b[:]
 while len(a)>1 and a[-1]==0:a.pop()
 while len(b)>1 and b[-1]==0:b.pop()
 return byte_convolution(a,b,degree)

class J:
 P=2048;D=360;S=1<<2048;mul_count=0
 def __init__(self,m,rad=0):
  self.m=m[:self.D+1]+[0]*max(0,self.D+1-len(m));self.rad=rad
 @classmethod
 def rational(cls,x):
  x=F(x);a=x*cls.S
  return cls([(a.numerator+a.denominator//2)//a.denominator],0 if a.denominator==1 else 1)
 def add(self,b,sign=1):return J([x+sign*y for x,y in zip(self.m,b.m)],self.rad+b.rad)
 def scalar(self,x):
  x=F(x);a=x.numerator;d=x.denominator
  if not a:return J([0])
  return J([(v*a+d//2)//d for v in self.m],(abs(a)*self.rad+d-1)//d+(d!=1))
 def shift(self,k):return J([0]*k+self.m[:self.D+1-k],self.rad)
 def mul(self,b):
  J.mul_count+=1
  raw=iconv(self.m,b.m,self.D)
  er=b.rad*sum(map(abs,self.m))+self.rad*sum(map(abs,b.m))+(self.D+1)*self.rad*b.rad
  return J([(v+self.S//2)//self.S for v in raw],(er+self.S-1)//self.S+1)
 def rational_poly(self,p):
  out=J([0])
  for i,v in enumerate(p):
   if v:out=out.add(self.scalar(v).shift(i))
  return out

def bernstein_bounds(jet):
 # w=2x-1; Q(x)=sum m_j w^j; jets use real-panel scale h.
 d=J.D;Q=[jet.m[-1]]
 for j in range(d-1,-1,-1):
  out=[0]*(len(Q)+1)
  for i,x in enumerate(Q):out[i]-=x;out[i+1]+=2*x
  out[0]+=jet.m[j];Q=out
 C=[Q[-1]]
 for j in range(d-1,-1,-1):
  deg=d-j;C=[0]+C
  for i in range(deg+1):C[i]+=Q[j]*comb(deg,i)
 controls=[F(C[i],comb(d,i)*J.S) for i in range(d+1)]
 error=F((d+1)*jet.rad,J.S)
 return min(controls)-error,max(controls)+error

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

def run(panel=0,K=600,d=360,P=2048,index=200):
 assert (panel,K,d,P,index)==(0,600,360,2048,200), "This package freezes one benchmark case"
 start=time.perf_counter();J.D=d;J.P=P;J.S=1<<P;J.mul_count=0
 OUTPUT.mkdir(parents=True,exist_ok=True)
 table=json.load(open(DATA/'node200.json'))['nodes']
 left,right=F(table[panel]),F(table[panel+1]);h=F(1,64*1001);c=(2*panel+1)*h;r=4*h
 t=2/(1/left+1/right);a=(1/right-1/left)*t/(2*h)
 B=ceilq(3*t/2);C=1<<B
 jeterr,tail,meta=analytic_errors(c,h,r,t,a,B,K,d,max(left,right),c+h)
 print('parameters',panel,K,d,P,'B',B,flush=True)
 outputs=[];buf=[deque([J([0])]) for _ in range(4)]
 def feed(level,x):
  if level==4:outputs.append(x);return
  b=buf[level];b.append(x)
  if len(b)==3:
   y=b[1].mul(b[1]).add(b[0].mul(b[2]),-1);b.popleft();feed(level+1,y)
 prev=J.rational(F(1,C));cur=J.rational(t/C);feed(0,prev);feed(0,cur)
 for k in range(1,K+4):
  nxt=cur.rational_poly([t*(1-k*c)/F(k+1),-t*k*h/F(k+1)])
  p=[2*c-(k-1)*c*c,2*h-2*(k-1)*c*h,-(k-1)*h*h]
  nxt=nxt.add(prev.rational_poly([t*t*x/F(k+1) for x in p]));prev,cur=cur,nxt;feed(0,cur)
  if k%100==0:print('generated',k,'seconds',time.perf_counter()-start,flush=True)
 assert len(outputs)==K+1
 # Exact rational coefficients of q(w)=-(1+a*h*w)^(-16), outward rounded.
 qm=[];qr=0
 for j in range(d+1):
  x=-F(comb(15+j,j))*(-a*h)**j*J.S
  qm.append((x.numerator+x.denominator//2)//x.denominator);qr=max(qr,int(x.denominator!=1))
 qjet=J(qm,qr);value=outputs[-1]
 for b in reversed(outputs[:-1]):value=value.mul(qjet).add(b)
 low,high=bernstein_bounds(value);total=jeterr+tail
 result={'scope':f'ONE index{index} moving node on ONE parameter panel, not full chain','index':index,'roundoff_error':str(F((d+1)*value.rad,J.S)),'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'panel':panel,'K':K,'d':d,'P':P,'t_center':str(t),'a':str(a),'c':str(c),'r':str(r),'jet_variable':'w=(u-c)/h','h':str(h),'lower_with_roundoff':str(low),'upper_with_roundoff':str(high),'parameter_Taylor_error':str(jeterr),'coefficient_tail':str(tail),'certified_negative':high+total<0,'certified_positive':low-total>0,'seconds':time.perf_counter()-start,'jet_multiplications':J.mul_count,'analytic_metadata':meta}
 path=OUTPUT/'receipt.json';path.write_text(json.dumps(result,indent=2))
 (OUTPUT/'final_jet.json').write_text(json.dumps({'midpoints':value.m,'radius':value.rad,'P':P,'d':d,'index':index,'panel':panel}))
 print({k:result[k] for k in ['certified_negative','certified_positive','seconds','jet_multiplications']},flush=True)
