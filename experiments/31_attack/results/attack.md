# 31 attack: one symbol, one letter

gap = score per letter of the best key minus real text in that language. 0 means it reads like the language; exp. 30 put texts with no such language in them at −0.19 to −0.47.

|  | value |
|---|---|
| combinations | 81 |
| best gap, VMS | -0.109 |
| best gap, copying model | -0.120 |
| VMS B better than copying model | 38 |
| VMS A better than copying model | 30 |
| mean B minus control | -0.004 |
| mean A minus control | -0.018 |
| best words share, VMS | 0.090 |
| best words share, copying model | 0.108 |
| within 0.05 of real text | 0 |

## the twelve best readings of the manuscript

| symbols as | spaces | language | n symbols | gap B | gap A | gap copying model | gap shuffled | words B | words A | words copying model | words real |
|---|---|---|---|---|---|---|---|---|---|---|---|
| glyphs | ignored | Latin | 26 | -0.109 | -0.151 | -0.163 | -0.337 | 0.025 | 0.014 | 0.007 | 0.363 |
| pieces | ignored | Latin | 400 | -0.109 | -0.123 | -0.184 | 0.052 | 0.031 | 0.025 | 0.014 | 0.363 |
| pieces | ignored | Italian | 400 | -0.131 | -0.129 | -0.206 | 0.042 | 0.041 | 0.036 | 0.025 | 0.540 |
| pieces | ignored | Czech | 400 | -0.198 | -0.133 | -0.250 | 0.031 | 0.027 | 0.021 | 0.013 | 0.488 |
| pieces | ignored | German | 400 | -0.134 | -0.159 | -0.255 | -0.010 | 0.051 | 0.041 | 0.025 | 0.587 |
| glyphs | ignored | German | 26 | -0.180 | -0.144 | -0.186 | -0.393 | 0.030 | 0.041 | 0.021 | 0.587 |
| pieces | ignored | Spanish | 400 | -0.152 | -0.172 | -0.276 | -0.017 | 0.016 | 0.015 | 0.023 | 0.553 |
| pieces | ignored | Hungarian | 400 | -0.162 | -0.159 | -0.278 | 0.007 | 0.036 | 0.060 | 0.022 | 0.663 |
| glyphs | ignored | Italian | 26 | -0.164 | -0.161 | -0.185 | -0.370 | 0.018 | 0.011 | 0.046 | 0.540 |
| merged 150 | kept | Italian | 176 | -0.165 | -0.194 | -0.162 | -0.340 | 0.000 | 0.002 | 0.001 | 0.587 |
| glyphs | ignored | Spanish | 26 | -0.176 | -0.261 | -0.266 | -0.440 | 0.017 | 0.014 | 0.009 | 0.553 |
| merged 60 | kept | Italian | 86 | -0.180 | -0.199 | -0.120 | -0.388 | 0.001 | 0.001 | 0.004 | 0.587 |

## where the manuscript beats the content-free control by most

| symbols as | spaces | language | gap B | gap A | gap copying model | B minus control | A minus control |
|---|---|---|---|---|---|---|---|
| pieces | ignored | Spanish | -0.152 | -0.172 | -0.276 | 0.123 | 0.103 |
| pieces | ignored | German | -0.134 | -0.159 | -0.255 | 0.121 | 0.096 |
| pieces | ignored | Hungarian | -0.162 | -0.159 | -0.278 | 0.116 | 0.119 |
| pieces | ignored | Czech | -0.198 | -0.133 | -0.250 | 0.052 | 0.117 |
| glyphs | kept | Spanish | -0.313 | -0.251 | -0.361 | 0.048 | 0.110 |
| pieces | ignored | Turkish | -0.201 | -0.215 | -0.309 | 0.108 | 0.094 |
| glyphs | ignored | Spanish | -0.176 | -0.261 | -0.266 | 0.090 | 0.004 |
| pieces | ignored | French | -0.216 | -0.185 | -0.264 | 0.049 | 0.079 |
| pieces | ignored | Italian | -0.131 | -0.129 | -0.206 | 0.075 | 0.077 |
| pieces | ignored | Latin | -0.109 | -0.123 | -0.184 | 0.075 | 0.061 |
| pieces | ignored | English (Middle) | -0.186 | -0.195 | -0.257 | 0.071 | 0.062 |
| glyphs | kept | Turkish | -0.320 | -0.222 | -0.282 | -0.038 | 0.060 |

