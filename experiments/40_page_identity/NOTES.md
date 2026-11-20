# 40 — Every page has its own setting

## What I think

Exp. 39 showed the forks follow the section. Inside a section the subject still changes (a
different plant, a different bathing scene, a different star list on every page), so the next
question was whether the forks change from page to page too.

## What I did

Every page of 80+ words, in four sections of one hand each, cut into two halves (odd lines,
even lines). For each half, are the fork choices (exp. 39's 34 features, now in
`voynich/forks.py`) closer to its own page's other half than to every other page's? Then:

- **lines shuffled between pages** of the section: chance, with real lines;
- **the exp. 36 generator** (sign chain + echo of the last five words), fitted on the section,
  filling the same pages;
- **the copying model**, which copies words from its own page;
- a second version of the test that removes, from each comparison, the words the two halves
  share, so that likeness from repeating the same words can't count;
- the same test on six real texts whose subject changes from entry to entry (`languages.py`),
  with a generic profile (commonest two-letter beginnings and endings);
- the IT transliteration (Takahashi) instead of ZL.

## Result

How often a half-page's closest match is its own other half:

| | manuscript | shared words removed | lines shuffled | echo generator | copying model (shared removed) |
|---|---|---|---|---|---|
| hand 1 herbal (51 pages) | **38%** | **31%** | 2% | 2% | 29% (8%) |
| hand 2 herbal (19) | **34%** | **32%** | 6% | 4% | 55% (24%) |
| hand 2 bathing (19) | **61%** | **53%** | 5% | 7% | 55% (24%) |
| hand 3 stars (24) | **73%** | **63%** | 5% | 7% | 38% (13%) |

IT transliteration: 37%, 34%, 68%, 77% (shared removed: 27%, 29%, 58%, 67%).

Real texts, same test with the generic profile:

| | own half closest | shared words removed |
|---|---|---|
| Casebook (English medical cases) | 11% | 14% |
| Cirurgie (English surgery) | 7% | 2% |
| Secreta secretorum (Latin) | 8% | 3% |
| Picatrix (Latin) | 5% | 7% |
| Rettorica (Italian) | 7% | 4% |
| Alphabet of Tales | 4% | 4% |
| manuscript, same generic profile | 28-73% | 21-48% |

1. **Every page has an identity.** In every section a half-page picks out its own page far
   above chance (34-73% against 2-6%), with neighbours somewhat alike too (neighbour/far
   distance 0.70-0.82).
2. **It isn't from repeating words.** The copying model also gives pages an identity, because its
   pages share words; remove the shared words and that identity collapses (to 8-24%). The
   manuscript's mostly stays (31-63%). What makes a Voynich page recognisable is the way its
   forks are weighted, across all its words, not a set of words it repeats.
3. **Real texts don't do this.** Pages of a casebook, a surgery, a book of tales or Picatrix are
   barely recognisable from word shapes (4-11%, against 2-5% chance). In a language the subject
   of a page lives in a few content words; the shapes of words in general hardly move.
4. A short-memory writer (the echo generator) gives no identity at all. Whatever produces this,
   it is set once per page and held for the whole page.

## So what

This changes the reading of exp. 39. A subject in a language doesn't shift the general shape of
words; it shifts a few words. The manuscript does the opposite: the same scribe, in the same
section, re-weights the whole table at the start of each page and keeps the weights to the end
of it. That is less like writing about a different plant and more like turning a dial before
each page: a new setting per page, possibly chosen with the picture, possibly not.

It also rules something in. Whatever the procedure was, it has a state that lasts exactly a
page: a key, a setting, a starting position on a wheel, a different column of a table. A cipher
with a page key (or a generator with a page setting) produces this; a plain language doesn't,
and neither does copying.

The obvious next question: is the page setting one of a few discrete options (a dial with a
handful of positions, which would show up as clusters of pages) or a continuum?

## Caveats

- A transcriber reading ambiguous strokes the same way across a page (e.g. *ee* vs *ch*) could
  make pages look internally consistent. IT, transcribed independently, gives the same result,
  which makes this unlikely to be one transcriber's habit, but both read the same scans.
- The real-text comparison uses a generic profile, not the EVA forks. On the manuscript the
  generic profile gives slightly lower numbers than the forks (21-48% against 31-63% with shared
  words removed) but still far above the languages.
- FG (Frogguy) uses a different alphabet and the fork profile doesn't apply to it.
