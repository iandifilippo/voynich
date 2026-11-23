# 65 family link

## The rhythm in all B sheets (next family over base rate)

| previous | n | next q | next c | next o | next x |
|---|---|---|---|---|---|
| qo-...-y | 1995 | 1.82 | 0.69 | 0.84 | 0.89 |
| qo-...-l | 514 | 0.44 | 1.71 | 0.82 | 0.88 |
| qo-...-r | 374 | 0.32 | 1.57 | 1.42 | 0.61 |
| qo-...-n | 773 | 0.41 | 1.74 | 1.36 | 0.46 |
| qo-...-other | 222 | 0.77 | 0.80 | 0.83 | 1.43 |
| ch/sh-...-y | 3194 | 1.90 | 0.59 | 0.80 | 0.96 |
| ch/sh-...-l | 620 | 0.93 | 0.98 | 0.84 | 1.18 |
| ch/sh-...-r | 449 | 0.55 | 1.22 | 1.26 | 0.88 |
| ch/sh-...-n | 334 | 0.79 | 1.63 | 1.17 | 0.48 |
| ch/sh-...-other | 501 | 0.66 | 0.67 | 0.80 | 1.62 |
| o-...-y | 1787 | 1.64 | 0.64 | 1.00 | 0.92 |
| o-...-l | 804 | 0.33 | 1.33 | 1.04 | 1.09 |
| o-...-r | 773 | 0.26 | 0.96 | 1.33 | 1.22 |
| o-...-n | 803 | 0.33 | 1.45 | 1.59 | 0.57 |
| o-...-other | 336 | 0.51 | 0.66 | 0.69 | 1.81 |
| other-...-y | 2380 | 1.45 | 0.77 | 0.78 | 1.09 |
| other-...-l | 1028 | 0.33 | 1.29 | 0.81 | 1.30 |
| other-...-r | 1422 | 0.20 | 1.12 | 1.14 | 1.27 |
| other-...-n | 1708 | 0.31 | 1.61 | 1.38 | 0.61 |
| other-...-other | 563 | 0.38 | 0.73 | 0.85 | 1.70 |

## qo k words back, against shuffles

| lag | real | shuffled in line | shuffled in sheet |
|---|---|---|---|
| 1 | 1.190 | 1.207 | 1.118 |
| 2 | 1.371 | 1.270 | 1.124 |
| 3 | 1.217 | 1.210 | 1.104 |
| 4 | 1.194 | 1.232 | 1.142 |

Line spread of qo share (variance over binomial): 1.41

## Neighbouring lines (qo-, -y, -n shares)

| lines apart | sheet mean removed | page mean removed | page, lines shuffled |
|---|---|---|---|
| 1 | 0.159 | 0.086 | -0.036 |
| 2 | 0.131 | 0.066 | -0.041 |
| 3 | 0.101 | 0.033 | -0.039 |
| 5 | 0.065 | 0.002 | -0.036 |
| 8 | 0.018 | -0.048 | -0.039 |

## Choice on the even sheets (mean of 3 seeds)

| model | within (of 11) | rhythm measures within (of 4) | rhythm | lag 2 | line spread | neighbours |
|---|---|---|---|---|---|---|
| B even sheets |  |  | 1.873 | 1.131 | 1.313 | 0.194 |
| last sign | 6 | 3 | 1.636 | 0.985 | 1.205 | 0.019 |
| family | 7 | 3 | 1.771 | 1.014 | 1.315 | 0.002 |
| family, line setting 0.3 drift 0.0 | 6 | 3 | 1.724 | 1.073 | 1.380 | 0.023 |
| family, line setting 0.4 drift 0.9 | 7 | 3 | 1.723 | 1.018 | 1.508 | 0.061 |
| family, line setting 0.6 drift 0.9 | 7 | 2 | 1.621 | 1.001 | 1.813 | 0.105 |
| family, echo window 15 edit 0.1 | 7 | 3 | 1.743 | 1.008 | 1.218 | 0.028 |
| family, echo window 15 edit 0.2 | 7 | 3 | 1.684 | 0.980 | 1.243 | 0.047 |
| family, echo window 15 edit 0.2 fits | 7 | 3 | 1.793 | 1.038 | 1.285 | 0.085 |
| family, echo window 25 edit 0.2 fits | 7 | 3 | 1.828 | 1.034 | 1.209 | 0.050 |
| family, echo window 25 edit 0.3 fits | 5 | 3 | 1.865 | 0.999 | 1.286 | 0.081 |

