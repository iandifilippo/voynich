"""The rhythm: what follows a ch-/sh- word, and why?

Exps. 53 and 61 left one regularity unmade by any generator: across all of
Currier B, a ch-/sh- word ending in -y is followed by a qo- word, and 'ol' by
a ch-/sh- word, more than chance. Before modelling it, describe it.

Words fall into start families: qo- (and q-), ch-/sh-, o-, d-, a-, y-, s-,
other. For each pair of families, observed adjacent pairs inside lines over
expected, expected from shuffling words inside each sheet among words at the
same line position (exps. 48-53). Then the alternation index: how much more
often consecutive words switch between the two big families (qo and ch/sh)
than stay in one, relative to the shuffle. Measured
  for Currier A and B;
  by section of B (herbal, bathing, stars, text-only);
  by position in the line (pairs starting at word 2, 3, ... );
  at physically wide spaces only (exp. 55 boxes), so false spaces can't make it.
"""
import math
import pathlib
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402

HERE = pathlib.Path(__file__).parent
SHUF = 30
FAM = ("qo", "ch/sh", "o", "d", "a", "y", "s", "other")


def fam(w):
    if w.startswith("q"):
        return "qo"
    if w[:2] in ("ch", "sh"):
        return "ch/sh"
    return w[0] if w[0] in "odays" else "other"


def pos(i, n):
    return 0 if i == 0 else 2 if i == n - 1 else 1


def shuffle(sheets, rng):
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


def pair_counts(sheets, start_at=None):
    c = Counter()
    for s in sheets:
        for l in s:
            for i, (a, b) in enumerate(zip(l, l[1:])):
                if start_at is None or i == start_at:
                    c[fam(a), fam(b)] += 1
    return c


def ratios(sheets, rng, start_at=None):
    obs = pair_counts(sheets, start_at)
    exp = Counter()
    for _ in range(SHUF):
        exp.update(pair_counts(shuffle(sheets, rng), start_at))
    return {k: (obs[k], exp[k] / SHUF) for k in set(obs) | set(exp)}


def alternation(r):
    sw = r.get(("qo", "ch/sh"), (0, 0))[0] + r.get(("ch/sh", "qo"), (0, 0))[0]
    st = r.get(("qo", "qo"), (0, 0))[0] + r.get(("ch/sh", "ch/sh"), (0, 0))[0]
    esw = r.get(("qo", "ch/sh"), (0, 0))[1] + r.get(("ch/sh", "qo"), (0, 0))[1]
    est = r.get(("qo", "qo"), (0, 0))[1] + r.get(("ch/sh", "ch/sh"), (0, 0))[1]
    return (sw / max(st, 1)) / (esw / max(est, 1e-9))


v = Voynich("ZL")


def sheets_where(cond):
    by = defaultdict(list)
    for l in v.lines:
        if l.unit == "P" and cond(l) and re.fullmatch(r"f\d+[rv]\d*", l.page):
            ws = [w for w in l.words if "?" not in w and "'" not in w]
            if ws:
                m = v.pages.get(l.page) or {}
                by[(m.get("Q"), m.get("B"))].append(ws)
    return list(by.values())


rng = random.Random(0)
groups = {"Currier B": lambda l: l.meta.get("L") == "B", "Currier A": lambda l: l.meta.get("L") == "A",
          "B herbal": lambda l: l.meta.get("L") == "B" and l.meta.get("I") == "H",
          "B bathing": lambda l: l.meta.get("L") == "B" and l.meta.get("I") == "B",
          "B stars": lambda l: l.meta.get("L") == "B" and l.meta.get("I") == "S",
          "B text only": lambda l: l.meta.get("L") == "B" and l.meta.get("I") == "T"}
summary, cells = [], {}
for name, cond in groups.items():
    S = sheets_where(cond)
    r = ratios(S, rng)
    cells[name] = r
    get = lambda a, b: r.get((a, b), (0, 1))  # noqa: E731
    summary.append({"text": name, "pairs": sum(o for o, _ in r.values()),
                    "qo -> ch/sh": get("qo", "ch/sh")[0] / max(get("qo", "ch/sh")[1], 1e-9),
                    "ch/sh -> qo": get("ch/sh", "qo")[0] / max(get("ch/sh", "qo")[1], 1e-9),
                    "qo -> qo": get("qo", "qo")[0] / max(get("qo", "qo")[1], 1e-9),
                    "ch/sh -> ch/sh": get("ch/sh", "ch/sh")[0] / max(get("ch/sh", "ch/sh")[1], 1e-9),
                    "alternation index": alternation(r)})
    print(summary[-1], flush=True)

