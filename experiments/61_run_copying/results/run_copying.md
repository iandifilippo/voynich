# 61 assembled words with copied runs, scored on B's odd sheets

## Choice of follow_p on the even sheets

| follow_p | within range on training sheets | beyond the boundary | recurring pairs excess | distinct per 1000 |
|---|---|---|---|---|
| 0.000 | 6 | 0.004 | 0.029 | 282.836 |
| 0.050 | 7 | 0.109 | 0.025 | 286.060 |
| 0.100 | 7 | 0.185 | 0.021 | 282.836 |
| 0.200 | 6 | 0.366 | 0.021 | 273.614 |
| 0.300 | 6 | 0.521 | 0.018 | 265.198 |
| 0.450 | 6 | 0.935 | 0.016 | 251.589 |

## Words

| model | distinct per 1000 | hapax share | new words vs training half | lexicon gain (bits) | mean signs per word | qo- words |
|---|---|---|---|---|---|---|
| Currier B, odd sheets | 248.948 | 0.677 | 0.183 | -0.263 | 4.377 | 0.195 |
| assembled words, no run copying | 283.802 | 0.700 | 0.215 | -0.364 | 4.274 | 0.159 |
| assembled words + run copying (follow_p 0.05, chosen on even sheets) | 280.603 | 0.689 | 0.214 | -0.323 | 4.289 | 0.163 |
| copying model (exp. 22) | 202.937 | 0.596 | 0.510 | 0.084 | 4.076 | 0.016 |

## Pages, lines and sequence

| model | sheet identity | gallows same line / other | beyond the boundary (bits) | recurring pairs excess | class sequence (bits) | within 0.8-1.25x of B |
|---|---|---|---|---|---|---|
| Currier B, odd sheets | 1.000 | 1.064 | 0.231 | 0.053 | 0.063 |  |
| assembled words, no run copying | 0.650 | 1.039 | 0.040 | 0.020 | 0.012 | 6 |
| assembled words + run copying (follow_p 0.05, chosen on even sheets) | 0.650 | 1.011 | 0.051 | 0.015 | 0.011 | 7 |
| copying model (exp. 22) | 0.950 | 1.036 | 0.204 | 0.028 | 0.002 | 6 |
