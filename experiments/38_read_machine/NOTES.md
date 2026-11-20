# 38 — Reading the machine

## What I did

A 12-state machine (exp. 37's method, best of six starts) fitted to all of Currier B and all of
Currier A, listing what each state writes and where it goes, drawn as a graph
(`results/machine_B.svg`, `results/machine_A.svg`).

## Result

Currier B, with the arrows that carry most of the traffic:

| state | writes | then goes to |
|---|---|---|
| S1 | the space | S2 (o) 0.28, S9 (ch/sh) 0.25, S10 (q) 0.22 |
| S10 | q | S2 (o) 0.99 |
| S2 | o | S3 (gallows) 0.61, S6 (l/r) 0.27 |
| S9 | ch 0.67, sh 0.31 | S4 (e) 0.72 |
| S3 | k 0.57, t 0.29, p 0.07 | S4 (e) 0.39, S7 (a) 0.39 |
| S4 | e 0.63, ee 0.29 | S8 (d) 0.52, S5 (y) 0.30 |
| S8 | d 0.88 | S5 (y) 0.67, S7 (a) 0.25 |
| S7 | a 0.91 | S6 (l/r) 0.54, S11 (i) 0.45 |
| S11 | ii 0.55, i 0.42 | S12 (n) 0.96 |
| S5 | y 0.94 | space 0.97 |
| S6 | l 0.55, r 0.35 | space 0.65 |
| S12 | n 0.89 | space 0.98 |

No state loops on itself (self-transition under 0.003 everywhere). Every state writes one
kind of sign. Read left to right it is: *q*, then *o*; or *ch/sh*; then a gallows; then *e* or
*ee*; then *d*; then *y* and stop. Or, after *a*: *l/r* and stop, or *ii* then *n* and stop.
That spells the familiar words: *qokedy, qokeedy, chedy, shedy, qokaiin, okal, chol, daiin*.

Currier A's machine has the same skeleton (q/ch/sh → o → l/r; gallows → e → y; a → ii → n)
with different weights: more *ch* at the start, more *o* after it, fewer *e-d-y* runs.

## So what

The machine isn't a black box: it's a short table of positions, each holding a few signs,
walked left to right with a few forks. It's essentially Zattera's slot grammar, found from
scratch by a method that knew nothing about slots, and it's the same table for both Currier
languages with the forks weighted differently.

That's something a person could carry out by hand: a strip or wheel with a column per position
and a rule for which column comes next. With 12 states it is coarser than the real text (exp.
37: 350 distinct words per 1000 instead of 248); the extra precision of a 48-state machine is
mostly in which branch follows which, i.e. in the habits around the forks.

This doesn't say whether the choices at each fork were free or dictated by something. That is
the question the rest of this series has to answer.