posrows = []
S = sheets_where(groups["Currier B"])
for k in range(0, 7):
    r = ratios(S, rng, start_at=k)
    posrows.append({"pair starts at word": k + 1, "pairs": sum(o for o, _ in r.values()), "alternation index": alternation(r)})

# wide spaces only, from the boxes of exp. 55
import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location("spaces", HERE.parent / "55_spaces_from_boxes" / "run.py")
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)
box = sp.load_lines()
gaprows = []
for L in ("B", "A"):
    lines = [l for f, ls in box.items() if (v.pages.get(f) or {}).get("L") == L for l in ls]
    gs = sorted(g for l in lines for _, g in l if g is not None)
    t2 = gs[2 * len(gs) // 3]
    for label, keep in (("all spaces", lambda g: True), ("widest third of spaces", lambda g: g > t2)):
        obs, exp = Counter(), Counter()
        pairs = [(a, l[i + 1][0]) for l in lines for i, (a, g) in enumerate(l) if g is not None and keep(g)]
        for a, b in pairs:
            obs[fam(a), fam(b)] += 1
        rights = [b for _, b in pairs]
        for _ in range(SHUF):
            rng.shuffle(rights)
            for (a, _), b in zip(pairs, rights):
                exp[fam(a), fam(b)] += 1
        r = {k: (obs[k], exp[k] / SHUF) for k in set(obs) | set(exp)}
        gaprows.append({"Currier": L, "spaces": label, "pairs": len(pairs), "alternation index": alternation(r),
                        "ch/sh -> qo": r[("ch/sh", "qo")][0] / r[("ch/sh", "qo")][1]})

save(HERE, "rhythm", {"summary": summary, "positions": posrows, "gaps": gaprows,
                      "cells_B": {f"{a} -> {b}": [o, e] for (a, b), (o, e) in cells["Currier B"].items()}})
md = "# 62 the rhythm\n\nObserved / expected (words shuffled inside sheets by line position).\n\n" + table(
    summary, ["text", "pairs", "qo -> ch/sh", "ch/sh -> qo", "qo -> qo", "ch/sh -> ch/sh", "alternation index"])
md += "\n## Along the line (Currier B)\n\n" + table(posrows, ["pair starts at word", "pairs", "alternation index"])
md += "\n## At physically wide spaces (word boxes, exp. 55; expected by shuffling right-hand words)\n\n" + table(
    gaprows, ["Currier", "spaces", "pairs", "alternation index", "ch/sh -> qo"])
full = cells["Currier B"]
crow = []
for a in FAM:
    row = {"word i \\ word i+1": a}
    for b in FAM:
        o, e = full.get((a, b), (0, 0))
        row[b] = f"{o / e:.2f}" if e >= 10 else "-"
    crow.append(row)
md += "\n## Currier B, all families (observed / expected; - where expected < 10)\n\n" + table(crow, ["word i \\ word i+1", *FAM])
write_md(HERE, "rhythm", md)
print(md)


# does the switch from ch/sh to qo depend on how the ch/sh word ends?
S = sheets_where(groups["Currier B"])
end_rows = []
for ending in ("y", "l", "r", "n", "other"):
    def keep_end(w, e=ending):
        last = w[-1]
        return last == e if e != "other" else last not in "ylrn"
    obs = exp = 0
    n = 0
    for s in S:
        for l in s:
            for a, b in zip(l, l[1:]):
                if fam(a) == "ch/sh" and keep_end(a):
                    n += 1
                    obs += fam(b) == "qo"
    base = []
    for _ in range(SHUF):
        for s in shuffle(S, rng):
            for l in s:
                for a, b in zip(l, l[1:]):
                    if fam(a) == "ch/sh" and keep_end(a):
                        base.append(fam(b) == "qo")
    exp = sum(base) / len(base)
    end_rows.append({"ch/sh word ends in": ending, "pairs": n, "next is qo": obs / max(n, 1), "if shuffled": exp,
                     "ratio": (obs / max(n, 1)) / exp if exp else float("nan")})
save(HERE, "rhythm_endings", end_rows)
md += "\n## ch/sh -> qo by how the ch/sh word ends (Currier B)\n\n" + table(
    end_rows, ["ch/sh word ends in", "pairs", "next is qo", "if shuffled", "ratio"])
write_md(HERE, "rhythm", md)
print(table(end_rows, ["ch/sh word ends in", "pairs", "next is qo", "if shuffled", "ratio"]))
