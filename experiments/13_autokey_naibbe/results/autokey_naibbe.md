# 13 autokey Naibbe

## 1. validation

| text | h2 | hapax_ratio | edge_coupling | word_len | zipf | mattr500 |
|---|---|---|---|---|---|---|
| Greshko's file (Pliny) | 2.088 | 0.576 | 0.004 | 5.229 | -0.876 | 0.661 |
| ours, same units | 2.112 | 0.594 | 0.004 | 5.224 | -0.868 | 0.664 |

## 2. autokey strength (arbitrary chart)

VMS: edge 0.147, h2 2.15, hapax 0.69

| plaintext | autokey_p | h2 | hapax_ratio | edge_coupling | word_len | zipf | mattr500 |
|---|---|---|---|---|---|---|---|
| pliny | 0.000 | 2.103 | 0.595 | 0.006 | 5.262 | -0.865 | 0.666 |
| pliny | 0.250 | 2.097 | 0.608 | 0.025 | 5.274 | -0.875 | 0.663 |
| pliny | 0.500 | 2.097 | 0.576 | 0.081 | 5.224 | -0.864 | 0.659 |
| pliny | 0.650 | 2.093 | 0.605 | 0.152 | 5.237 | -0.873 | 0.655 |
| pliny | 0.800 | 2.095 | 0.589 | 0.220 | 5.206 | -0.872 | 0.652 |
| pliny | 1.000 | 2.084 | 0.582 | 0.371 | 5.218 | -0.868 | 0.647 |
| dante | 0.000 | 2.112 | 0.583 | 0.005 | 5.184 | -0.868 | 0.655 |
| dante | 0.250 | 2.099 | 0.596 | 0.026 | 5.223 | -0.863 | 0.648 |
| dante | 0.500 | 2.100 | 0.577 | 0.091 | 5.188 | -0.872 | 0.647 |
| dante | 0.650 | 2.101 | 0.581 | 0.129 | 5.163 | -0.867 | 0.640 |
| dante | 0.800 | 2.102 | 0.557 | 0.205 | 5.155 | -0.865 | 0.639 |
| dante | 1.000 | 2.098 | 0.567 | 0.323 | 5.144 | -0.873 | 0.633 |

## 3. shape of the coupling

Correlation of PMI(last glyph, next initial) between patterns:

- VMS odd lines vs even lines: 0.98
- 20 random charts vs VMS (held-out half): mean 0.00, best 0.16
- chart fitted on odd lines (0.47 there), simulated cipher vs even lines: Pliny 0.43, Dante 0.24
- fitted chart: {'y': 'beta2', 'n': 'beta3', 'l': 'beta3', 'r': 'beta3', 's': 'beta3', 'm': 'beta3', 'o': 'gamma1', 'd': 'beta2', 'other': 'beta3'}
- strongest VMS pairs: o|r 2.66, s|a 2.31, o|l 2.04, r|a 1.64, o|k 1.58, d|y 1.42, o|t 1.14, l|k 0.93, y|qo 0.83, d|a 0.76

## 4. VMS coupling by space type

certain spaces only: 0.166 bits (27608 boundaries); uncertain only: 0.411 (2984).

## 5. benchmark

