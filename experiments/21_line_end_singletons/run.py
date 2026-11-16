"""Does a rule at the line end close the singleton gap?

Exp. 20: VMS singletons have the same make-up as the copying model's (63% one
edit from a known word, 15% two words joined, 22% neither); the model has too
few of them and the shortfall is at the line end (singleton rate of line-final
words 0.24 in the VMS, 0.11 in the model; mid-line 0.13 vs 0.12 in B).
VMS line-final singletons are often a known word with a glyph added at the end.

Here the last word of a line gets one more change with probability q: half
the time a glyph appended (y d g s m o r l, weights from exp. 20), otherwise
an -m/-g ending or a normal substitution. Boundary habit on (p = 0.65).

If the line end is the whole story, one q should fix the line-final singleton
rate, the hapax ratio and line_last_jsd together.
"""
import json
import pathlib
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
chart = {k: set(v) for k, v in json.loads(
    (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}


def take(lines, n=10000):
    out, k = [], 0
    for l in lines:
        if k >= n:
            break
        if l:
            out.append(l)
            k += len(l)
    return out


def rates(lines):
    lines = take(lines)
    f = Counter(w for l in lines for w in l)
    pos = {"first": [0, 0], "middle": [0, 0], "last": [0, 0]}
    for l in lines:
        if len(l) < 3:
            continue
        for i, w in enumerate(l):
            k = "first" if i == 0 else "last" if i == len(l) - 1 else "middle"
            pos[k][0] += f[w] == 1
            pos[k][1] += 1
    return {k: a / b for k, (a, b) in pos.items()}


def measure(lines):
    d, z, p = benchmark.score(lines, ref)
    r = rates(lines)
    return {"distance": d, "core": (sum(z[k] ** 2 for k in CORE) / len(CORE)) ** .5,
            "hapax": p["hapax_ratio"], "line_last_jsd": p["line_last_jsd"], "line_first_jsd": p["line_first_jsd"],
            "cohesion": p["line_cohesion"], "edge": p["edge_coupling"], "h2": p["h2"],
            "single_first": r["first"], "single_middle": r["middle"], "single_last": r["last"], "z": z}


rows = []
m = measure(Voynich("ZL").text_lines(unit="P", language="B"))
m.pop("z")
rows.append({"model": "VMS Currier B", "q": None, **m})
for q in (0.0, 0.2, 0.4, 0.6, 0.8):
    out = [measure(AutoCopy(seed=s, currier="B", boundary=chart, boundary_p=0.65, line_end_p=q).run(1400))
           for s in (1, 2, 3, 4)]
    r = {"model": "copying + boundary habit + line-end rule", "q": q}
    for k in out[0]:
        if k != "z":
            r[k] = statistics.mean(x[k] for x in out)
    zm = {k: statistics.mean(x["z"][k] for x in out) for k in KEYS}
    r["worst"] = ", ".join(f"{k} {zm[k]:+.1f}" for k in sorted(KEYS, key=lambda k: -abs(zm[k]))[:3])
    rows.append(r)
    print(r)



def spectrum(lines):
    f = Counter(w for l in take(lines) for w in l)
    n = sum(f.values())
    bins = [("1", 1, 1), ("2", 2, 2), ("3-5", 3, 5), ("6-20", 6, 20), ("21+", 21, 10 ** 9)]
    out = {}
    for name, lo, hi in bins:
        ts = [c for c in f.values() if lo <= c <= hi]
        out[f"types {name}"] = len(ts)
        out[f"tokens {name}"] = sum(ts) / n
    return out


spec = [{"text": "VMS Currier B", **spectrum(Voynich("ZL").text_lines(unit="P", language="B"))},
        {"text": "VMS Currier A", **spectrum(Voynich("ZL").text_lines(unit="P", language="A"))}]
ms = [spectrum(AutoCopy(seed=s, currier="B", boundary=chart, boundary_p=0.65, line_end_p=0.5).run(1400))
      for s in (1, 2, 3, 4)]
spec.append({"text": "model, q = 0.5 (mean of 4)", **{k: statistics.mean(x[k] for x in ms) for k in ms[0]}})
save(HERE, "line_end", {"rows": rows, "spectrum": spec})
md = "# 21 line-end rule in the copying model\n\n" + table(
    rows, ["model", "q", "distance", "core", "hapax", "single_first", "single_middle", "single_last",
           "line_last_jsd", "cohesion", "edge", "worst"])
md += "\n`single_*`: share of words in that line position that are singletons (first 10 000 words). 4 seeds per row.\n"
md += "\n## frequency spectrum (first 10 000 words)\n\n" + table(
    spec, ["text", "types 1", "types 2", "types 3-5", "types 6-20", "types 21+",
           "tokens 1", "tokens 2", "tokens 3-5", "tokens 6-20", "tokens 21+"])
md += "\n`types n`: number of word types occurring n times; `tokens n`: share of the text they cover.\n"
write_md(HERE, "line_end", md)
print(md)
