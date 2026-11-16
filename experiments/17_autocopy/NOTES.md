# 17 — Timm & Schinner's self-citation generator

## What they claim

Timm (2014) and Timm & Schinner (2020) argue there's no hidden plaintext at all: the scribe
wrote each word by looking at a word already on the page, usually in the line above at about
the same horizontal position, and changing it a little (swap a glyph for a similar one, add
or drop a prefix, glue two words, split one). Their app, VoynichTextGenerator, implements this
with explicit rule tables.

## What I think

It's the only serious proposal that explains why neighbouring lines share vocabulary and why
near-identical words cluster, which no cipher I've tested does (exp. 15). But it was tuned
by eye on a few pages, and I haven't seen it run through a battery like ours. I also expect it
to fail on edge coupling: copying a word from the line above shouldn't tie its first glyph to
the last glyph of the word to its left.

## What I did

Reimplemented the generator in Python (`voynich/autocopy.py`) from the app's source: same
substitution tables, prefix rules, gallows handling, line-end shortening, source choice by
position. Their repo has no license, so this is a reimplementation of the procedure, not a
translation of their code; their structure is simplified where it only served the app's UI.
Eight seeds each for Currier A and B settings, 1400 lines each (~11k words), scored like
everything else.

## Result

| model | distance | core | edge | hapax | h2 | line cohesion |
|---|---|---|---|---|---|---|
| VMS Currier B (for scale) | 1.23 | 0.71 | 0.245 | 0.68 | 1.94 | 1.95 |
| Naibbe (Greshko, published) | 4.54 | 0.94 | 0.002 | 0.58 | 2.09 | – |
| autokey Naibbe + line-start rule (exp. 13) | 3.92 | 0.49 | 0.143 | 0.63 | 2.15 | – |
| **self-citation, A settings** | **2.45** | 1.03 | 0.009 | 0.54 | 2.35 | 1.45 |
| **self-citation, B settings** | **2.46** | 0.97 | 0.013 | 0.55 | 2.22 | 2.01 |

Seed-to-seed spread is small (distance sd 0.15-0.20, core sd < 0.05).

- **Best overall distance of anything we've run**, and it gets there on the line metrics:
  line cohesion is right for B (2.01 vs 1.96), the near-repeat excess from exp. 15 appears
  (36.8 vs 28.2 shuffled-in-line; VMS 36.0 vs 30.8).
- **No edge coupling at all** (0.01 vs 0.15), as I expected. Same failure as every cipher.
- Vocabulary too repetitive: hapax 0.55 vs 0.69. h2 a little high.
- Line ends don't look like the VMS (line_last_jsd −7.3): the shortening rule fires too
  rarely. Line starts too weak too: d-, t-, q- initial lines are under-represented (2-7% vs
  10-15%).
- Exact repeats slightly *below* the in-line null (7.8 vs 8.6), because the generator throws
  out half of its immediate duplicates. The VMS shows no such avoidance.

## So what

The two families fail in opposite places. Ciphers built from a real plaintext get word
structure right and line structure wrong; the copying model gets line structure right and
word structure slightly wrong. Neither produces the cross-word glyph coupling, and only the
autokey rule (exp. 13) does. That makes the coupling the most useful discriminator we have:
any complete account has to say why the end of one word predicts the start of the next.

Next obvious test: autocopy + an autokey-like rule at the boundary (pick the source word
partly by its first glyph). If that closes the gap, the "no plaintext" model would match
everything we measure — which would be a strong result for Timm & Schinner, and a bad one
for anyone hoping to translate.
