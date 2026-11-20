"""Can habits alone make the 0.30 bits?

Exp. 48 left one thing my generator doesn't make: neighbouring words share
0.30 bits of their choices (Currier B) beyond the glyphs at the space and
the sheet's setting; the generator makes 0.02. Before reading that as a
message, give the generator the two habits it lacks and see how much they
explain:
  a setting per sheet: random weights on word starts, gallows and endings,
    exp(N(0, sigma)), drawn once per sheet (exps. 40-42);
  a favoured gallows per line, weight `hold` (exp. 49).
sigma and hold are set by matching Currier B's sheet identity and its
same-line gallows agreement; the measure of interest (exp. 48's conditional
MI, inside-sheet baseline) is not used for fitting.
"""
import math
import pathlib
import random
import re
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402
from voynich.assemble import GALLOWS, Assembler, signs  # noqa: E402
from voynich.forks import profile  # noqa: E402

HERE = pathlib.Path(__file__).parent
FEATS = {"start": lambda s: tuple(s[:2]), "gallows": lambda s: next((x for x in s if x in GALLOWS), "-"),
         "ending": lambda s: tuple(s[-2:]), "length": lambda s: min(len(s), 6)}

v = Voynich("ZL")
by = defaultdict(list)
for l in v.lines:
    if l.unit == "P" and l.meta.get("L") == "B" and re.fullmatch(r"f\d+[rv]\d*", l.page):
        ws = [w for w in l.words if "?" not in w and "'" not in w]
        if ws:
            m = v.pages.get(l.page) or {}
            by[(m.get("Q"), m.get("B"))].append((ws, l.para_start))
SHEETS = [ls for ls in by.values() if sum(len(w) for w, _ in ls) >= 100]
B = [[w for w, _ in s] for s in SHEETS]


def identity(sheets):
    H = [([w for l in s[0::2] for w in l], [w for l in s[1::2] for w in l]) for s in sheets]
    A = np.array([profile(a) for a, _ in H])
    Bm = np.array([profile(b) for _, b in H])
    D = ((A[:, None] - Bm[None]) ** 2).sum(-1)
    n = len(H)
    return sum(int(np.argmin(M[i])) == i for M in (D, D.T) for i in range(n)) / (2 * n)


def gallows_line_ratio(sheets):
    g = FEATS["gallows"]
    same = n_same = diff = n_diff = 0
    for lines in sheets:
        ls = [[g(signs(w)) for w in l[1:]] for l in lines if len(l) > 3]
        for i, l in enumerate(ls):
            for d in (2, 3, 4):
                for k in range(len(l) - d):
                    same += l[k] == l[k + d]
                    n_same += 1
            for j in range(i + 1, min(i + 4, len(ls))):
                m = ls[j]
                for d in (2, 3, 4):
                    for k in range(min(len(l), len(m)) - d):
                        diff += l[k] == m[k + d]
                        n_diff += 1
    return (same / n_same) / (diff / n_diff)


def cmi(trip):
    nz, nxz, nyz, nxyz = Counter(), Counter(), Counter(), Counter()
    for x, y, z in trip:
        nz[z] += 1
        nxz[x, z] += 1
        nyz[y, z] += 1
        nxyz[x, y, z] += 1
    n = len(trip)
    return sum(c / n * math.log2(c * nz[z] / (nxz[x, z] * nyz[y, z])) for (x, y, z), c in nxyz.items())


def beyond_boundary(sheets, rng, perms=15):
    pairs, sheet_of = [], []
    for k, lines in enumerate(sheets):
        for l in lines:
            seq = [signs(w) for w in l]
            for a, b in zip(seq, seq[1:]):
                pairs.append((a, b))
                sheet_of.append(k)
    total = 0
    for gx in FEATS.values():
        for gy in FEATS.values():
            trip = [(gx(a), gy(b), (a[-1], b[0])) for a, b in pairs]
            groups = defaultdict(list)
            for k, t in enumerate(trip):
                groups[t[2], sheet_of[k]].append(k)
            base = 0
            for _ in range(perms):
                xs = [t[0] for t in trip]
                for idx in groups.values():
                    vals = [xs[k] for k in idx]
                    rng.shuffle(vals)
                    for k, x in zip(idx, vals):
                        xs[k] = x
                base += cmi([(x, t[1], t[2]) for x, t in zip(xs, trip)])
            total += cmi(trip) - base / perms
    return total


def generate(sigma, hold, seed):
    m = Assembler(order=2, recall_p=0.01, edit_p=0.10, window=5, sheet_sigma=sigma, hold=hold).fit(
        [w for s in SHEETS for w, _ in s], [k for k, (_, p) in enumerate([x for s in SHEETS for x in s]) if p])
    return [m.fill_sheet([(len(w), p) for w, p in s], seed=seed * 1000 + i) for i, s in enumerate(SHEETS)]


if __name__ == "__main__":
    rng = random.Random(0)
    target = {"sheet identity": identity(B), "gallows line ratio": gallows_line_ratio(B)}
    print("target", target, flush=True)
    grid = []
    for sigma in (0.0, 0.3, 0.6, 0.9):
        for hold in (1.0, 1.5, 2.5):
            gs = [generate(sigma, hold, s) for s in (1, 2)]
            r = {"sigma": sigma, "hold": hold,
                 "sheet identity": np.mean([identity(g) for g in gs]),
                 "gallows line ratio": np.mean([gallows_line_ratio(g) for g in gs])}
            r["misfit"] = math.hypot(r["sheet identity"] - target["sheet identity"],
                                     4 * (r["gallows line ratio"] - target["gallows line ratio"]))
            grid.append(r)
            print({k: round(x, 3) for k, x in r.items()}, flush=True)
    best = min(grid, key=lambda r: r["misfit"])
    rows = [{"text": "Currier B", **target, "beyond the boundary (bits)": beyond_boundary(B, rng)}]
    for label, sg, hd in (("generator, no settings", 0.0, 1.0),
                          (f"generator, sheet setting sigma={best['sigma']}, line gallows hold={best['hold']}",
                           best["sigma"], best["hold"]),
                          ("generator, strong settings sigma=0.9, hold=2.5", 0.9, 2.5)):
        g = generate(sg, hd, 7)
        rows.append({"text": label, "sheet identity": identity(g), "gallows line ratio": gallows_line_ratio(g),
                     "beyond the boundary (bits)": beyond_boundary(g, rng)})
        print(rows[-1], flush=True)
    save(HERE, "settings", {"target": target, "grid": grid, "rows": rows})
    md = "# 50 habits only\n\n## Fit of sigma and hold to Currier B\n\n" + table(
        grid, ["sigma", "hold", "sheet identity", "gallows line ratio", "misfit"])
    md += f"\nCurrier B: sheet identity {target['sheet identity']:.3f}, gallows line ratio {target['gallows line ratio']:.3f}\n"
    md += "\n## Does it make the link between neighbours?\n\n" + table(
        rows, ["text", "sheet identity", "gallows line ratio", "beyond the boundary (bits)"])
    write_md(HERE, "settings", md)
    print(md)
