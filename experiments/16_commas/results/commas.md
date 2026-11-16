# 16 what ',' means

## size

| reading | subset | words | types | mean_len |
|---|---|---|---|---|
| split | all | 34863 | 7022 | 4.989 |
| split | A | 11231 | 3217 | 4.791 |
| split | B | 23084 | 4785 | 5.089 |
| smart | all | 34065 | 7013 | 5.106 |
| smart | A | 11000 | 3227 | 4.892 |
| smart | B | 22521 | 4796 | 5.216 |
| join | all | 32403 | 7984 | 5.365 |
| join | A | 10424 | 3543 | 5.158 |
| join | B | 21451 | 5405 | 5.475 |

## metrics (all paragraph text), with rank among 18 historical texts

| metric | split | split_rank | smart | smart_rank | join | join_rank | z_smart | z_join |
|---|---|---|---|---|---|---|---|---|
| hapax_ratio | 0.686 | 10/18 | 0.679 | 9/18 | 0.720 | 14/18 | -0.095 | 0.477 |
| mattr500 | 0.618 | 13/18 | 0.633 | 13/18 | 0.663 | 15/18 | 0.097 | 0.292 |
| word_len | 4.714 | 11/18 | 4.835 | 11/18 | 5.093 | 13/18 | 0.116 | 0.366 |
| word_len_sd | 1.756 | 3/18 | 1.705 | 3/18 | 1.817 | 3/18 | -0.047 | 0.057 |
| h1 | 3.842 | 1/18 | 3.848 | 1/18 | 3.864 | 1/18 | 0.015 | 0.058 |
| h2 | 2.154 | 0/18 | 2.154 | 0/18 | 2.180 | 0/18 | -0.000 | 0.121 |
| zipf | -0.996 | 7/18 | -0.952 | 8/18 | -0.932 | 8/18 | 0.314 | 0.450 |
| edge_coupling | 0.147 | 15/18 | 0.121 | 11/18 | 0.108 | 9/18 | -0.372 | -0.557 |
| word_mi | -0.008 | 0/18 | -0.010 | 0/18 | -0.015 | 0/18 | -0.041 | -0.217 |
| repeat_rate | 9.000 | 17/18 | 8.700 | 17/18 | 8.000 | 17/18 | -0.333 | -1.111 |
| line_first_jsd | 0.141 | 18/18 | 0.140 | 18/18 | 0.142 | 18/18 | -0.050 | 0.107 |
| line_last_jsd | 0.090 | 18/18 | 0.089 | 18/18 | 0.086 | 18/18 | -0.089 | -0.479 |
| line_cohesion | 1.959 | 17/18 | 1.936 | 17/18 | 2.022 | 17/18 | -0.105 | 0.289 |

`z_*` = shift from the split reading in benchmark units (MAD of the historical texts).

## how big is that shift

| pair | distance | core |
|---|---|---|
| split vs smart (all) | 0.177 | 0.174 |
| split vs join (all) | 0.446 | 0.338 |
| A vs B (split) | 1.309 | 0.759 |
| A vs B (smart) | 1.169 | 0.759 |
| A vs B (join) | 1.137 | 0.762 |

## Greshko's Naibbe ciphertext against each reading

| reading | distance | core | worst |
|---|---|---|---|
| split | 4.536 | 0.940 | edge_coupling -2.1, hapax_ratio -1.5, zipf +0.8 |
| smart | 4.437 | 0.797 | edge_coupling -1.7, hapax_ratio -1.4, word_mi +0.5 |
| join | 4.335 | 0.890 | hapax_ratio -2.0, edge_coupling -1.5, word_mi +0.7 |
