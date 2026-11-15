# 02 languages

283 comparison texts, first 10000 words each.

Texts with h2 at or below VMS (ZL, 2.15): **0**

Dropped 28 texts whose script the tokenizer breaks into 1-glyph words (mean word length < 2): Hebrew_Bereshit_vowel, Assamese, Bengali, Bihari, Bishnupriya Manipuri, Burmese, Divehi, Doteli, Dzongkha, Goan Konkani, Gujarati, Hindi, Kannada, Khmer, Maithili, Malayalam, Marathi, Nepali, Newar, Oriya, Punjabi, Sanskrit, Shan, Sinhalese, Tamil, Telugu, Tibetan, Tulu

## the VMS rows

| text | kind | h1 | h2 | word_len | hapax_ratio | zipf |
|---|---|---|---|---|---|---|
| VMS ZL | voynich | 3.842 | 2.154 | 4.714 | 0.686 | -0.996 |
| VMS GC | voynich | 3.960 | 2.572 | 3.694 | 0.716 | -0.960 |
| VMS CD | voynich | 3.820 | 2.424 | 3.864 | 0.683 | -0.980 |

## lowest h2 among natural texts

| text | kind | h1 | h2 | word_len | hapax_ratio | zipf |
|---|---|---|---|---|---|---|
| Sranan | wikipedia | 3.847 | 2.589 | 3.620 | 0.026 | -0.900 |
| Hakka | wikipedia | 4.250 | 2.686 | 3.108 | 0.349 | -1.318 |
| Venda | wikipedia | 4.042 | 2.787 | 4.705 | 0.607 | -0.955 |
| Min Dong | wikipedia | 4.303 | 2.814 | 3.066 | 0.384 | -1.256 |
| Atikamekw | wikipedia | 3.664 | 2.868 | 6.324 | 0.685 | -0.985 |
| Tswana | wikipedia | 3.975 | 2.869 | 4.421 | 0.632 | -1.037 |
| Malagasy | wikipedia | 3.846 | 2.900 | 5.304 | 0.641 | -0.954 |
| Pali | wikipedia | 4.346 | 2.907 | 8.658 | 0.665 | -0.908 |
| Samoan | wikipedia | 3.618 | 2.912 | 3.446 | 0.565 | -1.088 |
| Hawaiian | wikipedia | 3.705 | 2.934 | 4.130 | 0.517 | -1.218 |
| Maori | wikipedia | 3.863 | 2.947 | 4.029 | 0.605 | -1.117 |
| Tsonga | wikipedia | 4.107 | 3.034 | 4.913 | 0.626 | -0.979 |
| Chichewa | wikipedia | 4.119 | 3.043 | 5.735 | 0.673 | -0.940 |
| Tagalog | wikipedia | 3.835 | 3.048 | 5.241 | 0.623 | -0.870 |
| Kongo | wikipedia | 4.133 | 3.060 | 4.850 | 0.623 | -0.857 |

## nearest on all six metrics

| text | kind | h1 | h2 | word_len | hapax_ratio | zipf | dist_all |
|---|---|---|---|---|---|---|---|
| Venda | wikipedia | 4.042 | 2.787 | 4.705 | 0.607 | -0.955 | 1.157 |
| Tswana | wikipedia | 3.975 | 2.869 | 4.421 | 0.632 | -1.037 | 1.268 |
| Malagasy | wikipedia | 3.846 | 2.900 | 5.304 | 0.641 | -0.954 | 1.371 |
| Maori | wikipedia | 3.863 | 2.947 | 4.029 | 0.605 | -1.117 | 1.403 |
| Samoan | wikipedia | 3.618 | 2.912 | 3.446 | 0.565 | -1.088 | 1.466 |
| Tsonga | wikipedia | 4.107 | 3.034 | 4.913 | 0.626 | -0.979 | 1.490 |
| Kongo | wikipedia | 4.133 | 3.060 | 4.850 | 0.623 | -0.857 | 1.507 |
| Secreta_Secretorum_ENG | historical | 4.024 | 3.088 | 4.371 | 0.550 | -1.049 | 1.585 |
| Hausa | wikipedia | 3.946 | 3.161 | 4.617 | 0.644 | -0.873 | 1.586 |
| Chichewa | wikipedia | 4.119 | 3.043 | 5.735 | 0.673 | -0.940 | 1.588 |
| Waray-Waray | wikipedia | 3.933 | 3.171 | 5.048 | 0.625 | -1.017 | 1.603 |
| Agrippa_Book1 | historical | 4.066 | 3.185 | 4.624 | 0.630 | -1.075 | 1.613 |
| Javanese | wikipedia | 4.063 | 3.158 | 5.791 | 0.641 | -0.872 | 1.637 |
| Acehnese | wikipedia | 4.207 | 3.205 | 5.131 | 0.617 | -0.930 | 1.641 |
| Northern Sotho | wikipedia | 4.062 | 3.107 | 4.707 | 0.580 | -0.935 | 1.641 |

## nearest on h1/h2 only

| text | kind | h1 | h2 | word_len | hapax_ratio | zipf | dist_h |
|---|---|---|---|---|---|---|---|
| Sranan | wikipedia | 3.847 | 2.589 | 3.620 | 0.026 | -0.900 | 1.100 |
| Hakka | wikipedia | 4.250 | 2.686 | 3.108 | 0.349 | -1.318 | 1.412 |
| Venda | wikipedia | 4.042 | 2.787 | 4.705 | 0.607 | -0.955 | 1.614 |
| Min Dong | wikipedia | 4.303 | 2.814 | 3.066 | 0.384 | -1.256 | 1.736 |
| Tswana | wikipedia | 3.975 | 2.869 | 4.421 | 0.632 | -1.037 | 1.813 |
| Atikamekw | wikipedia | 3.664 | 2.868 | 6.324 | 0.685 | -0.985 | 1.814 |
| Malagasy | wikipedia | 3.846 | 2.900 | 5.304 | 0.641 | -0.954 | 1.885 |
| Samoan | wikipedia | 3.618 | 2.912 | 3.446 | 0.565 | -1.088 | 1.930 |
| Pali | wikipedia | 4.346 | 2.907 | 8.658 | 0.665 | -0.908 | 1.976 |
| Hawaiian | wikipedia | 3.705 | 2.934 | 4.130 | 0.517 | -1.218 | 1.977 |
| Maori | wikipedia | 3.863 | 2.947 | 4.029 | 0.605 | -1.117 | 2.003 |
| Tsonga | wikipedia | 4.107 | 3.034 | 4.913 | 0.626 | -0.979 | 2.241 |
| Tagalog | wikipedia | 3.835 | 3.048 | 5.241 | 0.623 | -0.870 | 2.258 |
| Chichewa | wikipedia | 4.119 | 3.043 | 5.735 | 0.673 | -0.940 | 2.265 |
| Kongo | wikipedia | 4.133 | 3.060 | 4.850 | 0.623 | -0.857 | 2.310 |
