"""Exact JSON comparison; ignore only two measured performance fields."""
import argparse
import json
from pathlib import Path
PERFORMANCE_FIELDS = {'seconds', 'peak_rss_kib'}

def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result

def _reject_constant(value):
    raise ValueError(f'Nonstandard JSON constant: {value}')

def read(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=_unique_object,
                      parse_constant=_reject_constant)

def exact_equal(a, b):
    """JSON equality without Python's bool/int/float coercion."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(exact_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(exact_equal(x, y) for x, y in zip(a, b))
    return a == b

def compare(final_a, receipt_a, final_b, receipt_b):
    if not exact_equal(read(final_a), read(final_b)):
        raise ValueError('FAIL: final midpoint/radius or parameter mismatch')
    a, b = read(receipt_a), read(receipt_b)
    a = {k: v for k, v in a.items() if k not in PERFORMANCE_FIELDS}
    b = {k: v for k, v in b.items() if k not in PERFORMANCE_FIELDS}
    if not exact_equal(a, b):
        raise ValueError('FAIL: nonperformance receipt mismatch')
    return True

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('reference', type=Path)
    p.add_argument('accelerated', type=Path)
    a = p.parse_args()
    compare(a.reference/'final_jet.json', a.reference/'receipt.json',
            a.accelerated/'final_jet.json', a.accelerated/'receipt.json')
    print('PASS: every final midpoint, common radius, parameter, and nonperformance receipt field agrees exactly')
