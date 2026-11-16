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

Details and caveats in `RESEARCH_LOG.md`.

## Other people's claims

`experiments/community/` reruns ideas from papers, voynich.ninja, r/voynich and other repos with the same data and controls: Greshko's Naibbe ciphertext, uncertain spaces, anagram decipherments, seasonal label prefixes, and whether EVA cuts the script in the wrong places. Each one has notes on what was claimed, what I expected and what came out.

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
