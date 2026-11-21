"""Is the sheet setting a writing session? Measure the handwriting.

Exps. 40-42: the way words are built is set per sheet. Two readings: a
deliberate setting (a key, a new choice per sheet), or simply the state of a
writer at one sitting. A sitting leaves marks in the handwriting too: how
wide the glyphs are drawn, how tightly lines are packed, how wide the
spaces are. Those can be read off the page.

From the word boxes (Rozanova & Temerev archive, exp. 55), per page, all
scale-free (divided by the page's median box height, since every page was
photographed at its own scale):
  glyph width: median of box width / number of EVA signs in the word
  line spacing: median vertical distance between consecutive lines
  space width: median gap between words in a line
  words per line
Then, as in exp. 42: are pages of the same sheet more alike in these than
pages that face each other in the binding but belong to different sheets?
And across pairs of pages in the same hand and section, does a difference
in handwriting go with a difference in fork setting (Mantel test)?
"""
import json
import math
import pathlib
import random
import re
import statistics
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402
from voynich.assemble import signs  # noqa: E402
from voynich.forks import profile  # noqa: E402

HERE = pathlib.Path(__file__).parent
BOXES = HERE.parent.parent / "data" / "external" / "voynich-units-boxes"
PHYS = ["glyph width", "line spacing", "space width", "words per line"]


def page_physics(path):
    d = json.loads(path.read_text())
    voc = [x[0] for x in d[0]]
    toks = d[1]
    if len(toks) < 40:
        return None
    mh = statistics.median([t[4] for t in toks]) or 1
    lines, cur, prev = [], [], None
    for t in toks:
        if prev is not None and (t[1] < prev[1] - 3 or abs(t[2] - prev[2]) >= 0.8 * mh):
            lines.append(cur)
            cur = []
        cur.append(t)
        prev = t
    lines.append(cur)
    gw = [t[3] / max(1, len(signs(voc[t[0]]))) / mh for t in toks]
    ys = [statistics.median([t[2] for t in l]) for l in lines]
    ls = [b - a for a, b in zip(ys, ys[1:]) if 0 < b - a < 4 * mh]
    gaps = [(b[1] - (a[1] + a[3])) / mh for l in lines for a, b in zip(l, l[1:])]
    if len(ls) < 5 or len(gaps) < 20:
        return None
    return np.array([statistics.median(gw), statistics.median(ls) / mh, statistics.median(gaps),
                     statistics.mean(len(l) for l in lines)]), [voc[t[0]] for t in toks]


v = Voynich("ZL")
phys, words, meta = {}, {}, {}
for f in sorted(BOXES.glob("*.js")):
    if not re.fullmatch(r"f\d+[rv]", f.stem) or f.stem not in v.pages:
        continue
    r = page_physics(f)
    if r is None:
        continue
    phys[f.stem], words[f.stem] = r
    m = v.pages[f.stem]
    meta[f.stem] = (m.get("H"), m.get("I"), (m.get("Q"), m.get("B")))

groups = {"hand 1 herbal (A)": ("1", "H"), "hand 1 pharmaceutical (A)": ("1", "P"),
          "hand 2 herbal (B)": ("2", "H"), "hand 2 bathing (B)": ("2", "B"), "hand 3 stars (B)": ("3", "S")}


def zscore(X):
    return (X - X.mean(0)) / (X.std(0) + 1e-9)


rng = np.random.default_rng(0)
rows, mantel = [], []
for name, (h, sec) in groups.items():
    ps = [p for p in phys if meta[p][0] == h and meta[p][1] == sec]
    if len(ps) < 8:
        continue
    Z = zscore(np.array([phys[p] for p in ps]))
    idx = {p: i for i, p in enumerate(ps)}
    D = ((Z[:, None] - Z[None]) ** 2).sum(-1)
    base = D[np.triu_indices(len(ps), 1)].mean()
    rel = defaultdict(list)
    folios = sorted({int(p[1:-1]) for p in ps})
    sheet = {f: meta.get(f"f{f}r", meta.get(f"f{f}v"))[2] for f in folios}
    for f in folios:
        if f"f{f}r" in idx and f"f{f}v" in idx:
            rel["same leaf"].append(D[idx[f"f{f}r"], idx[f"f{f}v"]] / base)
        if f + 1 in folios and sheet[f] != sheet[f + 1] and f"f{f}v" in idx and f"f{f + 1}r" in idx:
            rel["facing in the binding, other sheet"].append(D[idx[f"f{f}v"], idx[f"f{f + 1}r"]] / base)
    by_sheet = defaultdict(list)
    for f in folios:
        by_sheet[sheet[f]].append(f)
    for fs in by_sheet.values():
        if len(fs) == 2:
            a, b = sorted(fs)
            if b == a + 1:
                continue
            for x, y in ((f"f{a}r", f"f{b}r"), (f"f{a}r", f"f{b}v"), (f"f{a}v", f"f{b}r"), (f"f{a}v", f"f{b}v")):
                if x in idx and y in idx:
                    rel["other leaf of the same sheet"].append(D[idx[x], idx[y]] / base)
    row = {"pages": name, "n": len(ps)}
    for k in ("same leaf", "other leaf of the same sheet", "facing in the binding, other sheet"):
        row[k] = f"{np.mean(rel[k]):.2f} (n={len(rel[k])})" if rel[k] else "-"
    rows.append(row)
    # Mantel: handwriting distance vs fork-profile distance
    F = np.array([profile([w for w in words[p]]) for p in ps])
    DF = ((F[:, None] - F[None]) ** 2).sum(-1)
    iu = np.triu_indices(len(ps), 1)
    r_obs = np.corrcoef(D[iu], DF[iu])[0, 1]
    null = []
    for _ in range(2000):
        perm = rng.permutation(len(ps))
        null.append(np.corrcoef(D[iu], DF[perm][:, perm][iu])[0, 1])
    mantel.append({"pages": name, "n": len(ps), "r (handwriting vs fork setting)": r_obs,
                   "p": (1 + sum(x >= r_obs for x in null)) / 2001})
    print(row, mantel[-1], flush=True)

save(HERE, "hand_per_sheet", {"rows": rows, "mantel": mantel})
md = ("# 56 handwriting per sheet\n\nDistance between pages in four scale-free handwriting measures (glyph width, "
      "line spacing, space width, words per line), relative to any two pages of the group (1.00).\n\n")
md += table(rows, ["pages", "n", "same leaf", "other leaf of the same sheet", "facing in the binding, other sheet"])
md += "\n## Does handwriting go with the fork setting? (Mantel test over page pairs)\n\n" + table(
    mantel, ["pages", "n", "r (handwriting vs fork setting)", "p"])
write_md(HERE, "hand_per_sheet", md)
print(md)
