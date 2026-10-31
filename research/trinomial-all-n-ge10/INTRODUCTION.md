---
title: "Infinite log-concavity of trinomial powers"
subtitle: "A proposed computer-assisted proof of the all-exponent trinomial assertion"
date: "31 October 2026"
---

# Abstract

Let $a_{n,k}=[x^k](1+x+x^2)^n$, extended by zero outside its support, and define $(\mathcal La)_k=a_k^2-a_{k-1}a_{k+1}$. We give a computer-assisted proof that $\mathcal L^r a_n$ is entrywise nonnegative for every integer $n\ge10$ and every integer $r\ge0$. The proof joins an exact invariant-cone verification for $10\le n\le4003$ with a uniform analytic and algebraic argument for $n\ge4004$. In the latter range, a sixteen-variable integral and explicit saddle estimates supply bulk signs for the fourth iterate; exact moving-node certificates supply the remaining edge signs. Palindromicity and a degree count then prove negative real-rootedness of the fourth iterate. Separate Toeplitz-minor arguments establish the earlier layers, and a real-rootedness preservation theorem gives every later layer.

The numerical components use exact integers and rational enclosures. The claimed quantifiers are not inferred from a finite sample of exponents. This draft has undergone independent internal checks, including separately implemented arithmetic checks; it has not undergone external peer review or proof-assistant formalization. No assertion of exhaustive literature priority is made.

# The target and the proof architecture

**Theorem.** For every integer $n\ge10$, every integer $r\ge0$, and every integer $k$,
\[
 (\mathcal L^r a_n)_k\ge0,
 \qquad a_{n,k}=[x^k](1+x+x^2)^n.
\]
All sequences and iterates use zero extension beyond their natural finite support.

This is the specific trinomial assertion discussed in Example 5.3 of Medina and Straub, *On multiple and infinite log-concavity*, arXiv:1405.1765v1, printed page 11; the published article appears in *Annals of Combinatorics* **20** (2016), 125–138. The original work verified a finite range $10\le n\le500$. The present theorem does not assert the more general polynomial conjecture considered elsewhere in that paper.

The proof has four logically separate components:

1. **Finite exponents.** Every $10\le n\le4003$ reaches a sufficient invariant cone under exact directed ratio arithmetic. The cone proves all subsequent iterations at once.
2. **Earlier layers in the infinite range.** Finite certificates at exponents eight and nine imply the full $\mathrm{PF}_4$ property through symmetric-function identities. Convolution closure and determinant identities then prove nonnegativity through the third iterate for every $n\ge56$.
3. **Fourth-iterate roots.** Uniform bulk estimates and exact certificates on the continuous parameter interval $0\le u\le1/4004$ provide enough alternating real signs to locate all $2n$ zeros of the fourth iterate on the negative real axis for every integer $n\ge4004$.
4. **Later layers.** Brändén's preservation theorem applies to the fourth iterate and thereafter. It is not used backwards to infer positivity of the earlier layers.

The finite and infinite exponent ranges are complementary and leave no gap. The roles of the continuous parameter family and the finite polynomial at reciprocal integers are kept distinct throughout.

# Verification conventions

A rational enclosure is a proved inclusion, not a floating-point approximation. Every strict sign assertion subtracts all applicable rounding and analytic remainder bounds before it is accepted. The exact arithmetic backend is credited and pinned in the reproducibility package. A fast replay of saved enclosures and a full regeneration from the input formulas have different trust boundaries; the package documents both rather than conflating them.

The mathematical statements below are accompanied by portable verification commands and explicit certificate coverage. Raw development logs and internal review narratives are not part of the mathematical exposition.
