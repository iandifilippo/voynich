# 53 — Recurring word pairs

## What I think

Exp. 52: the residual doesn't transfer as a pattern between kinds of word. Something can be real
in-sample and still not be a class pattern: a set of exact word pairs that recur, like phrases.

## What I did

Share of adjacent word pairs in one half (alternate sheets) that occurred, as the same two words in
the same order, in the other half; minus the same after shuffling words among words at the same line
position inside each sheet (keeps frequencies, sheet setting and line-edge habits). And the same for
the reversed pair: in a language a common pair's reverse is rarer than chance, because word order is
fixed.

## Result

| | pairs seen before | if shuffled | excess (relative) | reversed pair: excess |
|---|---|---|---|---|
| Currier B | 0.178 | 0.132 | 0.045 (+34%) | −0.002 |
| Currier A | 0.105 | 0.089 | 0.016 (+18%) | −0.001 |
| habits generator (B) | 0.092 | 0.076 | 0.016 (+21%) | 0.001 |
| Naibbe cipher of Latin | 0.123 | 0.101 | 0.023 (+22%) | 0.003 |
| Latin words | 0.179 | 0.113 | 0.066 (+59%) | **−0.055** |
| Italian words | 0.317 | 0.180 | 0.137 (+76%) | **−0.086** |

Most over-represented pairs in B: *or aiin* (44 vs 5.6 expected), *s aiin* (35 vs 1.8), *ar aiin*,
*r aiin*, *o l*, *ar al*, *r ain*, *or ain* (words cut at a doubtful space, exp. 46); then *ol shedy*,
*shey qokain*, *shedy qokedy*, *chedy qokeey*, *shedy qokaiin*, *ol chedy*, *qol chedy*, *qokeedy
qokeedy*: a *ch-/sh-* word ending in *-y* followed by a *qo-* word, and *ol* followed by a *ch-/sh-*
word.

## So what

1. B repeats word pairs more than any content-free control (+34% against +21-22%), but less than
   Latin and Italian (+59-76%). A doesn't, beyond the controls.
2. A good part of B's excess is false word breaks in the transliteration (*or aiin* = *oraiin*).
3. The rest is a pattern of alternation: *ch-/sh-…-y* then *qo-…*, *ol* then *ch-/sh-*. It works
   like a rhythm in how words are strung together.
4. The telling difference is order. In Latin and Italian the reverse of a common pair is clearly
   rarer than chance (−0.055, −0.086): word order is grammatical. In the manuscript, reversed
   pairs occur at exactly the chance rate. Its recurring pairs don't come with a word order.

That's where the residual of exps. 48-51 ends up: false spaces, a ch/sh → qo rhythm, and repeated
pairs without word order. None of it looks like syntax. It does look like a writer with a few more
habits than my generator has.
