# 19 — Can copying make enough rare words?

## Why

After exp. 18 the copying model's biggest word-level miss is the hapax ratio: 0.55 against
0.68 for Currier B. The obvious fix is to change copies more.

## What I did

One extra knob: with probability q, every new word gets one more glyph substitution on top
of its normal change. Boundary habit from exp. 18 kept on (p = 0.65). q = 0, 0.3, 0.6, 0.9,
3 seeds each, B settings.

## Result

| | hapax | MATTR-500 | line cohesion | near-repeats (null) | distance |
|---|---|---|---|---|---|
| VMS Currier B | 0.684 | 0.535 | 1.95 | 33.7 (30.5) | 1.23 |
| q = 0 | 0.551 | 0.564 | 1.99 | 34.0 (27.9) | 2.42 |
| q = 0.3 | 0.561 | 0.590 | 1.95 | 29.1 (25.3) | 2.78 |
| q = 0.6 | 0.594 | 0.595 | 1.66 | 28.9 (27.1) | 2.49 |
| q = 0.9 | 0.593 | 0.599 | 1.67 | 28.6 (27.2) | 2.86 |

- Hapax barely moves (0.55 → 0.59) and stalls; cohesion and the near-repeat excess, the
  things copying gets right, are what it costs.
- The telling number is MATTR: the generator is *already* more diverse than the VMS locally
  (0.56 vs 0.54) while having fewer hapaxes. So it isn't short of variety, it's short of
  singletons. The VMS has more words that occur once and fewer mid-frequency words than a
  copying process makes.

## So what

More mutation isn't the fix. Copying spreads probability evenly over a cloud of variants of
whatever is on the page; the VMS has a longer tail of one-offs. Two readings: the scribe
sometimes wrote words that weren't copies (from a fixed stock, or freshly built from parts),
or the transcription splits/merges words in a way that creates singletons (exp. 16: under
the `join` reading hapax goes up to 0.72). The second is checkable: rerun the generator
comparison under each comma reading. Logged as the next thing to do; I'm leaving q = 0 as the
default.
