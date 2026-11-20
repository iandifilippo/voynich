# 45 — Do labels name what their page's text talks about?

## What I think

Drawings in the pharmaceutical, bathing and zodiac pages carry one-word labels. If the writing
means something, a label is a name, and the text on the same page should mention it more than
other pages' text does. This needs no knowledge of the language, and it is the most direct test
of meaning I can think of that the manuscript allows.

## What I did

Every label word of 4+ letters looked up, exactly and with one glyph different, in the running
text (paragraphs, rings, circles) of its own page, of the other page(s) of the same sheet, and
of the rest of the section, per 1000 words of text. A permutation test moves labels to random
pages of their section. Labels start with *o-* three times as often as text words and almost
never with *q-*, so I also tried reading label *o-* as text *qo-*, and dropping the *o-*.

## Result

| | own page | rest of section | p (labels moved at random) |
|---|---|---|---|
| all labels (P, B, Z), exact hits | 118 | 101 expected | 0.10 |
| *o-* labels as written | 57 | 45 expected | 0.09 |
| *o-* labels read as *qo-* | 76 | 52 expected | 0.04 |

Per section, exact hits per 1000 text words, own page / other sheets: pharmaceutical 0.61 /
0.62, bathing 1.82 / 1.46, zodiac 1.40 / 1.17.

How labels differ from text words: 60% start with *o-* (text 22%), 1% with *q-* (text 17%), 9%
with *ch/sh* (29%); only 47% (pharmaceutical) to 70% (bathing) of label words occur anywhere in
the running text.

## So what

The pharmaceutical labels, where a label sits next to a jar or a root on a page full of text,
are found on their own page exactly as often as anywhere else. Over the three sections there's
at most a faint excess (p 0.04-0.10 on three overlapping tests, which I don't count as a result).
Labels behave like a vocabulary of their own, built differently (*o-* first, never *q-*), and
the text doesn't talk about what they label any more than it talks about anything else.

The *o-* → *qo-* reading gives the largest excess and is worth keeping in mind: if labels are
text words in another form (a case, a prefix), that's the form. But nothing here shows it.

## Caveats

- Small counts (20 own-page hits in the pharmaceutical section).
- A page's setting (exp. 40) can make own-page matches a little more likely without meaning
  anything, which would push the excess up, not down; there's little to push.
