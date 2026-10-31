# Finite certificates and the first three iterates

Let $p(x)=1+x+x^2$ and $a_k=[x^k]p(x)^n$, with zero extension. All arithmetic certificates below use integers and directed rational enclosures.

## 1. Exact ratio verification for $10\le n\le4003$

The coefficient identity $p(x)(p(x)^n)'=np'(x)p(x)^n$ gives
\[
(k+1)a_{k+1}=(n-k)a_k+(2n-k+1)a_{k-1}.
\]
The coefficients are positive on $0\le k\le2n$ and symmetric. On the first half define $r_k=a_k/a_{k-1}$. Then $r_1=n$ and
\[
r_{k+1}=\frac{n-k+(2n-k+1)/r_k}{k+1},\qquad 1\le k<n.
\]
This expression decreases with $r_k$. If $S=2^{256}$ and $R_k^-\le Sr_k\le R_k^+$, directed integer divisions give
\[
\begin{aligned}
R_{k+1}^-&=\left\lfloor\frac{(n-k)SR_k^++(2n-k+1)S^2}{(k+1)R_k^+}\right\rfloor,\\
R_{k+1}^+&=\left\lceil\frac{(n-k)SR_k^-+(2n-k+1)S^2}{(k+1)R_k^-}\right\rceil.
\end{aligned}
\]
All denominators are positive, as checked by the certificate program.

For $q_k=a_{k-1}a_{k+1}/a_k^2$, the initial half-row enclosures are
\[
\begin{aligned}
Q_k^-&=\left\lfloor\frac{SR_{k+1}^-}{R_k^+}\right\rfloor,&
Q_k^+&=\left\lceil\frac{SR_{k+1}^+}{R_k^-}\right\rceil,
&&1\le k<n,\\
Q_n^-&=\left\lfloor\frac{S^3}{(R_n^+)^2}\right\rfloor,&
Q_n^+&=\left\lceil\frac{S^3}{(R_n^-)^2}\right\rceil,
\end{aligned}
\]
and $Q_0^-=Q_0^+=0$. Symmetry gives the remaining indices. The powers of $S$ in the central formula are essential.

Whenever $0\le q_k<1$, the next iterate is positive on its support and its ratios obey
\[
q'_k=\frac{q_k^2(1-q_{k-1})(1-q_{k+1})}{(1-q_k)^2}.
\]
The map increases in its own argument and decreases in either neighboring argument. Given integer enclosures $0\le Q^-\le Sq\le Q^+<S$, lower and upper bounds for $Sq'_k$ are therefore
\[
\left\lfloor\frac{(Q_k^-)^2(S-Q_{k-1}^+)(S-Q_{k+1}^+)}{S(S-Q_k^-)^2}\right\rfloor,
\qquad
\left\lceil\frac{(Q_k^+)^2(S-Q_{k-1}^-)(S-Q_{k+1}^-)}{S(S-Q_k^+)^2}\right\rceil.
\]
At the center of the symmetric half-array the right neighbor equals the left neighbor. No unbounded integer is replaced by floating-point arithmetic.

The exact program checks every integer $n=10,\ldots,4003$. At each step it verifies the strict upper bound $Q_k^+<S$, and it terminates only when $3Q_k^+\le S$ for every $k$. All 3994 cases terminate by depth 12. A separate verifier using exact coefficient rows instead of the successive-ratio initializer gives the same successful coverage. The terminal condition is sufficient because $q\le1/3$ implies
\[
q'\le\frac{(1/3)^2}{(1-1/3)^2}=\frac14<\frac13.
\]
Induction proves positivity of all later iterates, so a finite exact certificate per exponent establishes infinite log-concavity rather than merely a bounded number of successful iterations.

## 2. Finite certificates for the full $\mathrm{PF}_4$ property

For a zero-extended finite sequence $a$, let $T(a)_{i,j}=a_{j-i}$, $i,j\ge0$. The property $\mathrm{PF}_4$ means every minor of order at most four is nonnegative.

