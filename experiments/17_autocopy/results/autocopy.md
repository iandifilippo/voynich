# 17 self-citation generator

## summary

| text | distance | core | h2 | hapax | edge | word_len | cohesion | line_first | worst |
|---|---|---|---|---|---|---|---|---|---|
| VMS Currier A | 0.324 | 0.095 | 2.141 | 0.693 | 0.130 | 4.774 | 1.826 | 0.138 | repeat_rate -0.9, line_cohesion -0.6, line_last_jsd -0.3, edge_coupling -0.2 |
| VMS Currier B | 1.234 | 0.710 | 1.937 | 0.684 | 0.245 | 4.950 | 1.951 | 0.178 | line_last_jsd -2.8, line_first_jsd +2.6, edge_coupling +1.4, zipf -1.1 |
| VMS all | 0.000 | 0.000 | 2.154 | 0.686 | 0.147 | 4.714 | 1.959 | 0.141 | line_last_jsd -0.0, line_first_jsd +0.0, hapax_ratio +0.0, mattr500 +0.0 |
| autocopy A (mean of 8) | 2.449 | 1.032 | 2.351 | 0.542 | 0.009 | 4.600 | 1.449 | 0.123 | line_last_jsd -7.5, line_cohesion -2.3, hapax_ratio -2.0, edge_coupling -2.0 |
| autocopy B (mean of 8) | 2.461 | 0.965 | 2.223 | 0.546 | 0.013 | 5.049 | 2.009 | 0.098 | line_last_jsd -7.3, line_first_jsd -3.0, repeat_rate -2.4, hapax_ratio -1.9 |

## repeats per 1000 adjacent pairs (null = words shuffled within their line)

| text | exact | exact_null | near | near_null |
|---|---|---|---|---|
| VMS Currier A | 9.820 | 9.450 | 41.038 | 31.779 |
| VMS Currier B | 9.221 | 9.329 | 33.728 | 30.579 |
| VMS all | 9.371 | 9.230 | 36.020 | 30.742 |
| autocopy A (mean of 8) | 8.816 | 11.466 | 40.958 | 35.249 |
| autocopy B (mean of 8) | 7.793 | 8.604 | 36.838 | 28.151 |

## spread across seeds

| text | distance_sd | core_sd | h2_sd | edge_sd | hapax_sd |
|---|---|---|---|---|---|
| autocopy A (mean of 8) | 0.146 | 0.017 | 0.046 | 0.003 | 0.006 |
| autocopy B (mean of 8) | 0.196 | 0.048 | 0.046 | 0.003 | 0.011 |

## line-initial glyph shares

| text | s | d | t | k | p | q | o | y |
|---|---|---|---|---|---|---|---|---|
| VMS B | 0.162 | 0.154 | 0.100 | 0.015 | 0.120 | 0.127 | 0.110 | 0.144 |
| autocopy B seed 1 | 0.170 | 0.069 | 0.024 | 0.066 | 0.082 | 0.022 | 0.081 | 0.069 |

## sample (B, seed 1, first 12 lines)

```
polchedy qokeol okain checthy oteey lshedy okain qokain qokalshedy oteys
qokeal ar chear ytchy qokear ar arar okeeal al dain eom
okedy cheal or sheor sheol daiin chedain or al dain eor
daiin cheal chdaiin cheal sheal al cheol daiiir daiin
qokain kain ar
pypedy cheeal chal ol arar saiin shecphy qopaiin arar
daiin eear chedy sheal al dail chedy cheeckhy lokedy
daiiir aiiir qokeear chesheal sail sheckho daiin dain
daiiir qokain kain ar daiiir sheeol arar ol al aiin san
daiiir echy
fykain ol chedy okain shecfhy farar lsheokain ar ar edy
eshy sheckho eckho saiiir dair ckheeol chdy qokaiin dar
```
