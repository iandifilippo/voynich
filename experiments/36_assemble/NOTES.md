# 36 — Assembled words instead of copied words

## What I think

Exp. 34 ended with a suspicion about my own copying model (exps. 17-22): copying whole words
with small edits builds a vocabulary, and the manuscript doesn't seem to have one. What the
numbers pointed to instead was a word built fresh every time by a rule that only looks a
couple of signs back, with some influence from what was just written.

So I wrote that as a generator (`voynich/assemble.py`): a sign chain that looks back k signs,
with its own tables for paragraph-first, line-first and line-last words, the first sign of a
word drawn given the last sign of the word before. Nothing is copied.

## What I did

Fitted on half of Currier B (every other page), and asked to fill the other half: same pages,
same lines, same number of words per line, same paragraph starts. Everything is compared with
the held-out half. Two other models fill the same shape:

- **lexicon**: words drawn from the training half's own word frequencies. A pure vocabulary
  with no rule, the extreme opposite.
- **copying model**: exp. 22's best, which isn't fitted to text at all.

The plain assembler gets the vocabulary right but makes too few repeats next to each other and
too little page locality. So I gave it two more knobs, fitted on the training half only
(`tune.py`): with probability *p* a word inside a line repeats one of the last few words on
the page, and with probability *e* it repeats one with a single sign redrawn. The fit chose
p = 0.01, e = 0.10, last 5 words.

## Result (held-out Currier B; 3 seeds)

| | held-out VMS | assemble 2 | + recall | lexicon | copying |
|---|---|---|---|---|---|
| distinct words per 1000 | 248 | 262 | 291 | 190 | 214 |
| hapax share of types | 0.67 | 0.70 | 0.71 | 0.40 | 0.62 |
| **tokens never seen in the training half** | **17%** | **18%** | 21% | 0% | 49% |
| lexicon gain (bits, exp. 34) | −0.25 | −0.36 | −0.37 | +0.39 | +0.02 |
| adjacent exact repeats / 1000 | 9.1 | 5.3 | 7.6 | 4.3 | 7.2 |
| adjacent near repeats / 1000 | 33 | 24 | 34 | 21 | 37 |
| words starting q- | 18% | 18% | 17% | 18% | 1% |
| paragraph-first word starts with a gallows | 88% | 84% | 83% | 8% | 94% |
| line-last word ends in -m | 19% | 16% | 17% | 2% | 9% |
| doubletons with both on one page | 7.4% | 3.3% | 10.5% | 2.9% | 23.6% |
| measures within 0.8-1.25× of held-out | – | 9 of 14 | **11 of 14** | 5 | 6 |

The line that matters most is the novelty one. One token in six in the held-out half is a word
that never occurs in the other half. A sign chain that looks two signs back produces new words
at exactly that rate (18%), without being told to. A vocabulary produces none, by definition.
The copying model produces three times too many: it invents a new variant at every turn and
then mostly forgets it.

Looking back one sign is too little (316 distinct words per 1000), three is too many (it starts
to memorise: 12% new). Two is right. The link to the previous word barely matters.

**Robustness**, same knobs, not refitted:

| | new tokens: VMS / assemble 2 | lexicon gain: VMS / assemble 2 | within range (+ recall) |
|---|---|---|---|
| Currier A (ZL) | 24% / 22% | −0.37 / −0.41 | 12 of 14 |
| Currier B (IT) | 19% / 18% | −0.26 / −0.36 | 11 of 14 |
| Currier B (GC) | 20% / 18% | −0.32 / −0.37 | 10 of 14 |

(GC uses its own alphabet, so the EVA-based edge measures don't apply there and the copying
model, which is written in EVA, can't be compared.)

## So what

1. A Voynich word behaves like a draw from a two-sign rule, not like an item from a stock of
   words. That reproduces the size of the vocabulary, the share of one-off words, the rate of
   new words in unseen text, the frequency of the top words, the edge habits and the missing
   lexicon, in both Currier languages and three transliterations, on text the model never saw.
2. On top of that rule there is a small, real short-range habit: about one word in ten echoes
   one of the last five, usually with one sign changed. That accounts for the near repeats and
   the page locality of rare words (c11).
3. This replaces copying as my best account of how the text was produced. Copying gets the
   repeats but not the words; the rule gets the words, and a little copying gets the repeats.
   It also explains why the copying model kept failing on q- (exp. 23): q- is a property of the
   rule, not of what was copied.
4. What it means for meaning: such a text could still carry information if the choices at each
   step were dictated by a plaintext (a verbose cipher that walks a table, like Naibbe). But
   it doesn't need to, and the c-series keys have nothing to stand on: a rule like this makes
   pronounceable, word-like strings from nothing.

## Caveats

- The rule is fitted to half the manuscript, so it has thousands of parameters. It isn't a
  15th-century procedure; it's a description of what any procedure would have to produce.
  Finding a procedure a scribe could actually run that matches it (a table, a volvelle with
  dependent rings, a habit) is the next question.
- The recall version overshoots distinct words (291 against 248) and page locality (10.5%
  against 7.4%). Edits make new words; the real echoes must be more conservative than "redraw
  any sign".
- Adjacent exact repeats are still short (7.6 against 9.1).
- The benchmark distance (exp. 23) isn't used to judge here: its reference is the whole
  manuscript, so even the held-out half of B scores 1.79 against it.
