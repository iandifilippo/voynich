# 63 the boundary link on two signs

## Choice on the even sheets

| follow_p | within range on training sheets | rhythm |
|---|---|---|
| 0.000 | 8 | 1.545 |
| 0.050 | 7 | 1.419 |
| 0.100 | 7 | 1.453 |
| 0.150 | 5 | 1.544 |

## Words

| model | distinct per 1000 | hapax share | new words vs training half | lexicon gain (bits) | mean signs per word | qo- words |
|---|---|---|---|---|---|---|
| Currier B, odd sheets | 248.948 | 0.677 | 0.183 | -0.263 | 4.377 | 0.195 |
| link on 1 sign, run copying 0.05 (exp. 61) | 283.213 | 0.700 | 0.220 | -0.340 | 4.217 | 0.125 |
| link on 2 signs, run copying 0.0 (chosen on even sheets) | 290.958 | 0.709 | 0.220 | -0.364 | 4.250 | 0.130 |

## Pages, lines and sequence

| model | sheet identity | gallows same line / other | beyond the boundary (bits) | recurring pairs excess | class sequence (bits) | rhythm (ch/sh-y -> qo) | within 0.8-1.25x of B |
|---|---|---|---|---|---|---|---|
| Currier B, odd sheets | 1.000 | 1.064 | 0.232 | 0.053 | 0.063 | 1.960 |  |
| link on 1 sign, run copying 0.05 (exp. 61) | 0.800 | 1.018 | 0.054 | 0.018 | -0.000 | 1.564 | 6 |
| link on 2 signs, run copying 0.0 (chosen on even sheets) | 0.600 | 1.052 | 0.129 | 0.029 | 0.020 | 1.606 | 5 |
