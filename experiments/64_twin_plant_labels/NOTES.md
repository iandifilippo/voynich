# 64 — Twin plants: is the pharma label written in the herbal page?

## Why

Everything so far asks what kind of system the text is. This one asks for a reading at a place where
one would show even without knowing the language. Some plants in the pharma section are redrawn from
a herbal page (same root, same leaves, same berries). The small word next to the pharma plant is the
best candidate in the book for a plant name. If it is one, the herbal page about the same plant should
contain it, or something close to it, more often than other herbal pages do.

The twelve pairs come from the list in d2kx/voynich-research (attack 169), which credits each match
to Petersen, Stolfi, Zandbergen, Landini and others. I take the folio pairs as given and use only
their labels as ZL has them. I didn't check the matches by eye. Pair 07 has no label, so 11 pairs and
41 labels are left (some pharma plants are twins of two herbal pages).

## How

For each label, every herbal page gets three scores: the label occurs on it (exact), some word is at
most one sign away (near), and the best similarity of any word (1 − sign edit distance / length). The
twin is ranked only against herbal pages in the same Currier language and within 30% of its word
count, since a longer page wins just by having more words. 0 means the twin is the best page and 0.5
is chance. The null draws a random page from the same pool for every label. As a looser version I use
all 111 labels on the pharma sheet, and I also try both versions with an initial o-/y- removed.

Power check: plant the label once at a random spot in its twin page, or plant a variant one sign off.

## Result

| | n | exact | near | similarity |
|---|---|---|---|---|
| labels by the twin plant | 41 | 0 hits, 0.50 | 3 hits, 0.50 (p .50) | 0.44 (p .07) |
| same, o-/y- removed | 41 | 0 hits | 4 hits, 0.50 | 0.47 (p .25) |
| all labels on the pharma sheet | 111 | 2 hits, 0.50 | 0.49 (p .34) | 0.47 (p .15) |
| same, o-/y- removed | 111 | 4 hits | 0.48 (p .08) | 0.46 (p .06) |
| power: label planted once | 41 | 0.003 (p .002) | 0.04 (p .002) | 0.003 (p .002) |
| power: one-sign variant planted once | 41 | – | 0.04 (p .002) | 0.04 (p .002) |

Twin percentile, 0.5 = chance. The full table for each label is in `results/twins.md`.

## So what

None of the 41 labels appears in its twin herbal page. Taken together they aren't nearer to it than
to a herbal page of the same length chosen at random. The test isn't too weak: a single mention of
the label, or of a one-sign variant, anywhere in the twin page is found every time (p .002). So if the
label names the plant, the herbal text never writes that name, not even in a form one sign apart.
The similarity score leans a little toward the twin (0.44, p .07), but that is one of twelve rows,
it fades when the o- is removed, and the scribe of a page and of its copy often share spelling
habits. I wouldn't read anything into it.

That leaves three options: the drawings aren't twins (the pairs are matches by eye), the labels
aren't the names used in the text, or the text doesn't name its plant at all. The last fits what
exps. 34 and 40 found: the words of a page belong to its sheet's setting and don't make a lexicon.
