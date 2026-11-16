# c05 — Is EVA cutting the script in the wrong places?

## What was claimed

Two separate arguments that point the same way. Rozanova & Temerev (2026): EVA glyphs behave
like pieces of recurring multi-glyph units ("a glyph is not a letter"). A Reddit post ("Is it
too late to rethink EVA?", Nov 2026) splits words into stroke "particles" and asks whether we
picked the wrong unit from the start.

## What I thought

The low character entropy of Voynichese (experiment 02) is measured on EVA. If EVA slices one
real letter into two or three glyphs, h2 would be low for a boring reason: the second glyph of
a letter is almost fully predictable from the first. So the question is not "what's the right
alphabet", which nobody can answer, but: **is there any grouping of EVA glyphs that makes the
text behave like an ordinary alphabetic language?**

Hypothesis: if EVA is just over-split, merging the most common glyph pairs should bring the VMS
onto the curve that Latin, Italian and English follow when you merge their letters the same way.

## What I did

Byte-pair merging inside words: repeatedly fuse the most frequent adjacent pair into a new
symbol, and track alphabet size, h2, and h2 divided by log2(alphabet) so cuts with different
alphabet sizes can be compared. Same procedure on the VMS (all paragraph text and Currier B)
and on four comparison texts, 10k words each.

## Result

| merges | VMS alphabet | VMS h2/log2(alph) | Latin | Italian | English | VMS units per word | Latin units per word |
|---|---|---|---|---|---|---|---|
| 0 | 26 | 0.46 | 0.70 | 0.64 | 0.67 | 4.7 | 6.2 |
| 10 | 36 | 0.52 | 0.70 | 0.63 | 0.67 | 3.3 | 5.2 |
| 40 | 66 | 0.56 | 0.65 | 0.60 | 0.61 | 2.3 | 4.2 |
| 120 | 146 | 0.53 | 0.57 | 0.54 | 0.53 | 1.8 | 3.4 |

Merging pushes the VMS up and the natural texts down. They meet somewhere around 100-150 units.
At that point the gap in normalised entropy is gone, but a Voynich word is only ~1.8 units long,
against 2.4-3.4 for the natural texts at the same alphabet size.

## So what

Re-cutting EVA into a better *alphabet* doesn't make the text look like a language. Re-cutting
it into ~150 *bigger* units does, and then words are one or two units long. That's the profile
of a syllabary or a code (a verbose cipher where each plaintext letter or syllable becomes a
small group of glyphs), which fits the Naibbe idea (c01) better than the "wrong transcription
alphabet" idea. A stroke-level alphabet would go the other way (more, smaller units) and make
the entropy even lower.
