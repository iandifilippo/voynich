"""Zodiac nymph labels.

Each zodiac diagram has ~30 labelled figures, and the months are written in
the margins in a Romance dialect. Three questions:

T1  numbering: if label i meant "day/degree i", labels at the same position in
    different signs should look alike more often than labels at different positions.
T2  Cisiojanus (Pelling's idea): align label i with syllable i of that month's
    Cisiojanus line and test whether syllable similarity predicts label similarity
    (Mantel-style permutation test). Two alignments: calendar month, and the
    astrological span of the sign (starts around the 21st of the previous month).
T3  composition: prefix shares per sign (ot-/ok- seasonal shift, already noted
    by Zandbergen, Pelling and others; recomputed here for completeness).

Labels are taken in transcription order (ZL gives each a clock position).
"""
import pathlib
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich
from voynich.cisiojanus import months as cisio_months, DAYS

HERE = pathlib.Path(__file__).parent

SIGNS = [  # page(s), sign, marginal month, month number
    (["f70v2"], "Pisces", "mars", 3),
    (["f70v1", "f71r"], "Aries", "abril", 4),
    (["f71v", "f72r1"], "Taurus", "may", 5),
    (["f72r2"], "Gemini", "yony", 6),
    (["f72r3"], "Cancer", "jollet", 7),
    (["f72v3"], "Leo", "augst", 8),
    (["f72v2"], "Virgo", "setembre", 9),
    (["f72v1"], "Libra", "octembre", 10),
    (["f73r"], "Scorpio", "nouembre", 11),
    (["f73v"], "Sagittarius", "dezembre", 12),
]

v = Voynich("ZL", keep_uncertain=True)
labels = defaultdict(list)
for l in v.select(section=["Z"], unit="L"):
    labels[l.page].append(l.words[0] if l.words else "")

signs = []
for pages, sign, month, mnum in SIGNS:
    labs = [w for p in pages for w in labels[p]]
    signs.append({"sign": sign, "month": month, "mnum": mnum, "labels": labs})


def bigrams(w):
    w = f"^{w}$"
    return {w[i:i + 2] for i in range(len(w) - 1)}


def sim(a, b):
    if not a or not b or "?" in a or "?" in b:
        return None
    A, B = bigrams(a), bigrams(b)
    return len(A & B) / len(A | B)


rng = random.Random(0)

# ---- T1: same position across signs
def t1_stat(lists):
    same, diff = [], []
    for i in range(len(lists)):
        for j in range(i + 1, len(lists)):
            for p, a in enumerate(lists[i]):
                for q, b in enumerate(lists[j]):
                    s = sim(a, b)
                    if s is None:
                        continue
                    (same if p == q else diff).append(s)
    return sum(same) / len(same) - sum(diff) / len(diff)


full = [s["labels"][:30] for s in signs if len(s["labels"]) >= 29]
obs1 = t1_stat(full)
null1 = []
for _ in range(300):
    null1.append(t1_stat([rng.sample(x, len(x)) for x in full]))
p1 = sum(x >= obs1 for x in null1) / len(null1)

# also with reversed order (counter-clockwise reading)
obs1r = t1_stat([x[::-1] for x in full[:1]] + full[1:])

# robustness: the same test with blunter similarity measures
def t1_eq(lists, f):
    same = diff = ns = nd = 0
    for i in range(len(lists)):
        for j in range(i + 1, len(lists)):
            for p, a in enumerate(lists[i]):
                for q, b in enumerate(lists[j]):
                    if not a or not b or "?" in a or "?" in b:
                        continue
                    x = f(a, b)
                    if p == q:
                        same += x
                        ns += 1
                    else:
                        diff += x
                        nd += 1
    return same / ns - diff / nd


MEASURES = {
    "prefix2": lambda a, b: float(a[:2] == b[:2]),
    "suffix2": lambda a, b: float(a[-2:] == b[-2:]),
    "first_glyph": lambda a, b: float(a[:1] == b[:1]),
    "same_length": lambda a, b: float(len(a) == len(b)),
}
t1b = []
for name, f in MEASURES.items():
    o = t1_eq(full, f)
    null = [t1_eq([rng.sample(x, len(x)) for x in full], f) for _ in range(1000)]
    t1b.append({"measure": name, "obs": o, "p": sum(x >= o for x in null) / len(null)})

