# 46 where in the word the sequence lives

MI (bits) between a feature of one word and a feature of the next, minus words shuffled within their line position class.

| text | first sign -> same | first 2 -> same | last sign -> same | last 2 -> same | gallows -> same | length -> same | middle -> same | last sign -> first sign | last 2 -> first 2 | strongest pair |
|---|---|---|---|---|---|---|---|---|---|---|
| Currier B | 0.071 | 0.197 | 0.016 | 0.087 | 0.032 | 0.025 | 0.255 | 0.250 | 0.330 | last 2 -> first 2 (0.330) |
| Currier A | 0.056 | 0.148 | 0.016 | 0.098 | 0.029 | 0.016 | 0.189 | 0.139 | 0.222 | last 2 -> first 2 (0.222) |
| Naibbe cipher | 0.006 | 0.023 | 0.000 | 0.013 | 0.000 | 0.001 | 0.041 | 0.003 | 0.035 | middle -> first 2 (0.047) |
| one word per letter, 5 homophones | 0.081 | 0.224 | 0.047 | 0.257 | 0.034 | 0.006 | 0.512 | 0.060 | 0.213 | middle -> middle (0.512) |
| Latin (letters as signs) | 0.021 | 0.187 | 0.096 | 0.350 | 0.001 | 0.042 | -0.058 | 0.040 | 0.191 | last 2 -> last 2 (0.350) |
| Italian (letters as signs) | 0.060 | 0.405 | 0.057 | 0.448 | 0.006 | 0.056 | 0.010 | 0.118 | 0.594 | last 2 -> first 2 (0.594) |
