"""What is the page setting? How many knobs, and does it click?

Exp. 40: each page has its own weighting of the forks, held to the end of
the page. Two questions about that setting:

1. How many independent knobs? Principal components of the page profiles
   (fork shares, standardised), compared with the same analysis on pages
   whose lines were shuffled between pages (parallel analysis: only
   components larger than the shuffled ones are real).
2. Discrete or continuous? If pages come in a few kinds (a dial with
   positions), clustering one half of each page should predict how the
   other half clusters. For k = 2..6: k-means on the odd-line halves, then
   each even-line half is assigned to the nearest centre; agreement between
   the two assignments (adjusted Rand index) against the same with lines
   shuffled between pages. A continuum gives modest agreement at every k; a
   dial with k positions gives a peak at k.
Pages of 80+ words; Currier A (hand 1) and Currier B (hands 2 and 3) apart,
then inside single sections, where the subject stays the same kind.
"""
import pathlib
import random
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich
from voynich.forks import FEATS, profile

HERE = pathlib.Path(__file__).parent
MIN_WORDS = 80
SHUFFLES = 30


def kmeans(X, k, rng, iters=100, starts=20):
    best = None
    for _ in range(starts):
        C = X[rng.choice(len(X), k, replace=False)]
        for _ in range(iters):
            lab = ((X[:, None] - C[None]) ** 2).sum(-1).argmin(1)
            newC = np.array([X[lab == j].mean(0) if (lab == j).any() else C[j] for j in range(k)])
            if np.allclose(newC, C):
                break
            C = newC
        sse = ((X - C[lab]) ** 2).sum()
        if best is None or sse < best[0]:
            best = (sse, C, lab)
    return best[1], best[2]


def ari(a, b):
    from math import comb
    n = len(a)
    ct = defaultdict(int)
    for x, y in zip(a, b):
        ct[x, y] += 1
    ra, rb = defaultdict(int), defaultdict(int)
    for (x, y), c in ct.items():
        ra[x] += c
        rb[y] += c
    s = sum(comb(c, 2) for c in ct.values())
    sa = sum(comb(c, 2) for c in ra.values())
    sb = sum(comb(c, 2) for c in rb.values())
    exp = sa * sb / comb(n, 2)
    mx = (sa + sb) / 2
    return (s - exp) / (mx - exp) if mx != exp else 0.0


def halves(lines):
    return [w for l in lines[0::2] for w in l], [w for l in lines[1::2] for w in l]


def analyse(pages, rng):
    A = np.array([profile(halves(p)[0]) for p in pages])
    B = np.array([profile(halves(p)[1]) for p in pages])
    full = np.array([profile([w for l in p for w in l]) for p in pages])
    keep = full.std(0) > 0
    mu, sd = full[:, keep].mean(0), full[:, keep].std(0)
    Z = (full[:, keep] - mu) / sd
    ev = np.sort(np.linalg.eigvalsh(np.cov(Z.T)))[::-1]
    Za, Zb = (A[:, keep] - mu) / sd, (B[:, keep] - mu) / sd
    agree = {}
    for k in range(2, 7):
        C, la = kmeans(Za, k, rng)
        lb = ((Zb[:, None] - C[None]) ** 2).sum(-1).argmin(1)
        agree[k] = ari(la, lb)
    return ev, agree, Z, (Za + Zb) / 2


v = Voynich("ZL")
book, meta, quire = defaultdict(list), {}, {}
for l in v.lines:
    if l.unit == "P":
        ws = [w for w in l.words if "?" not in w and "'" not in w]
        if ws:
            book[l.page].append(ws)
            meta[l.page] = (l.meta.get("L"), l.meta.get("H"), l.meta.get("I"))
            quire[l.page] = l.meta.get("Q")

