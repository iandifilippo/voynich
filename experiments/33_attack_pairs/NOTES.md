# 33 — Attack 3: a sign is a letter or a pair of letters (not run: the solver isn't ready)

## The hypothesis

A syllabary, or a cipher that gives common letter pairs their own sign, as the Naibbe cipher
does with whole words. With two to three sign-like units per Voynich word (c05) that would
give words of three to five letters. It's the most plausible family left after exp. 31-32.

## What I did

Calibration first, as always. Held-out Latin and Italian written with one sign for each of
the 60 or 150 commonest letter pairs and one sign per remaining letter, spaces kept. The
solver's key maps each sign to a letter or to one of the language's 150 commonest pairs.
Hungarian written the same way as the honesty control.

## Result

| plaintext | signs | signs right | gap to real text | letters in real words (real: 26% / 59%) |
|---|---|---|---|---|
| Latin | 84 | 0% | −0.24 | 0.5% |
| Latin | 174 | 0% | −0.21 | 0.9% |
| Italian | 86 | 26% | −0.27 | 4.1% |
| Italian | 176 | 12% | −0.21 | 1.9% |
| Hungarian → Latin | 86, 176 | – | −0.28, −0.23 | 0.3%, 1.0% |
| Hungarian → Italian | 86, 176 | – | −0.37, −0.26 | 1.1%, 1.3% |

**The solver can't read this family.** On real Latin it ends up no closer to real text than it
gets on Hungarian. The true key exists and scores far better; the annealer doesn't find it.
With 176 choices per sign and signs of different lengths shifting everything after them, the
landscape is much rougher than with one letter per sign.

## So what

I have not run this attack on the manuscript. A null from a solver that can't read the
real thing would mean nothing, and reporting it would be dishonest.

What it needs before it's worth running:
- start from the one-letter solution and let signs grow a second letter, not from a random key;
- a search that isn't one change at a time (a beam over the commonest signs, or an EM over
  sign lengths);
- the same on Greshko's Naibbe ciphertext without his tables. A blind read of that is the
  proper entry test for this whole family, and my first two tries (exp. 30) didn't pass it.

This is the open front. Everything simpler has been tried and is empty or untestable.

**Later:** exp. 35 gets past this for the Naibbe kind of pairing (halves of words), with the full text and better cuts.
