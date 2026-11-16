"""Does the memory stop at the edge of the page?

Exp. 22: common words persist for about 25 lines. Exp. 24: not through
position. So what carries it? Three candidates predict different things at a
page boundary:

  the writer copies from what is on the page in front of him
      -> shared vocabulary collapses across any page break
  a slowly drifting habit (or subject matter)
      -> a page break is just a few more lines
  copying from the facing page as well
      -> verso -> next recto (visible together in the bound book) keeps more
         than recto -> verso (needs the leaf turned)

Statistic: for two lines, the number of word types they share, over the number
expected from how common each type is in that part of the manuscript ("lift").
Pairs 1-5 lines apart: inside a paragraph, across a paragraph break on the same
page, across a page break (counting lines through the break). Also pairs on
the same page 10-30 lines apart, and on pages 2 and 3+ pages apart, to see
where the level settles. Three homogeneous blocks so that scribe and section
changes can't produce the effect: herbal A (hand 1), balneological B (hand 2),
stars B (hand 3). Confidence intervals by resampling pages.
"""
import pathlib
import random
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich

HERE = pathlib.Path(__file__).parent
BOOT = 400
v = Voynich("ZL")
order = list(v.pages)
BLOCKS = [("herbal A, hand 1", dict(language="A", hand="1", section="H")),
          ("balneo B, hand 2", dict(language="B", hand="2", section="B")),
          ("stars B, hand 3", dict(language="B", hand="3", section="S"))]


def block_pages(sel):
    pages = {}
    for l in v.select(unit="P", **sel):
        if len(l.words) >= 3:
            pages.setdefault(l.page, []).append(l)
    return [(p, pages[p]) for p in order if p in pages]


def side(p):
    return "r" if "r" in p[1:] else "v"


def analyse(name, sel):
    pages = block_pages(sel)
    freq_lines = Counter()
    n_lines = 0
    for _, ls in pages:
        for l in ls:
            n_lines += 1
            freq_lines.update(set(l.words))
    base = {w: c / n_lines for w, c in freq_lines.items()}
    core = {w for w, _ in freq_lines.most_common(60)}
    pair = lambda c: c * (c - 1) / (n_lines * (n_lines - 1))    # the same type in two different lines
    exp_all = sum(pair(c) for c in freq_lines.values())
    exp_core = sum(pair(freq_lines[w]) for w in core)
    exp_rest = exp_all - exp_core

    # every pair is credited to the page of its lower line, for the bootstrap
    cats = {}

    def add(cat, page_idx, a, b):
        sa, sb = set(a.words), set(b.words)
        sh = sa & sb
        c = cats.setdefault(cat, {})
        t = c.setdefault(page_idx, [0, 0, 0])
        t[0] += 1
        t[1] += len(sh & core)
        t[2] += len(sh - core)

    para_id = []
    for _, ls in pages:
        ids, k = [], 0
        for l in ls:
            if l.para_start:
                k += 1
            ids.append(k)
        para_id.append(ids)

    for pi, (p, ls) in enumerate(pages):
        for i in range(len(ls)):
            for j in range(i + 1, len(ls)):
                d = j - i
                if d <= 5:
                    same = para_id[pi][i] == para_id[pi][j]
                    add("same paragraph, 1-5 lines apart" if same else "same page across a paragraph break, 1-5 lines", pi, ls[i], ls[j])
                elif 10 <= d <= 30:
                    add("same page, 10-30 lines apart", pi, ls[i], ls[j])
        if pi + 1 < len(pages):
            q, ms = pages[pi + 1]
            if order.index(q) == order.index(p) + 1:
                kind = "recto -> its verso (leaf turned)" if side(p) == "r" else "verso -> next recto (facing)"
                for i in range(max(0, len(ls) - 5), len(ls)):
                    for j in range(min(5, len(ms))):
                        if (len(ls) - i) + j <= 5:
                            add("across a page break, 1-5 lines", pi + 1, ls[i], ms[j])
                            add("  of which " + kind, pi + 1, ls[i], ms[j])
                # whole-page comparison for adjacent pages, sampled
                for a in ls[::3]:
                    for b in ms[::3]:
                        add("next page, any lines", pi + 1, a, b)
                        add("  of which " + kind + " ", pi + 1, a, b)
        # control with the same shape: end of this page against the start of a later page
        for gap in (2, 3, 4, 5, 6):
            if pi + gap < len(pages):
                ms = pages[pi + gap][1]
                for i in range(max(0, len(ls) - 5), len(ls)):
                    for j in range(min(5, len(ms))):
                        if (len(ls) - i) + j <= 5:
                            add("end of page vs start of a page 2-6 on (control)", pi + gap, ls[i], ms[j])
        for gap, label in [(2, "2 pages on"), (4, "4 pages on"), (10, "10 pages on")]:
            if pi + gap < len(pages):
                for a in ls[::4]:
                    for b in pages[pi + gap][1][::4]:
                        add(label + ", any lines", pi + gap, a, b)

    rng = random.Random(0)
    rows = []
    for cat, per_page in cats.items():
        keys = list(per_page)

        def lift(ks):
            n = sum(per_page[k][0] for k in ks)
            return (sum(per_page[k][1] for k in ks) / (n * exp_core),
                    sum(per_page[k][2] for k in ks) / (n * exp_rest),
                    (sum(per_page[k][1] + per_page[k][2] for k in ks)) / (n * exp_all))
        obs = lift(keys)
        boots = sorted(lift([rng.choice(keys) for _ in keys]) for _ in range(BOOT))
        b_all = sorted(b[2] for b in boots)
        b_core = sorted(b[0] for b in boots)
        b_rest = sorted(b[1] for b in boots)
        ci = lambda xs: f"{xs[int(.025 * BOOT)]:.2f}-{xs[int(.975 * BOOT)]:.2f}"
        rows.append({"block": name, "pairs of lines": cat, "pairs": sum(x[0] for x in per_page.values()),
                     "lift": obs[2], "ci": ci(b_all), "common words": obs[0], "ci_common": ci(b_core),
                     "other words": obs[1], "ci_other": ci(b_rest)})
    order_cats = ["same paragraph, 1-5 lines apart", "same page across a paragraph break, 1-5 lines",
                  "same page, 10-30 lines apart", "across a page break, 1-5 lines",
                  "  of which recto -> its verso (leaf turned)", "  of which verso -> next recto (facing)",
                  "end of page vs start of a page 2-6 on (control)", "next page, any lines", "  of which recto -> its verso (leaf turned) ",
                  "  of which verso -> next recto (facing) ", "2 pages on, any lines", "4 pages on, any lines",
                  "10 pages on, any lines"]
    rows.sort(key=lambda r: order_cats.index(r["pairs of lines"]))

    def contrast(a, b):
        """lift(a) / lift(b), pages resampled together"""
        pa, pb = cats.get(a, {}), cats.get(b, {})
        keys = sorted(set(pa) | set(pb))

        def ratio(ks):
            na = sum(pa[k][0] for k in ks if k in pa)
            nb = sum(pb[k][0] for k in ks if k in pb)
            if not na or not nb:
                return None
            la = sum(pa[k][1] + pa[k][2] for k in ks if k in pa) / na
            lb = sum(pb[k][1] + pb[k][2] for k in ks if k in pb) / nb
            return la / lb if lb else None
        obs = ratio(keys)
        bs = [ratio([rng.choice(keys) for _ in keys]) for _ in range(BOOT * 2)]
        bs = sorted(x for x in bs if x is not None)
        return {"block": name, "contrast": f"{a.strip()}  /  {b.strip()}", "ratio": obs,
                "ci": f"{bs[int(.025 * len(bs))]:.2f}-{bs[int(.975 * len(bs))]:.2f}",
                "p_ratio<=1": sum(x <= 1 for x in bs) / len(bs)}
    cons = [contrast("across a page break, 1-5 lines", "end of page vs start of a page 2-6 on (control)"),
            contrast("across a page break, 1-5 lines", "same paragraph, 1-5 lines apart"),
            contrast("  of which recto -> its verso (leaf turned)", "  of which verso -> next recto (facing)"),
            contrast("same paragraph, 1-5 lines apart", "same page, 10-30 lines apart")]
    return rows, len(pages), n_lines, cons


