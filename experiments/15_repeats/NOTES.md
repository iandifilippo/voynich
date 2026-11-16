# 15 — Why do words repeat next to each other?

## Why

Every cipher variant so far fails on `repeat_rate`: the VMS has plenty of immediate repeats
(qokedy qokedy, chol chol) and the ciphers have almost none. Before trying to build a mechanism
for it, I wanted to know what kind of thing it is. "Words repeat next to each other" could mean
the writer is repeating a word on purpose, or it could be a side effect of something else.

## Hypothesis

If repeats are about adjacency, shuffling words *within* each line should destroy them. If they
come from lines reusing the same vocabulary, shuffling within the line won't change the rate;
only shuffling across the whole text will.

## What I did

Rates of exact repeats and near-repeats (one glyph substituted, added or removed) per 1000
adjacent pairs. Two baselines: words shuffled within their line (300 times) and across the whole
text. Same for four natural texts and for Naibbe with and without the autokey. Then position in
the line, across line breaks, which words repeat, and what changes in near-repeats.

## Result

| text | exact | shuffled in line | shuffled everywhere | near | shuffled in line | shuffled everywhere |
|---|---|---|---|---|---|---|
| VMS | 9.4 | 9.3 | 3.4 | 36.0 | 30.8 | 16.9 |
| Latin (Aix) | 0.0 | 4.4 | 6.0 | 1.6 | 3.1 | 3.9 |
| Italian (Rettorica) | 0.2 | 8.1 | 7.0 | 7.1 | 16.9 | 19.8 |
| Naibbe | 1.3 | 3.1 | 3.9 | 11.4 | 13.0 | 14.2 |

- **Exact repeats are fully explained by line composition** (VMS 9.37 vs 9.25 in-line shuffles,
  p = 0.42; A p = 0.34, B p = 0.55). Lines reuse words; once two copies are in a line, they end up
  adjacent at the rate you'd expect.
- **Near-repeats are not.** 36.0 vs 30.8 (p < 0.003 in all, A and B): a word is followed by a
  slightly altered copy of itself more often than line composition allows. Commonest pairs:
  o l, ar al, qokedy qokeedy, or ol, okeey qokeey, daiin dain, chor chol.
- Real languages avoid immediate repeats (Latin 0 vs 4-6 expected). The VMS shows no avoidance
  at all. Naibbe inherits the avoidance from its plaintext.
- Repeats avoid the first pair in a line (3.4 per 1000 vs 11.1 in the middle) and almost never
  bridge a line break (6 vs 11.8 expected), consistent with line starts being rewritten (exp. 10).

## So what

"Repeat rate" in the benchmark is really two things. Exact repeats are line cohesion in disguise:
the thing to explain is why lines share vocabulary. Near-repeats are a genuine local effect of
copy-and-modify from the previous word, which is what Timm & Schinner's self-citation model
predicts and what no cipher does. Next: port their generator and see whether it gets the near-repeat
excess without overdoing everything else.
