# Finite certificates and the first three iterates

Let p(x)=1+x+x² and a_k=[x^k]p(x)^n, with zero extension. All arithmetic certificates below use integers and directed rational enclosures.

## 1. Exact ratio verification for 10≤n≤4003
The coefficient identity p(x)(p(x)^n)'=n p'(x)p(x)^n gives
(k+1)a_(k+1)=(n−k)a_k+(2n−k+1)a_(k−1).
The coefficients are positive on 0≤k≤2n and symmetric. On the first half define r_k=a_k/a_(k−1). Then r_1=n and
r_(k+1)=[n−k+(2n−k+1)/r_k]/(k+1), 1≤k<n.
This expression decreases with r_k. If S=2^256 and R_k^-≤S r_k≤R_k^+, directed integer divisions give
R_(k+1)^-=floor(((n−k)S R_k^+ +(2n−k+1)S²)/((k+1)R_k^+)),
R_(k+1)^+=ceil(((n−k)S R_k^- +(2n−k+1)S²)/((k+1)R_k^-)).
All denominators are positive, as checked by the certificate program.

For q_k=a_(k−1)a_(k+1)/a_k², the initial half-row enclosures are
Q_k^-=floor(S R_(k+1)^-/R_k^+), Q_k^+=ceil(S R_(k+1)^+/R_k^-), 1≤k<n;
Q_n^-=floor(S³/(R_n^+)²), Q_n^+=ceil(S³/(R_n^-)²),
and Q_0^-=Q_0^+=0. Symmetry gives the remaining indices. The powers of S in the central formula are essential.

Whenever 0≤q_k<1, the next iterate is positive on its support and its ratios obey
q'_k=q_k²(1−q_(k−1))(1−q_(k+1))/(1−q_k)².
The map increases in its own argument and decreases in either neighboring argument. Given integer enclosures 0≤Q^-≤S q≤Q^+<S, lower and upper bounds for S q'_k are therefore
floor((Q_k^-)²(S−Q_(k−1)^+)(S−Q_(k+1)^+)/[S(S−Q_k^-)²]),
ceil((Q_k^+)²(S−Q_(k−1)^-)(S−Q_(k+1)^-)/[S(S−Q_k^+)²]).
At the center of the symmetric half-array the right neighbor equals the left neighbor. No unbounded integer is replaced by floating-point arithmetic.

The exact program checks every integer n=10,...,4003. At each step it verifies the strict upper bound Q_k^+<S, and it terminates only when 3Q_k^+≤S for every k. All 3994 cases terminate by depth 12. A separate verifier using exact coefficient rows instead of the successive-ratio initializer gives the same successful coverage. The terminal condition is sufficient because q≤1/3 implies
q'≤(1/3)²/(1−1/3)²=1/4<1/3.
Induction proves positivity of all later iterates, so a finite exact certificate per exponent establishes infinite log-concavity rather than merely a bounded number of successful iterations.

## 2. Finite certificates for the full PF4 property
For a zero-extended finite sequence a, let T(a)_(i,j)=a_(j−i), i,j≥0. PF4 means every minor of order at most four is nonnegative.

Suppose A(x)=Σ_(k=0)^d a_k x^k=∏_(h=1)^d(1+z_h x), so a_k=e_k(z). It suffices to test the finite determinants
 det(a_(u_i−i+j))_(1≤i,j≤4)
for every d≥u_1≥u_2≥u_3≥u_4≥0. Here the z_h may be complex; the tests concern real evaluated determinants.

Indeed dual Jacobi–Trudi identifies these determinants with ordinary Schur functions s_λ(z) for λ'=u, namely all shapes of width≤4 and height≤d; zero padding includes smaller widths. Consider an arbitrary order-ℓ≤4 Toeplitz minor with increasing rows r_i and columns c_i. If c_i<r_i for some i, the first i columns can meet at most i−1 eligible rows, so every determinant term vanishes. Otherwise put
λ'_i=c_(ℓ+1−i)+i, μ'_i=r_(ℓ+1−i)+i.
These are partitions with λ'≥μ'. Transposition and simultaneous reversal transform the minor into det(e_(λ'_i−μ'_j−i+j))=s_(λ/μ)(z). The Littlewood–Richardson expansion
s_(λ/μ)=Σ_ν c_(μν)^λ s_ν
has nonnegative integer coefficients. For nonzero terms ν⊆λ, hence width(ν)≤ℓ≤4. If height(ν)>d its specialization to d variables vanishes. Every remaining ordinary Schur value is among the finite tests. Thus every arbitrary Toeplitz minor is nonnegative.

For p(x)^n use d=2n and n copies each of exp(iπ/3) and exp(−iπ/3). The exact tests at n=8 and n=9 enumerate respectively C(20,4)=4845 and C(22,4)=7315 determinants. Every determinant is positive; the minimum is 1. These are finite certificates for the complete infinite-matrix PF4 condition, not merely a sample of consecutive-row minors.

## 3. Convolution closure and nonnegative early iterates
T(a*b)=T(a)T(b). Each fixed minor of the product has a finite Cauchy–Binet sum: contributing intermediate indices lie between the selected row and column indices. If both factors are PF4, every summand is nonnegative. Thus convolution preserves PF4.

For n≥56 write n=8q+r, 0≤r≤7. Since q≥7≥r,
n=8(q−r)+9r.
Hence p^n is a convolution of the two certified PF4 seed rows, and is PF4.

Let D_j(k)=det(a_(k+s−t))_(0≤s,t<j), D_0=1. Desnanot–Jacobi gives
D_j(k)²−D_j(k−1)D_j(k+1)=D_(j−1)(k)D_(j+1)(k).
It follows algebraically that
(La)_k=D_2(k),
(L²a)_k=a_k D_3(k),
(L³a)_k=D_2(k)[a_k² D_4(k)+D_3(k−1)D_3(k+1)].
These are polynomial identities with no division by a minor, so endpoints and possible zero minors cause no exception. PF4 therefore implies nonnegativity of layers zero through three. The selected infinite range n≥4004 lies entirely within this proven range n≥56.

## References
The symmetric-function identities are dual Jacobi–Trudi and Littlewood–Richardson; see I. G. Macdonald, *Symmetric Functions and Hall Polynomials*, second edition, Chapter I §§3,5,9. The first three iteration identities and fourth-order limitations are discussed by P. R. W. McNamara and B. E. Sagan, *Infinite log-concavity: developments and conjectures*, https://arxiv.org/abs/0808.1065. These general algebraic tools are prior results, not new claims of this proof.
