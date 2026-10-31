# Exact arithmetic backend

Fast inequality replay uses only Python's integer and Fraction arithmetic.
Full generation may use the official released PyPI package python-flint 0.9.0,
API `fmpz_poly(a).mul_low(fmpz_poly(b), n)` with n=min(d+1,len(a)+len(b)-1).
All returned coefficients are converted to exact Python integers.

The original Linux wheel SHA256 was
`376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76`.
The original loaded fmpz_poly binary SHA256 was
`a637d8bbd1f03454b1ac85614022fa38f6a72115b68a28e3cc8603352b479893`.
Other platforms have different binaries; the mathematical comparison is against
all saved integer jet fields, not a platform-specific binary hash.
The original backend substitution was checked by a complete representative
node replay, matching all midpoint/radius fields exactly with the pure-Python
signed-integer convolution. A standard-library fallback is included here.
No binary or wheel is bundled; installing dependencies is a separate step.
