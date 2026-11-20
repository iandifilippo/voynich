# voynich

Tools and experiments for reading the Voynich Manuscript (Beinecke MS 408).

The goal is to actually read it. The rule is that nothing counts until it beats a shuffled or random control, and failed ideas stay in the log.

## What's here

- **`voynich/`** – small Python package, no dependencies
  - `ivtff.py` parser for every IVTFF transliteration on voynich.nu (ZL, IT, RF, VT, GC, CD, FG)
  - `corpus.py` page/section/Currier language/scribe filters, comparison corpora
  - `metrics.py` glyph and word statistics that work on any text: entropies, hapax ratio, Zipf, edge coupling, word MI, line-start/end effects, line cohesion
  - `benchmark.py` "how Voynich-like is this text?" – 13 metrics scaled by the spread among 18 historical texts
  - `ciphers.py` hand-executable ciphers and generators to score (substitution, homophonic, verbose, syllable code, Naibbe-like, self-citation)
  - `cisiojanus.py` the medieval syllable-per-day calendar, syllabified (365/365)
  - `naibbe.py` Greshko's Naibbe cipher from his published tables, plus an autokey variant and Smith's line-start rule
  - `scan.py` line and gap measurements on page images (numpy/scipy/scikit-image, only needed for experiment 12)
- **`experiments/`** – each one is a `run.py` plus its `results/`; `experiments/community/` tests other people's claims
- **`docs/`** – state of the field, notes on f116v, GitHub landscape, and a paper draft (`docs/paper/draft.md`) on line and word-boundary structure
- **`RESEARCH_LOG.md`** – what we tried and what came out

## Quick start

```
python -m voynich.download      # transliterations + Lindemann & Bowern corpora
python experiments/00_baseline/run.py
```

```python
from voynich import Voynich, metrics, benchmark

v = Voynich("ZL")
v.words(section=["Z"], unit="L")          # zodiac labels
v.text_lines(language="B", hand="2")      # Currier B, scribe 2

dist, z, profile = benchmark.score(my_lines)   # score any text (list of lines of words)
```

## Results so far

