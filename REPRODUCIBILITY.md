# Reproducibility and execution scope

All supplied Python programs use the standard library and require Python 3.10 or later. No package installation is required. Run from this directory with assertions enabled; do not use `-O`.

## Minimal new-certificate entry

```sh
python -B code/verify.py
```

The program reads and compares the four files under data/:

- poisson_certificates.json.gz: all first strict local certificates for centers 1..2047, using 256-bit dyadic bounds and an initial prefix through index 2064.
- poisson_integer_crosscheck.json.gz: 540 exact ratio comparisons from direct iteration of 64!/k!, through depth 8, with the artificial right edge discarded.
- polynomial_crosscheck.json.gz: 55 retained scaled polynomials through depth 4 from initial indices 0..12, with degree, leading coefficient, norm and finite evaluation checks.
- constant_checks.json.gz: rational inequalities and symbolic cutoff exponent bounds; the enormous cutoff itself is not constructed.

The arithmetic functions and stored data are preserved from the source implementation. The only entry adaptation places the script under code/ and reads data/ relative to the package root. Its documentation and one output-description sentence refer to the manuscript. In normal comparison mode it does not overwrite the stored data. After manuscript preparation, the packaged default entry was run separately under a 100-MiB process/job and 30-second wall limit. It passed with Python 3.12.10, child/guard/shell exit 0 and empty stderr. External wall time was 0.328 seconds and peak child working set was 19,853,312 bytes. Startup and minimum available physical memory were 474,877,952 and 474,726,400 bytes; the run did not trigger a limit. All 24 pre-execution input files remained byte-identical. See verification/release_entry_run.json. This is reproduction of the packaged entry, not another independent proof review; the baseline and write-data modes were not used.

## Existing execution evidence

| Recorded check | Actual recorded scope | Boundary |
|---|---|---|
| Local independent reconstruction, Python 3.12.10 | 2047 strict Poisson centers; 13 cumulative layers; 540 direct coefficient-ratio comparisons | A separately written implementation, followed by the source new suite; not a new run of this relocated entry |
| Source new suite in that local run | New Poisson, integer-ratio, polynomial and rational-constant checks passed | No legacy baseline run |
| Separate external exact check, Python 3.13.5 | 2047 centers at 512 bits in s=1-q; 755 direct coefficient comparisons; 55 polynomials and 330 evaluations | Externally recorded execution, not local repetition |
| Externally recorded source baseline run | 994 specified exponent certificates and the associated finite regression data | Not rerun locally during the supplied local check or this preparation |

Clean summaries appear in verification/. The local combined recorded computation took about 0.401 seconds with peak working set 26,681,344 bytes and exit 0. That historical run did not record its startup physical-memory snapshot; no later snapshot is substituted for it. The external independent program recorded 1.163 seconds. These timings identify recorded runs rather than guaranteed performance on another machine.

The cumulative strict Poisson certificate counts at depths 0..12 are

    0, 0, 2, 6, 13, 27, 56, 115, 231, 464, 930, 1862, 2047.

The formulas, arbitrary-index inductions, uniform tilted approximation, growing-depth holomorphic argument and threshold existence are mathematical arguments in the paper. Their infinite ranges are not replaced by these finite executions.

## Optional legacy comparison

```sh
python -B code/verify.py --baseline
```

This first runs the new checks, then invokes baseline/verify.py with `--full`. The baseline contains certificates for exactly {10,...,1000} union {2000,10000,100000}; it does not certify every exponent through 100000. It also contains the earlier finite determinant, boundary-polynomial and finite-chain regression data. This optional command is outside the minimal new-proof check and was not run in preparing this candidate.

The optional baseline command writes data/baseline_recheck_current.log. `--write-data` intentionally rewrites the four new data files and their summary. Use a separate working copy for these modes so the distributed certificate bytes remain intact. The original baseline program and its mathematical data are preserved unchanged.

The LaTeX source is standalone. The supplied PDF was compiled sequentially with package installation and shell escape disabled; document production is distinct from mathematical execution.
