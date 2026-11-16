# 22 — How local are words?

## Why

Exp. 21: the copying model has enough one-off words but too many of middling frequency and too
weak a core. Copying from the lines just above is a local process: a new variant gets copied
nearby a few times, then drifts out of reach. If VMS words don't behave like that, the fix
isn't another mutation rule.

## What I did

"Lift": for a word that's in line i, how much more likely than its base rate is it to be in
line i+k, for k from 1 to 100, split by how common the word is. Same for a second occurrence
within the line. VMS A and B, Latin, Italian, Naibbe, and the copying model with two changes
to where it copies from:

- **from anywhere**: a share of sources drawn from the whole text so far;
- **prefer common**: if the word about to be copied has been written fewer than three times,
  look again with probability c.

## Result

Lift one line later:

| | core words (21+) | middle (6-20) | low (2-5) |
|---|---|---|---|
| VMS Currier B | 1.7 | 1.9 | 2.2 |
| VMS Currier A | 1.5 | 3.1 | 4.0 |
| Latin | 1.0 | 1.8 | 2.2 |
| Italian | 1.4 | 4.5 | 11.4 |
| Naibbe of Pliny | 1.0 | 1.1 | 0.7 |
| copying model | 1.9 | 8.1 | 17.2 |

- **VMS rare words are barely local.** A middling or rare word is only about twice as likely
  as chance to come back on the next line; in the copying model it's 8 to 17 times. The
  model's rare words are born, copied nearby, and gone 100 lines later (lift 0.6-0.9); the
  VMS's are still slightly above chance at 100 lines (1.2-1.4).
- **VMS common words are the local ones**: lift 1.5-1.7 on the next line, fading over about
  25 lines. In Latin the common words have no locality at all (1.0); they're function words.
  The VMS core behaves like the copying model's core, not like function words.
- Copying from anywhere flattens everything, including the line cohesion the VMS has
  (1.09 vs 1.95). Not that.
- **Prefer common works.** At c = 0.5:

| | VMS B | model | + prefer common 0.5 |
|---|---|---|---|
| text covered by the core | 54% | 30% | 51% |
| line cohesion | 1.95 | 2.53 | 1.84 |
| MATTR-500 | 0.54 | 0.62 | 0.51 |
| h2 | 1.94 | 2.32 | 2.02 |
| distance (to whole MS) | 1.23 | 2.18 | **1.49** (sd 0.25, 4 seeds) |

  One rule moves five numbers to the right place. Distance 1.49 is close to how far Currier B
  itself sits from the whole-manuscript profile (1.23).
- Not fixed: the model's rare words are still 3-6× too local (6.8 and 13.5 vs 1.9 and 2.2),
  hapax 0.61 vs 0.68, and immediate repeats 6 vs 9 per 1000.

## Someone got here first

Schwartz (preprint, October 2026) fits a keyless procedure to scribes 1 and 2 with three
branches: reuse of a word from the scribe's own vocabulary, drawn by frequency (73-77% of
words), verbatim copying from the last ~20 words (2-5%), and coining new words from letter
habits (18-25%). He concludes that Timm & Schinner's process, with a local copy rate of
0.42-0.48, isn't the manuscript's. "Prefer common" below is a crude version of his reuse
branch, reached from the other side; the locality table is my evidence for the same thing.
What I add is small: the lift-by-frequency-band measurement, and that one change to the
published generator is enough to move core, cohesion, MATTR and h2 together.

## So what

The picture that fits: the writer works from a small set of familiar words, repeats them
with a memory of a couple of dozen lines, and produces variants *of those words* as one-offs.
The variants are not themselves copied much. In Timm & Schinner's procedure every word on
the page is an equally good model; in the manuscript, a word seems to need to be familiar
before it's reused.

Caution on the score: the model now has three fitted rates (boundary 0.65, line end 0.5,
prefer common 0.5) and a boundary list read off the manuscript. Distance 1.49 is measured on
the same 13 metrics I've been watching while adding them. Exp. 23 checks the model on things
I didn't look at.
