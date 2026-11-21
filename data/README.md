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
