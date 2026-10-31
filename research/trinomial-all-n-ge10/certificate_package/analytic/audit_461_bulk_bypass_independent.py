if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
"""Frozen-table audit: ONLY reported bypass panels; independent ordinary-power arithmetic."""
from fractions import Fraction as F
from math import comb,factorial
from pathlib import Path
import json,hashlib,time
root=Path(__file__).parent
started=time.monotonic()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
tp=root/'ALL249_HARMONIC_RATIONAL_CANDIDATES.json';rp=root/'ALL249_BULK_BYPASS_CLASSIFICATION.json'
assert sha(tp)=='2bce90973f2c0a47aa996457dea6e44e8d980976548bfe4b07f91d4eecd75b78'
assert sha(rp)=='c7e2a53fe0f1e18084c4967dd69c5be450eff6d9220b84e4210a966194f91c06'
table=json.loads(tp.read_text());receipt=json.loads(rp.read_text())
assert table['u_endpoints']==[str(F(i,32032)) for i in range(33)]
assert [r['node'] for r in table['nodes']]==list(range(1,250))
values={r['node']:list(map(F,r['endpoints'])) for r in table['nodes']}
assert all(len(v)==33 for v in values.values())
assert all(x>0 for x in values[1]);ordering=0
for j in range(1,249):
 for i in range(33):assert 0<values[j][i]<values[j+1][i];ordering+=1
assert ordering==8184
assert [r['node'] for r in receipt['nodes']]==list(range(1,250))
claimed=[];notcert=[]
for row in receipt['nodes']:
 assert [p['panel'] for p in row['panels']]==list(range(32))
 for p in row['panels']:
  assert p['bypass']==all(p['checks'].values())
  (claimed if p['bypass'] else notcert).append((row['node'],p['panel'],p))
assert len(claimed)==461 and len(notcert)==7507
assert receipt['not_certified_list']==[[j,k] for j,k,_ in notcert]
# Independently verify the rational transcendental enclosures; no generator imported.
def atan_bounds(q,n):
 part=sum(((-1)**i*q**(2*i+1)/F(2*i+1) for i in range(n)),F(0));nxt=(-1)**n*q**(2*n+1)/F(2*n+1)
 return min(part,part+nxt),max(part,part+nxt)
a,b=atan_bounds(F(1,5),50);c,d=atan_bounds(F(1,239),14)
pl=F(3141592653589793,10**15);pu=F(3141592653589794,10**15)
assert pl<16*a-4*d<16*b-4*c<pu
bounds={'c':(F(980785280403,10**12),F(980785280404,10**12)),'d':(F(195090322016,10**12),F(195090322017,10**12)),'c2':(F(923879532511,10**12),F(923879532512,10**12)),'d2':(F(382683432365,10**12),F(382683432366,10**12))}
def trig(q,cosine):
 offset=0 if cosine else 1
 part=sum((F((-1)**i,factorial(2*i+offset))*q**(2*i+offset) for i in range(20)),F(0))
 nxt=F(1,factorial(40+offset))*q**(40+offset)
 return part,part+nxt
for name,den,cosine in [('c',16,True),('d',16,False),('c2',8,True),('d2',8,False)]:
 low=trig((pu if cosine else pl)/den,cosine)[0];high=trig((pl if cosine else pu)/den,cosine)[1]
 assert bounds[name][0]<low<high<bounds[name][1]
# All subsequent polynomials are ordinary POWER coefficients, unlike source Bernstein arithmetic.
def clean(a):
 while len(a)>1 and a[-1]==0:a.pop()
 return a

def add(a,b):
 out=[F(0)]*max(len(a),len(b))
 for i,x in enumerate(a):out[i]+=x
 for i,x in enumerate(b):out[i]+=x
 return clean(out)
def neg(a):return [-x for x in a]
def scale(a,b):return clean([b*x for x in a])
def mul(a,b):
 out=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 return clean(out)
def pw(a,n):
 out=[F(1)]
 for _ in range(n):out=mul(out,a)
 return out

