# 65 — The rhythm, taken apart

## Why

Exps. 62-63 left one thing no generator of mine makes: in Currier B a *ch-/sh-…-y* word is followed
by a *qo-* word twice as often as chance, and how often depends on the family of the *-y* word, not
only on its last signs. If the book was written by hand following some rule, that rule has to be
simple enough to use while writing. So I first looked at the rhythm in more detail and then tried
rules a scribe could follow.

## What the rhythm is

Next word's family (qo-, ch/sh-, o-, other) by the previous word's family and ending, over the base
rate, all B sheets (`results/family_link.md` has the full table):

| previous | next qo- | next ch/sh- | next o- |
|---|---|---|---|
| ch/sh-…-y | 1.90 | 0.59 | 0.80 |
| qo-…-y | 1.82 | 0.69 | 0.84 |
| o-…-y | 1.64 | 0.64 | 1.00 |
| other-…-y | 1.45 | 0.77 | 0.78 |
| qo-…-n | 0.41 | 1.74 | 1.36 |
| ch/sh-…-n | 0.79 | 1.63 | 1.17 |
| o-…-r | 0.26 | 0.96 | 1.33 |

Three things come out of it:

1. **A table on a card.** After *-y* comes *qo-*, after *-n*/*-l*/*-r* comes *ch-/sh-* or *o-*, and
   the family of the previous word changes the strength (after *ch/sh-…-y* most, after *other-…-y*
   least). Twenty cells.
2. **qo two words back.** *qo-* is more likely when there was a *qo-* two words back (1.37), more than
   shuffling inside the line gives (1.27). Most of that comes from the table: a chain that only
   draws each word's family and ending from the one before gets 1.10 over its own shuffle, against
   B's 1.14. A chain on families alone, without endings, gets 1.00.
3. **Lines.** The qo- share of a line varies 1.4 times more than chance. Neighbouring lines share
   their qo-, -y and -n shares (r 0.16 with the sheet mean removed). Most of that is the page: with
   each page's own mean removed what's left is 0.09 against −0.04 for shuffled lines, gone by five
   lines. It doesn't reset at paragraph starts (0.20 across a paragraph start vs 0.20 within one, for
   -y).

## What I tried

The generator of exps. 60-61, with:

- **family link**: a word's start is drawn given the previous word's family and last sign
  (`link_by="family"`), instead of the last sign only;
- **line setting**: each line gets weights for families of starts and for endings,
  exp(N(0, σ)), drawn afresh or drifting from the line before (`line_sigma`, `line_drift`);
- **echo from above**: repeats and one-sign edits reaching back 15-25 words, preferring words whose
  start fits the link (`window`, `echo_fits`).

Choice on even sheets, scoring on odd sheets, mean of 5 seeds:

| | rhythm | lag 2 | beyond the boundary (bits) | recurring pairs | neighbours | within (of 11) |
|---|---|---|---|---|---|---|
| Currier B, odd sheets | 1.93 | 1.10 | 0.23 | 0.054 | 0.13 | – |
| exp. 61 (last sign) | 1.57 | 0.98 | 0.10 | 0.021 | 0.01 | 7 |
| family link (chosen) | 1.79 | 1.04 | 0.15 | 0.025 | 0.00 | 6 |
| family link + echo from above | 1.86 | 1.02 | 0.11 | 0.021 | 0.06 | 5 |

The line settings, tried on the even sheets, didn't help. To get neighbouring lines to agree at all
they have to swing the line shares far too much (σ 0.6, drift 0.9: neighbours 0.11 but spread 1.81
against B's 1.31).

## So what

The rhythm turned out to be one small table. Drawing word starts from it brings the rhythm from
1.57 to 1.79 (B 1.93) and the link between neighbouring words from 0.10 to 0.15 bits (B 0.23). Once
the table is there, most of the qo- two words back follows from it. A scribe could carry that table
in his head after a few pages, and it needs no message: it is about the shapes of words.

What I can't make is the agreement between neighbouring lines on a page. A setting re-drawn per line
over-shoots, and copying from the lines above gets a third of it while adding too many new words.
Taken together, every page has its own setting (exp. 40) and the two or three lines just written
weigh on the next one. That's the next thing to model, and it fits a scribe who looks back up the
page as he writes (Timm & Schinner's idea), with a narrower reach than their generator has.
