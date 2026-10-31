if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
# Independently generated balanced-tree polynomial moments; stdlib only.
from fractions import Fraction as F
from itertools import product
import json
nodes=[]
def tree(lo,hi):
 if hi-lo==1:return
 mid=(lo+hi)//2
 nodes.append((lo,mid,hi));tree(lo,mid);tree(mid,hi)
tree(0,16)
N=len(nodes)
def add_poly(a,b):
 for k,v in b.items():a[k]=a.get(k,F(0))+v
 return {k:v for k,v in a.items() if v}
def mul(a,b):
 out={}
 for ka,va in a.items():
  for kb,vb in b.items():
   k=tuple(x+y for x,y in zip(ka,kb));out[k]=out.get(k,F(0))+va*vb
 return {k:v for k,v in out.items() if v}
def power(a,n):
 b={(0,)*N:F(1)}
 for _ in range(n):b=mul(b,a)
 return b
def moment(poly):
 total=F(0)
 for exps,c in poly.items():
  for e,(lo,mid,hi) in zip(exps,nodes):
   if e%2:c=0;break
   a=e//2;df=1
   for v in range(1,2*a+2,2):df*=v
   c*=df*(hi-lo)**a
  total+=c
 return total
S3={};S4={}
for leaf in range(16):
 p={}
 for j,(lo,mid,hi) in enumerate(nodes):
  if lo<=leaf<hi:
   e=[0]*N;e[j]=1;p[tuple(e)]=F(1 if leaf<mid else -1,hi-lo)
 S3=add_poly(S3,power(p,3));S4=add_poly(S4,power(p,4))
a=moment(S4);b=moment(mul(S3,S3));sizes=sum(hi-lo for lo,mid,hi in nodes)
assert a==F(5055,16) and b==F(2835,4) and sizes==64
kernel=-F(3*sizes,12);fourth=a/24;cubic=-b/72
assert (kernel,fourth,cubic)==(-16,F(1685,128),F(-315,32))
# At real zeta=1: v=2/3,kappa3=0,kappa4=-2/3.
center=kernel/F(2,3)+fourth*F(-2,3)/F(2,3)**2
assert center==F(-11199,256)
print(json.dumps({'S3_monomials':len(S3),'E_sum_eta4':str(a),'E_sum_eta3_squared':str(b),'node_size_sum':sizes,'kernel_coefficient':str(kernel),'kappa4_coefficient':str(fourth),'kappa3_squared_coefficient':str(cubic),'B1_real_zeta1':str(center),'status':'exact arithmetic PASS; no analytic remainder claim'},indent=2))
