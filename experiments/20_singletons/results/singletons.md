# 20 singletons

## how many, and what they look like (first 10 000 words)

| text | types | singleton_share_of_types | one_edit_from_known | two_known_joined | neither | neither_per_1000_tokens | len_singleton | len_other |
|---|---|---|---|---|---|---|---|---|
| VMS Currier A | 2975 | 0.693 | 0.635 | 0.145 | 0.221 | 45.486 | 6.339 | 4.368 |
| VMS Currier B | 2302 | 0.684 | 0.627 | 0.148 | 0.225 | 35.500 | 6.339 | 4.690 |
| VMS B, smart commas | 2389 | 0.676 | 0.634 | 0.140 | 0.226 | 36.493 | 6.371 | 4.843 |
| copying model (B) | 2508 | 0.553 | 0.658 | 0.124 | 0.218 | 30.282 | 6.630 | 4.813 |
| copying model (A) | 2185 | 0.539 | 0.664 | 0.110 | 0.226 | 26.592 | 6.329 | 4.635 |
| Latin (Aix) | 3822 | 0.669 | 0.170 | 0.011 | 0.819 | 209.233 | 8.426 | 5.415 |
| Italian (Rettorica) | 2763 | 0.717 | 0.184 | 0.260 | 0.556 | 110.112 | 9.016 | 4.094 |
| Naibbe (Pliny) | 2981 | 0.576 | 0.813 | 0.024 | 0.162 | 27.875 | 6.045 | 5.061 |

`one_edit_from_known`: one glyph added, dropped or changed from a word that occurs 2+ times in the same sample. `two_known_joined`: not that, but splits into two such words. 

## where they sit in the line (share of words in that position that are singletons)

| text | rate_first | rate_middle | rate_last |
|---|---|---|---|
| VMS Currier A | 0.289 | 0.171 | 0.287 |
| VMS Currier B | 0.265 | 0.129 | 0.240 |
| VMS B, smart commas | 0.273 | 0.133 | 0.237 |
| copying model (B) | 0.289 | 0.119 | 0.112 |
| copying model (A) | 0.280 | 0.100 | 0.074 |
| Latin (Aix) | 0.242 | 0.258 | 0.248 |
| Italian (Rettorica) | 0.198 | 0.200 | 0.187 |
| Naibbe (Pliny) | 0.205 | 0.173 | 0.086 |

## VMS, whole manuscript

| position | words | singleton_rate | mean_len |
|---|---|---|---|
| paragraph-opening word | 740 | 0.473 | 6.341 |
| other line-first words | 3390 | 0.169 | 5.240 |
| rest of paragraph text | 30733 | 0.119 | 4.929 |
| labels | 1163 | 0.363 | 5.279 |

Paragraph openers hold 6.3% of all singletons, labels 7.6%.

## how VMS singletons differ from the nearest known word, by line position

| language | position | singletons | added_start | added_inside | added_end | changed_start | changed_inside | changed_end | dropped_start | dropped_inside | dropped_end |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | first | 428 | 0.402 | 0.222 | 0.070 | 0.201 | 0.241 | 0.121 | 0.019 | 0.110 | 0.023 |
| A | middle | 1326 | 0.186 | 0.329 | 0.109 | 0.146 | 0.316 | 0.171 | 0.032 | 0.097 | 0.040 |
| A | last | 429 | 0.145 | 0.210 | 0.191 | 0.114 | 0.217 | 0.184 | 0.028 | 0.077 | 0.023 |
| B | first | 618 | 0.383 | 0.249 | 0.040 | 0.217 | 0.235 | 0.128 | 0.019 | 0.083 | 0.029 |
| B | middle | 2034 | 0.222 | 0.374 | 0.069 | 0.177 | 0.341 | 0.159 | 0.036 | 0.119 | 0.040 |
| B | last | 589 | 0.187 | 0.221 | 0.154 | 0.129 | 0.277 | 0.154 | 0.022 | 0.085 | 0.019 |

Share of singletons in that position that are a known word with one glyph added / changed / dropped at the start, inside or at the end (a singleton can count in several columns).

## which glyph is added at the edge

| language | position | side | n | glyphs |
|---|---|---|---|---|
| A | first | start | 172 | y 21%, o 21%, t 12%, s 10%, d 9%, p 8%, k 6%, f 5%, q 5%, l 2%, c 1%, r 1% |
| A | last | end | 82 | y 21%, d 21%, g 17%, s 13%, o 9%, m 9%, a 4%, l 4%, u 1%, n 1%, r 1% |
| A | middle | start | 246 | o 14%, q 13%, d 11%, k 10%, t 9%, s 8%, y 8%, l 7%, c 6%, f 4%, e 4%, p 3%, r 2% |
| A | middle | end | 145 | y 26%, s 17%, d 16%, l 11%, o 9%, r 5%, m 4%, g 2%, t 2%, e 1%, p 1%, k 1%, n 1% |
| B | first | start | 237 | p 21%, t 20%, y 16%, s 13%, d 10%, o 6%, l 4%, k 3%, f 3%, a 1%, q 1%, r 1%, x 0 |
| B | last | end | 91 | y 35%, s 12%, r 10%, g 9%, d 9%, m 8%, o 7%, l 7%, n 2%, c 1%, f 1% |
| B | middle | start | 451 | l 16%, o 15%, q 12%, d 10%, y 9%, s 6%, k 6%, r 6%, a 6%, t 6%, f 4%, p 3%, e 2% |
| B | middle | end | 141 | y 26%, s 16%, o 12%, d 9%, r 9%, l 6%, k 5%, a 4%, p 3%, t 3%, e 2%, x 1%, f 1%, |
