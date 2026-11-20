"""Is the residual the same 'grammar' in Currier A and B?

Exps. 50-51: neighbouring words share structure that no habit I can model
makes, in A and B, in two transliterations. If it comes from one underlying
system (a grammar, or a code applied to a sequence), the same transitions
should be favoured and avoided in both. If it's two separate habits, the
patterns needn't agree.

Words (3+ signs) are put in coarse classes by start (qo, o, ch/sh, d, a, y,
s, other) and by ending (y, n, l, r, m, other). For each transition
'class of word i -> class of word i+1', the ratio of observed to expected,
expected from the permutation that keeps boundary glyphs and sheet (as in
exps. 48-50). Then the correlation of log ratios between texts, over cells
with enough counts:
  A against B;
  one half of B's sheets against the other half (the ceiling: how well B
    agrees with itself);
  B against the habits generator fitted to B.
"""
import math
import pathlib
import random
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "51_residual_replication"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "50_settings_generator"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich.assemble import signs  # noqa: E402

HERE = pathlib.Path(__file__).parent
src = (HERE.parent / "51_residual_replication" / "run.py").read_text()
ns = {"__file__": str(HERE.parent / "51_residual_replication" / "run.py")}
exec(compile(src[:src.index("rng = random.Random(0)\nrows = []")], "r51", "exec"), ns)
PERMS = 40
MIN_EXP = 10


def start_cls(s):
    w = "".join(s)
    for p in ("qo", "ch", "sh", "o", "d", "a", "y", "s"):
        if w.startswith(p):
            return "ch/sh" if p in ("ch", "sh") else p
    return "other"


def end_cls(s):
    return s[-1] if s[-1] in ("y", "n", "l", "r", "m") else "other"


def word_cls(s):
    return start_cls(s) + "_" + end_cls(s)


def ratios(sheets, rng):
    pairs, sheet_of = [], []
    for k, lines in enumerate(sheets):
        for l in lines:
            seq = [signs(w) for w in l if len(signs(w)) >= 3]
            for a, b in zip(seq, seq[1:]):
                pairs.append((a, b))
                sheet_of.append(k)
    trip = [(word_cls(a), word_cls(b), (a[-1], b[0])) for a, b in pairs]
    groups = defaultdict(list)
    for k, t in enumerate(trip):
        groups[t[2], sheet_of[k]].append(k)
    obs = Counter((x, y) for x, y, _ in trip)
    exp = Counter()
    for _ in range(PERMS):
        xs = [t[0] for t in trip]
        for idx in groups.values():
            vals = [xs[k] for k in idx]
            rng.shuffle(vals)
            for k, x in zip(idx, vals):
                xs[k] = x
        exp.update((x, t[1]) for x, t in zip(xs, trip))
    return {k: (obs[k], exp[k] / PERMS) for k in set(obs) | set(exp)}


def corr(r1, r2):
    keys = [k for k in r1 if k in r2 and r1[k][1] >= MIN_EXP and r2[k][1] >= MIN_EXP and k[0] != k[1]]
    a = np.array([math.log((r1[k][0] + 0.5) / (r1[k][1] + 0.5)) for k in keys])
    b = np.array([math.log((r2[k][0] + 0.5) / (r2[k][1] + 0.5)) for k in keys])
    return float(np.corrcoef(a, b)[0, 1]), len(keys)


rng = random.Random(0)
SB = ns["load"]("ZL", "B")
SA = ns["load"]("ZL", "A")
B = [[w for w, _ in s] for s in SB]
A = [[w for w, _ in s] for s in SA]
rB, rA = ratios(B, rng), ratios(A, rng)
half1, half2 = ratios(B[0::2], rng), ratios(B[1::2], rng)
a1, a2 = ratios(A[0::2], rng), ratios(A[1::2], rng)
G = [[[w for w in l] for l in s] for s in ns["generator"](SB, 0.9, 2.5, 7)]
rG = ratios(G, rng)
IT_B = [[w for w, _ in s] for s in ns["load"]("IT", "B")]
rIT = ratios(IT_B, rng)
rows = []
for label, x, y in (("B, half of sheets vs other half (ceiling)", half1, half2),
                    ("A, half of sheets vs other half (ceiling)", a1, a2),
                    ("A vs B", rA, rB),
                    ("B (ZL) vs B (IT), same pages, other transcriber", rB, rIT),
                    ("B vs habits generator fitted to B", rB, rG)):
    c, n = corr(x, y)
    rows.append({"comparison": label, "transitions compared": n, "correlation of log ratios": c})
    print(rows[-1], flush=True)

