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
  tested, by 0.7-3.8 bits per word, and not at all in the manuscript (exp. 34), however the words are
  cut, including by the physical gaps on the page (exp. 55).
- **The setting belongs to the sheet.** Each page has its own weighting of the forks, held to the
  end of the page (exp. 40); it survives removing shared words, unlike copying, and real texts
  barely show it. Pages of the same folded sheet share it even when fifteen folios apart, more
  than pages that face each other in the binding (exps. 41-42). The sheets were written as units,
  before the present binding (cf. Davis's singulions).
- **Habits between words.** A link across the space (exp. 46: last sign → next first sign, 0.25
  bits in B) that turns out to be mostly the inside of words split by the transcription: measured on
  the page it is 0.42 bits at the narrowest gaps and 0.08 at the widest (exp. 55); a favoured gallows along a line (exp. 49), echoes of recent words (exp. 36), a
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
| a few bits per word in the forks (plaintext down to random digits, exp. 59) | exp. 54 | Latin at 1, 2, 4 bits per word in qo-, start, end, gallows, length, e-run | nothing in B; in A a weak e-run habit inside lines |
| pharma labels are the plant names used in the herbal text | exp. 64 | label planted once in its twin page, exact or one sign off (p .002) | 0 of 41 labels in the twin page, not nearer than chance |

## What is left

- A residual link between neighbouring words, in A and B and in two transcriptions (exps. 48-51) and
  between physically separate words (exp. 55). Copying short runs within a sheet, one in 10-15 words,
  makes it (exp. 61): it needs no message. The ch/sh-…-y → qo- rhythm is a table of the next word's
  family by the previous word's family and ending, small enough to keep on a card; drawing word
  starts from it gets most of the rhythm and two thirds of the link (exp. 65). Still unmade:
  neighbouring lines of a page share their qo- and ending shares over two or three lines (exp. 65).
- The best single model (exp. 61: rule + sheet setting + echo + copied runs) passes 7 of 11 held-out
  statistics (exp. 60 scorecard). It doesn't form a consistent grammar (exp. 52) and decomposes
  into false spaces, a rhythm, and repeated pairs without word order (exp. 53).
- Channels not calibrated: line position, combinations of channels. Abbreviated text and numbers
  would have shown (exp. 59); only a code made statistically flat would not.
- Measured letter by letter (exp. 66), the transcribers' doubtful spaces are a third size of gap between letters and spaces, the end-start link sits in narrow spaces (0.64 bits across doubtful ones, 0.07 across the widest real spaces), and the qo- rhythm crosses wide spaces unchanged.
- Zodiac labels carry no calendar that shows in word shape (exp. 58).
- Labels behave like a separate vocabulary (exp. 45), and ring/circle text has hardly been looked
  at on its own.

On everything measured so far, a scribe following a short table, re-set at each sheet and
carrying a few habits of rhythm, accounts for the text, and no calibrated way of hiding a language
in it does.
