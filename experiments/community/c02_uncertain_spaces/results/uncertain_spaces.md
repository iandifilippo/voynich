# c02 uncertain spaces

| boundary | n | joins_into_known_word | both_sides_known_words | edge_mi_bits |
|---|---|---|---|---|
| certain space '.' | 28159 | 0.037 | 0.766 | 0.164 |
| uncertain space ',' | 2433 | 0.337 | 0.844 | 0.545 |
| random cut inside a word | 20000 | 0.828 | 0.390 | 1.695 |
| adjacent glyphs inside words | 138913 | None |  | 1.669 |

`joins_into_known_word`: gluing the two sides gives a word seen 2+ times elsewhere. `both_sides_known_words`: each side is a word seen 2+ times on its own.

If uncertain spaces were a mix of real spaces (like '.') and word-internal cuts, the join rate implies about **38%** of them are word-internal.