contrasts = []
out, md = {}, "# 25 does the memory stop at the page?\n\nLift = shared word types between two lines / expected from the block's overall rates. `common` = the block's 60 most widespread words.\n"
for name, sel in BLOCKS:
    rows, n_pages, n_lines, cons = analyse(name, sel)
    out[name] = {"rows": rows, "contrasts": cons}
    contrasts.extend(cons)
    md += f"\n## {name} ({n_pages} pages, {n_lines} lines)\n\n" + table(
        rows, ["pairs of lines", "pairs", "lift", "ci", "common words", "ci_common", "other words", "ci_other"])


# can the next page be picked out from the end of this one?
def successor(name, sel, k=5):
    pages = [(p, [set(l.words) for l in ls]) for p, ls in block_pages(sel)]

    def score(a, b):
        A, B = a[-k:], b[:k]
        return sum(len(x & y) for x in A for y in B) / (len(A) * len(B))
    res = {"r": [], "v": []}
    for i in range(len(pages) - 1):
        if order.index(pages[i + 1][0]) != order.index(pages[i][0]) + 1:
            continue
        true = score(pages[i][1], pages[i + 1][1])
        others = [score(pages[i][1], pages[j][1]) for j in range(len(pages)) if j not in (i, i + 1)]
        pct = (sum(o < true for o in others) + 0.5 * sum(o == true for o in others)) / len(others)
        res[side(pages[i][0])].append(pct)
    out = []
    rng2 = random.Random(1)
    for label, xs in [("all page breaks", res["r"] + res["v"]), ("recto -> its verso", res["r"]),
                      ("verso -> next recto", res["v"])]:
        if not xs:
            continue
        m = sum(xs) / len(xs)
        null = [sum(rng2.random() for _ in xs) / len(xs) for _ in range(5000)]
        out.append({"block": name, "breaks": label, "n": len(xs), "mean percentile of the real next page": m,
                    "in top tenth": sum(x >= 0.9 for x in xs) / len(xs),
                    "p": (1 + sum(x >= m for x in null)) / 5001})
    return out


succ = [r for name, sel in BLOCKS for r in successor(name, sel)]
out["successor"] = succ
md += "\n## is the next page recognisable from the end of this one?\n\nThe last 5 lines of a page against the first 5 lines of every other page in the block; where the real next page ranks (0.5 = chance).\n\n"
md += table(succ, ["block", "breaks", "n", "mean percentile of the real next page", "in top tenth", "p"])
md += "\n## contrasts\n\n" + table(contrasts, ["block", "contrast", "ratio", "ci", "p_ratio<=1"])
save(HERE, "page_memory", out)
write_md(HERE, "page_memory", md)
print(md)
