# 24 — Do similar words sit under each other?

## What is claimed

The heart of Timm & Schinner's self-citation idea is positional: the scribe looks at the
lines just above and copies, with changes, a word from about the same horizontal position.
Their papers show this with marked-up pages where similar words stack vertically. Their
generator builds it in (in my port, most sources are taken at the writer's current position
in a recent line).

## What I think

Everything I've shown in favour of copying so far (near-repeats, line cohesion, the core)
is about *which* words turn up near each other, not *where*. Marked-up examples can't tell
alignment from two lines simply sharing words, and I already know the margins behave
specially: line-first words resemble each other, and so do line-last words (exp. 10, 20).
So the positional claim has never really been tested here. I couldn't find a test of it with
a proper null elsewhere either.

## What I did

For every pair of lines on the same page, k lines apart: match each word of the lower line
to the same-or-one-edit words of the upper line, and measure how far apart they are
horizontally (glyphs from the left margin). Null: same upper line, interior words in random
order, 300 times. First and last words left out of the main test. Same measurement on the
copying model (where alignment exists by construction), Latin, Italian and Naibbe.

## Result

| one line apart | matches | distance | shuffled | closer by | z |
|---|---|---|---|---|---|
| VMS, all | 6884 | 17.18 | 17.38 | 1.1% | −1.3 |
| VMS Currier A | 1753 | 16.41 | 16.70 | 1.7% | −0.9 |
| VMS Currier B | 5092 | 17.47 | 17.66 | 1.1% | −1.3 |
| copying model | 6107 | 11.86 | 13.97 | **15.1%** | **−16.6** |
| Latin | 506 | 18.21 | 18.07 | −0.8% | +0.3 |
| Italian | 1444 | 15.06 | 15.61 | 3.5% | −1.9 |

- **One line apart, similar words in the VMS are not vertically aligned** beyond what the
  shuffle gives (p = 0.08). The generator, measured the same way, shows an effect fourteen
  times larger.
- Two and three lines apart there is a small real effect (3.6% and 3.0% closer, p = 0.003),
  about a quarter to a half of the generator's at those distances. Italian prose chopped
  into lines shows effects of the same size at some lags, so I don't read much into it.
- **With the margins left in, the VMS looks strongly aligned** (z = −9.2). That is the
  line-first and line-last words resembling each other, not copying down a column. It's
  very likely what the eye picks up on a marked-up page.
- By section and hand, only the stars section / hand 3 shows anything (3.4% closer,
  p = 0.01).

## Caveat

Glyph counts are a stand-in for millimetres, and on herbal pages lines bend around the
drawing. But the same measure finds the generator's alignment without trouble, and the
text-only stars pages show at most a fifth of it.

## So what

The positional half of the self-citation hypothesis doesn't hold up: words are not, in the
main, copied from the spot above. What does hold is weaker and more general: a line shares
words and near-words with the lines before it. Whatever produces that isn't the eye
travelling up the column. Together with exp. 22 (rare variants aren't reused) this leaves
"copying" looking less like copying from the page and more like a writer cycling through a
small working set held in the head.
