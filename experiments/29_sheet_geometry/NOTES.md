# 29 — Which page follows which, sheet by sheet

## Why

Exp. 26 found that for scribes 2 and 3 the end of a verso carries over onto the conjoint
leaf, not onto the next folio. That was one comparison on eight sheets, split by scribe after
the fact. Before leaning on it I wanted every transition a sheet allows, more than one
window size, and a prediction that could fail.

## The predictions

Leaf *a* is the earlier leaf of a sheet in the book, leaf *b* the later one.

| transition | quire nested first (book order) | sheet folded and written alone | sheet laid flat, a side at a time |
|---|---|---|---|
| recto → own verso | yes | yes | no |
| a verso → b recto (conjoint) | no | yes | yes |
| b verso → a recto (outside of sheet) | no | no | yes |
| a verso → next folio | yes | no | no |
| anything on a → anything on b, against b → a | no difference | a → b higher | mixed |

The last row is the new one. If a sheet is written as a unit, leaf *a* first, then the end of
any page on *a* is closer in time to the start of any page on *b* than the other way round.
If the two leaves were written many folios apart, direction can't matter.

## What I did

Same carry-over measure as exp. 25 (shared word types, last K lines against first K lines,
over the block's expectation), for every transition, in single-scribe blocks. Sheets in the
middle of a quire are kept apart (there the conjoint leaf *is* the next folio). K = 4, 5, 6,
8; with and without the 60 commonest words; intervals by resampling sheets.

## Result

**Scribes 2 and 3 (K = 5, all words)**

| transition | sheets | lift | interval |
|---|---|---|---|
| a verso → b recto (conjoint) | 14 | **1.50** | 1.20-1.80 |
| a verso → next folio | 9 | 1.28 | 0.96-1.55 |
| recto → own verso | 16 | 1.11 | 0.88-1.36 |
| b verso → a recto | 14 | 0.74 | 0.56-0.90 |
| unrelated verso → recto | 16 | 1.05 | 0.92-1.17 |

- **Conjoint beats next folio at every window size**: difference 0.79, 0.43, 0.42, 0.28 for
  K = 4, 5, 6, 8 (all p ≤ 0.004), and with common words removed at K = 5 (p = 0.005). It
  fades by K = 8 with common words removed, where there's little left to count.
- **Direction, the prediction that could have failed:**

| block | sheets | leaf a → leaf b | leaf b → leaf a | difference |
|---|---|---|---|---|
| stars B (scribe 3) | 4 | 1.48 | 0.77 | 0.71 (0.26 to 1.24), 4 of 4 sheets |
| herbal B (scribe 2) | 5 | 1.41 | 1.08 | 0.33 (−0.03 to 0.68), 4 of 5 |
| herbal A (scribe 1) | 15 | 1.41 | 1.29 | 0.12 (−0.11 to 0.38), 7 of 15 |

- In the stars quire the whole pattern is the one a singly folded sheet gives: recto → own
  verso 2.04, a verso → b recto 1.58, b recto → own verso 1.09, and the end of the last page
  against the start of the first is the lowest of all (0.43).
- The balneological sheets (4, one with a page lacking text) show the conjoint carry-over
  (1.39) and no recto → verso carry-over (1.00, 0.72), and are too few to order.
- **Scribe 1's herbal sheets show no direction at all.** All four pages of a sheet resemble
  each other (1.27-1.61 in every cell, against 1.13 for unrelated pages) and so does the
  next folio (1.53). That is Layfield & Davis's "conjoint pages are alike", seen again, but
  with nothing in it about order. The lean towards book order in exp. 26 doesn't hold up as a
  result.

## So what

- For scribes 2 and 3, and most clearly for the stars quire, the text was written a sheet at a
  time, first leaf then second. That is Layfield & Davis's singulion proposal, supported here
  by the direction of the text and not by resemblance, drawings or hands. I haven't seen it
  tested this way.
- It also means the stars quire as bound doesn't give the order of writing: the two halves of
  each sheet are a dozen folios apart. Any analysis that treats f103-f116 as one running
  text (mine included, in exp. 22 and 25) is reading it in the wrong order.
- For scribe 1 the question stays open. The sheet matters (its pages are alike) but I can't
  tell how he moved through it.

## Caveats

Four to sixteen sheets per cell. Pages in mixed-scribe quires, foldouts and missing leaves
are left out. The split by scribe came from exp. 26, so only the direction test and the
other window sizes count as fresh evidence. A drawing-free check would be to redo this on
Takahashi's transliteration; the loci are the same, so I expect the same answer.
