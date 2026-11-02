import sys
if not __debug__:
 raise RuntimeError('Assertions must be enabled; do not use python -O or -OO')
"""Independent exact Taylor check: no published generator/interval-jet imports.
Direct multinomial coefficient formula, rational polynomial arithmetic, four L maps.
"""
import gzip,json,math,time,hashlib,sys
from pathlib import Path
from flint import fmpq,fmpq_poly
BASE=Path(__file__).resolve().parents[2]/'certificate_package/edge'
D=3
Q=lambda x:fmpq(str(x))
def mul(a,b):return (a*b).truncate(D+1)
def coefficients(p,K):
 u=fmpq_poly([fmpq(2*p+1,64064),fmpq(1,64064)])
 one=fmpq_poly([1]); zero=fmpq_poly([])
 falling=[one]; powers=[one]
 for i in range(K+4):
  falling.append(mul(falling[-1],one-i*u));powers.append(mul(powers[-1],u))
 facts=[math.factorial(i) for i in range(K+5)]
 bs=[]
 for k in range(K+5):
  b=zero
  for q in range(k//2+1):b+=mul(powers[q],falling[k-q])/fmpq(facts[q]*facts[k-2*q])
  bs.append(b)
  if k%100==0: print('formula coefficient',p,k,flush=True)
 for lev in range(4):
  bs=[mul(v,v)-mul(bs[k-1] if k else zero,bs[k+1]) for k,v in enumerate(bs[:-1])]
  print('L layer',p,lev+1,flush=True)
 return bs

def check(p,j,bs,nodes):
 rows=[json.loads(s) for s in gzip.open(BASE/f'jets_panel{p}.jsonl.gz','rt')]
 r=next(r for r in rows if r['node']==j);K=r['K']
 left,right=map(Q,nodes[j][p:p+2]);t=2/(1/left+1/right)
 # normalized coordinate s=(u-c)/h; x(s)=-t^16*(1+beta*s)^(-16)
 beta=(1/right-1/left)*t/2
 x=fmpq_poly([-t**16*math.comb(15+i,i)*(-beta)**i for i in range(D+1)])
 out=fmpq_poly([])
 for b in reversed(bs[:K+1]):out=mul(out,x)+b
 shift=r['exponent']-r['precision'];scale=fmpq(2)**shift
 checks=[]
 for i in range(D+1):
  lo=(r['m'][i]-r['radius'])*scale; hi=(r['m'][i]+r['radius'])*scale
  assert lo<=out[i]<=hi,(p,j,i)
  checks.append({'order':i,'exact_value_sha256':hashlib.sha256(str(out[i]).encode()).hexdigest(),'numerator_bits':out[i].numerator.bit_length(),'denominator_bits':out[i].denominator.bit_length(),'contained':True})
 return {'panel':p,'node':j,'K':K,'orders':checks,'status':'PASS'}
if __name__=='__main__':
 st=time.monotonic();nodes={r['node']:r['endpoints'] for r in json.loads((BASE/'nodes.json').read_text())['nodes']}
 selected={0:[1,246],7:[1,237]};result=[]
 for p,js in selected.items():
  rs=[json.loads(s) for s in gzip.open(BASE/f'jets_panel{p}.jsonl.gz','rt')];K=max(r['K'] for r in rs if r['node'] in js)
  bs=coefficients(p,K)
  for j in js:
   result.append(check(p,j,bs,nodes));print('CHECK PASS',p,j,flush=True)
 receipt={'status':'PASS','method':'direct multinomial formula, exact fmpq polynomial Taylor algebra, independent four L maps','taylor_degree':D,'elapsed_seconds':time.monotonic()-st,'cases':result,'limitations':['Only orders 0..3 of finite K polynomial tested.','Does not independently certify tail/Cauchy/Bernstein bounds or whole interval.','Uses same official FLINT arithmetic library as primary regeneration, but different mathematical algorithm.']}
 (Path(__file__).parent/'explicit_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
