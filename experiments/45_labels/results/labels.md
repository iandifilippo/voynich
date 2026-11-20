# 45 labels and the text on their page

Hits per 1000 words of running text.

## Exact

| section | probes | n | same page: exact | same sheet, other page: exact | same section, other sheets: exact |
|---|---|---|---|---|---|
| pharmaceutical | labels | 225 | 0.612 | 0.650 | 0.620 |
| pharmaceutical | words from other pages' text (control) | 2250 | 3.919 | 4.040 | 4.197 |
| bathing | labels | 107 | 1.824 | 1.439 | 1.463 |
| bathing | words from other pages' text (control) | 1070 | 8.363 | 8.389 | 8.159 |
| zodiac | labels | 310 | 1.400 | 1.178 | 1.168 |
| zodiac | words from other pages' text (control) | 3100 | 2.420 | 3.808 | 3.525 |
| cosmological | labels | 170 | 1.633 | 2.540 | 0.769 |
| cosmological | words from other pages' text (control) | 1700 | 1.564 | 2.318 | 2.201 |
| astronomical | labels | 126 | 0.486 | 0.467 | nan |
| astronomical | words from other pages' text (control) | 1260 | 1.427 | 2.896 | nan |
| text | labels | 19 | 1.790 | nan | 1.084 |
| text | words from other pages' text (control) | 190 | 3.490 | 5.130 | 5.134 |

## One glyph different

| section | probes | n | same page: near | same sheet, other page: near | same section, other sheets: near |
|---|---|---|---|---|---|
| pharmaceutical | labels | 225 | 4.929 | 4.940 | 4.415 |
| pharmaceutical | words from other pages' text (control) | 2250 | 14.187 | 13.974 | 14.367 |
| bathing | labels | 107 | 9.813 | 9.626 | 8.456 |
| bathing | words from other pages' text (control) | 1070 | 27.069 | 27.186 | 26.812 |
| zodiac | labels | 310 | 7.078 | 6.997 | 8.488 |
| zodiac | words from other pages' text (control) | 3100 | 10.878 | 11.450 | 10.388 |
| cosmological | labels | 170 | 9.965 | 10.091 | 5.306 |
| cosmological | words from other pages' text (control) | 1700 | 8.327 | 8.985 | 8.376 |
| astronomical | labels | 126 | 5.634 | 3.579 | nan |
| astronomical | words from other pages' text (control) | 1260 | 7.596 | 7.616 | nan |
| text | labels | 19 | 10.204 | nan | 9.839 |
| text | words from other pages' text (control) | 190 | 19.445 | 20.011 | 20.809 |

## Raw counts

| section | label tokens | hits on own page | hits elsewhere in section | labels found anywhere in running text |
|---|---|---|---|---|
| pharmaceutical | 225 | 20 | 306 | 0.467 |
| bathing | 107 | 63 | 924 | 0.701 |
| zodiac | 310 | 35 | 315 | 0.574 |

## How labels are built

| words | n | start o | start q | start ch/sh | start d | end y | end n |
|---|---|---|---|---|---|---|---|
| labels | 965 | 0.602 | 0.010 | 0.091 | 0.086 | 0.436 | 0.082 |
| running text (4+ letters) | 30341 | 0.216 | 0.168 | 0.285 | 0.075 | 0.450 | 0.192 |

## Labels starting with o-, read three ways (exact hits per 1000 text words)

| labels starting with o- | section | n | same page: exact | same sheet, other page: exact | same section, other sheets: exact |
|---|---|---|---|---|---|
| as written | pharmaceutical | 95 | 0.282 | 0.297 | 0.135 |
| as written | bathing | 58 | 1.684 | 1.247 | 1.232 |
| as written | zodiac | 197 | 1.383 | 1.261 | 1.076 |
| o- removed | pharmaceutical | 95 | 0.000 | 0.094 | 0.043 |
| o- removed | bathing | 58 | 0.598 | 0.495 | 0.481 |
| o- removed | zodiac | 197 | 0.503 | 0.516 | 0.298 |
| o- read as qo- | pharmaceutical | 95 | 0.352 | 0.156 | 0.220 |
| o- read as qo- | bathing | 58 | 3.748 | 2.861 | 2.419 |
| o- read as qo- | zodiac | 197 | 0.126 | 0.024 | 0.069 |

## Permutation test (labels moved to random pages of their section; pharmaceutical, bathing, zodiac)

| probes | n | own-page hits | if pages were random (mean) | p |
|---|---|---|---|---|
| all labels, as written | 642 | 118 | 101.163 | 0.104 |
| o- labels, as written | 350 | 57 | 44.859 | 0.087 |
| o- labels read as qo- | 350 | 76 | 52.157 | 0.040 |
