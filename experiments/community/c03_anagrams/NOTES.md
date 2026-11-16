# c03 — How much does a perfect anagram prove?

## What was claimed

A May 2026 Zenodo preprint, "Voynich f99r Deciphered: Italian Anagrams of a Spagyric
Recipe" (record 20109175), converts EVA into another glyph alphabet and then rearranges
each string, letter-perfect, into Italian words. Lines 1-14 of f99r come out as a symbolic
alchemical vocabulary, and the author says the method is repeatable.

## What I thought

Anagram solutions have a long and bad history with this manuscript, starting with Newbold in
the 1920s, whose readings depended on rearranging letters freely. The problem is not the specific
reading, it's that anagramming gives you a lot of freedom. Before arguing about any one
mapping, I wanted a number for that freedom.

Hypothesis: with a decent Italian vocabulary and permission to use two words, most random
strings of label length can be anagrammed into Italian. If that's true, a successful anagram
says nothing about the source.

## What I did

Italian vocabulary: the 30k most frequent word forms from Italian Wikipedia plus the
Rettorica (Lindemann & Bowern corpora). For lengths 4 to 9, 300 strings each of:

- real Italian words, scrambled (should always work)
- random strings with Italian letter frequencies
- Voynich words through a frequency-matched glyph-to-letter key (most common glyph to most
  common Italian letter, and so on), i.e. a mapping chosen without looking at meaning

I didn't use the preprint's own mapping; the point is the size of the search space, which
any mapping inherits.

## Result

| length | random → 1 word | random → 1-2 words | VMS words → 1-2 words |
|---|---|---|---|
| 4 | 35% | 90% | 99% |
| 5 | 26% | 92% | 95% |
| 6 | 11% | 88% | 96% |
| 7 | 7% | 87% | 83% |
| 8 | 3% | 79% | 92% |
| 9 | 2% | 75% | 85% |

Single-word anagrams get rare as strings get longer, but allow a split into two words and
75-99% of meaningless strings become Italian. Voynich words through an arbitrary key behave
like random strings.

## So what

A letter-perfect Italian anagram of a Voynich label is expected even if the label means
nothing. Anagram readings need a test the method could fail: the same mapping producing
the same word for the same label everywhere, readings that match the drawing before you
look, or an anagram key that makes a page read as continuous Italian, which random strings
won't do. I haven't seen any anagram proposal pass that.
