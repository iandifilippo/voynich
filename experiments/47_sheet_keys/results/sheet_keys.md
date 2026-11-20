# 47 is the code different on every sheet?

MI between neighbouring words (bits), bias-corrected, pooled over the section vs inside each sheet.

## first -> first

| text | sheets | first -> first: pooled | first -> first: inside sheets |
|---|---|---|---|
| Currier B | 20 | 0.067 | 0.074 |
| Currier A | 28 | 0.051 | 0.051 |
| cipher of Latin, one key (B's sheets) | 20 | 0.034 | 0.032 |
| cipher of Latin, new key every sheet (B's sheets) | 20 | 0.000 | 0.027 |
| generator (exp. 36), B's sheets | 20 | 0.019 | 0.022 |

## last -> last

| text | sheets | last -> last: pooled | last -> last: inside sheets |
|---|---|---|---|
| Currier B | 20 | 0.014 | 0.020 |
| Currier A | 28 | 0.013 | 0.019 |
| cipher of Latin, one key (B's sheets) | 20 | 0.005 | 0.007 |
| cipher of Latin, new key every sheet (B's sheets) | 20 | 0.002 | 0.012 |
| generator (exp. 36), B's sheets | 20 | 0.014 | 0.018 |

## first -> last

| text | sheets | first -> last: pooled | first -> last: inside sheets |
|---|---|---|---|
| Currier B | 20 | 0.007 | 0.012 |
| Currier A | 28 | 0.011 | 0.011 |
| cipher of Latin, one key (B's sheets) | 20 | 0.013 | 0.013 |
| cipher of Latin, new key every sheet (B's sheets) | 20 | 0.001 | 0.013 |
| generator (exp. 36), B's sheets | 20 | 0.001 | 0.003 |

## last -> first

| text | sheets | last -> first: pooled | last -> first: inside sheets |
|---|---|---|---|
| Currier B | 20 | 0.249 | 0.260 |
| Currier A | 28 | 0.137 | 0.144 |
| cipher of Latin, one key (B's sheets) | 20 | 0.011 | 0.008 |
| cipher of Latin, new key every sheet (B's sheets) | 20 | 0.002 | 0.018 |
| generator (exp. 36), B's sheets | 20 | 0.233 | 0.226 |

## shape -> shape

| text | sheets | shape -> shape: pooled | shape -> shape: inside sheets |
|---|---|---|---|
| Currier B | 20 | 0.297 | 0.209 |
| Currier A | 28 | 0.161 | 0.069 |
| cipher of Latin, one key (B's sheets) | 20 | 0.154 | 0.091 |
| cipher of Latin, new key every sheet (B's sheets) | 20 | 0.047 | 0.131 |
| generator (exp. 36), B's sheets | 20 | 0.231 | 0.127 |

