"""Reference exact signed integer convolution using byte-buffer packing.
"""
def convolution(a,b,degree):
 n=min(degree,len(a)+len(b)-2)+1
 if not any(a) or not any(b):return [0]*n
 bits=max(abs(x).bit_length() for x in a)+max(abs(x).bit_length() for x in b)+min(len(a),len(b)).bit_length()+2
 width=(bits+7)//8;bits=8*width;base=1<<bits;mask=base-1;half=base>>1
 def pack(a):
  carry=0;parts=[]
  for x in a:
   y=x+carry;parts.append((y&mask).to_bytes(width,'little'));carry=y>>bits
  return int.from_bytes(b''.join(parts),'little')+(carry<<(bits*len(a)))
 product=pack(a)*pack(b)
 raw=(product&((1<<(bits*n))-1)).to_bytes(width*n,'little')
 out=[];carry=0
 for i in range(n):
  y=int.from_bytes(raw[i*width:(i+1)*width],'little')+carry
  if y>=half:y-=base;carry=1
  else:carry=0
  out.append(y)
 return out
if __name__=='__main__':
 import random
 r=random.Random(249)
 for la,lb,degree in [(10,10,18),(60,80,60),(361,361,360)]:
  a=[r.randrange(-10**10,10**10) for _ in range(la)];b=[r.randrange(-10**10,10**10) for _ in range(lb)]
  actual=[0]*(min(degree,la+lb-2)+1)
  for i,x in enumerate(a):
   for j,y in enumerate(b[:max(0,len(actual)-i)]):actual[i+j]+=x*y
  assert convolution(a,b,degree)==actual
 print('Three seeded exact classical-convolution comparisons PASS; no large benchmark.')
