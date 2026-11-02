# Provenance and attribution

## Backend

- Official released package: [python-flint 0.9.0](https://pypi.org/project/python-flint/0.9.0/).
- Source release: [python-flint](https://github.com/flintlib/python-flint).
- Arithmetic library: [FLINT](https://flintlib.org/).
- Operation: exact integer `fmpz_poly.mul_low`.
- Recorded wheel: `python_flint-0.9.0-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl`.
- SHA-256: `376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76`.
- Official metadata: https://pypi.org/pypi/python-flint/0.9.0/json

The wheel was downloaded from the official PyPI release and its digest matched
that release's metadata. The wheel itself and bundled native libraries are not
redistributed here. Their authors retain their respective attribution and license
terms. The benchmark uses this released wheel, not an unpublished root-isolation
branch or modified FLINT development package.

## Mathematical and engineering scope

Aurantium; prepared with AI assistance. The contribution shown here is backend
integration, a deterministic reproducibility harness, and exact-output validation.
FLINT and python-flint receive credit for the mature exact arithmetic backend.
Signed Kronecker substitution is an established technique, not a new algorithm
claimed by this benchmark.

The parent project's Medina–Straub conjectural context and Xie–Zhang–Zhang
method attribution remain as stated in its REFERENCES.md and RIGHTS.md. This
addition does not reassign mathematical credit, imply human peer review, or grant
a new license for the parent materials. No third-party papers or binaries are
included. The existing repository's distribution scope remains unchanged.
