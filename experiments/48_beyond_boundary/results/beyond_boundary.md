# 48 links between neighbouring words beyond the boundary glyphs

Conditional MI (bits) given the last sign of the first word and the first sign of the second, minus a permutation baseline.

| text | baseline | pairs | start -> start | gallows -> gallows | ending -> ending | length -> length | sum of all 16 |
|---|---|---|---|---|---|---|---|
| Currier B | whole text | 20580 | 0.040 | 0.034 | 0.038 | 0.008 | 0.351 |
| Currier A | whole text | 9674 | 0.035 | 0.032 | 0.033 | 0.014 | 0.310 |
| generator, boundary habit only (exp. 36) | whole text | 20580 | 0.007 | 0.003 | 0.004 | 0.002 | 0.017 |
| cipher of Latin, one key, Voynich words | whole text | 20580 | 0.068 | 0.024 | 0.089 | 0.028 | 0.898 |
| Latin (letters as signs) | whole text | 17777 | 0.104 | 0.009 | 0.171 | 0.057 | 1.178 |
| Italian (letters as signs) | whole text | 17777 | 0.198 | 0.008 | 0.278 | 0.084 | 1.832 |
| Currier B | inside the sheet | 20580 | 0.031 | 0.033 | 0.030 | 0.008 | 0.298 |
| Currier A | inside the sheet | 9674 | 0.024 | 0.028 | 0.020 | 0.011 | 0.231 |
| generator, boundary habit only (exp. 36) | inside the sheet | 20580 | 0.007 | 0.002 | 0.003 | 0.001 | 0.017 |
| cipher of Latin, one key, Voynich words | inside the sheet | 20580 | 0.066 | 0.022 | 0.088 | 0.027 | 0.878 |
| Latin (letters as signs) | inside the sheet | 17777 | 0.062 | 0.005 | 0.093 | 0.033 | 0.657 |
| Italian (letters as signs) | inside the sheet | 17777 | 0.144 | 0.007 | 0.208 | 0.065 | 1.369 |

## By distance (plain MI, baseline shuffled inside the sheet by line position)

| text | start d=1 | start d=2 | start d=3 | gallows d=1 | gallows d=2 | gallows d=3 | ending d=1 | ending d=2 | ending d=3 |
|---|---|---|---|---|---|---|---|---|---|
| Currier B | 0.182 | 0.053 | 0.028 | 0.032 | 0.024 | 0.019 | 0.078 | 0.024 | 0.021 |
| Currier A | 0.137 | 0.048 | 0.039 | 0.029 | 0.029 | 0.019 | 0.078 | 0.022 | 0.036 |
| generator, boundary habit only (exp. 36) | 0.064 | 0.012 | 0.013 | 0.003 | 0.002 | -0.000 | 0.055 | 0.009 | 0.007 |
| cipher of Latin, one key, Voynich words | 0.150 | 0.052 | 0.013 | 0.017 | 0.003 | 0.002 | 0.110 | 0.041 | 0.017 |
| Latin (letters as signs) | 0.180 | 0.079 | 0.041 | 0.001 | 0.000 | 0.000 | 0.351 | 0.113 | 0.060 |
