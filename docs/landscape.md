# Who is working on what (Nov 2026)

Snapshot taken 2026-11-15. Sources at the bottom.

## Academic

- **Voynich 2026 conference**, University of Malta, online, 9 Dec 2026. Chair Colin Layfield, co-chair John Abela. Programme committee includes Claire Bowern (Yale), Luke Lindemann, Rafał Prinke, René Zandbergen. Topics: history, computational text analysis, image processing, hoax/language/cipher question, digital humanities. *"Proposed solutions will not be accepted."* Follows the 2022 edition (CEUR vol. 3313).
- **Layfield & Davis (2026), "Singulion Structure and the Voynich Manuscript"**, Digital Medievalist 19, doi:10.4000/16k0a. The book was probably made of singulions (single folded bifolia) and later bound in the wrong order by someone who couldn't read it. Evidence: scribal hands alternating in ways that make no sense, drawings that continue on far-away pages, asymmetric stains, LSA similarity between pages. See our `experiments/04_page_order` and `26_writing_order` (a sequence test that agrees for scribes 2 and 3 and not for scribe 1), and `42_setting_unit`: the way words are built on a page is shared by the two leaves of the same sheet even when they are far apart in the binding, more than by pages that face each other in the binding but belong to different sheets.
- **Layfield, "The Application of Latent Semantic Analysis to the Voynich Manuscript"** (May 2026). Coherence and flow of the text with LSA.
- **Greshko (2025), "The Naibbe cipher"**, Cryptologia, doi:10.1080/01611194.2025.2566408. A verbose homophonic cipher, doable by hand with dice and cards, that turns Latin/Italian into text matching many VMS statistics at once. Author says it is almost certainly not how the VMS was made; proposed as a benchmark. Fails on parts of Currier B.
- **Rozanova & Temerev (Aug 2026), "A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space"**, arXiv:2608.17096. Using ZL: glyphs behave like recurring multi-glyph units, consecutive tokens share <1% of entropy (2-10% in controls), glyphs at token edges are coupled, uncertain spaces behave like word-internal breaks. Imitations (a published cipher and a generator) match low entropy but miss edge coupling and the rare-word-heavy vocabulary (70% singleton types vs 41% / 59-60%).
- **Schwartz (Oct 2026), "How the Voynich Manuscript was written"**, preprint on the author's site, marked preliminary. A keyless procedure fitted to scribes 1 and 2: frequency-weighted reuse of the scribe's own words (73-77%), verbatim local copying (2-5%), coinage from letter habits (18-25%). Timm & Schinner's process is too local (copy rate 0.42-0.48 against 0.28/0.38). No keyless generator reproduces the word-boundary coupling. Faint subject dependence in the astronomical and balneological sections, none in the herbal. See our `experiments/18`, `20-22`, `27`.
- **Zhang & Sheng (Oct 2026), "Does the Voynich Manuscript Mean Anything? Calibrated Tests Find Little Trace of Language"**, arXiv:2610.34499. Hypotheses written as page-generating programs with equal fitting budgets. Word statistics can't decide between self-citation and dialect-switching ciphers. Same-line word-pair tendency is half as strong as the weakest of 28 texts in 16 languages. Solvers find no readable text under letter ciphers, word codes or 28 syllable codes. Not excluded: a heavily miscopied nomenclator with a second key.
- Background: Lindemann & Bowern, character entropy corpora (arXiv:2010.14697); Bowern & Lindemann (2021) "The Linguistics of the Voynich Manuscript"; Davis (2020) five scribes; Gaskell & Bowern (2022) hoaxing experiments; Timm & Schinner self-citation.

## Community

