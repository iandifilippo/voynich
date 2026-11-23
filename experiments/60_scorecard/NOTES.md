# 60 — The scorecard

## What I did

The account the series has arrived at, as one generator (two-sign chain with position tables, setting
per sheet, favoured gallows per line, echo of recent words), fitted on Currier B's even sheets and
filling its odd sheets. Eleven statistics from exps. 34-53, measured on the odd sheets and on the
generator's output for the same sheets, with the copying model (exp. 22) and the Naibbe cipher of Pliny
for comparison. The generator's two settings were chosen on the even sheets (sigma 0.3, hold 1).

## Result

| | B (odd sheets) | generator | copying model | Naibbe cipher |
|---|---|---|---|---|
| distinct words per 1000 | 249 | 290 | 203 | 278 |
| new words vs training half | 18% | 22% | 51% | 35% |
| lexicon gain (bits) | −0.26 | −0.37 | +0.08 | +0.13 |
| qo- words | 19.5% | 14.6% | 1.6% | 17.9% |
| sheet identity | 1.00 | 0.85 | 0.95 | 0.15 |
| beyond the boundary (bits) | 0.23 | 0.07 | **0.21** | 0.08 |
| recurring pairs excess | 0.052 | 0.023 | 0.028 | 0.018 |
| class sequence (bits) | 0.063 | 0.013 | 0.002 | 0.024 |
| within 0.8-1.25× of B (of 11) | – | 6 | 6 | 5 |

## So what

No model passes. The generator gets what words look like and how many there are; the copying model,
surprisingly, gets the link between neighbouring words that no habit of mine could make (exp. 50) and
gets the words wrong. That points at a hybrid, tried in exp. 61. The Naibbe cipher is worst on the
page-level statistics, as exp. 43 said.

The per-sheet setting (sigma) costs the generator q- words (19.5% → 14.6%): random weights on starts
pull it away from the real start distribution. A setting that moves along the directions exp. 41 found
(three components) instead of random weights would do better.
