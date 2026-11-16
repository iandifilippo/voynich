# c12 — A language-independent affix parser (bi3mw, voynich.ninja)

## What was proposed

bi3mw posted a small parser that knows no language: it takes the 25 commonest word
beginnings and endings (2-5 letters) as prefixes and suffixes, strips them from both ends of
each word, and calls the rest the stem. His heatmap of prefix × suffix on the manuscript has
a few cells holding a lot of the text (*dai/in* 851, *qoka/iin*, *oka/iin*), and some cells
only ever occur with no stem at all. He suggested comparing it with generated texts, which is
exactly the right use.

## What I did

His algorithm, his setting (top 25), 10 000 words of each text: Currier A and B, the copying
model, the Naibbe cipher of Pliny, and Latin, Italian and English.

## Result

| | prefix and suffix | stems / distinct words | top 10 cells hold | prefix → suffix (bits) |
|---|---|---|---|---|
| Currier A | 15% | 0.52 | 8% | 0.06 |
| Currier B | 23% | 0.57 | 18% | 0.15 |
| copying model | 14% | 0.64 | 12% | 0.21 |
| Naibbe cipher of Latin | 21% | 0.50 | 14% | 0.14 |
| Latin | 16% | 0.83 | 4% | 0.13 |
| Italian | 11% | 0.82 | 4% | 0.10 |
| English | 3% | 0.86 | 2% | 0.07 |

In real languages, once the affixes are taken off, almost every distinct word still has its
own stem (0.82-0.86). In the manuscript about half do; the affixes are most of the word. The
Naibbe cipher gives the same picture, cell for cell almost (*qo/dy* is its biggest cell and
Currier B's). How strongly the prefix picks the suffix doesn't separate anything.

## So what

The heatmap is real and it's a good picture of Voynich word structure, but it's a picture of
the glyph system, not of a morphology: a cipher of plain Latin makes the same heatmap. It
agrees with exp. 34 from a different angle: the words are built from a small set of parts,
and there's little left over that could be a stem carrying meaning.
