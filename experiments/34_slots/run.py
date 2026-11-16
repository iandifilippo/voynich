"""Are the positions of a word filled independently?

Several proposals have the text coming out of a device: a volvelle (García
Jiménez, c10), a table (Rugg), a grille. The simplest device has one ring or
column per position in the word and picks from each separately. That makes a
hard prediction: knowing what sits in one position tells you nothing about
the others.

Words are parsed into twelve ordered slots, after Zattera's slot grammar
(2022): each slot holds one of a few glyphs or nothing, and the slots are
used in order. Then, for the words that parse:

  1. how much information the slots share (sum of slot entropies minus the
     entropy of the whole word), against the same columns shuffled
     independently, which is exactly what an independent device would give;
  2. held-out cost per word under three models: independent slots, a chain
     (each slot given the last glyph written), and the chain plus the split
     prefix / core / suffix;
  3. whether the start of a word knows about its end once the middle is
     fixed (suffix shuffled among words with the same core);
  4. what an independent device would have produced: number of distinct
     words in a text this long, and how many of them the manuscript has.

Controls: the copying model and a Naibbe cipher of Pliny, which is a
table-driven device.
"""
import json
import math
import pathlib
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich
from voynich.autocopy import AutoCopy
from voynich.corpus import DATA

HERE = pathlib.Path(__file__).parent
SLOTS = [("q", "s", "d"), ("y", "o"), ("l", "r"), ("t", "k", "p", "f"), ("ch", "sh"),
         ("cth", "ckh", "cph", "cfh"), ("eee", "ee", "e"), ("s", "d"), ("o", "a"),
         ("iii", "ii", "i"), ("d", "l", "r", "m", "n"), ("y",)]
GROUPS = {"prefix": (0, 1, 2), "core": (3, 4, 5, 6, 7), "suffix": (8, 9, 10, 11)}
N = len(SLOTS)


def parse(word, late=False):
    """First parse found, trying to fill early slots first (or late ones)."""
    def go(i, s):
        if i == len(word):
            return [""] * (N - s)
        if s == N:
            return None
        opts = [g for g in SLOTS[s] if word.startswith(g, i)] + [""]
        if late:
            opts = opts[::-1]
        for g in opts:
            rest = go(i + len(g), s + 1)
            if rest is not None:
                return [g] + rest
        return None
    r = go(0, 0)
    return tuple(r) if r else None


def H(counter):
    n = sum(counter.values())
    return -sum(c / n * math.log2(c / n) for c in counter.values())


def total_corr(rows):
    return sum(H(Counter(r[i] for r in rows)) for i in range(N)) - H(Counter(rows))


def shuffled(rows, rng):
    cols = [[r[i] for r in rows] for i in range(N)]
    for c in cols:
        rng.shuffle(c)
    return list(zip(*cols))


def grp(r, name):
    return tuple(r[i] for i in GROUPS[name])


def cond_mi(rows, a, b, c):
    """I(a; b | c) over groups of slots, plug-in."""
    by = defaultdict(list)
    for r in rows:
        by[grp(r, c)].append((grp(r, a), grp(r, b)))
    n, tot = len(rows), 0.0
    for pairs in by.values():
        ha = H(Counter(x for x, _ in pairs))
        hb = H(Counter(y for _, y in pairs))
        hab = H(Counter(pairs))
        tot += len(pairs) / n * (ha + hb - hab)
    return tot


def cond_mi_null(rows, a, b, c, rng, reps=200):
    by = defaultdict(list)
    for r in rows:
        by[grp(r, c)].append(r)
    out = []
    for _ in range(reps):
        new = []
        for rs in by.values():
            bs = [grp(r, b) for r in rs]
            rng.shuffle(bs)
            for r, x in zip(rs, bs):
                r = list(r)
                for i, g in zip(GROUPS[b], x):
                    r[i] = g
                new.append(tuple(r))
        out.append(cond_mi(new, a, b, c))
    return out


def heldout(rows, rng, folds=5, alpha=0.1):
    """Bits per word on held-out tokens."""
    idx = list(range(len(rows)))
    rng.shuffle(idx)
    cost = Counter()
    for f in range(folds):
        test = [rows[i] for i in idx[f::folds]]
        train = [rows[i] for k, i in enumerate(idx) if k % folds != f]
        ind = [Counter(r[i] for r in train) for i in range(N)]
        chain = [defaultdict(Counter) for _ in range(N)]
        chain3 = [defaultdict(Counter) for _ in range(N)]
        for r in train:
            last = "^"
            for i in range(N):
                chain[i][last][r[i]] += 1
                g = "prefix" if i < 3 else "core" if i < 8 else "suffix"
                ctx3 = (last, grp(r, "prefix") if g != "prefix" else None, grp(r, "core") if g == "suffix" else None)
                chain3[i][ctx3][r[i]] += 1
                if r[i]:
                    last = r[i]
        for r in test:
            last = "^"
            for i in range(N):
                k = len(SLOTS[i]) + 1
                cost["independent slots"] -= math.log2((ind[i][r[i]] + alpha) / (len(train) + alpha * k))
                c = chain[i][last]
                pc = (c[r[i]] + alpha) / (sum(c.values()) + alpha * k)
                cost["chain"] -= math.log2(pc)
                g = "prefix" if i < 3 else "core" if i < 8 else "suffix"
                ctx3 = (last, grp(r, "prefix") if g != "prefix" else None, grp(r, "core") if g == "suffix" else None)
                c3 = chain3[i][ctx3]
                lam = sum(c3.values()) / (sum(c3.values()) + 5.0)
                cost["whole word so far"] -= math.log2(lam * (c3[r[i]] / sum(c3.values()) if c3 else 0) + (1 - lam) * pc)
                if r[i]:
                    last = r[i]
    return {k: x / len(rows) for k, x in cost.items()}


