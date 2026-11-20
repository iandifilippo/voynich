"""Is it sequence, or just the page setting?

run.py found that in Currier B the class of a word predicts the class of the
next word on held-out pages (0.09 bits at K = 8-32), more than in any
content-free control. But exp. 40 showed every page has its own setting, so
two words on the same page are alike whatever their order. That alone would
make neighbours predictable.

Separate the two: with the classes from the training half, the held-out MI
between a word and the word 1, 2, 3, 5 places later in the same line, and
between two words drawn at random from the same page. A setting shared by
the page predicts the same MI at every distance; sequence predicts a peak at
distance 1.
"""
import math
import pathlib
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import run  # noqa: E402
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402
from voynich.crack.classes import fit  # noqa: E402

HERE = pathlib.Path(__file__).parent
K = 16


def mi(pairs):
    N = Counter(pairs)
    tot = sum(N.values())
    L, R = Counter(), Counter()
    for (a, b), c in N.items():
        L[a] += c
        R[b] += c
    return sum(c / tot * math.log2(c * tot / (L[a] * R[b])) for (a, b), c in N.items())


def lag_pairs(lines, assign, lag):
    return [(assign.get(l[i], K), assign.get(l[i + lag], K)) for l in lines for i in range(len(l) - lag)]


def page_pairs(pages, assign, rng, n):
    out = []
    pages = [p for p in pages if sum(map(len, p)) > 10]
    for _ in range(n):
        p = rng.choice(pages)
        ws = [w for l in p for w in l]
        a, b = rng.sample(range(len(ws)), 2)
        out.append((assign.get(ws[a], K), assign.get(ws[b], K)))
    return out


def vms_pages(lang):
    v = Voynich("ZL")
    pages = defaultdict(list)
    for l in v.lines:
        if l.unit == "P" and l.meta.get("L") == lang:
            ws = [w for w in l.words if "?" not in w and "'" not in w]
            if ws:
                pages[l.page].append(ws)
    order = list(pages)
    return [pages[p] for p in order[0::2]], [pages[p] for p in order[1::2]]


def chunk_pages(lines, size=14):
    return [lines[i:i + size] for i in range(0, len(lines), size)]


T = run.texts()
sources = {"VMS Currier B": vms_pages("B"), "VMS Currier A": vms_pages("A")}
for name in ("Naibbe cipher of Pliny", "Latin, words", "Italian, words", "assembled words (exp. 36)"):
    tr, te = T[name]
    sources[name] = (chunk_pages(tr), chunk_pages(te))
rng = random.Random(0)
rows = []
for name, (trp, tep) in sources.items():
    tr = run.cap([l for p in trp for l in p], run.N_WORDS)
    f = Counter(w for l in tr for w in l)
    keep = {w for w, c in f.items() if c >= run.MIN_COUNT}
    trm = run.merge_rare(tr, keep)
    tem = [run.merge_rare(p, keep) for p in tep]
    _, assign = fit(trm, K)
    sh = [w for l in trm for w in l]
    rng.shuffle(sh)
    it = iter(sh)
    _, a0 = fit([[next(it) for _ in l] for l in trm], K)
    lines = [l for p in tem for l in p]
    row = {"text": name}
    for lag in (1, 2, 3, 5):
        row[f"distance {lag}"] = mi(lag_pairs(lines, assign, lag)) - mi(lag_pairs(lines, a0, lag))
    n = sum(len(l) for l in lines)
    r1, r2 = random.Random(1), random.Random(1)
    row["same page, any distance"] = mi(page_pairs(tem, assign, r1, n)) - mi(page_pairs(tem, a0, r2, n))
    rows.append(row)
    print({k: (round(x, 3) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
save(HERE, "lags", rows)
md = f"# 44 sequence or page setting (K = {K}, held-out, minus shuffled-training baseline)\n\n" + table(
    rows, ["text", "distance 1", "distance 2", "distance 3", "distance 5", "same page, any distance"])
write_md(HERE, "lags", md)
print(md)
