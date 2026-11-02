# Selected independent review computations

This is a curated, public subset of the AI-assisted review completed on 2 November 2026. It is not human peer review or formal verification. The exact input-archive and per-file original/published SHA256 mapping is in `SOURCE_MAP.json`. Seventeen source/result files are byte-identical; the assembly script has only its source-path selection replaced by an explicit command-line argument. No mathematical operations or acceptance comparisons were changed. The portable assembly copy was subsequently run against the frozen source in a separate directory: all checks passed, and its result JSON matched the historical result exactly.

Historical JSON results are retained as historical results, **not new executions of the portable copies**. Running scripts normally overwrites their adjacent result JSONs: copy this directory before reproduction if you want to retain originals. The original analytic report's narrower, earlier scope is historical; the new top-level review closes its boundary and final-assembly dependencies without rewriting that report.

## Environment and frozen input

Use Python with assertions enabled; unset `PYTHONOPTIMIZE` and never pass `-O`/`-OO`. For the analytic scalar-premise script install `sympy==1.14.0`; for the single-panel check install `python-flint==0.9.0`, preferably in an isolated environment. Other included calculations use only the Python standard library.

Obtain the exact repository commit `68f4c920606ad239fbc3a8195bc0987b790f5905`, as described in `../REPRODUCE_REVIEW.md`. Let `EDGE` be the absolute path to its `research/trinomial-all-n-ge10/certificate_package/edge` directory. Commands below run from **this independent_review directory**.

## Analytic core: five independent calculations

```sh
python3 analytic_core_review/local/rederive_local.py
python3 analytic_core_review/local/verify_phase_identities.py
python3 analytic_core_review/torus/verify_torus_constants.py
python3 analytic_core_review/auxiliary/verify_model_and_assembly.py
python3 analytic_core_review/auxiliary/rederive_scalar_premises.py
```

These respectively derive the local derivative/moment majorant, phase/variance identities, torus geometry and exact tail budget, model correction and combined budget, and scalar-premise Bernstein certificates. They do not import the author's implementation or read saved edge jets. The model script imports the included independent local-moment module. The mathematical connection from these exact calculations to the integrals is explained in `analytic_core_review/REPORT.txt`; PASS strings alone do not establish it.

## Final boundary-to-root assembly arithmetic

```sh
python3 final_dependency_review/assembly/verify_assembly_inputs.py "$EDGE"
```

This independently checks 2,241 positive endpoints, 2,232 strict adjacent comparisons, 63 whole-panel bypass phase/variance bounds, and eight joins. It uses direct power-basis operations and Bernstein conversion, not the author's Bernstein-product implementation. It reads the frozen rational node table and bypass list, but no saved jets. The analytic bulk theorem and the proof of the positive `u=0` limit are separate mathematical inputs, explained in the top-level review and clarifications.

## One whole panel/node by a third coefficient algorithm

```sh
python3 final_dependency_review/edge_math/independent_minimum.py "$EDGE"
```

The logarithmic-series differential recurrence reconstructs all 87 retained coefficients at panel 7/node 22, then independently bounds the Bernstein polynomial and both tails over the entire closed parameter panel. The optional `--minimum-receipt PATH` additionally compares exact-value hashes with the selected multinomial supplement's `minimum_receipt.json`. Without that option the mathematical reconstruction and whole-panel sign checks still run; do not claim the optional receipt comparison was performed. This is one panel/node, not all 1,929, and still shares FLINT arithmetic with the original generator.

## Entire earlier independent finite-range calculation

```sh
python3 review_bundle/independent_finite.py --max-n 4003 --bits 160
```

The historical adjacent JSON contains all 3,994 entry depths and their canonical digest. This script initializes exact full coefficient rows and uses full-row directed intervals rather than the author's rounded half-row initializer. The invariant-cone argument makes each successful entry valid for every later iteration. Full reproduction may take substantially longer than the smaller review checks.

The final dependency audit also recomputed all 12,160 PF4 seed determinants and checked division-free identities; its full script/receipt chain is not included in this selected subset. The assessed repository already supplies the PF4 checker and data. Do not describe this subset as containing every program or result from the original review archive.

## Limitations

No whole 1,929-case independent second generator, independent FLINT kernel, formal verification, human review, or priority certification is implied. Source hashes bind bytes; the original full execution evidence remains separate from these selected cross-checks. Some earlier supplementary programs use unguarded assertions, so normal Python execution is mandatory even when other included programs explicitly reject optimization.
