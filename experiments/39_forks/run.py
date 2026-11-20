"""Do the forks follow the scribe or the subject?

Exp. 38: the words are walks through one small table, and what varies is
which way the walk goes at the forks (q- or o- or ch- at the start; gallows or
not; -edy, -aiin, -ol at the end). If the text says something, the choices at
the forks should follow the subject: a page about plants and a page about
bathing women should differ even in the same hand. If the forks are a
writer's habit, they should follow the hand and barely move with the subject.

The manuscript has a few crossings that let the two be separated. Davis's
hands against the illustration type:
  hand 1 (Currier A): herbal and pharmaceutical
  hand 2: herbal, balneological and text-only pages
  hand 3: herbal and stars
  herbal pages: hands 2, 3 and 5;  text-only pages: hands 2 and 5

Each page (60+ words) becomes a profile of fork choices: how its words start,
whether they carry a gallows, how they end. A control splits a single
section of a single hand into its first and second half (drift with time).
For each comparison, R^2 (share
of page-to-page variation explained by the grouping) with a permutation test
(pages shuffled between the groups being compared), and leave-one-page-out
nearest-centroid accuracy against chance.
"""
import pathlib
import random
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich

HERE = pathlib.Path(__file__).parent
MIN_WORDS = 60
PERMS = 2000
SECTIONS = {"H": "herbal", "P": "pharmaceutical", "B": "balneological", "S": "stars", "T": "text only",
            "C": "cosmological"}


def start(w):
    for p in ("qo", "q", "ch", "sh", "o", "d", "y", "s", "a"):
        if w.startswith(p):
            return p
    return "other"


def end(w):
    for e in ("edy", "eedy", "dy", "ey", "y", "aiin", "ain", "iin", "in", "al", "ol", "ar", "or", "l", "r", "m",
              "s", "o"):
        if w.endswith(e):
            return e
    return "other"


FEATS = [("start", s) for s in ("qo", "q", "ch", "sh", "o", "d", "y", "s", "a", "other")] + \
        [("gallows", g) for g in ("t", "k", "p", "f", "none")] + \
        [("end", e) for e in ("edy", "eedy", "dy", "ey", "y", "aiin", "ain", "iin", "in", "al", "ol", "ar", "or",
                              "l", "r", "m", "s", "o", "other")]


def profile(words):
    c = Counter()
    for w in words:
        c[("start", start(w))] += 1
        g = next((x for x in w if x in "tkpf"), "none")
        c[("gallows", g)] += 1
        c[("end", end(w))] += 1
    n = len(words)
    return np.array([c[f] / n for f in FEATS])


def r2(X, labels):
    mu = X.mean(0)
    tot = ((X - mu) ** 2).sum()
    within = sum(((X[labels == g] - X[labels == g].mean(0)) ** 2).sum() for g in set(labels))
    return 1 - within / tot


def loo_accuracy(X, labels):
    ok = 0
    for i in range(len(X)):
        keep = np.arange(len(X)) != i
        cents = {g: X[keep & (labels == g)].mean(0) for g in set(labels) if (keep & (labels == g)).any()}
        guess = min(cents, key=lambda g: ((X[i] - cents[g]) ** 2).sum())
        ok += guess == labels[i]
    return ok / len(X)


v = Voynich("ZL")
pages = defaultdict(list)
meta = {}
for l in v.lines:
    if l.unit == "P":
        pages[l.page] += [w for w in l.words if "?" not in w and "'" not in w]
        meta[l.page] = (l.meta.get("L"), l.meta.get("H"), l.meta.get("I"))
pages = {p: ws for p, ws in pages.items() if len(ws) >= MIN_WORDS and meta[p][1] and meta[p][2]}
X = {p: profile(ws) for p, ws in pages.items()}

comparisons = [
    ("subject, same hand", "hand 1: herbal vs pharmaceutical", lambda m: m[1] == "1" and m[2] in "HP", 2),
    ("subject, same hand", "hand 2: herbal vs balneological vs text", lambda m: m[1] == "2" and m[2] in "HBT", 2),
    ("subject, same hand", "hand 3: herbal vs stars", lambda m: m[1] == "3" and m[2] in "HS", 2),
    ("hand, same subject", "herbal, Currier B: hand 2 vs 3 vs 5", lambda m: m[2] == "H" and m[0] == "B", 1),
    ("hand, same subject", "text only: hand 2 vs 5", lambda m: m[2] == "T" and m[1] in "25", 1),
    ("hand, same subject", "herbal: hand 1 (A) vs hand 2 (B)", lambda m: m[2] == "H" and m[1] in "12", 1),
]
rng = np.random.default_rng(0)
rows = []
for kind, label, keep, by in comparisons:
    ps = [p for p in X if keep(meta[p])]
    lab = np.array([meta[p][by] for p in ps])
    M = np.array([X[p] for p in ps])
    obs = r2(M, lab)
    null = [r2(M, rng.permutation(lab)) for _ in range(PERMS)]
    acc = loo_accuracy(M, lab)
    chance = max(Counter(lab).values()) / len(lab)
    rows.append({"what varies": kind, "comparison": label,
                 "pages": " / ".join(f"{SECTIONS.get(g, 'hand ' + g)} {n}" for g, n in sorted(Counter(lab).items())),
                 "R2": obs, "R2 if random": float(np.mean(null)),
                 "p": (1 + sum(x >= obs for x in null)) / (PERMS + 1),
                 "pages told apart": acc, "chance": chance})
    print(rows[-1], flush=True)

