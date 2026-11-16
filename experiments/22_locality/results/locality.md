# 22 locality

Lift = how much more often than its base rate a word turns up k lines after a line that has it (first 10 000 words of each text).

## core 21+ occurrences

| text | types | share_of_text | same line | lag 1 | lag 2 | lag 5 | lag 10 | lag 25 | lag 100 |
|---|---|---|---|---|---|---|---|---|---|
| VMS Currier B | 87 | 0.535 | 0.944 | 1.732 | 1.614 | 1.355 | 1.345 | 1.164 | 1.039 |
| VMS Currier A | 79 | 0.429 | 0.882 | 1.523 | 1.454 | 1.458 | 1.254 | 1.124 | 0.981 |
| copying model | 57.750 | 0.304 | 0.785 | 1.857 | 1.543 | 1.410 | 1.199 | 1.087 | 0.952 |
| copying model, 60% of sources from anywhere | 68.250 | 0.497 | 0.507 | 1.144 | 1.052 | 1.057 | 1.025 | 1.004 | 0.979 |
| copying model, prefer common c = 0.3 | 79.750 | 0.396 | 0.910 | 2.222 | 1.836 | 1.565 | 1.353 | 1.117 | 0.893 |
| copying model, prefer common c = 0.5 | 85.750 | 0.513 | 0.801 | 1.804 | 1.626 | 1.399 | 1.229 | 1.069 | 0.965 |
| copying model, prefer common c = 0.7 | 87.250 | 0.640 | 0.746 | 1.730 | 1.516 | 1.412 | 1.243 | 1.088 | 1.006 |
| Latin (Aix) | 44 | 0.259 | 0.333 | 1.000 | 1.078 | 0.983 | 0.979 | 1.077 | 0.983 |
| Italian (Rettorica) | 74 | 0.474 | 0.487 | 1.367 | 1.280 | 1.180 | 1.104 | 1.088 | 1.021 |
| Naibbe (Pliny) | 73 | 0.429 | 0.483 | 1.008 | 1.024 | 0.997 | 0.980 | 0.959 | 0.990 |

## middle 6-20 occurrences

| text | types | share_of_text | same line | lag 1 | lag 2 | lag 5 | lag 10 | lag 25 | lag 100 |
|---|---|---|---|---|---|---|---|---|---|
| VMS Currier B | 177 | 0.177 | 1.980 | 1.869 | 2.495 | 2.275 | 1.370 | 1.443 | 1.425 |
| VMS Currier A | 184 | 0.189 | 2.261 | 3.124 | 2.311 | 2.461 | 1.998 | 1.119 | 1.182 |
| copying model | 296.250 | 0.297 | 3.211 | 8.110 | 5.227 | 3.872 | 2.765 | 1.377 | 0.884 |
| copying model, 60% of sources from anywhere | 198.250 | 0.191 | 1.137 | 2.939 | 1.880 | 1.378 | 1.181 | 1.031 | 0.800 |
| copying model, prefer common c = 0.3 | 267.250 | 0.276 | 3.182 | 7.425 | 5.178 | 3.352 | 2.507 | 1.244 | 0.990 |
| copying model, prefer common c = 0.5 | 209.250 | 0.213 | 2.761 | 6.775 | 4.924 | 3.424 | 2.273 | 1.174 | 0.962 |
| copying model, prefer common c = 0.7 | 153.250 | 0.163 | 2.841 | 6.921 | 4.489 | 2.920 | 2.335 | 1.037 | 0.811 |
| Latin (Aix) | 214 | 0.202 | 0.762 | 1.784 | 2.991 | 2.211 | 1.219 | 1.181 | 0.640 |
| Italian (Rettorica) | 175 | 0.182 | 1.014 | 4.455 | 4.455 | 2.492 | 1.634 | 2.224 | 0.888 |
| Naibbe (Pliny) | 136 | 0.122 | 0.373 | 1.137 | 0.965 | 0.895 | 0.936 | 0.760 | 0.746 |

## low 2-5 occurrences

