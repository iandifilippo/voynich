# 23 scorecard: best copying model on measures it wasn't tuned on


## B settings against Currier B

| measure | VMS | model | sd | model/VMS | verdict |
|---|---|---|---|---|---|
| exact repeats / in-line null | 0.919 | 0.707 | 0.111 | 0.770 | off |
| near repeats / in-line null | 0.996 | 1.061 | 0.066 | 1.066 | ok |
| singletons: one edit from known | 0.627 | 0.653 | 0.018 | 1.043 | ok |
| singletons: two known joined | 0.148 | 0.082 | 0.032 | 0.553 | off |
| mean word length | 4.950 | 5.214 | 0.222 | 1.053 | ok |
| words of length 1 | 0.026 | 0.003 | 0.002 | 0.135 | wrong |
| words of length 2 | 0.072 | 0.060 | 0.042 | 0.827 | ok |
| words of length 3 | 0.104 | 0.084 | 0.012 | 0.816 | ok |
| words of length 8+ | 0.056 | 0.069 | 0.014 | 1.238 | ok |
| words starting q- | 0.197 | 0.014 | 0.003 | 0.072 | wrong |
| words starting o- | 0.213 | 0.074 | 0.030 | 0.349 | wrong |
| words starting ch- | 0.135 | 0.182 | 0.024 | 1.353 | off |
| words starting sh- | 0.104 | 0.154 | 0.032 | 1.477 | off |
| words starting d- | 0.089 | 0.080 | 0.018 | 0.901 | ok |
| words starting y- | 0.041 | 0.025 | 0.007 | 0.612 | off |
| words ending -y | 0.512 | 0.357 | 0.095 | 0.696 | off |
| words ending -n | 0.135 | 0.205 | 0.029 | 1.523 | off |
| words ending -l | 0.152 | 0.078 | 0.058 | 0.515 | off |
| words ending -r | 0.119 | 0.157 | 0.034 | 1.324 | off |
| words ending -m | 0.017 | 0.014 | 0.003 | 0.839 | ok |
| line-first words starting s- | 0.180 | 0.229 | 0.041 | 1.269 | off |
| line-first words starting d- | 0.143 | 0.058 | 0.011 | 0.403 | wrong |
| line-first words starting t- | 0.101 | 0.029 | 0.003 | 0.289 | wrong |
| line-first words starting p- | 0.098 | 0.083 | 0.004 | 0.844 | ok |
| line-first words starting q- | 0.205 | 0.013 | 0.004 | 0.062 | wrong |
| top word share | 0.029 | 0.030 | 0.007 | 1.043 | ok |

ok 10, off 10, wrong 6 (ok = within 0.8-1.25x, off = within 2x)

## A settings against Currier A

| measure | VMS | model | sd | model/VMS | verdict |
|---|---|---|---|---|---|
| exact repeats / in-line null | 1.031 | 0.662 | 0.103 | 0.643 | off |
| near repeats / in-line null | 1.292 | 0.954 | 0.101 | 0.739 | off |
| singletons: one edit from known | 0.635 | 0.685 | 0.033 | 1.079 | ok |
| singletons: two known joined | 0.145 | 0.103 | 0.014 | 0.711 | off |
| mean word length | 4.774 | 4.590 | 0.180 | 0.962 | ok |
| words of length 1 | 0.044 | 0.011 | 0.008 | 0.248 | wrong |
| words of length 2 | 0.054 | 0.173 | 0.036 | 3.204 | wrong |
| words of length 3 | 0.117 | 0.084 | 0.014 | 0.722 | off |
| words of length 8+ | 0.064 | 0.036 | 0.011 | 0.568 | off |
| words starting q- | 0.096 | 0.005 | 0.001 | 0.047 | wrong |
| words starting o- | 0.156 | 0.172 | 0.030 | 1.099 | ok |
| words starting ch- | 0.194 | 0.172 | 0.032 | 0.884 | ok |
| words starting sh- | 0.088 | 0.122 | 0.014 | 1.381 | off |
| words starting d- | 0.156 | 0.089 | 0.015 | 0.574 | off |
| words starting y- | 0.064 | 0.026 | 0.005 | 0.405 | wrong |
| words ending -y | 0.318 | 0.276 | 0.069 | 0.868 | ok |
| words ending -n | 0.160 | 0.178 | 0.035 | 1.111 | ok |
| words ending -l | 0.176 | 0.153 | 0.031 | 0.867 | ok |
| words ending -r | 0.167 | 0.213 | 0.022 | 1.274 | off |
| words ending -m | 0.031 | 0.015 | 0.006 | 0.487 | wrong |
| line-first words starting s- | 0.127 | 0.228 | 0.012 | 1.795 | off |
| line-first words starting d- | 0.147 | 0.091 | 0.019 | 0.620 | off |
| line-first words starting t- | 0.089 | 0.029 | 0.005 | 0.332 | wrong |
| line-first words starting p- | 0.051 | 0.077 | 0.005 | 1.523 | off |
| line-first words starting q- | 0.144 | 0.005 | 0.002 | 0.035 | wrong |
| top word share | 0.046 | 0.054 | 0.012 | 1.176 | ok |

ok 8, off 11, wrong 7 (ok = within 0.8-1.25x, off = within 2x)

## A and B

| pair | distance |
|---|---|
| VMS A vs B | 1.309 |
| model A vs B settings (mean of 4) | 1.214 |
| model B vs B, different seeds (mean of 4) | 0.796 |
