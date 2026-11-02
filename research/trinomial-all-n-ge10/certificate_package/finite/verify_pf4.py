if not __debug__: raise RuntimeError("Do not disable assertions")
# Exact PF4 seed certificates; algebraic finite-to-infinite reduction is in the accompanying proof.
from itertools import permutations,combinations_with_replacement
import json
perms=[]
for p in permutations(range(4)):
 inv=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4));perms.append((p,(-1)**inv))
def det4(a):
 total=0
 for p,sgn in perms:
  term=sgn
  for i in range(4):term*=a[i][p[i]]
  total+=term
 return total
def row(n):
 a=[1]
 for _ in range(n):
  b=[0]*(len(a)+2)
  for i,v in enumerate(a):
   for j in range(3):b[i+j]+=v
  a=b
 return a
out=[]
for n in (8,9):
 a=row(n); d=2*n;count=0;minimum=None
 for seq in combinations_with_replacement(range(d+1),4):
  u=seq[::-1]
  mat=[[a[u[i]-i+j] if 0<=u[i]-i+j<=d else 0 for j in range(4)] for i in range(4)]
  v=det4(mat);assert v>=0
  minimum=v if minimum is None else min(minimum,v);count+=1
 out.append({'n':n,'count':count,'minimum':minimum})
assert out==[{'n':8,'count':4845,'minimum':1},{'n':9,'count':7315,'minimum':1}]
print(json.dumps({'checks':out,'arithmetic':'fresh stdlib integer Leibniz determinants','scope':'PF4 base seeds only; LR minor reduction, Cauchy-Binet convolution closure, and Desnanot-Jacobi give L^0..L^3 nonnegative for all n>=56; no all-iteration inference'},indent=2))
