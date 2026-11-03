# Independent review of the existing general Theorem B

**Review date:** 2026-11-02; independent cross-check incorporated 2026-11-03. **Review type:** AI-assisted independent mathematical audit (独立自动数学复核). **Verdict:** the complete proof chain is accepted as a mathematical audit, subject to the local wording correction in [ERRATUM.md](ERRATUM.md). This is an independent reconstruction and review of an existing theorem, not a new theorem, new polynomial family, priority claim, human peer-review certification, or formal proof-assistant verification.

## Fixed source and scope

The object is Aurantium's manuscript dated **14 October 2026**, specifically [paper/proof.tex at commit 68f4c920606ad239fbc3a8195bc0987b790f5905](https://github.com/Aurantium-47/eventual-infinite-log-concavity/blob/68f4c920606ad239fbc3a8195bc0987b790f5905/paper/proof.tex), §§2–4 and §8. This review does not derive general validity from the separate November 2 sharp-trinomial review. Its precise conclusion is

\[
\forall p(x)=\sum_{i=0}^{d}c_ix^i\ (c_i\in\mathbb R_{>0}),\quad
\exists N(p)\quad\forall n\in\mathbb Z,\ n\ge N(p),\quad
\forall j\ge0\quad\forall k\in\{0,\ldots,nd\}:\quad
(\mathcal L^j\operatorname{coeff}(p^n))_k>0,
\]

where \((\mathcal La)_k=a_k^2-a_{k-1}a_{k+1}\) and coefficients outside the original support remain zero. Iteration indices are nonnegative integers. Degree zero is the positive singleton. There is no uniform threshold over different polynomials, no internal-zero/sparse extension, and no noninteger-power assertion. In particular, this does **not** establish the sharp trinomial assertion for every integer \(n\ge10\).

