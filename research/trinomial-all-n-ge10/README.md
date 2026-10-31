# Trinomial proof — review draft

The proposed computer-assisted proof is in [24-page manuscript](manuscript/trinomial_research_draft.pdf) (24 pages), with combined Markdown and LaTeX alongside it. The chapter sources and `build_manuscript.py` reproduce the typesetting; see [build instructions](BUILD_README.md).

The exact arithmetic software/data are in `certificate_package/`; start with the [verification README](certificate_package/README.md) for the distinct fast-replay and full-regeneration commands. [Analytic verification map](ANALYTIC_VERIFICATION_MAP.md) documents arithmetic versus mathematical premises.

The claim is the specific all-integer n≥10 trinomial infinite-log-concavity assertion. Internal independent checks are complete; external peer review, proof-assistant formalization, and exhaustive novelty/priority certification are not claimed. This is a public review draft, not a peer-reviewed publication.

Run `python verify_manifest.py` to authenticate the included files. This verifies file identity, not the mathematical proof.

## AI assistance and validation scope

This work was developed with substantial AI assistance, including separate AI-assisted internal checks. These checks are not human peer review or formal proof-assistant certification. The original manuscript is preserved unchanged; later portable-validation results are reported here rather than silently rewriting its historical validation statements.

### Later portable-validation addendum

- [Full analytic validation](validation/portable_analytic.json): all 15 exact arithmetic stages passed, including cumulant certificates and all 28 weighted moments (70.957 seconds, exit 0).
- [Full finite validation](validation/portable_finite.json): every one of the 3,994 exponents from 10 through 4003 passed (366.180 seconds, exit 0); the canonical exact-results digest matches the frozen expected value.
- All 1,929 saved jet inequalities and 63 bypass boxes were replayed successfully. This fast replay does not regenerate enclosure provenance.
- Full portable regeneration of **one representative node** matched every saved integer field. The full portable regeneration of all 1,929 enclosures has **not** been rerun; commands are supplied. The original complete generating computation was performed.

These later validation results supplement the unchanged manuscript and do not imply human peer review, formal verification, or exhaustive novelty certification. Timing is environment-dependent.
