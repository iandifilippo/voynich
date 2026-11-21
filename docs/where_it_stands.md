# Where it stands (after experiments 34-54)

A short account of what the experiments say together. The details, numbers and caveats are in each
experiment's NOTES.md.

## How the text is made

- **Words are built, not chosen.** A Voynich word behaves like a draw from a rule that looks two
  signs back (exp. 36). Fitted on half of Currier B, that rule writes the other half with the right
  vocabulary size, the right share of one-off words and the same rate of never-seen words (18%
  against 17%). A vocabulary can't do that (0%), and neither can copying (49%).
- **The rule is a short table.** A 12-state machine reads as a list of positions walked left to
  right with a few forks: *q / o / ch-sh*, then a gallows, *e*, *d*, *y*; or *a*, then *l-r* or *ii-n*
  (exps. 37-38). It's Zattera's slot grammar found from scratch, the same for A and B with the
  forks weighted differently. A few dozen states describe the words fully; for Latin or Italian no
  small machine does.
- **There's no lexicon.** Remembering whole words helps predict held-out words in every language
  tested, by 0.7-3.8 bits per word, and not at all in the manuscript (exp. 34).
- **The setting belongs to the sheet.** Each page has its own weighting of the forks, held to the
  end of the page (exp. 40); it survives removing shared words, unlike copying, and real texts
  barely show it. Pages of the same folded sheet share it even when fifteen folios apart, more
  than pages that face each other in the binding (exps. 41-42). The sheets were written as units,
  before the present binding (cf. Davis's singulions).
- **Habits between words.** A strong rule at the space (exp. 46: last sign → next first sign, 0.25
  bits in B), a favoured gallows along a line (exp. 49), echoes of recent words (exp. 36), a
  *ch-/sh-…-y* → *qo-* rhythm and pairs without word order (exp. 53).

## What has been excluded, with calibration

| family | test | calibrated on | result in the manuscript |
|---|---|---|---|
| letter substitution (9 languages) | exp. 31 | known texts | nothing, same as controls |
| letter or pair per word (Naibbe kind) | exp. 35 | Naibbe cipher, read blind at 91-94% | nothing; inventory of halves is open |
| codebook (word per word) | exp. 34 | 10 historical texts | no lexicon |
| homophones, one word per letter or syllable | exp. 44 | Latin ciphers of Voynich words (0.28-0.69 bits) | 0.09, mostly the boundary habit |
| fixed tables of any kind | exp. 43 | Naibbe cipher (0% page identity) | 34-73% page identity |
| a new key on every sheet | exp. 47 | Latin ciphers, one key vs key per sheet | same rules on every sheet |
| a few bits per word in the forks | exp. 54 | Latin at 1, 2, 4 bits per word | nothing in any channel |

## What is left

- A residual link between neighbouring words that no habit I can model makes, in A and B and in
  two transcriptions (exps. 48-51). It doesn't form a consistent grammar (exp. 52) and decomposes
  into false spaces, a rhythm, and repeated pairs without word order (exp. 53).
- Channels not calibrated: the gallows, word length, *e*-runs, line position; text written with a
  plaintext that is itself near random.
- Labels behave like a separate vocabulary (exp. 45), and ring/circle text has hardly been looked
  at on its own.

On everything measured so far, a scribe following a short table, re-set at each sheet and
carrying a few habits of rhythm, accounts for the text, and no calibrated way of hiding a language
in it does.