| text | types | share_of_text | same line | lag 1 | lag 2 | lag 5 | lag 10 | lag 25 | lag 100 |
|---|---|---|---|---|---|---|---|---|---|
| VMS Currier B | 463 | 0.131 | 1.403 | 2.183 | 2.729 | 1.641 | 1.097 | 1.109 | 1.166 |
| VMS Currier A | 651 | 0.176 | 1.920 | 4.049 | 1.889 | 1.890 | 1.357 | 1.377 | 1.175 |
| copying model | 806.750 | 0.231 | 5.918 | 17.158 | 11.462 | 5.665 | 3.118 | 0.949 | 0.563 |
| copying model, 60% of sources from anywhere | 648.500 | 0.181 | 1.930 | 6.786 | 3.735 | 1.827 | 1.669 | 0.754 | 0.695 |
| copying model, prefer common c = 0.3 | 654.750 | 0.182 | 4.583 | 15.605 | 11.177 | 3.653 | 2.079 | 0.571 | 0.480 |
| copying model, prefer common c = 0.5 | 524.250 | 0.145 | 4.179 | 13.489 | 7.469 | 3.286 | 2.443 | 0.583 | 0.794 |
| copying model, prefer common c = 0.7 | 379.750 | 0.105 | 2.696 | 11.594 | 6.756 | 3.157 | 2.082 | 0.393 | 0.640 |
| Latin (Aix) | 1007 | 0.284 | 0.974 | 2.232 | 3.969 | 3.114 | 1.751 | 0.888 | 0.955 |
| Italian (Rettorica) | 533 | 0.145 | 3.397 | 11.396 | 9.641 | 5.093 | 2.564 | 1.556 | 0.557 |
| Naibbe (Pliny) | 1055 | 0.277 | 0.437 | 0.657 | 0.620 | 0.508 | 0.440 | 0.797 | 0.889 |

## summary

| text | distance | distance_sd | hapax | core_share | cohesion | mattr | h2 | repeat | edge | middle_lag1 | middle_lag25 | worst |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| VMS Currier B | 1.234 | None | 0.684 | 0.535 | 1.951 | 0.535 | 1.937 | 9.600 | 0.245 | 1.869 | 1.443 | line_last_jsd -2.8, line_first_jsd +2.6, edge_coupling +1.4 |
| VMS Currier A | 0.324 | None | 0.693 | 0.429 | 1.826 | 0.614 | 2.141 | 8.200 | 0.130 | 3.124 | 1.119 | repeat_rate -0.9, line_cohesion -0.6, line_last_jsd -0.3 |
| copying model | 2.182 | 0.414 | 0.592 | 0.304 | 2.526 | 0.620 | 2.324 | 4.950 | 0.115 | 8.110 | 1.377 | repeat_rate -4.5, line_last_jsd -3.8, line_first_jsd -3.4 |
| copying model, 60% of sources from anywhere | 2.283 | 0.357 | 0.588 | 0.497 | 1.095 | 0.552 | 2.084 | 4.275 | 0.107 | 2.939 | 1.031 | repeat_rate -5.2, line_cohesion -3.9, line_last_jsd -3.4 |
| copying model, prefer common c = 0.3 | 1.854 | 0.453 | 0.592 | 0.396 | 2.433 | 0.580 | 2.197 | 5.975 | 0.116 | 7.425 | 1.244 | line_first_jsd -3.6, repeat_rate -3.4, line_last_jsd -3.2 |
| copying model, prefer common c = 0.5 | 1.493 | 0.249 | 0.609 | 0.513 | 1.837 | 0.512 | 2.023 | 6.050 | 0.108 | 6.775 | 1.174 | repeat_rate -3.3, line_first_jsd -2.4, line_last_jsd -1.6 |
| copying model, prefer common c = 0.7 | 1.631 | 0.067 | 0.595 | 0.640 | 1.550 | 0.417 | 1.748 | 8.725 | 0.105 | 6.921 | 1.037 | line_first_jsd -3.4, line_last_jsd -2.2, h2 -1.9 |
| Latin (Aix) | 5.239 | None | 0.669 | 0.259 | 0.719 | 0.713 | 3.339 | 0.000 | 0.054 | 1.784 | 1.181 | repeat_rate -10.0, line_first_jsd -9.7, line_last_jsd -9.6 |
| Italian (Rettorica) | 4.953 | None | 0.717 | 0.474 | 0.983 | 0.534 | 3.111 | 0.500 | 0.135 | 4.455 | 2.224 | line_last_jsd -9.6, line_first_jsd -9.5, repeat_rate -9.4 |
| Naibbe (Pliny) | 4.536 | None | 0.576 | 0.429 | 0.928 | 0.661 | 2.088 | 0.900 | 0.002 | 1.137 | 0.760 | repeat_rate -9.0, line_last_jsd -8.9, line_first_jsd -8.8 |
