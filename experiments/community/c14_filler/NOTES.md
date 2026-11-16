# c14 — Real text hidden in filler (Mark Knowles, voynich.ninja thread 4057)

## What was claimed

That the manuscript is partly meaningful text and partly meaningless padding, maybe a fifth
real and the rest filler, which would explain why statistics on the whole thing look odd.
His suggestion: throw away the repetitive text and analyse what's left, since the real part
should be the least repetitive.

## What I think

It's a fair middle position and it makes a testable prediction, because exp. 34 found one
measure that separates language from the manuscript sharply: whether memorising whole words
helps predict held-out words. In every real text it does; in the manuscript it doesn't. If a
quarter of the text is language, that quarter should have a vocabulary.

## What I did

Every line scored by the share of its words that appear, exactly or with one glyph changed, in
the five lines above it on the same page. Kept the least repetitive quarter (4% repeated words
in A, 17% in B, against 71-77% in the most repetitive quarter). Same 2400 words per sample,
mean of five splits. The same selection applied to Latin and Italian cut into pages of
manuscript-sized lines, to check the selection itself doesn't erase a real vocabulary.

## Result (bits saved per held-out word by remembering whole words)

| | least repetitive quarter | most repetitive quarter | all lines |
|---|---|---|---|
| Currier A | −0.47 | −0.37 | −0.43 |
| Currier B | −0.48 | −0.31 | −0.45 |
| Latin | +1.41 | +1.40 | +1.50 |
| Italian | +1.41 | +1.10 | +1.16 |

## So what

The least repetitive quarter is no more language-like than the rest; if anything slightly
less. The selection leaves Latin's and Italian's vocabularies untouched, so it's not the
method. If there's meaningful text in the manuscript, it isn't the non-repetitive part, and it
doesn't carry a vocabulary in the ordinary sense anywhere. A meaningful fifth would have to be
somewhere this measure can't see (inside a cipher with no word-level vocabulary, exp. 35), not
hidden among filler.
