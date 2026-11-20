# 44 — Attack 5: does a word's neighbour give away what it stands for?

## What I think

Every cipher where a word stands for a letter (or a letter in context) leaves a trace that
doesn't depend on spelling, language or how words are cut: words for the same letter behave
alike towards their neighbours. Group the words so that one word's group predicts the next
word's group as well as possible, and the groups become the alphabet. It's the oldest attack on
homophonic ciphers, done here by exchange clustering (`voynich/crack/classes.py`), and it can't
be fooled by the slot grammar because it never looks inside a word.

## What I did

Classes fitted on half of each text (even pages), scored on the other half: the mutual
information between the classes of adjacent words, minus the same with classes fitted on the
training half with its words shuffled. Words seen fewer than 5 times are merged into one token
(with every rare word its own item, the classes memorise noise and the method fails even on the
Naibbe cipher: first pass, in the results). Then two checks on what the signal is:

- `lags.py`: the same MI at distance 1, 2, 3, 5 in the line, and for two random words of the
  same page. A page setting (exp. 40) predicts the same value at every distance; sequence
  predicts a peak at 1.
- `edges.py`: held-out text shuffled only among words with the same first and last sign, which
  keeps every word boundary's glyphs and destroys everything else. Exp. 18 found a habit at word
  boundaries; this shows how much of the sequence is that habit.

## Result

Held-out MI between adjacent words' classes (bits, above shuffled training):

| | K = 8 | K = 16 | K = 32 |
|---|---|---|---|
| Naibbe cipher of Latin (calibration) | 0.04 | 0.04 | 0.05 |
| **Currier B** | **0.09** | **0.09** | **0.08** |
| Currier A | 0.01 | −0.01 | −0.00 |
| copying model | 0.01 | 0.01 | 0.03 |
| assembled words (exp. 36) | 0.03 | 0.02 | 0.04 |
| Latin, words | 0.09 | 0.13 | 0.13 |
| Italian, words | 0.25 | 0.31 | 0.32 |

By distance (K = 16):

| | 1 | 2 | 3 | 5 | same page, any distance |
|---|---|---|---|---|---|
| Currier B | 0.083 | 0.012 | 0.010 | 0.006 | 0.006 |
| Latin, words | 0.149 | 0.021 | 0.002 | 0.005 | −0.001 |
| Naibbe cipher | 0.039 | 0.000 | 0.002 | −0.005 | −0.000 |
| Currier A | 0.005 | −0.005 | −0.002 | −0.019 | −0.002 |

Held-out text reshuffled under constraints (distance 1):

| | as written | keep first sign | keep first and last sign | keep first two and last two |
|---|---|---|---|---|
| Currier B | 0.083 | 0.006 | 0.051 | 0.073 |
| Latin | 0.135 | 0.001 | 0.025 | 0.112 |
| Italian | 0.305 | 0.005 | 0.039 | 0.257 |

1. **Calibration only half works.** On the Naibbe cipher the classes find real sequence (0.04),
   but they don't become the alphabet: most Naibbe words carry two letters, and rare homophones
   get merged. So this is a detector, not yet a decoder.
2. **Currier B has word-to-word sequence**, twice the Naibbe cipher's, two thirds of Latin's,
   peaking at the next word like a language and unlike a page setting. Nothing content-free I
   have makes it: the copying model and the assembled-words generator give 0.01-0.04.
3. **About 60% of it is the boundary habit** (the last glyph of one word with the first glyph of
   the next): keeping just those glyphs keeps 0.051 of the 0.083. In Latin and Italian the same
   constraint keeps only 13-19%. The remaining 0.03 bits is sequence between words as such.
4. **Currier A has none at all.** Adjacent words in A are as independent as words drawn at
   random from the same page. No language I know of does that in running prose.

## So what

This is the first place where Currier B does something none of my content-free generators do,
and it's in the dimension a message would live in: what follows what. Most of it is the glyph
habit at word boundaries, which a scribe could have without any message, but a residue remains.

Currier A is the opposite: whatever A is, its words are not a sequence. That fits a list (of
names, ingredients, labels), an encoding that scrambles order, or text without content. It is
also the strongest argument I have so far that A and B aren't two dialects of one thing.

## Caveats

- The edge-habit control keeps the first and last *sign* in my segmentation; with *e/ee/eee* as
  separate signs, some word identity leaks into "edges", which makes the 60% an upper bound.
- K and the rare-word threshold were chosen on the first pass, which included all texts.
- The generators don't model the boundary habit exactly (the assembler links the first sign to
  the previous last sign, which is the same habit), so the residue is the number to watch.