def bern(a,degree):
 assert len(a)<=degree+1
 return [sum((a[k]*F(comb(i,k),comb(degree,k)) for k in range(min(i,len(a)-1)+1)),F(0)) for i in range(degree+1)]

def certified_panel(L,R,ul,ur,j):
 A=[L*R];B=[R,L-R];u=[ul,ur-ul]
 AB=mul(A,B);uA2=mul(u,pw(A,2));uAB=mul(u,AB);u2A2=mul(pw(u,2),pw(A,2));B2=pw(B,2)
 def ratio(weight,upper):
  N=add(scale(AB,weight*bounds['d'][upper]),scale(uA2,bounds['d2'][upper]))
  D=add(add(B2,scale(uAB,weight*bounds['c'][1-upper])),scale(u2A2,bounds['c2'][1-upper]))
  assert min(bern(N,1))>0 and min(bern(D,2))>0
  return N,D
 Plo=ratio(1,0);Phi=ratio(1,1);Qlo=ratio(4,0);Qhi=ratio(4,1)
 def atanpoly(N,D,order,divide_u):
  if order==3:numerator=add(mul(N,pw(D,2)),scale(mul(pw(u,2),pw(N,3)),-F(1,3)))
  else:numerator=add(add(mul(N,pw(D,4)),scale(mul(mul(pw(u,2),pw(N,3)),pw(D,2)),-F(1,3))),scale(mul(pw(u,4),pw(N,5)),F(1,5)))
  if not divide_u:numerator=mul(u,numerator)
  return numerator,pw(D,order)
 def phasegap(pr,qr,lower):
  pnum,pden=atanpoly(*pr,3 if lower else 5,True)
  qnum,qden=atanpoly(*qr,5 if lower else 3,False)
  denominator=mul(pden,qden)
  expression=add(mul(mul(add([F(16)],scale(u,45)),pnum),qden),scale(mul(qnum,pden),-F(45,2)))
  C=F(j)+F(45,32)
  return add(expression,scale(denominator,F(1,3)-C*pu)) if lower else add(scale(denominator,C*pl+F(1,3)),neg(expression))
 uppergap=phasegap(Phi,Qlo,False);lowergap=phasegap(Plo,Qhi,True)
 central=add(add(B2,uAB),u2A2)
 Vgap=add(mul(AB,add(add(B2,scale(uAB,4)),u2A2)),scale(pw(central,2),-250))
 disk=add(B,neg(mul(u,A)))
 caps=[add(D,neg(mul(u,N))) for N,D in (Phi,Plo,Qhi,Qlo)]
 minima={'V':str(min(bern(Vgap,4))),'phase_upper':str(min(bern(uppergap,16))),'phase_lower':str(min(bern(lowergap,16))),'disk':str(min(bern(disk,1))),'ratio_caps':str(min(min(bern(cap,2)) for cap in caps))}
 assert all(F(x)>0 for x in minima.values())
 return hashlib.sha256(json.dumps(minima,sort_keys=True).encode()).hexdigest()
for number,(j,k,row) in enumerate(claimed,1):
 digest=certified_panel(values[j][k],values[j][k+1],F(k,32032),F(k+1,32032),j)
 assert digest==row['control_values_sha256'],(j,k,digest,row['control_values_sha256'])
 if number%100==0:print('independently certified',number,'seconds',round(time.monotonic()-started,3),flush=True)
out={'status':'PASS for exactly461 reported bypass panels and8184 strict endpoint comparisons','reported_bypass_panels_independently_certified':461,'each_positive_control_minimum_hash_matches':True,'ordering_comparisons':ordering,'not_certified_panels_preserved':7507,'remaining_panel_phase_flags_independently_checked':False,'phase_generator_or_jet_replayed':False,'method':'ordinary-power Fraction polynomial construction followed by direct Bernstein conversion; independent Machin/trig bounds','table_sha256':sha(tp),'classification_sha256':sha(rp),'seconds':time.monotonic()-started,'full_chain_proved':False}
(root/'ALL249_BULK_BYPASS_INDEPENDENT_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2),flush=True)