Suppose
\[
A(x)=\sum_{k=0}^d a_kx^k=\prod_{h=1}^d(1+z_hx),
\]
so $a_k=e_k(z)$. It suffices to test the finite determinants
\[
\det(a_{u_i-i+j})_{1\le i,j\le4}
\]
for every $d\ge u_1\ge u_2\ge u_3\ge u_4\ge0$. Here the $z_h$ may be complex; the tests concern real evaluated determinants.

Indeed dual Jacobi--Trudi identifies these determinants with ordinary Schur functions $s_\lambda(z)$ for $\lambda'=u$, namely all shapes of width at most four and height at most $d$; zero padding includes smaller widths. Consider an arbitrary order-$\ell\le4$ Toeplitz minor with increasing rows $r_i$ and columns $c_i$. If $c_i<r_i$ for some $i$, the first $i$ columns can meet at most $i-1$ eligible rows, so every determinant term vanishes. Otherwise put
\[
\lambda'_i=c_{\ell+1-i}+i,\qquad \mu'_i=r_{\ell+1-i}+i.
\]
These are partitions with $\lambda'\ge\mu'$. Transposition and simultaneous reversal transform the minor into
\[
\det(e_{\lambda'_i-\mu'_j-i+j})=s_{\lambda/\mu}(z).
\]
The Littlewood--Richardson expansion
\[
s_{\lambda/\mu}=\sum_\nu c_{\mu\nu}^{\lambda}s_\nu
\]
has nonnegative integer coefficients. For nonzero terms $\nu\subseteq\lambda$, hence $\operatorname{width}(\nu)\le\ell\le4$. If $\operatorname{height}(\nu)>d$, its specialization to $d$ variables vanishes. Every remaining ordinary Schur value is among the finite tests. Thus every arbitrary Toeplitz minor is nonnegative.

For $p(x)^n$ use $d=2n$ and $n$ copies each of $\exp(i\pi/3)$ and $\exp(-i\pi/3)$. The exact tests at $n=8$ and $n=9$ enumerate respectively $\binom{20}{4}=4845$ and $\binom{22}{4}=7315$ determinants. Every determinant is positive; the minimum is 1. These are finite certificates for the complete infinite-matrix $\mathrm{PF}_4$ condition, not merely a sample of consecutive-row minors.

## 3. Convolution closure and nonnegative early iterates

We have $T(a*b)=T(a)T(b)$. Each fixed minor of the product has a finite Cauchy--Binet sum: contributing intermediate indices lie between the selected row and column indices. If both factors are $\mathrm{PF}_4$, every summand is nonnegative. Thus convolution preserves $\mathrm{PF}_4$.

For $n\ge56$ write $n=8q+r$, $0\le r\le7$. Since $q\ge7\ge r$,
\[
n=8(q-r)+9r.
\]
Hence $p^n$ is a convolution of the two certified $\mathrm{PF}_4$ seed rows, and is $\mathrm{PF}_4$.

Let $D_j(k)=\det(a_{k+s-t})_{0\le s,t<j}$, $D_0=1$. Desnanot--Jacobi gives
\[
D_j(k)^2-D_j(k-1)D_j(k+1)=D_{j-1}(k)D_{j+1}(k).
\]
It follows algebraically that
\[
\begin{aligned}
(\mathcal La)_k&=D_2(k),\\
(\mathcal L^2a)_k&=a_kD_3(k),\\
(\mathcal L^3a)_k&=D_2(k)\bigl[a_k^2D_4(k)+D_3(k-1)D_3(k+1)\bigr].
\end{aligned}
\]
These are polynomial identities with no division by a minor, so endpoints and possible zero minors cause no exception. The property $\mathrm{PF}_4$ therefore implies nonnegativity of layers zero through three. The selected infinite range $n\ge4004$ lies entirely within this proven range $n\ge56$.

## References

The symmetric-function identities are dual Jacobi--Trudi and Littlewood--Richardson; see I. G. Macdonald, *Symmetric Functions and Hall Polynomials*, second edition, Chapter I, Sections 3, 5 and 9. The first three iteration identities and fourth-order limitations are discussed by P. R. W. McNamara and B. E. Sagan, *Infinite log-concavity: developments and conjectures*, <https://arxiv.org/abs/0808.1065>. These general algebraic tools are prior results, not new claims of this proof.
