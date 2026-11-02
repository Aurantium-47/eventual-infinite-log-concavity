"""Verify saved or newly replayed exact outputs; does not run timing jobs."""
import argparse
from pathlib import Path
import sys
if not __debug__:
    raise SystemExit("Assertions must remain enabled; do not use -O, -OO or PYTHONOPTIMIZE")
BASE = Path(__file__).resolve().parent
BENCH = BASE.parent.parent
sys.path.insert(0, str(BENCH))
from compare import compare
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--runs', type=Path, default=BASE/'runs')
a = p.parse_args()
for pair in range(1, 4):
    paths = [a.runs/f'pair{pair}_{backend}' for backend in ('reference', 'flint')]
    for path in paths:
        compare(BENCH/'evidence/expected_final_jet.json', BENCH/'evidence/reference_receipt.json', path/'final_jet.json', path/'receipt.json')
    compare(paths[0]/'final_jet.json', paths[0]/'receipt.json', paths[1]/'final_jet.json', paths[1]/'receipt.json')
    print(f'PAIR {pair}: both fixtures and pair exact PASS')