groups = {"Currier A, hand 1": lambda m: m[1] == "1",
          "Currier B, hands 2 and 3": lambda m: m[1] in ("2", "3") and m[0] == "B",
          "hand 1 herbal only": lambda m: m[1] == "1" and m[2] == "H",
          "hand 2 bathing only": lambda m: m[1] == "2" and m[2] == "B",
          "hand 3 stars only": lambda m: m[1] == "3" and m[2] == "S"}
rng = np.random.default_rng(0)
dims, clus, loads, where = [], [], [], []
for name, keep in groups.items():
    ps = [p for p in book if keep(meta[p]) and sum(map(len, book[p])) >= MIN_WORDS]
    pages = [book[p] for p in ps]
    ev, agree, Z, Zm = analyse(pages, rng)
    for k in (2, 3, 4):
        _, lab = kmeans(Zm, k, rng)
        for g in range(k):
            members = [ps[i] for i in range(len(ps)) if lab[i] == g]
            sec = Counter(meta[p][2] for p in members)
            qs = Counter(quire[p] for p in members)
            where.append({"pages": name, "k": k, "cluster": g + 1, "n": len(members),
                          "sections": ", ".join(f"{a} {b}" for a, b in sec.most_common()),
                          "quires": ", ".join(f"{a} {b}" for a, b in sorted(qs.items())),
                          "folios": " ".join(members) if "only" in name and k == 2 else ""})
    sev, sag = [], defaultdict(list)
    r = random.Random(0)
    for _ in range(SHUFFLES):
        sizes = [len(p) for p in pages]
        pool = [l for p in pages for l in p]
        r.shuffle(pool)
        sh, k0 = [], 0
        for s in sizes:
            sh.append(pool[k0:k0 + s])
            k0 += s
        e, a, _, _ = analyse(sh, rng)
        sev.append(e[:8])
        for k, x in a.items():
            sag[k].append(x)
    null = np.mean(sev, 0)
    n_real = int(np.argmax(ev[:8] <= null)) if (ev[:8] <= null).any() else 8
    dims.append({"pages": name, "n": len(pages), **{f"PC{i + 1}": f"{ev[i]:.2f} ({null[i]:.2f})" for i in range(5)},
                 "components above shuffled": n_real})
    clus.append({"pages": name, **{f"k={k}": f"{agree[k]:.2f} ({np.mean(sag[k]):.2f})" for k in agree}})
    # loadings of the real components on the fork features
    feats = [f for f, kp in zip(FEATS, (np.array([profile([w for l in p for w in l]) for p in pages]).std(0) > 0)) if kp]
    w, vecs = np.linalg.eigh(np.cov(Z.T))
    vecs = vecs[:, np.argsort(w)[::-1]]
    for c in range(min(n_real, 3)):
        order = np.argsort(-np.abs(vecs[:, c]))[:6]
        loads.append({"pages": name, "component": f"PC{c + 1}",
                      "main forks (sign of loading)": ", ".join(
                          f"{'+' if vecs[i, c] > 0 else '-'}{feats[i][0]} {feats[i][1]}" for i in order)})
    print(dims[-1], clus[-1], flush=True)

save(HERE, "dial", {"dims": dims, "clusters": clus, "loadings": loads, "where": where})
md = "# 41 the page setting\n\n## Principal components (eigenvalue; mean with lines shuffled between pages in brackets)\n\n"
md += table(dims, ["pages", "n", "PC1", "PC2", "PC3", "PC4", "PC5", "components above shuffled"])
md += "\n## Split-half cluster agreement, adjusted Rand (shuffled lines in brackets)\n\n"
md += table(clus, ["pages", "k=2", "k=3", "k=4", "k=5", "k=6"])
md += "\n## What the real components are made of\n\n" + table(loads, ["pages", "component", "main forks (sign of loading)"])
md += "\n## Where the clusters fall (sections, quires)\n\n" + table(where, ["pages", "k", "cluster", "n", "sections", "quires", "folios"])
write_md(HERE, "dial", md)
print(md)
