"""Recurring word pairs: does the text have phrases?

Exp. 52: the residual link between neighbouring words doesn't transfer at the
level of coarse word classes, neither across sheets nor inside a sheet. Yet
in-sample it is far above the habits generator. One thing that does both: a
few exact word pairs that recur (phrases, set expressions, or a writer
repeating a two-word pattern), invisible to classes but counted by in-sample
dependency measures.

Measure: for adjacent word pairs inside a line, the share of pairs in the
second half (odd sheets / second half of the text) that already occurred,
as the same two words in the same order, in the first half; minus the same
share after words are shuffled among words at the same line position inside
each sheet (keeps every word's frequency, the sheet setting and line-edge
habits; destroys pairs). Also the reverse order (w2 w1) as a check:
phrases have an order.
"""
import json
import pathlib
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "51_residual_replication"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "50_settings_generator"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich.corpus import DATA, historical  # noqa: E402

HERE = pathlib.Path(__file__).parent
src = (HERE.parent / "51_residual_replication" / "run.py").read_text()
ns = {"__file__": str(HERE.parent / "51_residual_replication" / "run.py")}
exec(compile(src[:src.index("rng = random.Random(0)\nrows = []")], "r51", "exec"), ns)
SHUF = 20


def pos(i, n):
    return 0 if i == 0 else 2 if i == n - 1 else 1


def shuffle_sheets(sheets, rng):
    out = []
    for lines in sheets:
        groups = defaultdict(list)
        for li, l in enumerate(lines):
            for i in range(len(l)):
                groups[pos(i, len(l))].append((li, i))
        new = [list(l) for l in lines]
        for where in groups.values():
            ws = [lines[a][b] for a, b in where]
            rng.shuffle(ws)
            for (a, b), w in zip(where, ws):
                new[a][b] = w
        out.append(new)
    return out


def pairs(sheets):
    return [(a, b) for s in sheets for l in s for a, b in zip(l, l[1:])]


def seen_rate(train, test):
    tr = set(pairs(train))
    te = pairs(test)
    fwd = sum(p in tr for p in te) / len(te)
    rev = sum((b, a) in tr for a, b in te if a != b) / len(te)
    return fwd, rev


def measure(sheets, rng):
    a, b = sheets[0::2], sheets[1::2]
    f, r = seen_rate(a, b)
    f2, r2 = seen_rate(b, a)
    f, r = (f + f2) / 2, (r + r2) / 2
    bf = br = 0
    for _ in range(SHUF):
        sa, sb = shuffle_sheets(a, rng), shuffle_sheets(b, rng)
        x, y = seen_rate(sa, sb)
        bf += x
        br += y
    return f, bf / SHUF, r, br / SHUF


def plain(ws):
    out = []
    for w in ws:
        w = unicodedata.normalize("NFD", w.lower())
        w = re.sub(r"[^a-z]", "", "".join(c for c in w if not unicodedata.combining(c)))
        if w:
            out.append(w)
    return out


def as_sheets(words, per_line=9, lines_per_sheet=40):
    lines = [words[i:i + per_line] for i in range(0, len(words), per_line)]
    return [lines[i:i + lines_per_sheet] for i in range(0, len(lines), lines_per_sheet)]


rng = random.Random(0)
SB, SA = ns["load"]("ZL", "B"), ns["load"]("ZL", "A")
B = [[w for w, _ in s] for s in SB]
A = [[w for w, _ in s] for s in SA]
G = ns["generator"](SB, 0.9, 2.5, 7)
nb = open(DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt",
          encoding="utf-8-sig").read().split()[:23000]
texts = {"Currier B": B, "Currier A": A, "habits generator (B)": G,
         "Naibbe cipher of Latin": as_sheets(nb),
         "Latin words": as_sheets(plain(historical("Secreta_Secretorum_LAT"))[:23000]),
         "Italian words": as_sheets(plain(historical("Rettorica"))[:23000])}
rows = []
for name, sheets in texts.items():
    f, bf, r, br = measure(sheets, rng)
    rows.append({"text": name, "pairs seen before": f, "if words were shuffled": bf, "excess": f - bf,
                 "excess / shuffled": (f - bf) / bf if bf else float("nan"),
                 "reversed pair seen before: excess": r - br})
    print({k: (round(x, 4) if isinstance(x, float) else x) for k, x in rows[-1].items()}, flush=True)
save(HERE, "recurring_pairs", rows)
md = "# 53 recurring word pairs\n\nShare of adjacent word pairs in one half that occurred (same order) in the other half.\n\n" + table(
    rows, ["text", "pairs seen before", "if words were shuffled", "excess", "excess / shuffled",
           "reversed pair seen before: excess"])
write_md(HERE, "recurring_pairs", md)
print(md)


# which pairs recur in Currier B more than shuffling predicts
obs = Counter(pairs(B))
exp = Counter()
for _ in range(SHUF):
    exp.update(pairs(shuffle_sheets(B, rng)))


def edit1(a, b):
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))


top = []
for p, o in obs.items():
    e = exp[p] / SHUF
    if o >= 6:
        top.append({"pair": " ".join(p), "observed": o, "expected": round(e, 1), "ratio": o / max(e, 0.5),
                    "kind": "same word" if p[0] == p[1] else "one glyph apart" if edit1(*p) else "different"})
top.sort(key=lambda r: -(r["observed"] - r["expected"]))
kinds = Counter()
excess_total = 0
for p, o in obs.items():
    e = exp[p] / SHUF
    if o > e:
        k = "same word" if p[0] == p[1] else "one glyph apart" if edit1(*p) else "different"
        kinds[k] += o - e
        excess_total += o - e
save(HERE, "recurring_pairs_B", {"top": top[:40], "excess by kind": {k: v / excess_total for k, v in kinds.items()}})
md += "\n## Currier B: pairs most over-represented\n\n" + table(top[:20], ["pair", "observed", "expected", "ratio", "kind"])
md += "\nShare of the excess (pairs above expectation) by kind: " + ", ".join(
    f"{k} {v / excess_total:.2f}" for k, v in kinds.most_common()) + "\n"
write_md(HERE, "recurring_pairs", md)
print(md[md.index("## Currier B"):])
