"""Fast deterministic arithmetic and comparator regression tests."""
import json
import random
import tempfile
import unittest
from pathlib import Path
from backends import reference, accelerated
from compare import compare, read, exact_equal

class ExactTests(unittest.TestCase):
    def test_signed_zero_truncated(self):
        rng = random.Random(313107)
        for k in range(160):
            a = [rng.randrange(-1000, 1001) for _ in range(rng.randrange(1, 25))]
            b = [rng.randrange(-1000, 1001) for _ in range(rng.randrange(1, 25))]
            if k % 7 == 0:
                a = [0]*len(a)
            if k % 9 == 0:
                b[-1] = 0
            d = rng.randrange(40)
            n = min(d+1, len(a)+len(b)-1)
            expected = [sum(a[j]*b[i-j] for j in range(len(a))
                            if 0 <= i-j < len(b)) for i in range(n)]
            self.assertEqual(reference(a,b,d), expected)
            self.assertEqual(accelerated(a,b,d), expected)

    def test_big_signed_coefficients(self):
        rng = random.Random(411)
        for d, bits in [(8,1024), (16,2048)]:
            a = [rng.getrandbits(bits)*rng.choice([-1,1]) for _ in range(d+1)]
            b = [rng.getrandbits(bits)*rng.choice([-1,1]) for _ in range(d+1)]
            self.assertEqual(reference(a,b,d), accelerated(a,b,d))

    def test_comparator_rejects_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)
            def write(name, value):
                (p/name).write_text(json.dumps(value))
                return p/name
            fa=write('a.json', {'midpoints':[1,2], 'radius':3})
            fb=write('b.json', {'midpoints':[1,2], 'radius':3})
            ra=write('ra.json', {'certified_positive':True,'seconds':1,'peak_rss_kib':10})
            rb=write('rb.json', {'certified_positive':True,'seconds':2,'peak_rss_kib':20})
            self.assertTrue(compare(fa,ra,fb,rb))
            for field, value in [('radius',4),('midpoints',[1,3])]:
                obj={'midpoints':[1,2],'radius':3};obj[field]=value
                write('b.json',obj)
                with self.assertRaises(ValueError):compare(fa,ra,fb,rb)
            write('b.json',{'midpoints':[1,2],'radius':3})
            write('rb.json',{'certified_positive':False,'seconds':2,'peak_rss_kib':20})
            with self.assertRaises(ValueError):compare(fa,ra,fb,rb)

    def test_type_mismatches_rejected(self):
        for a, b in [({'P':2048}, {'P':2048.0}),
                     ({'certified_positive':True}, {'certified_positive':1}),
                     ({'midpoints':[1,2]}, {'midpoints':[True,2]}),
                     ({'radius':3}, {'radius':3.0})]:
            self.assertFalse(exact_equal(a,b))
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)
            final={'midpoints':[1,2], 'radius':3, 'P':2048}
            receipt={'certified_positive':True, 'seconds':1}
            for name,obj in [('a',final),('b',final),('ra',receipt),('rb',receipt)]:
                (p/name).write_text(json.dumps(obj))
            for key,value in [('P',2048.0),('midpoints',[True,2]),('radius',3.0)]:
                (p/'b').write_text(json.dumps({**final,key:value}))
                with self.assertRaises(ValueError):compare(p/'a',p/'ra',p/'b',p/'rb')
            (p/'b').write_text(json.dumps(final))
            (p/'rb').write_text(json.dumps({**receipt,'certified_positive':1}))
            with self.assertRaises(ValueError):compare(p/'a',p/'ra',p/'b',p/'rb')

    def test_ambiguous_json_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'bad.json'
            for text in ['{"P":2048,"P":2048}', '{"x":NaN}',
                         '{"x":Infinity}', '{"x":-Infinity}']:
                p.write_text(text)
                with self.assertRaises(ValueError):read(p)

if __name__ == '__main__':
    unittest.main()
