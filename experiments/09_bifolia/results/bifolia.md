# 09 bifolia

101 leaves with 60+ words. Pairs compared only within a quire and only when both leaves share scribe and illustration type.

- conjoint pairs (same bifolium): 44
- other pairs: 182
- mean cosine, conjoint minus other: **+0.022** (random re-pairing: -0.017, p = 0.0054)

## other similarity measures (2000 re-pairings each)

| measure | diff | null_mean | p | quires_conjoint_higher |
|---|---|---|---|---|
| cosine | 0.022 | -0.017 | 0.002 | 9/10 |
| tfidf_cosine | -0.029 | -0.028 | 0.534 | 8/10 |
| jaccard_no_top50 | -0.007 | -0.008 | 0.432 | 7/10 |

## by leaf distance in the current order

| leaf_distance | conjoint_n | conjoint_cos | other_n | other_cos |
|---|---|---|---|---|
| 1 | 14 | 0.558 | 41 | 0.547 |
| 2 | 1 | 0.626 | 45 | 0.521 |
| 3 | 11 | 0.531 | 29 | 0.522 |
| 4 | 1 | 0.630 | 25 | 0.533 |
| 5 | 8 | 0.597 | 17 | 0.565 |
| 6 | 1 | 0.542 | 13 | 0.642 |
| 7 | 6 | 0.553 | 5 | 0.679 |
| 9 | 1 | 0.743 | 2 | 0.410 |

## by quire

| quire | leaves | conjoint_n | conjoint_cos | other_cos | adjacent_nonconjoint_cos |
|---|---|---|---|---|---|
| A | 8 | 3 | 0.514 | 0.459 | 0.407 |
| B | 7 | 3 | 0.599 | 0.539 | 0.544 |
| C | 8 | 4 | 0.549 | 0.420 | 0.479 |
| D | 8 | 4 | 0.521 | 0.450 | 0.406 |
| E | 8 | 4 | 0.602 | 0.571 | 0.557 |
| F | 8 | 4 | 0.478 | 0.400 | None |
| G | 8 | 4 | 0.464 | 0.391 | 0.357 |
| M | 10 | 4 | 0.801 | 0.712 | 0.714 |
| S | 4 | 2 | 0.527 | 0.535 | 0.533 |
| T | 12 | 5 | 0.699 | 0.604 | 0.642 |