The proof is analytic plus a finite exact certificate, not an extrapolation from experiments. The local stopping and shrinking-disk framework is prior work attributed in the manuscript to [Xie–Zhang–Zhang, v1, §2](https://arxiv.org/html/2610.12237v1#S2), including its cited antecedents. The conjectural context is [Medina–Straub, v1](https://arxiv.org/abs/1405.1765v1). No third-party paper is redistributed here.

## 1. Local stopping, with the corrected first-failure argument

For positive entries put \(q_j(k)=a^{(j)}_{k-1}a^{(j)}_{k+1}/(a^{(j)}_k)^2\), with \(q_j=0\) at genuine endpoints. Direct algebra gives

\[
q_{j+1}(k)=\frac{q_j(k)^2(1-q_j(k-1))(1-q_j(k+1))}{(1-q_j(k))^2}.
\]

If each center has a finite actual local positive certificate through \(T(k)\), including positive final neighbors and \(q_{T(k)}(k)\le1/3\), all iterates are positive. Indeed, take the earliest nonpositive layer \(r\) and a failed center \(k\). Endpoints only square, and \(T(k)<r\). Positivity of layers 0 through \(r-1\) implies all ratios belong to \([0,1)\) through **layer \(r-2\)**. These are precisely the inputs needed to propagate

\[
q_{j+1}(k)\le q_j(k)^2/(1-q_j(k))^2\le1/4<1/3
\]

to \(q_{r-1}(k)\le1/3\). If \(T(k)=r-1\), no propagation is needed. Then \(a^{(r)}_k>0\), a contradiction. After global positivity is proved, the bound persists. The same least-layer argument works on a half-line without taking an infinite maximum of stopping times. On finite support one may subsequently take the maximum of 0 and their finite times, also covering support with no interior indices.

## 2. Holomorphic amplification through growing depth

Write \(h=-\log q\), \(\Delta f(z)=f(z-1)-2f(z)+f(z+1)\), and
\(g(w)=\operatorname{Log}(1-e^{-w})\). On \(\Re w>0\), \(g\) is holomorphic with \(|\Im g|<\pi/2\), and
\(h_{j+1}=2h_j-\Delta g(h_j)\).
A holomorphic function with this imaginary-part bound on a radius-\(D_0\) disk has Taylor coefficients \(|c_m|\le2/D_0^m\) for \(m\ge1\), by Fourier coefficients of its imaginary part. Hence
\(|\Delta g(h_j)|\le4/(D_0^2-1)\) whenever the needed disk is available. Large negative real logarithms near zero cause no missing term.

Suppose \(\Re h_0\ge\mu\), \(0<\mu\le1\), \(\mu R^2\ge256\). Set
\(K=\lceil\log_2(4/\mu)\rceil\), \(R_j=R(3/4)^j\), and \(\beta=\log_2(4/3)<1/2\). Before using any positivity induction, the smallest successive radius gap satisfies

\[
d_{\min}^2>\frac{R^2}{16}(\mu/4)^{2\beta}
\ge16\mu^{2\beta-1}4^{-2\beta}\ge81/16>4.
\]

The normalized telescoping error is weighted, not a sum of \(K\) equally weighted errors:

\[
|2^{-j}h_j-h_0|\le E_j
=\sum_{i=0}^{j-1}\frac{2^{1-i}}{(R_i-R_j)^2-1}
<\frac8{3R^2}\sum_{r=1}^{j}\frac{(8/9)^{j-r}}{(1-(3/4)^r)^2}
<\frac{56}{R^2}.
\]

For the final bound, the reciprocal factors are bounded by 16, 6, 3, then \(7/3\). The first three sums are at most \(16,182/9,1699/81<21\); subsequently \(S_j\le(8/9)S_{j-1}+7/3<21\). Thus induction gives
\(\Re h_j>(25/32)2^j\mu>0\) and \(h_K(k)>25/8>\log3\).

For actual sequences the invariant is curvature agreement on integer samples within \(R_j\), and positive layer-\(j\) coefficients within \(R_j+1\). The initial data must include the unit-shift margin. Since each radius gap exceeds 2, every coefficient and curvature update stays in the preceding controlled domain, including final neighbors. No artificial endpoint is inserted. This explicitly controls growing \(K\), rather than invoking a fixed-depth limit.
Equivalently, \(R_K=3d_{\min}>27/4\) and \(R_j>2(K-j)+27/4>K+1-j\). Thus the minimal initial coefficient interval \([k-K-1,k+K+1]\) supports positivity on \(|m-k|\le K+1-j\) and curvature agreement on \(|m-k|\le K-j\) at layer \(j\); at \(j=K\) the center and both neighbors remain positive.


## 3. Poisson model: exact finite reconstruction and analytic tail

Let \(u_k=1/k!\) for \(k\ge0\), zero for negative indices. Initially \(q_0(k)=k/(k+1)\). The bundled `verify.py` independently implements the displayed ratio formula using integers with \(D=2^{256}\). Write \(l_k/D\le q(k)\le u_k/D\) (here \(u_k\) denotes an upper integer bound only in the following display). The outward updates are

\[
l'_k=\left\lfloor\frac{l_k^2(D-u_{k-1})(D-u_{k+1})}{D(D-l_k)^2}\right\rfloor,\qquad
u'_k=\left\lceil\frac{u_k^2(D-l_{k-1})(D-l_{k+1})}{D(D-u_k)^2}\right\rceil.
\]

The map is increasing in its center and decreasing in its neighbors on \([0,1)\). Every layer verifies \(0\le l_k\le u_k<D\). Initial bounds are floor/ceiling of \(Dk/(k+1)\) through index 2064. Each step discards the unsupported rightmost ratio; only the genuine left endpoint remains zero. Layer \(j\) retains ratios through \(2064-j\). Positivity of actual coefficients through at least \(2065-j\) follows inductively from these bounds and the infinite positive initial seed.

For every \(1\le k\le2047\), the first strict test \(3u_k<D\) passes by depth 12, with time at most \(\lceil\log_2(8k)\rceil\). The cumulative certified counts at depths 0–12 are exactly:

| depth | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| certified | 0 | 0 | 2 | 6 | 13 | 27 | 56 | 115 | 231 | 464 | 930 | 1862 | 2047 |

All 2047 records (index, first depth, lower, upper, strict gap) and all 13 layer summaries are compared field-for-field to the pinned author's gzip, not merely to this table. Independently, direct coefficient iteration starts with \(64!/k!\), \(0\le k\le64\), discards the artificial right edge each step, and checks positivity and ratio enclosures through eight iterations. At depth \(j=0,\ldots,8\), coefficients end at \(64-j\), so comparable ratios are only \(0,\ldots,63-j\). This gives **540 comparisons: 531 interior and 9 genuine left-endpoint comparisons**, with counts 64 down to 56. The largest direct coefficient has 75,775 bits.

A second AI-assisted independent reconstruction, `crosscheck_fraction.py`, evaluates the normalized map \((c/(1-c))^2(1-l)(1-r)\) with exact `Fraction` arithmetic before outward rounding, rather than reusing the merged integer expression. It compares the entire reference object and the first verifier's records. Its per-certificate dependency-cone check uses ratio indices \([\max(0,k-T+s),k+T-s]\) and coefficient indices \([\max(0,k-T+s-1),k+T-s+1]\) at stage \(s\). The maximum initial coefficient needed by any target certificate is 2060, leaving five positions within the actual coefficient prefix through 2065. The 260,512 cone-node checks count shared nodes repeatedly across certificates; they are not distinct certificates. A rounded lower bound of zero in a deep interval does not contradict strict positivity of the actual coefficients. The 540 direct coefficient comparisons above belong to `verify.py`, not to this second reconstruction.


For \(k\ge2048\), use the holomorphic initial curvature

\[
h_0(z)=\operatorname{Log}(1+1/z)=\int_0^1\frac{dt}{z+t},\qquad |z-k|\le k/2.
\]

Inversion of this disk gives \(\Re(1/(z+t))\ge1/(3k/2+t)\), hence \(\Re h_0\ge1/(3k/2+1)\ge1/(2k)\). With \(R=k/2\), \(\mu=1/(2k)\), we have \(\mu R^2=k/8\ge256\). Section 2 gives a strict certificate by \(K=\lceil\log_2(8k)\rceil\); the unit-shift margin stays positive since \(k/2-1>0\). The finite range 1–2047 and analytic range 2048 onward cover every positive index. The possible depth 14 at 2048 need not match the finite maximum 12. The endpoint squares, and Section 1 now proves positivity for all Poisson iterates.

## 4. Uniform tilted complex interpolation for every fixed positive p

For \(d\ge1\), define
\(\pi_i(\rho)=c_i\rho^i/p(\rho)\), \(m=EX_\rho\), \(v=\operatorname{Var}X_\rho\).
Since \(\rho m'(\rho)=v>0\), each interior \(k\) has a unique tilt with \(nm=k\). Put \(V=nv\) and \(b=\min(k,nd-k)\). The positive continuous ratio \(v/\min(m,d-m)\) tends to 1 at both ends: near zero both numerator and \(m\) equal \((c_1/c_0)\rho+O_p(\rho^2)\); use reversal at infinity. Compactification gives
\(0<c_pb\le V\le C_pb\), with constants depending only on fixed \(p\).
One explicit alternative, checked independently, is
\[
P=p(1),\quad S=\sum_i ic_i,\quad S^*=\sum_i(d-i)c_i,\qquad
c_p=\min\{c_0c_1/(PS),c_dc_{d-1}/(PS^*)\},\quad C_p=d.
\]
For \(\rho\le1\), \(v\ge\pi_0\pi_1\) and \(m\le\rho S/p(\rho)\) give \(v/\min(m,d-m)\ge c_0c_1/(PS)\); reversal gives the other half. The upper bound follows from \(v\le m(d-m)\le d\min(m,d-m)\).


For \(0<\rho\le1\), \(\pi_0\pi_1/v\) has a positive continuous extension at zero with value 1. The reversed polynomial treats \(\rho\ge1\). Taking a common positive lower bound \(a\), the adjacent pair in the modulus-squared identity gives, for \(|t|\le\pi\),

\[
|\phi_\rho(t)|^2\le1-2av(1-\cos t),\qquad
|\phi_\rho(t)|\le e^{-(2a/\pi^2)vt^2},\quad
\phi_\rho(t)=E e^{it(X_\rho-m)}.
\]

This is a full-tilt bound; very small positive coefficients affect constants but do not remove them. Since \(|X_\rho-m|\le d\) and \(E|X_\rho-m|^3\le dv\), one can take \(t_0=1/(4d)\). For \(|t|\le t_0\), writing \(w=\phi_\rho(t)-1\) gives
\(|w+vt^2/2|\le dv|t|^3/6\), \(|w|\le vt^2\le1/16\), and
\(|\operatorname{Log}(1+w)-w|\le|w|^2\le(d/4)v|t|^3\).
Thus \(|\operatorname{Log}\phi_\rho(t)+vt^2/2|\le dv|t|^3\) uniformly in tilt.

Define the entire interpolation and Gaussian

\[
F_{n,k}(z)=\frac{\sqrt V}{2\pi}\int_{-\pi}^{\pi}\phi_\rho(t)^n e^{-i\sqrt Vzt}\,dt,
\qquad G(z)=\frac{e^{-z^2/2}}{\sqrt{2\pi}}.
\]

At each integer \(s\), Fourier orthogonality gives
\(F_{n,k}(s/\sqrt V)=\sqrt V\rho^{k+s}[x^{k+s}]p(x)^n/p(\rho)^n\).
The same tilt is fixed over the entire local interval. In \(u=\sqrt Vt\), the central integrand error is at most
\(d|u|^3e^{-u^2/4}/\sqrt V\) for \(|u|\le t_0\sqrt V\). Outside it (including the truncated Fourier integral's exterior), it is at most
\((2/t_0)|u|e^{-cu^2}/\sqrt V\), where \(c=\min(2a/\pi^2,1/2)>0\).
Multiplying by \(e^{A|u|}\) leaves both bounds integrable for each fixed \(A\). Consequently

\[
\sup_{|z|\le A}|F_{n,k}(z)-G(z)|\le C_{p,A}/\sqrt V
\]

uniformly in \(n,k,\rho\). An explicit selection is
\[
D_p=\sum_{i<j}(j-i)^2c_ic_j,\quad
\alpha_p=\min(c_0c_1,c_{d-1}c_d)/D_p,\quad
\gamma_p=\min(2\alpha_p/\pi^2,1/2),
\]
\[
C_{p,A}=\frac{64d e^{2A^2}+(16d/\gamma_p)e^{A^2/(2\gamma_p)}}{2\pi}.
\]
Indeed, for \(\rho\le1\), \(v\le\rho D_p/p(\rho)^2\), so the adjacent-pair argument uses \(a=\alpha_p\); reversal preserves \(D_p\). Integrate the two kernels using \(A|u|\le u^2/8+2A^2\) and \(A|u|\le\gamma_pu^2/2+A^2/(2\gamma_p)\). This establishes complex-disk control directly; it is not an unsupported extension of a real-axis central limit theorem.

Take fixed \(A=24\). Since \(|G|\ge e^{-288}/\sqrt{2\pi}\) there, choose \(V_p\ge1\) so the relative error is at most \(1/4\). For example, \(C_{\rm rel}=\sqrt{2\pi}e^{288}C_{p,24}\) and \(V_p=\max\{1,(8C_{\rm rel})^2\}\) give the stronger bound \(1/8\). These are new choices of **p-dependent constants within the same existing proof**, not a new theorem; the trinomial-specific numerical coefficient in the manuscript's equation (21) is not inherited by general \(p\). Then \(\eta=\operatorname{Log}(F/G)\) is holomorphic, real on the real diameter, with \(|\eta|<1/2\). Cauchy's radius-3 estimate gives \(|\eta''|\le1/9\) on radius 21. For \(\delta=1/\sqrt V\le1\), the centered-difference integral on radius 20 gives initial physical curvature \(H_0\) satisfying
\(|VH_0-1|\le1/9\).
Here, with \(z=(w-k)/\sqrt V\) and \(f(z)=\log G(z)+\eta(z)\), the physical curvature is \(H_0(w)=2f(z)-f(z-\delta)-f(z+\delta)\); the Gaussian contribution is exactly \(1/V\). The exact sampling identity identifies this with actual initial curvature.
Thus \(\Re H_0\ge8/(9V)>2/(3V)\). Apply Section 2 with
\(R=20\sqrt V\), \(\mu=2/(3V)\), and \(\mu R^2=800/3>256\), obtaining a certificate at growing depth \(\lceil\log_2(6V)\rceil\).

Choose an integer \(B_p>\max(V_p/c_p,1600C_p,2)\). Whenever \(b\ge B_p\), we have \(V\ge V_p\), \(20\sqrt V\le b/2\), and \(20\sqrt V+1<b\). The initial disk and unit shifts therefore lie strictly inside the support. This supplies bulk certificates for **all** such \(n,k\), with no threshold depending on the final iteration count.

## 5. Finite boundary continuity and the single threshold N(p)

For each fixed \(m\ge0\), multinomial expansion gives

\[
b_m(n)=c_0^{-n}\left(\frac{c_0}{nc_1}\right)^m[x^m]p(x)^n\longrightarrow1/m!.
\]

After removing \(c_0^n\), the coefficient is a polynomial in \(n\) of degree \(m\) with leading coefficient \((c_1/c_0)^m/m!\); choosing any term of degree at least two lowers the number of nonconstant factors. No rationality or integrality of coefficients is used.

Fix one boundary center \(k<B_p\) and its finite Poisson certificate time \(T\). Only initial indices in \([k-T-1,k+T+1]\cap\mathbb Z_{\ge0}\) are needed; negative indices remain prescribed zeros. Every required positive-support coefficient through \(T\), and the terminal strict gap
\((a^{(T)}_k)^2-3a^{(T)}_{k-1}a^{(T)}_{k+1}\), is a polynomial in this finite vector. Their finitely many strict inequalities hold at the Poisson limit, so all persist for every sufficiently large integer \(n\). Exterior zeros are not required to become positive. This transfers a finite certificate, not infinitely many iterates by continuity. In particular, the perturbed sequence need not reproduce the same dyadic enclosures or computational path: only the finite strict coefficient inequalities are transferred.

The normalization is positive global/geometric scaling \(b_m=A_nB_n^ma_m\); induction gives
\((\mathcal L^jb)_m=A_n^{2^j}B_n^{m2^j}(\mathcal L^ja)_m\), preserving all signs and ratios. Reverse \(p\) for the right boundary; symmetry is unnecessary.

There are only finitely many left/right centers \(1,\ldots,B_p-1\). Take the maximum of their thresholds and the finitely many support-containment thresholds, obtaining one \(N(p)\). For every integer \(n\ge N(p)\), each interior center has either a boundary or bulk certificate. Original endpoints repeatedly square. Section 1 then gives all iterations simultaneously. This is \(\exists N(p)\,\forall n\ge N(p)\,\forall j\), not \(\forall j\,\exists N(p,j)\). Neither a huge explicit cutoff, a finite exponent baseline, a PF theorem, nor an unproved convolution-closure assertion is a dependency of this general conclusion.

## Reproduction and limits

Run `python -B verify.py` from this directory (or pass its path from any working directory). It uses only Python's standard library, no network, author-code imports, floating-point arithmetic, or large cutoff expansion. It reconstructs the finite component and writes `results.json` and `reconstructed_certificates.json`. `references/poisson_certificates.json.gz` is unchanged author data from the pinned source; [SOURCES.md](SOURCES.md) records provenance and hashes. The analytic arguments above are mathematical review, not machine-checked by this finite verifier. File integrity is recorded in `SHA256SUMS`.