| variant | plaintext | distance | core | edge | line_first | line_last | hapax | h2 | worst |
|---|---|---|---|---|---|---|---|---|---|
| VMS later pages | - | 1.056 | 0.182 | 0.177 | 0.142 | 0.085 | 0.703 | 2.135 | line_cohesion +3.6, repeat_rate +1.0, line_last_jsd -0.6 |
| VMS Currier B | - | 1.234 | 0.710 | 0.245 | 0.178 | 0.065 | 0.684 | 1.937 | line_last_jsd -2.8, line_first_jsd +2.6, edge_coupling +1.4 |
| + autokey p=.65, fitted chart + line-start q=0.5 | pliny | 3.854 | 0.609 | 0.077 | 0.150 | 0.004 | 0.625 | 2.190 | line_last_jsd -9.6, repeat_rate -8.6, line_cohesion -5.0 |
| + autokey p=.65, arbitrary chart + line-start q=0.5 | pliny | 3.920 | 0.494 | 0.143 | 0.131 | 0.002 | 0.632 | 2.151 | line_last_jsd -9.8, repeat_rate -8.7, line_cohesion -5.1 |
| + autokey p=.65, arbitrary chart + line-start q=0.5 | dante | 3.949 | 0.507 | 0.130 | 0.139 | 0.001 | 0.628 | 2.150 | line_last_jsd -9.9, repeat_rate -8.7, line_cohesion -5.3 |
| + autokey p=.65, fitted chart + line-start q=0.3 | pliny | 3.980 | 0.637 | 0.077 | 0.090 | 0.004 | 0.614 | 2.176 | line_last_jsd -9.6, repeat_rate -8.6, line_cohesion -5.0 |
| Naibbe (deck) + line-start q=0.5 | pliny | 4.034 | 0.799 | 0.007 | 0.130 | 0.003 | 0.655 | 2.157 | line_last_jsd -9.7, repeat_rate -9.1, line_cohesion -5.4 |
| Naibbe (deck) + line-start q=0.5 | dante | 4.090 | 0.814 | 0.006 | 0.141 | 0.002 | 0.637 | 2.157 | line_last_jsd -9.8, repeat_rate -9.2, line_cohesion -5.6 |
| + autokey p=.65, arbitrary chart + line-start q=0.3 | dante | 4.102 | 0.528 | 0.130 | 0.087 | 0.001 | 0.621 | 2.139 | line_last_jsd -9.9, repeat_rate -8.7, line_cohesion -5.4 |
| + autokey p=.65, fitted chart + line-start q=0.5 | dante | 4.105 | 0.700 | 0.062 | 0.177 | 0.003 | 0.608 | 2.188 | line_last_jsd -9.7, repeat_rate -9.2, line_cohesion -5.4 |
| + autokey p=.65, fitted chart + line-start q=0.3 | dante | 4.132 | 0.746 | 0.061 | 0.096 | 0.003 | 0.592 | 2.173 | line_last_jsd -9.7, repeat_rate -9.1, line_cohesion -5.5 |
| + autokey p=.65, arbitrary chart + line-start q=0.3 | pliny | 4.158 | 0.534 | 0.143 | 0.071 | 0.002 | 0.622 | 2.142 | line_last_jsd -9.8, repeat_rate -8.7, line_cohesion -5.2 |
| Naibbe (deck) + line-start q=0.3 | dante | 4.185 | 0.822 | 0.009 | 0.096 | 0.002 | 0.622 | 2.147 | line_last_jsd -9.8, repeat_rate -9.2, line_cohesion -5.6 |
| Naibbe (deck) + line-start q=0.3 | pliny | 4.205 | 0.802 | 0.006 | 0.079 | 0.003 | 0.648 | 2.146 | line_last_jsd -9.7, repeat_rate -9.1, line_cohesion -5.3 |
| + autokey p=.65, fitted chart | pliny | 4.717 | 0.780 | 0.076 | 0.002 | 0.004 | 0.579 | 2.136 | line_first_jsd -9.8, line_last_jsd -9.6, repeat_rate -8.4 |
| + autokey p=.65, arbitrary chart | pliny | 4.775 | 0.702 | 0.143 | 0.002 | 0.002 | 0.586 | 2.101 | line_first_jsd -9.8, line_last_jsd -9.8, repeat_rate -8.7 |
| + autokey p=.65, arbitrary chart | dante | 4.793 | 0.718 | 0.131 | 0.004 | 0.001 | 0.583 | 2.098 | line_last_jsd -9.9, line_first_jsd -9.7, repeat_rate -8.6 |
| Naibbe (deck) | pliny | 4.864 | 0.861 | 0.006 | 0.002 | 0.003 | 0.614 | 2.106 | line_first_jsd -9.9, line_last_jsd -9.7, repeat_rate -9.1 |
| + autokey p=.65, fitted chart | dante | 4.890 | 0.913 | 0.062 | 0.003 | 0.003 | 0.553 | 2.132 | line_first_jsd -9.8, line_last_jsd -9.7, repeat_rate -9.1 |
| Naibbe (deck) | dante | 4.926 | 0.923 | 0.008 | 0.003 | 0.002 | 0.583 | 2.106 | line_first_jsd -9.8, line_last_jsd -9.8, repeat_rate -9.2 |
