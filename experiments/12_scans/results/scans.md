# 12 scans: lines and spaces

Detector settings picked on 11 pages: strip=mid, smoothing=1.5, min distance=14 px, prominence=0.1.

Held-out pages (11): mean absolute error 3.2 lines, within one line on 7/11.

| page | split | zl_lines | detected | error | skew_deg |
|---|---|---|---|---|---|
| f103r | tuning | 54 | 54 | 0 | 1.750 |
| f103v | held-out | 46 | 47 | 1 | 0.000 |
| f104v | tuning | 44 | 45 | 1 | -1.000 |
| f105r | held-out | 37 | 37 | 0 | 0.000 |
| f105v | tuning | 38 | 40 | 2 | -1.000 |
| f106r | held-out | 47 | 44 | -3 | 1.000 |
| f106v | tuning | 47 | 44 | -3 | -1.000 |
| f107r | held-out | 51 | 45 | -6 | -1.000 |
| f107v | tuning | 49 | 51 | 2 | 2.000 |
| f108r | held-out | 50 | 51 | 1 | 2.500 |
| f108v | tuning | 53 | 52 | -1 | 0.000 |
| f111r | held-out | 54 | 51 | -3 | 0.500 |
| f111v | tuning | 51 | 51 | 0 | 2.000 |
| f112r | held-out | 45 | 27 | -18 | -1.500 |
| f112v | tuning | 47 | 46 | -1 | 3.000 |
| f113r | held-out | 51 | 50 | -1 | 1.750 |
| f113v | tuning | 49 | 50 | 1 | -0.250 |
| f114r | held-out | 45 | 45 | 0 | -1.000 |
| f114v | tuning | 41 | 42 | 1 | -1.000 |
| f115r | held-out | 45 | 44 | -1 | 2.000 |
| f115v | tuning | 45 | 47 | 2 | -3.000 |
| f116r | held-out | 50 | 49 | -1 | 0.250 |

## spaces

187 lines on 4 pages where the counts match (f103r, f105r, f111v, f114r). ZL marks 1607 certain and 145 uncertain spaces on them.

Gap widths are bimodal (peak at 2-3 px between glyphs, second bump around 10-16 px), but the two overlap, so the fit is repeated for several minimum gap widths.

big_gaps = a x dots + b x commas + c

| min_gap_px | mean_big_gaps | a_dots | b_commas | b_over_a | ratio_ci_low | ratio_ci_high | r_dots |
|---|---|---|---|---|---|---|---|
| 8 | 16.203 | 0.507 | 0.715 | 1.411 | 0.155 | 3.962 | 0.252 |
| 10 | 13.936 | 0.463 | 0.469 | 1.012 | -0.265 | 2.906 | 0.268 |
| 12 | 11.369 | 0.328 | 0.449 | 1.366 | -0.052 | 4.225 | 0.236 |
| 14 | 8.845 | 0.208 | 0.459 | 2.211 | -0.126 | 10.254 | 0.176 |
| 16 | 6.888 | 0.181 | 0.207 | 1.144 | -1.905 | 8.563 | 0.169 |
| 18 | 5.364 | 0.111 | 0.123 | 1.100 | -7.273 | 18.502 | 0.114 |

b/a near 1: an uncertain space shows up in the image like a certain one. Near 0: it mostly doesn't.
