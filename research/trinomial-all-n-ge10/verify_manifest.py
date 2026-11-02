"""Authenticate released input files; this is not mathematical verification."""
from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parent
d=json.loads((r/'RELEASE_MANIFEST.json').read_text())
for e in d['files']:
 p=r/e['path']
 if not p.resolve().is_relative_to(r):raise RuntimeError('Invalid path')
 b=p.read_bytes()
 if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise RuntimeError('Mismatch: '+e['path'])
print('PASS: authenticated',len(d['files']),'released files; no mathematical verification performed')
