# Theorem dependency map

Fixed assessed source: `68f4c920606ad239fbc3a8195bc0987b790f5905`.
All manuscript references below are within `research/trinomial-all-n-ge10/`; PDF page numbers refer to the 24-page manuscript. “Accepted” means the AI-assisted internal review's assessment, not external peer review or formal verification.

| Node | Exact scope | Mathematical / computational dependencies | Source | Assessment |
|---|---|---|---|---|
| D | Uniform two-saddle estimate, phase monotonicity and bulk signs; integer domain includes s=1, real-parameter domain excludes it | Sixteen-leaf identity, local and torus error bounds, scalar certificates | `ANALYTIC_PROOF.md` §§2–7; PDF pp. 7–16 | Earlier analytic review accepted; fixed-version identity checked |
| E_T | 1,929 true-function signs on closed panels | Defining recurrence, outward interval invariant, Bernstein range, two distinct analytic tails, literal full reconstruction | Analytic §8; PDF pp. 17–19; `certificate_package/edge/` | Accepted |
| E_B | 63 bypass signs, including u=0 | D's real-parameter interface, exact whole-panel phase/variance bounds, quantitative nonzero limiting amplitude | Analytic §9; PDF pp. 19–20 | Accepted |
| E | Exactly 1,992 panel/node pairs, positive ordered nodes | E_T + E_B, exact set partition, nine grid endpoints, reciprocal interpolation | Analytic §10; PDF pp. 20–21 | Accepted |
| J | `t_249(1/n)<n s_(n,250)` | Eight strict phase join bounds and D's strict phase monotonicity | Equation (9.3); PDF p. 20 | Accepted |
| R | Fourth-layer polynomial has 2n distinct negative roots for every integer n≥4004 | E + J + D, intermediate value theorem, exact degree and reciprocity | Analytic §10; PDF p. 21 | Accepted |
| F | Every iteration for every integer 10≤n≤4003 | Complete finite-range evidence; positivity before entry; invariant q≤1/3 cone | `FINITE_AND_ALGEBRAIC_PROOF.md` §1; PDF pp. 3–4 | Accepted |
| P | Layers 0–3 nonnegative for every n≥56 | PF4 finite-to-all-minors reduction, 12,160 seed determinants, convolution, division-free identities | Finite/algebraic §§2–3; PDF pp. 4–5 | Accepted |
| B | Real-rootedness and nonnegative coefficients preserved by L | Brändén's published theorem, applied to fourth-layer polynomial; nonzero endpoints | [Brändén, §3](https://arxiv.org/abs/0909.1927v3) | Existing theorem; hypotheses checked |
| T | Every integer n≥10, every iteration j≥0, every integer position k | F for n≤4003; P + R + B for n≥4004 | PDF pp. 2 and 21 | Accepted |

No additional unproved mathematical lemma was left by the final dependency review. This does not eliminate the explicit arithmetic/runtime/execution trust base or determine priority. In particular, R is not a premise for P, and coefficient positivity at layer 4 is not used to prove R.

## Frozen source identities

| File | SHA256 |
|---|---|
| `manuscript/trinomial_research_draft.pdf` | `5e9974bde3ef72d8a86d6ebdd72c1e07707c3612ac3549355a9689c574ac1739` |
| `ANALYTIC_PROOF.md` | `b137fcdbae9a0418d4b8f1b68a156d951cf0ecb00a20521c0c0a102d530107c3` |

The accompanying evidence mapping binds exact generator/input hashes separately. The original proof and data are retained unchanged; this review adds explanations and records rather than silently revising assessed source bytes.
