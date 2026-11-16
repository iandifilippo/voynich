# 27 — Would the page test see a subject if there was one?

## Why

In exp. 25 I concluded that a herbal page has no vocabulary of its own. I hadn't checked that
my measurement could find a subject in a text that certainly has one. That's the control
this experiment adds, and it changed the conclusion.

## What I did

- Control text: Pliny, *Natural History* book 16 (trees), 44 chapters, in the edition's own
  lines of about nine words. Latin, about plants, one topic per chapter. Also the same lines
  dealt at random into the chapters (no subject left), the same book through the Naibbe
  cipher with the chapters kept, and the copying model cut into 13-line pages.
- A cleaner statistic for "does a page have its own vocabulary": take pairs of lines 3-12
  lines apart and compare how many word types they share when both are on the same page
  against when a page break lies between them, at matched distances. Null: the same text
  with the page breaks slid along by a random amount (400 times). This keeps any
  short-range carry-over and asks only whether the *real* breaks matter.
- All words, and with each text's 60 most widespread words set aside.

## Result

Same page / across a break, at the same distance:

| | all words | without the 60 commonest |
|---|---|---|
| Pliny 16, chapters | 1.05 (p = 0.25) | **1.39 (p = 0.01)** |
| Pliny, lines dealt at random | 1.02 | 1.07 (p = 0.33) |
| Naibbe cipher of Pliny 16 | 1.01 | 0.97 (p = 0.64) |
| copying model | 1.15 (p = 0.01) | 1.93 (p = 0.007) |
| VMS herbal A (hand 1) | 0.92 (p = 0.91) | 1.23 (p = 0.09) |
| VMS balneological B (hand 2) | **1.36 (p = 0.005)** | **1.48 (p = 0.015)** |
| VMS stars B (hand 3) | **1.15 (p = 0.017)** | **1.39 (p = 0.007)** |

- **The test works, but only on the less common words.** Pliny's chapters show their
  subject at 1.39 once the common words are out, and nothing with them in. My exp. 25
  statement was made on the all-words version, which can't see a subject. Withdrawn there.
- **The balneological and stars pages do have vocabulary of their own**, as strongly as
  Pliny's chapters have. The herbal A pages: nothing in the common words, a weak and not
  significant sign in the rarer ones (1.23, p = 0.09; herbal pages are short, about 12
  lines, so this test has little to work with there).
- **A Naibbe-style cipher wipes the subject out.** The same book, same chapters, enciphered:
  0.97. Each plaintext word can come out as many different cipher words, so a chapter about
  oaks no longer repeats anything. The VMS's B sections don't look like that.
- **The copying model also gives pages their own vocabulary** (1.93), with no subject at
  all: it copies from the page it's on. So page vocabulary in the VMS doesn't prove a
  subject. It rules out one thing (the homophonic cipher) and is consistent with two
  (a subject, or copying within the page).

## Agreement with Schwartz (2026)

He measures subject dependence differently (how much word choice tracks the illustrated
section beyond scribe and page order) and finds it faint but present in the astronomical
(z = 2.6) and balneological (z = 2.9) sections and absent in the herbal (z = 1.2). Same
pattern as the table above, by a different route: B sections yes, herbal no.

## So what

Where things stand after 25 and 27, stated carefully:

- The common words are a habit that follows the order of writing and ignores page and plant.
- In the B sections the less common words belong to their page. A cipher of the Naibbe kind
  can't do that. A text with subjects can, and so can a writer who copies from the page in
  front of him.
- To tell those two apart I need a prediction they disagree on. One candidate: a subject
  can come back many pages later (two chapters on similar trees), page-bound copying can't.
  Another: labels next to drawings. Both are for the next round.

And a note to self: the control should have come before the claim, not after.
