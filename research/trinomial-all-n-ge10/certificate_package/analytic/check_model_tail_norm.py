"""Reconstruct the Gaussian correction L2 constant from regenerated exact moments."""
if not __debug__:raise RuntimeError('Assertions must remain enabled')
from fractions import Fraction as F
from pathlib import Path
import json,ast
p=Path(__file__).parent
m={ast.literal_eval(k):F(v) for k,v in json.loads((p/'LOCAL_HOMOTOPY_INDEPENDENT_MOMENTS.json').read_text()).items()}
b=F(20,19);a=b/12;c=b*b/18;d=b**3/50
value=a*a*m[0,0,0,0,2]+c*c*m[0,2,0,0,0]+d*d*m[4,0,0,0,0]+2*a*c*m[0,1,0,0,1]+2*a*d*m[2,0,0,0,1]+2*c*d*m[2,1,0,0,0]
assert value==F(7405704307825,1693651716)<67**2
print('PASS reconstructed squared model-tail norm:',value)
