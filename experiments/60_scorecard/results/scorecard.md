# 60 scorecard (fitted on B's even sheets, measured on its odd sheets)

## Words

| model | distinct per 1000 | hapax share | new words vs training half | lexicon gain (bits) | mean signs per word | qo- words |
|---|---|---|---|---|---|---|
| Currier B, odd sheets | 248.948 | 0.677 | 0.183 | -0.263 | 4.377 | 0.195 |
| final generator | 309.564 | 0.731 | 0.239 | -0.404 | 4.351 | 0.112 |
| copying model | 202.937 | 0.596 | 0.510 | 0.084 | 4.076 | 0.016 |
| Naibbe cipher of Pliny | 277.909 | 0.553 | 0.353 | 0.133 | 4.448 | 0.179 |

## Pages, lines and sequence

| model | sheet identity | gallows same line / other | beyond the boundary (bits) | recurring pairs excess | class sequence (bits) | within 0.8-1.25x of B |
|---|---|---|---|---|---|---|
| Currier B, odd sheets | 1.000 | 1.064 | 0.244 | 0.053 | 0.063 |  |
| final generator | 1.000 | 1.078 | 0.001 | 0.010 | 0.002 | 5 |
| copying model | 0.950 | 1.036 | 0.204 | 0.029 | 0.002 | 6 |
| Naibbe cipher of Pliny | 0.150 | 0.996 | 0.079 | 0.017 | 0.024 | 5 |
