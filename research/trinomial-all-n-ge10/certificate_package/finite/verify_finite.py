"""Exact finite-exponent verification for trinomial infinite log-concavity.
Python standard library only. Run without -O: assertions are proof checks.
"""
from pathlib import Path
import argparse, hashlib, json, time, sys
if not __debug__:
    raise RuntimeError("Assertions must remain enabled; do not use python -O")
P=256;S=1<<P

def up(n,d):
    assert n>=0 and d>0
    q,r=divmod(n,d)
    return q+bool(r)

def initial_q(n):
    assert n>=1
    rl=[0,n*S];ru=[0,n*S]
    for k in range(1,n):
        a=n-k;b=2*n-k+1
        # r_(k+1)=[a+b/r_k]/(k+1), decreasing in r_k.
        rl.append((a*S*ru[k]+b*S*S)//((k+1)*ru[k]))
        ru.append(up(a*S*rl[k]+b*S*S,(k+1)*rl[k]))
        assert 0<rl[-1]<=ru[-1]
    low=[0];high=[0]
    for k in range(1,n):
        low.append(S*rl[k+1]//ru[k])
        high.append(up(S*ru[k+1],rl[k]))
    low.append(S**3//ru[n]**2)
    high.append(up(S**3,rl[n]**2))
    return low,high,rl,ru

def advance(low,high):
    n=len(low)-1
    assert all(0<=a<=b<S for a,b in zip(low,high))
    ll=[0];hh=[0]
    for k in range(1,n+1):
        neighbor=k+1 if k<n else n-1
        a,b=low[k],high[k]
        ll.append(a*a*(S-high[k-1])*(S-high[neighbor])//(S*(S-a)**2))
        hh.append(up(b*b*(S-low[k-1])*(S-low[neighbor]),S*(S-b)**2))
    return ll,hh

def verify_n(n):
    low,high,rl,ru=initial_q(n)
    init_digest=hashlib.sha256(json.dumps([rl,ru],separators=(',',':')).encode()).hexdigest()
    stages=[]
    for depth in range(31):
        assert all(0<=a<=b<S for a,b in zip(low,high)),(n,depth,'not strictly positive next iterate')
        maximum=max(high)
        stages.append({'depth':depth,'maximum_upper_integer':str(maximum),'interval_sha256':hashlib.sha256(json.dumps([low,high],separators=(',',':')).encode()).hexdigest()})
        if 3*maximum<=S:
            return {'n':n,'cone_depth':depth,'ratio_initializer_sha256':init_digest,'stages':stages}
        low,high=advance(low,high)
    raise AssertionError((n,'cone not reached by depth30; NOT a counterexample'))

def toy_checks():
    # Exact rows built by repeated convolution, not the coefficient recurrence.
    row=[1];initial_tests=0;propagation_tests=0
    for n in range(1,31):
        nxt=[0]*(len(row)+2)
        for k,x in enumerate(row):
            nxt[k]+=x;nxt[k+1]+=x;nxt[k+2]+=x
        row=nxt
        low,high,rl,ru=initial_q(n)
        for k in range(1,n+1):
            assert rl[k]*row[k-1]<=S*row[k]<=ru[k]*row[k-1]
            numerator=S*row[k-1]*row[k+1];denominator=row[k]**2
            assert low[k]*denominator<=numerator<=high[k]*denominator
            initial_tests+=1
        if n>=10:
            exact=row[:]
            for depth in range(5):
                assert all(0<=a<=b<S for a,b in zip(low,high))
                for k in range(1,n+1):
                    numerator=S*exact[k-1]*exact[k+1];denominator=exact[k]**2
                    assert low[k]*denominator<=numerator<=high[k]*denominator
                    propagation_tests+=1
                if depth<4:
                    padded=[0]+exact+[0]
                    exact=[padded[k+1]**2-padded[k]*padded[k+2] for k in range(len(exact))]
                    assert min(exact)>0
                    low,high=advance(low,high)
    results=[verify_n(n) for n in range(10,31)]
    return {'status':'PASS','mode':'toy only','exact_initial_ratio_coefficient_checks':initial_tests,'exact_iterated_q_checks':propagation_tests,'small_cone_cases':len(results),'max_small_cone_depth':max(r['cone_depth'] for r in results),'scope':'independent initialization/propagation tests; full range NOT run'}

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full', action='store_true', help='Verify every exponent 10..4003; otherwise run small exact oracle tests')
    parser.add_argument('--output', type=Path, default=Path('finite_result.json'))
    args=parser.parse_args()
    if not args.full:
        report=toy_checks()
    else:
        started=time.monotonic(); rows=[]
        for n in range(10,4004):
            rows.append(verify_n(n))
            if n%100==0:
                print(n, 'PASS', round(time.monotonic()-started,2), flush=True)
        assert [r['n'] for r in rows]==list(range(10,4004))
        digest=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        assert digest=='d9863aac855893ef8c8a670ee6c3c3f2a4f611f1d98f793491d8a43b2c2786ba', ('Unexpected exact result digest',digest)
        report={'status':'PASS','range_inclusive':[10,4003],'count':3994,
                'precision_bits':P,'max_cone_depth':max(r['cone_depth'] for r in rows),
                'seconds':time.monotonic()-started,'results':rows}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
