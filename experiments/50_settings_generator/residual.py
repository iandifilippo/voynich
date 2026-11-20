"""What is the part habits don't explain made of?

run.py: Currier B 0.30 bits beyond the boundary, the best habits-only
generator 0.12. Two very different things could fill the gap:
  repetition: a word tends to take the same start, gallows or ending as
    the word before (priming, a habit; a message has no reason to repeat);
  structured transitions: particular choices tend to follow particular
    other choices (what an encoded sequence would leave).
Split the conditional MI accordingly. For each feature, the excess rate at
which a word repeats the previous word's value (over the permutation
baseline, same boundary context and sheet), and the conditional MI computed
only on pairs whose values differ (the off-diagonal), which repetition can't
contribute to.
"""
import pathlib
import random
import sys
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import run  # noqa: E402
from _common import save, table, write_md  # noqa: E402
from voynich.assemble import signs  # noqa: E402

HERE = pathlib.Path(__file__).parent
PERMS = 20


def analyse(sheets, rng):
    pairs, sheet_of = [], []
    for k, lines in enumerate(sheets):
        for l in lines:
            seq = [signs(w) for w in l]
            for a, b in zip(seq, seq[1:]):
                pairs.append((a, b))
                sheet_of.append(k)
    out = {}
    for f, g in run.FEATS.items():
        trip = [(g(a), g(b), (a[-1], b[0])) for a, b in pairs]
        groups = defaultdict(list)
        for k, t in enumerate(trip):
            groups[t[2], sheet_of[k]].append(k)
        rep = sum(x == y for x, y, _ in trip) / len(trip)
        off = [t for t in trip if t[0] != t[1]]
        base_rep = base_off = 0
        for _ in range(PERMS):
            xs = [t[0] for t in trip]
            for idx in groups.values():
                vals = [xs[k] for k in idx]
                rng.shuffle(vals)
                for k, x in zip(idx, vals):
                    xs[k] = x
            perm = [(x, t[1], t[2]) for x, t in zip(xs, trip)]
            base_rep += sum(x == y for x, y, _ in perm) / len(perm)
            base_off += run.cmi([t for t in perm if t[0] != t[1]])
        out[f] = {"repeats previous": rep, "repeats if order were random": base_rep / PERMS,
                  "off-diagonal CMI": run.cmi(off) - base_off / PERMS}
    return out


rng = random.Random(0)
fit = __import__("json").loads((HERE / "results" / "settings.json").read_text())
best = min(fit["grid"], key=lambda r: r["misfit"])
texts = {"Currier B": run.B, "generator with settings": run.generate(best["sigma"], best["hold"], 7)}
rows = []
for name, sheets in texts.items():
    res = analyse(sheets, rng)
    for f, r in res.items():
        rows.append({"text": name, "feature": f, **r,
                     "repeat excess": r["repeats previous"] - r["repeats if order were random"]})
        print(rows[-1], flush=True)
save(HERE, "residual", rows)
md = "# 50 repetition or structured transitions?\n\n" + table(
    rows, ["text", "feature", "repeats previous", "repeats if order were random", "repeat excess", "off-diagonal CMI"])
write_md(HERE, "residual", md)
print(md)


# which start -> start transitions carry it (Currier B): observed against the
# permutation expectation, summed over boundary contexts
pairs, sheet_of = [], []
for k, lines in enumerate(run.B):
    for l in lines:
        seq = [signs(w) for w in l]
        for a, b in zip(seq, seq[1:]):
            pairs.append((a, b))
            sheet_of.append(k)
g = run.FEATS["start"]
trip = [(g(a), g(b), (a[-1], b[0])) for a, b in pairs]
groups = defaultdict(list)
for k, t in enumerate(trip):
    groups[t[2], sheet_of[k]].append(k)
from collections import Counter  # noqa: E402
obs = Counter((x, y) for x, y, _ in trip)
exp = Counter()
for _ in range(50):
    xs = [t[0] for t in trip]
    for idx in groups.values():
        vals = [xs[k] for k in idx]
        rng.shuffle(vals)
        for k, x in zip(idx, vals):
            xs[k] = x
    exp.update((x, t[1]) for x, t in zip(xs, trip))
trans = []
for key, o in obs.items():
    e = exp[key] / 50
    if e >= 15 and key[0] != key[1]:
        trans.append({"word starts": "".join(key[0]), "next word starts": "".join(key[1]), "observed": o,
                      "expected": round(e, 1), "ratio": o / e})
trans.sort(key=lambda r: r["ratio"])
save(HERE, "residual_transitions", trans)
md += "\n## Start-to-start transitions in Currier B furthest from expectation (given the boundary glyphs and the sheet)\n\n"
md += table(trans[:8] + trans[-10:], ["word starts", "next word starts", "observed", "expected", "ratio"])
write_md(HERE, "residual", md)
print(table(trans[:8] + trans[-10:], ["word starts", "next word starts", "observed", "expected", "ratio"]))
