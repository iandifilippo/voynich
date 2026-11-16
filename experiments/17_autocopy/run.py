"""Timm & Schinner's self-citation generator through the benchmark.

The generator (voynich/autocopy.py) builds each word by copying a word from the
current or a recent line, usually at about the same horizontal position, and
changing it: swap one glyph for a similar one, add or drop a prefix, glue two
words, split one. No plaintext at all.

Questions
1. How close does it get on the 13 benchmark metrics, against the VMS and
   against the best cipher model so far (autokey Naibbe + line-start rule, 3.92)?
2. Does it get the things ciphers can't: edge coupling, the near-repeat excess
   from exp. 15, line cohesion?
3. Which metrics does it miss, and is the miss stable across seeds?
"""
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
SEEDS = range(1, 9)


def edit1(a, b):
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))


def repeats(lines):
    pairs = [(a, b) for l in lines for a, b in zip(l, l[1:])]
    n = len(pairs)
    return 1000 * sum(a == b for a, b in pairs) / n, 1000 * sum(edit1(a, b) for a, b in pairs) / n


def in_line_null(lines, reps=60, seed=0):
    rng = random.Random(seed)
    ex, nr = [], []
    for _ in range(reps):
        sh = []
        for l in lines:
            l = list(l)
            rng.shuffle(l)
            sh.append(l)
        e, n = repeats(sh)
        ex.append(e)
        nr.append(n)
    return statistics.mean(ex), statistics.mean(nr)


def first_word_s(lines):
    """share of line-initial words starting with s, d, t (exp. 10 glyphs)"""
    starts = [l[0][0] for l in lines if l]
    return {g: starts.count(g) / len(starts) for g in "sdtkpqoy"}


def row(name, lines):
    d, z, p = benchmark.score(lines, ref)
    core = (sum(z[k] ** 2 for k in CORE) / len(CORE)) ** .5
    ex, nr = repeats(lines)
    ex0, nr0 = in_line_null(lines)
    worst = sorted(KEYS, key=lambda k: -abs(z[k]))[:4]
    return {"text": name, "distance": d, "core": core, "h2": p["h2"], "hapax": p["hapax_ratio"],
            "edge": p["edge_coupling"], "word_len": p["word_len"], "cohesion": p["line_cohesion"],
            "line_first": p["line_first_jsd"], "exact": ex, "exact_null": ex0, "near": nr, "near_null": nr0,
            "worst": ", ".join(f"{k} {z[k]:+.1f}" for k in worst)}, z


v = Voynich("ZL")
rows, zs = [], {}
for lang in ("A", "B"):
    r, _ = row(f"VMS Currier {lang}", v.text_lines(unit="P", language=lang))
    rows.append(r)
r, _ = row("VMS all", v.text_lines(unit="P"))
rows.append(r)

gen_rows = {"A": [], "B": []}
for cur in ("A", "B"):
    for s in SEEDS:
        lines = AutoCopy(seed=s, currier=cur).run(1400)
        r, z = row(f"autocopy {cur} seed {s}", lines)
        gen_rows[cur].append(r)
        zs[cur, s] = z

summary = []
for cur in ("A", "B"):
    rs = gen_rows[cur]
    m = {"text": f"autocopy {cur} (mean of {len(rs)})"}
    for k in ("distance", "core", "h2", "hapax", "edge", "word_len", "cohesion", "line_first",
              "exact", "exact_null", "near", "near_null"):
        vals = [x[k] for x in rs]
        m[k] = statistics.mean(vals)
        m[k + "_sd"] = statistics.pstdev(vals)
    zmean = {k: statistics.mean(zs[cur, s][k] for s in SEEDS) for k in KEYS}
    m["worst"] = ", ".join(f"{k} {zmean[k]:+.1f}" for k in sorted(KEYS, key=lambda k: -abs(zmean[k]))[:4])
    m["z"] = zmean
    summary.append(m)

starts = {"VMS B": first_word_s(v.text_lines(unit="P", language="B"))}
starts["autocopy B seed 1"] = first_word_s(AutoCopy(seed=1, currier="B").run(1400))
sample = AutoCopy(seed=1, currier="B").run(40)

save(HERE, "autocopy", {"reference": rows, "runs": gen_rows, "summary": summary, "line_starts": starts,
                        "sample": [" ".join(l) for l in sample]})
cols = ["text", "distance", "core", "h2", "hapax", "edge", "word_len", "cohesion", "line_first", "worst"]
md = "# 17 self-citation generator\n\n## summary\n\n" + table(rows + summary, cols)
md += "\n## repeats per 1000 adjacent pairs (null = words shuffled within their line)\n\n"
md += table(rows + summary, ["text", "exact", "exact_null", "near", "near_null"])
md += "\n## spread across seeds\n\n" + table(summary, ["text", "distance_sd", "core_sd", "h2_sd", "edge_sd", "hapax_sd"])
md += "\n## line-initial glyph shares\n\n" + table(
    [{"text": k, **{g: f"{x:.3f}" for g, x in s.items()}} for k, s in starts.items()], ["text"] + list("sdtkpqoy"))
md += "\n## sample (B, seed 1, first 12 lines)\n\n```\n" + "\n".join(" ".join(l) for l in sample[:12]) + "\n```\n"
write_md(HERE, "autocopy", md)
print(md)
