# 34 slots

## Coverage and shared information

| text | parse | words | parsed | distinct words parsed | sum of slot entropies | word entropy | shared (bits) | shared if independent |
|---|---|---|---|---|---|---|---|---|
| VMS, Currier A | early slots first | 11231 | 0.790 | 0.471 | 13.064 | 8.650 | 4.414 | 1.676 |
| VMS, Currier A | late slots first | 11231 | 0.790 | 0.471 | 12.710 | 8.650 | 4.060 | 1.510 |
| VMS, Currier B | early slots first | 23084 | 0.842 | 0.477 | 14.010 | 8.854 | 5.156 | 1.507 |
| VMS, Currier B | late slots first | 23084 | 0.842 | 0.477 | 13.636 | 8.854 | 4.782 | 1.305 |
| copying model | early slots first | 35147 | 0.575 | 0.282 | 13.597 | 8.333 | 5.264 | 1.431 |
| Naibbe cipher of Pliny | early slots first | 30000 | 0.921 | 0.803 | 14.846 | 9.703 | 5.142 | 1.627 |

## Held-out bits per word

| text | independent slots | chain | whole word so far |
|---|---|---|---|
| VMS, Currier A | 13.071 | 9.380 | 9.261 |
| VMS, Currier B | 14.013 | 9.536 | 9.288 |
| copying model | 13.600 | 9.535 | 8.713 |
| Naibbe cipher of Pliny | 14.848 | 10.884 | 10.254 |

## Does the start know the end?

| text | I(prefix; suffix | core) | suffix shuffled within core | excess (bits) | p |
|---|---|---|---|---|
| VMS, Currier A | 0.412 | 0.196 | 0.216 | 0.005 |
| VMS, Currier B | 0.330 | 0.130 | 0.200 | 0.005 |
| copying model | 0.443 | 0.074 | 0.369 | 0.005 |
| Naibbe cipher of Pliny | 0.516 | 0.151 | 0.365 | 0.005 |

## What an independent device would write

| text | distinct words, real | distinct words, independent device | device words that exist in the text (types) | device words that exist (tokens) | real words the device made (types) |
|---|---|---|---|---|---|
| VMS, Currier A | 1515 | 4470 | 0.119 | 0.281 | 0.350 |
| VMS, Currier B | 2284 | 9704 | 0.084 | 0.195 | 0.359 |
| copying model | 1565 | 9154 | 0.067 | 0.195 | 0.390 |
| Naibbe cipher of Pliny | 4222 | 14766 | 0.100 | 0.185 | 0.350 |

## Shared information between pairs of slots, by distance (bits, bias removed)

| text | 1 apart | 2 apart | 3 apart | 4 apart | 6 apart | 8 apart | all pairs | pairs 4+ apart, share |
|---|---|---|---|---|---|---|---|---|
| VMS, Currier A | 1.542 | 1.283 | 0.570 | 0.338 | 0.202 | 0.208 | 4.666 | 0.272 |
| VMS, Currier B | 2.232 | 1.846 | 1.127 | 0.621 | 0.187 | 0.069 | 6.738 | 0.228 |
| copying model | 2.069 | 1.597 | 1.161 | 0.982 | 0.415 | 0.155 | 7.549 | 0.361 |
| Naibbe cipher of Pliny | 2.179 | 1.644 | 1.008 | 0.462 | 0.079 | 0.047 | 5.826 | 0.171 |

## Strongest pairs

| text | slots | apart | bits |
|---|---|---|---|
| VMS, Currier A | o/a  x  d/l/r/m/n | 2 | 0.862 |
| VMS, Currier A | iii/ii/i  x  d/l/r/m/n | 1 | 0.550 |
| VMS, Currier A | o/a  x  iii/ii/i | 1 | 0.298 |
| VMS, Currier A | d/l/r/m/n  x  y | 1 | 0.298 |
| VMS, Currier A | o/a  x  y | 3 | 0.214 |
| VMS, Currier A | q/s/d  x  y/o | 1 | 0.200 |
| VMS, Currier A | q/s/d  x  t/k/p/f | 3 | 0.172 |
| VMS, Currier A | y/o  x  t/k/p/f | 2 | 0.165 |
| VMS, Currier B | o/a  x  d/l/r/m/n | 2 | 0.950 |
| VMS, Currier B | iii/ii/i  x  d/l/r/m/n | 1 | 0.613 |
| VMS, Currier B | d/l/r/m/n  x  y | 1 | 0.470 |
| VMS, Currier B | o/a  x  y | 3 | 0.417 |
| VMS, Currier B | o/a  x  iii/ii/i | 1 | 0.310 |
| VMS, Currier B | eee/ee/e  x  y | 5 | 0.275 |
| VMS, Currier B | q/s/d  x  y/o | 1 | 0.271 |
| VMS, Currier B | y/o  x  t/k/p/f | 2 | 0.234 |
