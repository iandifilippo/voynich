"""Were bifolia written as units? (singulion hypothesis, Layfield & Davis 2026)

In a nested quire the two leaves of one bifolium end up far apart: f1 pairs
with f8, f2 with f7, and so on. If the text was written straight through the
quire as it is bound now, conjoint leaves have no reason to share more
vocabulary than any other pair of leaves at the same distance. If each
bifolium was written as a unit and the quires were assembled afterwards,
conjoint leaves should look more alike.

Leaves are compared as bags of words (recto + verso). Pairs are only compared
inside a quire, and the main statistic only uses pairs with the same scribe and
the same illustration type, so hand and topic can't drive the result.
Null: re-pair the leaves of each quire into random bifolia.
"""
import pathlib
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich

HERE = pathlib.Path(__file__).parent
v = Voynich("ZL")

leaf_words = defaultdict(Counter)
leaf_meta = {}
for l in v.lines:
    m = re.match(r"f(\d+)", l.page)
    if not m:
        continue
    leaf = int(m.group(1))
    leaf_words[leaf].update(l.words)
    meta = l.meta
    leaf_meta.setdefault(leaf, {"Q": meta.get("Q"), "B": meta.get("B"), "H": meta.get("H"), "I": meta.get("I")})

leaves = [x for x in sorted(leaf_words) if sum(leaf_words[x].values()) >= 60 and leaf_meta[x]["Q"]]
by_quire = defaultdict(list)
for x in leaves:
    by_quire[leaf_meta[x]["Q"]].append(x)


def cos(a, b):
    num = sum(a[w] * b[w] for w in a if w in b)
    da = sum(c * c for c in a.values()) ** .5
    db = sum(c * c for c in b.values()) ** .5
    return num / (da * db)


import math

df = Counter(w for x in leaves for w in leaf_words[x])
top = {w for w, _ in Counter(w for x in leaves for w, c in leaf_words[x].items() for _ in range(c)).most_common(50)}


def tfidf(a):
    return Counter({w: c * math.log(len(leaves) / df[w]) for w, c in a.items()})


def jaccard_rare(a, b):
    A = {w for w in a if w not in top and df[w] >= 2}
    B = {w for w in b if w not in top and df[w] >= 2}
    return len(A & B) / len(A | B) if A | B else 0.0


MEASURES = {
    "cosine": lambda a, b: cos(leaf_words[a], leaf_words[b]),
    "tfidf_cosine": lambda a, b: cos(tfidf(leaf_words[a]), tfidf(leaf_words[b])),
    "jaccard_no_top50": lambda a, b: jaccard_rare(leaf_words[a], leaf_words[b]),
}
SIMS = {}
for name, f in MEASURES.items():
    SIMS[name] = {}
    for q, ls in by_quire.items():
        for i in range(len(ls)):
            for j in range(i + 1, len(ls)):
                SIMS[name][(ls[i], ls[j])] = f(ls[i], ls[j])
sim = SIMS["cosine"]


def same_context(a, b):
    return leaf_meta[a]["H"] == leaf_meta[b]["H"] and leaf_meta[a]["I"] == leaf_meta[b]["I"]


def stat(bifolium_of):
    conj, other = [], []
    for (a, b), s in sim.items():
        if not same_context(a, b):
            continue
        if bifolium_of[a] == bifolium_of[b]:
            conj.append(s)
        else:
            other.append(s)
    if not conj or not other:
        return None, 0, 0
    return sum(conj) / len(conj) - sum(other) / len(other), len(conj), len(other)


real = {x: (leaf_meta[x]["Q"], leaf_meta[x]["B"]) for x in leaves}


def fake_pairing(rng):
    fake = {}
    for q, ls in by_quire.items():
        sizes = Counter(real[x] for x in ls)
        pool = ls[:]
        rng.shuffle(pool)
        i = 0
        for b, n in sizes.items():
            for x in pool[i:i + n]:
                fake[x] = b
            i += n
    return fake


