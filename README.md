# voynich

Working on the Voynich Manuscript (Beinecke MS 408). The goal is to actually read it.

Every idea gets tested against shuffled/random text before it counts for anything, and dead ends stay in the log.

## Running

Python 3.9+, no dependencies.

```
python scripts/download_data.py
cd scripts
python basic_stats.py
python zodiac_labels.py
```

`download_data.py` pulls the Zandbergen-Landini transliteration (ZL, IVTFF format) from voynich.nu. It's not redistributed here.

## Files

- `scripts/ivtff.py` – IVTFF parser
- `scripts/basic_stats.py` – baseline stats
- `scripts/zodiac_labels.py` – zodiac labels by page/month
- `RESEARCH_LOG.md` – notes and results

## Credits

- ZL transliteration: René Zandbergen & Gabriel Landini, https://www.voynich.nu/transcr.html
- Scans: Beinecke Library, Yale, https://collections.library.yale.edu/catalog/2002046
