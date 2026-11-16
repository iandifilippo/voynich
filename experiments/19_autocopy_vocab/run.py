"""Can the copying model reach the VMS vocabulary size without losing its line structure?

Exp. 17/18: hapax ratio 0.55 vs 0.69, the largest remaining miss on the word
side. The generator keeps too many copies unchanged. Here each new word gets
one more glyph substitution with probability q, on top of the usual change,
with the boundary habit of exp. 18 (fitted list, p = 0.65).

Watch hapax and MATTR go up; watch line cohesion and the near-repeat excess,
which come from copying, to see whether they survive.
"""
import json
import pathlib
import random
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, benchmark
from voynich.autocopy import AutoCopy

HERE = pathlib.Path(__file__).parent
ref = benchmark.reference()
KEYS = benchmark.KEYS
LINE = {"line_first_jsd", "line_last_jsd", "line_cohesion", "repeat_rate"}
CORE = [k for k in KEYS if k not in LINE]
chart = {k: set(v) for k, v in json.loads(
    (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}


def edit1(a, b):
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))


def near(lines, shuffle_seed=None):
    if shuffle_seed is not None:
        rng = random.Random(shuffle_seed)
        lines = [rng.sample(l, len(l)) for l in lines]
    pairs = [(a, b) for l in lines for a, b in zip(l, l[1:])]
    return 1000 * sum(edit1(a, b) for a, b in pairs) / len(pairs)


rows = []
vl = Voynich("ZL").text_lines(unit="P", language="B")
d, z, p = benchmark.score(vl, ref)
rows.append({"model": "VMS Currier B", "q": None, "distance": d, "hapax": p["hapax_ratio"],
             "mattr": p["mattr500"], "cohesion": p["line_cohesion"], "edge": p["edge_coupling"], "h2": p["h2"],
             "near": near(vl), "near_null": statistics.mean(near(vl, s) for s in range(20))})
for q in (0.0, 0.3, 0.6, 0.9):
    out = []
    for seed in (1, 2, 3):
        lines = AutoCopy(seed=seed, currier="B", boundary=chart, boundary_p=0.65, extra_change=q).run(1400)
        d, z, p = benchmark.score(lines, ref)
        out.append({"distance": d, "core": (sum(z[k] ** 2 for k in CORE) / len(CORE)) ** .5,
                    "hapax": p["hapax_ratio"], "mattr": p["mattr500"], "cohesion": p["line_cohesion"],
                    "edge": p["edge_coupling"], "h2": p["h2"], "near": near(lines),
                    "near_null": statistics.mean(near(lines, s) for s in range(20)), "z": z})
    r = {"model": "copying + habit", "q": q}
    for k in ("distance", "core", "hapax", "mattr", "cohesion", "edge", "h2", "near", "near_null"):
        r[k] = statistics.mean(x[k] for x in out)
    zm = {k: statistics.mean(x["z"][k] for x in out) for k in KEYS}
    r["worst"] = ", ".join(f"{k} {zm[k]:+.1f}" for k in sorted(KEYS, key=lambda k: -abs(zm[k]))[:3])
    rows.append(r)
    print(r)

save(HERE, "vocab", rows)
md = "# 19 copying model: vocabulary\n\n" + table(
    rows, ["model", "q", "distance", "core", "hapax", "mattr", "h2", "edge", "cohesion", "near", "near_null", "worst"])
md += "\n`q`: probability of one extra glyph substitution per word. `near`/`near_null`: near-repeats per 1000 adjacent pairs, as written and with words shuffled within lines (20 shuffles).\n"
write_md(HERE, "vocab", md)
print(md)
