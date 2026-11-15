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
- **`experiments/`** – each one is a `run.py` plus its `results/`
- **`docs/`** – state of the field, notes on f116v, GitHub landscape
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
| 04 | page order | neighbouring pages share vocabulary beyond hand + topic (p < 0.0005), but joins across leaves are weaker than recto→verso of the same leaf (0.33 vs 0.42, p = 0.0006), consistent with a disturbed binding |
| 05 | cipher benchmark | no cipher or generator reproduces the line effects; ciphers that reach VMS-level h2 lose the open vocabulary (hapax 0.22-0.41 vs 0.68) and edge coupling |
| 06 | zodiac labels | Cisiojanus alignment: null (2/40 tests at p<0.05, chance level). Position-as-number: not robust |
| 07 | word structure | glyph position inside words is far more fixed than in any comparison text (positional entropy 0.70 vs 0.83-0.93) |
| 08 | line positions | line-initial words starting with *s* are a common word plus *s* 52% of the time vs 8% mid-line |

Details and caveats in `RESEARCH_LOG.md`.

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
