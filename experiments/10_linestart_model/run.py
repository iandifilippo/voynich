"""Is a line-initial word just an ordinary word with one glyph stuck on the front?

Emma May Smith (Agnostic Voynich, 2016) proposed a "linestart transformation":
at the start of a line some words gain an extra glyph (s, d, y...) or have their
first glyph swapped. Nick Pelling has long suspected line-initial s is a null.
08_line_positions confirms the raw effect. Here we test the mechanism:

For each word type x, compare how often it opens a line with how often it
would if line position didn't matter (expected from its overall share).
- deficit(x) = expected - observed at line start
- surplus(g+x) = observed - expected for the same word with glyph g in front

If line-initial g+x really stands for x, word types missing from line starts
should be the ones showing up with g attached: corr(deficit(x), surplus(g+x)) > 0.
Null: shuffle which x each surplus is paired with (keeping the set of x's).
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
GLYPHS = ["s", "d", "y", "o", "t", "k", "p", "q", "l", "r"]


def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den if den else 0.0


def analyse(lines, label, rng):
    lines = [l for l in lines if len(l) >= 3]
    first = Counter(l[0] for l in lines)
    rest = Counter(w for l in lines for w in l[1:])
    n_first, n_rest = sum(first.values()), sum(rest.values())
    rows = []
    for g in GLYPHS:
        xs, defs, surs = [], [], []
        for x, cx in rest.items():
            gx = g + x
            if cx < 5:
                continue
            exp_x = cx / n_rest * n_first
            exp_gx = rest.get(gx, 0) / n_rest * n_first
            deficit = (exp_x - first.get(x, 0)) / math.sqrt(exp_x)
            surplus = (first.get(gx, 0) - exp_gx) / math.sqrt(exp_x)
            xs.append(x)
            defs.append(deficit)
            surs.append(surplus)
        if len(xs) < 15:
            continue
        r = pearson(defs, surs)
        hits = 0
        perm = surs[:]
        for _ in range(2000):
            rng.shuffle(perm)
            if pearson(defs, perm) >= r:
                hits += 1
        # how many line starts are g + an ordinary word
        gx_first = sum(c for w, c in first.items() if w.startswith(g) and len(w) > 1 and rest.get(w[1:], 0) >= 5)
        g_first = sum(c for w, c in first.items() if w.startswith(g))
        top = sorted(zip(xs, defs, surs), key=lambda t: -t[2])[:6]
        rows.append({"set": label, "glyph": g, "types_tested": len(xs), "r": r, "p": hits / 2000,
                     "line_starts_with_g": g_first, "of_which_g_plus_word": gx_first,
                     "top_pairs": ", ".join(f"{g}+{x} (def {d:.1f}, sur {s:.1f})" for x, d, s in top)})
    return rows


rng = random.Random(0)
v = Voynich("ZL")
rows = []
rows += analyse(v.text_lines(unit="P"), "all", rng)
rows += analyse(v.text_lines(unit="P", language="A"), "Currier A", rng)
rows += analyse(v.text_lines(unit="P", language="B"), "Currier B", rng)
rows += analyse(Voynich("IT").text_lines(unit="P"), "Takahashi (IT)", rng)

save(HERE, "linestart_model", rows)
md = "# 10 linestart transformation\n\n"
md += "Positive r: word types that are missing from line starts are the same ones that turn up there with the glyph in front.\n\n"
md += table(rows, ["set", "glyph", "types_tested", "r", "p", "line_starts_with_g", "of_which_g_plus_word"])
md += "\n## strongest pairs (all, by surplus)\n\n"
for r in rows:
    if r["set"] == "all":
        md += f"- **{r['glyph']}**: {r['top_pairs']}\n"
write_md(HERE, "linestart_model", md)
print(md)
