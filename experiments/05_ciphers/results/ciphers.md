# 05 cipher and generator benchmark

Lower distance = more VMS-like. Distance is the RMS of 13 z-scores (scale = spread among 18 historical texts).

VMS reference: h2 2.15, hapax 0.69, edge 0.147, line_first 0.141, cohesion 1.96

`core` drops the four line-level metrics (line_first, line_last, cohesion, repeat_rate), so it only looks at glyphs and words.

## sorted by full distance

| candidate | plaintext | distance | core | h2 | hapax | edge | line_first | cohesion | worst |
|---|---|---|---|---|---|---|---|---|---|
| VMS Currier A | - | 0.324 | 0.095 | 2.141 | 0.693 | 0.130 | 0.138 | 1.826 | repeat_rate -0.9, line_cohesion -0.6, line_last_jsd -0.3 |
| VMS (later pages) | - | 1.042 | 0.614 | 1.972 | 0.684 | 0.235 | 0.155 | 2.065 | line_last_jsd -3.0, edge_coupling +1.2, line_first_jsd +1.0 |
| VMS Currier B | - | 1.234 | 0.710 | 1.937 | 0.684 | 0.245 | 0.178 | 1.951 | line_last_jsd -2.8, line_first_jsd +2.6, edge_coupling +1.4 |
| control: VMS words shuffled | - | 4.480 | 0.718 | 2.111 | 0.686 | 0.001 | 0.003 | 0.967 | line_first_jsd -9.8, line_last_jsd -9.6, repeat_rate -6.9 |
| plain | italian | 4.984 | 1.685 | 3.086 | 0.716 | 0.091 | 0.004 | 1.023 | line_last_jsd -9.7, line_first_jsd -9.7, repeat_rate -9.4 |
| substitution | italian | 4.984 | 1.685 | 3.086 | 0.716 | 0.091 | 0.004 | 1.023 | line_last_jsd -9.7, line_first_jsd -9.7, repeat_rate -9.4 |
| naibbe_like | latin | 4.987 | 2.220 | 2.241 | 0.246 | 0.002 | 0.002 | 0.865 | line_last_jsd -9.9, line_first_jsd -9.8, repeat_rate -7.7 |
| naibbe_like | spanish | 4.993 | 2.098 | 2.239 | 0.291 | 0.003 | 0.004 | 0.791 | line_last_jsd -9.9, line_first_jsd -9.7, repeat_rate -8.0 |
| naibbe_like | italian | 5.021 | 2.331 | 2.264 | 0.228 | -0.000 | 0.001 | 0.802 | line_last_jsd -10.0, line_first_jsd -9.9, repeat_rate -7.3 |
| plain | english | 5.048 | 1.877 | 3.185 | 0.630 | 0.071 | 0.003 | 1.041 | line_first_jsd -9.8, repeat_rate -9.8, line_last_jsd -9.5 |
| substitution | english | 5.048 | 1.877 | 3.185 | 0.630 | 0.071 | 0.003 | 1.041 | line_first_jsd -9.8, repeat_rate -9.8, line_last_jsd -9.5 |
| plain | latin_med | 5.055 | 1.952 | 3.254 | 0.638 | 0.065 | 0.004 | 1.190 | repeat_rate -9.9, line_first_jsd -9.7, line_last_jsd -9.7 |
| substitution | latin_med | 5.055 | 1.952 | 3.254 | 0.638 | 0.065 | 0.004 | 1.190 | repeat_rate -9.9, line_first_jsd -9.7, line_last_jsd -9.7 |
| syllable_code | english | 5.074 | 2.175 | 2.277 | 0.412 | 0.028 | 0.005 | 0.981 | line_last_jsd -9.8, line_first_jsd -9.6, repeat_rate -9.1 |
| naibbe_like | english | 5.085 | 2.058 | 2.275 | 0.298 | 0.001 | 0.002 | 0.842 | line_last_jsd -9.9, line_first_jsd -9.8, repeat_rate -8.8 |
| plain | spanish | 5.112 | 1.877 | 3.154 | 0.728 | 0.125 | 0.007 | 0.938 | repeat_rate -10.0, line_last_jsd -9.8, line_first_jsd -9.5 |
| substitution | spanish | 5.112 | 1.877 | 3.154 | 0.728 | 0.125 | 0.007 | 0.938 | repeat_rate -10.0, line_last_jsd -9.8, line_first_jsd -9.5 |
| syllable_code | spanish | 5.144 | 2.624 | 2.272 | 0.386 | 0.022 | 0.004 | 0.817 | line_last_jsd -9.9, line_first_jsd -9.7, repeat_rate -8.0 |
| naibbe_like | latin_med | 5.172 | 2.350 | 2.254 | 0.221 | 0.002 | 0.003 | 0.797 | line_last_jsd -9.8, line_first_jsd -9.8, repeat_rate -8.8 |
| plain | latin | 5.239 | 2.101 | 3.339 | 0.669 | 0.054 | 0.005 | 0.719 | repeat_rate -10.0, line_first_jsd -9.7, line_last_jsd -9.6 |
| substitution | latin | 5.239 | 2.101 | 3.339 | 0.669 | 0.054 | 0.005 | 0.719 | repeat_rate -10.0, line_first_jsd -9.7, line_last_jsd -9.6 |
| syllable_code | latin_med | 5.259 | 2.790 | 2.236 | 0.322 | 0.018 | 0.002 | 1.081 | line_first_jsd -9.9, line_last_jsd -9.7, repeat_rate -9.0 |
| syllable_code | latin | 5.305 | 2.460 | 2.228 | 0.308 | 0.009 | 0.002 | 0.787 | line_last_jsd -10.0, line_first_jsd -9.8, repeat_rate -9.3 |
| syllable_code | italian | 5.313 | 2.915 | 2.237 | 0.376 | 0.019 | 0.001 | 0.858 | line_last_jsd -10.0, line_first_jsd -9.9, repeat_rate -8.2 |
| control: VMS glyphs shuffled | - | 5.317 | 3.133 | 3.797 | 0.950 | 0.000 | 0.005 | 2.031 | line_first_jsd -9.7, repeat_rate -9.7, line_last_jsd -9.6 |
| homophonic | english | 5.388 | 2.882 | 3.377 | 0.893 | 0.016 | 0.004 | 0.888 | repeat_rate -10.0, line_first_jsd -9.7, line_last_jsd -9.2 |
| homophonic | italian | 5.553 | 3.245 | 3.322 | 0.911 | 0.022 | 0.004 | 1.069 | repeat_rate -10.0, line_last_jsd -9.8, line_first_jsd -9.7 |
| homophonic | spanish | 5.567 | 3.145 | 3.343 | 0.905 | 0.035 | 0.003 | 0.878 | repeat_rate -10.0, line_first_jsd -9.8, line_last_jsd -9.7 |
| homophonic | latin_med | 5.670 | 3.503 | 3.348 | 0.944 | 0.013 | 0.004 | 1.073 | repeat_rate -10.0, line_last_jsd -9.8, line_first_jsd -9.7 |
| verbose | english | 5.673 | 3.505 | 2.128 | 0.630 | 0.011 | 0.001 | 1.041 | line_first_jsd -9.9, line_last_jsd -9.8, repeat_rate -9.8 |
| verbose | spanish | 5.880 | 3.845 | 2.099 | 0.728 | 0.020 | 0.003 | 0.938 | repeat_rate -10.0, line_last_jsd -9.9, line_first_jsd -9.8 |
| verbose | italian | 5.912 | 4.095 | 2.087 | 0.716 | 0.019 | 0.002 | 1.023 | line_last_jsd -10.0, line_first_jsd -9.8, word_len +9.5 |
| homophonic | latin | 6.014 | 3.784 | 3.370 | 0.955 | 0.008 | 0.002 | 0.423 | repeat_rate -10.0, line_first_jsd -9.8, line_last_jsd -9.8 |
| verbose | latin_med | 6.021 | 4.312 | 2.137 | 0.638 | 0.027 | 0.001 | 1.190 | word_len +10.8, line_first_jsd -9.9, repeat_rate -9.9 |
| verbose | latin | 6.370 | 4.707 | 2.142 | 0.669 | 0.015 | 0.002 | 0.719 | word_len +12.2, repeat_rate -10.0, line_last_jsd -9.9 |
| self_citation (seed 2) | - | 12.090 | 3.410 | 1.244 | 0.158 | 0.092 | 0.002 | 5.246 | repeat_rate +37.1, line_cohesion +15.0, line_first_jsd -9.9 |
| self_citation (seed 1) | - | 17.295 | 3.945 | 0.953 | 0.237 | 0.010 | 0.001 | 14.518 | line_cohesion +57.2, repeat_rate +16.6, line_last_jsd -9.9 |
| self_citation (seed 0) | - | 17.943 | 3.103 | 1.345 | 0.294 | 0.032 | 0.002 | 13.376 | line_cohesion +52.0, repeat_rate +34.6, line_last_jsd -10.0 |

