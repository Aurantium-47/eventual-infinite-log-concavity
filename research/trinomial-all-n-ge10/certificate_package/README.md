# Trinomial infinite-log-concavity verification package

This is a review copy accompanying the proposed computer-assisted proof that every integer power `(1+x+x^2)^n`, `n >= 10`, has an infinitely log-concave coefficient sequence under the zero-extended operator `L(a)_k = a_k^2 - a_(k-1)*a_(k+1)`.

The package is not a proof-assistant formalization. Mathematical arguments in the accompanying manuscript remain essential: integral identities, complex-analytic estimates, geometric decomposition, finite-to-infinite Toeplitz positivity, root counting and the preservation theorem are not replaced by a list of program exits.

## Environment

Use Python 3.11 or newer with assertions enabled; do not use `python -O`. Python 3.12.14 was used for the portable arithmetic checks. The finite verifier and saved-edge replay use only the standard library. Exact analytic polynomial checks require SymPy 1.14.0. Fast full edge regeneration uses the released python-flint 0.9.0 exact integer polynomial backend; an exact standard-library backend is also available, but slower.

For optional dependencies, an isolated environment may be prepared with:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Package verification itself performs no network access or external publication. Installing dependencies is a separate, explicit environment-preparation step.

## Verification levels and commands

Run the following from this directory.

### Finite exponents and earlier layers

```sh
python finite/verify_pf4.py
python finite/verify_finite.py --output finite_toy_result.json
python finite/verify_finite.py --full --output finite_result.json
```

The seed checker computes all 12,160 required determinants. The full finite command recomputes all 3,994 exponents `10..4003` with directed ratio bounds until the invariant cone is reached. It checks the ordered coverage and an exact canonical result digest. The complete recorded finite replay took about six minutes on one cloud CPU; runtime is hardware-dependent.

### Analytic arithmetic prerequisites

```sh
python analytic/run_analytic.py --full
```

This reconstructs cumulant polynomial certificates, weighted Gaussian moments, the local remainder budget, complement estimates, phase identities, ordering and join inequalities. It includes potentially expensive exact reconstruction rather than merely checking saved hashes. `ANALYTIC_VERIFICATION_MAP.md` in the accompanying draft specifies the stage-by-stage mathematical interface. All 15 portable analytic stages were subsequently rerun successfully with exit status 0; the exact code/input hashes and results are recorded in `../validation/portable_analytic.json`. The original manuscript retains its earlier validation-history wording; the public draft README records this later validation addendum.

### Saved edge inequalities: fast, conditional on saved enclosures

```sh
python edge/replay_saved_inequalities.py
```

This rechecks all 1,929 strict jet inequalities, the 63 bulk-bypass boxes, ordering and the final join. It authenticates and processes the eight compressed panel files, recomputes exact Bernstein bounds, and subtracts all rounding and analytic error budgets. **It does not regenerate the interval enclosures themselves.** Its output makes that exclusion explicit.

### Reconstructing enclosure provenance

```sh
python edge/regenerate.py --panel 0 --node 200
python edge/regenerate.py --full
```

The first command is a representative bounded regeneration. The second reconstructs every enclosure from the coefficient recurrence and interval operations, comparing all deterministic midpoint, radius and exponent data. It does not compare runtime, machine paths or gzip timestamps. Combining full regeneration, saved-inequality replay, the analytic checks and the finite checks supplies the computational premises of the manuscript. The original full generating program was run successfully; the portable full-chain command is provided for reproduction and is not represented as having already been rerun in its entirety.

## Exact coverage and mathematical conclusion

- Finite certificates cover every integer `10 <= n <= 4003`.
- The eight edge panels cover `[0, 8/32032] = [0, 1/4004]`, hence every reciprocal integer `u=1/n` with `n >= 4004`.
- Every panel contains all 249 required moving-node signs: 1,992 obligations in total, comprising 1,929 jet certificates and 63 analytically justified bypasses.
- The edge signs join the uniform bulk signs. Palindromicity and degree give all negative real roots for the fourth iterate in the infinite range.
- The separate PF4 argument supplies layers zero through three. Brändén's theorem supplies later layers.

No finite sampling of large exponents is used to infer the universal quantifier. The statement is specific to the trinomial target; it does not resolve the general positive-polynomial conjecture.

## Data and trust boundary

Each compressed edge part is below the ordinary 25 MB per-file web-upload limit. Shared intermediate checkpoints are omitted because the fast replay does not claim to establish their provenance; full regeneration reconstructs the necessary intervals. A deterministic package manifest authenticates all released files. Authentication is distinct from mathematical verification.

The companion manuscript, exact arithmetic implementation and output data have been independently checked internally. This is not external refereeing, proof-assistant certification, or an exhaustive novelty/priority determination. No external publication is performed by this package.
