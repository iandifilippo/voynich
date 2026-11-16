# c01 — Greshko's Naibbe cipher, the real thing

## What was claimed

Greshko (Cryptologia, 2025) built a verbose homophonic cipher that a 15th-century
person could run with dice and playing cards. Latin or Italian goes in, Voynich-looking
text comes out, and it matches a lot of the manuscript's statistics at once. He is
careful about it: he says it's almost certainly not how the VMS was made, and offers
it as a benchmark.

## What I thought

In experiment 05 I wrote my own "Naibbe-like" cipher from the description and it did
badly: it killed the open vocabulary (hapax 0.25 against 0.68). I suspected that was
my implementation, not his idea. His repo ships real ciphertext (Pliny's Natural History
run through his published tables), so there's no excuse not to test the original.

Hypothesis: on glyph/word statistics the real Naibbe should sit much closer to the VMS
than my version, but it should still fail where Rozanova & Temerev (2026) said published
imitations fail: edge coupling between words and the rare-word-heavy vocabulary.

## What I did

Took `encrypted/nathist_output_ciphertext.txt` from his repository as is and scored it
with the same benchmark as everything else. His file breaks lines every ~33 words, which
isn't a manuscript line, so I scored it both with his breaks and cut into 9-word lines.
Line metrics are meaningless here either way; the column to read is `core` (the 9
glyph/word metrics only).

## Result

| text | core distance | h2 | hapax | edge coupling |
|---|---|---|---|---|
| Naibbe (Greshko) | 0.94 | 2.09 | 0.58 | 0.002 |
| my naibbe_like | 2.22 | 2.24 | 0.25 | 0.002 |
| VMS, later pages | 0.18 | 2.14 | 0.70 | 0.18 |
| VMS, Currier B | 0.71 | 1.94 | 0.68 | 0.25 |

His cipher is far better than my reconstruction. It nails h2 and gets the vocabulary much
closer. On word-internal statistics it's about as far from the reference as Currier B is,
which is a real achievement.

What it doesn't do: consecutive words in the VMS are coupled at their edges (the last glyph
of one word tells you something about the first glyph of the next, 0.18 bits after removing
frequency effects). In Naibbe output that coupling is zero, because each word is enciphered
on its own. Vocabulary is still less open (0.58 vs 0.68).

## So what

Confirms the critique with the original files rather than a reimplementation. Any cipher
that works one word at a time will have this problem. If the VMS is a cipher, the process
had some memory across word boundaries, or the spaces aren't where the plaintext's word
boundaries were. That's worth chasing.
