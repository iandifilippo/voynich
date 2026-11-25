Downloaded data goes here (ignored by git). Run:

```
python -m voynich.download
```

Expected layout:

```
data/
  ZL3b-n.txt IT2a-n.txt RF1b-e.txt VT0e-n.txt GC2a-n.txt CD2a-n.txt FG2a-n.txt
  corpora/historical/   18 texts
  corpora/wikipedia/    294 languages
  benchmark_reference.json   (built on first use)
```

Word boxes for exp. 55 come from Rozanova and Temerev's reproduction archive (MIT licence):

```
git clone --depth 1 https://github.com/lrozanova/voynich-units /tmp/voynich-units
cp -r /tmp/voynich-units/data/voynich-units/morphometry_voynichese/voynichese_boxes data/external/voynich-units-boxes
```

Ink masks and traced row lines for exp. 57 come from the VoynichManuscriptOCR annotation project:

```
git clone --depth 1 --filter=blob:none --sparse https://github.com/daniilvaino/VoynichManuscriptOCR data/external/VoynichManuscriptOCR
git -C data/external/VoynichManuscriptOCR sparse-checkout set data img/ink_stage1
```

The glyph map for exp. 66 is Ryan Allen's download from https://ryanallen.com/voynich/research.html
(CC BY 4.0, credit "Ryan Allen, Voynich glyph map, ryanallen.com/voynich"). Unzip it so that
`data/external/glyph-map/words.tsv`, `letters.tsv` and `masks/` exist. Exp. 66 used the snapshot of
22 November 2026; the map is remade as the tracing goes on.
