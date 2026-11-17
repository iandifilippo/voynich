# 36 assembled vs copied words, on held-out Currier B

Fitted on even pages, measured on odd pages (3 seeds).

## Vocabulary

| model | distinct per 1000 words | hapax share of types | tokens unseen in training half | top word share | top 20 share | lexicon gain (bits) |
|---|---|---|---|---|---|---|
| held-out VMS (target) | 247.656 | 0.672 | 0.173 | 0.020 | 0.234 | -0.246 |
| assemble 1 | 316.539 | 0.802 | 0.262 | 0.039 | 0.331 | -0.475 |
| assemble 2 | 259.335 | 0.704 | 0.176 | 0.031 | 0.255 | -0.364 |
| assemble 3 | 230.946 | 0.608 | 0.115 | 0.025 | 0.231 | -0.122 |
| assemble 2, no link | 262.120 | 0.705 | 0.176 | 0.030 | 0.253 | -0.372 |
| lexicon | 190.480 | 0.404 | 0.000 | 0.023 | 0.235 | 0.386 |
| copying model | 214.440 | 0.615 | 0.489 | 0.026 | 0.263 | 0.023 |

## Sequence and edges

| model | adjacent exact repeats per 1000 | adjacent near repeats per 1000 | mean word length | words starting q | line-first starting q | para-first starting p/t/k/f | line-last ending m | doubletons on one page | benchmark distance | measures within 0.8-1.25x |
|---|---|---|---|---|---|---|---|---|---|---|
| held-out VMS (target) | 9.077 | 33.059 | 5.089 | 0.180 | 0.143 | 0.881 | 0.187 | 0.074 | 1.792 |  |
| assemble 1 | 7.357 | 32.741 | 5.082 | 0.181 | 0.156 | 0.855 | 0.174 | 0.033 | 2.054 | 8 |
| assemble 2 | 5.223 | 23.122 | 5.089 | 0.180 | 0.155 | 0.832 | 0.180 | 0.038 | 2.467 | 9 |
| assemble 3 | 4.650 | 21.307 | 5.085 | 0.177 | 0.157 | 0.840 | 0.157 | 0.024 | 2.357 | 9 |
| assemble 2, no link | 5.733 | 24.014 | 5.087 | 0.178 | 0.156 | 0.856 | 0.170 | 0.029 | 2.024 | 9 |
| lexicon | 4.268 | 21.148 | 5.096 | 0.178 | 0.168 | 0.079 | 0.024 | 0.029 | 4.300 | 5 |
| copying model | 7.167 | 36.983 | 5.197 | 0.014 | 0.017 | 0.942 | 0.085 | 0.236 | 1.317 | 6 |
