# 49 — A setting per line?

## What I did

For pairs of words on the same page (line-first words left out), how often they agree on a
feature: two words of the same line d places apart, against two words of different lines at the
same positions. Agreement ratio = same line / other line.

## Result

| | gallows d=1 / 2 / 3 / 4 | start | ending |
|---|---|---|---|
| Currier B | 1.12 / 1.11 / 1.07 / 1.07 | 1.02 / 1.14 / 1.11 / 1.10 | 1.00 / 1.04 / 1.01 / 1.03 |
| Currier A | 1.08 / 1.09 / 1.08 / 1.05 | 1.06 / 1.10 / 1.10 / 1.08 | 1.04 / 1.10 / 1.09 / 1.04 |
| generator (exp. 36) | 1.06 / 1.04 / 0.99 / 1.02 | 1.06 / 1.11 / 1.07 / 1.15 | 1.04 / 1.04 / 1.05 / 1.03 |
| Latin (stop consonant / first / last letter) | 1.00 / 1.00 / 1.00 / 1.02 | 0.72 / 0.98 / 0.99 / 1.07 | 1.12 / 1.22 / 1.18 / 1.13 |

## So what

Words in the same line agree on their gallows about 7-12% more than words in different lines of
the same page, and the excess barely fades with distance; in the generator it's gone by distance
3. Starts and endings agree more along a line too, but the generator (whose echo copies recent
words) does that as well, so only the gallows result is new. It's a weak effect: lines are a
unit, but a much weaker one than the sheet.
