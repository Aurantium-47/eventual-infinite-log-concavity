import sys
if not __debug__:
 raise RuntimeError('Assertions must be enabled; do not use python -O or -OO')
"""Memory-bounded explicit formula audit, independent rational arithmetic."""
import check_explicit as e
import json,time,gzip,math,hashlib,resource
from collections import deque
from pathlib import Path
p=Path(__file__).parent;results=[];st=time.monotonic()
nodes={r['node']:r['endpoints'] for r in json.loads((e.BASE/'nodes.json').read_text())['nodes']}
for panel,node in [(0,246),(7,237)]:
 r=next(json.loads(s) for s in gzip.open(e.BASE/f'jets_panel{panel}.jsonl.gz','rt') if json.loads(s)['node']==node)
 e.D=r['d'];K=r['K'];one=e.fmpq_poly([1]);zero=e.fmpq_poly([])
 u=e.fmpq_poly([e.fmpq(2*panel+1,64064),e.fmpq(1,64064)])
 falling=[one];powers=[one]
 for i in range(K+4):falling.append(e.mul(falling[-1],one-i*u));powers.append(e.mul(powers[-1],u))
 facts=[math.factorial(i) for i in range(K+5)]
 left,right=map(e.Q,nodes[node][panel:panel+2]);t=2/(1/left+1/right);beta=(1/right-1/left)*t/2
 x=e.fmpq_poly([-t**16*math.comb(15+i,i)*(-beta)**i for i in range(e.D+1)])
 queues=[deque([zero]) for _ in range(4)];out=zero;xp=one;count=0
 def feed(lev,v):
  global out,xp,count
  if lev==4:
   out+=e.mul(v,xp);xp=e.mul(xp,x);count+=1;return
  q=queues[lev];q.append(v)
  if len(q)==3:
   w=e.mul(q[1],q[1])-e.mul(q[0],q[2]);q.popleft();feed(lev+1,w)
 for k in range(K+5):
  b=zero
  for q in range(k//2+1):b+=e.mul(powers[q],falling[k-q])/e.fmpq(facts[q]*facts[k-2*q])
  feed(0,b)
  if k%25==0: print('stream',panel,node,k,'seconds',time.monotonic()-st,'peak_rss_kib',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,flush=True)
 assert count==K+1
 scale=e.fmpq(2)**(r['exponent']-r['precision']);checks=[]
 for i in range(e.D+1):
  assert (r['m'][i]-r['radius'])*scale<=out[i]<=(r['m'][i]+r['radius'])*scale
  checks.append({'order':i,'contained':True,'exact_value_sha256':hashlib.sha256(str(out[i]).encode()).hexdigest()})
 record={'panel':panel,'node':node,'K':K,'orders':checks,'status':'PASS'};results.append(record)
 (p/f'stream_full_panel{panel}_receipt.json').write_text(json.dumps(record,indent=2)+'\n')
 print('PASS full stream',panel,node,e.D+1,flush=True)
(p/'stream_full_receipt.json').write_text(json.dumps({'status':'PASS','cases':results,'elapsed_seconds':time.monotonic()-st,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2)+'\n')
