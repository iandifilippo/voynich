# Research log

Newest first. Numbers come from the `results/` folder of each experiment; rerun to check.

## 2026-11-16 (11)

### c06 tolor (r/voynich)
tolor f38r.1 (paragraph-initial), otolor labels f67r2 (1 of 64) and f77v (1 of 10). 1652 types with 2-5 occurrences; 61% of paragraph-opening words unique. Same layout (opening X, label oX, 2-5 total): tolor, torain, tokol, fcheody, pairar, palar, porain. l/r agreement vs in-line shuffle: VMS z 0.85 (A 2.09 p .017, B -1.07); Italian -a/-o z 16.1; Latin -a/-us 3.1, -am/-um 4.3. Context cosine / random: o- 1.53, t/k 1.98, l/r 1.77, q- 1.50, y- 1.45.

## 2026-11-16 (10)

### 19 copying model vocabulary
extra_change q (one more substitution per word), boundary p 0.65, B, 3 seeds. q 0/0.3/0.6/0.9: hapax 0.551/0.561/0.594/0.593, MATTR 0.564/0.590/0.595/0.599 (VMS B 0.535), cohesion 1.99/1.95/1.66/1.67, near 34.0/29.1/28.9/28.6 vs null 27.9/25.3/27.1/27.2. Hapax deficit is a shape problem (too few singletons, not too little variety). Not a comma artifact: VMS hapax 0.686/0.679/0.720 split/smart/join (exp 16).

## 2026-11-16 (9)

### 18 copying + boundary habit
AutoCopy(boundary=..., boundary_p=p). Fitted list from odd-line PMI > 0. B, 3 seeds. p 0/0.5/0.65/0.8/0.95: edge 0.013/0.057/0.115/0.227/0.508, core 0.98/0.83/0.71/0.79/1.85, distance ~2.42 until 0.95 (2.97), pattern r vs even lines 0.09/0.67/0.70/0.73/0.55. Random lists p 0.8: edge 0.18, r 0.02 (max 0.16). Odd vs even VMS r 0.98, so the hold-out is weak. Remaining misses: hapax 0.55, line_last -7, line-start d/t/q.

## 2026-11-16 (8)

### 17 self-citation (Timm & Schinner)
voynich/autocopy.py: reimplemented from VoynichTextGenerator's procedure and tables (their repo has no license; procedure only). 8 seeds x A/B settings, 1400 lines. Distance 2.45 / 2.46 (sd 0.15 / 0.20), core 1.03 / 0.97. Edge 0.009 / 0.013. Hapax 0.54. h2 2.35 / 2.22. Cohesion 1.45 / 2.01. Near-repeats 36.8 vs 28.2 in-line null (B); exact 7.8 vs 8.6 (generator drops half of immediate duplicates). Worst: line_last_jsd -7.3, line_first -3.0 (B). Line-initial d/t/q too rare.

Ciphers: right words, wrong lines. Copying: right lines, wrong words. Neither gives coupling except autokey.

## 2026-11-16 (7)

### 16 commas
Parser now takes `commas="split"|"smart"|"join"`. smart = glue across `,` when the result occurs 2+ times. Tokens 38718 / 37849 / 35973. Ranks among 18 historical texts, split/smart/join: h2 0/0/0, h1 1/1/1, word_mi 0/0/0, line_first 18/18/18, line_last 18/18/18, edge_coupling 15/11/9 (0.147/0.121/0.108). Shift split→smart 0.18 units vs A-B gap 1.17. Naibbe (Greshko) core 0.94/0.80/0.89.

Correction: edge coupling is real but not extreme; exp 13 target should be ~0.12 under smart.

## 2026-11-16 (6)

### 15 repeats
Exact repeats per 1000 adjacent pairs: VMS 9.37, words shuffled within their line 9.25 (300 shuffles, p 0.42; A 0.34, B 0.55), shuffled across the text 3.42. So exact repeats = line composition. Near-repeats (edit distance 1): 36.0 vs 30.8 in-line, p < 0.003 in all/A/B. Latin and Italian avoid immediate repeats (Aix 0 vs 4.4 expected); Naibbe inherits this (1.3 vs 3.1). Repeat rate by position: first pair 3.4, middle 11.1, last 5.9. Across line breaks 6 vs 11.8 expected. Near-repeat edits: mostly insert/delete, then r<->l, k<->t, c<->s, o<->a.

Consequence for the benchmark: `repeat_rate` and `line_cohesion` partly measure the same thing.

## 2026-11-15 (5)

