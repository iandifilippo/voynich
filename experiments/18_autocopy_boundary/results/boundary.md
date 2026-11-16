# 18 self-citation + boundary preference

Fitted chart (from odd lines): -y: d k l p q qo r s t; -n: c ch o sh y; -l: ch d k s sh t; -r: a ch o sh y; -s: a o sh; -m: ch o; -o: d k l r; -d: qo

| model | p | distance | core | edge | pattern_r | hapax | h2 | words_per_line | worst |
|---|---|---|---|---|---|---|---|---|---|
| VMS even lines vs odd | None |  |  | None | 0.982 |  |  | 8.441 |  |
| fitted chart | 0.000 | 2.436 | 0.976 | 0.013 | 0.092 | 0.542 | 2.217 | 8.139 | line_last_jsd -7.4, line_first_jsd -2.9, repeat_rate -2.0 |
| fitted chart | 0.500 | 2.413 | 0.835 | 0.057 | 0.666 | 0.549 | 2.232 | 8.303 | line_last_jsd -6.6, line_first_jsd -3.7, repeat_rate -3.0 |
| fitted chart | 0.650 | 2.424 | 0.706 | 0.115 | 0.701 | 0.551 | 2.187 | 8.143 | line_last_jsd -7.0, repeat_rate -3.3, line_first_jsd -2.9 |
| fitted chart | 0.800 | 2.445 | 0.790 | 0.227 | 0.726 | 0.553 | 2.159 | 8.367 | line_last_jsd -6.8, repeat_rate -3.4, line_first_jsd -2.9 |
| fitted chart | 0.950 | 2.973 | 1.852 | 0.508 | 0.554 | 0.546 | 2.117 | 7.869 | line_last_jsd -7.2, edge_coupling +5.1, repeat_rate -4.4 |
| random charts (mean of 5) | 0.800 | 2.476 | 0.736 | 0.176 | 0.020 | 0.549 | 2.143 | 8.164 | line_last_jsd -8.0, repeat_rate -4.7, line_first_jsd -4.3 |
| random charts (mean of 5) | 0.950 | 2.588 | 1.406 | 0.401 | -0.026 | 0.551 | 2.124 | 8.059 | line_last_jsd -7.4, repeat_rate -4.4, edge_coupling +3.7 |

`pattern_r`: correlation of the (final glyph, next word start) PMI table with the VMS's even lines. Generator in B settings, 3 seeds per row.
