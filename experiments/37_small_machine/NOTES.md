# 37 — How small can the word rule be?

## What I think

Exp. 36 matched Voynich words with a sign chain that looks two signs back. That has thousands of
parameters, and nobody in the 15th century wrote with a probability table of thousands of
entries. A scribe following a table, a volvelle or a habit is a machine with a handful of
states: in this state write one of these few signs, then move on. If the words come from
something like that, a small machine should be enough. If they come from a vocabulary, no
small machine will be.

## What I did

A hidden Markov model whose hidden states are the machine's states and whose outputs are EVA
signs plus the word space, trained by EM on the even pages, K = 2 to 48 states. Two scores on
the odd pages: held-out bits per sign, and the vocabulary the machine writes when asked for as
many words as the held-out half (exp. 36's measures). Same for Currier A, Latin, Italian, the
Naibbe cipher of Pliny and the copying model. All cut to comparable size (12 000 words per half).

## Result

Held-out bits per sign; sign chains for reference:

| | 12 states | 24 | 48 | best sign chain |
|---|---|---|---|---|
| Currier B | 2.22 | 2.03 | **1.97** | 1.97 (2 back) |
| Currier A | 2.51 | 2.28 | **2.25** | 2.25 (2 back) |
| Naibbe cipher of Latin | 2.38 | 2.13 | 2.03 | 2.04 (3 back) |
| copying model | 2.40 | 2.17 | 2.11 | 2.12 (2 back) |
| Latin | 3.28 | 3.06 | 2.84 | **2.25** (3 back) |
| Italian | 3.16 | 2.97 | 2.71 | **2.13** (3 back) |

What a 48-state machine writes, against the held-out text:

| | distinct per 1000, real / machine | words not in training half, real / machine |
|---|---|---|
| Currier B | 248 / 264 | 17% / 20% |
| Currier A | 348 / 344 | 24% / 25% |
| Latin | 355 / 669 | 23% / 76% |
| Italian | 264 / 533 | 19% / 66% |

A 48-state machine is as good as the best sign chain for Voynich, Currier A and B alike, and
writes a vocabulary of the right size with the right rate of new words. For Latin and Italian
it is far worse than a three-letter chain and writes three times too many distinct words, three
quarters of them never seen: a few dozen states can't hold a language's words. The two
content-free controls behave like the manuscript.

## So what

The difference between a rule and a vocabulary, measured in states: Voynich words are fully
described by a machine of a few dozen states; words of a language are not. Exp. 38 reads what
the machine is.

## Caveats

- EM finds local optima; three starts per K. The curves are smooth enough that this doesn't
  change the picture, but the exact K where the machine catches the chain is soft.
- Latin and Italian have more letters per word, so bits per sign aren't directly comparable
  across languages; the comparison that matters is machine against chain within each text.
