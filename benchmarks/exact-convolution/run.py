"""Run one deterministic certificate, explicitly selecting the backend."""
import argparse
import json
import platform
from pathlib import Path
import certificate
from backends import accelerated

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--backend', choices=['reference', 'flint'], required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
if not __debug__:
    p.error('Assertions must remain enabled (do not use python -O)')
if a.output.exists() and any(a.output.iterdir()):
    p.error('Choose an empty output directory to avoid overwriting evidence')
if a.backend == 'flint':
    certificate.iconv = accelerated
certificate.OUTPUT = a.output
certificate.run(panel=0, K=600, d=360, P=2048, index=200)
metadata = {'backend': a.backend, 'python': platform.python_version(),
            'machine': platform.machine(), 'system': platform.system()}
if a.backend == 'flint':
    import flint
    metadata['python_flint'] = flint.__version__
(a.output/'environment.json').write_text(json.dumps(metadata, indent=2)+'\n')
