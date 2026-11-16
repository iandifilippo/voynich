# c04 — Do zodiac label prefixes follow the seasons?

## What was claimed

voynich.ninja thread 5817 (June 2026), "Seasonal prefix clustering in Voynich zodiac nymph
labels": the share of labels starting with ot- or ok- shifts through the year. Replies agreed
the pattern is visible in the text and asked what it means.

## What I thought

I'd already seen the raw numbers in experiment 06 (ot- at 73% in Aries, 7% in Cancer). Two
things bothered me. First, "seasonal" implies an ordered trend through the year, not just
"signs differ". Second, the zodiac pages aren't uniform: different scribes, different layouts,
some pages with dark and light halves. If the circular text on the same pages shifts in the
same way, it's a page effect, not something about the labels.

Hypothesis: signs differ, but there's no ordered seasonal trend, and the ring text shows the
same kind of variation.

## What I did

Labels and ring text (circular and radial lines) from the 10 zodiac signs that survive.
Prefix classes: ot, ok, oe, ch, sh, y, d, other. Two statistics: chi-square of prefix by sign,
and the Spearman correlation between month (March to December) and ot- share. Null: deal the
same words back to the signs at random, 2000 times.

## Result

| text | words | sign differences (p) | month vs ot- trend | p (two-sided) |
|---|---|---|---|---|
| labels | 344 | < 0.001 | ρ = −0.60 | 0.084 |
| ring text | 947 | 0.001 | ρ = −0.49 | 0.158 |

Signs really do differ in prefixes, in both labels and ring text. The ordered trend through the
year is not significant for either. ot- is high in March and April, low in summer, and comes
back up in November.

## So what

The thread's observation holds, and the "seasonal" reading of it doesn't. The variation is
there in the non-label text of the same pages too, which points at the page (scribe, sitting,
which part of the diagram) rather than at a calendar meaning in the labels. Next step would be
splitting by the dark and light halves of Aries and Taurus, which sit on separate pages and
may have been made separately.
