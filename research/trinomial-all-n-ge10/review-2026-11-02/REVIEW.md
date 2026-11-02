# Fixed-version theorem review — 2 November 2026

**Assessment: accepted by an AI-assisted internal mathematical and computational review.** The assessed source is commit [`68f4c920606ad239fbc3a8195bc0987b790f5905`](https://github.com/Aurantium-47/eventual-infinite-log-concavity/tree/68f4c920606ad239fbc3a8195bc0987b790f5905/research/trinomial-all-n-ge10). This public summary does not replace the manuscript or its exact certificates. It is not human peer review, proof-assistant formalization, a publication decision, or a priority determination.

## Exact result

Let `a^(n)_k = [x^k](1+x+x²)^n`, extended by zero outside `0 ≤ k ≤ 2n`, and `(La)_k = a_k² − a_(k−1)a_(k+1)`. The reviewed computer-assisted proof establishes

> For every integer `n ≥ 10`, every integer `j ≥ 0`, and every integer `k`, `(L^j a^(n))_k ≥ 0`.

It also establishes that for **every integer `n ≥ 4004`**, the polynomial `f_(n,4)(x) = Σ_k (L⁴a^(n))_k x^k` has exactly `2n` distinct strictly negative real roots. The latter statement is not asserted for the finite range `10 ≤ n ≤ 4003`, or for noninteger exponents.

This is the specific trinomial assertion in Medina–Straub, [Example 5.3 and Table 1](https://arxiv.org/abs/1405.1765v1), not the general positive-polynomial Conjecture 5.2. No claim of first proof or methodological priority follows from this correctness assessment.

## Accepted analytic interface

Write `p(z)=1+z+z²`, `v(z)=z(1+4z+z²)/p(z)²`, `θ=π/16`, `ζ=s exp(iθ)`, and

`A_ν(s) = [2048 / (4(2π)^(15/2))] p(ζ)^(16ν) / (νv(ζ))^(45/2)`,

with the manuscript's continuous branches. The accepted uniform estimate is

`|f_(ν,4)(−s^16) − 2 Re A_ν(s)| / (2|A_ν(s)|) < 18717720003/20000000000 < 47/50`.

Its integer domain is `ν=n>0`, `0<s≤1`, `nv(s)≥250`. The real-parameter analytic-coefficient extension requires `ν>0`, **`0<s<1`**, `νv(s)≥250`, and the logarithm of `p` normalized at zero. It makes no noninteger polynomial-degree or reciprocal-root assertion.

The phase `Ψ_n(s)=16n arg p(se^(iθ))−(45/2)arg v(se^(iθ))` is strictly increasing for `n≥3`, with endpoint limits `−45π/32` and `nπ`. For integers `n≥1001`, the phase points `Ψ_n(s_(n,m))=mπ`, `250≤m≤n`, lie in the variance domain and have strict signs `(-1)^m f_(n,4)(−s_(n,m)^16)>0`. In particular, `s_(n,n)=1` and `−1` is not a root.

## What closes the boundary dependency

At `u=1/n`, the compactified coefficient family is generated from `g_u(z)=(1+uz+u²z²)^(1/u)`, with `g_0(z)=exp(z)`. Its initial coefficients satisfy

`(k+1)b_(0,k+1)=(1−ku)b_(0,k)+u(2−(k−1)u)b_(0,k−1)`.

Four zero-extended `L` operations define the target `F_u`. The reviewed generator obtains these coefficients from this recurrence; saved jets are comparison targets, not initial data. Coefficientwise outward interval arithmetic is justified by an invariant `2^(e−P)[m_i−ρ,m_i+ρ]`. Bernstein controls bound the midpoint polynomial on an **entire closed panel**; the coefficient radius, complex-parameter Taylor tail, and real-parameter coefficient tail are separately added. A pointwise sample is not substituted for this enclosure argument.

The frozen grid consists of nine endpoints `u_l=l/32032`, `l=0,…,8`. Exactly 1,929 distinct Taylor pairs and 63 disjoint bulk-bypass pairs partition all `8×249` panel/node pairs. The node functions are positive and strictly ordered by reciprocal interpolation. The bypasses use the real-parameter analytic interface above, including a quantitative strictly positive limit at `u=0`; see [clarifications](CLARIFICATIONS.md).

The literal unmodified `regenerate.py --full --backend flint` completed: each saved `m/rad/e/p` field matched and every required strict sign passed. Its eight panel counts were `246,245,243,241,240,239,238,237`; its recorded elapsed time was `29m39.084s`, exit 0. The terminal log's SHA256 is `f552e314b4acda4e9e8566ec9b00e4abc928c94e0c2701bfa7ad42dd39c946a8`. The final theorem review inspected the execution evidence; it did **not** run this entire computation again.

The selected alternate multinomial implementation checked **708 distinct coefficients**, not all 1,929 cases. A third, logarithmic-series implementation independently checked all 87 retained coefficients and both tails for panel 7/node 22. Both alternate implementations share FLINT arithmetic with the principal generator. They improve diagnostic independence but are not full independent implementations of the theorem.

## From boundary signs to all fourth-layer roots

The eight join bounds and phase monotonicity imply `t_249(1/n)<n s_(n,250)`. For integer `n≥4004`, put

`x_0=0`, `x_j=−(t_j(1/n)/n)^16` for `1≤j≤249`, and `y_m=−s_(n,m)^16` for `250≤m≤n`.

Then

`0=x_0>x_1>…>x_249>y_250>…>y_n=−1`.

The values alternate strictly in sign, starting with `f_(n,4)(0)=1`. There are 249 disjoint boundary root intervals, one joining interval, and `n−250` bulk intervals: exactly **n distinct roots in (−1,0)**. Endpoints are nonzero. Closed-panel certificates include the threshold `n=4004`.

The original row is palindromic of degree `2n`, with endpoints 1. The zero-extended `L` map preserves palindrome symmetry and those endpoints regardless of signs of intermediate coefficients. Thus the fourth-layer polynomial has degree exactly `2n` and obeys `f(x)=x^(2n)f(1/x)`. Its n roots in `(−1,0)` yield n distinct reciprocal roots below `−1`. These exhaust the degree, proving all roots are negative and simple. Fourth-layer coefficient positivity is a **consequence**, not an assumption, of this argument; there is no circular use of positivity.

## From finite checks and fourth-layer roots to every iteration

For `10≤n≤4003`, the complete finite computation verifies strict positivity until the ratios `q_k=a_(k−1)a_(k+1)/a_k²` enter `0≤q_k≤1/3` (with endpoint ratios zero). The identity

`q'_k=q_k²(1−q_(k−1))(1−q_(k+1))/(1−q_k)²`

then gives `0≤q'_k≤1/4<1/3`; the region is invariant forever. Thus finite entry depths, at most 12, imply **all future iterations**, not merely 12 iterations. A separate earlier 160-bit directed-interval full-row run covered all 3,994 exponents. The final dependency review verified its source and complete result identities rather than rerunning the full range.

For the large-n branch, the finite Schur criteria for `p^8` and `p^9` comprise `4,845+7,315=12,160` determinants. The review recomputed them by rational Gaussian elimination. Dual/skew Jacobi–Trudi and nonnegative Littlewood–Richardson coefficients reduce every Toeplitz minor of order at most four to these criteria; convolution via Cauchy–Binet gives PF4 for every `n≥56`, since `n=8(q−r)+9r` when `n=8q+r`, `0≤r≤7`.

Writing `D_j(k)=det(a_(k+s−t))_(0≤s,t<j)`, Desnanot–Jacobi yields the division-free identities

- `La=D_2`;
- `(L²a)_k=a_k D_3(k)`;
- `(L³a)_k=D_2(k)[a_k²D_4(k)+D_3(k−1)D_3(k+1)]`.

They remain valid at zero coefficients and support boundaries. PF4 therefore supplies layers 0–3. The fourth layer has positive coefficients and strictly negative real roots by the preceding root argument. [Brändén's preservation theorem](https://arxiv.org/abs/0909.1927v3), proved in §3, applies **forward from layer 4**, giving every subsequent layer. It is not applied to the original non-real-rooted trinomial power and is not used to infer earlier layers.

## Trust and credit

The mathematical and code reviews were AI-assisted, including separate computational cross-checks. The trust base includes the reviewed programs, Python exact arithmetic, FLINT, ordinary runtime correctness, and integrity of the recorded executions. File hashes identify bytes; they neither prove mathematics nor provide cryptographic process attestation. No human-refereeing or formal-verification claim is made.

The classical ingredients are credited to Medina–Straub for the target assertion, Brändén for real-root preservation, and the standard Jacobi–Trudi/Littlewood–Richardson, Cauchy–Binet, and Desnanot–Jacobi results. For the symmetric-function identities see Macdonald, *Symmetric Functions and Hall Polynomials*, second edition, Chapter I, equations (3.5), (5.5), (9.1), pp. 41, 71, 142. These tools are not claimed as new contributions.

## Public independent-review artifacts

[Selected independent scripts, full finite results, source mapping, and reproduction instructions](independent_review/README.md) accompany this summary. They distinguish byte-identical historical evidence from the portable assembly entry point.
