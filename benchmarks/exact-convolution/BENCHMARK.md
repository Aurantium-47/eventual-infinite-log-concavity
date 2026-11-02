# Observed benchmark

Recorded 31 October 2026. One existing reference run and one exact FLINT replay;
these are **not medians**. The benchmark is the complete node-200/panel-0
fixed-point computation at K=600, d=360, P=2048 (5,420 jet multiplications).

| Measurement | Byte-packed reference | Released FLINT backend |
|---|---:|---:|
| Total internal wall time | 283.532917 s | 13.777135 s |
| Generation through k=600 | 252.964613 s | 12.252219 s |
| Remainder | 30.568304 s | 1.524916 s |
| Peak RSS, Linux KiB | 25,616 | 40,624 |

Observed total ratio: **20.58×**. The generation/remainder split is a progress-log
boundary, not an instrumented separation of every algorithmic phase. The total
timer includes certificate generation, Horner evaluation, and bound construction;
it stops while constructing the receipt, before JSON files are written. Python
startup, dependency import, and the replay's preliminary tests are excluded.

The runs occurred in a shared Linux x86-64 cloud environment. The available
runtime reports CPython 3.12.14 and AMD EPYC 9V74; CPU allocation, scheduling,
frequency and concurrent load were not controlled or recorded per original run.
The environment observations are not a dedicated-machine performance guarantee.
Peak RSS is process-wide and includes imports and prior allocations; the original
FLINT replay also ran small preliminary checks. Do not interpret the RSS figures
as isolated per-kernel memory costs.

## Preserved evidence

- `evidence/reference_receipt.json` and `flint_receipt.json`: original exact
  certificate receipts, including their measured runtime and RSS.
- `evidence/expected_final_jet.json`: one copy of the identical final midpoint
  list and common radius, not two duplicate files.
- `evidence/observed_replay.json`: original successful replay summary;
  SHA-256 `b90c297209c14a6cf776f91ed099e2eb287661dbfa82d24c28b93bb68e58e27a`.
- `evidence/wheel_provenance.json`: official release filename, URL and SHA-256.

The original replay checked 160 seeded small cases against naive convolution and
the reference implementation, then compared all final midpoint/radius data and
all receipt fields except `seconds` and `peak_rss_kib`. Its recorded microbenchmarks
are supporting single samples, not the headline full-certificate timing.

The public runner is a path-portable extraction of that frozen computation.
Only input/output paths, the monotonic timer, per-run counter reset and explicit
CLI selection are adapted. Exact arithmetic and analytic bounds are preserved.
No heavyweight repeated baseline timing is included in this preparation.

## Limits and a future repeat protocol

The observation does not establish a universal 20× gain, a whole-proof ETA,
independent correctness of all mathematical bounds, or completion of the sharper
trinomial target. No new root-isolation development code is involved.

For a statistically stronger report, reserve an otherwise quiet CPU window,
record allocation and versions, perform three sequential paired runs in alternating
backend order, and check exact outputs for every pair before reporting raw times
and medians. Budget about 15–20 minutes of reference work plus overhead on the
observed machine. Do not run this protocol alongside a proof computation whose
throughput matters. No such repeated measurements are claimed here.

## Portable-package validation

After extraction, one additional accelerated-only run reproduced the original
final jet and every nonperformance reference receipt field exactly. It took
14.270370 s in a coordinated local CPU window; this is a portability check, not
a new paired speedup measurement or a replacement for the observed table above.
The 160 small-case tests, two large-integer cases and comparator mutation tests
also passed. See `evidence/package_validation.json`. The extracted reference
command was not rerun end to end; its arithmetic core is unchanged from the
recorded baseline. No repeated baseline jobs or medians are claimed.
