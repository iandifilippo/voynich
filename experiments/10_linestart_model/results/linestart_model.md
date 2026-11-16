# 10 linestart transformation

Positive r: word types that are missing from line starts are the same ones that turn up there with the glyph in front.

| set | glyph | types_tested | r | p | line_starts_with_g | of_which_g_plus_word |
|---|---|---|---|---|---|---|
| all | s | 785 | 0.130 | 0.000 | 599 | 327 |
| all | d | 785 | 0.158 | 0.000 | 624 | 551 |
| all | y | 785 | -0.080 | 0.977 | 590 | 393 |
| all | o | 785 | -0.019 | 0.701 | 547 | 377 |
| all | t | 785 | 0.097 | 0.000 | 391 | 265 |
| all | k | 785 | -0.071 | 0.996 | 104 | 54 |
| all | p | 785 | 0.070 | 0.007 | 375 | 219 |
| all | q | 785 | -0.133 | 0.997 | 529 | 422 |
| all | l | 785 | -0.087 | 0.998 | 69 | 57 |
| all | r | 785 | -0.152 | 0.998 | 12 | 7 |
| Currier A | s | 296 | 0.047 | 0.212 | 192 | 61 |
| Currier A | d | 296 | 0.015 | 0.334 | 231 | 196 |
| Currier A | y | 296 | -0.003 | 0.537 | 226 | 143 |
| Currier A | o | 296 | -0.194 | 0.998 | 267 | 158 |
| Currier A | t | 296 | 0.021 | 0.368 | 133 | 79 |
| Currier A | k | 296 | -0.164 | 0.998 | 64 | 36 |
| Currier A | p | 296 | -0.014 | 0.624 | 78 | 38 |
| Currier A | q | 296 | -0.142 | 0.979 | 210 | 136 |
| Currier A | l | 296 | -0.110 | 0.957 | 10 | 7 |
| Currier A | r | 296 | -0.010 | 0.619 | 2 | 1 |
| Currier B | s | 546 | 0.124 | 0.000 | 393 | 251 |
| Currier B | d | 546 | 0.168 | 0.000 | 376 | 324 |
| Currier B | y | 546 | -0.121 | 0.989 | 349 | 214 |
| Currier B | o | 546 | 0.049 | 0.120 | 269 | 177 |
| Currier B | t | 546 | 0.101 | 0.000 | 246 | 159 |
| Currier B | k | 546 | -0.082 | 0.960 | 38 | 16 |
| Currier B | p | 546 | 0.067 | 0.019 | 297 | 166 |
| Currier B | q | 546 | -0.105 | 0.999 | 314 | 253 |
| Currier B | l | 546 | -0.052 | 0.906 | 59 | 48 |
| Currier B | r | 546 | -0.150 | 1.000 | 9 | 5 |
| Takahashi (IT) | s | 800 | 0.116 | 0.000 | 592 | 338 |
| Takahashi (IT) | d | 800 | 0.143 | 0.001 | 623 | 552 |
| Takahashi (IT) | y | 800 | -0.053 | 0.923 | 581 | 403 |
| Takahashi (IT) | o | 800 | -0.005 | 0.514 | 538 | 368 |
| Takahashi (IT) | t | 800 | 0.102 | 0.000 | 393 | 261 |
| Takahashi (IT) | k | 800 | -0.078 | 0.998 | 105 | 61 |
| Takahashi (IT) | p | 800 | 0.077 | 0.005 | 378 | 226 |
| Takahashi (IT) | q | 800 | -0.168 | 1.000 | 528 | 418 |
| Takahashi (IT) | l | 800 | -0.087 | 0.997 | 68 | 57 |
| Takahashi (IT) | r | 800 | -0.138 | 0.998 | 16 | 11 |

## strongest pairs (all, by surplus)

- **s**: s+ain (def 3.8, sur 8.3), s+oiin (def 2.0, sur 6.2), s+aiin (def 7.6, sur 5.9), s+or (def 1.6, sur 4.3), s+ol (def 4.2, sur 4.1), s+ar (def 5.8, sur 3.8)
- **d**: d+aiin (def 7.6, sur 9.2), d+ain (def 3.8, sur 7.4), d+air (def 2.9, sur 5.6), d+shedy (def 6.5, sur 3.9), d+aiir (def 1.7, sur 3.3), d+shor (def -2.8, sur 2.6)
- **y**: y+tchedy (def -21.9, sur 5.0), y+cheeo (def -1.4, sur 4.3), y+teedy (def 1.4, sur 4.0), y+cheey (def 4.4, sur 3.7), y+cheo (def 2.0, sur 3.3), y+keeo (def 1.1, sur 3.3)
- **o**: o+tchol (def -2.9, sur 5.3), o+tchor (def -9.9, sur 4.3), o+ksho (def -2.9, sur 2.0), o+ain (def 3.8, sur 1.7), o+lcheol (def -1.4, sur 1.5), o+lkeey (def 1.8, sur 1.3)
- **t**: t+ol (def 4.2, sur 3.1), t+chedy (def 7.1, sur 3.0), t+sheeor (def 0.8, sur 2.5), t+odal (def 0.5, sur 2.3), t+oar (def -3.6, sur 2.2), t+oeedy (def 0.9, sur 2.2)
- **k**: k+cheeos (def 0.9, sur 1.1), k+odam (def 1.0, sur 1.0), k+olchdy (def 1.1, sur 0.9), k+chor (def 3.4, sur 0.8), k+chokchy (def 0.6, sur 0.7), k+oaiin (def -6.0, sur 0.7)
- **p**: p+chedar (def 2.1, sur 4.3), p+olaiin (def 0.5, sur 3.0), p+chedal (def 1.1, sur 2.9), p+chodain (def 1.0, sur 2.9), p+olal (def 0.8, sur 2.5), p+oar (def -3.6, sur 2.2)
- **q**: q+otchor (def -4.1, sur 6.7), q+otchy (def -0.1, sur 5.6), q+otor (def -0.2, sur 4.7), q+okchy (def -1.6, sur 4.4), q+ok (def 1.0, sur 4.0), q+okchor (def -1.0, sur 3.5)
- **l**: l+shes (def 0.8, sur 1.2), l+cheod (def 0.8, sur 1.1), l+shee (def 1.3, sur 0.8), l+sheody (def 2.0, sur 0.8), l+sho (def -5.8, sur 0.6), l+chdal (def 1.6, sur 0.5)
- **r**: r+oar (def -3.6, sur 1.1), r+oraiin (def 0.4, sur 0.5), r+olkeedy (def 1.0, sur 0.4), r+cheky (def 2.8, sur 0.3), r+ykal (def 1.1, sur 0.0), r+shol (def 0.7, sur 0.0)
