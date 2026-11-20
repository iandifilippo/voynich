# 49 a setting per line?

Share of word pairs that agree on a feature: same line vs different lines of the same page, at the same positions.

| text | feature | d=1 ratio | d=2 ratio | d=3 ratio | d=4 ratio |
|---|---|---|---|---|---|
| Currier B | gallows | 1.116 | 1.106 | 1.070 | 1.073 |
| Currier B | start | 1.016 | 1.141 | 1.107 | 1.097 |
| Currier B | ending | 0.998 | 1.038 | 1.006 | 1.030 |
| Currier A | gallows | 1.080 | 1.087 | 1.080 | 1.053 |
| Currier A | start | 1.058 | 1.101 | 1.098 | 1.078 |
| Currier A | ending | 1.043 | 1.102 | 1.086 | 1.041 |
| generator (exp. 36) | gallows | 1.063 | 1.036 | 0.993 | 1.019 |
| generator (exp. 36) | start | 1.058 | 1.106 | 1.068 | 1.148 |
| generator (exp. 36) | ending | 1.044 | 1.036 | 1.050 | 1.032 |
| Latin | has a stop (b c d g p t) | 1.002 | 1.000 | 1.003 | 1.015 |
| Latin | start | 0.717 | 0.980 | 0.985 | 1.067 |
| Latin | ending | 1.115 | 1.217 | 1.175 | 1.126 |

## Raw shares

| text | feature | d=1: same line / other line | d=2: same line / other line | d=3: same line / other line | d=4: same line / other line |
|---|---|---|---|---|---|
| Currier B | gallows | 0.377 / 0.337 | 0.373 / 0.337 | 0.359 / 0.336 | 0.359 / 0.335 |
| Currier B | start | 0.169 / 0.166 | 0.187 / 0.164 | 0.177 / 0.160 | 0.173 / 0.158 |
| Currier B | ending | 0.304 / 0.305 | 0.313 / 0.302 | 0.300 / 0.298 | 0.306 / 0.297 |
| Currier A | gallows | 0.390 / 0.361 | 0.398 / 0.366 | 0.397 / 0.367 | 0.399 / 0.378 |
| Currier A | start | 0.161 / 0.153 | 0.163 / 0.148 | 0.157 / 0.143 | 0.152 / 0.141 |
| Currier A | ending | 0.235 / 0.225 | 0.243 / 0.220 | 0.238 / 0.219 | 0.226 / 0.217 |
| generator (exp. 36) | gallows | 0.358 / 0.337 | 0.349 / 0.337 | 0.337 / 0.340 | 0.345 / 0.339 |
| generator (exp. 36) | start | 0.143 / 0.135 | 0.148 / 0.134 | 0.143 / 0.134 | 0.154 / 0.134 |
| generator (exp. 36) | ending | 0.282 / 0.270 | 0.279 / 0.270 | 0.285 / 0.271 | 0.281 / 0.273 |
| Latin | has a stop (b c d g p t) | 0.676 / 0.675 | 0.677 / 0.677 | 0.677 / 0.675 | 0.686 / 0.676 |
| Latin | start | 0.058 / 0.081 | 0.079 / 0.081 | 0.080 / 0.081 | 0.086 / 0.080 |
| Latin | ending | 0.145 / 0.130 | 0.157 / 0.129 | 0.152 / 0.129 | 0.147 / 0.130 |