robust = []
for name in MEASURES:
    sim = SIMS[name]
    o, nc, no = stat(real)
    r2 = random.Random(1)
    nl = [stat(fake_pairing(r2))[0] for _ in range(2000)]
    nl = [x for x in nl if x is not None]
    wins = 0
    nq = 0
    for q, ls in by_quire.items():
        c = [s for (a, b), s in sim.items() if a in ls and b in ls and same_context(a, b) and real[a] == real[b]]
        oo = [s for (a, b), s in sim.items() if a in ls and b in ls and same_context(a, b) and real[a] != real[b]]
        if c and oo:
            nq += 1
            wins += sum(c) / len(c) > sum(oo) / len(oo)
    robust.append({"measure": name, "diff": o, "null_mean": sum(nl) / len(nl),
                   "p": sum(x >= o for x in nl) / len(nl), "quires_conjoint_higher": f"{wins}/{nq}"})
sim = SIMS["cosine"]
obs, n_conj, n_other = stat(real)

rng = random.Random(0)
null = []
for _ in range(5000):
    fake = {}
    for q, ls in by_quire.items():
        sizes = Counter(real[x] for x in ls)
        pool = ls[:]
        rng.shuffle(pool)
        i = 0
        for b, n in sizes.items():
            for x in pool[i:i + n]:
                fake[x] = b
            i += n
    d, _, _ = stat(fake)
    if d is not None:
        null.append(d)
p = sum(x >= obs for x in null) / len(null)

# distance-matched view: conjoint pairs vs non-conjoint pairs at the same leaf distance
by_dist = defaultdict(lambda: {"conj": [], "other": []})
for (a, b), s in sim.items():
    if not same_context(a, b):
        continue
    d = abs(leaves.index(b) - leaves.index(a))
    by_dist[d]["conj" if real[a] == real[b] else "other"].append(s)
dist_rows = []
for d in sorted(by_dist):
    c, o = by_dist[d]["conj"], by_dist[d]["other"]
    if c and o:
        dist_rows.append({"leaf_distance": d, "conjoint_n": len(c), "conjoint_cos": sum(c) / len(c),
                          "other_n": len(o), "other_cos": sum(o) / len(o)})

# per quire
quire_rows = []
for q, ls in sorted(by_quire.items()):
    c = [s for (a, b), s in sim.items() if a in ls and b in ls and same_context(a, b) and real[a] == real[b]]
    o = [s for (a, b), s in sim.items() if a in ls and b in ls and same_context(a, b) and real[a] != real[b]]
    adj = [s for (a, b), s in sim.items() if a in ls and b in ls and same_context(a, b) and abs(ls.index(a) - ls.index(b)) == 1 and real[a] != real[b]]
    if c and o:
        quire_rows.append({"quire": q, "leaves": len(ls), "conjoint_n": len(c), "conjoint_cos": sum(c) / len(c),
                           "other_cos": sum(o) / len(o), "adjacent_nonconjoint_cos": (sum(adj) / len(adj)) if adj else None})

res = {"robustness": robust, "leaves": len(leaves), "observed_diff": obs, "conjoint_pairs": n_conj, "other_pairs": n_other,
       "null_mean": sum(null) / len(null), "p": p, "by_distance": dist_rows, "by_quire": quire_rows}
save(HERE, "bifolia", res)

md = "# 09 bifolia\n\n"
md += f"{len(leaves)} leaves with 60+ words. Pairs compared only within a quire and only when both leaves share scribe and illustration type.\n\n"
md += f"- conjoint pairs (same bifolium): {n_conj}\n- other pairs: {n_other}\n"
md += f"- mean cosine, conjoint minus other: **{obs:+.3f}** (random re-pairing: {res['null_mean']:+.3f}, p = {p:.4f})\n\n"
md += "## other similarity measures (2000 re-pairings each)\n\n" + table(robust, ["measure", "diff", "null_mean", "p", "quires_conjoint_higher"]) + "\n"
md += "## by leaf distance in the current order\n\n" + table(dist_rows, ["leaf_distance", "conjoint_n", "conjoint_cos", "other_n", "other_cos"])
md += "\n## by quire\n\n" + table(quire_rows, ["quire", "leaves", "conjoint_n", "conjoint_cos", "other_cos", "adjacent_nonconjoint_cos"])
write_md(HERE, "bifolia", md)
print(md)
