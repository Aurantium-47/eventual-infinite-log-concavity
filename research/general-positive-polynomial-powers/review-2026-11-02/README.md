# General positive-polynomial powers: independent review

This package is an **AI-assisted independent mathematical audit (独立自动数学复核)** of the **existing October 14, 2026 Theorem B**, at a fixed public commit. It is not a new theorem and does not settle the sharp trinomial starting threshold.

- [English mathematical review](REVIEW.md)
- [中文摘要](SUMMARY.zh-CN.md)
- [Local Lemma 1 wording erratum](ERRATUM.md)
- [Fixed sources and attribution](SOURCES.md)
- `verify.py`: independent exact standard-library finite verifier
- `crosscheck_fraction.py`: independently reconstructed normalized-rational route and dependency-cone checks
- `fraction_results.json`: deterministic second-route result summary
- `results.json`: reproduced result summary
- `reconstructed_certificates.json`: 2047 strict local certificates
- `reconstructed_layers.json`: 13 layer summaries
- `references/poisson_certificates.json.gz`: unchanged pinned author reference data
- `SHA256SUMS`: file-integrity manifest (all other files)

## Reproduce

```sh
python -B verify.py
python -B crosscheck_fraction.py
sha256sum -c SHA256SUMS
```

The script resolves data relative to itself, so it also runs when invoked by path from another working directory. Explicit checks remain enabled under `python -O`; no third-party packages or network are needed. The first script writes its three adjacent JSON outputs; the second writes `fraction_results.json`. Repeated runs are deterministic. On systems without `sha256sum`, use another SHA-256 implementation to check the manifest.

The finite computation matches all certificate and layer records and performs 540 direct ratio comparisons (531 interior, 9 left-endpoint). Analytic coverage of all remaining indices, full-tilt complex estimates, growing-depth control, and the common threshold are explained in the review, not claimed as machine verification.

This directory is self-contained and does not require changes to any sharp-trinomial materials, manuscript sources, or repository metadata.

The November 3 cross-check agrees with the original audit and supplies explicit p-dependent Gaussian constants and complete finite dependency-cone checks. This remains an AI-assisted review of the old theorem, not a new family, priority determination, human peer review, or formal certification.
