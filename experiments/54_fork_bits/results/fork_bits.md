# 54 bits hidden in the forks

Held-out bits per symbol, n-gram looking k symbols back, trained on half the sheets, tested on the other half.

| symbol | text | k=0 | k=1 | k=2 | k=3 | k=4 | k=6 | k=8 | gain k=1 over k=0 | gain from looking further than 1 back | best k |
|---|---|---|---|---|---|---|---|---|---|---|---|
| start (4) | cipher of Latin, 2 bits per word (start) | 1.840 | 1.806 | 1.775 | 1.690 | 1.642 | 1.651 | 1.814 | 0.034 | 0.179 | 5 |
| start (4) | cipher of Latin, 4 bits per word (start + end) | 1.854 | 1.839 | 1.835 | 1.833 | 1.845 | 2.053 | 2.422 | 0.015 | 0.006 | 3 |
| start (4) | habits generator (B) | 1.911 | 1.875 | 1.856 | 1.850 | 1.873 | 2.180 | 2.557 | 0.036 | 0.025 | 3 |
| start (4) | Currier B | 1.952 | 1.931 | 1.928 | 1.935 | 1.970 | 2.334 | 2.747 | 0.021 | 0.003 | 2 |
| start (4) | Currier A | 1.803 | 1.798 | 1.802 | 1.823 | 1.895 | 2.270 | 2.648 | 0.005 | 0.000 | 1 |
| end (4) | cipher of Latin, 2 bits per word (start) | 1.750 | 1.750 | 1.752 | 1.763 | 1.803 | 2.063 | 2.503 | 0.000 | 0.000 | 1 |
| end (4) | cipher of Latin, 4 bits per word (start + end) | 1.845 | 1.831 | 1.827 | 1.822 | 1.830 | 2.040 | 2.410 | 0.014 | 0.009 | 3 |
| end (4) | habits generator (B) | 1.824 | 1.821 | 1.823 | 1.834 | 1.869 | 2.186 | 2.615 | 0.003 | 0.000 | 1 |
| end (4) | Currier B | 1.795 | 1.789 | 1.785 | 1.791 | 1.825 | 2.126 | 2.530 | 0.006 | 0.004 | 2 |
| end (4) | Currier A | 1.919 | 1.916 | 1.914 | 1.921 | 2.004 | 2.479 | 2.797 | 0.003 | 0.002 | 2 |
| start and end (16) | cipher of Latin, 2 bits per word (start) | 3.560 | 3.542 | 3.640 | 3.961 | 4.278 |  |  | 0.017 | 0.000 | 1 |
| start and end (16) | cipher of Latin, 4 bits per word (start + end) | 3.666 | 3.481 | 3.251 | 3.174 | 3.238 |  |  | 0.185 | 0.307 | 3 |
| start and end (16) | habits generator (B) | 3.692 | 3.606 | 3.736 | 4.079 | 4.367 |  |  | 0.085 | 0.000 | 1 |
| start and end (16) | Currier B | 3.702 | 3.596 | 3.713 | 4.087 | 4.388 |  |  | 0.106 | 0.000 | 1 |
| start and end (16) | Currier A | 3.704 | 3.704 | 3.912 | 4.310 | 4.517 |  |  | -0.000 | 0.000 | 0 |