def device(rows, rng, n):
    cols = [[r[i] for r in rows] for i in range(N)]
    return ["".join(rng.choice(c) for c in cols) for _ in range(n)]


chart = {k: set(x) for k, x in json.loads(
    (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}
v = Voynich("ZL")
body = [l for l in v.lines if l.unit == "P"]
texts = {"VMS, Currier A": [w for l in body if l.meta.get("L") == "A" for w in l.words],
         "VMS, Currier B": [w for l in body if l.meta.get("L") == "B" for w in l.words],
         "copying model": [w for l in AutoCopy(seed=1, boundary=chart, boundary_p=0.65, line_end_p=0.5,
                                               common_p=0.5).run(4500) for w in l]}
src = DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt"
if src.exists():
    texts["Naibbe cipher of Pliny"] = open(src, encoding="utf-8-sig").read().split()[:30000]

rng = random.Random(0)
summary, models, ends, dev, pairs = [], [], [], [], {}
for name, words in texts.items():
    words = [w for w in words if w and "?" not in w]
    for late in (False, True):
        rows = [p for p in (parse(w, late) for w in words) if p]
        if late and not name.startswith("VMS"):
            continue
        types = set(words)
        tc = total_corr(rows)
        base = [total_corr(shuffled(rows, rng)) for _ in range(10)]
        hj = H(Counter(rows))
        summary.append({"text": name, "parse": "late slots first" if late else "early slots first",
                        "words": len(words), "parsed": len(rows) / len(words),
                        "distinct words parsed": sum(1 for t in types if parse(t)) / len(types),
                        "sum of slot entropies": tc + hj, "word entropy": hj, "shared (bits)": tc,
                        "shared if independent": sum(base) / len(base)})
        print(summary[-1], flush=True)
        if late:
            continue
        m = heldout(rows, rng)
        models.append({"text": name, **m})
        obs = cond_mi(rows, "prefix", "suffix", "core")
        null = cond_mi_null(rows, "prefix", "suffix", "core", rng)
        ends.append({"text": name, "I(prefix; suffix | core)": obs, "suffix shuffled within core": sum(null) / len(null),
                     "excess (bits)": obs - sum(null) / len(null), "p": (1 + sum(x >= obs for x in null)) / (len(null) + 1)})
        real = Counter("".join(r) for r in rows)
        made = Counter(device(rows, rng, len(rows)))
        dev.append({"text": name, "distinct words, real": len(real), "distinct words, independent device": len(made),
                    "device words that exist in the text (types)": sum(1 for w in made if w in real) / len(made),
                    "device words that exist (tokens)": sum(c for w, c in made.items() if w in real) / len(rows),
                    "real words the device made (types)": sum(1 for w in real if w in made) / len(real)})
        print(models[-1], ends[-1], dev[-1], flush=True)
        # pairwise, bias removed
        sh = [shuffled(rows, rng) for _ in range(5)]
        mat = {}
        for i in range(N):
            for j in range(i + 1, N):
                def mi(rs):
                    return H(Counter(r[i] for r in rs)) + H(Counter(r[j] for r in rs)) - H(Counter((r[i], r[j]) for r in rs))
                mat[f"{i}-{j}"] = mi(rows) - sum(mi(s) for s in sh) / len(sh)
        pairs[name] = mat

by_dist = []
for name, mat in pairs.items():
    row = {"text": name}
    for d in (1, 2, 3, 4, 6, 8):
        xs = [x for k, x in mat.items() if int(k.split("-")[1]) - int(k.split("-")[0]) == d]
        row[f"{d} apart"] = sum(xs)
    row["all pairs"] = sum(mat.values())
    row["pairs 4+ apart, share"] = sum(x for k, x in mat.items() if int(k.split("-")[1]) - int(k.split("-")[0]) >= 4) / sum(mat.values())
    by_dist.append(row)
top = []
for name in ("VMS, Currier A", "VMS, Currier B"):
    for k, x in sorted(pairs[name].items(), key=lambda t: -t[1])[:8]:
        i, j = map(int, k.split("-"))
        top.append({"text": name, "slots": f"{'/'.join(SLOTS[i])}  x  {'/'.join(SLOTS[j])}", "apart": j - i, "bits": x})

save(HERE, "slots", {"summary": summary, "models": models, "ends": ends, "device": dev, "pairs": pairs,
                     "by_distance": by_dist, "top": top})
md = "# 34 slots\n\n## Coverage and shared information\n\n" + table(
    summary, ["text", "parse", "words", "parsed", "distinct words parsed", "sum of slot entropies", "word entropy",
              "shared (bits)", "shared if independent"])
md += "\n## Held-out bits per word\n\n" + table(models, ["text", "independent slots", "chain", "whole word so far"])
md += "\n## Does the start know the end?\n\n" + table(
    ends, ["text", "I(prefix; suffix | core)", "suffix shuffled within core", "excess (bits)", "p"])
md += "\n## What an independent device would write\n\n" + table(
    dev, ["text", "distinct words, real", "distinct words, independent device",
          "device words that exist in the text (types)", "device words that exist (tokens)",
          "real words the device made (types)"])
md += "\n## Shared information between pairs of slots, by distance (bits, bias removed)\n\n" + table(
    by_dist, ["text", "1 apart", "2 apart", "3 apart", "4 apart", "6 apart", "8 apart", "all pairs", "pairs 4+ apart, share"])
md += "\n## Strongest pairs\n\n" + table(top, ["text", "slots", "apart", "bits"])
write_md(HERE, "slots", md)
print(md)
