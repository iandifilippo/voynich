# 36 assembled vs copied words, on held-out Currier A (ZL)

Fitted on even pages, measured on odd pages (3 seeds). Recall knobs as fitted on ZL Currier B.

## Vocabulary

| model | distinct per 1000 words | hapax share of types | tokens unseen in training half | top word share | top 20 share | lexicon gain (bits) |
|---|---|---|---|---|---|---|
| held-out VMS (target) | 348.250 | 0.709 | 0.241 | 0.050 | 0.238 | -0.366 |
| assemble 1 | 381.093 | 0.812 | 0.310 | 0.051 | 0.351 | -0.532 |
| assemble 2 | 340.025 | 0.707 | 0.224 | 0.040 | 0.263 | -0.412 |
| assemble 3 | 309.699 | 0.620 | 0.139 | 0.038 | 0.241 | -0.154 |
| assemble 2, no link | 338.490 | 0.705 | 0.217 | 0.038 | 0.263 | -0.404 |
| lexicon | 267.342 | 0.447 | 0.000 | 0.040 | 0.244 | 0.405 |
| assemble 2 + recall (exact 0.01, edited 0.1, last 5) | 365.071 | 0.719 | 0.256 | 0.035 | 0.246 | -0.398 |
| copying model | 202.156 | 0.593 | 0.470 | 0.060 | 0.391 | 0.241 |

## Sequence and edges

| model | adjacent exact repeats per 1000 | adjacent near repeats per 1000 | mean word length | words starting q | line-first starting q | para-first starting p/t/k/f | line-last ending m | doubletons on one page | benchmark distance | measures within 0.8-1.25x |
|---|---|---|---|---|---|---|---|---|---|---|
| held-out VMS (target) | 9.642 | 39.211 | 4.790 | 0.105 | 0.153 | 0.806 | 0.105 | 0.065 | 0.555 |  |
| assemble 1 | 9.856 | 35.355 | 4.772 | 0.096 | 0.137 | 0.898 | 0.124 | 0.030 | 1.428 | 10 |
| assemble 2 | 6.000 | 24.284 | 4.785 | 0.098 | 0.166 | 0.855 | 0.103 | 0.013 | 1.669 | 10 |
| assemble 3 | 6.214 | 26.141 | 4.788 | 0.094 | 0.150 | 0.861 | 0.110 | 0.025 | 1.706 | 8 |
| assemble 2, no link | 6.285 | 22.498 | 4.771 | 0.096 | 0.149 | 0.849 | 0.122 | 0.017 | 1.838 | 10 |
| lexicon | 5.357 | 18.070 | 4.791 | 0.090 | 0.092 | 0.096 | 0.039 | 0.020 | 4.225 | 3 |
| assemble 2 + recall (exact 0.01, edited 0.1, last 5) | 8.071 | 32.426 | 4.774 | 0.099 | 0.167 | 0.858 | 0.113 | 0.128 | 1.301 | 12 |
| copying model | 8.862 | 44.805 | 4.407 | 0.005 | 0.005 | 0.943 | 0.092 | 0.263 | 1.368 | 7 |
