#!/usr/bin/env python3
"""AI-assisted independent crosscheck adapting an independently supplied review method.

Evaluate the normalized ratio map using standard-library Fraction arithmetic,
not the merged integer expressions of verify.py or original author code. Rebuild
all data before comparing the pinned reference and the local reconstructed files.
Check every certificate's complete dependency cone. No network, source checkout,
third-party packages or enormous cutoff evaluation is needed. Explicit checks
remain active under Python -O. Only fraction_results.json is written.
"""
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMIT = "68f4c920606ad239fbc3a8195bc0987b790f5905"
REFERENCE_SHA256 = "d8191c9e9971d795a663212e88558fd82453e4335687590cb960abaa5091e31d"
PRECISION, MAX_INDEX, TARGET = 256, 2064, 2047
D = 1 << PRECISION


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def ceil_log2(value):
    require(value > 0, "nonpositive logarithm argument")
    power, count = 1, 0
    while power < value:
        power *= 2
        count += 1
    return count


def round_dyadic(value):
    require(value >= 0, "negative ratio endpoint")
    numerator, denominator = D * value.numerator, value.denominator
    lower, residual = divmod(numerator, denominator)
    upper = lower + (residual != 0)
    require(lower * denominator <= numerator < (lower + 1) * denominator, "floor residual")
    require((upper - 1) * denominator < numerator <= upper * denominator, "ceiling residual")
    return lower, upper


def ratio_map(center, left, right):
    require(all(0 <= v < 1 for v in (center, left, right)), "ratio map domain")
    odds = center / (1 - center)
    return odds * odds * (1 - left) * (1 - right)


