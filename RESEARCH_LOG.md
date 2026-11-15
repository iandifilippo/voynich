# Research log

## 0. Baseline (2026-11-15)

Sanity check of the parser against known numbers. ZL transliteration, 5385 lines, 38744 legible words, 7861 types (5378 hapax).

- top words: daiin 850, ol 564, aiin 507, chedy 507, shedy 434
- h1 3.87, h2 2.14 bits
- q is word-initial in 99.4% of words that contain it, followed by o 97.8%
- first word of a line starts with a gallows 21.8% (6.1% elsewhere)
- last word of a line ends in m 15.3% (0.9% elsewhere)
- p/f: 41.3 per 1000 chars on paragraph-first lines vs 2.6 on other lines
- 304 immediate word repeats, 12 triples

Currier A vs B, per 1000 words: chedy 0.1 / 20.7, qokeedy 0.0 / 12.8, chol 24.1 / 4.1, cthy 8.2 / 0.3

Words overrepresented by section: zodiac oteos x15, oteody x11; pharma qokeol x7.6; cosmo otody x8.1; bio olkain x4.7

All consistent with Currier, Bennett, Zandbergen.

h2 is way below Latin/Italian (3+). Simple substitution keeps h2 the same, so plain monoalphabetic substitution of Latin or Italian is out.

(These numbers came from a first pass; basic_stats.py treats `*` slightly differently so expect small differences.)

## 1. Zodiac labels vs calendar (open)

The zodiac pages are the only place where readable text (month names in the margins) sits next to Voynichese.

- ~30 nymphs per sign, one label each (Aries and Taurus split into two pages of ~15)
- 23% of zodiac words start with ot- vs 6% elsewhere (already noted by Zandbergen and Pelling)
- open question: are the 30 figures days or degrees?

Ideas to test:
- labels as syllables of a Cisiojanus (Pelling's suggestion, never tested properly as far as I can find)
- labels as day/degree numbers: should see repeated structure at the same position across months
- labels as saint/star names: fixed feasts (25/12, 24/6...) should stand out

TODO
- [x] extract labels with page/sign/month/order
- [ ] check nymph reading order on the scans
- [ ] check page -> sign -> month mapping on the scans
- [ ] get 15th c. Latin and German Cisiojanus texts
- [ ] metrics + shuffle control
