"""Does the residual replicate?

Exp. 50: Currier B (ZL) keeps 0.24-0.30 bits of structure between neighbouring
words that a generator with every known habit (sheet setting, line gallows,
echo, boundary rule) doesn't make, and it's structured transitions, not
repetition. A result like that has to survive another transcriber and the
other language.

For Currier B and Currier A, in ZL and in IT (Takahashi): fit the
habits-only generator to that text (sigma and hold matched to its sheet
identity and line gallows agreement, as in exp. 50), then measure, on words
of 3+ signs:
  beyond the boundary (exp. 48, inside-sheet baseline), text and generator;
  off-diagonal conditional MI per feature (exp. 50 residual.py).
"""
import math
import pathlib
import random
import re
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "50_settings_generator"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import residual  # noqa: E402
import run as r50  # noqa: E402
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402
from voynich.assemble import Assembler, signs  # noqa: E402

HERE = pathlib.Path(__file__).parent


def load(trans, lang):
    v = Voynich(trans)
    by = defaultdict(list)
    for l in v.lines:
        if l.unit == "P" and l.meta.get("L") == lang and re.fullmatch(r"f\d+[rv]\d*", l.page):
            ws = [w for w in l.words if "?" not in w and "'" not in w and "*" not in w]
            if ws:
                m = v.pages.get(l.page) or {}
                by[(m.get("Q"), m.get("B"))].append((ws, l.para_start))
    return [ls for ls in by.values() if sum(len(w) for w, _ in ls) >= 100]


def generator(sheets, sigma, hold, seed):
    m = Assembler(order=2, recall_p=0.01, edit_p=0.10, window=5, sheet_sigma=sigma, hold=hold).fit(
        [w for s in sheets for w, _ in s], [k for k, (_, p) in enumerate([x for s in sheets for x in s]) if p])
    return [m.fill_sheet([(len(w), p) for w, p in s], seed=seed * 1000 + i) for i, s in enumerate(sheets)]


def long_words(sheets):
    return [[[w for w in l if len(signs(w)) >= 3] for l in s] for s in sheets]


rng = random.Random(0)
rows = []
for trans in ("ZL", "IT"):
    for lang in ("B", "A"):
        S = load(trans, lang)
        text = [[w for w, _ in s] for s in S]
        tgt = (r50.identity(text), r50.gallows_line_ratio(text))
        best, bm = None, 1e9
        for sigma in (0.3, 0.6, 0.9, 1.2):
            for hold in (1.0, 2.5, 4.0):
                g = generator(S, sigma, hold, 1)
                mis = math.hypot(r50.identity(g) - tgt[0], 4 * (r50.gallows_line_ratio(g) - tgt[1]))
                if mis < bm:
                    best, bm = (sigma, hold), mis
        g = generator(S, *best, 7)
        rt = residual.analyse(long_words(text), rng)
        rg = residual.analyse(long_words(g), rng)
        row = {"text": f"{trans} Currier {lang}", "sheets": len(S), "fitted sigma, hold": f"{best[0]}, {best[1]}",
               "beyond boundary: text": r50.beyond_boundary(long_words(text), rng),
               "beyond boundary: generator": r50.beyond_boundary(long_words(g), rng)}
        for f in ("start", "gallows", "ending", "length"):
            row[f"off-diag {f}: text / gen"] = f"{rt[f]['off-diagonal CMI']:.3f} / {rg[f]['off-diagonal CMI']:.3f}"
        row["off-diag sum: text"] = sum(rt[f]["off-diagonal CMI"] for f in rt)
        row["off-diag sum: generator"] = sum(rg[f]["off-diagonal CMI"] for f in rg)
        rows.append(row)
        print(row, flush=True)
save(HERE, "replication", rows)
md = "# 51 the residual in other transliterations and in Currier A (words of 3+ signs)\n\n" + table(
    rows, ["text", "sheets", "fitted sigma, hold", "beyond boundary: text", "beyond boundary: generator",
           "off-diag sum: text", "off-diag sum: generator"])
md += "\n## Per feature\n\n" + table(rows, ["text"] + [f"off-diag {f}: text / gen" for f in ("start", "gallows", "ending", "length")])
write_md(HERE, "replication", md)
print(md)