def main():
    current = [round_dyadic(Fraction(k, k + 1)) for k in range(MAX_INDEX + 1)]
    all_layers, summaries, hits = [], [], {}
    domain_checks, map_evaluations = 0, 0
    for stage in range(ceil_log2(8 * TARGET) + 1):
        require(len(current) == MAX_INDEX - stage + 1, "retained prefix mismatch")
        require(current[0] == (0, 0), "original endpoint ratio changed")
        for lower, upper in current:
            require(type(lower) is int and type(upper) is int, "noninteger endpoint")
            require(0 <= lower <= upper < D, "invalid domain interval")
            domain_checks += 1
        all_layers.append(current)
        require(len(current) > TARGET, "lost target before certification")
        for k in range(1, TARGET + 1):
            lower, upper = current[k]
            if k not in hits and 3 * upper < D:
                require(stage <= ceil_log2(8 * k), "individual stopping time exceeded")
                hits[k] = {"k": k, "depth": stage, "lower": str(lower), "upper": str(upper),
                           "strict_gap_D_minus_3upper": str(D - 3 * upper)}
        summaries.append({
            "depth": stage, "retained_max_index": len(current) - 1,
            "maximum_upper": str(max(u for l, u in current)),
            "minimum_positive_index_lower": str(min(l for l, u in current[1:])),
            "maximum_interval_width": str(max(u - l for l, u in current)),
            "number_of_certified_target_indices": len(hits),
        })
        if len(hits) == TARGET:
            break
        previous, current = current, [(0, 0)]
        # Drop the artificial rightmost index; it has no supplied right neighbor.
        for k in range(1, len(previous) - 1):
            left, center, right = previous[k - 1:k + 2]
            lower_value = ratio_map(Fraction(center[0], D), Fraction(left[1], D), Fraction(right[1], D))
            upper_value = ratio_map(Fraction(center[1], D), Fraction(left[0], D), Fraction(right[0], D))
            require(0 <= lower_value <= upper_value, "monotone endpoint order")
            current.append((round_dyadic(lower_value)[0], round_dyadic(upper_value)[1]))
            map_evaluations += 2
    require(len(hits) == TARGET and stage == 12, "incomplete or unexpected final stage")
    certificates = [hits[k] for k in range(1, TARGET + 1)]
    computed = {
        "initial_sequence": "u_k=1/k!, k>=0; u_k=0 for k<0",
        "initial_ratio": "q_k=k/(k+1), including q_0=0",
        "precision_bits": PRECISION, "denominator": str(D),
        "initial_max_ratio_index": MAX_INDEX, "target_max_index": TARGET,
        "last_depth": stage, "layers": summaries, "certificates": certificates,
    }
    # Reference files are read only after independent reconstruction is finished.
    reference_bytes = (ROOT / "references" / "poisson_certificates.json.gz").read_bytes()
    require(hashlib.sha256(reference_bytes).hexdigest() == REFERENCE_SHA256, "reference hash mismatch")
    require(computed == json.loads(gzip.decompress(reference_bytes)), "full reference object mismatch")
    require(certificates == json.loads((ROOT / "reconstructed_certificates.json").read_text(encoding="utf-8")),
            "local reconstructed certificates mismatch")
    require(summaries == json.loads((ROOT / "reconstructed_layers.json").read_text(encoding="utf-8")),
            "local reconstructed layers mismatch")

    cone_nodes, max_initial_coefficient, min_headroom, min_time_slack = 0, 0, MAX_INDEX, 100
    for record in certificates:
        k, depth = record["k"], record["depth"]
        require(depth <= ceil_log2(8 * k), "certificate time cap")
        require(int(record["strict_gap_D_minus_3upper"]) > 0, "non-strict terminal gap")
        require(k + depth <= MAX_INDEX, "initial ratio dependency cone exceeds prefix")
        # At stage s, q through MAX_INDEX-s certifies positivity of the next
        # coefficient layer through MAX_INDEX-s. Initial coefficients 1/k!
        # are positive through MAX_INDEX+1 (and beyond). Induction thus gives
        # positive coefficients through MAX_INDEX+1-s at stage s.
        for s in range(depth + 1):
            q_left, q_right = max(0, k - depth + s), k + depth - s
            c_left, c_right = max(0, k - depth + s - 1), k + depth - s + 1
            require(q_right <= MAX_INDEX - s, "ratio cone reaches discarded edge")
            require(c_right <= MAX_INDEX + 1 - s, "coefficient cone exceeds positive range")
            for index in range(q_left, q_right + 1):
                lower, upper = all_layers[s][index]
                require(0 <= lower <= upper < D, "invalid dependency cone ratio")
                cone_nodes += 1
            if s == depth:
                require((c_left, c_right) == (k - 1, k + 1), "terminal neighbors missing")
        max_initial_coefficient = max(max_initial_coefficient, k + depth + 1)
        min_headroom = min(min_headroom, MAX_INDEX - k - depth)
        min_time_slack = min(min_time_slack, ceil_log2(8 * k) - depth)

    canonical = json.dumps(computed, sort_keys=True, separators=(",", ":")).encode()
    result = {
        "status": "PASS", "source_commit": COMMIT,
        "method": "AI-assisted independent normalized Fraction crosscheck; no author verifier imported or executed",
        "certificates_rebuilt": TARGET, "all_reference_fields_match": True,
        "local_reconstructed_certificates_and_layers_match": True,
        "reference_sha256": REFERENCE_SHA256,
        "canonical_reconstructed_object_sha256": hashlib.sha256(canonical).hexdigest(),
        "last_depth": stage, "retained_max_at_last_depth": MAX_INDEX - stage,
        "cumulative_certificates": [s["number_of_certified_target_indices"] for s in summaries],
        "first_hit_depth_distribution": dict(sorted(Counter(r["depth"] for r in certificates).items())),
        "domain_intervals_checked": domain_checks,
        "normalized_rational_endpoint_map_evaluations": map_evaluations,
        "per_certificate_cone_ratio_nodes_checked": cone_nodes,
        "all_terminal_ratios_have_positive_neighbors_by_cone_induction": True,
        "max_initial_coefficient_needed_by_target_certificates": max_initial_coefficient,
        "minimum_initial_right_headroom": min_headroom,
        "minimum_time_cap_slack": min_time_slack,
        "scope": "finite Poisson certificates only; analytic coverage and theorem closure require REVIEW.md",
    }
    output = json.dumps(result, indent=2) + "\n"
    (ROOT / "fraction_results.json").write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
