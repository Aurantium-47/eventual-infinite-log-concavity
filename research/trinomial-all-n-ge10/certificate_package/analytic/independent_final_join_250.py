if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
"""Independent final-join verification from receipt rational nodes ONLY.
Direct Bernstein-basis arithmetic; no phase solver, mpmath, or source checker import.
Uses fresh simpler certified pi brackets and independent Taylor truncations.
"""
from fractions import Fraction as Q
from math import comb,factorial
from pathlib import Path
import json
ROOT=Path(__file__).parent
nodes=[Q(x) for x in json.loads((ROOT/'FINAL_HARMONIC_JOIN_250_RECEIPT.json').read_text())['nodes']]
assert len(nodes)==33 and all(x>0 for x in nodes)

def atbr(x,k):
 p=sum((Q((-1)**i,2*i+1)*x**(2*i+1) for i in range(k)),Q(0))
 nxt=Q((-1)**k,2*k+1)*x**(2*k+1)
 return min(p,p+nxt),max(p,p+nxt)
a,b=atbr(Q(1,5),40);c,d=atbr(Q(1,239),12)
pi_lower=Q(3141592653589793,10**15);pi_upper=Q(3141592653589794,10**15)
assert pi_lower<16*a-4*d<16*b-4*c<pi_upper

def trigbr(x,cosine):
 offset=0 if cosine else 1
 vals=[Q((-1)**k,factorial(2*k+offset))*x**(2*k+offset) for k in range(17)]
 v=sum(vals[:16],Q(0));return min(v,v+vals[16]),max(v,v+vals[16])
B={'c':(Q(980785280403,10**12),Q(980785280404,10**12)),
'd':(Q(195090322016,10**12),Q(195090322017,10**12)),
'c2':(Q(923879532511,10**12),Q(923879532512,10**12)),
'd2':(Q(382683432365,10**12),Q(382683432366,10**12))}
for key,den,cosine in [('c',16,True),('d',16,False),('c2',8,True),('d2',8,False)]:
 lo=trigbr((pi_upper if cosine else pi_lower)/den,cosine)[0]
 hi=trigbr((pi_lower if cosine else pi_upper)/den,cosine)[1]
 assert B[key][0]<lo<hi<B[key][1]

def elevate(a,n):
 while len(a)<=n:
  d=len(a)-1
  a=[a[0]]+[Q(i,d+1)*a[i-1]+Q(d+1-i,d+1)*a[i] for i in range(1,d+1)]+[a[-1]]
 return a

def plus(a,b):
 n=max(len(a),len(b))-1;a=elevate(a,n);b=elevate(b,n)
 return [x+y for x,y in zip(a,b)]
def scale(a,c):return [c*x for x in a]
def times(a,b):
 m=len(a)-1;n=len(b)-1
 return [sum((Q(comb(m,i)*comb(n,k-i),comb(m+n,k))*a[i]*b[k-i] for i in range(max(0,k-n),min(m,k)+1)),Q(0)) for k in range(m+n+1)]
def power(a,n):
 r=[Q(1)]
 for _ in range(n):r=times(r,a)
 return r
rows=[]
for panel in range(32):
 L,R=nodes[panel:panel+2]
 # Bernstein controls of B and u; A is constant.
 A=[L*R];bb=[R,L];uu=[Q(panel,32032),Q(panel+1,32032)]
 ab=times(A,bb);ua2=times(uu,power(A,2));uab=times(uu,ab);u2a2=times(power(uu,2),power(A,2))
 pl=plus(scale(ab,B['d'][1]),scale(ua2,B['d2'][1]))
 pd=plus(plus(power(bb,2),scale(uab,B['c'][0])),scale(u2a2,B['c2'][0]))
 ql=plus(scale(ab,4*B['d'][0]),scale(ua2,B['d2'][0]))
 qd=plus(plus(power(bb,2),scale(uab,4*B['c'][1])),scale(u2a2,B['c2'][1]))
 qcheck=plus(qd,scale(times(uu,ql),-1));assert min(qcheck)>0
 pp=plus(plus(times(pl,power(pd,4)),scale(times(times(power(uu,2),power(pl,3)),power(pd,2)),-Q(1,3))),scale(times(power(uu,4),power(pl,5)),Q(1,5)))
 qp=plus(times(times(uu,ql),power(qd,2)),scale(times(power(uu,3),power(ql,3)),-Q(1,3)))
 gap=plus(plus(scale(times(power(pd,5),power(qd,3)),Q(8045,32)*pi_lower),scale(times(times(plus([Q(16)],scale(uu,45)),pp),power(qd,3)),-1)),scale(times(qp,power(pd,5)),Q(45,2)))
 assert len(gap)==17 and min(gap)>0
 rows.append({'panel':panel,'degree':16,'positive_gap_controls':True,'positive_Q_cap_controls':True})
 print(panel,'PASS',flush=True)
result={'status':'PASS','input':'Only33 rational nodes read from reference receipt; no numerical generator used','method':'Direct Bernstein-basis exact rational arithmetic, fresh Machin and Taylor trig certificates','pi_lower':str(pi_lower),'pi_upper':str(pi_upper),'panels':rows,'scope':'join only; no sign/ordering certificates for other edge nodes'}
(ROOT/'INDEPENDENT_FINAL_JOIN_250_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
