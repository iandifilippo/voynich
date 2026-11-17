# 36 assembled vs copied words, on held-out Currier B

Fitted on even pages, measured on odd pages (3 seeds).

## Vocabulary

| model | distinct per 1000 words | hapax share of types | tokens unseen in training half | top word share | top 20 share | lexicon gain (bits) |
|---|---|---|---|---|---|---|
| held-out VMS (target) | 247.656 | 0.672 | 0.173 | 0.020 | 0.234 | -0.246 |
| assemble 1 | 316.311 | 0.796 | 0.263 | 0.038 | 0.327 | -0.475 |
| assemble 2 | 262.177 | 0.700 | 0.179 | 0.030 | 0.254 | -0.362 |
| assemble 3 | 229.525 | 0.593 | 0.116 | 0.024 | 0.231 | -0.097 |
| assemble 2, no link | 260.898 | 0.701 | 0.177 | 0.030 | 0.256 | -0.368 |
| lexicon | 190.480 | 0.404 | 0.000 | 0.023 | 0.235 | 0.386 |
| assemble 2 + recall (exact 0.01, edited 0.1, last 5) | 290.622 | 0.712 | 0.214 | 0.028 | 0.237 | -0.365 |
| copying model | 214.440 | 0.615 | 0.489 | 0.026 | 0.263 | 0.023 |

## Sequence and edges

| model | adjacent exact repeats per 1000 | adjacent near repeats per 1000 | mean word length | words starting q | line-first starting q | para-first starting p/t/k/f | line-last ending m | doubletons on one page | benchmark distance | measures within 0.8-1.25x |
|---|---|---|---|---|---|---|---|---|---|---|
| held-out VMS (target) | 9.077 | 33.059 | 5.089 | 0.180 | 0.143 | 0.881 | 0.187 | 0.074 | 1.792 |  |
| assemble 1 | 7.707 | 32.168 | 5.106 | 0.183 | 0.158 | 0.847 | 0.175 | 0.034 | 2.344 | 8 |
| assemble 2 | 5.319 | 24.237 | 5.081 | 0.179 | 0.152 | 0.836 | 0.160 | 0.033 | 2.033 | 9 |
| assemble 3 | 4.618 | 22.103 | 5.099 | 0.180 | 0.158 | 0.849 | 0.149 | 0.033 | 2.447 | 8 |
| assemble 2, no link | 5.669 | 24.365 | 5.074 | 0.178 | 0.168 | 0.839 | 0.156 | 0.031 | 2.435 | 9 |
| lexicon | 4.268 | 21.148 | 5.096 | 0.178 | 0.168 | 0.079 | 0.024 | 0.029 | 4.300 | 5 |
| assemble 2 + recall (exact 0.01, edited 0.1, last 5) | 7.612 | 33.728 | 5.080 | 0.173 | 0.161 | 0.828 | 0.168 | 0.105 | 1.246 | 11 |
| copying model | 7.167 | 36.983 | 5.197 | 0.014 | 0.017 | 0.942 | 0.085 | 0.236 | 1.317 | 6 |
