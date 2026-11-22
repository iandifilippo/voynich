"""Spaces in the ink.

Exp. 55 used word boxes drawn by a transcriber. Here the spaces are read from
the ink itself: daniilvaino/VoynichManuscriptOCR publishes, for all 227 page
images, a mask of the ink and a traced line along the middle of every row of
text (two independent tracing runs agreeing or a human check). Along each row
line, a band of +-0.9 x-heights is scanned; every stretch with no ink between
two inked stretches is a gap, measured in x-heights.

1. The gap widths of the whole manuscript: is there a clear second mode, a
   'word space', separate from the small gaps between glyphs of a word?
2. Words per line counted from the ink (gaps wider than a threshold, + 1)
   against the transliterations' counts for the same lines, with doubtful
   spaces read as spaces or not. Lines are matched by order on pages where the
   traced lines and ZL's lines are equal in number; only lines of running
   text (paragraphs) are compared.
"""
import json
import pathlib
import re
import sys
from collections import Counter

import numpy as np
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402

HERE = pathlib.Path(__file__).parent
SRC = HERE.parent.parent / "data" / "external" / "VoynichManuscriptOCR"  # see data/README.md
BAND = 0.9
STEP = 0.5


def row_gaps(img_id, idx):
    d = idx[img_id]
    disp = d["display"]
    s = disp["scale"]
    ink = np.array(Image.open(SRC / "img" / "ink_stage1" / f"{img_id}.png"))[:, :, 3] > 0
    L = json.loads((SRC / "data" / "lines" / f"{img_id}.json").read_text())
    xh = L["xheight"] * s
    out = []
    for ln in L["lines"]:
        pts = (np.array(ln["pts"], float) - [disp["scan_x0"], disp["scan_y0"]]) * s
        if len(pts) < 2:
            out.append(None)
            continue
        cum = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(pts, axis=0).T))])
        t = np.arange(0, cum[-1], STEP)
        x, y = np.interp(t, cum, pts[:, 0]), np.interp(t, cum, pts[:, 1])
        col = np.zeros(len(t), bool)
        xx = np.clip(x.astype(int), 0, ink.shape[1] - 1)
        for dy in np.arange(-BAND * xh, BAND * xh + 0.01, STEP):
            col |= ink[np.clip((y + dy).astype(int), 0, ink.shape[0] - 1), xx]
        if not col.any():
            out.append(None)
            continue
        first, last = int(np.argmax(col)), len(col) - 1 - int(np.argmax(col[::-1]))
        gaps, i = [], first
        while i <= last:
            if not col[i]:
                j = i
                while j <= last and not col[j]:
                    j += 1
                gaps.append((j - i) * STEP / xh)
                i = j
            else:
                i += 1
        out.append(gaps)
    return out


def zl_lines(v, folio):
    return [l for l in v.lines if l.page == folio]


if __name__ == "__main__":
    idx = {d["image"]: d for d in json.loads((SRC / "data" / "index.json").read_text())}
    v = Voynich("ZL", commas="split")
    vj = Voynich("ZL", commas="join")
    all_gaps, rows = [], []
    matched = []
    for img_id, d in idx.items():
        if d.get("kind") != "page" or not (SRC / "data" / "lines" / f"{img_id}.json").exists():
            continue
        try:
            g = row_gaps(img_id, idx)
        except FileNotFoundError:
            continue
        for x in g:
            if x:
                all_gaps += x
        zs = zl_lines(v, d["folio"])
        zj = zl_lines(vj, d["folio"])
        if len(zs) == len(g) and len(zs) > 3:
            for a, b, gg in zip(zs, zj, g):
                if a.unit == "P" and gg:
                    matched.append((d["folio"], a.meta.get("L"), len(a.words), len(b.words), gg))
    hist = Counter(min(int(x / 0.1), 40) for x in all_gaps)
    n = len(all_gaps)
    hrows = [{"gap (x-heights)": f"{i / 10:.1f}-{(i + 1) / 10:.1f}" if i < 40 else "4.0+", "share": hist[i] / n}
             for i in range(41)]
    for T in (0.6, 0.8, 1.0, 1.2):
        ink_n = np.array([sum(1 for x in gg if x >= T) + 1 for *_, gg in matched])
        zl_s = np.array([a for _, _, a, _, _ in matched])
        zl_j = np.array([b for _, _, _, b, _ in matched])
        rows.append({"space if gap >= (x-heights)": T, "lines": len(matched),
                     "words per line, ink": ink_n.mean(),
                     "ZL, doubtful spaces as spaces": zl_s.mean(), "ZL, doubtful spaces joined": zl_j.mean(),
                     "lines where ink = ZL (spaces)": float(np.mean(ink_n == zl_s)),
                     "lines where ink = ZL (joined)": float(np.mean(ink_n == zl_j)),
                     "r ink vs ZL": float(np.corrcoef(ink_n, zl_s)[0, 1])})
        print(rows[-1], flush=True)
    save(HERE, "ink_spaces", {"histogram": hrows, "counts": rows, "pages": len({m[0] for m in matched})})
    md = (f"# 57 spaces in the ink\n\n{n} gaps between inked stretches along {sum(1 for _ in all_gaps) and len(idx)} "
          "page images' row lines.\n\n## Gap widths\n\n") + table(hrows, ["gap (x-heights)", "share"])
    md += f"\n## Words per line, ink against ZL ({len(matched)} paragraph lines on {len({m[0] for m in matched})} pages)\n\n"
    md += table(rows, ["space if gap >= (x-heights)", "lines", "words per line, ink", "ZL, doubtful spaces as spaces",
                       "ZL, doubtful spaces joined", "lines where ink = ZL (spaces)", "lines where ink = ZL (joined)",
                       "r ink vs ZL"])
    write_md(HERE, "ink_spaces", md)
    print(md[md.index("## Words per line"):])
