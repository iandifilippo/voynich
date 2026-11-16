"""Scorecard for the best copying model on things it was not tuned on.

The model of exp. 22 (copying + boundary habit p = 0.65 + line-end rule
q = 0.5 + prefer-common c = 0.5) was adjusted on benchmark distance, edge
coupling, line-end singletons and the size of the core. Here it is checked on
measurements that were never used to set a knob:

  repeats        exact and near repeats against the in-line shuffle (exp. 15)
  singletons     make-up: one edit from known / two joined / neither (exp. 20)
  word shape     word-length distribution, share of words by first and last glyph
  line start     share of line-first words by first glyph
  A vs B         whether its A and B settings differ the way Currier A and B do
Eight seeds, B settings, compared with Currier B; A settings with Currier A.
"""
import json
import math
import pathlib
import random
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, benchmark
from voynich.autocopy import AutoCopy

HERE = pathlib.Path(__file__).parent
ref = benchmark.reference()
chart = {k: set(v) for k, v in json.loads(
    (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}
SEEDS = range(1, 9)


def best(seed, currier="B"):
    return AutoCopy(seed=seed, currier=currier, boundary=chart, boundary_p=0.65,
                    line_end_p=0.5, common_p=0.5).run(1400)


def take(lines, n=10000):
    out, k = [], 0
    for l in lines:
        if k >= n:
            break
        if l:
            out.append(list(l))
            k += len(l)
    return out


def edit1(a, b):
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))


def repeat_rates(lines):
    pairs = [(a, b) for l in lines for a, b in zip(l, l[1:])]
    return (1000 * sum(a == b for a, b in pairs) / len(pairs),
            1000 * sum(edit1(a, b) for a, b in pairs) / len(pairs))


def features(lines):
    lines = take(lines)
    words = [w for l in lines for w in l]
    f = Counter(words)
    out = {}
    ex, nr = repeat_rates(lines)
    rng = random.Random(0)
    null = [repeat_rates([rng.sample(l, len(l)) for l in lines]) for _ in range(30)]
    out["exact repeats / in-line null"] = ex / statistics.mean(x[0] for x in null)
    out["near repeats / in-line null"] = nr / statistics.mean(x[1] for x in null)
    known = {w for w, c in f.items() if c >= 2}
    index = defaultdict(set)
    for w in known:
        index[w].add(w)
        for i in range(len(w)):
            index[w[:i] + w[i + 1:]].add(w)
    single = [w for w, c in f.items() if c == 1]
    near = joined = 0
    for w in single:
        cands = set(index.get(w, ()))
        for i in range(len(w)):
            cands |= index.get(w[:i] + w[i + 1:], set())
        n = any(edit1(w, c) for c in cands)
        near += n
        joined += (not n) and any(w[:i] in known and w[i:] in known for i in range(2, len(w) - 1))
    out["singletons: one edit from known"] = near / len(single)
    out["singletons: two known joined"] = joined / len(single)
    out["mean word length"] = statistics.mean(map(len, words))
    for n in (1, 2, 3, 8):
        out[f"words of length {n}{'+' if n == 8 else ''}"] = sum((len(w) >= n) if n == 8 else (len(w) == n) for w in words) / len(words)
    for g in ("q", "o", "ch", "sh", "d", "y"):
        out[f"words starting {g}-"] = sum(w.startswith(g) for w in words) / len(words)
    for g in ("y", "n", "l", "r", "m"):
        out[f"words ending -{g}"] = sum(w.endswith(g) for w in words) / len(words)
    firsts = [l[0] for l in lines if len(l) >= 3]
    for g in ("s", "d", "t", "p", "q"):
        out[f"line-first words starting {g}-"] = sum(w.startswith(g) for w in firsts) / len(firsts)
    out["top word share"] = f.most_common(1)[0][1] / len(words)
    return out


def dist_ab(a, b):
    """benchmark distance between two texts' profiles"""
    pa, pb = benchmark.score(a, ref)[2], benchmark.score(b, ref)[2]
    return math.sqrt(sum(((pa[k] - pb[k]) / ref["scale"][k]) ** 2 for k in benchmark.KEYS) / len(benchmark.KEYS))


v = Voynich("ZL")
rows = []
for cur in ("B", "A"):
    target = features(v.text_lines(unit="P", language=cur))
    runs = [features(best(s, cur)) for s in SEEDS]
    for k in target:
        vals = [r[k] for r in runs]
        mu, sd = statistics.mean(vals), statistics.pstdev(vals)
        ratio = mu / target[k] if target[k] else float("nan")
        verdict = "ok" if 0.8 <= ratio <= 1.25 else "off" if 0.5 <= ratio <= 2 else "wrong"
        rows.append({"settings": cur, "measure": k, "VMS": target[k], "model": mu, "sd": sd,
                     "model/VMS": ratio, "verdict": verdict})

tally = Counter((r["settings"], r["verdict"]) for r in rows)
ab = {"VMS A vs B": dist_ab(v.text_lines(unit="P", language="A"), v.text_lines(unit="P", language="B")),
      "model A vs B settings (mean of 4)": statistics.mean(dist_ab(best(s, "A"), best(s, "B")) for s in (1, 2, 3, 4)),
      "model B vs B, different seeds (mean of 4)": statistics.mean(dist_ab(best(s, "B"), best(s + 10, "B")) for s in (1, 2, 3, 4))}

save(HERE, "scorecard", {"rows": rows, "tally": {f"{a} {b}": c for (a, b), c in tally.items()}, "a_vs_b": ab})
md = "# 23 scorecard: best copying model on measures it wasn't tuned on\n\n"
for cur in ("B", "A"):
    md += f"\n## {cur} settings against Currier {cur}\n\n" + table(
        [r for r in rows if r["settings"] == cur], ["measure", "VMS", "model", "sd", "model/VMS", "verdict"])
    md += f"\nok {tally[cur, 'ok']}, off {tally[cur, 'off']}, wrong {tally[cur, 'wrong']} (ok = within 0.8-1.25x, off = within 2x)\n"
md += "\n## A and B\n\n" + table([{"pair": k, "distance": x} for k, x in ab.items()], ["pair", "distance"])
write_md(HERE, "scorecard", md)
print(md)
