# Mathematical scope

For a sequence with zero extension, (L a)_k=a_k^2-a_(k-1)a_(k+1). Infinite log-concavity requires every iterate to be entrywise nonnegative. The new theorems assert strict positivity on the original positive support, while exterior zeros remain zero.

## Main result B

For every fixed polynomial p(x)=sum_(i=0)^d c_i x^i with all c_i real and strictly positive, there exists N(p) such that, for every integer n>=N(p), every iterate L^j of the coefficient sequence of p(x)^n is strictly positive on indices 0..nd, for every j>=0. The degree-zero case is included. N(p) may depend on the entire polynomial, but not on a subsequently specified j.

This is the integer-power formulation of Medina–Straub Conjecture 5.2. It makes no statement about generalized noninteger powers, internal coefficient gaps, arbitrary coefficient signs or a threshold uniform over all p.

## Trinomial result A

For T(n,k)=[x^k](1+x+x^2)^n, define B=2^20001, M=B+20005 and H=2^(M+1) M!. The explicit cutoff

    N0 = 2 H^(2^20005)

suffices for all integer n>=N0 and all iterations. The simpler larger bound 2^(2^40100) also suffices. The whole row reaches the 3-factor cone by ceil(log2(8n)) and stays there. These bounds are proved symbolically, not evaluated or exhaustively tested.

## Trinomial curvature result C

Let b=min(k,2n-k), and use the exponentially tilted variance V specified in the paper, with reflection on the right half. As b tends to infinity, uniformly in allowed n,k,

    sup_(0<=j<=ceil(log2(6V))) |V 2^(-j) h_j(k)-1| -> 0.

The curvatures refer to positive local coefficient iterates on the required dependency intervals. The stated cone-entry inequalities follow without assuming monotonicity in j or distant global positivity. At the center, the local entry time is log2(n)+O(1).

## Unresolved sharper statement

The claim for **every integer n>=10** in Medina–Straub Example 5.3 is not proved or disproved here. The cofinite theorem and the separately supplied finite-exponent certificates leave a finite but unexhausted set below N0. Neither finiteness of that set nor taking another convolution proves that no exceptions remain.
