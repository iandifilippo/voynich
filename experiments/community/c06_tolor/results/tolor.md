# c06 'tolor' = fertilization

## A. the occurrences

| page | locus | unit | position | word | line |
|---|---|---|---|---|---|
| f38r | f38r.1 | P | 0 | tolor | tolor chockhy oky choiin okshol oly oky |
| f67r2 | f67r2.62 | L | 0 | otolor | otolor |
| f77v | f77v.4 | L | 0 | otolor | otolor |

`unit` P = paragraph text, L = label.

## B. look-elsewhere

1652 word types occur 2-5 times. 61% of paragraph-opening words occur nowhere else. Paragraph-opening words X (4+ glyphs) for which oX also exists somewhere: 116. Same layout as tolor/otolor (X opens a paragraph, oX is a label, 2-5 occurrences in all):

| opening word | label | substring count |
|---|---|---|
| tolor | otolor | 3 |
| torain | otorain | 2 |
| tokol | otokol | 2 |
| fcheody | ofcheody | 4 |
| pairar | opairar | 2 |
| palar | opalar | 2 |
| porain | oporain | 2 |

## C. do -l / -r endings agree like gender?

| text | pairs | log_odds | null | z | p_agree |
|---|---|---|---|---|---|
| VMS paragraphs, -l vs -r | 3254 | 0.451 | 0.395 | 0.848 | 0.196 |
| VMS Currier A, -l vs -r | 1390 | 0.644 | 0.445 | 2.092 | 0.017 |
| VMS Currier B, -l vs -r | 1807 | 0.250 | 0.341 | -1.072 | 0.870 |
| VMS paragraphs, -y vs -n (control) | 10803 | 0.073 | 0.338 | -6.665 | 1.000 |
| Italian (Rettorica), -a vs -o | 3597 | 1.479 | 0.576 | 16.098 | 0.003 |
| Latin (Aix), -a vs -us | 819 | 1.228 | 0.850 | 3.074 | 0.003 |
| Latin (Aix), -am vs -um | 563 | 1.591 | 0.821 | 4.293 | 0.003 |

Positive log odds above the within-line null = neighbours tend to share the ending.

## D. contexts of minimal pairs

| pairs | n | context_cosine | random_matched | ratio | examples |
|---|---|---|---|---|---|
| X / oX (o- as article) | 92 | 0.134 | 0.088 | 1.531 | daiin/odaiin, chedy/ochedy, aiin/oaiin, ar/oar, s/os |
| tX / kX (t noun, k verb) | 98 | 0.188 | 0.095 | 1.983 | otaiin/okaiin, otedy/okedy, otar/okar, otal/okal, oteey/okeey |
| Xl / Xr (feminine / masculine) | 63 | 0.196 | 0.111 | 1.773 | ol/or, chol/chor, al/ar, dal/dar, qokal/qokar |
| X / qX (control prefix) | 73 | 0.159 | 0.106 | 1.499 | ol/qol, or/qor, okaiin/qokaiin, okeey/qokeey, o/qo |
| X / yX (control prefix) | 44 | 0.112 | 0.078 | 1.447 | daiin/ydaiin, chedy/ychedy, chol/ychol, chey/ychey, shey/yshey |

Cosine of left/right neighbour counts (paragraph text, words with 8+ occurrences). `random_matched`: the first word against random words of similar frequency.
