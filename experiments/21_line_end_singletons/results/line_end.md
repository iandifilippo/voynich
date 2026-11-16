# 21 line-end rule in the copying model

| model | q | distance | core | hapax | single_first | single_middle | single_last | line_last_jsd | cohesion | edge | worst |
|---|---|---|---|---|---|---|---|---|---|---|---|
| VMS Currier B | None | 1.234 | 0.710 | 0.684 | 0.265 | 0.129 | 0.240 | 0.065 | 1.951 | 0.245 |  |
| copying + boundary habit + line-end rule | 0.000 | 2.388 | 0.694 | 0.553 | 0.273 | 0.111 | 0.105 | 0.028 | 1.948 | 0.116 | line_last_jsd -6.9, repeat_rate -3.5, line_first_jsd -2.8 |
| copying + boundary habit + line-end rule | 0.200 | 2.317 | 0.702 | 0.560 | 0.257 | 0.112 | 0.166 | 0.036 | 2.189 | 0.110 | line_last_jsd -6.1, repeat_rate -3.6, line_first_jsd -3.2 |
| copying + boundary habit + line-end rule | 0.400 | 2.061 | 0.694 | 0.570 | 0.282 | 0.121 | 0.217 | 0.048 | 2.332 | 0.118 | line_last_jsd -4.6, repeat_rate -3.7, line_first_jsd -2.7 |
| copying + boundary habit + line-end rule | 0.600 | 1.893 | 0.677 | 0.590 | 0.311 | 0.131 | 0.273 | 0.082 | 2.336 | 0.111 | repeat_rate -4.4, line_first_jsd -2.9, line_cohesion +1.7 |
| copying + boundary habit + line-end rule | 0.800 | 1.863 | 0.704 | 0.598 | 0.310 | 0.130 | 0.327 | 0.095 | 2.199 | 0.099 | repeat_rate -3.7, line_first_jsd -2.3, hapax_ratio -1.2 |

`single_*`: share of words in that line position that are singletons (first 10 000 words). 4 seeds per row.

## frequency spectrum (first 10 000 words)

| text | types 1 | types 2 | types 3-5 | types 6-20 | types 21+ | tokens 1 | tokens 2 | tokens 3-5 | tokens 6-20 | tokens 21+ |
|---|---|---|---|---|---|---|---|---|---|---|
| VMS Currier B | 1575 | 240 | 223 | 177 | 87 | 0.158 | 0.048 | 0.083 | 0.177 | 0.535 |
| VMS Currier A | 2061 | 379 | 272 | 184 | 79 | 0.206 | 0.076 | 0.100 | 0.189 | 0.429 |
| model, q = 0.5 (mean of 4) | 1680.750 | 405 | 401.750 | 296.250 | 57.750 | 0.168 | 0.081 | 0.150 | 0.297 | 0.304 |

`types n`: number of word types occurring n times; `tokens n`: share of the text they cover.
