# 54 bits hidden in the forks

Held-out bits per symbol, n-gram looking k symbols back, trained on half the sheets, tested on the other half.

| symbol | text | k=0 | k=1 | k=2 | k=3 | k=4 | k=6 | k=8 | gain k=1 over k=0 | gain from looking further than 1 back | best k |
|---|---|---|---|---|---|---|---|---|---|---|---|
| starts with qo (2) | cipher of Latin, 1 bit per word (qo or not) | 0.926 | 0.921 | 0.910 | 0.907 | 0.899 | 0.856 | 0.835 | 0.005 | 0.085 | 8 |
| starts with qo (2) | cipher of Latin, 2 bits per word (start) | 0.980 | 0.967 | 0.966 | 0.964 | 0.963 | 0.963 | 0.970 | 0.013 | 0.005 | 4 |
| starts with qo (2) | cipher of Latin, 4 bits per word (start + end) | 0.974 | 0.975 | 0.975 | 0.975 | 0.974 | 0.981 | 0.992 | -0.000 | 0.000 | 0 |
| starts with qo (2) | habits generator (B) | 0.665 | 0.652 | 0.643 | 0.637 | 0.634 | 0.633 | 0.654 | 0.013 | 0.020 | 5 |
| starts with qo (2) | Currier B | 0.677 | 0.675 | 0.671 | 0.670 | 0.671 | 0.672 | 0.689 | 0.002 | 0.005 | 3 |
| starts with qo (2) | Currier A | 0.457 | 0.456 | 0.458 | 0.459 | 0.464 | 0.478 | 0.501 | 0.001 | 0.000 | 1 |
| gallows (4) | cipher of Latin, 1 bit per word (qo or not) | 1.864 | 1.865 | 1.868 | 1.879 | 1.914 | 2.253 | 2.697 | -0.000 | 0.000 | 0 |
| gallows (4) | cipher of Latin, 2 bits per word (start) | 1.674 | 1.674 | 1.676 | 1.682 | 1.707 | 1.908 | 2.342 | 0.000 | 0.000 | 1 |
| gallows (4) | cipher of Latin, 4 bits per word (start + end) | 1.677 | 1.679 | 1.682 | 1.691 | 1.721 | 1.946 | 2.365 | -0.002 | 0.000 | 0 |
| gallows (4) | habits generator (B) | 1.870 | 1.835 | 1.818 | 1.819 | 1.857 | 2.146 | 2.541 | 0.035 | 0.017 | 2 |
| gallows (4) | Currier B | 1.698 | 1.673 | 1.664 | 1.671 | 1.701 | 1.916 | 2.288 | 0.025 | 0.009 | 2 |
| gallows (4) | Currier A | 1.631 | 1.609 | 1.599 | 1.623 | 1.679 | 1.942 | 2.295 | 0.022 | 0.010 | 2 |
| start (4) | cipher of Latin, 1 bit per word (qo or not) | 1.516 | 1.511 | 1.503 | 1.510 | 1.527 | 1.656 | 1.932 | 0.005 | 0.008 | 2 |
| start (4) | cipher of Latin, 2 bits per word (start) | 1.840 | 1.806 | 1.775 | 1.690 | 1.642 | 1.651 | 1.814 | 0.034 | 0.179 | 5 |
| start (4) | cipher of Latin, 4 bits per word (start + end) | 1.854 | 1.839 | 1.835 | 1.833 | 1.845 | 2.053 | 2.422 | 0.015 | 0.006 | 3 |
| start (4) | habits generator (B) | 1.914 | 1.906 | 1.892 | 1.895 | 1.939 | 2.336 | 2.714 | 0.008 | 0.015 | 2 |
| start (4) | Currier B | 1.952 | 1.931 | 1.928 | 1.935 | 1.970 | 2.334 | 2.747 | 0.021 | 0.003 | 2 |
| start (4) | Currier A | 1.803 | 1.798 | 1.802 | 1.823 | 1.895 | 2.270 | 2.648 | 0.005 | 0.000 | 1 |
| end (4) | cipher of Latin, 1 bit per word (qo or not) | 1.776 | 1.777 | 1.780 | 1.790 | 1.815 | 2.079 | 2.518 | -0.001 | 0.000 | 0 |
| end (4) | cipher of Latin, 2 bits per word (start) | 1.758 | 1.758 | 1.761 | 1.770 | 1.802 | 2.055 | 2.475 | -0.000 | 0.000 | 0 |
| end (4) | cipher of Latin, 4 bits per word (start + end) | 1.845 | 1.831 | 1.827 | 1.822 | 1.830 | 2.040 | 2.410 | 0.014 | 0.009 | 3 |
| end (4) | habits generator (B) | 1.825 | 1.822 | 1.824 | 1.834 | 1.868 | 2.179 | 2.607 | 0.003 | 0.000 | 1 |
| end (4) | Currier B | 1.795 | 1.789 | 1.785 | 1.791 | 1.825 | 2.126 | 2.530 | 0.006 | 0.004 | 2 |
| end (4) | Currier A | 1.919 | 1.916 | 1.914 | 1.921 | 2.004 | 2.479 | 2.797 | 0.003 | 0.002 | 2 |
| start and end (16) | cipher of Latin, 1 bit per word (qo or not) | 3.282 | 3.290 | 3.381 | 3.642 | 3.980 |  |  | -0.008 | 0.000 | 0 |
| start and end (16) | cipher of Latin, 2 bits per word (start) | 3.563 | 3.544 | 3.639 | 3.946 | 4.250 |  |  | 0.019 | 0.000 | 1 |
| start and end (16) | cipher of Latin, 4 bits per word (start + end) | 3.666 | 3.481 | 3.251 | 3.174 | 3.238 |  |  | 0.185 | 0.307 | 3 |
| start and end (16) | habits generator (B) | 3.706 | 3.657 | 3.797 | 4.166 | 4.454 |  |  | 0.049 | 0.000 | 1 |
| start and end (16) | Currier B | 3.702 | 3.596 | 3.713 | 4.087 | 4.388 |  |  | 0.106 | 0.000 | 1 |
| start and end (16) | Currier A | 3.704 | 3.704 | 3.912 | 4.310 | 4.517 |  |  | -0.000 | 0.000 | 0 |
