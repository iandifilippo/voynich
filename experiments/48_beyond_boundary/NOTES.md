# 48 — Does anything pass from word to word except through the boundary?

## What I think

Exp. 46: the strongest link between neighbouring words is the pair of glyphs at the space (last
sign → next first sign). A writer's habit makes that with no message at all. A message makes
something else: what one word chose (its start, gallows, ending) tells you about the choices in
the next word beyond what the boundary glyphs carry.

## What I did

Conditional mutual information I(feature of word i ; feature of word i+1 | last sign of i, first
sign of i+1), minus a baseline that permutes the first feature among words with the same boundary
context. Twice: baseline over the whole text, and inside each sheet (so the per-sheet setting of
exps. 40-42 is in the baseline too). Then plain MI at distance 1, 2, 3 in the line, to see
whether what's left falls off with distance (sequence) or stays flat (a setting per line).

## Result

Sum over all 16 feature pairs (bits), baseline inside the sheet:

| | beyond the boundary |
|---|---|
| Currier B | 0.30 |
| Currier A | 0.23 |
| generator with boundary habit and echo (exp. 36) | 0.02 |
| cipher of Latin, one key, Voynich words | 0.88 |
| Latin, letters | 0.66 |
| Italian, letters | 1.37 |

By distance (plain MI, bits):

| | start d=1 / 2 / 3 | gallows d=1 / 2 / 3 | ending d=1 / 2 / 3 |
|---|---|---|---|
| Currier B | 0.18 / 0.05 / 0.03 | 0.032 / 0.024 / 0.020 | 0.078 / 0.024 / 0.021 |
| generator | 0.06 / 0.01 / 0.01 | 0.003 / 0.002 / 0.000 | 0.055 / 0.009 / 0.007 |
| cipher of Latin | 0.15 / 0.05 / 0.01 | 0.017 / 0.003 / 0.002 | 0.110 / 0.041 / 0.017 |
| Latin letters | 0.18 / 0.08 / 0.04 | 0.001 / 0.000 / 0.000 | 0.35 / 0.11 / 0.06 |

1. There is a link between neighbouring words that goes around the boundary glyphs and survives
   the sheet setting: 0.30 bits in B, 0.23 in A, fifteen times what my generator makes, a third of
   a letter cipher of Latin.
2. Part of it doesn't fall off with distance. The gallows of one word predicts the gallows of the
   next three words almost equally (0.032, 0.024, 0.020): that's a choice held along a stretch of
   line, not a sequence. Exp. 49 measures it directly: two words of the same line agree on their
   gallows 7-12% more often than two words of different lines of the page at the same positions,
   flat with distance; the generator's excess dies by distance 3.
3. The start of a word falls off with distance like Latin's letters do (0.18 → 0.05 → 0.03 against
   0.18 → 0.08 → 0.04), though some of that is the boundary.

## So what

This is the part of Currier B (and, surprisingly, A) that none of my content-free models produce:
a word's choices depend on the previous word's choices, not only on its last glyph, and a
setting persists along stretches of a line. Exp. 44 said A has no word-to-word sequence; at the
level of whole-word classes that's right, but at the level of the choices inside words A has
almost as much as B. Classes of whole words hid it.

It's what's left for a message to live in, and it's small: well under what one letter per word
would leave. Either the text carries much less than a letter per word, or this is still the
writer's habit at a level my generator doesn't model (a choice of gallows held for a few words,
the start of a word echoing the start of the last).

## Caveats

- Plug-in estimates with permutation baselines; the many-valued features (two signs) have more
  bias left than the others.
- The generator doesn't model a per-line or per-sheet setting, so it understates what a habit
  alone could produce. A generator with a gallows choice held for a few words is the obvious next
  control.
