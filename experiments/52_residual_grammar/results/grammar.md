# 52 is the residual the same in A and B?

Correlation of log(observed/expected) over class transitions (expected keeps boundary glyphs and sheet).

| comparison | transitions compared | correlation of log ratios |
|---|---|---|
| B, half of sheets vs other half (ceiling) | 153 | -0.019 |
| A, half of sheets vs other half (ceiling) | 46 | 0.073 |
| A vs B | 151 | -0.033 |
| B (ZL) vs B (IT), same pages, other transcriber | 338 | 0.828 |
| B vs habits generator fitted to B | 274 | -0.034 |

## Transitions favoured or avoided in both A and B

| word i | word i+1 | A obs/exp | B obs/exp | A ratio | B ratio |
|---|---|---|---|---|---|
| a_n | ch/sh_y | 5/10 | 96/100 | 0.509 | 0.958 |
| ch/sh_r | ch/sh_other | 16/18 | 9/15 | 0.868 | 0.611 |
| ch/sh_r | o_r | 6/12 | 18/18 | 0.542 | 0.991 |
| other_l | o_y | 10/15 | 29/32 | 0.685 | 0.922 |
| o_y | d_l | 7/11 | 19/20 | 0.667 | 0.965 |
| other_y | d_n | 29/31 | 20/29 | 0.937 | 0.694 |
| other_l | ch/sh_y | 24/32 | 74/86 | 0.763 | 0.863 |
| o_r | ch/sh_l | 12/17 | 12/13 | 0.722 | 0.914 |
| ch/sh_y | o_n | 20/18 | 102/91 | 1.134 | 1.124 |
| ch/sh_y | other_n | 15/15 | 89/71 | 1.025 | 1.246 |
| ch/sh_y | qo_r | 15/12 | 94/87 | 1.192 | 1.086 |
| d_n | o_l | 17/15 | 12/10 | 1.120 | 1.182 |
| other_y | qo_y | 38/31 | 235/212 | 1.206 | 1.111 |
| other_y | d_r | 14/10 | 20/19 | 1.343 | 1.050 |
| ch/sh_l | d_n | 71/64 | 14/11 | 1.106 | 1.306 |
| ch/sh_y | ch/sh_l | 51/43 | 75/57 | 1.196 | 1.314 |
| d_y | other_y | 14/10 | 32/27 | 1.381 | 1.166 |
| other_l | ch/sh_l | 45/42 | 26/16 | 1.066 | 1.601 |

## Does the structure transfer? (bits per pair above a no-structure baseline)

| text | learned on half the sheets, scored on the rest (bits/pair) | learned on odd lines, scored on even lines, all sheets pooled | learned and scored inside each sheet separately |
|---|---|---|---|
| Currier B | 0.003 | 0.002 | 0.004 |
| Currier A | 0.001 | -0.004 | -0.001 |
| habits generator (B) | 0.004 | 0.003 | 0.002 |
