"""Recompute interval enclosure provenance. Full run is opt-in; no checkpoints needed."""
from collections import deque
from fractions import Fraction as F
from math import comb
import time,json,argparse
import interval_jets as fj
from replay_saved_inequalities import load,records,verify
def generation(panel,K,D,P,c,h):
 zero=fj.Jet.zero(D,P);one=fj.Jet.rational(1,D,P);buffers=[deque([zero]) for _ in range(4)];out=[]
 def feed(level,x):
  if level==4:out.append(x);return
  b=buffers[level];b.append(x)
  if len(b)==3:
   y=b[1].mul(b[1]).add(b[0].mul(b[2]),-1);b.popleft();feed(level+1,y)
 prev=one;cur=one;feed(0,prev);feed(0,cur);start=time.perf_counter()
 for k in range(1,K+4):
  nxt=cur.rational_poly([(1-k*c)/F(k+1),-k*h/F(k+1)])
  pp=[2*c-(k-1)*c*c,2*h-2*(k-1)*c*h,-(k-1)*h*h]
  nxt=nxt.add(prev.rational_poly([x/F(k+1) for x in pp]));prev,cur=cur,nxt;feed(0,cur)
  if k%100==0:print('shared generated',k,'seconds',time.perf_counter()-start,flush=True)
 assert len(out)==K+1
 return out,time.perf_counter()-start

def evaluate(shared,r,c,h,L,R):
 K,d,P=r['K'],r['d'],r['precision'];t=2/(1/L+1/R);a=(1/R-1/L)*t/(2*h)
 coeff=[x.truncate(d).reprecision(P) for x in shared[:K+1]]
 q=fj.Jet.zero(d,P)
 for j in range(d+1):q=q.add(fj.Jet.rational(-t**16*comb(15+j,j)*(-a*h)**j,d,P).shift(j))
 value=coeff[-1]
 for b in reversed(coeff[:-1]):value=value.mul(q).add(b)
 assert value.record()=={'m':r['m'],'rad':r['radius'],'e':r['exponent'],'p':P}
 return value

def main(panel,node,backend,full):
 if backend=='flint':
  import flint
  from flint import fmpz_poly
  assert flint.__version__=='0.9.0'
  def conv(a,b,d):
   n=min(d+1,len(a)+len(b)-1);v=fmpz_poly(a).mul_low(fmpz_poly(b),n)
   return [int(v[k]) for k in range(n)]
  fj.set_backend(conv,'python-flint0.9.0')
 m,us,nodes=load();count=0
 for p in (range(8) if full else [panel]):
  chosen=[r for r in records(m,p) if full or r['node']==node];assert chosen
  c=(us[p]+us[p+1])/2;h=(us[p+1]-us[p])/2
  shared,_=generation(p,600,360,2048,c,h)
  for r in chosen:
   evaluate(shared,r,c,h,*nodes[r['node']][p:p+2]);verify(r,us,nodes);count+=1
  print('panel',p,'matched',len(chosen),flush=True)
 print(json.dumps({'status':'PASS','deterministic_enclosures_regenerated':count,'full_edge_generation':full}))
if __name__=='__main__':
 if not __debug__:raise RuntimeError('Do not run with Python -O')
 p=argparse.ArgumentParser();p.add_argument('--full',action='store_true');p.add_argument('--panel',type=int,choices=range(8),default=0);p.add_argument('--node',type=int,choices=range(1,250),default=200);p.add_argument('--backend',choices=['flint','byte'],default='flint');a=p.parse_args();main(a.panel,a.node,a.backend,a.full)
