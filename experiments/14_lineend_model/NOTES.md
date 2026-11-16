# 14 — Is there a line-end transformation?

## Why

Experiment 10 found that line starts in Currier B behave like a rewrite: words that go missing
from line starts reappear there with s, d or t in front. Line ends have their own oddity: words
ending in -m are about 17 times commoner in the last slot (627 line-final -m tokens). The obvious
guess is the mirror image: some ordinary ending gets rewritten as -m when a word lands at the end
of a line.

## Hypothesis

For some ending e (-in, -iin, -r, -y...), word types x ending in e should be rarer at line end
than expected, and x with e replaced by -m should be commoner, in matching amounts across word
types. If no single ending works, maybe -m stands for several endings at once, which would show
up when the whole family of endings for a stem is pooled.

## What I did

Same machinery as experiment 10: for every candidate rewrite "-e → -m" (and "-e → -g", and a
control "-e → -l"), correlate the line-end deficit of x with the line-end surplus of its rewritten
partner, with a permutation null. 97 tests, Bonferroni threshold p < 0.0005. Then a stem-level
version: for every stem that ever takes -m, pool the line-end deficit of stem+{r, l, s, n, in, iin,
y, dy} and correlate it with the surplus of stem+m. Checked on ZL (all, A, B) and on Takahashi.

## Result

No rewrite into -m or -g reaches significance in any set. Several are strongly *negative*
(-l → -m r = −0.50, -n → -m r = −0.66): both partners are favoured at line end, so nothing is
being taken from one and given to the other. The stem-level test is null too (r between −0.29 and
−0.02, p 0.60–0.98).

What does happen at line end:

- words are shorter (4.73 glyphs vs 4.96 inside the line and 5.43 at the start)
- -m forms are hugely over-represented: am ×23, dam ×12, otam ×12 against expectation
- their siblings mostly aren't (al ×1.0, ar ×0.55, aiin ×0.61), except the d- family (dal ×2.0,
  dar ×1.4, daiin ×1.6)

## So what

Line starts and line ends are different mechanisms. The start behaves like something added to an
ordinary word. The end doesn't rewrite anything I can find; it favours short words and a set of
-m forms that barely exist elsewhere. That fits a scribe filling the end of the line (abbreviation,
a special final form, padding) better than a systematic transformation. It also explains why the
autokey + line-start cipher in experiment 13 still fails on line_last: there is no rule to borrow.
