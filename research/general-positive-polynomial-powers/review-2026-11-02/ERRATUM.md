# Local wording correction: Lemma 1

Applies only to the proof of Lemma 1, §2 of [the fixed manuscript](https://github.com/Aurantium-47/eventual-infinite-log-concavity/blob/68f4c920606ad239fbc3a8195bc0987b790f5905/paper/proof.tex).

The first-failure argument must distinguish **input ratio layers through r−2** from the **output center bound at r−1**. Positivity of all coefficient layers through r−1 implies all ratios lie in [0,1) only through r−2, not necessarily at r−1.

Replace the relevant justification by:

> All entire coefficient layers before r are positive, so all ratios in layers 0 through r−2 lie in [0,1). These are precisely the input layers required to propagate (3) from T(k) to the center bound q_{r−1}(k) ≤ 1/3. If T(k) = r−1, the certificate already gives that bound and no propagation is needed.

The next displayed positivity conclusion is unchanged. This repairs the local wording, not the theorem statement, stopping criterion, or proof strategy. The source TeX and PDF have not been edited by this review.
