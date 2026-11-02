"""Independent final-join verification from receipt rational nodes ONLY.
Direct Bernstein-basis arithmetic; no phase solver, mpmath, or source checker import.
Uses fresh simpler certified pi brackets and independent Taylor truncations.
"""
from fractions import Fraction as Q
from math import comb,factorial
from pathlib import Path
import json
def atbr(x,k):
 p=sum((Q((-1)**i,2*i+1)*x**(2*i+1) for i in range(k)),Q(0))
 nxt=Q((-1)**k,2*k+1)*x**(2*k+1)
 return min(p,p+nxt),max(p,p+nxt)
a,b=atbr(Q(1,5),40);c,d=atbr(Q(1,239),12)
pi_lower=Q(3141592653589793,10**15);pi_upper=Q(3141592653589794,10**15)
assert pi_lower<16*a-4*d<16*b-4*c<pi_upper

def trigbr(x,cosine):
 offset=0 if cosine else 1
 vals=[Q((-1)**k,factorial(2*k+offset))*x**(2*k+offset) for k in range(17)]
 v=sum(vals[:16],Q(0));return min(v,v+vals[16]),max(v,v+vals[16])
B={'c':(Q(980785280403,10**12),Q(980785280404,10**12)),
'd':(Q(195090322016,10**12),Q(195090322017,10**12)),
'c2':(Q(923879532511,10**12),Q(923879532512,10**12)),
'd2':(Q(382683432365,10**12),Q(382683432366,10**12))}
for key,den,cosine in [('c',16,True),('d',16,False),('c2',8,True),('d2',8,False)]:
 lo=trigbr((pi_upper if cosine else pi_lower)/den,cosine)[0]
 hi=trigbr((pi_lower if cosine else pi_upper)/den,cosine)[1]
 assert B[key][0]<lo<hi<B[key][1]

def elevate(a,n):
 while len(a)<=n:
  d=len(a)-1
  a=[a[0]]+[Q(i,d+1)*a[i-1]+Q(d+1-i,d+1)*a[i] for i in range(1,d+1)]+[a[-1]]
 return a

def plus(a,b):
 n=max(len(a),len(b))-1;a=elevate(a,n);b=elevate(b,n)
 return [x+y for x,y in zip(a,b)]
def scale(a,c):return [c*x for x in a]
def times(a,b):
 m=len(a)-1;n=len(b)-1
 return [sum((Q(comb(m,i)*comb(n,k-i),comb(m+n,k))*a[i]*b[k-i] for i in range(max(0,k-n),min(m,k)+1)),Q(0)) for k in range(m+n+1)]
def power(a,n):
 r=[Q(1)]
 for _ in range(n):r=times(r,a)
 return r
def rat_atan(n,d,u,order,divide_u):
    # Returns numerator and denominator; order3 or5.
    if order==3:
        num=plus(times(n,power(d,2)),scale(times(power(u,2),power(n,3)),-Q(1,3)))
        den=power(d,3)
    else:
        num=plus(plus(times(n,power(d,4)),scale(times(times(power(u,2),power(n,3)),power(d,2)),-Q(1,3))),scale(times(power(u,4),power(n,5)),Q(1,5)))
        den=power(d,5)
    if not divide_u:num=times(u,num)
    return num,den

def phase_gap(np,dp,nq,dq,u,lower,node_index):
    pn,pd=rat_atan(np,dp,u,3 if lower else 5,True)
    qn,qd=rat_atan(nq,dq,u,5 if lower else 3,False)
    common=times(pd,qd)
    expr=plus(times(times(plus([Q(16)],scale(u,45)),pn),qd),scale(times(qn,pd),-Q(45,2)))
    C=Q(node_index)+Q(45,32)
    if lower:
        return plus(expr,scale(common,Q(1,3)-C*pi_upper))
    return plus(scale(common,C*pi_lower+Q(1,3)),scale(expr,-1))

def certify_harmonic_panel(L,R,u_left,u_right,node_index):
    assert L>0 and R>0 and 0<=u_left<u_right<=Q(1,1001)
    A=[L*R];bb=[R,L];u=[Q(u_left),Q(u_right)]
    ab=times(A,bb);a2=power(A,2);ua2=times(u,a2);uab=times(u,ab);u2a2=times(power(u,2),a2)
    b2=power(bb,2)
    def ratio(weight,upper):
        numer=plus(scale(ab,weight*B['d'][int(upper)]),scale(ua2,B['d2'][int(upper)]))
        denom=plus(plus(b2,scale(uab,weight*B['c'][int(not upper)])),scale(u2a2,B['c2'][int(not upper)]))
        assert min(denom)>0 and min(numer)>0
        return numer,denom
    pu=ratio(1,True);pl=ratio(1,False);qu=ratio(4,True);ql=ratio(4,False)
    uppergap=phase_gap(*pu,*ql,u,False,node_index)
    lowergap=phase_gap(*pl,*qu,u,True,node_index)
    central=plus(plus(b2,uab),u2a2)
    vgap=plus(times(ab,plus(plus(b2,scale(uab,4)),u2a2)),scale(power(central,2),-250))
    disk=plus(bb,scale(times(u,A),-1))
    caps=[plus(den,scale(times(u,num),-1)) for num,den in [pu,pl,qu,ql]]
    checks={'V_ge_250':min(vgap)>0,'phase_upper_1over3':min(uppergap)>0,'phase_lower_minus1over3':min(lowergap)>0,'s_lt_1':min(disk)>0,'all_ratio_caps_lt1':all(min(v)>0 for v in caps)}
    return {'checks':checks,'bypass':all(checks.values()),'degrees':{'V':len(vgap)-1,'phase_upper':len(uppergap)-1,'phase_lower':len(lowergap)-1},'minimum_controls':{'V':str(min(vgap)),'phase_upper':str(min(uppergap)),'phase_lower':str(min(lowergap)),'disk':str(min(disk)),'ratio_caps':str(min(min(v) for v in caps))}}

def certify_join(L,R,u_left,u_right):
 # Bernstein controls of B and u; A is constant.
 A=[L*R];bb=[R,L];uu=[u_left,u_right]
 ab=times(A,bb);ua2=times(uu,power(A,2));uab=times(uu,ab);u2a2=times(power(uu,2),power(A,2))
 pl=plus(scale(ab,B['d'][1]),scale(ua2,B['d2'][1]))
 pd=plus(plus(power(bb,2),scale(uab,B['c'][0])),scale(u2a2,B['c2'][0]))
 ql=plus(scale(ab,4*B['d'][0]),scale(ua2,B['d2'][0]))
 qd=plus(plus(power(bb,2),scale(uab,4*B['c'][1])),scale(u2a2,B['c2'][1]))
 qcheck=plus(qd,scale(times(uu,ql),-1));assert min(qcheck)>0
 pp=plus(plus(times(pl,power(pd,4)),scale(times(times(power(uu,2),power(pl,3)),power(pd,2)),-Q(1,3))),scale(times(power(uu,4),power(pl,5)),Q(1,5)))
 qp=plus(times(times(uu,ql),power(qd,2)),scale(times(power(uu,3),power(ql,3)),-Q(1,3)))
 gap=plus(plus(scale(times(power(pd,5),power(qd,3)),Q(8045,32)*pi_lower),scale(times(times(plus([Q(16)],scale(uu,45)),pp),power(qd,3)),-1)),scale(times(qp,power(pd,5)),Q(45,2)))
 assert len(gap)==17 and min(gap)>0

 return True
