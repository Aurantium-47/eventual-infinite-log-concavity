# Exact edge certificates

This directory covers 249 moving real nodes on eight closed parameter panels
`u in [i/32032,(i+1)/32032]`, i=0,...,7. Thus it covers `0 <= u <= 1/4004`.
The original application substitutes u=1/n. All numbers stored here are exact.

## Three distinct verification levels

1. `python edge/replay_saved_inequalities.py` (standard library only) checks
   hashes, all **1,929 strict sign inequalities given the saved interval jets**,
   63 bulk-bypass arithmetic tests, node ordering and the last-node join.
   It recomputes the Bernstein bounds and both analytic truncation-error budgets.
   It does **not** recompute the provenance of the saved jet enclosures, nor prove
   the analytic bulk theorem. Its output explicitly reports these exclusions.
2. `python edge/regenerate.py --panel 0 --node 200` regenerates one representative
   enclosure from the coefficient recurrence, four L operations and Horner
   evaluation, then compares every midpoint, common radius and binary exponent.
3. `python edge/regenerate.py --full` regenerates **all 1,929 enclosures** and
   compares those exact deterministic mathematical outputs. Combine this with
   step 1, the analytic proofs/checks in `../analytic/`, and `../finite/` for the
   entire computer-assisted argument. The packaged full-generation command has
   not itself been run across all cases; the original generating program was.

Default generation requires `python-flint==0.9.0`; `--backend byte` uses an exact
standard-library signed-integer convolution instead (substantially slower).
Run with Python 3.11+ **without `-O`**, since assertions are verification checks.
Commands above assume the working directory is `certificate_package`.
Data lookup is relative to the scripts and is otherwise working-directory independent.
No command downloads, publishes, or writes to external services.

## Stored data and omitted data

`nodes.json` is the exact first nine endpoints of each of the 249 original
rational harmonic node families. Each `jets_panelN.jsonl.gz` stores original
unmodified final interval jets. `data_manifest.json` binds their compressed and
uncompressed bytes, case counts, node table and the 63 bypass pairs.
Shared coefficient checkpoints (317 MB) are deliberately omitted: step 1 does
not claim to verify their provenance, and step 3 reconstructs them in memory.
No timing, machine paths or gzip metadata are compared during regeneration.

## Mathematical interface

For zero-extended sequences, L(a)_k=a_k^2-a_(k-1)a_(k+1). Let b_(0,k)(u)
be the coefficient of z^k in (1+uz+u^2 z^2)^(1/u), with removable value exp(z)
at u=0. Generate by b_(0,0)=b_(0,1)=1 and

    (k+1)b_(0,k+1)=(1-ku)b_(0,k)+u(2-(k-1)u)b_(0,k-1).

Apply L four times to obtain b_(4,k). For integer n=1/u, the evaluated series
is f_(n,4)(x/n^16). A harmonic node joins positive endpoints L,R by
`t(u)=t0/(1+a(u-c))`, where t0=2/(1/L+1/R),
a=(1/R-1/L)t0/(2h), c=(u_left+u_right)/2, h=(u_right-u_left)/2.
The tested value is sum b_(4,k)(u)(-t(u)^16)^k; its sign is (-1)^j.

A stored jet encloses each coefficient in w=(u-c)/h by
`2^(exponent-precision)*(m_i + [-radius,radius])`.
The replay bounds its midpoint polynomial by exact Bernstein controls and adds
`(d+1)*radius*2^(exponent-precision)`. The two additional rational errors bound
parameter Taylor truncation and the infinite coefficient tail. Their derivation
is a proof prerequisite, not inferred merely from passing arithmetic.
Generation uses K=600,d=360,P=2048 shared coefficients; each case retains its
stored K,d,P, identically to the original computation.

The 63 bypasses require the analytic theorem that V>=250 and phase distance
<=1/3 give the indicated sign (relative error <47/50 and cos(1/3)>=17/18).
Ordering follows from endpoint ordering of harmonic interpolants. The final join
places node249 below bulk phase250. These edge checks alone are not the original
infinite-log-concavity theorem: the bulk/root-count proof, earlier-layer
nonnegativity, preservation theorem and finite-range proof remain separate.
