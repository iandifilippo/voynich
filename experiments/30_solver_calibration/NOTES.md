# 30 — A cipher solver, and what it's worth

## Why

Up to now I've tested other people's readings. This starts the direct attack: assume a
family of ciphers, search the keys, see whether any key turns the manuscript into a
language. Before that means anything the solver has to pass two tests, and the second one
is the one decipherment claims never run:

- **Power.** Given real text enciphered by a known scheme, does it get the text back?
- **Honesty.** Given text with none of the target language in it, how good a "solution" does
  it hand me anyway?

## The solver

`voynich/crack`: simulated annealing over keys, compiled C called from Python. A key gives
every cipher symbol a short string of letters (one letter here). The decoded text is scored
by a letter 4-gram model of the target language, interpolated down to letter frequencies,
plus a term that pulls the decoded letter frequencies towards the language's. Scoring is
incremental (only the text around the changed symbol is rescored), which makes hundreds of
symbols affordable.

Two bugs on the way, both instructive. With add-k smoothing the best "solution" was a
key that mapped everything to *y*: contexts never seen got a flat 1/28, which beat real
letters in wrong places. And without the frequency term a word-level key settled on
*alalaal…*. A solver will find whatever the scoring function lets it get away with.

## What I did

4000 words of Latin held out from the model (Albert of Aix), enciphered with a simple
substitution and with homophonic substitutions of 50 to 400 symbols, spaces kept or
removed. Then the same ciphers on two texts with no Latin in them: Hungarian, and the same
Latin words with their letters shuffled.

## Result

| plaintext | symbols | letters right | score per letter (real Latin −0.91 / −0.99) | letters in Latin words (real 26-29%) |
|---|---|---|---|---|
| Latin | 26 to 400, spaces kept | 99.9% | −0.907 | 26.1% |
| Latin | 50 to 400, no spaces | 98.8-99.4% | −0.989 | 27.5-29.0% |
| Hungarian | 26 to 400, spaces kept | – | −1.21 to −1.24 | 0.1-0.3% |
| Hungarian | 50 to 400, no spaces | – | −1.18 to −1.20 | 0.6-1.9% |
| scrambled Latin | 26 to 400, spaces kept | – | −1.33 to −1.38 | 0-0.2% |
| scrambled Latin | 50 to 400, no spaces | – | −1.27 to −1.30 | 0.3-0.5% |

- **Power: complete within this family.** Any one-symbol-one-letter cipher up to 400 symbols,
  with or without word spaces, is read back essentially perfectly from 4000 words.
- **Honesty: a clear gap.** On text without Latin the best key stays 0.19-0.47 per letter
  below real Latin and puts under 2% of letters into Latin words, against 26-29%. More
  symbols do let it bend further (scrambled Latin: −1.38 at 26 symbols, −1.27 at 400), so
  the gap narrows as the key grows, but it's nowhere near closing at 400.

## A warning from a first try at Naibbe

I also threw the solver at Greshko's published Naibbe ciphertext without using his tables,
treating word pieces as symbols. With pieces cut by an unsupervised segmenter (83% of cuts
right, 597 symbols) the solver produced text that scores −1.04, *better* than the true key
restricted to those cuts (−1.20), with 19% of letters right. It reads like Latin
("…anceresentantiodesibustitificertia…") and is wrong. Two lessons: a 4-gram score near
real text is not evidence once the symbolisation itself is uncertain, and word hits are the
check that matters. Cracking Naibbe blind is its own project (joint segmentation and key);
it's the calibration target for the next attack.

## So what

The rule for exp. 31 onwards: a reading counts only if it lands within about 0.05 per letter
of real text **and** puts real words at something like the real rate, **and** the controls
run through the same pipeline don't.
