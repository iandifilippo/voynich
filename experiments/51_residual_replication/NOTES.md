# 51 — Does the residual replicate?

## What I did

Exp. 50's test (habits-only generator fitted to the text, then the link between neighbours
beyond the boundary glyphs and the sheet setting, and its off-diagonal part) on Currier A and B,
in ZL and in IT (Takahashi), words of 3+ signs only. Then eight generator seeds per text to see
its spread (`seeds.py`).

## Result

| | beyond boundary: text / generator | off-diagonal: text / generator |
|---|---|---|
| ZL Currier B | 0.240 / 0.076 | 0.038 / −0.014 |
| ZL Currier A | 0.181 / 0.052 | 0.075 / −0.008 |
| IT Currier B | 0.259 / 0.109 | 0.041 / −0.010 |
| IT Currier A | 0.159 / 0.039 | 0.053 / −0.016 |

Eight generator runs: B 0.064-0.116 (text 0.240), off-diagonal −0.023 to 0.001 (text 0.038); A
0.010-0.086 (text 0.181), off-diagonal −0.042 to 0.003 (text 0.075). The text is outside every run.

## So what

The residual is in both languages and both transcriptions, and every generator run falls short of
it. It's not a property of one reading of the glyphs. Exps. 52-53 ask what it's made of.
