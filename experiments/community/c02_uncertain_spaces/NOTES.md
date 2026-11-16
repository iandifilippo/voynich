# c02 — Are uncertain spaces real spaces?

## What was claimed

Rozanova & Temerev (arXiv:2608.17096, Aug 2026): in ZL, the spaces transcribers marked as
uncertain (`,`) behave like breaks *inside* a word, not like word separators.

## What I thought

That's a strong claim with a practical consequence: if true, everyone who treats `,` as a
space (most of us, including my own parser) is cutting words in half a few thousand times.
But "behaves like" can mean many things. My guess was that it's a mixture: some commas are
transcribers hedging on genuinely tight spaces, some are glyph spacing inside a word.

Hypothesis: if commas are a mix, any measure of "is this a word boundary" should put them
between certain spaces and real word-internal cuts, not on one side.

## What I did

Two measures, text only:

1. **Join test.** Glue the pieces on both sides of the separator and check whether the
   result is a word that appears 2+ times elsewhere as a single token. Compare with `.` and
   with random cuts made inside real words (the "definitely one word" reference).
2. **Edge MI.** Mutual information between the glyph before and the glyph after the
   separator.

Then, assuming commas are a mix of real spaces and internal cuts, solve for the share of
internal cuts that reproduces the observed join rate.

## Result

| boundary | joins into a known word | edge MI (bits) |
|---|---|---|
| certain `.` | 3.7% | 0.16 |
| uncertain `,` | 33.7% | 0.55 |
| random cut inside a word | 82.8% | 1.70 |

Commas land in between on both measures. The join rate implies roughly **38%** of uncertain
spaces are word-internal and the rest behave like normal spaces. Both sides of a comma are
usually words in their own right (84%), so most commas aren't splitting nonsense.

I also tried to see this in the scans (experiment 12): at the resolution of the PDF the gap
measurements are too noisy to separate the two, so no help there yet.

## So what

Rozanova & Temerev are right for a large minority of cases, not for all of them. Practical
upshot for the parser: a per-comma decision (join if the glued form is a known word, keep
the space otherwise) is better than either blanket rule. I'll add that as an option and
rerun the benchmark with it.
