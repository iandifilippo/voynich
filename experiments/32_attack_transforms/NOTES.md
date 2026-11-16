# 32 — Attack 2: letters, but not written the plain way

## The hypotheses

Three ideas that keep "a sign is a letter" and change the text instead, all of them with a
long history in Voynich proposals:

- **no vowels**: the text is written consonants only, as in Hebrew or Arabic, or abbreviated;
- **letters sorted**: the letters of each word are put into a fixed order, which would explain
  why glyphs sit in such rigid positions inside words;
- **backwards**: each word is written back to front.

Plus Hebrew, Arabic and Persian as written (consonantal anyway).

## What I did

The solver needs nothing new: the language model is trained on text that has had the same
thing done to it. For every variant, a power check first (held-out text of that kind behind
100 homophones), then the manuscript (Currier A and B) and the copying model as control,
with glyphs, glyph groups and 60 merged units as symbols.

## Result

**Power**: every variant is readable when it's really there. Letters right: backwards
99.8-100%, Hebrew / Arabic / Persian 100%, sorted 95-99%, no vowels 92-100%.

**The manuscript**:

| target | best gap, manuscript | best gap, copying model | words: manuscript / control / real |
|---|---|---|---|
| Latin, letters sorted | −0.29 | −0.27 | 3% / 8% / 30% |
| Italian, letters sorted | −0.27 | −0.25 | 7% / 6% / 61% |
| Latin, backwards | −0.12 | −0.07 | 7% / 0.4% / 26% |
| Italian, backwards | −0.19 | −0.12 | 4% / 10% / 59% |
| Hebrew | −0.16 | −0.16 | 10% / 16% / 72% |
| Arabic | −0.15 | −0.08 | 19% / 22% / 72% |
| Persian | −0.17 | −0.11 | 19% / 24% / 59% |
| **Latin, no vowels** | **+0.09** | **+0.12** | **34% / 32% / 32%** |
| **Italian, no vowels** | **+0.01** | **+0.05** | **33% / 35% / 46%** |
| **German, no vowels** | **−0.03** | **+0.02** | **29% / 26% / 48%** |

- Sorted, backwards, Hebrew, Arabic, Persian: nothing. The manuscript is 0.12-0.38 short of
  real text and the control does as well or better.
- **"No vowels" passes every bar, and so does the control.** The manuscript decodes to
  consonant strings that score *above* real vowelless Latin and put a third of their letters
  into real vowelless Latin words, the same rate as real text. The copying model, which
  contains nothing, does exactly the same or better.

## What that means

Text without vowels has so little left in it that a key can turn anything into it. Strip the
vowels and *dmns*, *trr*, *prt* are all "words"; with twenty-odd consonants and short words,
most short strings are. So:

- A consonant-only reading of the manuscript **cannot be tested** by how language-like or
  how full of words the result is. Every such reading will look good. This is, I think, why
  abjad-style solutions keep being announced with long lists of matching words.
- It isn't evidence against a vowelless plaintext either. It's a hypothesis this kind of
  attack can't touch; it would need something outside the text (a crib, a label that has to
  be a particular word).

The control did the work here. Without it I'd be looking at "34% real Latin words, score
above real text" for Currier B.