## Odd sheets (mean of 5 seeds): words

| model | distinct per 1000 | hapax share | new words vs training half | lexicon gain (bits) | mean signs per word | qo- words |
|---|---|---|---|---|---|---|
| Currier B, odd sheets | 248.948 | 0.677 | 0.183 | -0.263 | 4.377 | 0.195 |
| exp. 61 (last sign) | 282.421 | 0.694 | 0.217 | -0.311 | 4.300 | 0.156 |
| family link (chosen) | 284.492 | 0.697 | 0.220 | -0.327 | 4.314 | 0.155 |
| family link, echo from above (window 25, edit 0.2, fits) | 309.076 | 0.697 | 0.262 | -0.302 | 4.340 | 0.155 |

## Odd sheets: pages, lines, sequence

| model | sheet identity | gallows same line / other | beyond the boundary (bits) | recurring pairs excess | class sequence (bits) | within (of 11) |
|---|---|---|---|---|---|---|
| Currier B, odd sheets | 1.000 | 1.064 | 0.231 | 0.054 | 0.063 |  |
| exp. 61 (last sign) | 0.760 | 1.032 | 0.097 | 0.021 | 0.005 | 7 |
| family link (chosen) | 0.770 | 1.015 | 0.152 | 0.025 | 0.010 | 6 |
| family link, echo from above (window 25, edit 0.2, fits) | 0.740 | 1.006 | 0.113 | 0.021 | 0.012 | 5 |

## Odd sheets: the rhythm

| model | rhythm | lag 2 | line spread | neighbours | rhythm within (of 4) |
|---|---|---|---|---|---|
| Currier B, odd sheets | 1.927 | 1.098 | 1.424 | 0.128 |  |
| exp. 61 (last sign) | 1.573 | 0.981 | 1.266 | 0.008 | 3 |
| family link (chosen) | 1.786 | 1.035 | 1.243 | 0.004 | 3 |
| family link, echo from above (window 25, edit 0.2, fits) | 1.862 | 1.016 | 1.184 | 0.058 | 3 |

## The family table from the family-link generator

| previous | n | next q | next c | next o | next x |
|---|---|---|---|---|---|
| qo-...-y | 995 | 1.71 | 0.80 | 0.82 | 0.85 |
| qo-...-l | 275 | 0.71 | 1.35 | 0.83 | 1.02 |
| qo-...-r | 265 | 0.68 | 1.36 | 1.15 | 0.83 |
| qo-...-n | 369 | 0.83 | 1.40 | 1.33 | 0.59 |
| qo-...-other | 203 | 0.83 | 1.20 | 0.81 | 1.08 |
| ch/sh-...-y | 1655 | 1.76 | 0.69 | 0.84 | 0.89 |
| ch/sh-...-l | 206 | 0.92 | 1.14 | 0.69 | 1.15 |
| ch/sh-...-r | 177 | 0.61 | 1.53 | 1.11 | 0.77 |
| ch/sh-...-n | 150 | 0.65 | 1.54 | 1.28 | 0.63 |
| ch/sh-...-other | 287 | 0.96 | 0.70 | 0.83 | 1.35 |
| o-...-y | 854 | 1.43 | 0.61 | 1.19 | 0.91 |
| o-...-l | 415 | 0.42 | 1.32 | 1.18 | 0.99 |
| o-...-r | 318 | 0.31 | 0.80 | 1.41 | 1.28 |
| o-...-n | 353 | 0.54 | 1.20 | 1.60 | 0.73 |
| o-...-other | 191 | 0.48 | 0.76 | 0.67 | 1.69 |
| other-...-y | 1242 | 1.35 | 0.90 | 0.71 | 1.06 |
| other-...-l | 585 | 0.43 | 1.16 | 0.99 | 1.22 |
| other-...-r | 733 | 0.25 | 1.07 | 0.98 | 1.40 |
| other-...-n | 977 | 0.41 | 1.47 | 1.37 | 0.76 |
| other-...-other | 363 | 0.56 | 0.88 | 0.80 | 1.47 |
