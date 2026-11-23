"""Twin plants: does a pharma label turn up in the text of its herbal twin?

Several people have pointed out plants in the pharma section that are
redrawn from a page of the herbal section (the root, the leaf shape, the
berry cluster are the same). A list of twelve such pairs, with who first
proposed each, is in d2kx/voynich-research (attack 169). If the small label
written next to the pharma plant is its name, the same word, or something
close to it, should be somewhere in the herbal page that describes the same
plant. That is a test that doesn't need to know the language: it only asks
whether the label is closer to its twin page than to the other herbal pages.

For each label next to a twin plant (and, as a looser version, for every
label on the pharma sheet), score each herbal page by:
  exact   the label occurs as a word on the page
  near    some word on the page is at most one sign away
  sim     best similarity to any word on the page (1 - signs edit distance / longer)
and with an initial o-/y- removed from both sides (60% of labels start
with o-; exp 45).

Longer pages win on all three just by having more words, so the twin page
is ranked only against herbal pages of the same Currier language whose
word count is within 30% of it. The statistic is the twin's percentile
among them (0 = best, 0.5 = chance), averaged over labels, with a p-value
from drawing a random page of the same pool for every label instead.

Power: the same test with the label planted once at a random place in its
twin page (as if the name were mentioned once in the text), and with a
one-sign variant planted instead.
"""
import pathlib
import random
import sys
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402
from voynich.assemble import signs  # noqa: E402

HERE = pathlib.Path(__file__).parent
# herbal folio, pharma folio, labels written next to the pharma plant; the
# names after each pair are the people the list credits for the match.
PAIRS = [
    ('01', 'f1v', 'f102r1', ['ddardsh']),  # Petersen, Stolfi
    ('02', 'f18v', 'f102r2', ['loeekadag', 'osheal', 'sodch', 'koldarod', 'odalydary']),  # FSG, Stolfi
    ('03', 'f19r', 'f102v1', ['ypcholdy', 'loralody', 'opchdard']),  # Stolfi, Petersen
    ('04', 'f23r', 'f102r2', ['loeekadag', 'osheal', 'sodch', 'koldarod', 'odalydary']),  # FSG, Landini (GL)
    ('05', 'f32v', 'f102r2', ['kodaiig']),  # FSG, Stolfi
    ('06', 'f37v', 'f102r1', ['ddardsh']),  # Stolfi
    ('07', 'f39r', 'f95r2', []),  # Stolfi, Zandbergen
    ('08', 'f47v', 'f102r2', ['kodaiig']),  # Petersen, Holm
    ('09', 'f48r', 'f89v2', ['opaloiiry', 'otaram', 'chtchy', 'sada', 'daseky']),  # Stolfi
    ('10', 'f48v', 'f89v1', ['okoraldy', 'otoikhy', 'otchar', 'darshody']),  # Stolfi
    ('11', 'f90v2', 'f100r', ['chosaroshol', 'sochorcfhy', 'otear', 'chofary', 'sar', 'char', 'daiindy', 'oraro', 'chalsain', 'soity', 'sosam', 'dakocth', 'sofam']),  # Stolfi
    ('12', 'f96v', 'f99r', ['yteoldy', 'tolsasy']),  # Landini (GL)
]

v = Voynich("ZL")
text = defaultdict(list)
lang = {}
labels_on = defaultdict(list)
section = {}
for l in v.lines:
    section.setdefault(l.page, l.section)
    lang.setdefault(l.page, l.language)
    words = [w for w in l.words if "?" not in w]
    if l.unit.startswith("L"):
        labels_on[l.page] += words
    else:
        text[l.page] += words

pairs = [{"pair_id": i, "herbal_folio": h, "pharma_folio": f, "pharma_register_labels": ls} for i, h, f, ls in PAIRS]
herbal = sorted({p for p in text if section.get(p) == "H"} | {p["herbal_folio"] for p in pairs})


