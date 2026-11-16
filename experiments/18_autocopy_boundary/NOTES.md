# 18 — Copying plus a habit at the word boundary

## Why

Exp. 17 left one clean gap: the self-citation generator makes no cross-word coupling
(0.01 vs 0.15), and neither does any cipher except the autokey of exp. 13. The question is
whether the copying model can absorb the coupling without breaking anything else, and how
little it takes.

## Hypothesis

A scribe with a mild visual or rhythmic preference (after a word ending in -y, start the next
with q/qo/d/k/t rather than a/o) would produce coupling without any key. If that's enough, the
coupling doesn't need a cryptographic explanation at all.

## What I did

Added an optional boundary list to the generator: for each final glyph, the word starts
the scribe "prefers". A copied word that doesn't fit is discarded with probability p and
another is copied. Two lists: one fitted from the VMS (starts with positive PMI after each
final glyph, odd lines only), and five random lists of the same sizes. Pattern checked
against even lines. B settings, 3 seeds per row.

## Result

| boundary list | p | distance | core | edge | pattern r |
|---|---|---|---|---|---|
| none | 0 | 2.44 | 0.98 | 0.013 | 0.09 |
| fitted | 0.5 | 2.41 | 0.83 | 0.057 | 0.67 |
| fitted | 0.65 | 2.42 | **0.71** | 0.115 | 0.70 |
| fitted | 0.8 | 2.45 | 0.79 | 0.227 | 0.73 |
| fitted | 0.95 | 2.97 | 1.85 | 0.508 | 0.55 |
| random (5) | 0.8 | 2.48 | 0.74 | 0.176 | 0.02 (best 0.16) |

- p ≈ 0.65-0.7 gives VMS-sized coupling (0.12-0.15) and the core distance drops to 0.71,
  the same as Currier B's own distance from the whole manuscript. The line metrics don't move.
- With the fitted list the pattern matches (r 0.70); random lists give the right size, wrong
  pattern, same as in exp. 13.
- The rule has nothing to say about line ends: line_last_jsd stays at about −7.

## Caveats, honestly

The fitted list is ~40 yes/no choices read off the manuscript. Odd and even lines agree at
r = 0.98, so the held-out check is weak: getting r 0.7 here mostly shows the rule *can* carry
the pattern, not that it explains it. The autokey of exp. 13 had to earn its pattern through
the tables (r 0.24-0.43); this one is handed it. What it does show is that coupling is not
evidence of a cipher: a copying scribe with a habit reproduces it at no cost to anything else.

## So what

Best model so far: copying + boundary habit, distance 2.42, core 0.71. What's left is
(1) too few hapaxes (0.55 vs 0.69) — the generator recycles too much; (2) line ends; (3) the
d/t/q line-start excess. The next real test is (1): if raising the mutation rate fixes the
hapax ratio without wrecking cohesion, the plaintext-free model fits every number we have,
and "it's meaningless" becomes the default to beat.
