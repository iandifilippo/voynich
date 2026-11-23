# 50 — Can habits alone make the 0.30 bits?

## What I think

Exp. 48 found 0.30 bits shared between neighbouring words of Currier B beyond the glyphs at
the space and the sheet's setting, against 0.02 for my generator. Before calling that a
message, the generator should get every habit I already know the scribes had. So:

- a **setting per sheet**: random weights on word starts, gallows and endings, drawn once per
  sheet (exps. 40-42), strength sigma;
- a **favoured gallows per line** (exp. 49), strength hold.

sigma and hold were fitted to B's sheet identity and same-line gallows agreement. The measure
under test was not used for fitting.

## Result

| | sheet identity | gallows same line / other line | beyond the boundary (bits) |
|---|---|---|---|
| Currier B | 0.98 | 1.07 | **0.30** |
| generator, no settings | 0.10 | 1.05 | 0.07 |
| generator, fitted settings (sigma 0.9, hold 2.5) | 1.00 | 1.08 | 0.12 |

Habits explain part of it (0.07 → 0.12) and no more: the settings match B's sheet identity and
line agreement exactly, and the link between neighbours stays at less than half.

What the rest is made of (`residual.py`): split into repetition (a word taking the same start,
gallows or ending as the word before) and structured transitions (particular values followed by
particular other values, measured only on pairs that differ):

| | repeat excess (start / gallows / ending) | off-diagonal CMI (start / gallows / ending / length) |
|---|---|---|
| Currier B | 0.004 / 0.032 / 0.018 | **0.028 / 0.010 / 0.014 / 0.008** |
| generator with settings | 0.008 / 0.018 / 0.011 | −0.006 / −0.006 / 0.006 / −0.004 |

The generator's repetitions are as large as B's; its structured transitions are zero. B's aren't.

Could doubtful spaces be making it (`spacing.py`)? The transitions that carry most of it involve
short pieces (*or → aii*, *ar → al*, *da → al*), like words cut at an uncertain space:

| Currier B | beyond the boundary |
|---|---|
| as everywhere so far | 0.30 |
| words of 3+ signs only | 0.24 |
| doubtful spaces read as no space | 0.26 |
| no doubtful spaces, 3+ signs only | 0.24 |
| generator with settings, 3+ signs only | 0.07 |

## So what

About 0.17 bits per pair of neighbouring words in Currier B is structure I can't make with any
habit I know of, survives removing doubtful spaces and short words, and isn't repetition: it's
which kind of word tends to follow which other kind. That is the shape a sequence carrying
information has. It's small (a one-letter-per-word cipher of Latin leaves 0.88), but it is the
first residual in this whole series that survives every content-free control I've built.

It doesn't decide the question. A habit I haven't thought of could make it. But it says where
any decipherment would have to start: not with the glyphs of single words, and not with whole
words, but with the classes of word that follow each other.

## Caveats

- Plug-in conditional MI with permutation baselines; the generator gives a sense of the noise
  (±0.006 per feature pair).
- The settings model is one specific way to have per-sheet and per-line habits. A richer habit
  model could close more of the gap; that's the next thing to try to break this result.

**Later (exp. 61):** the generator used here reset its echo of recent words at every line (a bug in
`fill_sheet`). Fixed in exp. 61. Exp. 61 also shows that copying short runs within a sheet (one in 10-15
words) makes the beyond-the-boundary link on its own.
