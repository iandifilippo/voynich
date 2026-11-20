"""Does each herbal page have fork habits of its own?

Exp. 39: the forks follow the section, steady for twenty pages at a time.
That fits a text about different subjects, but also a per-section setting or
writing sessions. Inside one section the subject still changes: each herbal
page shows a different plant. If the forks follow the content, each page
should have habits of its own, beyond what its neighbours share.

Test: cut every page into two halves (odd lines, even lines). For each half,
rank the other halves in the section by similarity of their fork profiles
(exp. 39's 34 features). How often is the page's own other half the closest?
How often is a neighbouring page's half closer than a far page's?

Nulls and controls:
  lines shuffled between pages of the section (keeps each page's size): what
    chance looks like with real lines;
  the exp. 36 generator (sign chain + echo of recent words), fitted on the
    section and filling the same pages: what a page-blind writer with short
    memory produces, since the echo alone makes a page's halves alike;
  the copying model, whose words are copies of words on the same page: a
    writer whose memory is the page, as Timm and Schinner propose.
A second version drops, from each comparison, the words the two halves have
in common, so that likeness from repeating the same words is removed.
Run on hand 1's herbal pages (Currier A) and hand 2's herbal and bathing
pages (Currier B), pages of 80+ words.
"""
import pathlib
import random
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich
import json

from voynich.assemble import Assembler
from voynich.autocopy import AutoCopy
from voynich.forks import profile

HERE = pathlib.Path(__file__).parent
MIN_WORDS = 80
SHUFFLES = 50
PAGE_LINES = 20
chart = {k: set(x) for k, x in json.loads(
    (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}


def halves(lines):
    a = [w for l in lines[0::2] for w in l]
    b = [w for l in lines[1::2] for w in l]
    return a, b


def score(pages):
    """pages: list (in book order) of lists of lines. Returns self-match rate,
    mean rank of own half (0 = closest), neighbour vs far."""
    H = [halves(p) for p in pages]
    A = np.array([profile(a) for a, _ in H])
    B = np.array([profile(b) for _, b in H])
    n = len(pages)
    D = ((A[:, None, :] - B[None, :, :]) ** 2).sum(-1)
    D2 = ((B[:, None, :] - A[None, :, :]) ** 2).sum(-1)
    top, ranks, nb, far = 0, [], [], []
    for M in (D, D2):
        for i in range(n):
            order = np.argsort(M[i])
            r = int(np.where(order == i)[0][0])
            ranks.append(r / (n - 1))
            top += r == 0
            others = [j for j in range(n) if j != i]
            near = [j for j in (i - 1, i + 1) if 0 <= j < n]
            nb.append(np.mean([M[i, j] for j in near]))
            far.append(np.mean([M[i, j] for j in others if abs(j - i) > 3]))
    return {"own half closest": top / (2 * n), "own half, mean rank (0 best, 0.5 chance)": float(np.mean(ranks)),
            "neighbour / far distance": float(np.mean(nb) / np.mean(far))}


def score_unshared(pages):
    """Same, but each comparison of half a (page i) with half b (page j) uses
    only words of a whose type doesn't occur in b, and vice versa. Pages that
    are alike because they repeat the same words lose their likeness; pages
    alike because their forks are set the same way keep it."""
    H = [halves(p) for p in pages]
    n = len(pages)
    sets = [(set(a), set(b)) for a, b in H]
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a = [w for w in H[i][0] if w not in sets[j][1]]
            b = [w for w in H[j][1] if w not in sets[i][0]]
            D[i, j] = ((profile(a) - profile(b)) ** 2).sum()
    top, ranks = 0, []
    for M in (D, D.T):
        for i in range(n):
            r = int(np.where(np.argsort(M[i]) == i)[0][0])
            ranks.append(r / (n - 1))
            top += r == 0
    return {"own half closest, shared words removed": top / (2 * n),
            "mean rank, shared words removed": float(np.mean(ranks))}


def shuffle_lines(pages, rng):
    sizes = [len(p) for p in pages]
    pool = [l for p in pages for l in p]
    rng.shuffle(pool)
    out, k = [], 0
    for s in sizes:
        out.append(pool[k:k + s])
        k += s
    return out


import os
TRANS = os.environ.get("VMS_TRANS", "ZL")
v = Voynich(TRANS)
book = defaultdict(list)
meta = {}
for l in v.lines:
    if l.unit == "P":
        ws = [w for w in l.words if "?" not in w and "'" not in w]
        if ws:
            book[l.page].append((ws, l.para_start))
            meta[l.page] = (l.meta.get("L"), l.meta.get("H"), l.meta.get("I"))

groups = {"hand 1 herbal (A)": ("1", "H"), "hand 2 herbal (B)": ("2", "H"), "hand 2 bathing (B)": ("2", "B"),
          "hand 3 stars (B)": ("3", "S")}
rows = []
for name, (hand, sec) in groups.items():
    ps = [p for p in book if meta[p][1] == hand and meta[p][2] == sec and sum(len(l) for l, _ in book[p]) >= MIN_WORDS]
    real = [[l for l, _ in book[p]] for p in ps]
    rows.append({"pages": name, "text": "manuscript", "n pages": len(ps), **score(real), **score_unshared(real)})
    rng = random.Random(0)
    sh = []
    for k in range(SHUFFLES):
        x = shuffle_lines(real, rng)
        sh.append({**score(x), **(score_unshared(x) if k < 10 else {})})
    sh = [{**s_, **{kk: np.mean([y[kk] for y in sh if kk in y]) for kk in sh[0] if "removed" in kk}} for s_ in sh]
    rows.append({"pages": name, "text": "lines shuffled between pages", "n pages": len(ps),
                 **{k: float(np.mean([s[k] for s in sh])) for k in sh[0]}})
    starts = [k for k, (l, s) in enumerate([x for p in ps for x in book[p]]) if s]
    m = Assembler(order=2, recall_p=0.01, edit_p=0.10, window=5).fit(
        [l for p in ps for l, _ in book[p]], starts)
    gens = []
    for seed in range(5):
        filled = [m.fill([(len(l), s) for l, s in book[p]], seed=seed * 1000 + i) for i, p in enumerate(ps)]
        gens.append(score(filled))
    rows.append({"pages": name, "text": "generator with echo (exp. 36)", "n pages": len(ps),
                 **{k: float(np.mean([s[k] for s in gens])) for k in gens[0]}})
    cps = []
    for seed in range(3):
        g = AutoCopy(seed=seed + 1, currier=meta[ps[0]][0], boundary=chart, boundary_p=0.65, line_end_p=0.5,
                     common_p=0.5, page_lines=PAGE_LINES)
        lines = [l for l in g.run(PAGE_LINES * len(ps))]
        cpages = [lines[i:i + PAGE_LINES] for i in range(0, len(lines), PAGE_LINES)][:len(ps)]
        cps.append({**score(cpages), **score_unshared(cpages)})
    rows.append({"pages": name, "text": "copying model (copies from its own page)", "n pages": len(ps),
                 **{k: float(np.mean([s[k] for s in cps])) for k in cps[0]}})
    for r in rows[-4:]:
        print(r, flush=True)

TAG = "" if TRANS == "ZL" else "_" + TRANS
save(HERE, "page_identity" + TAG, rows)
md = f"# 40 page identity inside a section ({TRANS})\n\n" + table(
    rows, ["pages", "text", "n pages", "own half closest", "own half, mean rank (0 best, 0.5 chance)",
           "neighbour / far distance", "own half closest, shared words removed",
           "mean rank, shared words removed"])
write_md(HERE, "page_identity" + TAG, md)
print(md)
