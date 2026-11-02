# Editorial and evidence clarifications

These clarify the proof at fixed commit `68f4c920606ad239fbc3a8195bc0987b790f5905`. They do not change its theorem, constants, nodes, data, algorithm, or computation range, and are not presented as repairs to a fatal proof gap.

## Candidate grid versus certified grid

The opening of analytic §10 describes a candidate grid with `0≤l≤32`; the completed certificate subsequently uses its **first eight panels**. The frozen `nodes.json` has exactly nine endpoints `u_l=l/32032`, `0≤l≤8`, and the eight closed intervals cover exactly `[0,1/4004]`. No node at `l>8` is used or required for the stated threshold. Reading the larger candidate grid as 32 required certificates would misstate the proof.

## Why the bypass signs remain strict at u=0

Strict positivity for `u>0` alone does not imply a strictly positive limiting value. Both convergence of the true function and a nonzero limiting amplitude are needed here.

Let `t(u)` be one of the panel-0 bypass nodes, `t0=t(0)>0`, `θ=π/16`, and `C=2048/[4(2π)^(15/2)]`. Set

`L(u,z)=log(1+uz+u²z²)/u`, `L(0,z)=z`.

For `|z|≤T=253` and small `u≥0`, the logarithmic coefficients give

`|L(u,z)−z|≤δ(u)=uT²/(1−uT)→0`.

The node is a rational function with positive denominator, so `t(u)−t0=O(u)`. In the same sixteen-leaf representation, normalized measure has total mass 1 and the kernel lies between 0 and `2^15`. Comparing the exponentials gives

`|F_u(−t(u)^16)−F_0(−t0^16)| ≤ 2^15 exp(16t0) {exp[16(δ(u)+|t(u)−t0|)]−1} → 0`.

Thus convergence controls the actual fourth iterate, not merely a finite coefficient truncation. Also

`A_(1/u)(ut(u)) → A0 = C exp(16t0 exp(iθ))/(t0 exp(iθ))^(45/2)`,

so

`|A0|=C exp(16t0 cosθ)/t0^(45/2)>0`.

For example, the denominator limit is quantified by

`v(z)−z=z²(2−2z−2z²−z³)/p(z)²`

and `|p(z)|≥1−|z|−|z|²>0` on `|z|≤1/15`. The bypass phase error is less than `1/3`, and

`cos(1/3)−47/50≥17/18−47/50=1/225`.

Consequently, for `u>0`, the signed true value exceeds `2|A_(1/u)(ut(u))|/225`. Taking the now-justified limit gives

`(−1)^j F_0(−t0^16) ≥ 2|A0|/225 > 0`.

This closes the three panel-0 bypass endpoints `j=247,248,249`. All other panel-0 endpoints have closed Taylor certificates.

## What the regeneration digest does and does not establish

`22c038b14345430607d71e0eb7e599dd06338b2a453419d8d0b8fe15ade8904c` is the canonical digest of **saved input jet records**, not an independently captured regenerated output stream. Reconstruction is connected to those records by the reviewed full CLI's exact equality checks of every `m/rad/e/p` field and its successful terminal execution record. Hashes are not proof or cryptographic execution attestation.

## Exact scope of alternate-coefficient checks

The alternate explicit-multinomial computation covers:

| Panel / node | Retained orders | Distinct coefficients |
|---|---|---:|
| 0 / 246 | 0–310 | 311 |
| 7 / 237 | 0–301 | 302 |
| 7 / 22 | 0–86 | 87 |
| 0 / 1 | 0–3 | 4 |
| 7 / 1 | 0–3 | 4 |
| **Total** | | **708** |

Eight overlapping checks have matching exact-value hashes but are not double-counted. These five cases are not a second full reconstruction of all 1,929 cases. They share python-flint with the principal generator. Coefficient containment alone does not replace interval-wide Bernstein signs and the two tail bounds.

The original evidence snapshot retained an optional `PENDING` state. The later supplement supplies the completed full-order receipts for the selected cases; it supersedes that pending status, not the original snapshot's bytes. An interrupted trial log is not counted as successful execution.

## Assertions and reproduction

Some supplementary scripts use `assert` without a `__debug__` guard. Their recorded normal-interpreter runs are useful evidence, but running them with `python -O` or `-OO` would suppress checks. **Use normal Python without optimization and unset `PYTHONOPTIMIZE`.** The main regeneration CLI rejects optimized execution; the independent whole-panel logarithmic-series checker also rejects it. This caveat limits claims about the supplemental receipt machinery; it is not a missing premise in the interval proof.

The finite-range portable receipt is a summary, not a saved trace of every directed interval. Its separate full independent finite run and corresponding complete results are distinct evidence; do not describe a summary identity check as reexecuting all 3,994 exponents.
