# 16 — What does a comma mean?

## Why

ZL writes `,` where the transcriber wasn't sure there was a space. Every experiment so far
reads it as a space. In c02 I found that about a third of those commas glue into a word that
exists elsewhere, so a fair share of them probably aren't spaces. If some headline numbers
depend on that choice I want to know now, not after writing them up.

## What I did

Added a `commas=` option to the parser (`split`, `smart`, `join`). `smart` glues across a comma
only if the glued form occurs at least twice elsewhere in the text. Reran the full profile for
all / A / B under each reading, ranked each metric against the 18 historical texts, measured how
far the readings sit from each other (using the A-B gap as a yardstick), and rescored
Greshko's published Naibbe output against each.

## Result

- `smart` glues ~800 of 38 700 tokens; `join` ~2 700. Mean word length 4.99 → 5.11 → 5.37.
- **Robust to the comma choice:** h2 is lowest of all 18 under every reading (2.15 / 2.15 / 2.18),
  h1 lowest, word MI lowest, line-first and line-last JSD highest, line cohesion 17/18.
- **Not robust: edge coupling.** 0.147 (15th of 18) under `split`, 0.121 (11th) under `smart`,
  0.108 (9th) under `join`. Part of the cross-word coupling I'd been treating as a VMS oddity
  comes from boundaries that probably aren't boundaries.
- The whole shift split → smart is 0.18 benchmark units; the A-B gap is 1.1-1.3. So the comma
  question is small next to the dialect question, except for coupling.
- Naibbe core distance 0.94 (split) → 0.80 (smart): it looks a bit better once fake boundaries
  are removed, but edge coupling is still its worst metric (-1.7).

## So what

Two corrections to earlier write-ups:

1. "Strong edge coupling" should be "edge coupling in the upper half of natural texts". It's still
   real (any word-by-word cipher gives ~0) but it's not extreme. The autokey target in exp. 13
   should be ~0.12, which by interpolating the sweep means p ≈ 0.58 rather than 0.65.
2. Anything about the first or last glyph of words should be checked under `smart` before it
   goes in a paper. The line-position effects survive; I've checked those here.

I'm keeping `split` as the default so old results stay reproducible.
