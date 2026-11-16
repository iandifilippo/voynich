# c07 — Stephen Bax's partial decoding (2014)

## What was claimed

Bax worked "bottom-up", the way Champollion and Ventris did: find proper names first.
He identified about ten words with plants and one constellation: *kydainy* on f2r as
*kantairon* (centaury), *koaiin* on f3v as *kaur* (black hellebore), *oror* as *arar*
(juniper), the label next to the Pleiades on f68r as *taurn* (Taurus), plus coriander,
nigella, cotton, crocus and Chiron. From these he proposed sound values for 14 EVA signs
and clusters (his Appendix 1):

| EVA | k | y | d | r | m | n | sh | s | o | a | in | iin | e | ee |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sound | k | n | t/d/θ | r | r | r | kʰ/x/tʃ | s | a | ə/u/wa | ir | ur | o | oo |

He called it provisional and partial, and pointed towards a Near Eastern / Indo-Iranian
language. He singled out Taurus, centaury and *kaur* as the strongest readings.

## What I think

His method is the right kind of method and his paper is careful about its own limits. The
problem with proper-name readings is that each one is chosen with the picture in mind, so
the readings can't be their own evidence. The key has to keep working on text it wasn't
built from. That's testable.

## What I did

- Took every VMS word written only with his 14 signs (11 665 tokens, 30% of the text) and
  read it with his key.
- Vowels are the least certain part of his key and of any medieval spelling, so I compared
  consonant skeletons only: K N T R X S. Lexicon words in 30 candidate languages (Wikipedia
  samples in their own scripts: Arabic, Persian, Pashto, Kurdish, Turkic languages, Hebrew,
  Greek, Latin, Romance, Slavic, ...) were reduced to skeletons the same way.
- Null: 1000 keys that use **exactly his sound values**, just given to the ten consonant
  signs in a random order. If his assignment is right, it should beat its own shuffles.
- Two controls that carry no Near Eastern language at all: Greshko's Naibbe cipher of Pliny
  (Latin underneath) and our self-citation generator (no language underneath).

## Result

- His own words come out as intended: *kydainy* → KNTRN, *koaiin* → KR, *oror* → RR. The
  Taurus label is *dary* in ZL (he read *doary*); same skeleton, TRN.
- On the whole text, his key does beat its shuffles in many Near Eastern and Turkic languages
  (17-20 of 30 languages at p ≤ 0.05; best: Tatar, Uzbek, Azerbaijani, Arabic, p ≈ 0.001).
  Taken alone, that looks like support.
- **The control kills it.** The Naibbe cipher of a *Latin* text gets the same result, and
  stronger: 21-23 of 30 languages, with Arabic, Egyptian Arabic and Persian at the top
  (p = 0.001). There's no Arabic in Pliny. The generator, whose glyph statistics are
  further from the VMS, gets almost nothing (0-6 of 30).
- So what his key captures is *which glyphs are frequent where* in Voynich-like text. Very
  common sequences such as *daiin* (→ TR), *aiin*/*r* endings (→ R) and *k-* words (→ KR)
  map onto consonant patterns that are common in Turkic, Iranian and Arabic word endings.
  Any text with VMS-like glyph statistics benefits, meaning or not.

## Caveats

Skeletons over six consonant classes are coarse; at that level 80-90% of words match
*something* in a big lexicon, which is why the comparison is against shuffled keys and
against control texts, not against zero. I didn't test his plant identifications, which
need a botanist, only whether the sound values carry over to the rest of the text.

## So what

Bax's key doesn't do better on the Voynich text than on a cipher of Latin built to look
like it, so the agreement with Near Eastern languages comes from glyph statistics, not from
a language. This doesn't make his method wrong. It means that any proposed key has to be
checked against a control text with matching glyph statistics, which I'll use as the
standard test for future decipherment claims.
