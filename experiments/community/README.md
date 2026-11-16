# Testing other people's claims

Ideas from papers, voynich.ninja, r/voynich and other repos, rerun here with the same data and
the same controls as everything else. Each folder has `NOTES.md` (what was claimed, what I
expected, what I did, what came out), a `run.py`, and `results/`.

| | claim | source | verdict |
|---|---|---|---|
| c01 | Naibbe cipher reproduces VMS statistics | Greshko 2025, Cryptologia; his ciphertext | close on word-internal stats; no edge coupling between words, less open vocabulary |
| c02 | uncertain spaces behave like word-internal breaks | Rozanova & Temerev 2026, arXiv | partly: ~38% of them do, the rest look like real spaces |
| c03 | f99r labels are Italian anagrams | Zenodo 20109175, May 2026 | any string anagrams into 1-2 Italian words 75-99% of the time; no evidential value without a stronger test |
| c04 | zodiac label prefixes cluster by season | voynich.ninja thread 5817 | signs differ, ring text too; no ordered seasonal trend (p = 0.08) |
| c05 | EVA is the wrong unit (multi-glyph units / stroke particles) | Rozanova & Temerev 2026; r/voynich "Is it too late to rethink EVA?" | merging glyphs into ~150 units brings entropy in line with natural text, but words are then 1-2 units long: syllabary/code-like, not a mis-cut alphabet |
| c06 | "tolor" = fertilization; o- = article, t-/k- = noun/verb, -l/-r = feminine/masculine | r/voynich, u/Worldmaster777 | six other words share the exact tolor/otolor layout; no gender agreement (VMS z 0.8, Italian 16); t/k pairs have the most similar contexts of all; o- behaves like the control prefixes q-, y- |
| c07 | Bax's 14 sound values (kantairon, kaur, taurn...) point to a Near Eastern language | Bax 2014, stephenbax.net | his key beats its own shuffles in Turkic/Iranian/Arabic lexicons, but a Naibbe cipher of Latin does too, more strongly: glyph statistics, not language |
| c08 | f67r1 line 1 is Byzantine Greek; the script merges voiced and voiceless sounds | voynich.ninja, G. Caveney | merging those letters lowers h2 by 0.1 bit (gap to the VMS: 1 bit); his values allow 8192 readings of the line; 31% of words read as Greek vs 13% shuffled, but the copying model gives 30% |
| c09 | Old Turkic sound values (Ata Team 2018) | voynich.ninja listing of the team's video | 20% of words read as Turkic vs 7% shuffled; copying model 20%, Naibbe cipher of Latin 17%. m = k and q = d ignore that 70% of -m end a line and 99% of q start a word |
| c10 | no language: an astronomical code (o = degree, q = rising, e-runs = Moon days, gallows open paragraphs) | voynich.ninja, A. García Jiménez | q before o: true (98%). Gallows: only p and f belong to first lines; 3.4% of gallows open a paragraph. e-runs stop at 4. Repeats are not commoner in the stars section |
| c11 | do the two occurrences of a doubleton sit together? | voynich.ninja, DG97EEB / R. Sale | same page 3.9% (2.7× chance), same sheet 11.7% (2.0×); two thirds are more than 20 pages apart |

Also related: `experiments/08` and `10` (line-start effects; Smith 2016, Pelling), `11` (labels reused
across drawings, r/voynich "Same word, different images"), `12` (scans, with notes on the tracing
and OCR projects).

Not tested yet, and why:
- Elu-Sinhala decipherment (Zenodo 18601765, 117-star repo): needs the published vocabulary and
  transliteration rules, which are on Zenodo; will add once downloaded.
- Timm & Schinner self-citation generator: now reimplemented and scored in `experiments/17-19`.
- "Middle Scots / Anglo-Saxon cursive" (r/voynich, Nov 2026): no method or mapping posted.
