"""Which words like to open or close a line?

In ordinary text line breaks fall wherever the page runs out, so no word
should care. For each frequent word we compare its share of line-initial
and line-final slots with its overall share, and check the result against
lines rebuilt from shuffled words.
"""
import math
import pathlib
import random
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich

HERE = pathlib.Path(__file__).parent
v = Voynich("ZL")
lines = [l for l in v.text_lines(unit="P") if len(l) >= 3]
allw = Counter(w for l in lines for w in l)
first = Counter(l[0] for l in lines)
last = Counter(l[-1] for l in lines)
second = Counter(l[1] for l in lines)
N, F = sum(allw.values()), len(lines)

rows = []
for w, c in allw.most_common(300):
    exp = c / N * F
    rows.append({"word": w, "count": c,
                 "first_ratio": first[w] / exp, "last_ratio": last[w] / exp, "second_ratio": second[w] / exp,
                 "first": first[w], "last": last[w]})

# how extreme is that with shuffled lines?
rng = random.Random(0)
flat = [w for l in lines for w in l]
max_null = []
for _ in range(20):
    rng.shuffle(flat)
    i, fs, ls = 0, Counter(), Counter()
    for l in lines:
        seg = flat[i:i + len(l)]
        fs[seg[0]] += 1
        ls[seg[-1]] += 1
        i += len(l)
    worst = max(max(fs[w] / (c / N * F), ls[w] / (c / N * F)) for w, c in allw.most_common(300))
    max_null.append(worst)

# line length in glyphs vs words: are lines filled to a width (text) or to a count (records)?
glen = [sum(len(w) for w in l) for l in lines]
wlen = [len(l) for l in lines]
mg, mw = sum(glen) / len(glen), sum(wlen) / len(wlen)
cv_g = (sum((x - mg) ** 2 for x in glen) / len(glen)) ** .5 / mg
cv_w = (sum((x - mw) ** 2 for x in wlen) / len(wlen)) ** .5 / mw

# Do line-initial words look like an ordinary word with one extra glyph in front?
common = {w for w, _ in allw.most_common(500)}


def stripped_is_common(w):
    return len(w) > 2 and w[1:] in common


def share(ws):
    return sum(stripped_is_common(w) for w in ws) / len(ws)


first_tokens = [l[0] for l in lines]
mid_tokens = [w for l in lines for w in l[1:-1]]
glyph_stats = {}
for g in "dstypkfo":
    fg = [w for w in first_tokens if w[0] == g]
    mg_ = [w for w in mid_tokens if w[0] == g]
    if len(fg) >= 20 and len(mg_) >= 20:
        glyph_stats[g] = {"first_n": len(fg), "first_share": share(fg), "mid_n": len(mg_), "mid_share": share(mg_)}
extra = {"first_share": share(first_tokens), "mid_share": share(mid_tokens), "by_glyph": glyph_stats}

res = {"extra_glyph": extra, "rows": rows, "max_ratio_shuffled": max_null, "cv_glyphs": cv_g, "cv_words": cv_w}
save(HERE, "line_positions", res)
md = "# 08 line positions\n\n"
md += f"{len(lines)} paragraph lines (3+ words). With shuffled words, the most extreme first/last ratio among the top 300 words is at most {max(max_null):.1f}.\n\n"
cols = ["word", "count", "first_ratio", "last_ratio", "second_ratio", "first", "last"]
md += "## words that open lines\n\n" + table(sorted(rows, key=lambda r: -r["first_ratio"])[:20], cols, {k: ".2f" for k in cols})
md += "\n## words that close lines\n\n" + table(sorted(rows, key=lambda r: -r["last_ratio"])[:20], cols, {k: ".2f" for k in cols})
md += "\n## words that avoid line starts\n\n" + table(sorted(rows, key=lambda r: r["first_ratio"])[:15], cols, {k: ".2f" for k in cols})
md += "\n## one extra glyph at the start of the line?\n\n"
md += f"Share of words that become one of the 500 most common words when the first glyph is removed: **{extra['first_share']:.1%}** of line-initial words vs **{extra['mid_share']:.1%}** of line-internal words.\n\n"
md += table([{"glyph": g, **x} for g, x in glyph_stats.items()], ["glyph", "first_n", "first_share", "mid_n", "mid_share"])
md += f"\nCoefficient of variation of line length: {cv_g:.3f} in glyphs, {cv_w:.3f} in words.\n"
write_md(HERE, "line_positions", md)
print(md)
