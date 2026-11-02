import sys
if not __debug__:
 raise RuntimeError('Assertions must be enabled; do not use python -O or -OO')
import check_explicit as e
import json,time,hashlib
from pathlib import Path
p=Path(__file__).parent
candidate=json.loads((p.parent/'evidence/minimum-margins.json').read_text())[0]
e.D=candidate['d'];st=time.monotonic()
nodes={r['node']:r['endpoints'] for r in json.loads((e.BASE/'nodes.json').read_text())['nodes']}
bs=e.coefficients(candidate['panel'],candidate['K'])
r=e.check(candidate['panel'],candidate['node'],bs,nodes)
receipt={'status':'PASS','case':r,'elapsed_seconds':time.monotonic()-st,'all_retained_orders_independently_checked':True,'selection':'lowest relative sign margin across 1929 records from parent ranking','selection_sha256':hashlib.sha256((p.parent/'evidence/minimum-margins.json').read_bytes()).hexdigest()}
(p/'minimum_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS all retained orders',e.D+1,'seconds',receipt['elapsed_seconds'],flush=True)
