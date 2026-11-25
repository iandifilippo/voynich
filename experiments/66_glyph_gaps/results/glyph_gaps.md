# 66 spaces from the glyph map

## Gap widths (x-heights; 10/25/50/75/90th percentiles)

| gap | n | quantiles |
|---|---|---|
| letters inside a word (ligatures left out) | 87363 | [-0.13, 0.04, 0.17, 0.29, 0.45] |
| doubtful space (ZL ',') | 1304 | [0.33, 0.5, 0.64, 0.81, 1.0] |
| certain space (ZL '.'), all words | 21983 | [-0.92, 0.45, 1.22, 1.67, 2.19] |
| certain space, machine-drafted words, gap > 0 | 8461 | [0.72, 1.0, 1.36, 1.77, 2.35] |

Share of certain spaces with overlapping ink (gap < 0), by trust of the first word: auto 0.083, auto-checked 0.085, auto-placed 0.306, owner-answered 0.587, owner-traced 0.175

## Link across the boundary (excess mutual information, equal n)

| boundary | n | median gap | link (bits) | sd |
|---|---|---|---|---|
| doubtful space | 1304 | 0.636 | 0.638 |  |
| certain space, narrow | 2844 | 0.871 | 0.244 | 0.013 |
| certain space, mid | 2816 | 1.360 | 0.185 | 0.012 |
| certain space, wide | 2801 | 2.000 | 0.069 | 0.009 |

## Same, within each Currier language (each tercile at its own n)

| language | space | n | median gap | link (bits) |
|---|---|---|---|---|
| A | narrow | 1427 | 0.821 | 0.168 |
| A | mid | 1385 | 1.286 | 0.117 |
| A | wide | 1405 | 1.922 | 0.035 |
| B | narrow | 1353 | 0.917 | 0.367 |
| B | mid | 1357 | 1.422 | 0.273 |
| B | wide | 1337 | 2.043 | 0.129 |

## The qo- rhythm by space width (over the base rate of qo-)

| space | n | P(qo) | after ch/sh-y | after -n/-l/-r |
|---|---|---|---|---|
| narrow | 2844 | 0.147 | 1.782 | 0.425 |
| mid | 2816 | 0.189 | 1.757 | 0.440 |
| wide | 2801 | 0.125 | 1.657 | 0.572 |

## Wide gaps inside words (3687 of 87363, 0.042)

| letters | wide (>= 0.6) | all | share wide |
|---|---|---|---|
| q-o | 332 | 4150 | 0.080 |
| o-k | 216 | 4363 | 0.050 |
| o-r | 161 | 1874 | 0.086 |
| d-y | 144 | 4507 | 0.032 |
| d-a | 139 | 2729 | 0.051 |
| o-t | 136 | 2576 | 0.053 |
| h-e | 134 | 5005 | 0.027 |
| o-l | 130 | 3646 | 0.036 |
