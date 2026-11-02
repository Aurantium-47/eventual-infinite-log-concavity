# Reproduction and evidence roles

## Freeze the assessed source first

Use a separate checkout, not a moving branch head:

```sh
git clone https://github.com/Aurantium-47/eventual-infinite-log-concavity.git trinomial-fixed
cd trinomial-fixed
git checkout --detach 68f4c920606ad239fbc3a8195bc0987b790f5905
python3 -m venv .venv
. .venv/bin/activate
python -m pip install python-flint==0.9.0
unset PYTHONOPTIMIZE
```

The official dependency version is pinned for reproduction. The historical full-run environment used Python 3.12.14 and python-flint 0.9.0; timings vary by hardware. Run the commands below from this repository root. Read `research/trinomial-all-n-ge10/certificate_package/README.md` for the complete certificate interface and finite/analytic stage commands.

## Full boundary regeneration versus saved-inequality replay

```sh
python research/trinomial-all-n-ge10/certificate_package/edge/regenerate.py --full --backend flint
```

This reconstructs shared jets from the defining recurrence, checks exact equality against every saved midpoint/radius/exponent/precision field, and checks all 1,929 strict Taylor signs. It is not the fast saved-inequality replay. The reviewed literal run finished with exit 0 in `29m39.084s`; final review inspected that run's evidence rather than repeating it.

Fast replay is useful for the closed-panel inequalities, coverage, bypasses, and joins, but **does not regenerate enclosure provenance**. Follow the distinct replay command in the fixed certificate README; do not substitute a replay PASS for a full regeneration.

The original two-queue reconstruction and the later literal sequential reconstruction are separate recorded runs. The latter supplements rather than rewrites the earlier run-method note.

## What the supplemental checks establish

| Check | Evidence role | Not established by that check alone |
|---|---|---|
| Source/input hashes and exact pair-set comparison | Binds the frozen program/data and proves 1,929+63 disjoint exact coverage | Mathematical soundness, or independent execution attestation |
| Full literal regeneration | Complete reconstruction through the original unchanged algorithm; exact field equality and strict signs | An independently implemented full generator |
| Explicit multinomial construction, four L maps, 708 distinct coefficients | Selected heterogeneous algorithm checks across five cases | Full 1,929-case independent reconstruction; independent arithmetic backend |
| Logarithmic-series construction, panel 7/node 22 | 87 exact coefficients, Bernstein controls, and independently evaluated two tails for one entire panel/node | All panels, bypasses, or the complete theorem |
| Independent bypass/assembly arithmetic | 63 whole-panel phase/variance premises, eight joins, endpoint/node ordering | The analytic two-saddle theorem without its mathematical proof |
| Finite/PF4 dependency audit | Complete 12,160 seed determinant recomputation, polynomial identities, prior finite evidence binding, selected interfaces | A fresh execution of all 3,994 finite exponents |
| Earlier full independent finite run | Every exponent 10…4003 reaches an invariant cone | Priority or formal proof-assistant certification |

The full independent finite evidence was bound by these SHA256 identities:

- Earlier independent finite script: `f07270c09dca3bae5a909a0890797931e471b28d8da124a0f9880e4c5e4067f9`.
- Complete earlier finite result: `728d141f55857067b3938c95796bd3d6774a1b19d2947c38024e86d47965900c`.
- Ordered 3,994-entry depths digest: `0f6607d35447274cf1f2fb2c4e4fe58e0ea6fe8f882a63d828ccdacb958b3e3c`.

## Interpretation of reproduction

A successful command is meaningful only together with the reviewed implication from its exact checks to the mathematical statement. The proofs of interval invariants, the two tail bounds, the real-parameter interface, root counting, and preservation remain necessary. Neither a PASS label nor a hash replaces those arguments.

Use assertions-enabled Python for all supplemental checks. Some historical supplements lack an optimization guard; never use `-O`, `-OO`, or a nonempty `PYTHONOPTIMIZE`. The recorded runs used the normal interpreter. Preserve historical receipt copies before rerunning scripts that overwrite their result JSONs, and distinguish original receipts from newly generated results.

The final review accepted the fixed mathematical dependencies without changing source constants or data. Editorial additions here explain that assessment. Human review and independent reproduction remain welcome; no claim of external refereeing, formalization, or exhaustive priority certification is made.
