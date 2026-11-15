# Research log

Newest first. Numbers come from the `results/` folder of each experiment; rerun to check.

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
- line-initial s-: is the stripped word predictable from context?
- page order per singulion, against a baseline from a normally bound manuscript
- f116v glyphs vs the main text's slot rules
- web explorer (GitHub Pages)
