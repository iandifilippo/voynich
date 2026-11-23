"""The rhythm as a two-sign boundary rule.

Exp. 62: the qo / ch-sh rhythm is almost entirely words ending in -y (above
all -dy, -ey) being followed by qo- words; ch/sh words ending in -l, -r, -n
don't prefer qo at all. The generator links a word's first sign to the last
*one* sign of the previous word, which makes the rhythm only partly (ch/sh-y
-> qo 1.59x against B's 1.96x). Here the link looks at the last two signs.

Same protocol as exps. 60-61: choose follow_p on the even sheets, score
eleven statistics on the odd sheets, plus the rhythm itself (ch/sh-y -> qo
over the base rate of qo).
"""
import importlib.util
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich.assemble import Assembler  # noqa: E402

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("scorecard", HERE.parent / "60_scorecard" / "run.py")
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)


def gen(seed, follow_p, link_signs, shapes=None):
    m = Assembler(order=2, recall_p=0.01, edit_p=0.10, window=5, sheet_sigma=0.3, hold=1.0,
                  follow_p=follow_p, link_signs=link_signs).fit(
        [w for s in sc.train for w, _ in s], [k for k, (_, p) in enumerate([x for s in sc.train for x in s]) if p])
    return [m.fill_sheet([(len(w), p) for w, p in s], seed=seed * 1000 + i)
            for i, s in enumerate(shapes or sc.test)]


def rhythm(sheets):
    n = o = q = t = 0
    for s in sheets:
        for l in s:
            for a, b in zip(l, l[1:]):
                t += 1
                q += b.startswith("q")
                if a[:2] in ("ch", "sh") and a.endswith("y"):
                    n += 1
                    o += b.startswith("q")
    return (o / n) / (q / t)


rng = random.Random(0)
train_text = [[w for w, _ in s] for s in sc.train]
t = sc.measure(train_text, rng)
grid, best, best_n = [], 0.0, -1
for fp in (0.0, 0.05, 0.1, 0.15):
    out = gen(5, fp, 2, shapes=sc.train)
    r = sc.measure(out, rng)
    n = sum(1 for k in t if t[k] and 0.8 <= r[k] / t[k] <= 1.25)
    grid.append({"follow_p": fp, "within range on training sheets": n, "rhythm": rhythm(out)})
    print(grid[-1], flush=True)
    if n > best_n:
        best, best_n = fp, n
models = {"Currier B, odd sheets": sc.test_text,
          "link on 1 sign, run copying 0.05 (exp. 61)": gen(1, 0.05, 1),
          f"link on 2 signs, run copying {best} (chosen on even sheets)": gen(1, best, 2)}
rows = []
for name, sheets in models.items():
    r = sc.measure(sheets, rng)
    rows.append({"model": name, **r, "rhythm (ch/sh-y -> qo)": rhythm(sheets)})
    print({k: (round(x, 3) if isinstance(x, float) else x) for k, x in rows[-1].items()}, flush=True)
target = rows[0]
keys = [k for k in target if k not in ("model", "rhythm (ch/sh-y -> qo)")]
for r in rows[1:]:
    r["within 0.8-1.25x of B"] = sum(1 for k in keys if target[k] and 0.8 <= r[k] / target[k] <= 1.25)
save(HERE, "link_two_signs", {"grid": grid, "rows": rows})
md = "# 63 the boundary link on two signs\n\n## Choice on the even sheets\n\n" + table(
    grid, ["follow_p", "within range on training sheets", "rhythm"])
md += "\n## Words\n\n" + table(rows, ["model", "distinct per 1000", "hapax share", "new words vs training half",
                                    "lexicon gain (bits)", "mean signs per word", "qo- words"])
md += "\n## Pages, lines and sequence\n\n" + table(rows, ["model", "sheet identity", "gallows same line / other",
                                                       "beyond the boundary (bits)", "recurring pairs excess",
                                                       "class sequence (bits)", "rhythm (ch/sh-y -> qo)",
                                                       "within 0.8-1.25x of B"])
write_md(HERE, "link_two_signs", md)
print(md)
