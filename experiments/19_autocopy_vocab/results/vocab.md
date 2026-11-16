# 19 copying model: vocabulary

| model | q | distance | core | hapax | mattr | h2 | edge | cohesion | near | near_null | worst |
|---|---|---|---|---|---|---|---|---|---|---|---|
| VMS Currier B | None | 1.234 |  | 0.684 | 0.535 | 1.937 | 0.245 | 1.951 | 33.728 | 30.508 |  |
| copying + habit | 0.000 | 2.424 | 0.706 | 0.551 | 0.564 | 2.187 | 0.115 | 1.988 | 33.984 | 27.905 | line_last_jsd -7.0, repeat_rate -3.3, line_first_jsd -2.9 |
| copying + habit | 0.300 | 2.780 | 0.687 | 0.561 | 0.590 | 2.237 | 0.115 | 1.946 | 29.101 | 25.300 | line_last_jsd -7.6, repeat_rate -5.3, line_first_jsd -3.3 |
| copying + habit | 0.600 | 2.493 | 0.562 | 0.594 | 0.595 | 2.231 | 0.106 | 1.656 | 28.896 | 27.051 | line_last_jsd -6.5, repeat_rate -4.7, line_first_jsd -2.9 |
| copying + habit | 0.900 | 2.862 | 0.558 | 0.593 | 0.599 | 2.181 | 0.117 | 1.667 | 28.594 | 27.189 | line_last_jsd -7.4, repeat_rate -5.7, line_first_jsd -3.5 |

`q`: probability of one extra glyph substitution per word. `near`/`near_null`: near-repeats per 1000 adjacent pairs, as written and with words shuffled within lines (20 shuffles).
