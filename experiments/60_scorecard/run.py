"""The scorecard: one generator against everything measured since exp. 34.

The account the series has arrived at, as a single generator: words drawn
from a two-sign chain with position tables (exp. 36), a setting per sheet and
a favoured gallows per line (exp. 50), an echo of recent words (exp. 36).
Fitted on Currier B's even sheets only, it fills the odd sheets' shapes.
Every statistic below is measured on the odd sheets of the manuscript and on
the generator's output for the same sheets, plus two older models for
comparison (the copying model of exp. 22 and the Naibbe cipher of Pliny).
"""
import json
import math
import pathlib
import random
import re
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import importlib.util  # noqa: E402

from _common import save, table, write_md  # noqa: E402
from voynich.assemble import Assembler, signs  # noqa: E402
from voynich.autocopy import AutoCopy  # noqa: E402
from voynich.corpus import DATA  # noqa: E402
from voynich.crack.classes import class_mi, fit  # noqa: E402

HERE = pathlib.Path(__file__).parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r50 = _load("settings_generator", HERE.parent / "50_settings_generator" / "run.py")
spaces = _load("spaces", HERE.parent / "55_spaces_from_boxes" / "run.py")

train = r50.SHEETS[0::2]
test = r50.SHEETS[1::2]
test_text = [[w for w, _ in s] for s in test]
train_vocab = Counter(w for s in train for ws, _ in s for w in ws)


def final_generator(seed, sigma=0.9, hold=2.5, shapes=None):
    m = Assembler(order=2, recall_p=0.01, edit_p=0.10, window=5, sheet_sigma=sigma, hold=hold).fit(
        [w for s in train for w, _ in s], [k for k, (_, p) in enumerate([x for s in train for x in s]) if p])
    return [m.fill_sheet([(len(w), p) for w, p in s], seed=seed * 1000 + i) for i, s in enumerate(shapes or test)]


def copying(seed):
    chart = {k: set(x) for k, x in json.loads(
        (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}
    g = AutoCopy(seed=seed, currier="B", boundary=chart, boundary_p=0.65, line_end_p=0.5, common_p=0.5)
    lines = [l for l in g.run(sum(len(s) for s in test)) if l]
    out, k = [], 0
    for s in test:
        out.append(lines[k:k + len(s)])
        k += len(s)
    return out


def naibbe():
    ws = open(DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt",
              encoding="utf-8-sig").read().split()
    out, k = [], 0
    for s in test:
        out.append([])
        for l, _ in s:
            out[-1].append(ws[k:k + len(l)])
            k += len(l)
    return out


def recurring_excess(sheets, rng):
    def pairs(ss):
        return [(a, b) for s in ss for l in s for a, b in zip(l, l[1:])]

    a, b = sheets[0::2], sheets[1::2]
    tr = set(pairs(a))
    obs = sum(p in tr for p in pairs(b)) / max(1, len(pairs(b)))
    base = 0
    for _ in range(10):
        flat = [w for s in b for l in s for w in l]
        rng.shuffle(flat)
        it = iter(flat)
        sb = [[[next(it) for _ in l] for l in s] for s in b]
        base += sum(p in tr for p in pairs(sb)) / max(1, len(pairs(sb)))
    return obs - base / 10


def class_seq(sheets):
    tr, te = sheets[0::2], sheets[1::2]
    trl = [l for s in tr for l in s]
    tel = [l for s in te for l in s]
    f = Counter(w for l in trl for w in l)
    keep = {w for w, c in f.items() if c >= 5}
    m = lambda ls: [[w if w in keep else "<r>" for w in l] for l in ls]  # noqa: E731
    _, assign = fit(m(trl), 16)
    flat = [w for l in m(trl) for w in l]
    random.Random(0).shuffle(flat)
    it = iter(flat)
    _, a0 = fit([[next(it) for _ in l] for l in m(trl)], 16)
    return class_mi(m(tel), assign, unknown=16) - class_mi(m(tel), a0, unknown=16)


def measure(sheets, rng):
    words = [w for s in sheets for l in s for w in l]
    c = Counter(words)
    long = [[[w for w in l if len(signs(w)) >= 3] for l in s] for s in sheets]
    return {
        "distinct per 1000": 1000 * len(c) / len(words),
        "hapax share": sum(1 for x in c.values() if x == 1) / len(c),
        "new words vs training half": sum(1 for w in words if w not in train_vocab) / len(words),
        "lexicon gain (bits)": spaces.lexicon_gain(words, random.Random(0)),
        "mean signs per word": statistics.mean(len(signs(w)) for w in words),
        "qo- words": sum(w.startswith("qo") for w in words) / len(words),
        "sheet identity": r50.identity(sheets),
        "gallows same line / other": r50.gallows_line_ratio(sheets),
        "beyond the boundary (bits)": r50.beyond_boundary(long, rng, perms=10),
        "recurring pairs excess": recurring_excess(sheets, rng),
        "class sequence (bits)": class_seq(sheets),
    }


if __name__ == "__main__":
    rng = random.Random(0)

    # choose sigma and hold on the training sheets only: the generator fills the
    # training sheets' shapes and is scored against the training text itself
    train_text = [[w for w, _ in s] for s in train]
    t_target = measure(train_text, rng)
    best, best_n = (0.9, 2.5), -1
    grid = []
    for sigma in (0.0, 0.3, 0.6, 0.9):
        for hold in (1.0, 2.5):
            r = measure(final_generator(5, sigma, hold, shapes=train), rng)
            n = sum(1 for k in t_target if t_target[k] and 0.8 <= r[k] / t_target[k] <= 1.25)
            grid.append({"sigma": sigma, "hold": hold, "within range on training sheets": n})
            print(grid[-1], flush=True)
            if n > best_n:
                best, best_n = (sigma, hold), n

    models = {"Currier B, odd sheets": test_text,
              f"final generator (sigma {best[0]}, hold {best[1]}, chosen on even sheets)": final_generator(1, *best),
              "final generator (sigma 0.9, hold 2.5, exp. 50)": final_generator(1),
              "copying model": copying(1), "Naibbe cipher of Pliny": naibbe()}
    rows = []
    for name, sheets in models.items():
        r = measure(sheets, rng)
        rows.append({"model": name, **r})
        print({k: (round(x, 3) if isinstance(x, float) else x) for k, x in rows[-1].items()}, flush=True)
    target = rows[0]
    keys = [k for k in target if k != "model"]
    for r in rows[1:]:
        r["within 0.8-1.25x of B"] = sum(1 for k in keys if target[k] and 0.8 <= r[k] / target[k] <= 1.25)
    save(HERE, "scorecard", {"rows": rows, "grid": grid})
    cols1 = ["model", "distinct per 1000", "hapax share", "new words vs training half", "lexicon gain (bits)",
             "mean signs per word", "qo- words"]
    cols2 = ["model", "sheet identity", "gallows same line / other", "beyond the boundary (bits)",
             "recurring pairs excess", "class sequence (bits)", "within 0.8-1.25x of B"]
    md = "# 60 scorecard (fitted on B's even sheets, measured on its odd sheets)\n\n## Words\n\n" + table(rows, cols1)
    md += "\n## Pages, lines and sequence\n\n" + table(rows, cols2)
    md += "\n## Choice of settings on the training sheets\n\n" + table(grid, ["sigma", "hold", "within range on training sheets"])
    write_md(HERE, "scorecard", md)
    print(md)
