"""Fit the recall knobs on the training half only.

The plain assembler makes too few adjacent repeats and too little page
locality (run.py). recall_p (exact repeat of a recent word), edit_p (a recent
word with one sign redrawn) and window are set by filling the training
half's own shape and matching the training half on four measures that
concern repetition: adjacent exact and near repeats, doubletons on one page,
and distinct words per 1000. The held-out half is not touched here.
"""
import itertools
import math
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import run  # noqa: E402
from _common import save, table, write_md  # noqa: E402
from voynich.assemble import Assembler  # noqa: E402

HERE = pathlib.Path(__file__).parent
KEYS = ["adjacent exact repeats per 1000", "adjacent near repeats per 1000", "doubletons on one page",
        "distinct per 1000 words"]
target = run.measure(run.train, run.vocab)
tshape = [[(len(l), ps) for l, ps in p] for p in run.train]
rows = []
for p, e, window in itertools.product([0.0, 0.005, 0.01, 0.02], [0.0, 0.03, 0.06, 0.1, 0.15], [5, 15, 50]):
    if p == e == 0 and window != 5:
        continue
    m = Assembler(order=2, recall_p=p, edit_p=e, window=window).fit(run.tr_lines, run.tr_starts)
    ms = []
    for seed in (1, 2):
        pages = [list(zip(m.fill(pg, seed=seed * 1000 + i), [ps for _, ps in pg])) for i, pg in enumerate(tshape)]
        ms.append(run.measure(pages, run.vocab))
    r = {"p": p, "edit": e, "window": window}
    for k in KEYS:
        r[k] = statistics.mean(x[k] for x in ms)
    r["misfit"] = sum(math.log(r[k] / target[k]) ** 2 for k in KEYS) ** 0.5
    rows.append(r)
    print(r, flush=True)
best = min(rows, key=lambda r: r["misfit"])
save(HERE, "tune", {"target": {k: target[k] for k in KEYS}, "rows": rows, "best": {"p": best["p"], "edit": best["edit"], "window": best["window"]}})
md = "# 36 recall knobs, fitted on the training half\n\ntraining half: " + ", ".join(
    f"{k} {target[k]:.3f}" for k in KEYS) + "\n\n" + table(sorted(rows, key=lambda r: r["misfit"])[:12],
                                                          ["p", "edit", "window"] + KEYS + ["misfit"])
write_md(HERE, "tune", md)
print(md)
