"""Identical coefficient contract; no floating-point approximation."""
from byte_packed_convolution import convolution as reference

def accelerated(a, b, degree):
    import flint
    if flint.__version__ != '0.9.0':
        raise RuntimeError('Use released python-flint==0.9.0, not a development build')
    n = min(degree + 1, len(a) + len(b) - 1)
    z = flint.fmpz_poly(a).mul_low(flint.fmpz_poly(b), n)
    return [int(z[k]) for k in range(n)]
