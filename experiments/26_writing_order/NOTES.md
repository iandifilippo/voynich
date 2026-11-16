# 26 — Leaf by leaf, or sheet by sheet?

## What is claimed

Layfield & Davis (*Digital Medievalist*, 2026) argue that many of the manuscript's bifolia
were made as separate units ("singulions") and only later nested into the quires we see.
Their evidence: conjoint pages are more alike than facing pages in most quires (LSA on whole
pages), drawings that run from one page onto its conjoint (78v/81r, 76v/83r, 33v/40r,
10v/15r, 58v/65r), and one scribe per bifolium in 50 of 52 cases.

## What I think

Whole-page similarity says two pages are alike, not which was written after which. Exp. 25
gave me something that does: the end of a page carries over into the start of whatever was
written next. A sheet written as a unit goes leaf 1 recto, leaf 1 verso, leaf 2 recto, leaf
2 verso (or, laid flat, the two inner pages side by side). Either way the verso of the first
leaf is followed by the recto of its conjoint leaf, not by the next folio in the book.
Wherever those two candidates are different pages, the carry-over can choose.

## What I did

For every sheet where the next folio and the conjoint leaf are different pages written by
the same scribe in the same section: last 5 lines of the first leaf's verso against the
first 5 lines of each candidate, and against all other rectos of the block as a baseline.
19 sheets qualify: 11 by scribe 1 (herbal A), 8 by scribes 2 and 3 (herbal B, balneological,
stars).

## Result

| | sheets | next folio in the book | conjoint leaf | any other recto | wins: book / conjoint / tie |
|---|---|---|---|---|---|
| scribe 1 (Currier A) | 11 | 1.56 | 1.28 | 1.21 | 9 / 2 / 0 |
| scribes 2 and 3 (Currier B) | 8 | 1.21 | **1.64** | 1.26 | 1 / 5 / 2 |

- **The two groups go opposite ways** (Fisher exact on wins, p = 0.035).
- **Scribes 2 and 3: the text continues onto the conjoint leaf.** The next folio in the book is
  no better than a random recto (1.21 vs 1.26); the conjoint leaf is clearly better
  (difference 0.43, interval 0.12-0.73).
- The sheets where the conjoint leaf wins include three of Layfield & Davis's drawing
  continuities: f76v→f83r (29 shared word types against 20 for the next folio), f78v→f81r
  (16 against 11) and f33v→f40r (20 against 13). The text agrees with the drawings.
- **Scribe 1: the text continues onto the next folio in the book** in 9 of 11 sheets,
  including f10v→f11r (21) over f10v→f15r (15), one of their pairs. The pooled difference
  isn't significant by itself (interval −0.61 to +0.93), so this half is a lean, not a result.
- One scribe-1 sheet goes strongly the other way: f19v shares nothing with f20r and 20
  word types with f22r.

## How this fits exp. 25

In the balneological quire the carry-over from a recto to its own verso was missing (0.68).
That is odd if the scribe wrote a leaf front then back, and expected if the sheet lay flat
and was written a side at a time: the two inner pages are then consecutive (leaf 1 verso,
leaf 2 recto, which is where the drawings cross), and a recto is never followed by its own
verso. Small numbers, but the pieces point the same way.

## Follow-up

Exp. 29 runs every transition within a sheet. The scribes 2-3 result holds at every window
size and passes a direction test; the scribe 1 lean towards book order does not survive.

## So what

- For the Currier B scribes this is independent support for sheet-at-a-time writing, from
  the order of the text and not from page similarity or drawings.
- For scribe 1 the herbal A quires look as if they were written in the order they are bound.
  If that holds, "singulions" is a habit of some scribes, not of the whole book.
- Eight and eleven sheets. The split by scribe was made after seeing the pooled result, even
  if scribe is the obvious thing to split by. The properly powered version needs the pages I
  left out (mixed-scribe quires, foldouts) and a better end-of-page measure.
