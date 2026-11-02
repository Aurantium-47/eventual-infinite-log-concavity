# Independent boundary-source soundness audit

Date: 2026-11-02. Fixed source: `68f4c920606ad239fbc3a8195bc0987b790f5905`.
Auditor scope: fresh boundary reconstruction and its mathematical interpretation, not the whole trinomial theorem. This is an internal AI audit, not human peer review or formal verification.

## Verdict

**ACCEPT the boundary-source certification of the 1,929 Taylor cases**, conditional on ordinary correctness of Python integer/Fraction operations and FLINT exact integer convolution. The released algorithm genuinely reconstructs the relevant finite Taylor polynomials from the defining coefficient family; the observed full-run equality is not merely replay of saved inequalities. Inspection of the enclosure invariants and analytic tails establishes why these are interval-wide sign certificates rather than sampled signs.

**ACCEPT exact coverage and the arithmetic premises for the additional 63 bypasses and eight joins.** Their sign interpretation remains explicitly conditional on the separately reviewed uniform bulk estimate for real ν > 0, 0 < s < 1, νv(s) ≥ 250. This audit does not independently reprove that integral estimate. The u = 0 endpoint follows from the positive limiting amplitude and continuity, detailed below.

No critical mathematical gap found in this boundary component. This verdict is NOT acceptance of the full infinite-log-concavity theorem, its finite/PF4 components, preservation theorem, novelty or priority.

## Execution and frozen evidence

Source base: the frozen commit and its boundary package; see `SOURCE_MAP.json`.
The audit script `check.py` independently compared every source/input SHA listed in `evidence/receipt.json` both with current bytes and the exact Git commit blobs, verified HEAD and absence of tracked changes in the research tree, and checked terminal log and exit receipt. An untracked `__pycache__` exists; it is not a tracked-source modification.

The full log SHA256 is `f552e314b4acda4e9e8566ec9b00e4abc928c94e0c2701bfa7ad42dd39c946a8`. It contains fresh shared-generation progress for eight panels, matches 246, 245, 243, 241, 240, 239, 238, 237, terminal `full_edge_generation: true`, count 1929, and Bash wall time 29m39.084s. The separate exit receipt is 0. The reviewed CLI rejects Python -O; its success requires full exact `{m,rad,e,p}` equality and strict signs, not a numerical tolerance.

The canonical saved-jets digest is a digest of input records, not a separately captured regenerated output stream. The full CLI's comparisons are what connect that digest to reconstruction. This distinction is sound and must remain in any report. This is normal local execution evidence, not cryptographic process attestation.

## Why the generator computes the claimed object

For g_u(z) = (1 + uz + u²z²)^(1/u), interpreted analytically at u = 0, differentiation gives

`(1 + uz + u²z²) g'_u(z) = (1 + 2uz) g_u(z)`.

Coefficient comparison gives exactly the implemented recurrence

`(k+1)b_(k+1) = (1-ku)b_k + [2u-(k-1)u²]b_(k-1)`, with b_0=b_1=1.

The code substitutes u=c+hw and performs formal Taylor algebra. Its four streaming three-element buffers begin with a zero negative-index neighbor. Feeding coefficients through index K+4 therefore produces precisely indices 0..K of four zero-extended L stencils. There is no accidental shift and no read of saved coefficient jets in `generation`.

`evaluate` takes the independently generated shared coefficients, truncates/reprecisions them, constructs the Taylor coefficients of `-t_c^16 (1+ahw)^(-16)` by the binomial formula, and Horner-evaluates the finite K polynomial. The saved record is used as the comparison target, not as the starting polynomial. Shared d=360 and K=600 cover every row; record guards enforce these caps. Formal truncation cannot change lower retained coefficients, including through four L maps or Horner composition.

The separate explicit multinomial formula

`b_(0,k)(u) = sum_(q=0..floor(k/2)) u^q product_(i=0..k-q-1)(1-iu)/(q!(k-2q)!)`

