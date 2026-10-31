if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
"""Independent integer-encoded polynomial evaluator; no author code imported."""
from fractions import Fraction
from functools import lru_cache
from collections import defaultdict
from pathlib import Path
import ast,re,json,time
root=Path(__file__).parent
nodes=[(start,start+length//2,start+length) for length in (2,4,8,16) for start in range(0,16,length)]
units=[1<<(5*j) for j in range(15)]; paritymask=sum(units)

def times(p,q):
 r=defaultdict(int)
 for a,x in p.items():
  for b,y in q.items():r[a+b]+=x*y
 return {a:x for a,x in r.items() if x}

bases=[]
for degree in (3,4,5,6):
 result=defaultdict(int)
 for leaf in range(16):
  linear={units[j]:(16//(b-a))*(1 if leaf<m else -1) for j,(a,m,b) in enumerate(nodes) if a<=leaf<b}
  p={0:1}
  for _ in range(degree):p=times(p,linear)
  for k,x in p.items():result[k]+=x
 bases.append({k:x for k,x in result.items() if x})
bases.append({2*u:1 for u in units})
@lru_cache(None)
def polynomial(exps):
 p={0:1}
 for e,b in zip(exps,bases):
  for _ in range(e):p=times(p,b)
 return p

def grouped(p):
 g=defaultdict(list)
 for k,x in p.items():g[k&paritymask].append((k,x))
 return g

moments=[]
for lo,mid,hi in nodes:
 a=[0]*19
 for j in range(0,19,2):
  df=1
  for x in range(1,j+2,2):df*=x
  a[j]=df*(hi-lo)**(j//2)
 moments.append(a)
@lru_cache(None)
def monomial_moment(key):
 result=1
 for j in range(15):
  exp=key&31;key>>=5
  assert exp<19
  result*=moments[j][exp]
 return result

def evaluate(exps):
 # Split by factor count, unlike author's degree-balancing partition.
 factors=[j for j,e in enumerate(exps) for _ in range(e)]
 left=[0]*5;right=[0]*5
 for i,j in enumerate(factors):(left if i%2==0 else right)[j]+=1
 a=grouped(polynomial(tuple(left)));b=grouped(polynomial(tuple(right)))
 total=0
 for parity,terms in a.items():
  for ka,va in terms:
   for kb,vb in b.get(parity,()):total+=va*vb*monomial_moment(ka+kb)
 denom_degree=sum(e*d for e,d in zip(exps,(3,4,5,6,0)))
 return Fraction(total,16**denom_degree)

expected={}
for line in (root/'LOCAL_HOMOTOPY_BUDGET.log').read_text().splitlines():
 if line.startswith('moment '):
  match=re.fullmatch(r'moment (\(.*?\)) (.*)',line)
  expected[ast.literal_eval(match[1])]=Fraction(match[2])
ans={}
for exps,value in expected.items():
 start=time.time();actual=evaluate(exps)
 assert actual==value,(exps,actual,value)
 ans[str(exps)]=str(actual)
 print('PASS',exps,actual,'seconds',round(time.time()-start,3),flush=True)
(root/'LOCAL_HOMOTOPY_INDEPENDENT_MOMENTS.json').write_text(json.dumps(ans,indent=2)+'\n')
print('ALL',len(ans),'independently encoded exact moments PASS',flush=True)
