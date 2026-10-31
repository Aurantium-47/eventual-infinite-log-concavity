# Exact arithmetic acceleration for a mathematical certificate

A small, reproducible AI-for-Math engineering case study: replace Python's
byte-packed integer convolution with the **released python-flint 0.9.0** backend,
while leaving the fixed-point certificate arithmetic and error bounds unchanged.

One observed single-node run fell from **283.533 s to 13.777 s (20.58×)**.
Every final integer midpoint, common error radius, and nonperformance receipt
field agreed exactly. This is one workload and one observed run per backend,
not a statistical speedup estimate or a universal multiplication algorithm.

**Mathematical scope:** node 200, panel 0, K=600, degree=360, precision=2048.
The sharper trinomial infinite-log-concavity target for all exponents n≥10
remains unresolved. This benchmark does not prove that target or certify a
whole chain. It does not change the scope of the parent project's theorems.

## Reproduce

Use CPython 3.12 on Linux x86-64 for the recorded wheel. A clean virtual
environment keeps this release separate from development builds:

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install --index-url https://pypi.org/simple --only-binary=:all: \
  --require-hashes -r requirements-linux-x86_64.txt
python -m unittest -v test_exact
python run.py --backend reference --output results/reference
python run.py --backend flint --output results/flint
python compare.py results/reference results/flint
```

Run from this directory. The reference command takes roughly five minutes in
the observed environment; runtime depends on hardware and other jobs. Neither
command is launched by import or by the fast tests. Output directories must be
empty. Do not disable Python assertions. The reference run requires only the
standard library. On other supported platforms, `pip install -r requirements.txt`
pins the release, but selects a different wheel: record its filename and hash
rather than claiming to reproduce the Linux wheel exactly.

To compare either run with the preserved final integer fixture:

```sh
python - <<'PY'
from compare import compare
compare('evidence/expected_final_jet.json', 'evidence/reference_receipt.json',
        'results/flint/final_jet.json', 'results/flint/receipt.json')
print('PASS: recorded exact output reproduced')
PY
```

## What changes, and why exact agreement matters

`backends.py` converts signed Python integer coefficient lists to `fmpz_poly`,
uses `mul_low` for the retained low coefficients, and converts every coefficient
back to a Python integer, explicitly retaining zero padding. No floating-point
approximation is introduced. The reference uses signed Kronecker/byte packing
and Python integer multiplication; it is not a naive quadratic baseline.

The jet enclosure is `(midpoint[i] ± radius) / 2**P`. A faster result with a
slightly different sign, radius, truncation rule, or error bound would not be
the same certificate. The comparator therefore checks **all final integers and
all nonperformance receipt fields**, ignoring only elapsed time and peak RSS.
Comparison is recursively type-strict: JSON booleans, integers and floats are
not interchangeable. Duplicate object keys and NaN/Infinity are rejected.
It does not merely compare a positive/negative flag. Fast tests cover signed,
zero, truncated and large-integer products plus deliberate comparator failures.

Both backends share the same certificate implementation. Exact replay checks
the arithmetic substitution, not an independent reimplementation or a complete
proof audit. The supplied rational node data are deterministic candidates;
reproducing this one-node certificate does not certify other nodes or joins.

See [BENCHMARK.md](BENCHMARK.md) for evidence and timing limitations and
[PROVENANCE.md](PROVENANCE.md) for dependency provenance and attribution.

## 中文简介

这是一个 AI 辅助数学研究中的精确计算工程案例：把证书程序的整数多项式卷积
接入已发布的 **python-flint 0.9.0 / FLINT**，保留原有定点区间运算和误差界。
在一个固定节点任务的单次实测中，运行时间从 **283.533 秒降至 13.777 秒，约
20.58 倍加速**；最终所有整数中点、公共误差半径及非性能回执字段完全一致。

这里公开的是后端集成、可复现实验和逐项一致性检查。加速来自成熟的 FLINT
精确算术实现；不宣称发明通用乘法算法，也不宣称解决了三项式锐界猜想。
更强的全部 n≥10 目标仍未完成，单节点证书不能替代完整证明链。
