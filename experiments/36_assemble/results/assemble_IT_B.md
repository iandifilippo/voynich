# 36 assembled vs copied words, on held-out Currier B (IT)

Fitted on even pages, measured on odd pages (3 seeds). Recall knobs as fitted on ZL Currier B.

## Vocabulary

| model | distinct per 1000 words | hapax share of types | tokens unseen in training half | top word share | top 20 share | lexicon gain (bits) |
|---|---|---|---|---|---|---|
| held-out VMS (target) | 260.445 | 0.675 | 0.185 | 0.022 | 0.231 | -0.259 |
| assemble 1 | 320.334 | 0.800 | 0.274 | 0.037 | 0.322 | -0.486 |
| assemble 2 | 258.900 | 0.700 | 0.179 | 0.033 | 0.260 | -0.363 |
| assemble 3 | 223.944 | 0.584 | 0.111 | 0.023 | 0.232 | -0.057 |
| assemble 2, no link | 255.307 | 0.696 | 0.178 | 0.033 | 0.259 | -0.352 |
| lexicon | 184.608 | 0.374 | 0.000 | 0.021 | 0.233 | 0.448 |
| assemble 2 + recall (exact 0.01, edited 0.1, last 5) | 289.617 | 0.712 | 0.221 | 0.030 | 0.242 | -0.369 |
| copying model | 213.842 | 0.612 | 0.495 | 0.026 | 0.263 | 0.022 |

## Sequence and edges

| model | adjacent exact repeats per 1000 | adjacent near repeats per 1000 | mean word length | words starting q | line-first starting q | para-first starting p/t/k/f | line-last ending m | doubletons on one page | benchmark distance | measures within 0.8-1.25x |
|---|---|---|---|---|---|---|---|---|---|---|
| held-out VMS (target) | 8.679 | 31.698 | 5.147 | 0.178 | 0.141 | 0.830 | 0.181 | 0.082 | 1.710 |  |
| assemble 1 | 5.943 | 28.836 | 5.170 | 0.186 | 0.158 | 0.867 | 0.198 | 0.037 | 2.627 | 8 |
| assemble 2 | 5.377 | 22.013 | 5.146 | 0.187 | 0.150 | 0.863 | 0.201 | 0.032 | 2.432 | 9 |
| assemble 3 | 4.245 | 20.377 | 5.165 | 0.190 | 0.173 | 0.864 | 0.187 | 0.028 | 2.722 | 9 |
| assemble 2, no link | 5.535 | 22.421 | 5.141 | 0.185 | 0.165 | 0.872 | 0.187 | 0.024 | 2.614 | 9 |
| lexicon | 3.899 | 19.245 | 5.179 | 0.188 | 0.184 | 0.076 | 0.029 | 0.033 | 4.439 | 4 |
| assemble 2 + recall (exact 0.01, edited 0.1, last 5) | 8.365 | 31.855 | 5.162 | 0.186 | 0.162 | 0.870 | 0.201 | 0.110 | 1.402 | 11 |
| copying model | 7.197 | 37.010 | 5.197 | 0.014 | 0.017 | 0.942 | 0.086 | 0.237 | 1.296 | 8 |