### 14 line-end model
Mirror of 10 for line ends. Rewrites "-e → -m/-g" for 12 endings, ZL all/A/B + Takahashi: nothing significant (97 tests); -l→-m and -n→-m strongly negative (both partners favoured). Stem-level pooled test (stem+{r,l,s,n,in,iin,y,dy} vs stem+m): r −0.29 to −0.02, p 0.60-0.98. Line-final words shorter (4.73 vs 4.96 internal, 5.43 first). am ×23, dam ×12, otam ×12 at line end; al ×1.0, ar ×0.55, aiin ×0.61. Line start = rewrite, line end = selection/special forms.

### 13 autokey Naibbe
Reimplemented Naibbe from Greshko's tables; matches his ciphertext (h2 2.11/2.09, hapax 0.59/0.58, edge 0.004/0.004).

Autokey (last glyph of the previous word picks the next table from a fixed chart, with probability p): edge coupling 0.006 / 0.08 / 0.15 / 0.37 at p = 0 / 0.5 / 0.65 / 1; nothing else moves. p ≈ 0.65 matches the VMS for Pliny and Dante.

Pattern of coupling (PMI of last glyph x next initial): VMS odd vs even lines 0.98; random charts 0.00 (best 0.16); chart fitted on odd lines → simulated cipher vs even lines 0.43 (Pliny), 0.24 (Dante). Partial.

VMS coupling is not a comma artifact: 0.166 bits across certain spaces only (0.411 across uncertain ones).

Benchmark distance: 4.86 (published Naibbe) → 4.78 (+autokey) → 3.92 (+autokey + line-start rule, q=0.5). Untouched: line_last, repeat_rate, line_cohesion.

Bug on the way: a chart object that subclassed an empty dict was replaced by the default chart (`chart or DEFAULT`), so the first chart search returned nonsense (-0.04). Fixed (`is None`); the quick check done earlier outside the experiment had it right (0.47).

## 2026-11-15 (4)

### community tests (experiments/community)
Reran five outside claims with our data and controls; full notes in each folder.