## what the best readings look like

| text | symbols as | spaces | language | gap | decoded |
|---|---|---|---|---|---|
| VMS Currier B | glyphs | ignored | Latin | -0.109 | ucienaetellrmeaescetsausiaausitaelosesesiuuta#tsiaetiietaanipiasitaaditatasipitans#eellocp |
| VMS Currier B | pieces | ignored | Latin | -0.109 | alacentalium#ribusarence#murobeditetosroene#eteaeacamoeti#susbibieteabaei#ree#dietaregento |
| VMS Currier A | pieces | ignored | Latin | -0.123 | alalalisihabanesa#aamulaanurisuntututi#asulalasobedime#monotheysmalami#muatutaduma#ae#mute |
| VMS Currier A | pieces | ignored | Italian | -0.129 | utididicolitaloca#bitidialiniciamimire#utiditicaperese#sidachelasidise#siatimilivi#be#sife |
| VMS Currier B | pieces | ignored | Italian | -0.131 | bracizzolato#diquledismo#toreladetelanriini#erieeelateile#consosoirialleu#dee#pielarivinch |
| VMS Currier A | pieces | ignored | Czech | -0.133 | vmehohynevizumine#vizepoumitynejleleno#vrapomenyzabyva#vijoulacscepoco#viurelenere#va#veda |

## and the best readings of the control

| text | symbols as | spaces | language | gap | decoded |
|---|---|---|---|---|---|
| control: copying model | merged 60 | kept | Italian | -0.120 | tea pre co e cda se co po pee cral#coe pran po di atda e pra#nopra me e mal po di pr e e e |
| control: copying model | groups | ignored | German | -0.136 | amernharmtanderstteiteerntandhandhahernterte#tanersttertuhangerstersteitundtert#unterterbb |
| control: copying model | groups | kept | German | -0.136 | ahist bish eind iste erse eist eind bind bilist ersea#einiste erseu bind iste isterse und  |

## every combination

