# c01 Greshko's Naibbe ciphertext

`core` = distance on the 9 glyph/word metrics (no line metrics). `core_vs_B` = same, against the Currier B profile.

| text | distance | core | core_vs_B | h2 | hapax | edge | word_mi | word_len | zipf | worst_core |
|---|---|---|---|---|---|---|---|---|---|---|
| Naibbe (Greshko), his line breaks | 4.536 | 0.940 | 1.461 | 2.088 | 0.576 | 0.002 | 0.007 | 5.229 | -0.876 | edge_coupling -2.1, hapax_ratio -1.5, zipf +0.8 |
| Naibbe (Greshko), 9-word lines | 4.956 | 0.946 | 1.461 | 2.088 | 0.576 | 0.004 | 0.012 | 5.229 | -0.876 | edge_coupling -2.0, hapax_ratio -1.5, zipf +0.8 |
| naibbe_like (ours), Latin | 4.987 | 2.220 | 2.407 | 2.241 | 0.246 | 0.002 | 0.023 | 5.820 | -1.097 | hapax_ratio -6.1, edge_coupling -2.1, word_len +1.1 |
| VMS Currier B | 1.234 | 0.710 | 0.000 | 1.937 | 0.684 | 0.245 | -0.002 | 4.950 | -1.152 | edge_coupling +1.4, zipf -1.1, h2 -1.0 |
| VMS later pages | 1.056 | 0.182 | 0.579 | 2.135 | 0.703 | 0.177 | -0.009 | 4.854 | -1.023 | edge_coupling +0.4, hapax_ratio +0.2, zipf -0.2 |
