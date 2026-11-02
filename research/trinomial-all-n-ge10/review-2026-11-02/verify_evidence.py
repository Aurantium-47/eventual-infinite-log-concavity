"""Authenticate curated evidence and frozen edge inputs; not a theorem prover."""
from pathlib import Path
import hashlib,json,sys
if not __debug__:
 raise RuntimeError('Assertions must be enabled')
B=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
manifest=json.loads((B/'MANIFEST.json').read_text())
for name,digest in manifest['files'].items():require(sha(B/name)==digest,'Evidence hash: '+name)
receipt=json.loads((B/'evidence/receipt.json').read_text());edge=B.parent/'certificate_package/edge'
for section in ['source_sha256','input_sha256']:
 for name,digest in receipt[section].items():require(sha(edge/name)==digest,'Frozen source/input hash: '+name)
require(sha(B/'evidence/full-regenerate.log')==receipt['full_log_sha256'],'Full log hash')
require((B/'evidence/full-regenerate.exit').read_text().strip()=='0','Full-run exit')
require('"deterministic_enclosures_regenerated": 1929, "full_edge_generation": true' in (B/'evidence/full-regenerate.log').read_text(),'Terminal record')
require(sha(B/'evidence/canonical_cases.json')==receipt['canonical_saved_jets_digest'],'Saved record digest')
for item in json.loads((B/'SOURCE_MAP.json').read_text())['files']:
 require(sha(B/item['public_path'])==item['published_sha256'],'Source mapping '+item['public_path'])
a=json.loads((B/'independent_formula/aggregate_receipt.json').read_text())
require(a['distinct_exact_taylor_coefficients']==708 and a['overlapping_coefficients_agree']==8,'Selected coverage')
print(json.dumps({'status':'PASS','curated_files':len(manifest['files']),'frozen_edge_source_and_data':'byte-identical','limits':'Identity and receipt checks only; not execution attestation or theorem verification'}))
