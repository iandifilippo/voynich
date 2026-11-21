# 54 — Attack 7: a few bits per word, hidden in the forks

## What I think

This is the last cipher family the series hadn't calibrated, and the one most consistent with
everything found so far: the message isn't in which word is written but in one or two choices
inside it (how it starts, how it ends), one plaintext letter spread over several words, the rest
of each word filler from the slot machine. Such a text has the manuscript's word shapes, no
lexicon, and weak links between neighbours.

What it can't hide is that the sequence of those choices spells something, so it is predictable
from several words back, not only from the previous word.

## What I did

Streams of fork choices in reading order through each sheet: whether a word starts with *qo*
(2 values), its start class (*qo / o / ch-sh / other*), its end class (*y / n / l-r / other*), its
gallows (*t / k / p-f / none*), start and end together (16). Held-out bits per symbol under an
n-gram model that looks k symbols back (up to 12), trained on half the sheets and tested on the
other half. The number that matters: how much looking further than one word back helps.

Calibration: ciphers of Latin built with the manuscript's own word machine (exp. 36, B tables).
Letters become 5-bit codes, the bits are laid into words: 1 bit per word (*qo* or not), 2 bits
(start class) or 4 bits (start and end class); everything else in each word chosen freely by the
machine. Laid out in B's own sheets and lines.

## Result (bits per symbol gained by looking further than one word back)

| | qo or not | start | start and end |
|---|---|---|---|
| cipher, 1 bit per word | **0.085** (best k = 8) | 0.008 | – |
| cipher, 2 bits per word | 0.005 | **0.179** (k = 5) | 0.000 |
| cipher, 4 bits per word | 0.000 | 0.006 | **0.307** (k = 3) |
| habits generator | 0.017 | 0.064 | 0.000 |
| Currier B | 0.005 | 0.003 | 0.000 |
| Currier A | 0.000 | 0.000 | 0.000 |

Gallows stream: B 0.009, A 0.010, generator 0.018. End stream: B 0.004, A 0.002.

Each cipher shows up clearly in the channel it uses, at the context length its letters span
(8 words for 1 bit, 5 for 2 bits, 3 for 4 bits). Currier A and B show nothing in any channel:
less than my habits-only generator.

## So what

A Latin message carried at 1, 2 or 4 bits per word in the start, the ending, or *qo-* would have
been found here, from half the book, without knowing the code. It isn't there. With exps. 31-35
(letters, pairs and pieces), 44 and 47 (homophones, sheet keys), and 34 (codebook), every way of
putting a language into Voynich words that I've been able to calibrate is now excluded.

## Caveats

- The gallows channel wasn't calibrated with its own cipher, and neither were channels I haven't
  thought of (length, the *e*-run, line position). A code in those would need its own test.
- The codes were fixed for the whole book; a code changed per sheet would be harder to see with
  half the sheets as training. Exp. 47 found no sign of per-sheet keys in the neighbour links.
- Plaintext letters' own redundancy is what the test feeds on. A plaintext that is itself close to
  random (numbers, a compressed or abbreviated text) would leave almost nothing to find.

## Later: the remaining channels (`channels.py`)

Same test with ciphers that put their bits in the gallows (2 bits per word), the length parity
(1 bit) and whether the word has an *e*-run (1 bit):

| channel | cipher in that channel | habits generator | Currier B | Currier A |
|---|---|---|---|---|
| gallows | 0.179 (k = 5) | 0.012 | 0.009 | 0.010 |
| length parity | 0.097 (k = 9) | 0.000 | 0.000 | 0.000 |
| *e*-run | 0.097 (k = 9) | 0.001 | 0.007 | **0.022** (k = 5) |

All calibrated, all empty in B. Currier A's *e*-run channel is above the generator, in both ZL
(0.022) and IT (0.026), but most of it survives putting each sheet's lines in random order (0.014,
0.019): it lives inside lines, a habit of *e*-heavy and *e*-free stretches, not a sequence running
through the text. It's a quarter of what a 1-bit cipher leaves. I note it and don't count it.
