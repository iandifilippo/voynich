# 44 word classes from neighbours

Held-out mutual information (bits) between the classes of adjacent words, minus the same with classes fitted on the training half with its words shuffled.

| text | types (train) | test tokens seen in train | K=2 | K=4 | K=8 | K=16 | K=24 | K=32 |
|---|---|---|---|---|---|---|---|---|
| Naibbe cipher of Pliny | 3172 | 0.834 | 0.011 | 0.001 | 0.002 | 0.007 | 0.008 | 0.006 |
| VMS Currier B | 2985 | 0.830 | 0.007 | 0.003 | 0.011 | 0.030 | 0.028 | 0.049 |
| VMS Currier A | 2069 | 0.759 | 0.001 | -0.000 | -0.005 | 0.007 | 0.003 | 0.026 |
| copying model | 2547 | 0.866 | 0.001 | 0.000 | 0.000 | -0.000 | -0.001 | -0.000 |
| assembled words (exp. 36) | 3215 | 0.784 | -0.000 | -0.000 | 0.001 | 0.004 | 0.009 | -0.002 |
| Latin, words | 3994 | 0.759 | 0.012 | 0.023 | 0.045 | 0.082 | 0.069 | 0.078 |
| Italian, words | 3010 | 0.805 | 0.013 | 0.022 | 0.099 | 0.149 | 0.172 | 0.186 |
| Latin, letters as tokens | 23 | 1.000 | 0.231 | 0.251 | 0.264 | 0.207 | 0.000 | 0.000 |

## Raw held-out MI and training MI

| text | K=2 raw | K=4 raw | K=8 raw | K=16 raw | K=24 raw | K=32 raw | K=8 train | K=24 train |
|---|---|---|---|---|---|---|---|---|
| Naibbe cipher of Pliny | 0.011 | 0.002 | 0.007 | 0.026 | 0.058 | 0.092 | 0.500 | 0.913 |
| VMS Currier B | 0.009 | 0.005 | 0.017 | 0.058 | 0.084 | 0.138 | 0.455 | 0.879 |
| VMS Currier A | 0.002 | 0.005 | 0.014 | 0.057 | 0.116 | 0.206 | 0.625 | 1.207 |
| copying model | 0.001 | 0.002 | 0.005 | 0.021 | 0.048 | 0.087 | 0.375 | 0.721 |
| assembled words (exp. 36) | 0.000 | 0.002 | 0.005 | 0.025 | 0.057 | 0.090 | 0.482 | 0.877 |
| Latin, words | 0.014 | 0.033 | 0.060 | 0.131 | 0.176 | 0.234 | 0.784 | 1.373 |
| Italian, words | 0.017 | 0.028 | 0.114 | 0.190 | 0.274 | 0.361 | 0.653 | 1.213 |
| Latin, letters as tokens | 0.233 | 0.293 | 0.379 | 0.528 | 0.580 | 0.580 | 0.383 | 0.587 |
