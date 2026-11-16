# 12 — Reading lines and spaces off the scans

## Why

Everything else in this repo trusts the transliteration. Two things I keep wondering about
can only be checked on the parchment: whether the line structure in ZL matches what's on the
page (it should, but it's worth a number), and whether the spaces transcribers marked as
uncertain look different from the certain ones.

There's a lot of image work going on right now. Ryan Allen's "Trace the Voynich" has a model
that traced the whole manuscript pixel by pixel, with volunteers correcting it letter by letter;
the data isn't released yet. People on r/voynich are training OCR models. Kraken (kraken.re) is
the open engine built for historical scripts and could be trained on ZL-aligned crops. I didn't
want to start with a trained model; first, what can plain image processing say?

## What I did

Source: the page images embedded in Yale's PDF of MS 408. They're about 1100 x 1536 px, so a
text line is ~25 px tall and a glyph ~12 px. Quire 20 (f103r–f116r) is all text in a single
block, so it's the easiest place to start.

- Sauvola binarisation, small specks removed, skew corrected by maximising the row profile
  variance, text lines found as peaks of the row profile.
- To avoid tuning the detector on the same pages I evaluate it on, parameters were picked on
  every other page and the error reported on the pages it never saw.
- On pages where the line count matched ZL exactly, I paired lines in order and counted the
  wide gaps in each line, then fit `gaps = a·dots + b·commas + c`.

## Result

Lines: on the 11 held-out pages, mean error 3.2 lines, within ±1 line on 7. The big miss is
f112r (27 found, 45 in ZL): a damaged leaf with a cut edge and lines that bend into each other.
f104r is stored at half resolution in the PDF and was skipped.

Spaces: 187 lines on 4 pages, 1607 certain and 145 uncertain spaces. Gap widths are bimodal
(2–3 px between glyphs, 10–16 px between words) but the two overlap. Across gap thresholds from
10 to 18 px the ratio b/a stays around 1.0–1.4, i.e. an uncertain space seems to leave about as
much of a gap as a certain one, but the confidence intervals are huge (roughly 0 to 4) and the
correlation between counted gaps and ZL spaces is only 0.25. At this resolution I can't tell.

## So what

The line detector is good enough to be useful and honest about where it fails. The space
question needs the full-resolution Beinecke images and word-level alignment, not line-level
counts. The text-only version of the question (community/c02) gives a clearer answer: about 38%
of uncertain spaces behave like word-internal breaks. If the image measurement ever gets precise
enough, that's the number it should reproduce.

Next: full-res scans for a few pages, align ZL words to ink blobs along each line, and measure the
gap at every `.` and `,` directly.
