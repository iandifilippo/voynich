# 47 — Attack 6: is the code different on every sheet?

## What I think

Two results pull in opposite directions. Exp. 43: a cipher with one set of tables can't give
sheets their own setting, so if the manuscript is a cipher, the key changed per sheet. Exp. 44:
Currier B's words depend on their neighbours far less than any letter or syllable cipher of
Latin would. A key per sheet would explain both: pooling sheets with different keys scrambles
which word stands for what, and the sequence washes out across the book while staying intact
inside each sheet.

That makes a sharp prediction. Measure the dependency between neighbouring words inside each
sheet and across the whole section: with a key per sheet, inside ≫ pooled; with one code for
the book, inside ≈ pooled.

## What I did

For the links a cipher would carry (first sign → next first sign, last → next last, first →
next last, last → next first, and the word's start-end shape → next shape), the MI pooled over
the section and averaged inside sheets, both corrected by the same baseline (words shuffled
inside each sheet among words at the same line position).

Calibrated on two ciphers of Latin made of Voynich words (one word per letter, about 5
homophones each) laid out in B's own sheets and lines: one key for the whole book, and a new key
on every sheet. Control: the exp. 36 generator, which has no key at all.

## Result (bits)

| | first → first: pooled / inside | shape → shape: pooled / inside |
|---|---|---|
| cipher of Latin, one key | 0.034 / 0.032 | 0.154 / 0.091 |
| **cipher of Latin, new key every sheet** | **0.000 / 0.027** | **0.047 / 0.131** |
| generator, no key | 0.019 / 0.022 | 0.231 / 0.127 |
| Currier B | 0.067 / 0.074 | 0.297 / 0.209 |
| Currier A | 0.051 / 0.051 | 0.161 / 0.069 |

The calibration works: a key per sheet leaves almost nothing pooled and a clear signal inside
sheets, the reverse of one key. The manuscript, A and B alike, looks like one key or no key:
pooled is as large as inside, or larger.

## So what

The rules between neighbouring words are the same on every sheet; only the way words are built
changes from sheet to sheet. That rules out the per-sheet-key cipher that exp. 43 left open,
at least any cipher of the one-word-per-letter kind. Combined:

- one key for the book → sheets wouldn't have their own setting (exp. 43);
- a key per sheet → the neighbour links would be sheet-specific (this test), and they aren't;
- a codebook (word per word) → there'd be a lexicon (exp. 34), and there isn't.

None of the cipher families I can calibrate fits all of exps. 34-47 at once. What fits is a
procedure whose word-building is re-set per sheet and whose word-to-word rules (mostly the
boundary habit, exp. 46) are a constant habit of the writer. That's what a person generating
text without a plaintext would produce, and it is what my generator (exp. 36) does once a
per-sheet setting is added.

## Caveats

- The calibration ciphers put one letter in each word. A scheme that spreads a letter over
  several words, or puts several bits in the fork choices of each word, was not calibrated.
- Sheets are 100+ words; per-sheet MI is noisy and the bias correction matters a lot (the
  shape-shape numbers are lower inside sheets for every text, including the one-key cipher,
  because the baseline also absorbs part of the effect). The comparison that matters is between
  the two calibration ciphers and the manuscript, all measured the same way.
