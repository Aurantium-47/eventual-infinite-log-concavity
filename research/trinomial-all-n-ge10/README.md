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
- [Complete fresh edge reconstruction](validation/portable_full_edge_regeneration.json) subsequently rebuilt **all 1,929 enclosures** using the unchanged published generation, evaluation and sign-verification functions. Every midpoint, common radius and binary exponent matched. [Independent coverage checking](validation/portable_full_edge_coverage.json) verified all eight panels and the exact union with the 63 previously certified bypasses.
- This complete run used a reviewed resumable wrapper with two panel queues, with no restart or reuse of the earlier representative node. It did **not** invoke the literal `regenerate.py --full` command. The [run-method note](validation/FULL_EDGE_REGENERATION_METHOD.md) explains the execution and reproduction options.

These later validation results supplement the unchanged manuscript and do not imply human peer review, formal verification, or exhaustive novelty certification. Timing is environment-dependent.

## Completed whole-theorem internal review — 2026-11-02

**All integer exponents n ≥ 10; all iterations.** The final AI-assisted dependency review accepts the complete computer-assisted argument at fixed source `68f4c920606ad239fbc3a8195bc0987b790f5905`, including 2n distinct strictly negative fourth-iterate roots for n ≥ 4004. It covers the specific Medina–Straub trinomial assertion, not general Conjecture 5.2.

- [Review and precise acceptance scope](review-2026-11-02/REVIEW.md)
- [Whole-theorem dependency table](review-2026-11-02/DEPENDENCIES.md)
- [Literal regeneration, provenance, and independent-check limits](review-2026-11-02/REPRODUCE.md)
- [Grid and endpoint clarifications](review-2026-11-02/CLARIFICATIONS.md)

A new literal sequential `regenerate.py --full --backend flint` run exited 0, exactly rebuilding all 1,929 enclosures in 29m39.084s. This supplements—not rewrites—the earlier two-queue run above. The heterogeneous check covers 708 selected exact Taylor coefficients, not a second complete generator. The original manuscript, proof, data, and historical validation records remain byte-identical. Review summaries and a separately hashed evidence addendum are new; the original manuscript manifest does not authenticate this later addendum.

This completed internal review is AI-assisted, not human refereeing, formal proof-assistant verification, or an exhaustive novelty/priority determination. The draft remains open for external scrutiny.
