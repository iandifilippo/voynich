"""The zodiac labels: thirty names reused, a count, or neither?

Each zodiac sign (f70v2-f73v) has about thirty nymphs, one per degree or day,
each with a label. If the labels named the days (a calendar), two signs
would share their names, and label i in one sign would resemble label i in
another. Neither needs a language to test.

1. Reuse: how many label words occur in more than one sign, against what
   the slot machine of exp. 36 (fitted on all labels of the manuscript)
   produces when asked for as many labels per sign.
2. Position: labels are listed in ZL in their order around the rings. For
   pairs of signs with 30 labels, agreement on features (starts with ot/ok/
   other, gallows, ending, length in signs) between labels at the same index
   against labels at different indices. Same with the index counted from the
   other end, in case the order runs the other way.
"""
import pathlib
import random
import sys
from collections import Counter, defaultdict
from itertools import combinations

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402
from voynich.assemble import GALLOWS, Assembler, signs  # noqa: E402

HERE = pathlib.Path(__file__).parent
SIGN = {"f70v2": "Pisces", "f70v1": "Aries (light)", "f71r": "Aries (dark)", "f71v": "Taurus (light)",
        "f72r1": "Taurus (dark)", "f72r2": "Gemini", "f72r3": "Cancer", "f72v3": "Leo", "f72v2": "Virgo",
        "f72v1": "Libra", "f73r": "Scorpio", "f73v": "Sagittarius"}
MERGE = {"Aries (light)": "Aries", "Aries (dark)": "Aries", "Taurus (light)": "Taurus", "Taurus (dark)": "Taurus"}
FEATS = {"start": lambda s: "ot" if "".join(s).startswith("ot") else "ok" if "".join(s).startswith("ok") else "other",
         "gallows": lambda s: next((x for x in s if x in GALLOWS), "-"),
         "ending": lambda s: s[-1], "length": lambda s: min(len(s), 6)}

v = Voynich("ZL")
labels = defaultdict(list)
for l in v.lines:
    if l.page in SIGN and l.unit.startswith("L") and l.words and "?" not in l.words[0]:
        labels[MERGE.get(SIGN[l.page], SIGN[l.page])].append(l.words[0])
all_labels = [w for l in v.lines if l.unit.startswith("L") for w in l.words[:1] if "?" not in w]

rng = random.Random(0)


def reuse(groups):
    seen = Counter()
    for ws in groups.values():
        for w in set(ws):
            seen[w] += 1
    words = [w for ws in groups.values() for w in ws]
    return sum(1 for w in words if seen[w] >= 2) / len(words), len(set(words)) / len(words)


m = Assembler(order=2).fit([[w] for w in all_labels])
sim = []
for seed in range(20):
    r = random.Random(seed)
    g = {k: ["".join(m.word(r, "middle", "#")) for _ in ws] for k, ws in labels.items()}
    sim.append(reuse(g))
obs = reuse(labels)
reuse_rows = [{"labels": "zodiac labels", "share in more than one sign": obs[0], "distinct / all": obs[1]},
              {"labels": "drawn from the label machine (20 runs, mean)",
               "share in more than one sign": sum(x[0] for x in sim) / 20, "distinct / all": sum(x[1] for x in sim) / 20},
              {"labels": "machine, highest of 20 runs", "share in more than one sign": max(x[0] for x in sim),
               "distinct / all": max(x[1] for x in sim)}]

full = {k: [signs(w) for w in ws] for k, ws in labels.items() if len(ws) == 30}
pos_rows = []
for f, g in FEATS.items():
    for direction in ("same order", "reversed"):
        same = other = n_same = n_other = 0
        for a, b in combinations(full, 2):
            A = [g(s) for s in full[a]]
            Bv = [g(s) for s in full[b]]
            if direction == "reversed":
                Bv = Bv[::-1]
            for i in range(30):
                same += A[i] == Bv[i]
                n_same += 1
                for j in range(30):
                    if j != i:
                        other += A[i] == Bv[j]
                        n_other += 1
        pos_rows.append({"feature": f, "index": direction, "agree at same index": same / n_same,
                         "agree at other indices": other / n_other, "ratio": (same / n_same) / (other / n_other)})
save(HERE, "zodiac", {"signs": {k: len(v_) for k, v_ in labels.items()}, "reuse": reuse_rows, "position": pos_rows})
md = "# 58 zodiac labels\n\nSigns and label counts: " + ", ".join(f"{k} {len(x)}" for k, x in labels.items()) + "\n\n"
md += "## Reuse across signs\n\n" + table(reuse_rows, ["labels", "share in more than one sign", "distinct / all"])
md += f"\n## Same position in different signs ({len(full)} signs with 30 labels)\n\n" + table(
    pos_rows, ["feature", "index", "agree at same index", "agree at other indices", "ratio"])
write_md(HERE, "zodiac", md)
print(md)