- **voynich.ninja** is where the serious discussion happens. Biggest boards: Analysis of the text (725 threads / 15.9k posts), Imagery (655 / 15.3k), Theories & Solutions (367 / 14.5k, with a "Slop Bucket" subforum). Recent active topics include alternative early page orderings from physical damage, liaisons in the text, f116v, Horčický's books and zodiac degree works.
- Zodiac labels specifically: 30 nymphs/labels per sign is widely read as degrees rather than days (Zandbergen); counts don't always match (one diagram: 30 nymphs, 30 labels, 29 stars, 28 left arms); ot-/ok- overrepresentation in labels is well known (Zandbergen, Pelling); Pelling suggested the labels might hold Cisiojanus syllables. We tested that in `experiments/06_zodiac`: null.
- Line-start effects: Emma May Smith (Agnostic Voynich blog, 2015-2016) on the "linestart transformation"; Nick Pelling on line-initial s as a possible null; voynich.ninja threads 2945, 4343, 5309. See `experiments/08` and `10`.
- Glyph tracing: Ryan Allen's "Trace the Voynich" (ryanallen.com/voynich), pixel-level tracings of the whole manuscript checked by volunteers; glyph map, OCR and font announced. Kraken (kraken.re) is the obvious open HTR engine if we ever build our own transcription from the scans.
- **r/voynich** (Reddit): pinned post is the Malta conference. Recent front page: single-language claims ("Language: Middle Scots. Alphabet: Anglo-Saxon cursive", 13 Nov 2026), label reuse across drawings ("Same word, different images"), the tracing project, and whether EVA should be replaced by a stroke-level alphabet ("Is it too late to rethink EVA?").
- **voynich.net forum** and others keep receiving "SOLVED" threads (e.g. a volvelle/"industrial codex" claim, Jan-Feb 2026), usually answered with the same checklist: readable text that matches the drawings, reproducibility, peer review.
- **Tools posted on voynich.ninja's Software board (2025-2026)**: *VAIS* (VoyBear, vineyardcode.github.io/vais), 144 reproducible tests with pre-registered kill criteria, a calibrated control battery (Latin/Italian, period ciphers, Rugg grille, Timm self-citation) and a verdict ledger in which most entries are killed hypotheses; the closest thing to this repository, and worth checking before claiming any result as new. *pykeedy* (pwspen/pykeedy), a Python loader with filtering, n-gram/entropy/position statistics and a Naibbe encoder/decoder. *voynich-claims* (vosreth), ~20 000 forum claims extracted and indexed by folio. *Voynich Scout / voynichviewer.com*, a 3D model of the book in its current binding and in Davis's singulion order (scribe changes from leaf to leaf: 31 bound, 22 in her order; in her order f75v faces f84r). bi3mw's affix parser (tested in `community/c12`). Blasto (Merricx/blasto), a hill-climbing solver for simple substitution and turning grilles with English/German/Spanish quadgrams: the same family as exp. 31. pykeedy and VAIS overlap with exps. 23 and 34 here.
- **Other undeciphered material discussed alongside**: a proposed logographic reading of ~60% of the Rohonc Codex as a constructed religious language; Giovanni Fontana's *Bellicorum instrumentorum liber* (Venice, 1420-1430), whose captions use an invented alphabet that is plain Latin by simple substitution, a reminder that the commonest "cipher" of the period is the one exp. 31 rules out for the manuscript.
- **YouTube**: Voynich Talk (Koen Gheuens). "The part of the Voynich Manuscript we CAN read (f116v)", 6 Dec 2025, ~214k views, 23 min. See `docs/f116v.md`.

## GitHub

599 repositories match "voynich" (summary in `docs/github_landscape.json`). Total stars across all of them: 717.

| year created | repos |
|---|---|
| 2014-2023 | 130 |
| 2024 | 31 |
| 2025 | 88 |
| 2026 | 342 |

By a keyword heuristic on descriptions, ~70 of the 2026 repos announce a decipherment/translation. Only 13 repos have 10+ stars and 3 have 50+.

| repo | stars | note |
|---|---|---|
| brianmg/voynich-nlp-analysis | 130 | NLP analysis |
| okesipoke/manuscript-phoneme-decipher | 117 | Elu-Sinhala decipherment claim (2026) |
| lizadaly/nanogenmo2014 | 112 | generated fake Voynich (art project) |
| voynichese/voynichese | 30 | old code.google export |
| chirila/Voynich-public | 16 | Lindemann & Bowern corpora (we use these) |
| YaleDHLab/voynich | 12 | computer vision |
| mzattera/v4j | 12 | Java library, actively maintained |
| danielgaskell/voynich | 8 | Gaskell & Bowern hoax experiments |
| TorstenTimm/VoynichTextGenerator | 8 | self-citation generator |
| noah-chelednik/voynich-data | 9 | data infrastructure (2026) |

What's missing in that list, and what this repo tries to be: a small, dependency-free Python package that loads every transliteration the same way, a benchmark any proposal can be scored against, comparison corpora wired in, and experiments that report their nulls.

## Sources

- https://vineyardcode.github.io/vais/
- https://github.com/pwspen/pykeedy
- https://github.com/vosreth/voynich-claims
- https://voynichviewer.com/
- https://github.com/Merricx/blasto
- https://www.um.edu.mt/events/voynich2026/about/
- https://journals.openedition.org/digitalmedievalist/2331
- https://www.livescience.com/archaeology/undeciphered-voynich-manuscript-may-have-been-bound-out-of-order-study-finds
- https://www.researchgate.net/publication/405027080_The_Application_of_Latent_Semantic_Analysis_to_the_Voynich_Manuscript
- https://www.livescience.com/archaeology/mysterious-voynich-manuscript-may-be-a-cipher-a-new-study-suggests
- https://arxiv.org/abs/2608.17096
- https://arxiv.org/abs/2610.34499
- https://arxiv.org/abs/2010.14697
- https://voynich.ninja/
- https://www.reddit.com/r/voynich/
- https://voynich.net/forum/viewtopic.php?p=782
- https://www.youtube.com/watch?v=JnGBl5usAMM
- GitHub search API, `q=voynich`, 2026-11-15
