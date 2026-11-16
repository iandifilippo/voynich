# c07 Bax's sound values on the rest of the text

Words written only with Bax's 14 signs: 11665 of 38718 tokens (30%). Each is reduced to its consonant skeleton (K N T R X S); lexicon words are reduced the same way, per script.

His own words under his key:

| word | skeleton | in_text |
|---|---|---|
| kydainy (f2r, 'kantairon') | KNTRN | 1 |
| koaiin (f3v, 'kaur') | KR | 1 |
| oror (f16r, 'arar') | RR | 8 |
| dary (f68r1.6, 'taurn'; Bax saw doary) | TRN | 23 |

Most common skeletons the key produces: R ×1844, TR ×1741, KR ×921, XTN ×674, XN ×546, KN ×519, KTN ×481, S ×450, SR ×395, TN ×367, N ×339, XR ×296, RR ×275, X ×255, ∅ ×222

## summary: does Bax's assignment beat its own shuffles?

| text | consonants | count | items | langs_p<=0.05 | top3 | p_best_language |
|---|---|---|---|---|---|---|
| VMS (ZL, all) | 2+ | tokens | 8350 | 17/30 | Tatar 0.001, Azerbaijani 0.002, Tajik 0.003 | 0.096 |
| VMS (ZL, all) | 2+ | types | 255 | 17/30 | Uzbek 0.001, Arabic 0.002, Egyptian Arabic 0.002 | 0.044 |
| VMS (ZL, all) | 3+ | tokens | 2791 | 17/30 | Tatar 0.001, Azerbaijani 0.002, Tajik 0.003 | 0.096 |
| VMS (ZL, all) | 3+ | types | 224 | 20/30 | Uzbek 0.001, Tatar 0.001, Arabic 0.002 | 0.033 |
| self-citation generator (no meaning) | 2+ | tokens | 7744 | 6/30 | Tatar 0.005, Chechen 0.006, Pashto 0.015 | 0.461 |
| self-citation generator (no meaning) | 2+ | types | 241 | 0/30 | Chechen 0.067, Pashto 0.200, Czech 0.201 | 0.701 |
| self-citation generator (no meaning) | 3+ | tokens | 1784 | 6/30 | Tatar 0.005, Chechen 0.006, Pashto 0.015 | 0.461 |
| self-citation generator (no meaning) | 3+ | types | 207 | 1/30 | Chechen 0.041, Pashto 0.134, Czech 0.145 | 0.649 |
| Naibbe cipher of Pliny (Latin) | 2+ | tokens | 8264 | 21/30 | Arabic 0.001, Egyptian Arabic 0.001, Persian 0.001 | 0.024 |
| Naibbe cipher of Pliny (Latin) | 2+ | types | 149 | 23/30 | Arabic 0.001, Egyptian Arabic 0.001, Persian 0.001 | 0.018 |
| Naibbe cipher of Pliny (Latin) | 3+ | tokens | 3347 | 21/30 | Arabic 0.001, Egyptian Arabic 0.001, Persian 0.001 | 0.024 |
| Naibbe cipher of Pliny (Latin) | 3+ | types | 118 | 23/30 | Arabic 0.001, Egyptian Arabic 0.001, Persian 0.001 | 0.019 |

`langs_p<=0.05`: languages (of 30) where Bax's key matches more than 95% of shuffled keys. `p_best_language`: how often a shuffled key's best language matches as well as Bax's best language.

## VMS, distinct skeletons of 3+ consonants (224), per language

| language | lexicon | bax | shuffled_mean | rank_of_bax | p |
|---|---|---|---|---|---|
| Uzbek | 13872 | 0.598 | 0.410 | 1 | 0.001 |
| Tatar | 6960 | 0.531 | 0.362 | 1 | 0.001 |
| Arabic | 7460 | 0.473 | 0.314 | 2 | 0.002 |
| Egyptian Arabic | 6836 | 0.504 | 0.323 | 2 | 0.002 |
| Pashto | 7212 | 0.504 | 0.352 | 2 | 0.002 |
| Chechen | 8907 | 0.571 | 0.402 | 2 | 0.002 |
| Azerbaijani | 13081 | 0.652 | 0.430 | 3 | 0.003 |
| Kurdish | 5437 | 0.589 | 0.414 | 4 | 0.004 |
| Ossetian | 5632 | 0.429 | 0.288 | 3 | 0.004 |
| Persian | 5087 | 0.518 | 0.356 | 5 | 0.005 |
| Urdu | 5355 | 0.442 | 0.326 | 5 | 0.005 |
| Czech | 12809 | 0.536 | 0.390 | 10 | 0.010 |
| Tajik | 9423 | 0.603 | 0.455 | 11 | 0.011 |
| Turkish | 14134 | 0.625 | 0.439 | 11 | 0.011 |
| Greek | 9466 | 0.580 | 0.409 | 13 | 0.013 |
| German | 14946 | 0.643 | 0.508 | 13 | 0.013 |
| Crimean Tatar | 6809 | 0.464 | 0.321 | 24 | 0.024 |
| Kazakh | 14305 | 0.518 | 0.356 | 26 | 0.026 |
| Romani | 3141 | 0.362 | 0.268 | 34 | 0.034 |
| Hebrew | 8519 | 0.397 | 0.284 | 48 | 0.048 |
| Croatian | 14147 | 0.473 | 0.374 | 61 | 0.061 |
| Turkmen | 9260 | 0.469 | 0.356 | 79 | 0.079 |
| Romanian | 8797 | 0.522 | 0.404 | 84 | 0.084 |
| Spanish | 10488 | 0.558 | 0.438 | 135 | 0.135 |
| English | 9264 | 0.531 | 0.448 | 162 | 0.162 |
| Latin | 13064 | 0.562 | 0.477 | 185 | 0.185 |
| Hungarian | 17112 | 0.473 | 0.388 | 220 | 0.220 |
| Albanian | 10804 | 0.500 | 0.424 | 218 | 0.227 |
| Italian | 9573 | 0.522 | 0.450 | 230 | 0.230 |
| Latin (Aix, medieval) | 6254 | 0.344 | 0.311 | 349 | 0.349 |

`bax`: share of tokens whose skeleton is a word (2+ occurrences) in that language's Wikipedia sample. `shuffled_mean`, `rank_of_bax`, `p`: against 1000 keys with Bax's sound values given to the 10 consonant signs in random order.
