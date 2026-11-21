"""Does the residual of exps. 48-51 survive at physically wide spaces?

run.py: the coupling across the space is strong at narrow gaps (0.42 bits in
B) and weak at wide ones (0.08, close to Latin and Italian). The residual of
exps. 48-51 (neighbouring words sharing choices beyond the boundary glyphs)
might live at the same narrow gaps. Here exp. 48's conditional MI (start,
gallows, ending, length; given the boundary glyphs; permutation inside the
sheet and boundary context) is computed separately for word pairs whose
physical gap is in the narrowest, middle and widest third, on the boxed text.
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
from voynich.assemble import GALLOWS, signs  # noqa: E402

HERE = pathlib.Path(__file__).parent
FEATS = {"start": lambda s: tuple(s[:2]), "gallows": lambda s: next((x for x in s if x in GALLOWS), "-"),
         "ending": lambda s: tuple(s[-2:]), "length": lambda s: min(len(s), 6)}
PERMS = 20


def cmi(trip):
    nz, nxz, nyz, nxyz = Counter(), Counter(), Counter(), Counter()
    for x, y, z in trip:
        nz[z] += 1
        nxz[x, z] += 1
        nyz[y, z] += 1
        nxyz[x, y, z] += 1
    n = len(trip)
    return sum(c / n * math.log2(c * nz[z] / (nxz[x, z] * nyz[y, z])) for (x, y, z), c in nxyz.items())


def beyond(pairs, rng):
    """pairs: (left signs, right signs, sheet)."""
    total = 0
    for gx in FEATS.values():
        for gy in FEATS.values():
            trip = [(gx(a), gy(b), (a[-1], b[0])) for a, b, _ in pairs]
            groups = defaultdict(list)
            for k, (a, b, s) in enumerate(pairs):
                groups[(a[-1], b[0]), s].append(k)
            base = 0
            for _ in range(PERMS):
                xs = [t[0] for t in trip]
                for idx in groups.values():
                    vals = [xs[i] for i in idx]
                    rng.shuffle(vals)
                    for i, x in zip(idx, vals):
                        xs[i] = x
                base += cmi([(x, t[1], t[2]) for x, t in zip(xs, trip)])
            total += cmi(trip) - base / PERMS
    return total


v = Voynich("ZL")
meta = {p: (v.pages[p].get("L"), (v.pages[p].get("Q"), v.pages[p].get("B"))) for p in v.pages}
lines = run.load_lines()
rng = random.Random(0)
rows = []
for L in ("B", "A"):
    pairs = []
    for f, ls in lines.items():
        if meta.get(f, (None,))[0] != L:
            continue
        for l in ls:
            for i, (w, g) in enumerate(l):
                if g is not None:
                    pairs.append((signs(w), signs(l[i + 1][0]), meta[f][1], g))
    gs = sorted(p[3] for p in pairs)
    t1, t2 = gs[len(gs) // 3], gs[2 * len(gs) // 3]
    for name, sel in (("narrowest third", lambda g: g <= t1), ("middle third", lambda g: t1 < g <= t2),
                      ("widest third", lambda g: g > t2), ("all", lambda g: True)):
        ps = [(a, b, s) for a, b, s, g in pairs if sel(g)]
        rows.append({"Currier": L, "gaps": name, "pairs": len(ps), "beyond the boundary (bits)": beyond(ps, rng)})
        print(rows[-1], flush=True)
save(HERE, "residual_by_gap", rows)
md = "# 55 the residual by physical gap\n\n" + table(rows, ["Currier", "gaps", "pairs", "beyond the boundary (bits)"])
write_md(HERE, "residual_by_gap", md)
print(md)
