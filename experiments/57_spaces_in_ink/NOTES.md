# 57 — Spaces in the ink

## What I think

Exp. 55 measured spaces with word boxes, but boxes are drawn by a transcriber, so they carry the
transcriber's idea of where words are. The ink doesn't. The VoynichManuscriptOCR annotation project
(github.com/daniilvaino/VoynichManuscriptOCR) publishes, for all 227 page images, an ink mask and a
traced line through the middle of every row of text (two independent tracing runs that agree, or a
human check). That's enough to read the spaces off the ink.

## What I did

Along each traced row, a band of ±0.9 x-heights is scanned every half pixel; every stretch without
ink between two inked stretches is a gap, measured in x-heights (the row's letter height).

1. The distribution of gap widths over the whole manuscript (116 000 gaps).
2. Words per line counted from the ink (gaps above a threshold, + 1), against ZL's count for the same
   line, with doubtful spaces read as spaces or as no space. Lines matched by order on the 26 pages
   whose traced rows and ZL lines are equal in number (499 paragraph lines).
3. Each of ZL's boundaries on those lines placed in the ink (glyphs laid out in proportion to their
   count along the inked row; the boundary gets the widest gap within 1.5 glyph-widths of where it
   should be), then the width of certain and doubtful spaces, and exp. 46's coupling by ink width
   (`boundaries.py`).

## Result

Gap widths: a tall peak at 0.1-0.3 x-heights (the gaps between glyphs inside a word), a trough at
about 1.0 (1.2% of gaps per 0.1 bin), and a broad second hump at 1.2-1.9 (spaces between words). The
manuscript's spaces are a physical category of their own.

| space if the ink gap is at least | words per line, ink | ZL, doubtful spaces as spaces | ZL, doubtful spaces joined | r |
|---|---|---|---|---|
| 0.8 x-heights | **7.37** | 7.88 | **7.38** | 0.90 |
| 1.0 x-heights | 6.43 | 7.88 | 7.38 | 0.85 |

Each transcribed boundary in the ink:

| | boundaries | mean ink gap | wider than 0.8 |
|---|---|---|---|
| certain space (ZL '.') | 3183 | 1.35 x-heights | 73% |
| doubtful space (ZL ',') | 252 | 0.94 | 53% |

Coupling across certain spaces by ink width: 0.21 bits (narrowest third), 0.19, 0.12 (widest third).

## So what

1. The ink has word spaces, and at a threshold just below the trough the ink gives the same number of
   words per line as ZL with its doubtful spaces closed (7.37 against 7.38). The transcribers' certain
   spaces are, on average, the ink's spaces; the doubtful ones are mostly not.
2. Doubtful spaces are a third narrower in the ink, as Rozanova and Temerev found with boxes and a
   300-gap pixel audit. Here it's 3435 boundaries measured on the ink directly.
3. Even among certain spaces, the coupling across the space falls as the ink gap widens (0.21 → 0.12),
   the same direction as exp. 55 with boxes. Two independent measures, boxes and ink, agree: the
   boundary habit is strongest where the space is least a space.

## Caveats

- Placing boundaries by glyph count assumes glyphs of equal width; *ch*, *sh* and the gallows are wider
  than *i* or *e*, so some boundaries pick up a neighbouring gap. That blurs the coupling-by-width
  gradient, it doesn't create it.
- Only 26 pages could be matched line by line; the gap histogram uses all 227.
- The ink masks are the project's stage-1 masks; the paper's resolution is that of the published display
  images (x-height about 8-10 px).
