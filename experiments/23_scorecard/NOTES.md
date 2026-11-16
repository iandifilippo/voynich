# 23 — Checking the best model on things I didn't tune

## Why

By exp. 22 the copying model scores 1.49 on the benchmark, but I got there by adding three
rules while watching that same benchmark. A model that's any good should also get right
things nobody adjusted it for.

## What I did

Best model (copying + boundary habit + line-end rule + prefer common), 8 seeds, against 26
measures that never set a knob: repeats against the in-line shuffle, make-up of singletons,
word lengths, which glyphs words start and end with, how line-first words start, share of
the top word. B settings against Currier B, A settings against Currier A. "ok" = within
0.8-1.25× of the VMS, "off" = within 2×, "wrong" = further.

## Result

- B: 10 ok, 10 off, 6 wrong. A: 8 ok, 11 off, 7 wrong.
- **Right**: near-repeat excess (1.06 vs 1.00 in B), singletons one edit from a known word
  (65% vs 63%), mean word length, long words, share of the top word, -m endings, d- words.
- **Badly wrong: which words.** q- words are 20% of Currier B and 1.4% of the model's
  output. o- words 21% vs 7%. Line-first d-, t- and q- words 3 to 16 times too rare.
  One-glyph words nearly absent. In A settings, two-glyph words three times too common.
- The model's A and B settings differ from each other (1.21) about as much as Currier A and
  B do (1.31), but two B runs with different seeds already differ by 0.80, so most of that
  is noise, not dialect.

## So what

The benchmark can't see *what the words are*. All 13 metrics are about shape: entropy,
lengths, frequencies, positions. A text can sit at distance 1.5 and contain almost no *qo-*
words. Two consequences:

1. Every claim of the form "model X reproduces the VMS statistics" (ours included, and
   Naibbe's, and the generator's) needs a second stage that compares glyph content. This
   scorecard is now that second stage.
2. For the copying model specifically, the q- shortfall is probably in the rules, and maybe
   in my port of them: the only way to gain *q* is a prefix rule that fires rarely, while
   the substitution table turns *qo* back into *o* whenever it's picked. I haven't run the
   original app to see whether it has the same shortfall, so I'm not attributing this to
   Timm & Schinner's procedure, only to my implementation of it.

The honest summary of where the model stands: right about how the text is organised (lines,
repeats, core, edges), wrong about what it's made of.
