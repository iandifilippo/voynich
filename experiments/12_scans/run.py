"""What the scans say about lines and spaces (quire 20, text-only pages).

Images: the page JPEGs embedded in Yale's PDF of MS 408 (about 1100x1536 px,
600 ppi as stored). Put them in data/scans/q20/img-000.jpg ... img-022.jpg
with `pdfimages -j -f 183 -l 205 <pdf> data/scans/q20/img` (PDF pages 183-205
are f103r-f108v, f111r-f116r).

Part A: count text lines on each page from the image alone and compare with
the number of paragraph lines in ZL. Detector settings are tuned on every
other page and the error is reported on the pages it never saw.

Part B: on pages where the line count matches exactly, pair image lines with
ZL lines in order and ask how the large gaps in each image line relate to
ZL's word separators: '.' (certain space) and ',' (uncertain space).
Fit gaps ~ a*dots + b*commas + c. If uncertain spaces are as real as certain
ones, b should be close to a; if they are mostly not visible as gaps, b near 0.
"""
import itertools
import json
import pathlib
import re
import sys

import numpy as np
from PIL import Image
from scipy import ndimage, signal
from skimage.filters import threshold_otsu

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import scan
from voynich.corpus import DATA

HERE = pathlib.Path(__file__).parent
SCANS = DATA / "scans" / "q20"
PAGES = ["f103r", "f103v", "f104r", "f104v", "f105r", "f105v", "f106r", "f106v", "f107r", "f107v",
         "f108r", "f108v", "f111r", "f111v", "f112r", "f112v", "f113r", "f113v", "f114r", "f114v",
         "f115r", "f115v", "f116r"]

# ZL paragraph lines with their separators, straight from the file
zl = {}
for raw in open(DATA / "ZL3b-n.txt", encoding="latin-1"):
    m = re.match(r"^<(f\d+[rv]\d?)\.(\d+),[+@=&~*]?P\w*>\s*(.*)$", raw.rstrip("\n"))
    if not m:
        continue
    page, _, text = m.groups()
    t = re.sub(r"<![^>]*>", "", text)
    t = re.sub(r"\[([^:\]]*)[^\]]*\]", r"\1", t)
    t = re.sub(r"<[^>]*>", "", t)
    zl.setdefault(page, []).append({"dots": t.count("."), "commas": t.count(","),
                                    "glyphs": len(re.sub(r"[^a-z]", "", t))})


def prepare(path):
    g = scan.load_gray(path)
    ink = scan.binarize(g)
    r0, r1, c0, c1 = scan.text_box(ink)
    ink = ink[r0:r1, c0:c1]
    a = scan.best_skew(ink)
    return ndimage.rotate(ink.astype(np.uint8), a, reshape=False, order=0).astype(bool), a


def peaks(ink, strip, smooth, dist, prom):
    w = ink.shape[1]
    a, b = {"left": (0, .45), "mid": (.25, .75), "all": (0, 1)}[strip]
    prof = ndimage.gaussian_filter1d(ink[:, int(w * a):int(w * b)].sum(axis=1).astype(float), smooth)
    pk, _ = signal.find_peaks(prof, distance=dist, prominence=prof.max() * prom)
    return pk


ink, angle = {}, {}
for i, p in enumerate(PAGES):
    path = SCANS / f"img-{i:03d}.jpg"
    if not path.exists() or Image.open(path).width < 900:   # f104r is stored at half resolution
        continue
    ink[p], angle[p] = prepare(path)

keys = [p for p in PAGES if p in ink]
calib, test = keys[::2], keys[1::2]
grid = list(itertools.product(["left", "mid", "all"], [1.5, 2, 3], [10, 12, 14, 16], [0.03, 0.06, 0.1]))
scores = []
for params in grid:
    err = [abs(len(peaks(ink[p], *params)) - len(zl[p])) for p in calib]
    scores.append((sum(err) / len(err), params))
scores.sort()
best = scores[0][1]

