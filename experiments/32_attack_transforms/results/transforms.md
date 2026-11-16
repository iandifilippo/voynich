# 32 attack: transformed plaintext

## can the solver read each variant? (held-out text, 100 homophones)

| language | written | letters right | gap | in real words | real text in words | sample |
|---|---|---|---|---|---|---|
| Latin | no vowels | 0.919 | 0.016 | 0.295 | 0.319 | lbrt f dhstr hrslstn dpdtnsllr cp prmm sqnts prs#ncpt llr prss dpdtns hrslstn rl |
| Latin | letters sorted | 0.953 | 0.018 | 0.247 | 0.296 | aaelrt eo aahiiiorstv aaeehiilmnoorsty bdeeeiiiilnoprstv acip i eimmoopru eeinqs |
| Italian | no vowels | 0.981 | 0.002 | 0.455 | 0.459 | r chrtr l t vnnr fs n n nc#grpp ch vnn chmt grp r frnc l fbbr#l gvrn frncs nz n  |
| Latin | backwards | 0.998 | 0.003 | 0.263 | 0.263 | trebla fo airotsihxia eanatimolosoreih rebilsinoitidepxe paci i muimeoorp sitneu |
| Italian | letters sorted | 0.969 | 0.014 | 0.548 | 0.605 | eln aeginno l air aceenr aaevv ddeeiinnpt art ciu#iilopt e aeiinssstt di loov e  |
| Italian | backwards | 1.000 | -0.000 | 0.587 | 0.587 | len oianneg l ria ecnarf aveva itnednepid art iuc#itolip e itnetsissa id olov e  |
| German | no vowels | 1.000 | -0.000 | 0.483 | 0.483 | d klnst glcn snd s chrl nd trtn mt#bsndrr rmlchr nrdnng f n bsndrht wst d mnsr#p |
| German | letters sorted | 0.986 | 0.007 | 0.489 | 0.528 | eein bdeeehinorst eistw dei aaeimnorsu ilnopr afu deenr aegimnoppru#ein adeeknrs |
| Hebrew | plain | 1.000 | 0.000 | 0.721 | 0.721 | avbvlym wvvh ork lwywyj od xcy mwkr yvmv wl#pvol obvr hhwjjpvj baspj hom aj hxvq |
| Arabic | plain | 1.000 | 0.000 | 0.717 | 0.717 | hmas d obd allh ozam alanftah algrby oly hrkh#hmas brnamj ma uraa alxbr qnah alj |
| Persian | plain | 1.000 | 0.000 | 0.587 | 0.587 | darnd mwxc wund brx az sbk ha moruf obartnd#az uaqo gra uaqo gra suryalsm fra ua |

## the manuscript and the control

gap = best key's score per letter minus real text of that kind (0 = reads like the real thing).

| language | written | symbols as | gap B | gap A | gap control | words B | words A | words control | words real |
|---|---|---|---|---|---|---|---|---|---|
| Latin | no vowels | glyphs | 0.024 | 0.035 | 0.032 | 0.231 | 0.243 | 0.316 | 0.319 |
| Latin | no vowels | groups | 0.080 | 0.056 | 0.085 | 0.335 | 0.218 | 0.291 | 0.319 |
| Latin | no vowels | merged 60 | 0.085 | 0.080 | 0.116 | 0.068 | 0.056 | 0.054 | 0.319 |
| Latin | letters sorted | glyphs | -0.354 | -0.287 | -0.368 | 0.033 | 0.001 | 0.081 | 0.296 |
| Latin | letters sorted | groups | -0.378 | -0.359 | -0.268 | 0.002 | 0.002 | 0.001 | 0.296 |
| Latin | letters sorted | merged 60 | -0.382 | -0.428 | -0.329 | 0.000 | 0.001 | 0.001 | 0.296 |
| Latin | backwards | glyphs | -0.143 | -0.122 | -0.174 | 0.016 | 0.074 | 0.004 | 0.263 |
| Latin | backwards | groups | -0.150 | -0.147 | -0.074 | 0.003 | 0.004 | 0.002 | 0.263 |
| Latin | backwards | merged 60 | -0.152 | -0.184 | -0.101 | 0.001 | 0.000 | 0.002 | 0.263 |
| Italian | no vowels | glyphs | -0.079 | -0.050 | -0.097 | 0.289 | 0.262 | 0.350 | 0.459 |
| Italian | no vowels | groups | -0.012 | -0.016 | -0.029 | 0.327 | 0.254 | 0.300 | 0.459 |
| Italian | no vowels | merged 60 | 0.008 | -0.002 | 0.053 | 0.071 | 0.069 | 0.058 | 0.459 |
| Italian | letters sorted | glyphs | -0.293 | -0.315 | -0.264 | 0.065 | 0.022 | 0.059 | 0.605 |
| Italian | letters sorted | groups | -0.367 | -0.289 | -0.289 | 0.009 | 0.003 | 0.011 | 0.605 |
| Italian | letters sorted | merged 60 | -0.267 | -0.332 | -0.254 | 0.004 | 0.002 | 0.002 | 0.605 |
| Italian | backwards | glyphs | -0.188 | -0.226 | -0.127 | 0.040 | 0.004 | 0.097 | 0.587 |
| Italian | backwards | groups | -0.191 | -0.232 | -0.206 | 0.016 | 0.008 | 0.004 | 0.587 |
| Italian | backwards | merged 60 | -0.202 | -0.228 | -0.115 | 0.001 | 0.002 | 0.002 | 0.587 |
| German | no vowels | glyphs | -0.065 | -0.089 | -0.094 | 0.208 | 0.174 | 0.255 | 0.483 |
| German | no vowels | groups | -0.038 | -0.070 | -0.051 | 0.291 | 0.174 | 0.235 | 0.483 |
| German | no vowels | merged 60 | -0.026 | -0.043 | 0.023 | 0.043 | 0.037 | 0.040 | 0.483 |
| German | letters sorted | glyphs | -0.233 | -0.273 | -0.347 | 0.037 | 0.043 | 0.057 | 0.528 |
| German | letters sorted | groups | -0.336 | -0.374 | -0.262 | 0.010 | 0.014 | 0.005 | 0.528 |
| German | letters sorted | merged 60 | -0.440 | -0.491 | -0.429 | 0.002 | 0.000 | 0.002 | 0.528 |
| Hebrew | plain | glyphs | -0.186 | -0.191 | -0.180 | 0.034 | 0.091 | 0.162 | 0.721 |
| Hebrew | plain | groups | -0.161 | -0.202 | -0.155 | 0.100 | 0.095 | 0.127 | 0.721 |
| Hebrew | plain | merged 60 | -0.222 | -0.247 | -0.170 | 0.021 | 0.024 | 0.018 | 0.721 |
| Arabic | plain | glyphs | -0.175 | -0.170 | -0.125 | 0.118 | 0.175 | 0.194 | 0.717 |
| Arabic | plain | groups | -0.153 | -0.179 | -0.082 | 0.185 | 0.141 | 0.218 | 0.717 |
| Arabic | plain | merged 60 | -0.241 | -0.262 | -0.187 | 0.037 | 0.025 | 0.028 | 0.717 |
| Persian | plain | glyphs | -0.222 | -0.218 | -0.199 | 0.165 | 0.174 | 0.241 | 0.587 |
| Persian | plain | groups | -0.174 | -0.201 | -0.117 | 0.189 | 0.115 | 0.243 | 0.587 |
| Persian | plain | merged 60 | -0.184 | -0.213 | -0.113 | 0.023 | 0.023 | 0.026 | 0.587 |
