"""What carries the page setting: the leaf, the sheet, or one side of a sheet?

Exp. 41's clusters inside a section were made of whole leaves (recto and
verso together) and of conjoint leaves, the two halves of one folded sheet.
In the stars quire one side of a sheet (f107v with f112r) fell in one cluster
and the other side (f107r with f112v) in the other. That would mean the
setting was chosen per sheet, or per side of an unfolded sheet, before the
sheets were folded and bound.

A sheet is two leaves, a (earlier in the book) and b, four pages:
  inside of the sheet:  a verso, b recto
  outside of the sheet: a recto, b verso
For every pair of pages in the same hand and section, the distance between
their fork profiles (voynich.forks), relative to the mean distance of all
pairs in that group, by how the two pages are related:
  same leaf (recto - verso)
  same side of one sheet (a_v - b_r, a_r - b_v)
  opposite sides of one sheet (a_r - b_r, a_v - b_v)
  neighbours in the binding on different sheets (verso of one folio - recto of the next)
  any two pages in the group (1 by construction)
Intervals by resampling sheets. Sheets where a and b are consecutive folios
(the centre of a quire) are left out, since there a_v and b_r also face each
other in the bound book.
"""
import pathlib
import random
import re
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich
from voynich.forks import profile

HERE = pathlib.Path(__file__).parent
MIN_WORDS = 60
BOOT = 2000
KINDS = ["same leaf", "same side of a sheet", "opposite sides of a sheet", "binding neighbours, other sheet"]

v = Voynich("ZL")
words, meta = defaultdict(list), {}
for l in v.lines:
    if l.unit == "P" and re.fullmatch(r"f\d+[rv]", l.page):
        words[l.page] += [w for w in l.words if "?" not in w and "'" not in w]
        meta[l.page] = (l.meta.get("H"), l.meta.get("I"))
prof = {p: profile(ws) for p, ws in words.items() if len(ws) >= MIN_WORDS}

groups = {"hand 1 herbal (A)": ("1", "H"), "hand 1 pharmaceutical (A)": ("1", "P"),
          "hand 2 herbal (B)": ("2", "H"), "hand 2 bathing (B)": ("2", "B"), "hand 3 stars (B)": ("3", "S")}


def sheet_of(folio):
    m = v.pages.get(f"f{folio}r") or v.pages.get(f"f{folio}v")
    return (m.get("Q"), m.get("B")) if m else None


def pairs_for(ps):
    """Relation-labelled page pairs, grouped by sheet (for resampling)."""
    folios = sorted({int(p[1:-1]) for p in ps})
    by_sheet = defaultdict(list)
    for f in folios:
        by_sheet[sheet_of(f)].append(f)
    out = defaultdict(lambda: defaultdict(list))
    for key, fs in by_sheet.items():
        for f in fs:
            out[key]["same leaf"].append((f"f{f}r", f"f{f}v"))
        if len(fs) == 2:
            a, b = sorted(fs)
            if b == a + 1:
                continue
            out[key]["same side of a sheet"] += [(f"f{a}v", f"f{b}r"), (f"f{a}r", f"f{b}v")]
            out[key]["opposite sides of a sheet"] += [(f"f{a}r", f"f{b}r"), (f"f{a}v", f"f{b}v")]
    for f in folios:
        if f + 1 in folios and sheet_of(f) != sheet_of(f + 1):
            out[sheet_of(f)]["binding neighbours, other sheet"].append((f"f{f}v", f"f{f + 1}r"))
    return out


def measure(group_pages, by_sheet, keys):
    X = np.array([prof[p] for p in group_pages])
    base = np.mean([((X[i] - X[j]) ** 2).sum() for i in range(len(X)) for j in range(i + 1, len(X))])
    res = {}
    for kind in KINDS:
        ds = [((prof[a] - prof[b]) ** 2).sum() / base for k in keys for a, b in by_sheet[k][kind]
              if a in prof and b in prof]
        res[kind] = (float(np.mean(ds)) if ds else float("nan"), len(ds))
    return res


rng = random.Random(0)
rows, contrasts = [], []
for name, key in groups.items():
    ps = [p for p in prof if meta[p] == key]
    by_sheet = pairs_for(ps)
    keys = list(by_sheet)
    obs = measure(ps, by_sheet, keys)
    boots = [measure(ps, by_sheet, [rng.choice(keys) for _ in keys]) for _ in range(BOOT)]
    row = {"pages": name, "n pages": len(ps)}
    for kind in KINDS:
        m, n = obs[kind]
        b = sorted(x[kind][0] for x in boots if x[kind][0] == x[kind][0])
        row[kind] = f"{m:.2f} [{b[int(.025 * len(b))]:.2f}, {b[int(.975 * len(b))]:.2f}] n={n}" if n else "-"
    rows.append(row)
    for k1, k2 in [("same side of a sheet", "opposite sides of a sheet"),
                   ("same side of a sheet", "binding neighbours, other sheet"),
                   ("same leaf", "same side of a sheet")]:
        d = [x[k1][0] - x[k2][0] for x in boots if x[k1][1] and x[k2][1]]
        if obs[k1][1] and obs[k2][1] and d:
            d.sort()
            contrasts.append({"pages": name, "contrast": f"{k1}  minus  {k2}", "difference": obs[k1][0] - obs[k2][0],
                              "95% interval": f"[{d[int(.025 * len(d))]:.2f}, {d[int(.975 * len(d))]:.2f}]",
                              "share of resamples > 0": sum(x > 0 for x in d) / len(d)})
    print(row, flush=True)

save(HERE, "setting_unit", {"rows": rows, "contrasts": contrasts})
md = "# 42 what carries the page setting\n\nDistance between fork profiles, relative to any two pages of the group (1.00); lower = more alike.\n\n"
md += table(rows, ["pages", "n pages"] + KINDS)
md += "\n## Contrasts (negative = the first relation is more alike)\n\n" + table(
    contrasts, ["pages", "contrast", "difference", "95% interval", "share of resamples > 0"])
write_md(HERE, "setting_unit", md)
print(md)
