"""Each transcribed space, measured in the ink.

run.py compared counts. Here each boundary of ZL's line (a certain space
'.' or a doubtful one ',') is located in the ink: the line's glyphs are laid
out in proportion to their count along the inked extent of the traced row,
and the boundary gets the width of the widest ink gap within 1.5 glyph-widths
of where it should be (0 if there is none). Then, with an independent measure
from exp. 55's boxes:
  widths of certain and doubtful spaces;
  the coupling across the space (last sign -> next first sign) by ink width.
"""
import json
import math
import pathlib
import random
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import run  # noqa: E402
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402
from voynich.assemble import signs  # noqa: E402

HERE = pathlib.Path(__file__).parent
TOL = 1.5


def gap_positions(img_id, idx):
    """Per row: (list of (centre fraction, width in x-heights))."""
    d = idx[img_id]
    disp = d["display"]
    s = disp["scale"]
    from PIL import Image
    ink = np.array(Image.open(run.SRC / "img" / "ink_stage1" / f"{img_id}.png"))[:, :, 3] > 0
    L = json.loads((run.SRC / "data" / "lines" / f"{img_id}.json").read_text())
    xh = L["xheight"] * s
    out = []
    for ln in L["lines"]:
        pts = (np.array(ln["pts"], float) - [disp["scan_x0"], disp["scan_y0"]]) * s
        if len(pts) < 2:
            out.append(None)
            continue
        cum = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(pts, axis=0).T))])
        t = np.arange(0, cum[-1], run.STEP)
        x, y = np.interp(t, cum, pts[:, 0]), np.interp(t, cum, pts[:, 1])
        col = np.zeros(len(t), bool)
        xx = np.clip(x.astype(int), 0, ink.shape[1] - 1)
        for dy in np.arange(-run.BAND * xh, run.BAND * xh + 0.01, run.STEP):
            col |= ink[np.clip((y + dy).astype(int), 0, ink.shape[0] - 1), xx]
        if not col.any():
            out.append(None)
            continue
        first, last = int(np.argmax(col)), len(col) - 1 - int(np.argmax(col[::-1]))
        span = max(1, last - first)
        gaps, i = [], first
        while i <= last:
            if not col[i]:
                j = i
                while j <= last and not col[j]:
                    j += 1
                gaps.append((((i + j) / 2 - first) / span, (j - i) * run.STEP / xh))
                i = j
            else:
                i += 1
        out.append(gaps)
    return out


def separators(split_words, joined_words):
    """Which boundaries of the split line are doubtful (absent when joined)."""
    seps, j, acc = [], 0, ""
    for k, w in enumerate(split_words):
        acc += w
        if k == len(split_words) - 1:
            break
        if j < len(joined_words) and acc == joined_words[j]:
            seps.append(".")
            acc = ""
            j += 1
        else:
            seps.append(",")
    return seps


idx = {d["image"]: d for d in json.loads((run.SRC / "data" / "index.json").read_text())}
v, vj = Voynich("ZL", commas="split"), Voynich("ZL", commas="join")
bounds = []
for img_id, d in idx.items():
    if d.get("kind") != "page" or not (run.SRC / "data" / "lines" / f"{img_id}.json").exists():
        continue
    zs, zj = run.zl_lines(v, d["folio"]), run.zl_lines(vj, d["folio"])
    g = gap_positions(img_id, idx)
    if len(zs) != len(g) or len(zs) <= 3:
        continue
    for a, b, gg in zip(zs, zj, g):
        if a.unit != "P" or not gg or len(a.words) < 2 or any("?" in w for w in a.words):
            continue
        seps = separators(a.words, b.words)
        sz = [len(signs(w)) for w in a.words]
        total = sum(sz)
        pos = 0
        for k in range(len(a.words) - 1):
            pos += sz[k]
            f = pos / total
            near = [wd for c, wd in gg if abs(c - f) <= TOL / total]
            bounds.append({"folio": d["folio"], "lang": a.meta.get("L"), "sep": seps[k],
                           "left": signs(a.words[k])[-1], "right": signs(a.words[k + 1])[0],
                           "width": max(near) if near else 0.0})

rng = random.Random(0)


def coupling(pairs, shuffles=30):
    def mi(ps):
        N = Counter(ps)
        tot = sum(N.values())
        L_, R_ = Counter(), Counter()
        for (x, y), c in N.items():
            L_[x] += c
            R_[y] += c
        return sum(c / tot * math.log2(c * tot / (L_[x] * R_[y])) for (x, y), c in N.items())
    right = [b for _, b in pairs]
    base = 0
    for _ in range(shuffles):
        rng.shuffle(right)
        base += mi([(a, b) for (a, _), b in zip(pairs, right)])
    return mi(pairs) - base / shuffles


rows = []
for sep in (".", ","):
    w = [b["width"] for b in bounds if b["sep"] == sep]
    rows.append({"ZL separator": "certain space" if sep == "." else "doubtful space", "boundaries": len(w),
                 "mean ink gap (x-heights)": float(np.mean(w)), "median": float(np.median(w)),
                 "share wider than 0.8": float(np.mean(np.array(w) >= 0.8))})
ws = sorted(b["width"] for b in bounds if b["sep"] == ".")
t1, t2 = ws[len(ws) // 3], ws[2 * len(ws) // 3]
crow = []
for name, sel in (("narrowest third", lambda x: x <= t1), ("middle third", lambda x: t1 < x <= t2),
                  ("widest third", lambda x: x > t2)):
    ps = [(b["left"], b["right"]) for b in bounds if b["sep"] == "." and sel(b["width"])]
    crow.append({"certain spaces, ink gap": name, "pairs": len(ps), "last sign -> next first sign (bits)": coupling(ps)})
save(HERE, "boundaries", {"widths": rows, "coupling": crow, "n": len(bounds)})
md = (f"# 57 each transcribed space measured in the ink ({len(bounds)} boundaries)\n\n" +
      table(rows, ["ZL separator", "boundaries", "mean ink gap (x-heights)", "median", "share wider than 0.8"]) +
      "\n## Coupling across certain spaces, by ink width\n\n" +
      table(crow, ["certain spaces, ink gap", "pairs", "last sign -> next first sign (bits)"]))
write_md(HERE, "boundaries", md)
print(md)
