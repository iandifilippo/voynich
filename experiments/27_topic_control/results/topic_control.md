# 27 would the page test see a subject?

| text | pages | lines | same page, 1-5 lines apart | same page, 10-30 lines apart | across the page break, 1-5 lines | end of page vs start of a page 2-6 on | next page, any lines | 3 pages on, any lines | 8 pages on, any lines |
|---|---|---|---|---|---|---|---|---|---|
| VMS herbal A, hand 1 | 95 | 1188 | 1.400 | 0.970 | 1.329 | 1.121 | 1.053 | 0.972 | 0.895 |
| VMS balneo B, hand 2 | 19 | 725 | 1.404 | 1.168 | 0.894 | 0.862 | 0.997 | 0.928 | 0.915 |
| VMS stars B, hand 3 | 22 | 1035 | 1.514 | 1.324 | 1.280 | 0.962 | 1.101 | 0.949 | 1.003 |
| Pliny 16, chapters | 44 | 978 | 1.251 | 1.006 | 0.946 | 0.978 | 1.160 | 1.137 | 1.022 |
| Pliny 16, lines dealt at random into the chapters | 44 | 978 | 0.987 | 1.040 | 0.910 | 0.880 | 0.935 | 0.926 | 0.890 |
| Naibbe cipher of Pliny 16, chapters | 44 | 1019 | 1.013 | 1.011 | 0.979 | 0.995 | 1.003 | 1.042 | 1.047 |
| copying model, 13-line pages | 95 | 1209 | 1.398 | 1.048 | 1.136 | 1.009 | 1.012 | 0.984 | 0.976 |

## does a page have vocabulary of its own?

Lines 3-12 apart: shared word types when both are on the same page, over shared word types when a page break lies between them, at matched distances. Null: the page breaks slid along the text.

| text | words | same page / across a break, same distance | with breaks slid along | p |
|---|---|---|---|---|
| VMS herbal A, hand 1 | all | 0.923 | 0.994 | 0.905 |
| VMS herbal A, hand 1 | without the 60 commonest | 1.233 | 1.013 | 0.090 |
| VMS balneo B, hand 2 | all | 1.355 | 1.006 | 0.005 |
| VMS balneo B, hand 2 | without the 60 commonest | 1.481 | 1.020 | 0.015 |
| VMS stars B, hand 3 | all | 1.145 | 0.996 | 0.017 |
| VMS stars B, hand 3 | without the 60 commonest | 1.392 | 1.011 | 0.007 |
| Pliny 16, chapters | all | 1.048 | 1.006 | 0.254 |
| Pliny 16, chapters | without the 60 commonest | 1.389 | 1.012 | 0.010 |
| Pliny 16, lines dealt at random into the chapters | all | 1.016 | 1.001 | 0.344 |
| Pliny 16, lines dealt at random into the chapters | without the 60 commonest | 1.073 | 1.013 | 0.327 |
| Naibbe cipher of Pliny 16, chapters | all | 1.011 | 0.999 | 0.289 |
| Naibbe cipher of Pliny 16, chapters | without the 60 commonest | 0.972 | 1.000 | 0.636 |
| copying model, 13-line pages | all | 1.152 | 0.998 | 0.010 |
| copying model, 13-line pages | without the 60 commonest | 1.932 | 1.018 | 0.007 |

## carry-over at the break

| text | break / same page near | ci_break | break / control | ci_control | next page percentile |
|---|---|---|---|---|---|
| VMS herbal A, hand 1 | 0.949 | 0.79-1.09 | 1.186 | 1.03-1.36 | 0.621 |
| VMS balneo B, hand 2 | 0.637 | 0.43-0.86 | 1.037 | 0.76-1.36 | 0.526 |
| VMS stars B, hand 3 | 0.846 | 0.59-1.08 | 1.330 | 0.95-1.78 | 0.580 |
| Pliny 16, chapters | 0.757 | 0.59-0.93 | 0.967 | 0.75-1.21 | 0.526 |
| Pliny 16, lines dealt at random into the chapters | 0.922 | 0.71-1.18 | 1.034 | 0.84-1.25 | 0.507 |
| Naibbe cipher of Pliny 16, chapters | 0.967 | 0.89-1.05 | 0.984 | 0.91-1.05 | 0.484 |
| copying model, 13-line pages | 0.813 | 0.74-0.89 | 1.127 | 1.03-1.23 | 0.580 |

## the same without each text's 60 most widespread words

| text | same page, 1-5 lines apart | same page, 10-30 lines apart | across the page break, 1-5 lines | end of page vs start of a page 2-6 on | next page, any lines | 3 pages on, any lines | 8 pages on, any lines |
|---|---|---|---|---|---|---|---|
| VMS herbal A, hand 1 | 2.279 | 1.666 | 1.531 | 0.980 | 0.977 | 1.017 | 1.099 |
| VMS balneo B, hand 2 | 1.817 | 1.388 | 0.793 | 1.142 | 0.953 | 0.860 | 0.904 |
| VMS stars B, hand 3 | 1.907 | 1.502 | 1.857 | 0.780 | 1.213 | 0.863 | 0.973 |
| Pliny 16, chapters | 4.071 | 1.936 | 2.140 | 0.678 | 1.634 | 1.237 | 1.209 |
| Pliny 16, lines dealt at random into the chapters | 1.220 | 1.120 | 1.352 | 1.041 | 0.922 | 0.679 | 0.770 |
| Naibbe cipher of Pliny 16, chapters | 1.077 | 1.011 | 1.008 | 1.090 | 1.031 | 1.003 | 1.002 |
| copying model, 13-line pages | 6.551 | 1.971 | 2.963 | 1.068 | 1.141 | 0.933 | 0.851 |

| text | break / same page near | ci_break | break / control | ci_control | next page percentile |
|---|---|---|---|---|---|
| VMS herbal A, hand 1 | 0.672 | 0.46-0.94 | 1.561 | 1.06-2.10 | 0.572 |
| VMS balneo B, hand 2 | 0.437 | 0.07-1.04 | 0.694 | 0.13-1.61 | 0.493 |
| VMS stars B, hand 3 | 0.973 | 0.37-1.76 | 2.381 | 0.81-5.26 | 0.474 |
| Pliny 16, chapters | 0.526 | 0.28-0.88 | 3.156 | 1.53-6.75 | 0.632 |
| Pliny 16, lines dealt at random into the chapters | 1.108 | 0.44-1.97 | 1.298 | 0.55-2.40 | 0.495 |
| Naibbe cipher of Pliny 16, chapters | 0.936 | 0.76-1.10 | 0.925 | 0.74-1.13 | 0.427 |
| copying model, 13-line pages | 0.452 | 0.33-0.60 | 2.774 | 1.91-3.85 | 0.649 |

`break / same page near` = 1: the page break costs nothing.
