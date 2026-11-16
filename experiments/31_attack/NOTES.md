# 31 — Attack 1: one symbol, one letter

## The hypothesis

The oldest idea: the manuscript is ordinary text with each letter replaced by a sign. The
objection is that there are too few glyphs behaving too regularly, so the modern version
says the *signs* aren't single glyphs: groups of glyphs stand for letters (a verbose
cipher), several signs can stand for the same letter (homophones), and the word spaces may
be decoration. That is a big family, and exp. 30 says the solver reads all of it back
when it's really there.

## What I did

Five ways of cutting the text into symbols (single glyphs; the glyph groups *ol, dy, qo,
iin…*; frequent pairs merged until 60 or 150 extra units; words cut into two pieces), with
spaces kept or ignored, against nine languages: Latin, Italian, Spanish, French, German,
Middle English, Czech, Hungarian, Turkish. 81 combinations, each on 3000 words of Currier A
and of Currier B.

Two controls go through exactly the same pipeline: the copying model's output, which has no
content by construction, and Currier B with the glyphs of every word shuffled.

## Result

- **Nothing reads.** The best key over all 81 combinations leaves the manuscript 0.109 per
  letter below real text (Currier B, glyphs, spaces ignored, Latin). None comes within the
  0.05 I set as the bar. Real words: at most 9% of letters against 36-66% for real text.
- **The manuscript does no better than text with no content.** The copying model's best is
  −0.120, and across the 81 combinations the manuscript minus the control averages −0.004
  (B) and −0.018 (A): B wins 38 times, loses 43. The best "reading" of the control is as
  convincing as the best of the manuscript:

  | | decoded |
  |---|---|
  | VMS B → Latin | *alacentalium ribusarence murobeditetosroene…* |
  | VMS A → Italian | *utididicolitaloca bitidialiniciamimire…* |
  | control → German | *ahist bish eind iste erse eist eind bind bilist…* |

- **One scheme can't be trusted at this size.** With words cut into two pieces (400 symbols)
  the manuscript beats the copying model in all nine languages by 0.05-0.12. But the other
  control, shuffled glyphs, then scores *above real text* in five languages (+0.05 for
  Latin). 400 free symbols on 3000 words is enough rope to make Latin out of anything, and
  the advantage being the same in Spanish, Hungarian and Turkish says it comes from the
  shape of the text, not from a language. That scheme has to be rerun on the whole
  manuscript before it means anything.

## What this rules out, and what it doesn't

Ruled out, within the solver's demonstrated power: that Currier A or B is one of these nine
languages written with one sign (a glyph, a glyph group, or a merged unit, up to about 180
of them) per letter, spaces meaningful or not.

Not ruled out: other languages; signs that stand for more than one letter (syllables, or the
letter-pairs of a Naibbe-type cipher); text that was changed before enciphering (no vowels,
letters rearranged: exp. 32); anything with a key that changes as it goes; a code where a
whole word stands for a whole word.

## So what

The useful part isn't the null, which most people expected. It's that the control is
indistinguishable: any future "the manuscript decodes to X-like text" has to show the
copying model doesn't decode to X-like text just as well.
