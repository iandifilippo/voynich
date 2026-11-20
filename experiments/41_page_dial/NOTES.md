# 41 — The page setting: how many knobs, and does it click?

## What I did

Page fork profiles (pages of 80+ words), standardised. Two questions:

- **How many independent knobs?** Principal components, keeping only those larger than with
  lines shuffled between pages (parallel analysis).
- **Discrete or continuous?** k-means on the odd-line halves, then each even-line half is put in
  the nearest cluster. If pages come in k kinds, the two halves agree (adjusted Rand index)
  far above shuffled lines.

## Result

| | pages | real components | split-half agreement, k = 2 / 3 / 4 / 5 (shuffled: ~0) |
|---|---|---|---|
| Currier A, hand 1 | 67 | 6 | 0.29 / 0.55 / 0.55 / 0.35 |
| Currier B, hands 2 and 3 | 69 | 3 | 0.89 / 0.59 / 0.73 / 0.33 |
| hand 1 herbal only | 51 | 3 | 0.00 / 0.66 / 0.53 / 0.30 |
| hand 2 bathing only | 19 | 4 | 0.60 / 0.69 / 0.60 / 0.47 |
| hand 3 stars only | 24 | 3 | 0.83 / 0.84 / 0.85 / 0.91 |

Across Currier B the clusters are the sections (stars, bathing, herbal), as exp. 39 found.
More interesting is *inside* a section: the clusters are reproducible from half a page, and they
are made of physical units. Stars, k = 2:

- f104r/v, f105r/v, f106r/v, f107r, f112v, f113r/v, f114r/v, f115v (+ f58r/v)
- f103r/v, f107v, f108r/v, f111r/v, f112r, f116r

Recto and verso of a leaf go together; so do conjoint leaves (f103 with f116, f108 with f111,
f105 with f114, f106 with f113); and in the sheet f107|f112 one side (f107v + f112r) sits in one
cluster and the other side (f107r + f112v) in the other. Hand 1's herbal pages split the same
way (f3 with f6, f18 with f23, f17 with f24, f20 with f21...).

Three components carry the setting in each section; the first, in Currier B, trades *qo-*,
*-edy* and *-ol* against *a-*, *-ar* and *-dy*.

## So what

The setting isn't one dial with a few positions for the whole book; it's a few knobs, and inside
a section it comes in groups that follow the sheets. Exp. 42 tests that directly.
