# Eventual infinite log-concavity of positive polynomial powers

Aurantium · version 0.1.0 · 14 October 2026

[Complete English paper](paper/proof.pdf) · [Standalone LaTeX source](paper/proof.tex)

For each fixed polynomial p(x)=sum(c_i x^i) with real c_i>0 at every degree from 0 through d, the main result gives a threshold N(p) such that every **integer** power p(x)^n with n>=N(p) has all log-concavity iterates strictly positive on its original support. The threshold depends on p and is independent of the subsequent iteration count. Prescribed zeros outside the support remain zero.

The paper also contains an explicit cofinite theorem for trinomial powers and a uniform bulk-curvature estimate through growing iteration depth. It does **not** establish the sharper assertion for every trinomial exponent n>=10, and it does not extend to noninteger powers or polynomials with internal zero coefficients. Precise statements appear in [SCOPE.md](SCOPE.md).

The complete proofs and formulas are included, with the general positive-polynomial theorem highlighted in the introduction. The original shrinking-disk and local stopping machinery is credited to Xie, Zhang and Zhang and its cited antecedents; the conjectural context is credited to Medina and Straub. The paper does not claim these methods as newly invented. See [REFERENCES.md](REFERENCES.md).

## Exact data and reproduction

Python 3.10 or later, standard library only:

```sh
python -B code/verify.py
```

This minimal entry regenerates the 2047 strict Poisson certificates, 540 direct integer/interval comparisons, polynomial structural checks and rational constants. Assertions must remain enabled. The separate legacy baseline is included for the finite-exponent comparison and is not a dependency of the proofs of the main results.

[REPRODUCIBILITY.md](REPRODUCIBILITY.md) distinguishes recorded local exact checks, externally recorded computations, and what was not rerun during manuscript preparation. The packaged default entry was executed successfully with Python 3.12.10 on 14 October 2026: all 2047 strict Poisson certificates, 540 direct comparisons, polynomial checks and constant bounds passed. The release-entry run took 0.328 seconds with peak child working set 19,853,312 bytes; all 24 checked input files remained unchanged. No huge cutoff, all-exponent range or noninteger-power claim is certified by a finite numerical scan.

This work was prepared with AI assistance. No global-priority determination, independent human certification or formal proof-assistant verification is claimed. Third-party papers are referenced rather than redistributed. The exact release file list and hashes are in WHITELIST.txt and MANIFEST.json; attribution and distribution scope are in [RIGHTS.md](RIGHTS.md).
