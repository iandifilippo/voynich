# c08 — Caveney's Greek line (voynich.ninja)

## What was claimed

Geoffrey Caveney reads the first line of f67r1, *teeodaiin shey epairody osaiin yteeoey
shey epaiin oaiin*, as Byzantine Greek: *geiopan tis ipeirous otan skiiois tis epan oan*,
"when the whole Earth and all the continents are in the shadows, as they said". He is careful
to call it tentative. His values let *t* be k or g, *e* be e or i, *d* be u or p, and he
suggests that the script doesn't distinguish voiced from voiceless sounds, which would lower
the entropy. He proposes a test: merge those letters in ordinary texts and see.

## What I think

It's the most honest kind of proposal: one line, clearly labelled as a guess, with a test
attached. So I ran his test, and then the two things a single reading can't tell you:
how much room the values leave, and what they do to text that isn't that line.

## Result

- **His test.** Merging g/k, d/t, b/p, z/s, p/f/v and u/v lowers h2 by about 0.1 bit in
  Greek, Latin, Italian and French (3.08-3.34 → 2.97-3.22). The manuscript is at 2.15. The
  merger explains about a tenth of the gap.
- **Room.** With the alternatives he allows, that one line has 8192 possible readings
  (*teeodaiin* alone has 16). Finding one that is Greek-like among 8192 is much less
  surprising than finding it among one.
- **The rest of the text.** Words written only with his signs come out as some Greek word
  31% of the time, against 13% when the same values are dealt to the signs at random
  (p = 0.01). That looks like support until the control: the copying model, which says
  nothing, gives 30% against 16%.

## So what

Third time the same thing has happened (Bax in c07, the Turkic key in c09). A key that gives
vowels to the glyphs that behave like vowels (*o, a, e, y*) and consonants to the rest will
produce pronounceable strings from any Voynich-like text, and pronounceable strings of four
or five letters are often words in a big lexicon. Beating your own shuffled key is necessary
and not nearly sufficient. The control text is what decides.