## sorted by core distance

| candidate | plaintext | distance | core | h2 | hapax | edge | line_first | cohesion | worst |
|---|---|---|---|---|---|---|---|---|---|
| VMS Currier A | - | 0.324 | 0.095 | 2.141 | 0.693 | 0.130 | 0.138 | 1.826 | repeat_rate -0.9, line_cohesion -0.6, line_last_jsd -0.3 |
| VMS (later pages) | - | 1.042 | 0.614 | 1.972 | 0.684 | 0.235 | 0.155 | 2.065 | line_last_jsd -3.0, edge_coupling +1.2, line_first_jsd +1.0 |
| VMS Currier B | - | 1.234 | 0.710 | 1.937 | 0.684 | 0.245 | 0.178 | 1.951 | line_last_jsd -2.8, line_first_jsd +2.6, edge_coupling +1.4 |
| control: VMS words shuffled | - | 4.480 | 0.718 | 2.111 | 0.686 | 0.001 | 0.003 | 0.967 | line_first_jsd -9.8, line_last_jsd -9.6, repeat_rate -6.9 |
| plain | italian | 4.984 | 1.685 | 3.086 | 0.716 | 0.091 | 0.004 | 1.023 | line_last_jsd -9.7, line_first_jsd -9.7, repeat_rate -9.4 |
| substitution | italian | 4.984 | 1.685 | 3.086 | 0.716 | 0.091 | 0.004 | 1.023 | line_last_jsd -9.7, line_first_jsd -9.7, repeat_rate -9.4 |
| plain | spanish | 5.112 | 1.877 | 3.154 | 0.728 | 0.125 | 0.007 | 0.938 | repeat_rate -10.0, line_last_jsd -9.8, line_first_jsd -9.5 |
| substitution | spanish | 5.112 | 1.877 | 3.154 | 0.728 | 0.125 | 0.007 | 0.938 | repeat_rate -10.0, line_last_jsd -9.8, line_first_jsd -9.5 |
| plain | english | 5.048 | 1.877 | 3.185 | 0.630 | 0.071 | 0.003 | 1.041 | line_first_jsd -9.8, repeat_rate -9.8, line_last_jsd -9.5 |
| substitution | english | 5.048 | 1.877 | 3.185 | 0.630 | 0.071 | 0.003 | 1.041 | line_first_jsd -9.8, repeat_rate -9.8, line_last_jsd -9.5 |
| plain | latin_med | 5.055 | 1.952 | 3.254 | 0.638 | 0.065 | 0.004 | 1.190 | repeat_rate -9.9, line_first_jsd -9.7, line_last_jsd -9.7 |
| substitution | latin_med | 5.055 | 1.952 | 3.254 | 0.638 | 0.065 | 0.004 | 1.190 | repeat_rate -9.9, line_first_jsd -9.7, line_last_jsd -9.7 |
| naibbe_like | english | 5.085 | 2.058 | 2.275 | 0.298 | 0.001 | 0.002 | 0.842 | line_last_jsd -9.9, line_first_jsd -9.8, repeat_rate -8.8 |
| naibbe_like | spanish | 4.993 | 2.098 | 2.239 | 0.291 | 0.003 | 0.004 | 0.791 | line_last_jsd -9.9, line_first_jsd -9.7, repeat_rate -8.0 |
| plain | latin | 5.239 | 2.101 | 3.339 | 0.669 | 0.054 | 0.005 | 0.719 | repeat_rate -10.0, line_first_jsd -9.7, line_last_jsd -9.6 |
| substitution | latin | 5.239 | 2.101 | 3.339 | 0.669 | 0.054 | 0.005 | 0.719 | repeat_rate -10.0, line_first_jsd -9.7, line_last_jsd -9.6 |
| syllable_code | english | 5.074 | 2.175 | 2.277 | 0.412 | 0.028 | 0.005 | 0.981 | line_last_jsd -9.8, line_first_jsd -9.6, repeat_rate -9.1 |
| naibbe_like | latin | 4.987 | 2.220 | 2.241 | 0.246 | 0.002 | 0.002 | 0.865 | line_last_jsd -9.9, line_first_jsd -9.8, repeat_rate -7.7 |
| naibbe_like | italian | 5.021 | 2.331 | 2.264 | 0.228 | -0.000 | 0.001 | 0.802 | line_last_jsd -10.0, line_first_jsd -9.9, repeat_rate -7.3 |
| naibbe_like | latin_med | 5.172 | 2.350 | 2.254 | 0.221 | 0.002 | 0.003 | 0.797 | line_last_jsd -9.8, line_first_jsd -9.8, repeat_rate -8.8 |
| syllable_code | latin | 5.305 | 2.460 | 2.228 | 0.308 | 0.009 | 0.002 | 0.787 | line_last_jsd -10.0, line_first_jsd -9.8, repeat_rate -9.3 |
| syllable_code | spanish | 5.144 | 2.624 | 2.272 | 0.386 | 0.022 | 0.004 | 0.817 | line_last_jsd -9.9, line_first_jsd -9.7, repeat_rate -8.0 |
| syllable_code | latin_med | 5.259 | 2.790 | 2.236 | 0.322 | 0.018 | 0.002 | 1.081 | line_first_jsd -9.9, line_last_jsd -9.7, repeat_rate -9.0 |
| homophonic | english | 5.388 | 2.882 | 3.377 | 0.893 | 0.016 | 0.004 | 0.888 | repeat_rate -10.0, line_first_jsd -9.7, line_last_jsd -9.2 |
| syllable_code | italian | 5.313 | 2.915 | 2.237 | 0.376 | 0.019 | 0.001 | 0.858 | line_last_jsd -10.0, line_first_jsd -9.9, repeat_rate -8.2 |
| self_citation (seed 0) | - | 17.943 | 3.103 | 1.345 | 0.294 | 0.032 | 0.002 | 13.376 | line_cohesion +52.0, repeat_rate +34.6, line_last_jsd -10.0 |
| control: VMS glyphs shuffled | - | 5.317 | 3.133 | 3.797 | 0.950 | 0.000 | 0.005 | 2.031 | line_first_jsd -9.7, repeat_rate -9.7, line_last_jsd -9.6 |
| homophonic | spanish | 5.567 | 3.145 | 3.343 | 0.905 | 0.035 | 0.003 | 0.878 | repeat_rate -10.0, line_first_jsd -9.8, line_last_jsd -9.7 |
| homophonic | italian | 5.553 | 3.245 | 3.322 | 0.911 | 0.022 | 0.004 | 1.069 | repeat_rate -10.0, line_last_jsd -9.8, line_first_jsd -9.7 |
| self_citation (seed 2) | - | 12.090 | 3.410 | 1.244 | 0.158 | 0.092 | 0.002 | 5.246 | repeat_rate +37.1, line_cohesion +15.0, line_first_jsd -9.9 |
| homophonic | latin_med | 5.670 | 3.503 | 3.348 | 0.944 | 0.013 | 0.004 | 1.073 | repeat_rate -10.0, line_last_jsd -9.8, line_first_jsd -9.7 |
| verbose | english | 5.673 | 3.505 | 2.128 | 0.630 | 0.011 | 0.001 | 1.041 | line_first_jsd -9.9, line_last_jsd -9.8, repeat_rate -9.8 |
| homophonic | latin | 6.014 | 3.784 | 3.370 | 0.955 | 0.008 | 0.002 | 0.423 | repeat_rate -10.0, line_first_jsd -9.8, line_last_jsd -9.8 |
| verbose | spanish | 5.880 | 3.845 | 2.099 | 0.728 | 0.020 | 0.003 | 0.938 | repeat_rate -10.0, line_last_jsd -9.9, line_first_jsd -9.8 |
| self_citation (seed 1) | - | 17.295 | 3.945 | 0.953 | 0.237 | 0.010 | 0.001 | 14.518 | line_cohesion +57.2, repeat_rate +16.6, line_last_jsd -9.9 |
| verbose | italian | 5.912 | 4.095 | 2.087 | 0.716 | 0.019 | 0.002 | 1.023 | line_last_jsd -10.0, line_first_jsd -9.8, word_len +9.5 |
| verbose | latin_med | 6.021 | 4.312 | 2.137 | 0.638 | 0.027 | 0.001 | 1.190 | word_len +10.8, line_first_jsd -9.9, repeat_rate -9.9 |
| verbose | latin | 6.370 | 4.707 | 2.142 | 0.669 | 0.015 | 0.002 | 0.719 | word_len +12.2, repeat_rate -10.0, line_last_jsd -9.9 |
