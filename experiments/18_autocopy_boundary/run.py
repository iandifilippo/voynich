"""Self-citation plus a preference at the word boundary.

Exp. 17: copying gets the line structure but no edge coupling (0.01 vs 0.15).
Exp. 13: an autokey rule gets the coupling. Here the copying scribe gets a
small habit instead: after a word ending in glyph x, a copied word whose start
isn't on x's list is thrown away (with probability p) and another is copied.
No plaintext, no key, just a preference.

Two kinds of list:
  fitted  for each final glyph, the word starts with positive PMI in the VMS,
          estimated on odd lines only; pattern evaluated on even lines
  random  same list sizes, starts drawn at random (5 charts)
"""
import math
import pathlib
import random
import statistics
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, benchmark
from voynich.autocopy import AutoCopy

HERE = pathlib.Path(__file__).parent
ref = benchmark.reference()
KEYS = benchmark.KEYS
LINE = {"line_first_jsd", "line_last_jsd", "line_cohesion", "repeat_rate"}
CORE = [k for k in KEYS if k not in LINE]
LAST = ["y", "n", "l", "r", "s", "m", "o", "d"]
SEEDS = (1, 2, 3)


def first_cls(w):
    return w[:2] if w[:2] in ("ch", "sh", "qo") else w[0]


def last_cls(w):
    return w[-1] if w[-1] in LAST else "other"


def pairs_of(lines):
    return [(last_cls(l[i]), first_cls(l[i + 1])) for l in lines for i in range(len(l) - 1)]


def pmi(pairs, mincount=30):
    a = Counter(x for x, _ in pairs)
    b = Counter(y for _, y in pairs)
    ab = Counter(pairs)
    n = len(pairs)
    return {k: math.log2((c / n) / ((a[k[0]] / n) * (b[k[1]] / n))) for k, c in ab.items() if c >= mincount}


def corr(p, q):
    ks = [k for k in p if k in q]
    if len(ks) < 3:
        return 0.0
    xs, ys = [p[k] for k in ks], [q[k] for k in ks]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den if den else 0.0


v = Voynich("ZL")
vl = v.text_lines(unit="P")
odd, even = pmi(pairs_of(vl[::2])), pmi(pairs_of(vl[1::2]))
starts = sorted({f for _, f in pairs_of(vl) if f})
fitted = {L: {f for (l, f), x in odd.items() if l == L and x > 0} for L in LAST}
fitted = {L: s for L, s in fitted.items() if s}


def random_chart(seed):
    rng = random.Random(seed)
    common = [f for f, _ in Counter(f for _, f in pairs_of(vl)).most_common(14)]
    return {L: set(rng.sample(common, len(s))) for L, s in fitted.items()}


def run(name, chart, p):
    out = []
    for s in SEEDS:
        lines = AutoCopy(seed=s, currier="B", boundary=chart, boundary_p=p).run(1400)
        d, z, prof = benchmark.score(lines, ref)
        out.append({"distance": d, "core": (sum(z[k] ** 2 for k in CORE) / len(CORE)) ** .5,
                    "edge": prof["edge_coupling"], "hapax": prof["hapax_ratio"], "h2": prof["h2"],
                    "words_per_line": sum(map(len, lines)) / len(lines),
                    "pattern_r": corr(pmi(pairs_of(lines)), even), "z": z})
    r = {"model": name, "p": p}
    for k in ("distance", "core", "edge", "hapax", "h2", "words_per_line", "pattern_r"):
        r[k] = statistics.mean(x[k] for x in out)
    zm = {k: statistics.mean(x["z"][k] for x in out) for k in KEYS}
    r["worst"] = ", ".join(f"{k} {zm[k]:+.1f}" for k in sorted(KEYS, key=lambda k: -abs(zm[k]))[:3])
    return r


rows = [{"model": "VMS even lines vs odd", "p": None, "edge": None, "pattern_r": corr(odd, even),
         "words_per_line": sum(map(len, vl)) / len(vl)}]
for p in (0.0, 0.5, 0.65, 0.8, 0.95):
    rows.append(run("fitted chart", fitted, p))
    print(rows[-1])
for p in (0.8, 0.95):
    rs = [run(f"random chart {i}", random_chart(i), p) for i in range(5)]
    m = {"model": "random charts (mean of 5)", "p": p}
    for k in ("distance", "core", "edge", "hapax", "h2", "words_per_line", "pattern_r"):
        m[k] = statistics.mean(x[k] for x in rs)
    m["pattern_r_max"] = max(x["pattern_r"] for x in rs)
    m["worst"] = rs[0]["worst"]
    rows.append(m)
    print(m)

save(HERE, "boundary", {"chart": {k: sorted(v) for k, v in fitted.items()}, "rows": rows})
md = "# 18 self-citation + boundary preference\n\n"
md += "Fitted chart (from odd lines): " + "; ".join(f"-{k}: {' '.join(sorted(v))}" for k, v in fitted.items()) + "\n\n"
md += table(rows, ["model", "p", "distance", "core", "edge", "pattern_r", "hapax", "h2", "words_per_line", "worst"])
md += "\n`pattern_r`: correlation of the (final glyph, next word start) PMI table with the VMS's even lines. Generator in B settings, 3 seeds per row.\n"
write_md(HERE, "boundary", md)
print(md)
