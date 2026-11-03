#!/usr/bin/env python3
"""Reconstruct bounded Poisson certificates from the displayed ratio recurrence.

Python standard library only; exact integer arithmetic, no network or imports of
an author verifier. Both ordinary and optimized Python execute every check.
The finite computation is not a replacement for the analytic part of REVIEW.md.
Running this file regenerates its three adjacent JSON result files.
"""
import gzip
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMIT = "68f4c920606ad239fbc3a8195bc0987b790f5905"
SOURCE = ("https://github.com/Aurantium-47/eventual-infinite-log-concavity/blob/"
          + COMMIT + "/data/poisson_certificates.json.gz")
REFERENCE_SHA256 = "d8191c9e9971d795a663212e88558fd82453e4335687590cb960abaa5091e31d"
D = 2 ** 256


def require(condition, message):
    if not condition:
        raise ValueError(message)


def ceil_div(numerator, denominator):
    require(denominator > 0, "nonpositive denominator")
    quotient, remainder = divmod(numerator, denominator)
    return quotient + (remainder != 0)


def initial(last_index):
    # Exact outward rounding of q_0(k) = k/(k+1).
    return [(D * k // (k + 1), ceil_div(D * k, k + 1))
            for k in range(last_index + 1)]


def advance(row):
    require(row[0] == (0, 0), "true left endpoint changed")
    require(all(0 <= lo <= hi < D for lo, hi in row), "invalid input interval")
    result = [(0, 0)]
    # f(c,l,r)=c^2(1-l)(1-r)/(1-c)^2 increases in c and decreases
    # in l,r on [0,1). Its dyadic numerator/denominator includes the D below.
    # The artificial right edge is discarded, never assigned a zero neighbor.
    for left, center, right in zip(row, row[1:], row[2:]):
        lo, hi = center
        lower = lo * lo * (D - left[1]) * (D - right[1]) // (D * (D - lo) ** 2)
        upper = ceil_div(hi * hi * (D - left[0]) * (D - right[0]),
                         D * (D - hi) ** 2)
        require(0 <= lower <= upper < D, "invalid output interval")
        result.append((lower, upper))
    require(len(result) == len(row) - 1, "incorrect prefix shortening")
    return result


def main():
    row = initial(2064)
    hits, counts, layers = {}, [], []
    for depth in range(13):
        require(len(row) == 2065 - depth, "unexpected retained ratio range")
        require(all(0 <= lo <= hi < D for lo, hi in row), "invalid layer")
        for k in range(1, 2048):
            if k not in hits and 3 * row[k][1] < D:
                require(depth <= (8 * k - 1).bit_length(), "stopping-time bound failed")
                lo, hi = row[k]
                hits[k] = {
                    "k": k, "depth": depth, "lower": str(lo), "upper": str(hi),
                    "strict_gap_D_minus_3upper": str(D - 3 * hi),
                }
        counts.append(len(hits))
        layers.append({
            "depth": depth, "retained_max_index": len(row) - 1,
            "maximum_upper": str(max(hi for lo, hi in row)),
            "minimum_positive_index_lower": str(min(lo for lo, hi in row[1:])),
            "maximum_interval_width": str(max(hi - lo for lo, hi in row)),
            "number_of_certified_target_indices": len(hits),
        })
        if depth < 12:
            row = advance(row)
    require(counts == [0, 0, 2, 6, 13, 27, 56, 115, 231, 464, 930, 1862, 2047],
            "stage counts differ")
    require(len(hits) == 2047, "not all target indices certified")
    certificates = [hits[k] for k in range(1, 2048)]
    reference_bytes = (ROOT / "references" / "poisson_certificates.json.gz").read_bytes()
    require(hashlib.sha256(reference_bytes).hexdigest() == REFERENCE_SHA256,
            "reference hash mismatch")
    stored = json.loads(gzip.decompress(reference_bytes))
    require(stored["certificates"] == certificates, "certificate records differ")
    require(stored["layers"] == layers, "layer records differ")
    for key, value in {"denominator": str(D), "last_depth": 12,
                       "initial_max_ratio_index": 2064, "target_max_index": 2047,
                       "precision_bits": 256}.items():
        require(stored[key] == value, "reference metadata differs: " + key)

    # A second route: L applied to exact integer coefficients 64!/k!.
    # At depth j coefficients exist through 64-j, so ratios only through 63-j.
    scale = math.factorial(64)
    coefficients = [scale // math.factorial(k) for k in range(65)]
    row = initial(64)
    checks, endpoint_checks, direct = 0, 0, []
    for depth in range(9):
        require(len(coefficients) == 65 - depth and all(a > 0 for a in coefficients),
                "direct retained coefficient positivity failed")
        for k in range(len(coefficients) - 1):
            numerator = 0 if k == 0 else coefficients[k - 1] * coefficients[k + 1]
            denominator = coefficients[k] ** 2
            lo, hi = row[k]
            require(lo * denominator <= D * numerator <= hi * denominator,
                    "direct coefficient ratio outside interval")
            checks += 1
            endpoint_checks += (k == 0)
        direct.append({
            "depth": depth, "last_coefficient_index": len(coefficients) - 1,
            "compared_ratio_indices": [0, len(coefficients) - 2],
            "comparisons": len(coefficients) - 1,
            "max_coefficient_bits": max(a.bit_length() for a in coefficients),
        })
        if depth < 8:
            coefficients = [a * a - (coefficients[k - 1] * coefficients[k + 1] if k else 0)
                            for k, a in enumerate(coefficients[:-1])]
            row = advance(row)
    require(checks == 540 and endpoint_checks == 9, "unexpected comparison counts")
    result = {
        "status": "PASS", "counts": counts,
        "maximum_stopping_time": max(item["depth"] for item in certificates),
        "all_first_certified_times_obey_ceil_log2_8k": True,
        "strict_certificates_matched_pinned_data": 2047,
        "all_layer_records_match": True,
        "direct_ratio_comparisons": checks,
        "direct_endpoint_comparisons": endpoint_checks,
        "direct_interior_comparisons": checks - endpoint_checks,
        "direct_layers": direct, "source_commit": COMMIT,
        "reference_url": SOURCE, "reference_sha256": REFERENCE_SHA256,
    }
    for filename, data in (("results.json", result),
                           ("reconstructed_certificates.json", certificates),
                           ("reconstructed_layers.json", layers)):
        (ROOT / filename).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
