# Line and word-boundary structure in the Voynich manuscript: what ciphers and copying each explain

*Working draft, November 2026. Numbers are reproducible from `experiments/` in this repository;
each section names the experiment it comes from.*

## Abstract

We measure the Voynich manuscript (Beinecke MS 408) against 18 historical texts on thirteen
statistics and use the gaps to test two families of text-generating models: verbose
homophonic ciphers (Greshko's Naibbe and an autokey variant) and the self-citation process of
Timm & Schinner. Four observations about line and word boundaries drive the comparison.
(1) Line starts are rewritten: word types missing from line-initial position reappear there
with *s*, *d* or *t* prefixed (r = 0.10-0.16, p < 0.001), in Currier B only. Line ends are
not rewritten but selected. (2) Immediate repeats of the same word are entirely accounted for
by lines reusing their own vocabulary (9.4 vs 9.3 per 1000 pairs with words shuffled within
lines), while near-repeats exceed that baseline (36.0 vs 30.8, p < 0.003). (3) The last glyph
of a word predicts the first glyph of the next; this coupling survives every reading of the
transliteration's uncertain spaces, but its size depends on that reading (rank 15 → 11 of 18).
(4) The cipher models reproduce word-internal statistics and none of the line structure; the
copying model reproduces line structure and near-repeats but not the coupling or the share
of one-off words. A copying scribe with a simple preference at the word boundary reproduces
the coupling with no cost elsewhere, so the coupling is not evidence of encipherment.

## 1. Introduction

Most quantitative work on the manuscript compares single numbers (character entropy, word
length, Zipf slope) with natural-language corpora (Lindemann & Bowern 2020; Bowern &
Lindemann 2021). Two recent constructive models reverse the question: given a mechanism, how
many of the manuscript's statistics does it reproduce? Greshko (2025) shows that a
hand-executable verbose cipher applied to Latin or Italian matches the low conditional
entropy and much of the word structure. Timm & Schinner (2020) propose that there is no
underlying text at all and that each word is a modified copy of a word nearby. Rozanova &
Temerev (2026) show that both kinds of imitation miss the coupling of glyphs across word
boundaries and the high share of one-off words.

We put both mechanisms through the same battery and focus on structure that sits at line
and word boundaries, because that is where the two families make different predictions.

## 2. Data and methods

**Transliteration.** Zandbergen's ZL transliteration (IVTFF 3b), paragraph text only, with
ligature braces resolved and uncertain readings dropped. Takahashi's transliteration is used
as a replication set. Currier language and Davis' scribal hands from the page headers.

**Uncertain spaces.** ZL marks uncertain spaces with a comma. We use three readings (exp. 16):
*split* (a space), *join* (no space) and *smart* (joined when the glued form occurs at least
twice elsewhere). *split* is the default; every headline result is checked under the others.

**Benchmark.** Thirteen metrics on 10 000-word samples: hapax ratio, MATTR-500, mean and SD of
word length, h1, h2, Zipf slope, edge coupling (mutual information between a word's last
glyph and the next word's first glyph minus a shuffled baseline), word-level MI, repeat rate,
divergence of line-first and line-last word distributions from the rest, and line cohesion.
Each metric is scaled by the median absolute deviation over the 18 historical texts of
Lindemann & Bowern (floor: 10% of the manuscript's value). Distance = RMS of scaled
differences; "core" uses the nine metrics that don't depend on line breaks.

**Models.** Naibbe from Greshko's published tables, validated against his ciphertext
(h2 2.11 vs 2.09, hapax 0.59 vs 0.58). Autokey variant: with probability p the table for the
next word is read from the last glyph of the previous word through a fixed chart (exp. 13).
Line-start rule after Smith: with probability q a line-initial word takes an *s*, *d* or *t*
prefix. Self-citation generator reimplemented from the procedure and rule tables of Timm's
VoynichTextGenerator (exp. 17), optionally with a boundary preference (exp. 18).

## 3. Results

### 3.1 Where the manuscript is extreme (exp. 00-02, 16)

Under all three readings of uncertain spaces the manuscript has the lowest h2 (2.15), the
lowest h1 and the lowest word-level MI of the 18 historical texts, and the highest
line-first and line-last divergence. h2 is also below all 265 Wikipedia samples with mean
word length above 2. Edge coupling is in the upper half (15th of 18 under *split*, 11th
under *smart*, 9th under *join*): real, but not extreme once probable non-spaces are removed.

### 3.2 Line starts are rewritten, line ends are selected (exp. 08, 10, 14)

Line-initial *s*-words are a common word with *s* prefixed 52% of the time vs 8% mid-line,
replicating Smith and Pelling. To test the stronger claim, that line-initial position
*transforms* words, we correlate, across word types, the deficit of a type at line start with
the surplus of glyph+type there. For *s*, *d* and *t* the correlation is positive and
significant (r 0.13, 0.16, 0.10, p < 0.001, permutation null; replicated on Takahashi), in
Currier B only; *y*, *q* and *k* go the other way. The mirror test at line end (12 endings
rewritten as -m or -g, singly and pooled by stem; 97 tests) finds nothing: line-final words
are shorter (4.73 vs 4.96 glyphs) and favour -m forms (*am* ×23, *dam* ×12 over expectation)
without taking anything from their siblings. Line starts behave like a transformation; line
ends add rather than replace (3.6).

### 3.3 Repeats: composition vs adjacency (exp. 15)

Natural texts avoid immediate repeats (Latin 0.0 per 1000 adjacent pairs vs 4.4 expected
from within-line shuffling). The manuscript doesn't (9.4 vs 9.3, p = 0.42; A 0.34; B 0.55).
Its exact repeats are therefore not an adjacency effect but a consequence of lines reusing
their own vocabulary. Near-repeats (edit distance 1) are different: 36.0 vs 30.8 per 1000
(p < 0.003 in A and B separately), most often insertion/deletion, *r↔l*, *k↔t*, *c↔s*.
Repeats avoid the first pair of a line (3.4 vs 11.1 mid-line) and line breaks (6 observed vs
11.8 expected), consistent with 3.2.

### 3.4 Models

| model | distance | core | edge | hapax | line cohesion |
|---|---|---|---|---|---|
| Currier B vs whole manuscript (scale) | 1.23 | 0.71 | 0.245 | 0.68 | 1.95 |
| Naibbe, published ciphertext | 4.54 | 0.94 | 0.002 | 0.58 | – |
| autokey Naibbe + line-start rule | 3.92 | 0.49 | 0.143 | 0.63 | – |
| self-citation (B settings, 8 seeds) | 2.46 | 0.97 | 0.013 | 0.55 | 2.01 |
| self-citation + boundary preference, p = 0.65 | 2.42 | 0.71 | 0.115 | 0.55 | 1.99 |
| + line-end rule, q = 0.6 | 1.89 | 0.68 | 0.111 | 0.59 | 2.34 |
| + prefer common sources, c = 0.5 (q = 0.5) | 1.49 | – | 0.108 | 0.61 | 1.84 |

The cipher models fail on line metrics (line-last −9.8, repeat rate −8.7, cohesion −5.1 in
scaled units for the best variant); the copying model fails on word metrics (hapax −1.9,
h2 high) and has no coupling. The autokey reproduces the size of the coupling but only part
of its pattern (held-out r 0.24-0.43; manuscript odd vs even lines 0.98).

### 3.5 Coupling without a key (exp. 18)

If the copying scribe discards, with probability p, words whose start does not suit the
previous word's last glyph, coupling appears at the manuscript's level for p ≈ 0.65-0.8 and
the core distance falls from 0.98 to 0.71 with line metrics unchanged. With preference lists
fitted on odd lines the pattern matches even lines (r 0.70); random lists of the same size
give the size but not the pattern (r 0.02, best 0.16). Because the fitted list is read off the
manuscript and the pattern is stable across halves, the pattern match shows only that the
rule can carry it.

### 3.6 Rare words (exp. 19-21)

Four in five of the manuscript's singletons are one edit from a word that occurs at least
twice, or two such words joined (Latin and Italian: one in five), and they concentrate at
line edges: 27% of line-first words, 13-17% mid-line, 24-29% of line-final words.
Line-first singletons typically add a glyph in front of a known word, line-final ones add a
glyph at the end. A line-end rule in the copying model reproduces the line-final singleton
rate and the line-final word distribution together (distance 2.39 → 1.9), but not the hapax
ratio: the model has the singletons and lacks the core. In Currier B the 87 types with more
than 20 occurrences cover 54% of a 10 000-word sample; the model's 58 such types cover 30%.


Raising the copying model's mutation rate moves hapax only from 0.55 to 0.59 and costs line
cohesion (1.99 → 1.66) and the near-repeat excess. The model is already more varied locally
than the manuscript (MATTR 0.56 vs 0.54); what it lacks is one-off words. The manuscript's
frequency distribution has a heavier tail of singletons than copying produces.

### 3.7 Locality and the core (exp. 22)

In the manuscript, words of middling or low frequency recur on the next line only about
twice as often as chance (Latin: the same; Italian 4-11×; copying model 8-17×), while the
most frequent words are the locally persistent ones (1.5-1.7×, fading over about 25 lines;
Latin function words 1.0). A copying process in which rare variants are seldom used as
models (the source is re-drawn with probability 0.5 if it has been written fewer than three
times) reproduces the size of the core (51% vs 54% of the text), line cohesion, MATTR and h2
together, and brings the distance to 1.49.

### 3.8 Out-of-sample check (exp. 23)

On 26 measures not used for tuning, the best model is within 0.8-1.25× of the manuscript on
10 (near-repeat excess, singleton composition, word length) and more than 2× off on 6, all
of them about glyph content: *q*-initial words are 1.4% of its output against 20% of Currier
B. The thirteen benchmark metrics are insensitive to which glyphs words are made of; scores
on them, for any model, need a content check alongside.

### 3.9 Position on the page (exp. 24, 25)

Self-citation as proposed is positional: sources lie above the word being written. With
line-first and line-last words excluded, same-or-similar words in consecutive lines are
1.1% closer horizontally than under a within-line shuffle (z = −1.3, p = 0.08); the
generator, measured identically, gives 15% (z = −16.6). Including the margins gives z = −9
in the manuscript, which is the line-edge effect of 3.2 and 3.6, not columnar copying.

Short-range sharing of vocabulary ignores the page. In herbal A (one scribe, 95 pages, one
plant per page) the last lines of a page share as many word types with the first lines of
the next page as adjacent lines within a paragraph do (ratio 1.00, 95% interval 0.84-1.18;
1.22× a shape-matched control, p = 0.001), and the real next page ranks in the top tenth of
candidates for 26% of page breaks. Lines 10-30 apart on the same page share no more than
chance (0.95). The carry-over is weaker in the stars section and absent in the
balneological quire, where it fails at the leaf turn.

## 4. Discussion

The two families fail in complementary places. Encipherment of a real text gives the
manuscript's word-internal statistics and, with an autokey, its boundary coupling, but no
mechanism that makes lines share vocabulary or makes line starts rewrite. Copying gives line
cohesion, near-repeats and position-dependent vocabulary, and with one habit at the word
boundary, the coupling. The features that remain unexplained by copying (singleton excess,
line-end selection, the *s/d/t* line-start transformation) are all ones a scribe could produce
by rules about *where* on the line a word goes, which suggests the next generation of models
should treat line position as an input, not an outcome.

Two results bear on what the short-range structure is. It is not positional (3.9), so it is
not the product of an eye moving up the column; and in the herbal it runs through the
change of plant at every page break, so it is not the product of subject matter. What
remains is a property of the act of writing: a small working set of forms, renewed slowly,
with one-off variants at the line edges.

We do not claim the manuscript is meaningless. A plaintext could survive under a copying
process if copying were the cipher's mechanism. But the statistics we can measure no longer
require one.

## 5. Limitations

All numbers are conditional on the ZL transliteration and on its word division; the comma
analysis bounds but does not remove that dependence. Edge coupling depends on what counts as
a space. The benchmark weights metrics equally and its scale comes from 18 texts. Both
generators have many tunable rates; we report seeds and settings but have not searched the
full space. The boundary list in 3.5 is fitted to the manuscript, and the final model has three rates fitted while monitoring the benchmark (3.8 is the check on that).

## References

- Bowern, C. & Lindemann, L. (2021). The linguistics of the Voynich manuscript. *Annual Review of Linguistics* 7.
- Currier, P. (1976). Papers on the Voynich manuscript. In M. D'Imperio (ed.), *New Research on the Voynich Manuscript*.
- Davis, L. F. (2020). How many glyphs and how many scribes? Digital paleography and the Voynich manuscript. *Manuscript Studies* 5(1).
- Greshko, M. (2025). The Naibbe cipher. *Cryptologia*. doi:10.1080/01611194.2025.2566408.
- Lindemann, L. & Bowern, C. (2020). Character entropy in modern and historical texts. arXiv:2010.14697.
- Rozanova, ? & Temerev, ? (2026). A glyph is not a letter, a token is not a word, a space is not a space. arXiv:2608.17096.
- Smith, E. M. (2015-2016). Posts on line-initial glyphs, *Agnostic Voynich* (blog).
- Timm, T. (2014). How the Voynich manuscript was created. arXiv:1407.6639.
- Timm, T. & Schinner, A. (2020). A possible generating algorithm of the Voynich manuscript. *Cryptologia* 44(1).
- Zandbergen, R. Transliteration files (IVTFF), voynich.nu.

*To check before submission: initials for Rozanova & Temerev; exact title/venue of Davis 2020;
page ranges.*
