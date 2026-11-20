# 46 — Where in the word the sequence lives

## What I did

For each feature of a word (first sign, first two, last sign, last two, gallows, length, the
middle), the mutual information with each feature of the next word in the same line, minus the
same with words shuffled among words at the same place in their line (first, inside, last), so
that line-edge habits stay in the baseline. Currier A and B, the Naibbe cipher, the synthetic
one-word-per-letter cipher made of Voynich words (exp. 44), and Latin and Italian with letters as
signs.

## Result (bits)

| | first → first | last → last | gallows → gallows | last sign → next first sign |
|---|---|---|---|---|
| Currier B | 0.071 | 0.016 | 0.032 | **0.250** |
| Currier A | 0.056 | 0.016 | 0.029 | **0.139** |
| Naibbe cipher | 0.006 | 0.000 | 0.000 | 0.003 |
| one word per letter (5 homophones) | 0.081 | 0.047 | 0.034 | 0.060 |
| Latin | 0.021 | 0.096 | 0.001 | 0.040 |
| Italian | 0.060 | 0.057 | 0.006 | 0.118 |

(The many-valued features, middle and last/first two signs, are left out here: with plug-in
estimates their bias doesn't cancel cleanly. They are in the results file.)

The strongest link between neighbouring Voynich words is across the space: the last sign of one
word and the first sign of the next, 0.25 bits in B and 0.14 in A, two to six times what Latin
and Italian have across their spaces. The most favoured pairs in B are *s·a*, *o·r*, *o·l*,
*r·a*, *l·k* (3-6× chance) and *y·q* (1.7×, but 3000 times); the most avoided *y·a*, *n·l*,
*r·l*, *r·q*.

## So what

1. Some of these look like one word cut in two: *s·aiin*, *o·r*, *o·l*, *r·aiin* are probably
   *saiin*, *or*, *ol*, *raiin* with a space read where there's only a gap (exp. 16 found the
   same with the uncertain spaces). Those inflate the coupling and say something about the
   transliteration, not the text.
2. The rest is a writing rule at the boundary (*-y* then *q-*, never *-y* then *a-*). It works
   like a phonological rule across words, or like the boundary chart a generator needs (exp. 18).
3. The Naibbe cipher has none of it: its words are chosen independently of each other's glyphs.
   A cipher that adds this habit would need a rule on top that looks at the previous word's
   ending, which is easy for a writer and hard to explain as part of a cipher.
4. First sign → next first sign is about the same in B (0.071) as in a word-per-letter cipher
   (0.081). It's the one link that looks like what an encoded sequence would leave.