# strongest shared transitions (A and B both far from expectation in the same direction)
shared = []
for k in rA:
    if k in rB and rA[k][1] >= MIN_EXP and rB[k][1] >= MIN_EXP and k[0] != k[1]:
        la = math.log((rA[k][0] + .5) / (rA[k][1] + .5))
        lb = math.log((rB[k][0] + .5) / (rB[k][1] + .5))
        if la * lb > 0:
            shared.append({"word i": k[0], "word i+1": k[1], "A obs/exp": f"{rA[k][0]}/{rA[k][1]:.0f}",
                           "B obs/exp": f"{rB[k][0]}/{rB[k][1]:.0f}", "A ratio": math.exp(la), "B ratio": math.exp(lb),
                           "_s": la + lb})
shared.sort(key=lambda r: r["_s"])
save(HERE, "grammar", {"rows": rows, "shared": shared})
md = "# 52 is the residual the same in A and B?\n\nCorrelation of log(observed/expected) over class transitions (expected keeps boundary glyphs and sheet).\n\n"
md += table(rows, ["comparison", "transitions compared", "correlation of log ratios"])
md += "\n## Transitions favoured or avoided in both A and B\n\n" + table(
    shared[:8] + shared[-10:], ["word i", "word i+1", "A obs/exp", "B obs/exp", "A ratio", "B ratio"])
write_md(HERE, "grammar", md)
print(md)


# Predictive check. Learn the transition ratios on one part, score the other:
# sum over test pairs of log2 R(x, y), minus the same for the test pairs after
# the boundary-and-sheet permutation (what the score would be with no
# transferable structure). Per pair, in bits. Two splits: half of the sheets
# against the other half (a grammar shared across the book), and odd lines
# against even lines inside each sheet (structure particular to the sheet).
def pairs_of(sheets, line_filter=None):
    out = []
    for k, lines in enumerate(sheets):
        for j, l in enumerate(lines):
            if line_filter is not None and j % 2 != line_filter:
                continue
            seq = [signs(w) for w in l if len(signs(w)) >= 3]
            for a, b in zip(seq, seq[1:]):
                out.append((word_cls(a), word_cls(b), (a[-1], b[0]), k))
    return out


def learn(pairs, rng, shrink=5.0):
    groups = defaultdict(list)
    for i, p in enumerate(pairs):
        groups[p[2], p[3]].append(i)
    obs = Counter((p[0], p[1]) for p in pairs)
    exp = Counter()
    for _ in range(PERMS):
        xs = [p[0] for p in pairs]
        for idx in groups.values():
            vals = [xs[i] for i in idx]
            rng.shuffle(vals)
            for i, x in zip(idx, vals):
                xs[i] = x
        exp.update((x, p[1]) for x, p in zip(xs, pairs))
    return {k: math.log2((obs[k] + shrink) / (exp[k] / PERMS + shrink)) for k in set(obs) | set(exp)}


def transfer(train, test, rng):
    R = learn(train, rng)
    score = sum(R.get((p[0], p[1]), 0.0) for p in test) / len(test)
    groups = defaultdict(list)
    for i, p in enumerate(test):
        groups[p[2], p[3]].append(i)
    base = 0.0
    for _ in range(PERMS):
        xs = [p[0] for p in test]
        for idx in groups.values():
            vals = [xs[i] for i in idx]
            rng.shuffle(vals)
            for i, x in zip(idx, vals):
                xs[i] = x
        base += sum(R.get((x, p[1]), 0.0) for x, p in zip(xs, test)) / len(test)
    return score - base / PERMS


pred = []
for name, sheets in (("Currier B", B), ("Currier A", A), ("habits generator (B)", G)):
    across = (transfer(pairs_of(sheets[0::2]), pairs_of(sheets[1::2]), rng) +
              transfer(pairs_of(sheets[1::2]), pairs_of(sheets[0::2]), rng)) / 2
    inside = (transfer(pairs_of(sheets, 0), pairs_of(sheets, 1), rng) +
              transfer(pairs_of(sheets, 1), pairs_of(sheets, 0), rng)) / 2
    # inside, but with the ratios learned per sheet
    per_sheet = []
    for k, s in enumerate(sheets):
        tr = [p for p in pairs_of([s], 0)]
        te = [p for p in pairs_of([s], 1)]
        if len(tr) > 30 and len(te) > 30:
            per_sheet.append((transfer(tr, te, rng) + transfer(te, tr, rng)) / 2 * len(te))
    n_te = sum(len(pairs_of([s], 1)) for s in sheets if len(pairs_of([s], 0)) > 30 and len(pairs_of([s], 1)) > 30)
    pred.append({"text": name, "learned on half the sheets, scored on the rest (bits/pair)": across,
                 "learned on odd lines, scored on even lines, all sheets pooled": inside,
                 "learned and scored inside each sheet separately": sum(per_sheet) / n_te})
    print(pred[-1], flush=True)
save(HERE, "grammar_transfer", pred)
md += "\n## Does the structure transfer? (bits per pair above a no-structure baseline)\n\n" + table(
    pred, ["text", "learned on half the sheets, scored on the rest (bits/pair)",
           "learned on odd lines, scored on even lines, all sheets pooled",
           "learned and scored inside each sheet separately"])
write_md(HERE, "grammar", md)