rows_a = []
for p in keys:
    n = len(peaks(ink[p], *best))
    rows_a.append({"page": p, "split": "tuning" if p in calib else "held-out", "zl_lines": len(zl[p]),
                   "detected": n, "error": n - len(zl[p]), "skew_deg": angle[p]})
held = [r for r in rows_a if r["split"] == "held-out"]
mae = sum(abs(r["error"]) for r in held) / len(held)
within1 = sum(abs(r["error"]) <= 1 for r in held)

# ---- Part B
matched = []
for p in keys:
    pk = peaks(ink[p], *best)
    if len(pk) == len(zl[p]):
        matched.append(p)

per_line = []
for p in matched:
    pk = peaks(ink[p], *best)
    for y, z in zip(pk, zl[p]):
        gaps, (x0, x1) = scan.line_gaps(ink[p], int(y), half=7)
        per_line.append((p, gaps, z))

THRESHOLDS = [8, 10, 12, 14, 16, 18]
fits = []
rng = np.random.default_rng(0)
for thr in THRESHOLDS:
    X = np.array([[z["dots"], z["commas"], 1.0] for _, _, z in per_line])
    y = np.array([sum(g >= thr for g in gaps) for _, gaps, _ in per_line], dtype=float)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    boots = []
    for _ in range(2000):
        idx = rng.integers(0, len(y), len(y))
        c, *_ = np.linalg.lstsq(X[idx], y[idx], rcond=None)
        boots.append(c)
    boots = np.array(boots)
    ratio = boots[:, 1] / np.where(boots[:, 0] == 0, np.nan, boots[:, 0])
    fits.append({"min_gap_px": thr, "mean_big_gaps": float(y.mean()),
                 "a_dots": float(coef[0]), "b_commas": float(coef[1]),
                 "b_over_a": float(coef[1] / coef[0]),
                 "ratio_ci_low": float(np.nanpercentile(ratio, 2.5)), "ratio_ci_high": float(np.nanpercentile(ratio, 97.5)),
                 "r_dots": float(np.corrcoef(y, X[:, 0])[0, 1])})
fit = {"lines": len(per_line), "pages": matched,
       "total_dots": int(sum(z["dots"] for _, _, z in per_line)),
       "total_commas": int(sum(z["commas"] for _, _, z in per_line)),
       "by_threshold": fits}
all_gaps = [g for _, gaps, _ in per_line for g in gaps]
hist = np.bincount(np.minimum(all_gaps, 40))

save(HERE, "scans", {"params": dict(zip(["strip", "smooth", "distance", "prominence"], best)),
                     "part_a": rows_a, "held_out_mae": mae, "held_out_within1": within1, "part_b": fit,
                     "gap_histogram_px": hist.tolist()})
md = "# 12 scans: lines and spaces\n\n"
md += f"Detector settings picked on {len(calib)} pages: strip={best[0]}, smoothing={best[1]}, min distance={best[2]} px, prominence={best[3]}.\n\n"
md += f"Held-out pages ({len(held)}): mean absolute error {mae:.1f} lines, within one line on {within1}/{len(held)}.\n\n"
md += table(rows_a, ["page", "split", "zl_lines", "detected", "error", "skew_deg"])
if per_line:
    md += f"\n## spaces\n\n{fit['lines']} lines on {len(matched)} pages where the counts match ({', '.join(matched)}). ZL marks {fit['total_dots']} certain and {fit['total_commas']} uncertain spaces on them.\n\n"
    md += "Gap widths are bimodal (peak at 2-3 px between glyphs, second bump around 10-16 px), but the two overlap, so the fit is repeated for several minimum gap widths.\n\n"
    md += "big_gaps = a x dots + b x commas + c\n\n"
    md += table(fits, ["min_gap_px", "mean_big_gaps", "a_dots", "b_commas", "b_over_a", "ratio_ci_low", "ratio_ci_high", "r_dots"])
    md += "\nb/a near 1: an uncertain space shows up in the image like a certain one. Near 0: it mostly doesn't.\n"
write_md(HERE, "scans", md)
print(md)
