# 55 — Spaces measured on the page

## What I think

Everything in this series uses the transliteration's spaces, and two results (exps. 46, 53) put
their strongest effects at doubtful spaces. Exp. 12 tried to measure spaces on the scans myself
and couldn't resolve them at the resolution I had. Rozanova and Temerev ("A Glyph Is Not a Letter,
a Token Is Not a Word, a Space Is Not a Space", arXiv:2608.17096, August 2026) published, with
their reproduction archive (github.com/lrozanova/voynich-units), bounding boxes for every word on
223 folios, drawn on the page images (from voynichese.com). They used them to show that ZL's
uncertain spaces are physically narrower than its certain ones (normalised gap 0.004 vs 0.129).

The boxes let me redraw word boundaries from the page and re-ask two questions that matter for
everything after exp. 34: is there really no lexicon, and where does the coupling across the space
come from?

## What I did

Boxes read in reading order per folio, lines split where the next box starts back at the left or
drops by most of a line height. Gap = distance between one box's right edge and the next box's
left edge, divided by the folio's median box height. Folio language from ZL.

1. Words re-defined by closing boundaries whose boxes touch (gap ≤ 0) or nearly touch (≤ 0.125,
   ≤ 0.143), then exp. 34's lexicon gain on the result, against the same number of boundaries
   closed at random.
2. Exp. 46's coupling (last sign → next first sign), by tertile of physical gap, each with its own
   shuffle baseline.
3. Exp. 48's residual (choices shared by neighbouring words beyond the boundary glyphs, inside-sheet
   baseline), by tertile of gap (`residual.py`).

## Result

Lexicon gain (bits per word; positive in every language tested in exp. 34):

| | as boxed | touching joined | gap ≤ 0.125 joined | gap ≤ 0.143 joined |
|---|---|---|---|---|
| Currier B | −0.22 | −0.36 (random: −0.39) | −0.37 (−0.41) | −0.51 (−0.58) |
| Currier A | −0.32 | −0.40 (−0.44) | −0.54 (−0.59) | −0.58 (−0.60) |

Coupling across the space and the residual, by physical gap:

| | narrowest third | middle third | widest third |
|---|---|---|---|
| B: last sign → next first sign | **0.42** | 0.21 | **0.08** |
| A: last sign → next first sign | 0.25 | 0.09 | 0.03 |
| B: residual beyond the boundary | 0.29 | 0.24 | **0.25** |
| A: residual beyond the boundary | 0.14 | 0.03 | 0.13 |

1. **Still no lexicon.** However the words are cut from the page, remembering whole words doesn't
   help. Cutting by physical gaps is a little better than cutting at random (0.03-0.07 bits), so the
   gaps do follow word structure somewhat, but no vocabulary appears. Exp. 34's central result
   doesn't depend on the transcribers' spaces.
2. **The boundary habit is mostly narrow spaces.** At the narrowest third of gaps the last and first
   signs share 0.42 bits; at the widest third, 0.08, which is what Latin (0.04) and Italian (0.12)
   have across their spaces. Most of the "rule at the space" of exp. 46 is junctures inside what are
   really single words, as Rozanova and Temerev argue ("a space is not a space"). They reported a
   weak correlation between coupling and gap (r = −0.15) and no clean dose-response; with tertiles
   on the box text it is steep and monotonic.
3. **The residual isn't.** What neighbouring words share beyond the boundary glyphs is the same at
   wide gaps as at narrow ones in B (0.25 vs 0.29). It's between real, separate words.

## So what

This corrects part of exp. 46 and sharpens exps. 48-53. The boundary coupling that looked like a
writer's rule across words is, for the most part, the inside of words that the transcription split.
At real spaces Voynich words are about as independent at their edges as words of a language. What
remains between separate words is the residual: real, not made by spacing, still without a lexicon
or a consistent grammar (exp. 52).

## Caveats

- The boxes come from voynichese.com's segmentation and transcription, not ZL; a box is a
  transcriber's word, so "touching boxes" partly measures how that transcriber drew boxes.
- Gaps are quantised (box coordinates are coarse), so tertile edges fall on ties.
- The residual by tertile uses a third of the pairs each, so its noise is larger than exp. 48's.
