# 60 scorecard (fitted on B's even sheets, measured on its odd sheets)

## Words

| model | distinct per 1000 | hapax share | new words vs training half | lexicon gain (bits) | mean signs per word | qo- words |
|---|---|---|---|---|---|---|
| Currier B, odd sheets | 248.948 | 0.677 | 0.183 | -0.263 | 4.377 | 0.195 |
| final generator (sigma 0.3, hold 1.0, chosen on even sheets) | 289.864 | 0.714 | 0.220 | -0.366 | 4.276 | 0.146 |
| final generator (sigma 0.9, hold 2.5, exp. 50) | 298.535 | 0.719 | 0.238 | -0.340 | 4.255 | 0.136 |
| copying model | 202.937 | 0.596 | 0.510 | 0.084 | 4.076 | 0.016 |
| Naibbe cipher of Pliny | 277.909 | 0.553 | 0.353 | 0.133 | 4.448 | 0.179 |

## Pages, lines and sequence

| model | sheet identity | gallows same line / other | beyond the boundary (bits) | recurring pairs excess | class sequence (bits) | within 0.8-1.25x of B |
|---|---|---|---|---|---|---|
| Currier B, odd sheets | 1.000 | 1.064 | 0.225 | 0.052 | 0.063 |  |
| final generator (sigma 0.3, hold 1.0, chosen on even sheets) | 0.850 | 1.044 | 0.072 | 0.023 | 0.013 | 6 |
| final generator (sigma 0.9, hold 2.5, exp. 50) | 1.000 | 1.054 | 0.043 | 0.034 | 0.029 | 5 |
| copying model | 0.950 | 1.036 | 0.207 | 0.028 | 0.002 | 6 |
| Naibbe cipher of Pliny | 0.150 | 0.996 | 0.082 | 0.018 | 0.024 | 5 |

## Choice of settings on the training sheets

| sigma | hold | within range on training sheets |
|---|---|---|
| 0.000 | 1.000 | 6 |
| 0.000 | 2.500 | 5 |
| 0.300 | 1.000 | 7 |
| 0.300 | 2.500 | 6 |
| 0.600 | 1.000 | 6 |
| 0.600 | 2.500 | 6 |
| 0.900 | 1.000 | 6 |
| 0.900 | 2.500 | 6 |