def ed(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[-1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def strip(s):
    return s[1:] if len(s) > 2 and s[0] in ("o", "y") else s


def scores(label, words, stripped=False):
    a = signs(label)
    if stripped:
        a = strip(a)
    best_d, best_s = 99, 0.0
    for w in set(words):
        b = signs(w)
        if stripped:
            b = strip(b)
        if abs(len(a) - len(b)) > 3:
            continue
        d = ed(a, b)
        best_d = min(best_d, d)
        best_s = max(best_s, 1 - d / max(len(a), len(b)))
    return {"exact": float(best_d == 0), "near": float(best_d <= 1), "sim": best_s}


def pool(twin):
    n = len(text[twin])
    return [p for p in herbal if p != twin and lang.get(p) == lang.get(twin) and 0.7 * n <= len(text[p]) <= 1.3 * n]


def percentile(val, others):
    worse = sum(o < val for o in others)
    tie = sum(o == val for o in others)
    better = len(others) - worse - tie
    return (better + 0.5 * tie) / len(others)


def run(items, pages, stripped, rng, reps=2000):
    """items: (label, twin). pages: dict page -> words (may be edited for power)."""
    cache = {}

    def sc(lab, p):
        k = (lab, p)
        if k not in cache:
            cache[k] = scores(lab, pages[p], stripped)
        return cache[k]

    out = {}
    for key in ("exact", "near", "sim"):
        obs, nulls = [], [[] for _ in range(reps)]
        hits_twin = 0
        for lab, twin in items:
            others = pool(twin)
            vals = {p: sc(lab, p)[key] for p in others}
            t = sc(lab, twin)[key]
            hits_twin += t if key != "sim" else 0
            obs.append(percentile(t, list(vals.values())))
            for r in range(reps):
                q = rng.choice(others)
                nulls[r].append(percentile(vals[q], [vals[o] for o in others if o != q] + [t]))
        m = sum(obs) / len(obs)
        null = [sum(x) / len(x) for x in nulls]
        out[key] = {"percentile": m, "null_mean": sum(null) / reps,
                    "p": (1 + sum(x <= m for x in null)) / (reps + 1), "twin_hits": hits_twin}
    return out


def variant(w, rng):
    s = signs(w)
    i = rng.randrange(len(s))
    alt = rng.choice(["o", "a", "e", "y", "d", "l", "r", "ch", "k", "t"])
    return "".join(s[:i] + [alt] + s[i + 1:])


tight, loose = [], []
for p in pairs:
    if p["herbal_folio"] not in text or not p["pharma_register_labels"]:
        continue
    for lab in p["pharma_register_labels"]:
        tight.append((lab, p["herbal_folio"]))
    for lab in labels_on[p["pharma_folio"]]:
        loose.append((lab, p["herbal_folio"]))

rows, res = [], {}
for name, items in (("labels by the twin plant", tight), ("all labels on the pharma sheet", loose)):
    for stripped in (False, True):
        rng = random.Random(1)
        r = run(items, text, stripped, rng)
        tag = f"{name}{' (o-/y- removed)' if stripped else ''}"
        res[tag] = r
        for key, x in r.items():
            rows.append({"set": tag, "n": len(items), "score": key, "twin percentile": x["percentile"],
                         "null": x["null_mean"], "p": x["p"], "twin hits": int(x["twin_hits"])})

# power: plant the label (or a one-sign variant) once into the twin page
power = []
for kind in ("label planted once", "one-sign variant planted once"):
    pv = []
    for seed in range(5):
        rng = random.Random(100 + seed)
        pages = {p: list(ws) for p, ws in text.items()}
        for lab, twin in tight:
            w = lab if kind.startswith("label") else variant(lab, rng)
            pages[twin].insert(rng.randrange(len(pages[twin]) + 1), w)
        r = run(tight, pages, False, rng, reps=500)
        pv.append(r)
    for key in ("exact", "near", "sim"):
        power.append({"planted": kind, "score": key,
                      "twin percentile": sum(x[key]["percentile"] for x in pv) / 5,
                      "p (mean of 5)": sum(x[key]["p"] for x in pv) / 5})

# per pair detail (tight, sim)
detail = []
for p in pairs:
    if p["herbal_folio"] not in text or not p["pharma_register_labels"]:
        continue
    twin = p["herbal_folio"]
    others = pool(twin)
    for lab in p["pharma_register_labels"]:
        t = scores(lab, text[twin])
        per = percentile(t["sim"], [scores(lab, text[o])["sim"] for o in others])
        detail.append({"pair": p["pair_id"], "herbal": twin, "pharma": p["pharma_folio"], "label": lab,
                       "exact": int(t["exact"]), "near": int(t["near"]), "sim": t["sim"],
                       "percentile": per, "pool": len(others)})

save(HERE, "twins", {"rows": rows, "power": power, "detail": detail})
md = "## Twin page against length-matched herbal pages\n\n"
md += table(rows, ["set", "n", "score", "twin percentile", "null", "p", "twin hits"])
md += "\n## Power (label or variant planted once in its twin page)\n\n"
md += table(power, ["planted", "score", "twin percentile", "p (mean of 5)"])
md += "\n## Each label next to a twin plant\n\n"
md += table(detail, ["pair", "herbal", "pharma", "label", "exact", "near", "sim", "percentile", "pool"], {"sim": ".2f", "percentile": ".2f"})
write_md(HERE, "twins", md)
print(md)
