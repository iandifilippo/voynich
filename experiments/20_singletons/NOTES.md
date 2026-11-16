# 20 — What are the one-off words?

## Why

Exp. 19 ended on a puzzle: the copying model is locally more varied than the VMS but makes
fewer words that occur only once. Before changing the model again I wanted to look at the
singletons themselves. If they aren't copies, the copying model is the wrong tool.

## Hypothesis

In a real language a rare word is rare because of what it means, and it looks like nothing
else nearby. If VMS singletons are mostly a known word with one glyph changed, they are
variants, not vocabulary.

## What I did

First 10 000 words of each text. A singleton is "one edit from known" if adding, dropping or
changing one glyph gives a word that occurs 2+ times in the same sample; failing that, "two
known joined" if it splits into two such words. Then where singletons sit in the line, and
for those one edit away, which edit and at which end of the word.

## Result

| | singletons / types | one edit from known | two known joined | neither |
|---|---|---|---|---|
| VMS Currier A | 0.69 | 64% | 15% | 22% |
| VMS Currier B | 0.68 | 63% | 15% | 23% |
| copying model (B) | 0.55 | 66% | 12% | 22% |
| Naibbe of Pliny | 0.58 | 81% | 2% | 16% |
| Latin (Aix) | 0.67 | 17% | 1% | 82% |
| Italian (Rettorica) | 0.72 | 18% | 26% | 56% |

- **VMS singletons are variants.** Four in five are a known word with one glyph changed, or
  two known words run together. In Latin and Italian it's the other way round. The make-up
  is almost exactly what the copying model produces. Reading commas the `smart` way changes
  nothing.
- **They pile up at the line edges.** Singleton rate: first word 27-29%, mid-line 13-17%,
  last word 24-29%. Latin and Italian are flat (20-25% everywhere). Paragraph-opening
  words: 47%. Labels: 36%.
- **The edges make them in different ways.** Line-first singletons are a known word with a
  glyph added *in front* (38-40% of them, against ~20% mid-line): *p, t, y, s, d* in B.
  Line-last singletons are a known word with a glyph added *at the end* (15-19% against
  7-11%): *y, d, g, s, m*.
- The copying model matches the VMS at line start (0.29) and mid-line in B (0.12 vs 0.13) and
  misses the line end completely (0.11 vs 0.24).

## A disagreement to resolve

Schwartz (2026) reads boundary words as distinct words, not edge-modified forms. My numbers
say otherwise for the singletons: 38-40% of line-first singletons are a known word with one
glyph in front (about 20% mid-line), and exp. 10's deficit/surplus correlation points the
same way. We're measuring different things (he scores all boundary words under a fitted
model; I count one-edit links for singletons), so both can be partly right, but it needs a
head-to-head on the same definition.

## A correction to exp. 14

In 14 I tested whether line ends *rewrite* an ending (-l → -m and so on) and found nothing.
That still stands. What I didn't test was *adding* a glyph, and that does happen: the line
end tacks something on. "Starts rewrite, ends don't" should read "starts prefix, ends
suffix; neither swaps".

## So what

The one-off words are not a hidden vocabulary. They're what you get when words are altered
at the edges of the line. That is bad news for reading them as rare nouns or names (which is
what the *tolor* post did, c06), and it gives the model a concrete thing to add: a rule at
the line end. Exp. 21.
