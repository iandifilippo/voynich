"""Is the current page order meaningful?

Layfield & Davis (2026) argue the book was bound out of order. If pages that
sit next to each other were written together, their vocabularies should be
more alike than random page pairs. We test that in the current order and
inside each bifolium/quire, with a permutation baseline.
"""
import pathlib
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich

HERE = pathlib.Path(__file__).parent
v = Voynich("ZL")

order, bag, meta = [], defaultdict(Counter), {}
for l in v.lines:
    if l.page not in bag:
        order.append(l.page)
        meta[l.page] = l.meta
    bag[l.page].update(l.words)
order = [p for p in order if sum(bag[p].values()) >= 40]


def cos(a, b):
    num = sum(a[w] * b[w] for w in a if w in b)
    da = sum(x * x for x in a.values()) ** .5
    db = sum(x * x for x in b.values()) ** .5
    return num / (da * db) if da and db else 0.0


def mean_adjacent(seq):
    return sum(cos(bag[a], bag[b]) for a, b in zip(seq, seq[1:])) / (len(seq) - 1)


obs = mean_adjacent(order)
rng = random.Random(0)
null = []
for _ in range(2000):
    s = order[:]
    rng.shuffle(s)
    null.append(mean_adjacent(s))
p_adj = sum(x >= obs for x in null) / len(null)

# control for section/hand: shuffle only among pages of the same hand and illustration type
groups = defaultdict(list)
for p in order:
    groups[(meta[p].get("H"), meta[p].get("I"))].append(p)
null_strat = []
for _ in range(2000):
    pools = {k: rng.sample(g, len(g)) for k, g in groups.items()}
    idx = {k: 0 for k in groups}
    s = []
    for p in order:
        k = (meta[p].get("H"), meta[p].get("I"))
        s.append(pools[k][idx[k]])
        idx[k] += 1
    null_strat.append(mean_adjacent(s))
p_strat = sum(x >= obs for x in null_strat) / len(null_strat)

# where are the weakest joins? (candidate misbindings)
joins = sorted(({"from": a, "to": b, "cos": cos(bag[a], bag[b]),
                 "hand": f"{meta[a].get('H')}->{meta[b].get('H')}",
                 "section": f"{meta[a].get('I')}->{meta[b].get('I')}"}
                for a, b in zip(order, order[1:])), key=lambda r: r["cos"])

# Recto -> verso of the same leaf can never be separated by rebinding;
# verso -> next recto can. If the binding scrambled things, cross-leaf joins
# should look less related than same-leaf joins.
import re
def leaf(p):
    m = re.match(r"f(\d+)([rv])", p)
    return (int(m.group(1)), m.group(2)) if m else (None, None)


same_leaf, cross_leaf = [], []
for a, b in zip(order, order[1:]):
    (na, sa), (nb, sb) = leaf(a), leaf(b)
    if na is None or nb is None:
        continue
    c = cos(bag[a], bag[b])
    if na == nb and sa == "r" and sb == "v":
        same_leaf.append(c)
    elif sa == "v" and sb == "r" and na != nb:
        cross_leaf.append(c)
diff = sum(same_leaf) / len(same_leaf) - sum(cross_leaf) / len(cross_leaf)
pool = same_leaf + cross_leaf
perm = 0
for _ in range(5000):
    rng.shuffle(pool)
    a_, b_ = pool[:len(same_leaf)], pool[len(same_leaf):]
    if sum(a_) / len(a_) - sum(b_) / len(b_) >= diff:
        perm += 1
leaf_test = {"same_leaf_n": len(same_leaf), "same_leaf_mean": sum(same_leaf) / len(same_leaf),
             "cross_leaf_n": len(cross_leaf), "cross_leaf_mean": sum(cross_leaf) / len(cross_leaf),
             "diff": diff, "p": perm / 5000}

res = {"leaf_test": leaf_test, "pages": len(order), "observed": obs, "null_mean": sum(null) / len(null), "p_random": p_adj,
       "null_strat_mean": sum(null_strat) / len(null_strat), "p_within_hand_section": p_strat,
       "weakest_joins": joins[:25], "strongest_joins": joins[-15:]}
save(HERE, "page_order", res)
md = "# 04 page order\n\n"
md += f"{len(order)} pages with 40+ words. Mean cosine similarity of word counts between consecutive pages:\n\n"
md += f"- current order: **{obs:.3f}**\n- random order: {res['null_mean']:.3f} (p = {p_adj:.4f})\n"
md += f"- shuffled only within same hand + illustration type: {res['null_strat_mean']:.3f} (p = {p_strat:.4f})\n\n"
md += "If the second p is small, neighbouring pages share vocabulary beyond what hand and topic explain.\n\n"
md += "## same leaf vs across leaves\n\n"
md += f"- recto->verso of the same leaf ({leaf_test['same_leaf_n']} joins): mean cos {leaf_test['same_leaf_mean']:.3f}\n"
md += f"- verso->next recto ({leaf_test['cross_leaf_n']} joins): mean cos {leaf_test['cross_leaf_mean']:.3f}\n"
md += f"- difference {leaf_test['diff']:.3f}, permutation p = {leaf_test['p']:.4f}\n\n"
md += "## weakest joins in the current order\n\n" + table(joins[:20], ["from", "to", "cos", "hand", "section"])
md += "\n## strongest joins\n\n" + table(joins[-10:], ["from", "to", "cos", "hand", "section"])
write_md(HERE, "page_order", md)
print(md)