# ---- T2: Cisiojanus
cis = cisio_months()


def syl_sim(a, b):
    A, B = bigrams(a), bigrams(b)
    return len(A & B) / len(A | B)


def mantel(lab, syl, perms=2000):
    n = min(len(lab), len(syl))
    lab, syl = lab[:n], syl[:n]
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    ls = {(i, j): sim(lab[i], lab[j]) for i, j in pairs}
    pairs = [p for p in pairs if ls[p] is not None]
    if len(pairs) < 20:
        return None, None

    def corr(order):
        xs = [ls[(i, j)] for i, j in pairs]
        ys = [syl_sim(syl[order[i]], syl[order[j]]) for i, j in pairs]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        den = (sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** .5
        return num / den if den else 0.0

    idx = list(range(n))
    r = corr(idx)
    hits = 0
    for _ in range(perms):
        o = idx[:]
        rng.shuffle(o)
        if corr(o) >= r:
            hits += 1
    return r, hits / perms


def span_syllables(mnum):
    """Days of the sign: 21st of previous month to 20th of this one."""
    prev = 12 if mnum == 1 else mnum - 1
    return cis[prev][20:] + cis[mnum][:20]


t2 = []
for s in signs:
    labs = s["labels"]
    for align, syl in (("calendar month", cis[s["mnum"]]), ("sign span", span_syllables(s["mnum"]))):
        for direction, ll in (("as transcribed", labs), ("reversed", labs[::-1])):
            r, p = mantel(ll, syl)
            t2.append({"sign": s["sign"], "alignment": align, "direction": direction,
                       "n": min(len(ll), len(syl)), "r": r, "p": p})

# combine: how many tests reach p < 0.05 vs the ~5% expected by chance
valid = [x for x in t2 if x["p"] is not None]
hits = sum(x["p"] < 0.05 for x in valid)

# ---- T3: prefixes per sign
t3 = []
for s in signs:
    c = Counter(w[:2] for w in s["labels"] if w)
    n = sum(c.values())
    t3.append({"sign": s["sign"], "month": s["month"], "labels": n,
               "ot": c["ot"] / n, "ok": c["ok"] / n, "oe": c["oe"] / n, "ch/sh": (c["ch"] + c["sh"]) / n,
               "o_any": sum(v for k, v in c.items() if k.startswith("o")) / n})

save(HERE, "zodiac", {"signs": signs, "t1": {"obs": obs1, "p": p1, "reversed_first": obs1r, "robustness": t1b},
                      "t2": t2, "t2_hits": hits, "t2_tests": len(valid), "t3": t3})

md = "# 06 zodiac labels\n\n"
md += "## labels by sign (transcription order)\n\n"
for s in signs:
    md += f"- **{s['sign']}** ({s['month']}, {len(s['labels'])}): " + " ".join(s["labels"]) + "\n"
md += f"\n## T1 numbering\n\nMean bigram-Jaccard similarity of labels at the same position minus at different positions, across signs: **{obs1:+.4f}** (permutation p = {p1:.3f}).\n\n"
md += "A positive, significant value would support labels encoding position (day/degree number).\n\n"
md += "Same test with blunter measures (1000 permutations each):\n\n" + table(t1b, ["measure", "obs", "p"]) + "\n"
md += "## T2 Cisiojanus\n\n"
md += f"{len(valid)} Mantel tests, {hits} with p < 0.05 (about {0.05 * len(valid):.1f} expected by chance).\n\n"
md += table(t2, ["sign", "alignment", "direction", "n", "r", "p"])
md += "\n## T3 prefixes\n\n" + table(t3, ["sign", "month", "labels", "ot", "ok", "oe", "ch/sh", "o_any"])
write_md(HERE, "zodiac", md)
print(md)
