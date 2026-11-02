# Reproducing the computational premises

The accompanying `certificate_package` has three independent directories: `finite`, `analytic`, and `edge`. It requires Python with assertions enabled. Exact analytic polynomial checks use SymPy 1.14.0, and accelerated edge regeneration uses python-flint 0.9.0. The finite checks and saved-edge replay require only the standard library. Dependency versions and backend provenance are pinned in the package.

From the package directory, the following commands reconstruct the stated premises:

```sh
python finite/verify_pf4.py
python finite/verify_finite.py --full --output finite_result.json
python analytic/run_analytic.py --full
python edge/regenerate.py --full
python edge/replay_saved_inequalities.py
```

The finite command verifies all 3994 exponents in the finite range, not a selection. The analytic command reconstructs the rational polynomial and weighted-moment arithmetic underlying the displayed inequalities. The edge-generation command reconstructs all interval enclosures from the coefficient recurrence and four applications of the operator. Finally, the saved-inequality command evaluates every enclosure's strict sign margin and its two analytic remainder budgets.

For a shorter inspection, `python edge/replay_saved_inequalities.py` alone checks all 1929 saved enclosure inequalities, 63 bypass boxes, node ordering and the final join. This shorter command is deliberately described as *conditional on the saved enclosures*: it does not reproduce their interval-propagation provenance. The separate representative command

```sh
python edge/regenerate.py --panel 0 --node 200
```

reconstructs one enclosure and compares every deterministic midpoint, radius and exponent. A successful representative test is not represented as a full-chain rerun. The original complete generation and independent saved-inequality checks were performed; the portable full-generation command is supplied for reproduction.

Eight deterministic compressed data files contain the original final jets, one file per parameter panel. Hash manifests authenticate the files and identify the exact reproducibility version. Hash agreement is not a substitute for the mathematical implications proved in the manuscript or for arithmetic reconstruction. Intermediate shared coefficient checkpoints are omitted from the compact distribution; full regeneration rebuilds them in memory.

The computational evidence and proof composition have received independent internal checks. External peer review and proof-assistant formalization remain distinct activities; neither is claimed by the present draft.
