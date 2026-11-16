# 34 — Slots, memory, and whether the words are a vocabulary at all

## What was claimed

That the text came out of a device. García Jiménez says a volvelle (c10), Rugg a table and
grille, and Zattera (2022) showed that most words fit a grammar of twelve ordered slots, each
holding one of a few glyphs or nothing. The cheapest device you could build from that has one
ring per slot and reads them off separately.

## What I think

That version makes a prediction sharp enough to kill it: the slots would be independent. And
once you are measuring how much one part of a word knows about another, there is a more
general question underneath, which doesn't need a slot grammar: does a Voynich word behave
like an item in a vocabulary, or like the output of a short-sighted rule?

## What I did

Three scripts.

- `run.py`: parse words into twelve slots (my reading of Zattera's table; it takes 79% of
  the tokens of Currier A and 84% of B, under half of the distinct words). Shared information
  between slots against columns shuffled independently. Held-out cost per word under
  independent slots, a chain (each slot given the last glyph written), and a model that sees
  the whole word so far. What an independent device would have written.
- `memory.py`: no slots. Held-out cost of a word when the model sees the last 1, 2, 3, 4
  signs, in the manuscript, two content-free controls and ten historical texts, all cut to
  11 000 words. Then the same with a model that may also remember whole words.
- `between.py`: what the previous word saves on the next.

## Result

**Independent rings: no.** Slots share 4.4 bits per word in A and 5.2 in B; independent
filling would show 1.5-1.7 at this sample size. A device with independent rings would have
produced three to four times as many distinct words as the text has (4470 against 1515 in A,
9704 against 2284 in B), and only one in ten of them exists. The dependence is mostly between
neighbours: *o/a* with the final *d/l/r/m/n*, the *i*-run with the final, the final with *y*.

**A chain: nearly all of it.** Per held-out word: independent 13.1-14.0 bits, chain 9.4-9.5,
whole word so far 9.3. Knowing everything written so far in the word is worth 0.1-0.25 bits
more than knowing the last glyph.

**The same without slots, against real texts** (bits per held-out word):

| | last sign | last 2 | last 4 | gain 1 → 4 |
|---|---|---|---|---|
| Currier A | 11.8 | 11.3 | 11.9 | −0.1 |
| Currier B | 11.1 | 10.4 | 10.9 | +0.1 |
| copying model | 12.1 | 10.5 | 10.5 | +1.5 |
| Naibbe cipher of Pliny | 12.4 | 11.3 | 11.2 | +1.3 |
| ten historical texts | 16-25 | 13-21 | 10-17 | +2.2 to +8.8 |

In the manuscript the best model looks two signs back and anything longer does worse on
held-out text. It holds with every EVA character as its own sign (best: 2; in both controls:
4). In Latin, Italian, English, French, Hebrew, Armenian, Old Norse the long view saves a
quarter to four tenths of the cost.

**Remembering whole words does not help.** Let the model memorise the words of four fifths
of the text and fall back on the two-sign model for the rest. In every language that saves
0.7 to 3.8 bits per word (5-22%). In the manuscript it saves nothing (−0.3: the model pays
for a memory that buys nothing). The frequency of a Voynich word is what its sign pairs
predict. The two controls: +0.1.

**Between words.** The previous word saves 0.16 (A) and 0.23 (B) bits on the next, measured
against the shuffled text. Languages: 0.9-1.4. Naibbe cipher of Latin: 0.10; copying model: 0.15.

## So what

1. The volvelle with independent rings is out. A device is not: what fits is something read
   left to right where each step depends on the step before, a table walked row to row, or a
   habit.
2. The words are not a lexicon. This is the strongest form I can give to something exp. 31
   and 32 kept running into. Any system where a Voynich word stands for a plaintext word
   keeps that language's vocabulary under the disguise: letter substitution, with or without
   nulls, sorted or reversed letters, a codebook. A vocabulary shows up in this test whatever
   the alphabet, and it isn't there. That family is excluded by a measurement, not by a
   failed search.
3. What survives is what the Naibbe cipher does: a word stands for a letter or two, chosen
   among alternatives, so word identity carries almost nothing and the message, if there is
   one, is in the sequence. And the meaningless-text reading survives too. On these three
   measures the cipher of Latin and the manuscript are close, and I can't separate them here.
4. Two new defects in my copying model: only 57% of its words fit the slot order (manuscript
   79-84%), so its edits put glyphs where the scribes never did, and it remembers too much
   (gain 1.5 bits where the manuscript has none). Copying whole words with small edits makes a
   vocabulary. The manuscript looks more like every word is assembled fresh from the same
   rule, with neighbours influencing the choices.

Point 4 changes how I read exp. 17-22. I'd been treating copying as the mechanism and the
word grammar as a side effect. It may be the other way round.

## Caveats

The slot table is my reconstruction and its coverage is lower than what Zattera reports for
his; the slot results should be read with that. The no-slot results don't depend on it. All
comparisons are at 11 000 words: with more text a language's lexicon would pay even more, and
I can't say what the manuscript would do with more than it has.
