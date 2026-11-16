# 35 — Attack 4: a word is one letter or two, on the full text

## The hypothesis

After exp. 34 this is the family left standing if the text is a cipher at all: the words
carry no vocabulary, so a word can't be a word; it can be a letter or a pair, picked among
alternatives. That is how the Naibbe cipher works (Greshko 2025), and exp. 33 couldn't read
it, so the manuscript was never tested.

## What was wrong in exp. 33

Not the annealer. With the true cuts and all 35 000 words, it reads the Naibbe text: 98% of
letters right. Two other things:

- **Length.** At 3000-5000 words there are enough keys that score like Latin without being
  the plaintext. At 5000 words the solver still returns a score within 0.011 of real Latin
  and the output is nonsense. From 11 000 words on it reads.
- **The cuts.** My segmenter agreed with the true cuts on 80% of tokens, and one wrong cut in
  five inserts and drops letters all along the stream. Most errors were one-letter words
  being split. The fix is one assumption: a word that stands for a single letter is much
  more frequent than one that stands for a pair, so the k most frequent words are whole and
  the rest are cut where both halves are commonest. Agreement: 93-95% for k between 80 and
  160.

I also tried the textbook method first (EM over an HMM with Latin's letter-pair table,
`em.py`). It gets 10-20% of letters, and the true key has a *lower* likelihood than what EM
finds. Letter pairs are too weak a constraint for 400 symbols.

## Entry test

The Naibbe cipher of Pliny, ciphertext only, no tables:

| k | language tried | read? | score vs real text | lost when words are shuffled |
|---|---|---|---|---|
| 110 | Latin | **94% of the plaintext** | −1.002 / −0.990 | 0.083 |
| 200 | Latin | 90% | −1.025 / −0.990 | 0.073 |
| 60 | Latin | no | −1.034 / −0.990 | 0.032 |
| any | Italian | no | 0.11-0.17 short | 0.02-0.04 |
| any | German | no | 0.04-0.12 short | – |

Cut to the manuscript's sizes (11 231 and 23 084 words) it is still read, 91% and 94%.
One annealing run finds it two times in three and a miss scores visibly lower, so every job
is the best of four.

So the signature of a hit is: within about 0.02 of real text, and shuffling the words costs
0.07 or more. A miss (wrong language, wrong k) is 0.03 or more short and loses 0.02-0.04
when shuffled.

## The manuscript

| | k | Latin: score / lost by shuffling | Italian: score / lost by shuffling |
|---|---|---|---|
| Currier A | 60 | −1.374 / 0.008 | −1.391 / 0.007 |
| | 110 | −1.454 / 0.005 | −1.479 / 0.004 |
| | 200 | −1.622 / 0.019 | −1.652 / 0.022 |
| Currier B | 60 | −1.395 / 0.014 | −1.406 / 0.018 |
| | 110 | −1.492 / 0.012 | −1.507 / 0.021 |
| | 200 | −1.667 / 0.029 | −1.700 / 0.032 |
| copying model | 60 | −1.450 / 0.009 | −1.493 / −0.031 |
| | 110 | −1.558 / 0.012 | −1.575 / 0.031 |
| | 200 | −1.821 / −0.023 | −1.783 / 0.034 |

(real text: Latin −0.990, Italian −0.895)

Nothing. The scores are 0.4-0.7 short, and what matters more, the text scores the same
with its words in random order, and so does the copying model. The scores themselves aren't
comparable with the Naibbe rows, for the reason in the next section.

## The inventory of halves

The more useful result came out of the bookkeeping. A Naibbe-type cipher has a table: so
many first halves, so many second halves, and that is all there will ever be. Cut the same
way (`pieces.py`):

| | words | first halves | second halves | all pieces | seen once |
|---|---|---|---|---|---|
| Naibbe cipher | 2500 | 171 | 125 | 406 | 20% |
| | 20 000 | 243 | 149 | 502 | 15% |
| Currier B | 2500 | 286 | 181 | 584 | 43% |
| | 20 000 | 906 | 525 | 1549 | 51% |
| Currier A | 2500 | 256 | 200 | 569 | 45% |
| | 10 000 | 627 | 438 | 1183 | 52% |
| copying model | 20 000 | 750 | 607 | 1468 | 42% |

Eight times more text adds a quarter to the Naibbe inventory (and most of that is my
segmenter's mistakes: the real table has 138 + 138 + 137 entries). In the manuscript it
nearly triples and half the pieces occur once. There is no closed table of halves. The
copying model grows the same way.

## So what

1. The solver now reads the family it couldn't. Blind, from ciphertext, at the manuscript's
   sizes. That was the entry test I set after exp. 33.
2. The manuscript is not a Naibbe-type cipher of Latin or Italian with a table of a few
   hundred halves. Two independent reasons: the attack that reads one finds nothing and
   shuffling costs nothing; and the inventory of halves is open where a table's is closed.
3. What this does not cover: a cipher whose pieces are not "at most two per word, frequent
   words whole" (three pieces, or pieces spanning words); a table several times larger,
   which would need more text than exists; other languages. With 1200-1700 pieces and only
   the 500 commonest given a letter, 5-7% of the stream is unread and the 4-letter contexts
   around the gaps are lost; that is why the absolute scores are so low, and why the
   shuffle test is the number to trust.
4. With exp. 34, the picture for a cipher is getting narrow. Word-for-word systems are
   excluded by the missing vocabulary. Letter-or-pair with a small table is excluded here.
   What is left would have to spread a letter over an open-ended set of word shapes with
   very little carried from word to word, at which point it is hard to say what
   distinguishes it from the rule-plus-neighbours account of exp. 34.