follows directly from the formal binomial expansion and is polynomial in u. I inspected the alternative checker: it does not import the published recurrence or Jet arithmetic. The worker's four low-order cases include maximum K=556, final boundary K=538 and both near-origin endpoints. More decisively, I independently reexecuted the alternative checker for panel7/node22, K108, all retained orders 0..86: PASS, exit0, ~7.97s, recorded in `independent_minimum.log`. The formula method still uses FLINT rational polynomials, so its independence is mathematical/algorithmic, not arithmetic-library independence. The full-degree extreme cases were pending at this audit stage and are NOT counted in this boundary-only verdict; their subsequent terminal results are recorded separately in `independent_formula/aggregate_receipt.json`.

## Interval arithmetic invariant

Represent each exact Taylor coefficient by `2^(e-p) [m_i-rad,m_i+rad]`.

- Rational construction and scalar multiplication round integer quotients and add the exact absolute residual divided by a positive denominator, rounded upward. Negative numerators are safe: Python divmod plus the tie convention need only supply an integer midpoint; the residual bound is exact.
- Normalization, exponent alignment and precision reduction use `ceil((rad+max residual)/D)`. Increasing precision or nonpositive normalization shifts are exact powers of two. Normalization retains zero midpoints with nonzero radius.
- Addition aligns scales before summing radii. Shift may unnecessarily retain radius on introduced zeros, but that is conservative.
- For multiplication, each retained coefficient's error is bounded by `rad_b sum|m_a| + rad_a sum|m_b| + (d+1)rad_a rad_b`; exact integer convolution supplies the midpoint. The stored raw exponent e_a+e_b-p is correct because the representation contributes a further factor 2^-p.
- Truncation preserves the coefficientwise invariant. No floating-point quantities occur in the enclosure arithmetic or sign test.

These observations establish an induction over the computation, rather than relying on test counts. As diagnostic support, `check.py` also used independent Python Fraction values at interval edges/interiors to exercise low precisions, signed midpoints, large radii, shifts, scalar arithmetic, multiplication and exponent changes, plus independent Bernstein formulas (1200 checks). These finite diagnostics are not presented as the proof.

## Analytic error terms: mathematical enclosure, not just execution match

I checked §§8.1–8.4 against `certificate_math.py`:

1. The coefficient of log p(w) is 1/l when 3 does not divide l and -2/l otherwise. Thus the positive absolute derivative majorant H has coefficient |c_l|(l-1) at q^(l-2). Terms l=2..32 plus `2q^31/(1-q)` dominate the whole derivative series. The disk |u-c|≤r remains inside |uz|<1 when q=(c+r)R<1. The removable u=0 singularity is handled analytically by this series.
2. At real c>0, |g_c(z)|≤p(cR)^(1/c). Integrating the parameter derivative yields E = log p(cR)/c + rR²H(q). Cauchy gives |b_0,k|≤exp(E)R^-k. Four L applications give constants C_(j+1)=2C_j², hence 2^15 exp(16E) R^-16k. A missing negative-index neighbor improves, not worsens, the estimate.
3. The moving node is analytic on the disk if |a|r<1, with |t(u)|≤T. Summing the K-polynomial bound using R>T gives M/(1-(T/R)^16). Cauchy in parameter u yields the Taylor remainder factor `(h/r)^(d+1)/(1-h/r)`. The verifier supplies r=4h, so h<r is guaranteed even though the helper does not separately assert it.
4. The coefficient tail uses a DIFFERENT real-parameter radius R0=2T0. For 0≤u≤U and UR0<1, log p(uR0)/u≤R0+UR0²/2. To verify this elementary inequality, the derivative of q+q²/2-log(1+q+q²) equals q²(q+2)/(1+q+q²)≥0. Cauchy and the geometric tail give exactly the implemented binary factor 2^-16(K+1)/(1-2^-16).
5. `log_upper` is the positive atanh partial sum plus a geometric upper remainder. The ten-term atanh sum for log2 is a lower bound; since E is positive, `ceil(16E/log2lower)` is an upper exponent for exp(16E). All such comparisons are exact Fraction arithmetic.
6. The verifier uses B=0. No unaccounted normalization factor is being applied to the analytic errors or recorded Taylor coefficients.

