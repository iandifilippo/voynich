# c13 — Sukhotin's vowel algorithm

## What it is

Sukhotin (1962), made known in the West by Jacques Guy ("Vowel identification: an old (but
good) algorithm", Cryptologia 15, 1991). It finds the vowels of an unknown alphabet from
nothing but which letters touch which: vowels and consonants alternate, so the letter with
the most contacts is a vowel, its neighbours lean consonant, and so on. Guy applied it to the
manuscript. The scan of his paper that was shared with me has no text layer, so I haven't
checked my output against his.

## What I did

The algorithm on Currier A and B (EVA characters, and again with *ch, sh, cth...* as single
signs), the two content-free controls, and five real texts. Besides the list of vowels, how
well the split works: the share of letter pairs inside words that cross it (vowel next to
consonant), against the same letters shuffled.

## Result

| | vowels (in order found) | crossing pairs | excess over shuffled |
|---|---|---|---|
| Currier A, composites as one | o a y n e c g u | 0.83 | 0.27 |
| Currier B, composites as one | o e a y n c h u z | 0.84 | 0.30 |
| copying model | a e y o n sh | 0.78 | 0.23 |
| Naibbe cipher of Latin | o a e y n g f | 0.82 | 0.27 |
| Latin | i e u a o y | 0.84 | 0.30 |
| Italian | e i a o u h | 0.80 | 0.26 |
| English | e a o i u y | 0.80 | 0.26 |
| Georgian | ა ი ე ო უ ... | 0.83 | 0.28 |
| Hebrew, no vowel points | ו י ל ר ... | 0.63 | 0.09 |

The manuscript alternates as strongly as Latin, and the algorithm picks the obvious
candidates (*o, a, e, y*), plus *n*, which is really "the thing after *i*". But the copying
model and the Naibbe cipher do it just as well.

## So what

Alternation is there and it's strong, but it's a property of how Voynich glyphs combine, and
any generator that copies the glyph combinations reproduces it. This is the root of the
c07-c09 problem: every proposed key that puts vowels on *o, a, e, y* gets pronounceable output
from anything with these statistics. Unvowelled Hebrew is the one text that doesn't
alternate, so the manuscript isn't written like an abjad, unless the glyphs are something
other than letters.
