# 28 — Do pages follow a template?

## Why

Exp. 27 left page vocabulary with two explanations: a subject, or copying within the page.
An entry in a herbal is written to a plan: what the plant looks like, then what it's good
for. If the VMS herbal pages are entries, the words used should depend on how far down the
page you are, in the same way on every page. A writer recycling recent words has no reason
to do that.

## What I did

Lines of each page split into top, middle and bottom thirds; G statistic for the table of
the 150 most frequent words against the thirds. Paragraph-first lines, paragraph-last lines
and the first and last word of every line are removed first, because those position effects
are already known (gallows openers, exp. 10, exp. 20).

Two nulls. Shuffling the lines of each page is the obvious one, but it also breaks up runs
of similar neighbouring lines, which makes the real table look lumpier than the null for a
reason unrelated to templates. The strict null keeps every page's lines in
sequence and only moves the frame: start at a random line, wrap around, read upwards half
the time. Only an effect that points the same way on every page can beat that.

## Result

| | pages | z, lines shuffled | z, strict | p, strict |
|---|---|---|---|---|
| VMS herbal A, hand 1 | 75 | −0.4 | −0.6 | 0.71 |
| VMS herbal A, nothing removed | 95 | 1.6 | 1.6 | 0.06 |
| VMS balneological B | 19 | 2.7 | 1.7 | 0.04 |
| VMS stars B | 22 | 2.2 | 1.3 | 0.10 |
| Pliny 16, chapters | 44 | 1.6 | 1.0 | 0.16 |
| copying model | 184 | 0.6 | 0.1 | 0.47 |

- **No template in the herbal.** Once the known edge effects are out, the body of a herbal A
  page uses the same words at the top, in the middle and at the bottom. Even with the
  paragraph openers left in, it only reaches p = 0.06.
- The B sections looked position-dependent under the simple shuffle (p = 0.006 and 0.02),
  and a third to a half of that goes away under the strict null (p = 0.04 and 0.10). What
  was there was mostly runs of similar lines, not a plan.

## What this doesn't show

I have no real herbal with one entry per page to run as a positive control (Pliny's chapters
are continuous prose, not entries), so I can't say how big a template effect a genuine
herbal would give on this test. This is a "didn't find it", not a "it isn't there". A
transcribed medieval herbal (a *Circa instans* or a *Tractatus de herbis*) would settle
what the test can see; that's the missing piece.

## So what

Nothing here helps the "subject" reading over the "copying" one. The 75 herbal A pages give
this test decent power, and they show no sign of entry structure beyond the first line.
