# 21 — A line-end rule, and what it doesn't fix

## Hypothesis

From exp. 20: the copying model's singleton shortfall is at the line end. If the last word of a
line gets one more change (often a glyph tacked on), then one setting should fix three things
at once: the line-final singleton rate, the line-end word distribution (`line_last_jsd`, our
worst metric at −7), and the overall hapax ratio.

## What I did

`AutoCopy(line_end_p=q)`: with probability q the last word of a line gets one more change:
half the time a glyph appended (y d g s m o r l, weighted as in exp. 20), otherwise an -m/-g
ending or an ordinary substitution. Boundary habit on. q from 0 to 0.8, four seeds each.

## Result

| q | distance | singletons at line end | line_last_jsd | hapax |
|---|---|---|---|---|
| VMS B | (1.23) | 0.24 | 0.065 | 0.68 |
| 0 | 2.39 | 0.11 | 0.028 | 0.55 |
| 0.4 | 2.06 | 0.22 | 0.048 | 0.57 |
| 0.6 | 1.89 | 0.27 | 0.082 | 0.59 |
| 0.8 | 1.86 | 0.33 | 0.095 | 0.60 |

- Two out of three. At q ≈ 0.5 the line-final singleton rate and `line_last_jsd` both land on
  the VMS values, and the distance drops from 2.39 to about 1.9, the best of any model so
  far (Currier B itself sits at 1.23 from the whole-manuscript profile).
- **The hapax ratio barely moves** (0.55 → 0.59), even though the model now has the right
  share of singleton *tokens* in every line position. I was wrong about where the gap is.
- The frequency spectrum shows where it really is:

| first 10 000 words | types ×1 | types ×2-20 | types ×21+ | text covered by the ×21+ types |
|---|---|---|---|---|
| VMS Currier B | 1575 | 640 | 87 | 54% |
| model, q = 0.5 | 1681 | 1103 | 58 | 30% |

  The model has enough singletons. It has far too many words of middling frequency and too
  weak a core: in the VMS 87 words make up more than half the text, in the model 58 words
  make up less than a third.

## So what

The model's singletons were never the problem; its middle is. A pure copy-and-change process
spreads itself over a cloud of variants. The VMS keeps coming back to the same ~90 words
(daiin, chedy, qokeedy, ol, ...) and treats everything else as a one-off variation on them.
That points at something the Timm & Schinner procedure doesn't have: a stock of preferred
forms that changes get pulled back to. Whether that stock is a scribe's habit or a
vocabulary is the open question, and probably the most important one we've reached.

Leaving `line_end_p` off by default; 0.5 is the fitted value.
