# 52 — Is the residual a grammar?

## What I think

If the residual comes from one underlying system (a grammar, or a code applied to a sequence),
the same kinds of word should follow each other everywhere: in A and B, and in both halves of B.

## What I did

Words of 3+ signs put in coarse classes (start: *qo, o, ch/sh, d, a, y, s*, other; ending: *y, n,
l, r, m*, other). For each class transition, observed over expected, expected from the permutation
that keeps the boundary glyphs and the sheet. Correlation of the log ratios between texts. Then a
predictive version: learn the ratios on one part, score the other part against a no-structure
baseline.

## Result

| comparison | transitions | correlation |
|---|---|---|
| B (ZL) vs B (IT), same pages | 339 | **0.83** |
| B, half the sheets vs the other half | 153 | −0.02 |
| A, half vs half | 46 | 0.07 |
| A vs B | 151 | −0.03 |
| B vs the habits generator | 283 | −0.04 |

Held-out gain from the learned transitions, bits per pair: B 0.003 (across sheets) / 0.002
(across lines) / 0.004 (inside each sheet); A 0.001 / −0.004 / −0.001; generator 0.004 / 0.003 /
0.002.

## So what

Two transcribers agree on the pattern (0.83), so it's in the manuscript, not in a reading of it.
But it doesn't carry from one half of B to the other, nor from odd lines to even lines of the same
sheet, and it doesn't predict anything the generator's doesn't. At the level of kinds of word,
there is no grammar: no transition is favoured consistently across the book. Whatever makes the
in-sample residual is finer-grained than these classes. Exp. 53 looks at exact word pairs.
