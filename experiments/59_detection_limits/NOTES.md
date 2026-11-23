# 59 — What plaintext could still hide in the forks?

## What I think

Exp. 54 found nothing in the forks, but its calibration used full Latin text, and the test feeds on
the plaintext's redundancy. A heavily abbreviated text, or numbers, leaves less to find. The question
is where the test goes blind.

## What I did

Same channel (2 bits per word in the start class) and test as exp. 54, with six plaintexts, each
alphabet coded in the fewest bits that hold it: full Latin; Latin without vowels; the first three
letters of each word; word initials only; the word lengths of the Latin text as digits (real
numbers with little redundancy); random digits.

## Result (bits gained by looking further than one word back)

| plaintext | gain | best k |
|---|---|---|
| Latin, no vowels | 0.354 | 5 |
| Latin, full | 0.179 | 5 |
| numbers (word lengths) | 0.143 | 4 |
| first 3 letters of each word | 0.120 | 4 |
| word initials only | 0.033 | 3 |
| random digits | 0.024 | 3 |
| **Currier B** | **0.003** | |

## So what

Every plaintext tried is detectable, down to random digits. A digit coded in 4 bits uses only 10 of
16 codes, and that gap in the code is itself structure. What the test can't see is a plaintext whose
code uses every value equally and independently: random bits, or text compressed to its entropy,
which no 15th-century scheme does. Currier B sits below even random digits.

So the "near-random plaintext" exception left open in exp. 54 is narrower than it looked: abbreviation
and numbers would have shown. Only a code designed to be statistically flat would hide, in this channel.

## Caveats

- One channel (start class, 2 bits per word). Exp. 54 covers the other channels with full Latin only.
- Fixed-length binary codes are my choice; a scheme with variable-length codes would leave different
  (not necessarily less) structure.
