"""Exact replay GIVEN saved enclosures, not enclosure-provenance regeneration."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,gzip,sys,argparse
from certificate_math import bernstein,analytic_errors
from interval_jets import Jet
from bulk_bounds import certify_harmonic_panel,certify_join
sys.set_int_max_str_digits(0)
BASE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def load():
 m=json.loads((BASE/'data_manifest.json').read_text());raw=(BASE/'nodes.json').read_bytes();assert sha(raw)==m['nodes_sha256'];t=json.loads(raw)
 us=list(map(F,t['u_endpoints']));assert us==[F(i,32032) for i in range(9)]
 assert [r['node'] for r in t['nodes']]==list(range(1,250))
 nodes={r['node']:list(map(F,r['endpoints'])) for r in t['nodes']}
 assert all(len(v)==9 and min(v)>0 for v in nodes.values())
 return m,us,nodes
def records(m,panel=None):
 assert len(m['parts'])==8
 for p,part in enumerate(m['parts']):
  if panel is not None and p!=panel:continue
  assert part['file']==f'jets_panel{p}.jsonl.gz'
  blob=(BASE/part['file']).read_bytes();assert len(blob)==part['bytes'] and sha(blob)==part['sha256'];raw=gzip.decompress(blob);assert sha(raw)==part['uncompressed_sha256']
  rows=[json.loads(line) for line in raw.splitlines()];assert len(rows)==part['cases']
  for r in rows:assert r['panel']==p;yield r
def verify(r,us,nodes):
 for k in ['panel','node','K','d','precision','radius','exponent']:assert type(r[k]) is int
 p,j,K,d,P=r['panel'],r['node'],r['K'],r['d'],r['precision']
 assert 0<=p<8 and 1<=j<=249 and 0<=K<=600 and 0<=d<=360 and P>=2 and r['radius']>=0
 assert len(r['m'])==d+1 and all(type(x) is int for x in r['m'])
 c=(us[p]+us[p+1])/2;h=(us[p+1]-us[p])/2;L,R=nodes[j][p:p+2];t=2/(1/L+1/R);a=(1/R-1/L)*t/(2*h)
 jet=Jet.from_record({'m':r['m'],'rad':r['radius'],'e':r['exponent'],'p':P})
 low,high,roundoff=bernstein(jet);err,tail,_=analytic_errors(c,h,4*h,t,a,0,K,d,max(L,R),c+h)
 assert (low>err+tail) if j%2==0 else (high < -err-tail)
 return True
def main(panel=None):
 m,us,nodes=load();selected=range(8) if panel is None else [panel];seen=set();count=bulk=0
 for r in records(m,panel):
  pair=(r['panel'],r['node']);assert pair not in seen;seen.add(pair);verify(r,us,nodes);count+=1
 for p,j in m['bypasses']:
  if p not in selected:continue
  assert 0<=p<8 and 1<=j<=249 and (p,j) not in seen
  assert certify_harmonic_panel(*nodes[j][p:p+2],us[p],us[p+1],j)['bypass'];seen.add((p,j));bulk+=1
 for p in selected:
  assert all(nodes[j][i]<nodes[j+1][i] for j in range(1,249) for i in [p,p+1])
  assert certify_join(*nodes[249][p:p+2],us[p],us[p+1])
 assert seen=={(p,j) for p in selected for j in range(1,250)}
 if panel is None:assert count==1929 and bulk==63
 print(json.dumps({'status':'PASS','jet_inequalities':count,'bulk_boxes':bulk,'ordering_and_join':True,'enclosure_provenance_recomputed':False,'analytic_bulk_theorem_reproved':False}))
if __name__=='__main__':
 if not __debug__:raise RuntimeError('Do not run with Python -O')
 p=argparse.ArgumentParser();p.add_argument('--panel',type=int,choices=range(8));a=p.parse_args();main(a.panel)
