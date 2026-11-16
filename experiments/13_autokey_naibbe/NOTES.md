# 13 — An autokey for the Naibbe cipher

## Where this comes from

community/c01 left one clear gap. Greshko's Naibbe cipher gets the inside of words right
(entropy, word length, vocabulary close enough) but consecutive words are independent: the
last glyph of one word says nothing about how the next one starts. In the VMS it does
(0.17 bits after removing frequency effects, and it holds across certain spaces only, so it
isn't a comma artifact).

In Naibbe the reason is mechanical. Every word's table comes from a fresh card. If the choice
of table depended on what was just written, the coupling would appear for free.

## Hypothesis

A rule a scribe could actually follow: look at the last glyph of the word you just wrote, and
use a small fixed chart to pick the next table (ends in y → table 1, ends in n → table 2, …).
Do it most of the time, draw a card otherwise. Progressive and autokey ideas are 15th–16th
century (Belaso published the classic autokey in 1553), and this needs nothing beyond the
tables Greshko already proposes.

Prediction: coupling appears and scales with how often the rule is used, everything else stays
put. Harder prediction: with the right chart, the *pattern* of coupling (which endings are
followed by which beginnings) should match the VMS, not only the amount.

## What I did

- Reimplemented the cipher from Greshko's published tables and checked it against his own
  ciphertext on the same plaintext units: h2 2.11 vs 2.09, hapax 0.59 vs 0.58, edge 0.004 vs
  0.004. Same thing.
- Swept the autokey probability from 0 to 1 with an arbitrary chart, on Pliny (his test text)
  and Dante (his Italian one).
- For the pattern: computed PMI for every (last glyph, next initial) pair in the VMS. Fitted a
  chart to the odd lines of the manuscript, then compared the cipher it produces with the even
  lines, which the fit never saw. Compared with 20 random charts.
- Full benchmark with lines and paragraphs cut to the VMS length distributions, with and
  without Smith's line-start transformation (s/d/t in front of line-initial words with
  probability q, gallows at paragraph starts).

## Result

Amount: coupling goes 0.006 → 0.08 → 0.15 → 0.37 as p goes 0 → 0.5 → 0.65 → 1. At p ≈ 0.65 it
matches the VMS (0.15) for both plaintexts. h2, hapax, word length and Zipf don't move.

Pattern: the VMS agrees with itself at 0.98 (odd vs even lines). Random charts: 0.00 on average,
0.16 at best. The fitted chart: 0.43 on held-out lines with Pliny, 0.24 with Dante. So an autokey
gets part of the way, and the tables themselves limit how far: the strongest VMS pairs (o|r, s|a,
o|l, r|a, y|qo) need specific word starts right after specific endings, and Naibbe's tables
don't offer all of those.

Benchmark (lower is closer to the VMS):

| variant | distance | word-level distance |
|---|---|---|
| Naibbe as published | 4.86 | 0.86 |
| + autokey | 4.78 | 0.70 |
| + autokey + line-start rule | 3.92 | 0.49 |
| VMS later pages (floor) | 1.06 | 0.18 |

What none of the variants touch: line-final behaviour (words ending in -m at line ends),
immediate word repeats, and how much words repeat inside a line.

## So what

Edge coupling isn't evidence against a cipher; one hand-executable rule produces the right
amount of it. The exact pattern is harder and probably says something about the tables, not
just the procedure. Next: let the chart and tables co-evolve (still checked on held-out lines),
and look at the three line-level properties nothing reproduces yet. Those may be where the
scribe, not the cipher, shows.