Consequently the two errors bound distinct omissions: Taylor truncation of Q_K, and coefficient truncation from F_u to Q_K. Neither substitutes for the other.

## Bernstein signs

After w=2x-1, a polynomial with power coefficients q_k has degree-d Bernstein controls

`beta_i = sum_(k≤i) q_k * C(i,k)/C(d,k)`.

The implementation's two triangular conversions produce exactly these controls. Their convex-hull property bounds the midpoint polynomial on the entire closed panel. The common coefficient radius contributes at most `(d+1)rad*2^(e-p)` because |w|≤1, added only after converting the midpoint polynomial. This avoids incorrectly assuming that power-basis coefficientwise errors remain unchanged in Bernstein basis.

I independently computed the closed-form conversion with Python Fraction for the actual degree86 panel7/node22 record, as well as small signed polynomials, and obtained exactly the same lower/upper bounds. The sign verifier then subtracts both analytic errors with strict inequalities and the correct node parity.

## Parameter coverage, bypass and join dependencies

The frozen input grid is checked to equal i/32032 for i=0..8, so its closed union is exactly [0,1/4004]. Endpoint node lists are positive, of length9, indexed uniquely1..249. Independent set inspection confirmed 1929 unique Taylor pairs and 63 unique disjoint bypass pairs whose union is exactly all 8×249 pairs. Counts alone are not the coverage argument.

Reciprocal interpolation gives `t(u)=LR / ((1-lambda)R+lambda L)`. Positive denominators and endpoint ordering imply strict ordering throughout each panel; adjacent panels share the same table endpoint. This is the same node formula used by regeneration and by bulk bounds.

I inspected `bulk_bounds.py`: its Machin/alternating-series pi and trig brackets, positive Bernstein denominator bounds, rational arctan bounds, monotonicity caps below1 for the cubic lower approximation, variance inequality and degree16 phase margins align with §9. The bypass check explicitly requires s=ut<1 and νv(s)>250; for u>0, ν=1/u>0. Thus it stays within the real-ν domain reported accepted by the separate analytic-core review, without using real-ν reciprocal roots or polynomial degree. The joins certify phase below250pi; using that for ordering against the actual bulk phase point additionally depends on phase monotonicity in the separately reviewed core.

At u→0, t(u)→t0>0. Formula(4.1) with ν=1/u and s=ut(u) yields the positive modulus limit

`|A_0| = [2048/(4(2pi)^(15/2))] * exp(16t0 cos(pi/16)) / t0^(45/2) > 0`.

The coefficient majorants above give local uniform convergence of F_u at these moving nodes. Since cos(1/3)−47/50≥1/225, the signed values for u>0 are at least 2|A_ν|/225; continuity preserves a strictly positive endpoint margin. This supplies the endpoint argument, not an unsupported inference that limits of positive values must stay positive.

## Residual assumptions and exclusions

- Correct exact arithmetic/runtime/library and integrity of recorded local execution; no formal proof assistant or independent implementation of FLINT internals.
- The uniform bulk theorem and its stated real-ν extension, plus phase monotonicity for the joins, must be accepted from their own audit. They are not consequences of regenerating 1929 records.
- Whole-theorem assembly additionally requires the finite n=10..4003 and PF4 proofs, polynomial/scaling/root-counting premises and the preservation result. This audit is not a substitute for those checks.
- No novelty, external peer review, publication readiness, or legal/authorship declaration is inferred.

## Audit execution receipts

`checks.json`: frozen blob/hash, execution-log structure, independent interval/Bernstein diagnostics and exact pair coverage PASS.
`independent_minimum.log`: independently reexecuted alternative explicit formula comparison of all87 coefficients PASS.
`replay.log` / `replay.exit`: this auditor also reran the released exact inequality/coverage/bypass/join checker, obtaining1929 Taylor inequalities,63 bulk boxes, ordering/join PASS, exit0. This was an inexpensive verification of inequalities, not a second full regeneration, and is labeled accordingly.