| symbols as | spaces | language | n symbols | gap B | gap A | gap copying model | gap shuffled | words B | words A | words copying model | words real |
|---|---|---|---|---|---|---|---|---|---|---|---|
| glyphs | ignored | Czech | 26 | -0.214 | -0.246 | -0.241 | -0.423 | 0.033 | 0.009 | 0.009 | 0.488 |
| glyphs | ignored | English (Middle) | 26 | -0.261 | -0.251 | -0.274 | -0.364 | 0.024 | 0.010 | 0.005 | 0.389 |
| glyphs | ignored | French | 26 | -0.252 | -0.191 | -0.245 | -0.396 | 0.033 | 0.080 | 0.031 | 0.614 |
| glyphs | ignored | German | 26 | -0.180 | -0.144 | -0.186 | -0.393 | 0.030 | 0.041 | 0.021 | 0.587 |
| glyphs | ignored | Hungarian | 26 | -0.201 | -0.201 | -0.236 | -0.419 | 0.027 | 0.026 | 0.018 | 0.663 |
| glyphs | ignored | Italian | 26 | -0.164 | -0.161 | -0.185 | -0.370 | 0.018 | 0.011 | 0.046 | 0.540 |
| glyphs | ignored | Latin | 26 | -0.109 | -0.151 | -0.163 | -0.337 | 0.025 | 0.014 | 0.007 | 0.363 |
| glyphs | ignored | Spanish | 26 | -0.176 | -0.261 | -0.266 | -0.440 | 0.017 | 0.014 | 0.009 | 0.553 |
| glyphs | ignored | Turkish | 26 | -0.269 | -0.202 | -0.250 | -0.432 | 0.025 | 0.059 | 0.035 | 0.666 |
| glyphs | kept | Czech | 26 | -0.305 | -0.320 | -0.311 | -0.548 | 0.003 | 0.006 | 0.005 | 0.551 |
| glyphs | kept | English (Middle) | 26 | -0.375 | -0.344 | -0.309 | -0.593 | 0.006 | 0.061 | 0.005 | 0.492 |
| glyphs | kept | French | 26 | -0.263 | -0.308 | -0.299 | -0.536 | 0.043 | 0.085 | 0.018 | 0.639 |
| glyphs | kept | German | 26 | -0.226 | -0.207 | -0.253 | -0.459 | 0.021 | 0.079 | 0.067 | 0.523 |
| glyphs | kept | Hungarian | 26 | -0.322 | -0.284 | -0.318 | -0.508 | 0.015 | 0.047 | 0.025 | 0.629 |
| glyphs | kept | Italian | 26 | -0.238 | -0.219 | -0.219 | -0.521 | 0.031 | 0.081 | 0.058 | 0.587 |
| glyphs | kept | Latin | 26 | -0.183 | -0.196 | -0.206 | -0.437 | 0.051 | 0.090 | 0.074 | 0.330 |
| glyphs | kept | Spanish | 26 | -0.313 | -0.251 | -0.361 | -0.576 | 0.012 | 0.012 | 0.013 | 0.612 |
| glyphs | kept | Turkish | 26 | -0.320 | -0.222 | -0.282 | -0.536 | 0.003 | 0.051 | 0.103 | 0.703 |
| groups | ignored | Czech | 51 | -0.276 | -0.247 | -0.236 | -0.418 | 0.013 | 0.022 | 0.026 | 0.488 |
| groups | ignored | English (Middle) | 51 | -0.287 | -0.287 | -0.195 | -0.413 | 0.003 | 0.008 | 0.000 | 0.389 |
| groups | ignored | French | 51 | -0.270 | -0.235 | -0.213 | -0.393 | 0.044 | 0.035 | 0.045 | 0.614 |
| groups | ignored | German | 51 | -0.202 | -0.263 | -0.136 | -0.359 | 0.029 | 0.027 | 0.108 | 0.587 |
| groups | ignored | Hungarian | 51 | -0.276 | -0.285 | -0.246 | -0.420 | 0.014 | 0.012 | 0.019 | 0.663 |
| groups | ignored | Italian | 51 | -0.200 | -0.248 | -0.204 | -0.346 | 0.022 | 0.019 | 0.038 | 0.540 |
| groups | ignored | Latin | 51 | -0.188 | -0.247 | -0.143 | -0.323 | 0.015 | 0.008 | 0.022 | 0.363 |
| groups | ignored | Spanish | 51 | -0.255 | -0.268 | -0.217 | -0.423 | 0.012 | 0.015 | 0.011 | 0.553 |
| groups | ignored | Turkish | 51 | -0.281 | -0.296 | -0.217 | -0.427 | 0.041 | 0.032 | 0.020 | 0.666 |
| groups | kept | Czech | 51 | -0.311 | -0.240 | -0.245 | -0.533 | 0.005 | 0.004 | 0.001 | 0.551 |
| groups | kept | English (Middle) | 51 | -0.318 | -0.304 | -0.203 | -0.561 | 0.003 | 0.001 | 0.007 | 0.492 |
| groups | kept | French | 51 | -0.296 | -0.304 | -0.188 | -0.535 | 0.005 | 0.001 | 0.000 | 0.639 |
| groups | kept | German | 51 | -0.234 | -0.241 | -0.136 | -0.470 | 0.006 | 0.001 | 0.001 | 0.523 |
| groups | kept | Hungarian | 51 | -0.264 | -0.325 | -0.227 | -0.498 | 0.009 | 0.001 | 0.001 | 0.629 |
| groups | kept | Italian | 51 | -0.209 | -0.206 | -0.137 | -0.493 | 0.020 | 0.014 | 0.005 | 0.587 |
| groups | kept | Latin | 51 | -0.199 | -0.206 | -0.158 | -0.435 | 0.012 | 0.008 | 0.003 | 0.330 |
| groups | kept | Spanish | 51 | -0.268 | -0.298 | -0.245 | -0.560 | 0.015 | 0.004 | 0.004 | 0.612 |
| groups | kept | Turkish | 51 | -0.323 | -0.310 | -0.203 | -0.526 | 0.004 | 0.005 | 0.001 | 0.703 |
| merged 150 | ignored | Czech | 176 | -0.309 | -0.352 | -0.353 | -0.381 | 0.006 | 0.008 | 0.003 | 0.488 |
| merged 150 | ignored | English (Middle) | 176 | -0.324 | -0.350 | -0.338 | -0.372 | 0.005 | 0.002 | 0.007 | 0.389 |
| merged 150 | ignored | French | 176 | -0.322 | -0.360 | -0.354 | -0.349 | 0.017 | 0.015 | 0.022 | 0.614 |
| merged 150 | ignored | German | 176 | -0.286 | -0.337 | -0.324 | -0.337 | 0.017 | 0.011 | 0.020 | 0.587 |
| merged 150 | ignored | Hungarian | 176 | -0.332 | -0.361 | -0.355 | -0.375 | 0.015 | 0.015 | 0.013 | 0.663 |
| merged 150 | ignored | Italian | 176 | -0.268 | -0.297 | -0.307 | -0.317 | 0.007 | 0.025 | 0.017 | 0.540 |
| merged 150 | ignored | Latin | 176 | -0.234 | -0.273 | -0.257 | -0.283 | 0.010 | 0.017 | 0.008 | 0.363 |
| merged 150 | ignored | Spanish | 176 | -0.328 | -0.362 | -0.374 | -0.393 | 0.012 | 0.013 | 0.008 | 0.553 |
| merged 150 | ignored | Turkish | 176 | -0.342 | -0.379 | -0.394 | -0.399 | 0.022 | 0.019 | 0.022 | 0.666 |
| merged 150 | kept | Czech | 176 | -0.235 | -0.267 | -0.219 | -0.414 | 0.000 | 0.000 | 0.001 | 0.551 |
| merged 150 | kept | English (Middle) | 176 | -0.289 | -0.302 | -0.265 | -0.418 | 0.002 | 0.000 | 0.001 | 0.492 |
| merged 150 | kept | French | 176 | -0.281 | -0.301 | -0.290 | -0.387 | 0.001 | 0.000 | 0.000 | 0.639 |
| merged 150 | kept | German | 176 | -0.383 | -0.405 | -0.428 | -0.393 | 0.000 | 0.000 | 0.000 | 0.523 |
| merged 150 | kept | Hungarian | 176 | -0.235 | -0.269 | -0.195 | -0.374 | 0.001 | 0.000 | 0.000 | 0.629 |
| merged 150 | kept | Italian | 176 | -0.165 | -0.194 | -0.162 | -0.340 | 0.000 | 0.002 | 0.001 | 0.587 |
| merged 150 | kept | Latin | 176 | -0.244 | -0.289 | -0.267 | -0.318 | 0.002 | 0.001 | 0.002 | 0.330 |
| merged 150 | kept | Spanish | 176 | -0.287 | -0.324 | -0.294 | -0.429 | 0.000 | 0.000 | 0.000 | 0.612 |
| merged 150 | kept | Turkish | 176 | -0.404 | -0.429 | -0.458 | -0.434 | 0.000 | 0.000 | 0.001 | 0.703 |
| merged 60 | ignored | Czech | 86 | -0.312 | -0.357 | -0.290 | -0.400 | 0.005 | 0.010 | 0.008 | 0.488 |
| merged 60 | ignored | English (Middle) | 86 | -0.321 | -0.346 | -0.304 | -0.391 | 0.002 | 0.002 | 0.002 | 0.389 |
| merged 60 | ignored | French | 86 | -0.325 | -0.344 | -0.293 | -0.387 | 0.025 | 0.008 | 0.025 | 0.614 |
| merged 60 | ignored | German | 86 | -0.269 | -0.309 | -0.262 | -0.359 | 0.021 | 0.020 | 0.036 | 0.587 |
| merged 60 | ignored | Hungarian | 86 | -0.300 | -0.338 | -0.286 | -0.389 | 0.016 | 0.018 | 0.016 | 0.663 |
| merged 60 | ignored | Italian | 86 | -0.272 | -0.288 | -0.256 | -0.342 | 0.007 | 0.017 | 0.021 | 0.540 |
| merged 60 | ignored | Latin | 86 | -0.221 | -0.256 | -0.222 | -0.292 | 0.017 | 0.015 | 0.019 | 0.363 |
| merged 60 | ignored | Spanish | 86 | -0.318 | -0.374 | -0.316 | -0.407 | 0.017 | 0.013 | 0.012 | 0.553 |
| merged 60 | ignored | Turkish | 86 | -0.327 | -0.388 | -0.332 | -0.406 | 0.039 | 0.016 | 0.021 | 0.666 |
| merged 60 | kept | Czech | 86 | -0.243 | -0.286 | -0.187 | -0.462 | 0.001 | 0.000 | 0.000 | 0.551 |
| merged 60 | kept | English (Middle) | 86 | -0.291 | -0.303 | -0.211 | -0.469 | 0.001 | 0.000 | 0.001 | 0.492 |
| merged 60 | kept | French | 86 | -0.277 | -0.293 | -0.234 | -0.432 | 0.000 | 0.000 | 0.007 | 0.639 |
| merged 60 | kept | German | 86 | -0.336 | -0.372 | -0.280 | -0.413 | 0.002 | 0.000 | 0.000 | 0.523 |
| merged 60 | kept | Hungarian | 86 | -0.254 | -0.279 | -0.164 | -0.413 | 0.000 | 0.001 | 0.000 | 0.629 |
| merged 60 | kept | Italian | 86 | -0.180 | -0.199 | -0.120 | -0.388 | 0.001 | 0.001 | 0.004 | 0.587 |
| merged 60 | kept | Latin | 86 | -0.225 | -0.259 | -0.176 | -0.340 | 0.000 | 0.000 | 0.001 | 0.330 |
| merged 60 | kept | Spanish | 86 | -0.286 | -0.313 | -0.224 | -0.460 | 0.001 | 0.001 | 0.000 | 0.612 |
| merged 60 | kept | Turkish | 86 | -0.367 | -0.401 | -0.356 | -0.462 | 0.001 | 0.001 | 0.002 | 0.703 |
| pieces | ignored | Czech | 400 | -0.198 | -0.133 | -0.250 | 0.031 | 0.027 | 0.021 | 0.013 | 0.488 |
| pieces | ignored | English (Middle) | 400 | -0.186 | -0.195 | -0.257 | 0.024 | 0.009 | 0.010 | 0.007 | 0.389 |
| pieces | ignored | French | 400 | -0.216 | -0.185 | -0.264 | -0.050 | 0.017 | 0.040 | 0.045 | 0.614 |
| pieces | ignored | German | 400 | -0.134 | -0.159 | -0.255 | -0.010 | 0.051 | 0.041 | 0.025 | 0.587 |
| pieces | ignored | Hungarian | 400 | -0.162 | -0.159 | -0.278 | 0.007 | 0.036 | 0.060 | 0.022 | 0.663 |
| pieces | ignored | Italian | 400 | -0.131 | -0.129 | -0.206 | 0.042 | 0.041 | 0.036 | 0.025 | 0.540 |
| pieces | ignored | Latin | 400 | -0.109 | -0.123 | -0.184 | 0.052 | 0.031 | 0.025 | 0.014 | 0.363 |
| pieces | ignored | Spanish | 400 | -0.152 | -0.172 | -0.276 | -0.017 | 0.016 | 0.015 | 0.023 | 0.553 |
| pieces | ignored | Turkish | 400 | -0.201 | -0.215 | -0.309 | -0.051 | 0.048 | 0.044 | 0.020 | 0.666 |
