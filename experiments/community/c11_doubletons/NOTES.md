# c11 — Do rare words stay together? (voynich.ninja, "Hapax and doubletons")

## The question

DG97EEB built a tool for words that occur once or twice, hoping to find nouns. R. Sale asked
the right follow-up: do the two occurrences of a doubleton sit on the same page, in the same
hand, or anywhere? If a rare word names a thing, the thing is talked about in one place.

## What I did

Every word with exactly two occurrences (537 with a known Currier language). How often are
the two on the same line, page, sheet, section, hand, against two tokens drawn at random
from the same Currier language.

## Result

| both on the same | observed | at random | ratio |
|---|---|---|---|
| line | 0.6% | 0.05% | 11.7 |
| page | 3.9% | 1.4% | 2.7 |
| sheet | 11.7% | 5.8% | 2.0 |
| section | 52% | 38% | 1.4 |
| hand | 66% | 58% | 1.1 |

Distance between the two: same page 2%, next page 4%, 2-5 pages 9%, 6-20 pages 19%, further
than 20 pages 65%.

## So what

There is a pull (nearly three times chance for the same page), but it's small in absolute
terms: 96% of doubletons have their two occurrences on different pages, two thirds more than
twenty pages apart. That is not how names of things on a page behave, and it fits exp. 20
(rare words are edge variants of common ones) and exp. 22 (rare words are barely local).
The sheet doing better than chance by 2× is one more small sign that the sheet is a unit
(exp. 29).
