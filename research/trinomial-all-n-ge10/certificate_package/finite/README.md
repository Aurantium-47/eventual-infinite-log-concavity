# Finite exponents and PF4 seeds

Requirements: Python 3 standard library; assertions must be enabled (do not use `-O`). No network or third-party library is required.

From this directory:

```sh
python verify_pf4.py
python verify_finite.py --output toy_result.json
python verify_finite.py --full --output finite_result.json
```

The first command computes all 12,160 seed determinants exactly. The second runs small exact oracle comparisons. The third recomputes every exponent 10 through 4003, using directed successive-ratio initialization and a symmetry-reduced ratio iteration until the invariant cone is reached. It checks the complete ordered range and matches a canonical digest of all exact stage certificates. The recorded full verification required approximately six minutes on one cloud CPU; hardware and load change runtime.

The complete mathematical reduction is in `FINITE_AND_ALGEBRAIC_PROOF_TYPESET.md` in the research draft. The seed output alone does not assert infinite log-concavity, and the finite range alone does not imply the all-exponent theorem. They are joined with the separately verified infinite-range proof.
