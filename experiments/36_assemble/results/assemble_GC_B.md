# 36 assembled vs copied words, on held-out Currier B (GC)

Fitted on even pages, measured on odd pages (3 seeds). Recall knobs as fitted on ZL Currier B.

## Vocabulary

| model | distinct per 1000 words | hapax share of types | tokens unseen in training half | top word share | top 20 share | lexicon gain (bits) |
|---|---|---|---|---|---|---|
| held-out VMS (target) | 280.081 | 0.691 | 0.199 | 0.022 | 0.215 | -0.320 |
| assemble 1 | 328.970 | 0.802 | 0.272 | 0.036 | 0.323 | -0.487 |
| assemble 2 | 275.312 | 0.697 | 0.176 | 0.033 | 0.234 | -0.372 |
| assemble 3 | 239.729 | 0.585 | 0.105 | 0.023 | 0.220 | -0.103 |
| assemble 2, no link | 276.233 | 0.696 | 0.178 | 0.031 | 0.233 | -0.368 |
| lexicon | 208.699 | 0.415 | 0.000 | 0.024 | 0.221 | 0.333 |
| assemble 2 + recall (exact 0.01, edited 0.1, last 5) | 300.027 | 0.702 | 0.209 | 0.028 | 0.222 | -0.367 |
| copying model | 214.440 | 0.615 | 0.984 | 0.026 | 0.263 | 0.023 |

## Sequence and edges

| model | adjacent exact repeats per 1000 | adjacent near repeats per 1000 | mean word length | words starting q | line-first starting q | para-first starting p/t/k/f | line-last ending m | doubletons on one page | benchmark distance | measures within 0.8-1.25x |
|---|---|---|---|---|---|---|---|---|---|---|
| held-out VMS (target) | 6.705 | 43.041 | 3.962 | 0.000 | 0.000 | 0.262 | 0.068 | 0.071 | 2.976 |  |
| assemble 1 | 6.856 | 43.252 | 3.921 | 0.000 | 0.000 | 0.297 | 0.058 | 0.035 | 2.482 | 7 |
| assemble 2 | 4.259 | 33.496 | 3.927 | 0.000 | 0.000 | 0.277 | 0.062 | 0.034 | 3.178 | 8 |
| assemble 3 | 4.380 | 32.016 | 3.913 | 0.000 | 0.000 | 0.276 | 0.067 | 0.036 | 3.314 | 7 |
| assemble 2, no link | 4.953 | 30.869 | 3.931 | 0.000 | 0.000 | 0.305 | 0.066 | 0.029 | 2.998 | 8 |
| lexicon | 3.594 | 27.969 | 3.926 | 0.000 | 0.000 | 0.029 | 0.093 | 0.025 | 4.244 | 3 |
| assemble 2 + recall (exact 0.01, edited 0.1, last 5) | 6.585 | 51.559 | 3.915 | 0.000 | 0.000 | 0.271 | 0.075 | 0.101 | 2.495 | 10 |
| copying model | 7.167 | 36.983 | 5.197 | 0.014 | 0.017 | 0.942 | 0.085 | 0.236 | 1.317 | 5 |