# drift control: the same statistic for a split that has nothing to do with
# subject or hand: one section, one hand, first half of its pages (folio order)
# against the second half. Sections are contiguous runs of pages written at
# one time, so if fork habits drift as the book is written, two halves of the
# same section will differ too.
book_order = {p: k for k, p in enumerate(dict.fromkeys(l.page for l in v.lines))}
drift = [("hand 2 herbal", lambda m: m[1] == "2" and m[2] == "H"),
         ("hand 2 balneological", lambda m: m[1] == "2" and m[2] == "B"),
         ("hand 3 stars", lambda m: m[1] == "3" and m[2] == "S"),
         ("hand 1 herbal", lambda m: m[1] == "1" and m[2] == "H")]
for label, keep in drift:
    ps = sorted((p for p in X if keep(meta[p])), key=book_order.get)
    lab = np.array(["first half" if k < len(ps) / 2 else "second half" for k in range(len(ps))])
    M = np.array([X[p] for p in ps])
    obs = r2(M, lab)
    null = [r2(M, rng.permutation(lab)) for _ in range(PERMS)]
    rows.append({"what varies": "time only (control)", "comparison": f"{label}: first vs second half",
                 "pages": f"{len(ps) // 2 + len(ps) % 2} / {len(ps) // 2}", "R2": obs,
                 "R2 if random": float(np.mean(null)), "p": (1 + sum(x >= obs for x in null)) / (PERMS + 1),
                 "pages told apart": loo_accuracy(M, lab), "chance": 0.5})
    print(rows[-1], flush=True)

# subject in hand 2, two groups only, for a like-for-like comparison with the halves
ps = [p for p in X if meta[p][1] == "2" and meta[p][2] in "HB"]
lab = np.array([meta[p][2] for p in ps])
M = np.array([X[p] for p in ps])
obs = r2(M, lab)
null = [r2(M, rng.permutation(lab)) for _ in range(PERMS)]
rows.append({"what varies": "subject, same hand", "comparison": "hand 2: herbal vs balneological",
             "pages": f"herbal {sum(lab == 'H')} / balneological {sum(lab == 'B')}", "R2": obs,
             "R2 if random": float(np.mean(null)), "p": (1 + sum(x >= obs for x in null)) / (PERMS + 1),
             "pages told apart": loo_accuracy(M, lab), "chance": max(Counter(lab).values()) / len(lab)})

# which forks carry the hand-2 subject difference, and the herbal hand difference
detail = []
for label, keep, by in [("hand 2, by subject", lambda m: m[1] == "2" and m[2] in "HBT", 2),
                        ("herbal B, by hand", lambda m: m[2] == "H" and m[0] == "B", 1)]:
    ps = [p for p in X if keep(meta[p])]
    groups = defaultdict(list)
    for p in ps:
        groups[meta[p][by]].append(X[p])
    means = {g: np.mean(v, 0) for g, v in groups.items()}
    spread = np.ptp(np.array(list(means.values())), 0)
    for i in np.argsort(-spread)[:6]:
        detail.append({"comparison": label, "fork": f"{FEATS[i][0]} {FEATS[i][1]}",
                       **{SECTIONS.get(g, "hand " + g): float(means[g][i]) for g in sorted(means)}})

save(HERE, "forks", {"rows": rows, "detail": detail})
md = "# 39 forks: scribe or subject?\n\n" + table(
    rows, ["what varies", "comparison", "pages", "R2", "R2 if random", "p", "pages told apart", "chance"])
md += "\n## Forks that differ most\n\n"
for label in ("hand 2, by subject", "herbal B, by hand"):
    sub = [d for d in detail if d["comparison"] == label]
    md += f"### {label}\n\n" + table(sub, [k for k in sub[0] if k != "comparison"]) + "\n"
write_md(HERE, "forks", md)
print(md)
