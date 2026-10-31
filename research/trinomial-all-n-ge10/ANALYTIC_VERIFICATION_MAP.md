# Regenerating the analytic certificates

This map separates exact arithmetic regeneration from file authentication and from mathematical arguments. The portable arithmetic route is `certificate_package/analytic/`. It does not generate edge jets or finite-exponent certificates. The accompanying analytic chapter supplies the integral representation, contour/domain arguments, geometric decomposition and inequality implications.

## Environment and command

Use Python3 with its standard library and SymPy, with assertions enabled (never `python -O`). The exact selected source copies are listed with their original and portable SHA256 hashes in `analytic/SOURCE_MAPPING.json`. Arithmetic uses integers, Fractions and SymPy exact rationals; float diagnostics do not determine acceptance. The checked environment used Python 3.12.14 and SymPy 1.14.0; the package requirements pin SymPy 1.14.0. These versions specify the reproducibility environment, not an additional mathematical assumption.

From any working directory:

```sh
python /path/to/certificate_package/analytic/run_analytic.py --full
```

Without `--full`, the command only lists the plan. With it, it executes every stage below, requires successful exit, and records stdout/stderr under `analytic/run_logs/`. This includes potentially expensive exact cumulant and weighted-moment reconstruction. All 15 stages were subsequently rerun successfully from the portable package, including exact cumulant and weighted-moment reconstruction. The code/input hashes and terminal result are recorded in `validation/portable_analytic.json`. Earlier smoke tests are described below.

## Required stages and dependency graph

All script/data names in this table are relative to `certificate_package/analytic/`.

| Stage | Executable | Inputs beyond code | Arithmetic regenerated |
|---|---|---|---|
| Global16-saddle algebra | `check_16_saddle_algebra.py` | none | curvature numerator identities and the outer-angle gap15/164 |
| Gaussian conditioning | `check_complex_variance_conditioning.py` | none | exact positive Bernstein coefficients; imaginary/real variance ratio and normalization loss<2 |
| Sharp real cumulants | `check_sharp_real_cumulant_bounds.py` | none | rational positive certificates for Imκ3 and Reκ4 and supporting exact variance/loss comparisons |
| Saddle complex cumulants | `check_uniform_cumulant_bounds.py` | none | κ3..κ8 rational numerator derivatives, squared-modulus polynomials, Bernstein coefficients on all prescribed rectangles |
| Wide box cumulants | `check_wide_box_cumulant_bounds.py` | none | corresponding κ4..κ6 bounds on the wider angular box |
| First correction | `check_first_saddle_correction_independent.py` | none | balanced-tree weighted Gaussian moments and exact B1 coefficients−16,1685/128,−315/32 |
| Local remainder moments | `audit_local_moments_independent.py` | `LOCAL_HOMOTOPY_BUDGET.log` | independent integer-encoded enumeration of all28 moment values; compares each to supplied expected value and writes `LOCAL_HOMOTOPY_INDEPENDENT_MOMENTS.json` |
| Local fourth-derivative budget | `audit_local_budget_independent.py` | regenerated moments; `LOCAL_HOMOTOPY_TAU_BUDGET_RECEIPT.json` | independent89-term positive polynomial, complete exponent-set equality, exact τ-integrals, square-root bounds and C100<36821; includes model-tail L2 reconstruction |
| Explicit model norm cross-check | `check_model_tail_norm.py` | regenerated moments | six-term squared-norm formula=7405704307825/1693651716<67²; redundant with previous stage but short and transparent |
| Gaussian model restoration | `check_gaussian_correction_box_tails.py` | none | rational Chernoff bounds and positive exponential partial sums; model restoration<11/500 at V>=225 |
| Actual torus scalar inputs | `audit_actual_torus_certificates.py` | none | central curvature and wideκ4 certificate,17 slab bounds, scalar tail comparisons and the B1 bound53/V; older320/400 checks are harmless additional checks |
| Selected V250 budget | `independent_audit_v250_arithmetic.py` | none | all selected outer-region/slab bounds, corrected two-outer prefactor, full nonprincipal gap and exact budget18717720003/20000000000<47/50 |
| Phase bridge algebra | `check_phase_bridge_algebra.py` | none | Im(mp), Im(mq), Im(v), modulus comparisons, real variance monotonicity and exact1001*v(7/20)>400, hence also>250 |
| Final harmonic join | `independent_final_join_250.py` | `FINAL_HARMONIC_JOIN_250_RECEIPT.json` rational33 nodes | fresh Machin/trigonometric rational enclosures and exact direct-Bernstein verification of all32 join panels; ignores original claimed controls |
| Ordering and bypass | `audit_461_bulk_bypass_independent.py` | frozen node table and frozen classification below | all8184 endpoint comparisons and independent power-polynomial/Bernstein checks of exactly461 reported bypasses, including phase margins, variance and domain bounds |

