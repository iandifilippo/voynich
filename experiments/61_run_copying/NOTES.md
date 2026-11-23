# 61 — Words built fresh, runs copied

## What I think

Exp. 60 split the job between two models that each fail: the assembled-words generator gets the words
and misses the link between neighbours (0.04-0.07 bits beyond the boundary, B 0.23); Timm and Schinner's
copying model gets the link (0.21) and misses the words. A hybrid: every word is built by the rule, but
now and then the writer, having just written a word that already stands on the sheet, writes again what
followed it there, a short run copied, sometimes with a sign changed (`follow_p` in
`voynich/assemble.py`).

## What I did

follow_p from 0 to 0.45, chosen on the even sheets (against the even sheets' own text), everything scored
on the odd sheets as in exp. 60.

While writing this I found a bug in the generator used in exps. 50-60: its echo of recent words was reset
at every line, because `fill_sheet` filled one line at a time. It now keeps the sheet's history. Exp. 50's
fitted settings came from the line-level echo; the effect on its conclusions is small (the echo is 11% of
words and mostly reaches back within a line anyway), but the numbers here use the corrected generator.

## Result

Beyond-the-boundary link (bits) as follow_p grows, on the even sheets: 0.00, 0.11 (0.05), 0.19 (0.10), 0.37
(0.20), 0.52 (0.30). B: 0.23. A run copied every 10-15 words is enough to make the link that exps. 48-51
couldn't produce.

Scored on the odd sheets (follow_p 0.05, the first of two tied choices on the even sheets):

| | B | assembled, no run copying | + run copying | copying model |
|---|---|---|---|---|
| beyond the boundary | 0.23 | 0.04 | 0.05 | 0.20 |
| recurring pairs excess (across sheets) | 0.053 | 0.020 | 0.015 | 0.028 |
| class sequence | 0.063 | 0.012 | 0.011 | 0.002 |
| within 0.8-1.25× of B (of 11) | – | 6 | 7 | 6 |

## So what

1. The residual of exps. 48-51 can be made by copying short runs within a sheet, at about the rate where
   copying shows up in nothing else (one run in 10-15 words). That's Timm and Schinner's self-citation,
   at the level of word pairs rather than words, on top of words built by the rule. The residual doesn't
   need a message.
2. Two things still aren't made by anything: pairs that recur *across* sheets (0.053, runs copied within a
   sheet give less, not more) and the class-level sequence (0.063). Both are the ch/sh-…-y → qo- rhythm of
   exp. 53, a habit of alternation that holds across the whole of B. A generator with that rhythm written
   in would be fitting it, not explaining it.
3. On the held-out scorecard the hybrid is the best model so far (7 of 11 within 0.8-1.25×), and still
   not good: its words are a little too varied (281 vs 249 distinct per 1000) and q- too rare.
