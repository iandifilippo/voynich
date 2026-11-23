"""Words built fresh, runs copied: does that close the gap?

Exp. 60: no single model passes the scorecard. The assembled-words generator
gets the vocabulary right and the links between neighbours wrong (beyond the
boundary 0.04-0.07 bits against B's 0.23); the copying model of Timm and
Schinner gets the links (0.21) and the vocabulary wrong (half its words are
new, no q-). That suggests a hybrid: words are built by the rule, but now
and then the writer, having just written a word that already stands on the
page, writes again what followed it there (a short run copied, sometimes
with a sign changed).

follow_p is chosen on the even sheets (against the even sheets' own text),
then everything is scored on the odd sheets, as in exp. 60.

Correction found while writing this: in exps. 50-60 the generator's echo
(recall of recent words) was reset at every line, because fill_sheet called
fill line by line; it now keeps the sheet's history. The scorecard below uses
the corrected generator throughout.
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


def hybrid(seed, follow_p, sigma=0.3, hold=1.0, shapes=None):
    m = Assembler(order=2, recall_p=0.01, edit_p=0.10, window=5, sheet_sigma=sigma, hold=hold,
                  follow_p=follow_p).fit(
        [w for s in sc.train for w, _ in s], [k for k, (_, p) in enumerate([x for s in sc.train for x in s]) if p])
    return [m.fill_sheet([(len(w), p) for w, p in s], seed=seed * 1000 + i)
            for i, s in enumerate(shapes or sc.test)]


rng = random.Random(0)
train_text = [[w for w, _ in s] for s in sc.train]
t = sc.measure(train_text, rng)
grid, best, best_n = [], 0.0, -1
for fp in (0.0, 0.05, 0.1, 0.2, 0.3, 0.45):
    r = sc.measure(hybrid(5, fp, shapes=sc.train), rng)
    n = sum(1 for k in t if t[k] and 0.8 <= r[k] / t[k] <= 1.25)
    grid.append({"follow_p": fp, "within range on training sheets": n,
                 "beyond the boundary": r["beyond the boundary (bits)"],
                 "recurring pairs excess": r["recurring pairs excess"], "distinct per 1000": r["distinct per 1000"]})
    print(grid[-1], flush=True)
    if n > best_n:
        best, best_n = fp, n
models = {"Currier B, odd sheets": sc.test_text,
          "assembled words, no run copying": hybrid(1, 0.0),
          f"assembled words + run copying (follow_p {best}, chosen on even sheets)": hybrid(1, best),
          "copying model (exp. 22)": sc.copying(1)}
rows = []
for name, sheets in models.items():
    r = sc.measure(sheets, rng)
    rows.append({"model": name, **r})
    print({k: (round(x, 3) if isinstance(x, float) else x) for k, x in rows[-1].items()}, flush=True)
target = rows[0]
keys = [k for k in target if k != "model"]
for r in rows[1:]:
    r["within 0.8-1.25x of B"] = sum(1 for k in keys if target[k] and 0.8 <= r[k] / target[k] <= 1.25)
save(HERE, "run_copying", {"grid": grid, "rows": rows})
md = "# 61 assembled words with copied runs, scored on B's odd sheets\n\n## Choice of follow_p on the even sheets\n\n" + table(
    grid, ["follow_p", "within range on training sheets", "beyond the boundary", "recurring pairs excess", "distinct per 1000"])
md += "\n## Words\n\n" + table(rows, ["model", "distinct per 1000", "hapax share", "new words vs training half",
                                    "lexicon gain (bits)", "mean signs per word", "qo- words"])
md += "\n## Pages, lines and sequence\n\n" + table(rows, ["model", "sheet identity", "gallows same line / other",
                                                       "beyond the boundary (bits)", "recurring pairs excess",
                                                       "class sequence (bits)", "within 0.8-1.25x of B"])
write_md(HERE, "run_copying", md)
print(md)
