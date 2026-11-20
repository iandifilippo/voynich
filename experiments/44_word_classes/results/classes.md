# 44 word classes from neighbours

Held-out mutual information (bits) between the classes of adjacent words, minus the same with classes fitted on the training half with its words shuffled.

| text | types (train) | tokens merged as rare | K=4 | K=8 | K=16 | K=32 |
|---|---|---|---|---|---|---|
| Naibbe cipher of Pliny | 287 | 0.411 | 0.036 | 0.042 | 0.039 | 0.047 |
| VMS Currier B | 346 | 0.320 | 0.037 | 0.087 | 0.087 | 0.083 |
| VMS Currier A | 196 | 0.428 | 0.007 | 0.009 | -0.007 | -0.001 |
| copying model | 409 | 0.275 | 0.001 | 0.008 | 0.008 | 0.032 |
| assembled words (exp. 36) | 337 | 0.339 | 0.008 | 0.027 | 0.021 | 0.036 |
| Latin, words | 347 | 0.459 | 0.079 | 0.092 | 0.133 | 0.130 |
| Italian, words | 284 | 0.324 | 0.148 | 0.250 | 0.308 | 0.317 |
| Latin, letters as tokens | 23 | 0.000 | 0.251 | 0.264 | 0.207 | 0.000 |

## Same, counting only pairs inside a line (first and last word left out)

| text | K=4 mid | K=8 mid | K=16 mid | K=32 mid |
|---|---|---|---|---|
| Naibbe cipher of Pliny | 0.038 | 0.044 | 0.042 | 0.051 |
| VMS Currier B | 0.042 | 0.097 | 0.092 | 0.091 |
| VMS Currier A | 0.007 | 0.013 | -0.012 | -0.011 |
| copying model | 0.002 | 0.011 | 0.010 | 0.038 |
| assembled words (exp. 36) | 0.009 | 0.029 | 0.025 | 0.036 |
| Latin, words | 0.081 | 0.090 | 0.136 | 0.120 |
| Italian, words | 0.143 | 0.247 | 0.305 | 0.303 |
| Latin, letters as tokens | 0.249 | 0.261 | 0.211 | 0.000 |

## Raw held-out MI and training MI

| text | K=4 raw | K=8 raw | K=16 raw | K=32 raw | K=8 train | K=32 train |
|---|---|---|---|---|---|---|
| Naibbe cipher of Pliny | 0.036 | 0.045 | 0.060 | 0.133 | 0.109 | 0.283 |
| VMS Currier B | 0.039 | 0.094 | 0.115 | 0.183 | 0.177 | 0.379 |
| VMS Currier A | 0.009 | 0.018 | 0.050 | 0.201 | 0.117 | 0.416 |
| copying model | 0.003 | 0.013 | 0.028 | 0.114 | 0.112 | 0.321 |
| assembled words (exp. 36) | 0.008 | 0.032 | 0.039 | 0.112 | 0.109 | 0.289 |
| Latin, words | 0.081 | 0.135 | 0.218 | 0.338 | 0.225 | 0.497 |
| Italian, words | 0.155 | 0.261 | 0.362 | 0.528 | 0.307 | 0.665 |
| Latin, letters as tokens | 0.293 | 0.379 | 0.528 | 0.580 | 0.383 | 0.587 |
