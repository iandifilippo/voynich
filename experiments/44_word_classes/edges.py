"""Is Currier B's word sequence anything more than the edge habit?

lags.py: in Currier B the class of a word predicts the next word's class
(0.083 bits), and it is sequence, not page setting. But exp. 18 already
found a glyph-level habit at word boundaries: the last glyph of a word and
the first glyph of the next are coupled. Classes could just be learning
that.

Control: in the held-out text, shuffle words only among words that share both
their first and their last sign. Every boundary keeps exactly the same pair
of glyphs on both sides; everything else about which word follows which is
destroyed. Then the classes' MI on that text. Also with the key looser
(first sign only) and stricter (first two and last two signs).
"""
import pathlib
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import lags  # noqa: E402
import run  # noqa: E402
from _common import save, table, write_md  # noqa: E402
from voynich.assemble import signs  # noqa: E402
from voynich.crack.classes import fit  # noqa: E402

HERE = pathlib.Path(__file__).parent
K = lags.K
KEYS = {"first sign only": lambda s: (s[0],),
        "first and last sign": lambda s: (s[0], s[-1]),
        "first two and last two signs": lambda s: (tuple(s[:2]), tuple(s[-2:]))}


def constrained_shuffle(lines, key, rng):
    groups = defaultdict(list)
    for i, l in enumerate(lines):
        for j, w in enumerate(l):
            groups[key(signs(w))].append((i, j))
    out = [list(l) for l in lines]
    for pos in groups.values():
        ws = [lines[i][j] for i, j in pos]
        rng.shuffle(ws)
        for (i, j), w in zip(pos, ws):
            out[i][j] = w
    return out


rows = []
rng = random.Random(0)
for name in ("VMS Currier B", "Latin, words", "Italian, words"):
    if name.startswith("VMS"):
        trp, tep = lags.vms_pages("B")
    else:
        tr, te = run.texts()[name]
        trp, tep = lags.chunk_pages(tr), lags.chunk_pages(te)
    tr = run.cap([l for p in trp for l in p], run.N_WORDS)
    te = [l for p in tep for l in p]
    f = Counter(w for l in tr for w in l)
    keep = {w for w, c in f.items() if c >= run.MIN_COUNT}
    _, assign = fit(run.merge_rare(tr, keep), K)
    sh = [w for l in run.merge_rare(tr, keep) for w in l]
    rng.shuffle(sh)
    it = iter(sh)
    _, a0 = fit([[next(it) for _ in l] for l in run.merge_rare(tr, keep)], K)

    def score(lines):
        m = run.merge_rare(lines, keep)
        return lags.mi(lags.lag_pairs(m, assign, 1)) - lags.mi(lags.lag_pairs(m, a0, 1))

    row = {"text": name, "as written": score(te)}
    for label, key in KEYS.items():
        vals = [score(constrained_shuffle(te, key if name.startswith("VMS") else (lambda s, k=key: k(list(s))), rng))
                for _ in range(5)]
        row[f"shuffled, keeping {label}"] = sum(vals) / len(vals)
    row["shuffled freely"] = sum(score(constrained_shuffle(te, lambda s: (), rng)) for _ in range(5)) / 5
    rows.append(row)
    print({k: (round(x, 3) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
save(HERE, "edges", rows)
cols = ["text", "as written"] + [f"shuffled, keeping {k}" for k in KEYS] + ["shuffled freely"]
md = f"# 44 sequence beyond the edge habit (K = {K}, distance 1, held-out)\n\n" + table(rows, cols)
write_md(HERE, "edges", md)
print(md)