- **c01 Naibbe (Greshko's own ciphertext).** Core distance 0.94, about as far from the reference as Currier B is (0.71); my reimplementation in 05 was 2.22, so that one was my fault. h2 2.09 matches. Misses: edge coupling 0.002 vs 0.18, hapax 0.58 vs 0.68. One-word-at-a-time ciphers can't produce coupling across word boundaries.
- **c02 uncertain spaces (Rozanova & Temerev).** Gluing across `,` gives a known word 33.7% of the time vs 3.7% for `.` and 82.8% for real word-internal cuts; edge MI 0.55 vs 0.16 and 1.70. Implies ~38% of commas are word-internal. Partly right.
- **c03 anagram decipherments.** With a 30k-word Italian vocabulary, random strings of 4-9 letters anagram into one or two Italian words 75-90% of the time; Voynich words through an arbitrary key 83-99%. A successful anagram is expected from noise.
- **c04 seasonal label prefixes (voynich.ninja 5817).** Prefix mix differs between signs (chi-square p < 0.001) for labels and also for ring text (p = 0.001). Ordered trend through the year: rho -0.60, p = 0.08. Page effect, not a season effect.
- **c05 re-cutting EVA.** Byte-pair merging: VMS h2/log2(alphabet) goes 0.46 → 0.56 → 0.53 (0, 40, 120 merges) while Latin/Italian/English fall from 0.64-0.70 to 0.53-0.57. They meet around 100-150 units, where a VMS word is ~1.8 units (natural texts 2.4-3.4). Looks like a syllabary or code, not a mis-cut alphabet.

### 12 scans
PDF scans of quire 20 (~1100x1536 px). Line detector tuned on alternate pages: held-out MAE 3.2 lines, within ±1 on 7/11; fails on f112r (damaged leaf), f104r skipped (half resolution). Space test on 187 lines: b/a 1.0-1.4 across thresholds but CI roughly 0-4. Inconclusive at this resolution.

## 2026-11-15 (3)

### correction on 08
Line-initial s is not new. Emma May Smith described a "linestart transformation" (Agnostic Voynich, 2015-2016: s, d, y added or swapped in at line start, sa-/so- words strongly line-initial esp. in Q20); Nick Pelling has long called line-initial s a likely null; voynich.ninja threads 2945, 4343 and 5309 cover it. 08 is a replication.

### 10 linestart model
Testing Smith's mechanism directly. For every word type x with 5+ line-internal uses: deficit(x) = how much rarer x is at line start than expected, surplus(g+x) = how much commoner g+x is there. If g+x at line start stands for x, the two should correlate across x.

| glyph | r (all) | p | Currier A | Currier B | Takahashi |
|---|---|---|---|---|---|
| s | 0.130 | <0.001 | 0.047 (ns) | 0.124 (<0.001) | 0.116 (<0.001) |
| d | 0.158 | <0.001 | 0.015 (ns) | 0.168 (<0.001) | 0.143 (0.001) |
| t | 0.097 | <0.001 | 0.021 (ns) | 0.101 (<0.001) | 0.102 (<0.001) |
| p | 0.070 | 0.007 | ns | 0.067 (0.019) | 0.077 (0.005) |
| y, q, k, l, r, o | negative or ns | | | | |

40 tests, so only p < 0.00125 counts: s, d, t survive, p doesn't. Strongest pairs: s+ain, s+aiin, s+ol, s+ar; d+aiin, d+ain, d+shedy; t+ol, t+chedy.

Reading: in Currier B, s/d/t at line start behave like something added to an ordinary word. y does not (Smith already suggested y replaces ch rather than being added). Nothing like this in Currier A. The correlations are modest: plenty of line-initial g-words are not g + a known word.

As far as we found, nobody has tested the transformation this way (deficit vs surplus with a permutation null). Needs a proper literature check before claiming it.

### 09 bifolia (singulion hypothesis)
101 leaves with 60+ words, pairs inside each quire, same scribe and same illustration type only. Conjoint leaves (same bifolium) vs other pairs:

- raw cosine: +0.022 vs -0.017 under random re-pairing, p = 0.002, higher in 9/10 quires
- tf-idf cosine: p = 0.53
- Jaccard without the 50 most common words: p = 0.43

So conjoint leaves share their common-word profile (which could be the scribe's state or the session) but not specific vocabulary. Suggestive at most. Not evidence for or against singulions on its own.

### 04 again, with better measures
Same-leaf (recto→verso) vs cross-leaf (verso→next recto): tf-idf cosine 0.116 vs 0.085 (p = 0.015), rare-word Jaccard 0.094 vs 0.068 (p < 0.001). This one holds: the two sides of a leaf share specific vocabulary more than pages that face each other across leaves. Still needs a baseline from a manuscript we know is bound correctly.

### 11 label reuse
758 single-word labels, 634 distinct, 63 repeated on 2+ pages, 49 of those across sections (e.g. otaly on 7 pages: zodiac, biological, pharmaceutical; otaldy on f70v2, f88r, f101v). Same-section share of repeat pairs 30.8% vs 22.6% when sections are shuffled (p = 0.009). Mostly short ot-/ok- forms, many rare in running text. Looks more like a stock of label words than unique names. Full list in results for checking against the scans.

## 2026-11-15 (2)

### parser fix
`{...}` in IVTFF are ligatures (`{ckh}`, `{cth}`, `{ikh}`), not comments. The first parser dropped them. Comments are `<!...>`. All numbers below use the fixed parser, so they differ slightly from entry (1).

### 08 line positions
Some frequent words almost only appear at the start of a line (dshedy 29/32, tchedy 25/34, pol, tol, sol, sor, sain, saiin). With shuffled words no top-300 word gets above a 3.4x ratio; these reach 4-8x.

Many look like a normal word with one glyph in front: d+shedy, t+chedy, s+ol, s+ain. Measured: removing the first glyph turns 60.6% of line-initial words into one of the 500 most common words, vs 40.4% of line-internal ones. Almost all of that comes from **s**: 52.4% at line start vs 7.7% mid-line (599 vs 3291 words). d, t, y show small differences.

Reading: line-initial s- behaves like something added to the word because it is at the start of the line. Next: check whether the stripped word is the one that *would* be expected there (e.g. compare with the last word of the previous line), and look at p/f in the same way.

### 07 word structure
Glyph positions inside words are far more fixed than in any comparison text: positional entropy 0.70 (A 0.71, B 0.63) vs 0.83-0.93 for Latin, Italian, Spanish, English, Icelandic, Hebrew, Georgian. Inside-word conditional entropy 2.13 vs 2.98-3.78. Same with Glen Claston's alphabet (0.72, 2.65), so it isn't an EVA artifact.

### 06 zodiac labels
Labels taken in ZL order (each has a clock position). 10 signs, 30 labels each (Gemini 29, Aries and Taurus split across two pages).

- **Cisiojanus (Pelling's idea)**: aligned label i with syllable i of that month's Cisiojanus, calendar month and sign span (21st to 20th), both reading directions. Mantel test of label similarity vs syllable similarity: 2 of 40 at p<0.05, which is what chance gives. **Null.** The Cisiojanus file syllabifies to exactly 365 syllables (31, 28, 31...), so it isn't a counting problem.
- **Position as number**: same-position labels across signs are slightly more alike by bigram Jaccard (+0.005, p=0.043), but nothing with prefix, suffix, first glyph or length (p 0.17-0.99). **Not robust**, treat as nothing.
- ot- share by sign: high in spring (Aries 73%, Pisces 53%), low in summer/autumn (Cancer 7%, Virgo 7%). Known already.

### 05 cipher benchmark
13 metrics, z-scored by the spread across 18 historical texts. VMS reference = first 10k paragraph words of ZL (mostly Currier A herbal, so "VMS Currier A" overlaps the reference and its 0.32 is optimistic; "later pages" at 1.04 and "Currier B" at 1.23 are the honest floor).

- Every cipher/generator: distance 5-6. Shuffled VMS words: 4.5. Nothing gets close.
- The four line metrics (line-start/end distributions, repeats, cohesion) are what nothing reproduces. Without them ("core"), plain Italian (1.69) is still closer than any cipher (2.06+).
- Verbose, syllable and Naibbe-like ciphers do reach VMS h2 (2.12-2.28) but lose the open vocabulary (hapax 0.22-0.41 vs 0.68) and edge coupling (~0 vs 0.15). Same conclusion as Rozanova & Temerev (2026) for published imitations.
- My self-citation generator is far too repetitive (cohesion 5-14). It's a crude version, not Timm & Schinner's. Next: run their actual generator (TorstenTimm/VoynichTextGenerator).
- My Naibbe-like cipher is my reading of the idea, not Greshko's tables.

### 04 page order
225 pages with 40+ words. Mean cosine between consecutive pages 0.366, random 0.217, shuffled within same hand and illustration type 0.314 (both p<0.0005). So the current order keeps real local structure.

Recto→verso of the same leaf (can't be separated by rebinding): 0.415, n=98. Verso→next recto: 0.329, n=99. Difference p=0.0006. Fits Layfield & Davis (2026): joins between leaves are weaker than inside a leaf. Caveat: the two sides of a leaf may have been written in one sitting even in a correct order. Need a baseline from a normal manuscript, and to redo this per singulion.

Weakest joins listed in results (f68r1→f68r2, f24v→f25r, f67v1→f68r1...).

### 03 scribes and Currier languages
Hand 1: 10,749 A / 0 B. Hand 2: 0 / 11,128. Hand 3: 750 / 10,908. Hands 4, 5: only B where marked. Closest vocabularies: hands 2-3 (JSD 0.27). Most distant: 1-5 (0.61). Marker words: hand 1 daiin, chol, chor, cthy; hand 2 shedy, qokedy, qol; hand 3 qokeey, al, lkaiin; hand 4 oteody, oteos.

### 02 languages
283 texts (265 Wikipedia + 18 historical) after dropping 28 whose script my tokenizer breaks into 1-glyph "words" (Brahmic scripts, Thaana, pointed Hebrew...). **None has h2 at or below the VMS (2.15).** Lowest: Sranan 2.59, Hakka 2.69, Venda 2.79. Even the GC transliteration (2.57) is below all of them. Nearest on six metrics combined: Venda, Tswana, Malagasy, Maori, Samoan — CV-syllable languages, but still far off on h2.

### 01 transliterations
Seven files, first 8000 paragraph tokens. EVA family (ZL, IT, RF, VT) agree closely (h2 2.148-2.151). Bigger-unit alphabets push h2 to 2.40-2.57: still under every natural text. Line-start effect 0.11-0.16 and cohesion 1.7-1.9 in every file. These are properties of the manuscript, not of the transcriber.

### 00 baseline
227 pages, 5,385 loci, 38,718 legible tokens, 8,048 types, 308 tokens dropped for uncertain glyphs. q word-initial 99.4%, then o 97.7%. p+f: 41.8 per 1000 glyphs on paragraph-first lines vs 2.7 elsewhere. Hapax 0.68, h2 2.11 on paragraph text.

By scribe: hand 3 has the strongest line-start effect (0.30), hand 4 the weakest (0.11).

## 2026-11-15 (1)

First pass with a simple parser. Baseline numbers matched Currier, Bennett, Zandbergen. h2 far below Latin/Italian means plain monoalphabetic substitution of either is out. Started the zodiac work.

## Next

- run Timm & Schinner's generator and Greshko's actual Naibbe tables through the benchmark
- benchmark metric from Zhang & Sheng: same-line word-pair tendency across 28 texts
- leaf test against a baseline from a manuscript we know is bound correctly
- check the cross-section repeated labels against the drawings
- glyph tracings (Trace the Voynich) once released: stroke-level stats
- f116v glyphs vs the main text's slot rules
- web explorer (GitHub Pages)
- parser option: decide each `,` by whether the glued form is a known word (c02), rerun benchmark
- port Timm & Schinner's generator from Swift and score it
- autokey: co-fit chart and tables on held-out lines; line-end and repeat mechanisms
- Elu-Sinhala claim once the Zenodo vocabulary is downloaded
- full-resolution scans + word alignment for the space question
