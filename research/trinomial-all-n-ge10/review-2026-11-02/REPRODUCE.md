# Reproduce the evidence

The audited proof, generator and data are fixed at commit `68f4c920606ad239fbc3a8195bc0987b790f5905`. This directory only adds review evidence. Its supplemental scripts have portable path adjustments and a fail-closed assertion guard; `SOURCE_MAP.json` records original and published SHA-256 values. The original proof files are unchanged.

From the repository root, using Python 3.12 and the official `python-flint==0.9.0` package:

```sh
python -m venv .venv-review
.venv-review/bin/python -m pip install python-flint==0.9.0
PY="$PWD/.venv-review/bin/python"
cd research/trinomial-all-n-ge10
"$PY" verify_manifest.py
cd certificate_package
"$PY" edge/replay_saved_inequalities.py
# Sequential full reconstruction, not replay. Bash's time keyword is sufficient.
time "$PY" -u edge/regenerate.py --full --backend flint
cd ../review-2026-11-02
"$PY" verify_evidence.py
```

The recorded literal full run exited 0 in 29m39.084s, rebuilding all 1,929 enclosures with exact equality of every midpoint, common radius, exponent and precision, and rechecking strict signs. Panel counts were 246, 245, 243, 241, 240, 239, 238, 237. Replay separately establishes the disjoint union of these pairs with 63 bulk bypasses equals all 8×249 cases, with ordering and joins. Run times vary with hardware.

`evidence/full-regenerate.log` SHA-256 is `f552e314b4acda4e9e8566ec9b00e4abc928c94e0c2701bfa7ad42dd39c946a8`. The canonical digest `22c038b14345430607d71e0eb7e599dd06338b2a453419d8d0b8fe15ade8904c` hashes the **saved** records, not a separately captured regenerated stream. Reviewed equality assertions plus the terminal log connect those records to this run. This is local execution evidence, not cryptographic execution attestation.

## Selected heterogeneous checks

Run the following in a disposable checkout/copy of the repository (preserving the sibling `certificate_package` directory) because scripts replace their own result files (new timings will change the evidence manifest):

```sh
"$PY" independent_formula/check_explicit.py
"$PY" independent_formula/check_minimum.py
"$PY" independent_formula/check_boundary_stream.py
"$PY" independent_formula/aggregate.py
```

The alternative algorithm expands the multinomial coefficient formula rather than importing the published recurrence or interval-Jet arithmetic. It uses the same FLINT backend. Its coverage is **708 distinct exact Taylor coefficients in five cases**, with eight duplicate coefficients agreeing: all 311 coefficients for panel 0/node 246, all 302 for panel 7/node 237, all 87 for panel 7/node 22, and orders 0–3 at panel 0/node 1 and panel 7/node 1. This does not independently reconstruct all 1,929 cases, reprove arithmetic-library internals, or alone certify analytic tails and whole-panel signs. The full-degree stream is substantially slower than replay and uses additional memory.

The original supplementary scripts relied on `assert` without rejecting optimized Python. The recorded runs used normal Python, not `-O`; their reported checks are valid under that execution condition. Published portable copies now explicitly reject `-O`/`-OO`. This is harness hardening, not a claimed repair of the mathematical proof. Official regeneration already rejects optimized Python. Never disable assertions.

The source receipt records the official wheel hash and installed-library identity checks. Those are environment provenance, not a substitute for the mathematical interval invariant and tail proofs. Mathematical source reasoning is in `BOUNDARY_SOUNDNESS.md`; whole-theorem dependencies are in `DEPENDENCIES.md`.
