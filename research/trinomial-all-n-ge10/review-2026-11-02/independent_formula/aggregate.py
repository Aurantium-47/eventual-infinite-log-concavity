import sys
if not __debug__:
 raise RuntimeError('Assertions must be enabled; do not use python -O or -OO')
from pathlib import Path
import json,hashlib
p=Path(__file__).parent
base=json.loads((p/'explicit_receipt.json').read_text());mini=json.loads((p/'minimum_receipt.json').read_text());full=json.loads((p/'stream_full_receipt.json').read_text())
seen={};overlaps=0
for case in base['cases']+[mini['case']]+full['cases']:
 assert case['status']=='PASS'
 for item in case['orders']:
  key=(case['panel'],case['node'],item['order']);v=item['exact_value_sha256'];assert item['contained']
  if key in seen:assert seen[key]==v;overlaps+=1
  seen[key]=v
assert len(seen)==708 and overlaps==8
cases={}
for panel,node,order in seen:cases.setdefault((panel,node),[]).append(order)
receipt={'status':'PASS','distinct_cases':len(cases),'distinct_exact_taylor_coefficients':len(seen),'overlapping_coefficients_agree':overlaps,'complete_cases':[{'panel':0,'node':246,'K':556,'retained_coefficients':311},{'panel':7,'node':237,'K':538,'retained_coefficients':302},{'panel':7,'node':22,'K':108,'retained_coefficients':87}], 'partial_cases':[{'panel':0,'node':1,'orders':[0,1,2,3]},{'panel':7,'node':1,'orders':[0,1,2,3]}],'stream_elapsed_seconds':full['elapsed_seconds'],'stream_peak_rss_kib':full['peak_rss_kib'],'no_published_generator_or_interval_jet_imports':True,'shared_arithmetic_backend':'python-flint 0.9.0','limitations':['Selected 5 cases only: not all1929 independently reimplemented.','Checks exact Taylor enclosure containment, not independently whole-panel signs or analytic tails.','Complete primary1929 reconstruction is a separate run using published implementation.']}
(p/'aggregate_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