The two frozen inputs for the last row are `ALL249_HARMONIC_RATIONAL_CANDIDATES.json` and `ALL249_BULK_BYPASS_CLASSIFICATION.json`. Their hashes are pinned in the checker. They supply rational candidates and a proposed subset, not assumed mathematical positivity: the checker proves every selected inequality itself. Failures outside that subset are not interpreted as false signs. The selected eight-panel theorem uses63 of the461 certified boxes; the edge package proves every remaining sign.

The final join's33 candidate nodes must coincide with node249 of the frozen249-node table. The portable runner explicitly checks this identity before executing the stages.

## Why this is a compact route

The local remainder uses the independently encoded moment/budget route. It therefore does not need the original cwd-dependent `check_local_homotopy_tau_budget.py`, its dynamic source-prefix import, or `check_second_saddle_correction.py`. The28 expected values and89-term expected receipt are retained for exact comparison; they are NOT substitutes for regenerating the arithmetic. The runner always regenerates the moment file before consuming it. That output is generated by the runner before the budget stage consumes it; it is not supplied as a substitute for reconstruction.

The wide-box quarter-partition checker replaces the duplicative eighth-partition checker. The V250 independent arithmetic replaces the reference threshold checker. The independent final-join route does not import the numerical phase solver, mpmath or source generator. The bypass independent route does not need the candidate generator, classification compiler or phase-solving imports. Only the exact arithmetic premises used in the stated proof are included in this regeneration plan.

## Mathematical arguments not replaced by these programs

The scripts verify algebraic identities and quantitative arithmetic. They do not by themselves prove: the exact16-leaf integral and kernel identity; branches/absolute convergence of the real-exponent extension; the global saddle/torus cover and coarea factors; local homotopy differentiation and parity cancellations; complex Gaussian moment interpretation; Gaussian-to-torus distinction; monotonic extension of scalar estimates to all V>=250; phase existence/uniqueness; arctangent inequality directions; or the final real-root count and preservation theorem. Those are explicit arguments in the proof chapters. In particular, a collection of positive Bernstein outputs alone is not the analytic lemma.

## Portability and validation scope

1. Sealed originals are untouched. Copies add an assertions-enabled guard. Both cumulant loops now assert each computed `ok`: the old stdout-only scripts could exit0 even when a result row said false. This closes an execution-validation weakness without changing their polynomials, domains or rational arithmetic.
2. Every selected copied script already uses `__file__`-relative paths or no paths. The avoided author moment generator had hardcoded cwd paths; it is not required here.
3. Scripts that write sibling receipts operate only inside this copied directory. Running the portable plan must not overwrite sealed original receipts. Hash checks authenticate version/content; they do not regenerate arithmetic.
4. `SOURCE_MAPPING.json` identifies source-to-portable transformations. The final package manifest additionally covers the runner and short norm checker. A subsequent full portable analytic rerun passed; see `validation/portable_analytic.json`.
5. Light packaging checks: original/portable finite core byte equivalence and expected canonical full-result digest; finite exact toy oracle and -O guard; analytic saddle/phase algebra; all32 final joins; all461 bypasses plus8184 ordering comparisons; local budget from the previously regenerated28 moments; independent six-moment norm reconstruction; Gaussian tail bounds; V250 scalar budget. These checks regenerate their arithmetic, not just hashes. The subsequent full command also regenerated all moment/cumulant arithmetic successfully; the validation record distinguishes these later results from the earlier smoke tests.