| # | experiment | result |
|---|---|---|
| 00 | baseline | 38,718 tokens / 8,048 types; q word-initial 99.4%, then o 97.7%; p/f 15x denser on paragraph-first lines |
| 01 | 7 transliterations | line effects and low h2 hold in every transliteration and alphabet (h2 2.15 EVA, 2.57 with Glen Claston's 65-glyph alphabet) |
| 02 | 283 languages | VMS h2 is lower than every comparison text that tokenizes correctly (0 of 283) |
| 03 | scribes | Davis' hands split cleanly by Currier language (hand 1 = A; 2, 4, 5 = B; 3 mostly B); hands 2 and 3 are the closest pair |
| 04 | page order | neighbouring pages share vocabulary beyond hand + topic (p < 0.0005); joins across leaves are weaker than recto→verso of the same leaf, and that holds with tf-idf (p = 0.015) and rare-word overlap (p < 0.001), consistent with a disturbed binding |
| 05 | cipher benchmark | no cipher or generator reproduces the line effects; ciphers that reach VMS-level h2 lose the open vocabulary (hapax 0.22-0.41 vs 0.68) and edge coupling |
| 06 | zodiac labels | Cisiojanus alignment: null (2/40 tests at p<0.05, chance level). Position-as-number: not robust |
| 07 | word structure | glyph position inside words is far more fixed than in any comparison text (positional entropy 0.70 vs 0.83-0.93) |
| 08 | line positions | line-initial *s*-words are a common word plus *s* 52% of the time vs 8% mid-line (replicates Smith 2016, Pelling) |
| 09 | bifolia | conjoint leaves look more alike only with raw cosine (p = 0.002); with tf-idf or rare words, nothing. They share common-word profile, not vocabulary |
| 10 | linestart model | words missing from line starts are the ones that reappear there with *s*, *d* or *t* in front (r 0.10-0.16, p < 0.001, ZL and Takahashi); only in Currier B; *y* and *q* don't behave this way |
| 11 | label reuse | 63 labels repeat on 2+ pages, 49 of them across sections; same-section repeats only slightly above chance (31% vs 23%, p = 0.009) |
| 12 | scans | line detector on the PDF scans of quire 20 (tuned on half, tested on the other half): within ±1 line of ZL on 7/11 pages; certain vs uncertain spaces not separable at this resolution |
| 13 | autokey Naibbe | Greshko's tables + a rule where the last glyph picks the next table (p ≈ 0.65) gives VMS-level edge coupling without moving anything else; the coupling pattern only partly (held-out r 0.24-0.43 vs 0.98); with Smith's line-start rule, distance 4.86 → 3.92 |
| 14 | line-end model | no ending is rewritten as -m at line end, singly or pooled by stem (all p > 0.1, several strongly negative); line ends favour short words and -m forms (am ×23, dam ×12) without taking from their siblings. Starts rewrite, ends don't |
| 15 | repeats | exact repeats of the same word side by side are fully explained by lines reusing their vocabulary (9.4 vs 9.3 per 1000 with words shuffled inside the line, p = 0.42); near-repeats (one glyph changed) are not (36.0 vs 30.8, p < 0.003, A and B). Natural texts avoid repeats, the VMS doesn't; repeats avoid line starts and line breaks |
| 16 | commas | reading ZL's uncertain spaces as spaces, as joins, or joining only when the result is a known word: h2, h1, word MI and all line effects keep their extreme ranks; edge coupling does not (15th → 11th of 18 historical texts under the known-word reading) |
| 17 | self-citation | reimplementation of Timm & Schinner's generator: distance 2.45 (best so far; Naibbe 4.54, autokey + line-start 3.92), right line cohesion and near-repeat excess, but no edge coupling (0.01 vs 0.15) and too few hapaxes (0.55 vs 0.69). Ciphers and copying fail in opposite places |
| 18 | copying + boundary habit | the copying scribe discards, with probability p, words whose start doesn't suit the previous word's last glyph: p ≈ 0.65 gives VMS-sized edge coupling, core distance 0.98 → 0.71, line metrics unchanged. Coupling is not evidence of a cipher (but the fitted list is read off the VMS, so the pattern match is weak evidence) |
| 19 | copying: vocabulary | more glyph changes per copy raise hapax only 0.55 → 0.59 and cost line cohesion and the near-repeat excess. The model is already more varied locally than the VMS (MATTR 0.56 vs 0.54); what it lacks is one-off words |
| 20 | singletons | 4 in 5 one-off words are a known word with one glyph changed or two known words joined (Latin/Italian: 1 in 5); they pile up at line edges (27% first, 13-17% mid, 24-29% last; paragraph openers 47%). Line-first ones add a glyph in front, line-last ones add one at the end |
| 21 | line-end rule | giving the copying model one extra change on line-final words fixes line-end singletons and the line-end word distribution, distance 2.39 → 1.9 (best so far); hapax ratio stays low because the model lacks a core: 87 words cover 54% of Currier B, the model's top 58 cover 30% |
| 22 | locality | VMS rare words come back on the next line only ~2× more often than chance (copying model: 8-17×, Italian 4-11×); its common words are the local ones (1.5-1.7×, Latin 1.0). A copying model that prefers to copy words it has already written a few times gets the core, cohesion, MATTR and h2 right together: distance 2.18 → 1.49 (cf. Schwartz 2026, who fits frequency-weighted reuse at 73-77%) |
| 23 | scorecard | the best model on 26 measures it wasn't tuned on: right on near-repeats, singleton make-up, word length; badly wrong on which words (q- words 1.4% vs 20%). The benchmark sees shape, not content |
| 24 | vertical alignment | similar words in consecutive lines are not under each other once the margins are set aside: 1.1% closer than shuffled (p = 0.08) against 15% in the positional-copying generator. The alignment the eye sees is the line-first and line-last words (z −9 with margins in) |
| 25 | page memory | in herbal A the last lines of one plant page share as many word types with the first lines of the next as neighbouring lines of one paragraph (ratio 1.00; 1.22× a shape-matched control, p = 0.001): the common-word layer follows writing order and ignores the change of plant. The carry-over breaks in the balneological quire. (An earlier claim that herbal pages have no vocabulary of their own is withdrawn, see 27) |
| 26 | writing order | using the carry-over as a clock on 19 sheets: for scribes 2 and 3 the text of a verso continues onto the conjoint leaf of the same sheet (lift 1.64) and not onto the next folio in the book (1.21; difference CI 0.12-0.73), including three pairs where Layfield & Davis see drawings cross (76v/83r, 78v/81r, 33v/40r). For scribe 1 it is the other way round in 9 of 11 sheets. Groups differ at p = 0.035; small n |
| 27 | topic control | the page test on a real plant text (Pliny 16 by chapter): chapters have their own vocabulary only once common words are set aside (1.39, p = 0.01). Same test: VMS balneological 1.48, stars 1.39 (p ≤ 0.015), herbal A 1.23 (n.s.). A Naibbe cipher of the same book erases it (0.97); the copying model produces it without any subject (1.93) |
| 28 | page template | with paragraph openers and line edges removed, herbal A pages use the same words at the top, middle and bottom (z −0.6 against a null that keeps runs of similar lines). B sections: weak (p = 0.04, 0.10). No sign of entry structure; no real herbal available yet as a positive control |
| 29 | sheet geometry | every page-to-page transition within a sheet. Scribes 2 and 3: conjoint leaf beats next folio at every window size (p ≤ 0.004); in the stars quire the end of the earlier leaf runs into the start of the later leaf far more than the reverse (1.48 vs 0.77, 4 of 4 sheets), the signature of sheets written one at a time. Scribe 1: all four pages of a sheet are alike but no direction |
| 30 | solver calibration | a compiled annealing solver (`voynich/crack`) reads back any one-symbol-one-letter cipher of Latin up to 400 symbols, spaces or not, at 99% from 4000 words; on text with no Latin in it the best key stays 0.19-0.47 per letter below real Latin with under 2% of letters in Latin words (real: 26-29%). That gap is the acceptance test for every attack that follows |
| 31 | attack: symbol = letter | 5 ways of cutting the text into symbols × spaces kept or ignored × 9 languages (81 combinations): no key brings Currier A or B within 0.109 per letter of real text (bar: 0.05), and the manuscript decodes no better than the content-free copying model (mean difference −0.004). Two-piece symbols overfit at 3000 words (a shuffled control beats real text) |
| 32 | attack: transformed plaintext | same solver against text with vowels dropped, letters sorted within words, words reversed, and Hebrew / Arabic / Persian (each readable at 92-100% when really there). Sorted, reversed, Semitic: nothing (0.12-0.38 short, control as good). No vowels: the manuscript scores above real vowelless Latin with 34% of letters in real words, and so does the content-free control (32%). Consonant-only readings can't be tested this way |
| 33 | attack: letter or pair (not run) | calibration fails: on real Latin and Italian written with signs for letter pairs the solver gets 0-26% of signs and lands no closer to real text than on Hungarian. Not run on the manuscript; this family (syllabaries, Naibbe-type ciphers) is the open front |
| 34 | slots, memory, lexicon | twelve-slot parse: slots share 4.4-5.2 bits per word (1.5-1.7 if filled independently), so a device with independent rings is out; a chain on the last glyph gets within 0.1-0.25 bits of a model that sees the whole word. Without slots: the best model of a word looks two signs back, longer views do worse (languages gain 2-9 bits per word from the long view). Remembering whole words saves 0.7-3.8 bits per word in ten historical texts and nothing here: the words are not a vocabulary, which excludes every word-for-word encoding. A Naibbe cipher of Latin behaves like the manuscript on all three measures |
| 35 | attack: letter or pair, full text | the solver now reads the Naibbe cipher from ciphertext alone (94% of the plaintext; 91% and 94% when cut to the sizes of Currier A and B). What was missing in exp. 33: text length, and cuts (the commonest words are taken whole; cut agreement 80% → 95%). Signature of a hit: within 0.02 of real text and 0.07-0.08 lost when words are shuffled. Manuscript, Latin and Italian, three settings: 0.4-0.7 short, 0.004-0.03 lost by shuffling, same as the copying model. And the inventory of word halves is open (584 → 1549 pieces from 2500 to 20 000 words, half seen once) where the cipher's is closed (406 → 502) |
| 36 | assembled words | a generator that builds each word sign by sign, looking two signs back (`voynich/assemble.py`), fitted on half of Currier B and filling the other half: 18% of its tokens are words absent from the training half, held-out text 17% (a vocabulary: 0%; copying model: 49%); distinct words, hapax share, top words, q-, edge habits and the missing lexicon all match. Plus a short echo habit (1 word in 10 repeats one of the last five, usually with a sign changed): 11 of 14 measures within 0.8-1.25×; holds on Currier A and on IT and GC unrefitted. Replaces copying as the best account of the text |
| 37 | small machine | a hidden-state machine of 48 states writes Voynich words as well as the best sign chain (held-out bits per sign 1.97 vs 1.97 in B, 2.25 vs 2.25 in A) and with the right vocabulary (17% vs 20% new words). For Latin and Italian it is far worse than a 3-letter chain and writes 3x too many words. Voynich words are fully described by a few dozen states; words of a language aren't |
| 38 | read the machine | a 12-state machine is a readable table: space → q/o/ch-sh → gallows → e → d → y → space, or a → l-r / ii → n. No state loops; each writes one kind of sign. Zattera's slot grammar, found from scratch; same table for Currier A and B with different weights at the forks |
| 39 | forks: scribe or subject? | the same scribe (Davis's hand 2) takes the forks differently on herbal and bathing pages: R² 0.31 (random 0.03), pages told apart 95% (chance 51%); qo- 24% vs 9%, -edy 26% vs 14%. Subject explains more than hand does within herbal B (0.16). Halves of one section don't differ (no drift). First result pointing toward content; sessions or a per-section setting still fit |
| 40 | page identity | each page has its own fork weights: a half-page picks out its own other half 34-73% of the time (chance 2-6%), and 31-63% when the words the halves share are removed. The copying model's page identity collapses when shared words are removed (to 8-24%); an echo generator has none; real texts (casebook, surgery, tales, Picatrix, Latin, Italian) have almost none (4-11%). Replicates on IT. The procedure has a state that is set per page and held to its end |
| 41 | the page setting | 3 independent knobs per section beyond noise; inside a section pages fall into reproducible clusters (split-half agreement up to 0.91 in the stars, ~0 shuffled) made of whole leaves and conjoint leaves; in the stars quire one side of sheet f107-f112 in one cluster, the other side in the other |
| 42 | the setting belongs to the sheet | pages on the same sheet are more alike than pages facing each other in the bound book but on different sheets (−0.20, −0.36, −0.21 relative distance in herbal A, bathing, stars; intervals exclude 0), even when the two leaves are fifteen folios apart. Hint that the unit is one side of the unfolded sheet in Currier B. The sheets were written as units before binding (cf. exp. 29, Davis's singulions) |
| 43 | cipher page identity | the Naibbe cipher (fixed tables) and its plaintext give pages no identity (0% and 1%, chance 2%), against 34-73% in the manuscript. A fixed-table cipher is out; a cipher would need a key changed per sheet |
| 44 | attack: word classes from neighbours | exchange clustering, fitted on half, scored on the other: Currier B's words predict the next word's class (0.09 bits; Naibbe cipher 0.04, Latin words 0.13, copying and assembled generators 0.01-0.04), peaking at distance 1 like a language. 60% of it is the boundary glyph habit, 0.03 bits is sequence between words as such. Currier A has none: its adjacent words are as independent as random words from the page. On Naibbe the classes detect sequence but don't become the alphabet |
| 45 | labels vs their page's text | labels aren't found in their own page's text more than elsewhere (pharmaceutical 0.61 vs 0.62 per 1000; all sections p 0.10). Labels are built differently (60% o-, 1% q-), and half never occur in running text |
| 46 | where the sequence lives | the strongest link between neighbouring words is across the space: last sign → next first sign 0.25 bits in B, 0.14 in A (Latin 0.04, Italian 0.12, Naibbe cipher 0.00). Part is likely false spaces (s·aiin, o·r); the rest is a boundary rule (-y then q-, never -y then a-) |
| 47 | attack: a key per sheet? | calibrated on ciphers of Latin made of Voynich words: a new key per sheet leaves nothing pooled and a signal inside sheets (first → first 0.000 / 0.027); one key gives the same pooled and inside. The manuscript looks like one key or none (B 0.067 / 0.074). The neighbour rules are constant across sheets; only word-building is re-set. Together with 34 and 43: no calibrated cipher family fits |
| 48 | beyond the boundary | conditional on the glyphs at the space and with the sheet setting in the baseline, neighbouring words still share 0.30 bits (B) and 0.23 (A) of choices; generator 0.02, letter cipher of Latin 0.88, Latin letters 0.66. Part of it is a gallows choice held along the line; the rest falls off with distance like letters. What's left for a message is well under a letter per word |
| 49 | a setting per line? | words in the same line agree on their gallows 7-12% more than words of different lines at the same positions, flat with distance (generator: gone by distance 3). Lines are a unit, much weaker than the sheet |
| 50 | habits alone? | a generator given a setting per sheet and a favoured gallows per line, fitted to B's sheet identity and line agreement, reaches 0.12 bits beyond the boundary (B 0.30). The rest isn't repetition (the generator repeats as much as B) but structured transitions between kinds of word (B 0.028 bits start→start off-diagonal, generator −0.006), and survives removing doubtful spaces and short words (0.24 vs 0.07). First residual to survive every content-free control |

Details and caveats in `RESEARCH_LOG.md`.

## Other people's claims

`experiments/community/` reruns ideas from papers, voynich.ninja, r/voynich and other repos with the same data and controls: Greshko's Naibbe ciphertext, uncertain spaces, anagram decipherments, seasonal label prefixes, whether EVA cuts the script in the wrong places, the Bax, Greek and Turkic keys, a star-code reading, an affix parser, Sukhotin's vowels and the meaningful-text-among-filler idea. Each one has notes on what was claimed, what I expected and what came out.

## Data

Nothing third-party is committed. `python -m voynich.download` fetches:

- IVTFF transliterations from https://www.voynich.nu/transcr.html (René Zandbergen and contributors)
- historical and Wikipedia corpora from https://github.com/chirila/Voynich-public (Lindemann & Bowern)

The Cisiojanus text in `corpora/` is medieval and public domain.

Scans: Beinecke Library, Yale, https://collections.library.yale.edu/catalog/2002046

## Tests

```
python -m pytest tests
```

Run on every push (GitHub Actions).
