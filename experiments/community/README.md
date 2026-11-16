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

Also related: `experiments/08` and `10` (line-start effects; Smith 2016, Pelling), `11` (labels reused
across drawings, r/voynich "Same word, different images"), `12` (scans, with notes on the tracing
and OCR projects).

Not tested yet, and why:
- Elu-Sinhala decipherment (Zenodo 18601765, 117-star repo): needs the published vocabulary and
  transliteration rules, which are on Zenodo; will add once downloaded.
- Timm & Schinner self-citation generator: the reference implementation is a Swift iOS app; it
  needs porting before it can be scored (and it builds line-start glyphs in on purpose).
- "Middle Scots / Anglo-Saxon cursive" (r/voynich, Nov 2026): no method or mapping posted.
| c06 | r/voynich (u/Worldmaster777) | "tolor" = fertilization; o- = article, t-/k- = noun/verb, -l/-r = feminine/masculine | six other words share tolor/otolor's exact layout; no gender agreement (VMS z 0.8 vs Italian 16); t/k pairs have the most similar contexts of all, o- behaves like the control prefixes q-, y- |
