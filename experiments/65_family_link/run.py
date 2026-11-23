"""The rhythm, taken apart, and two rules a scribe could follow by hand.

Exp. 62-63 left one piece of word-to-word structure no generator makes: in
Currier B, ch/sh-...-y words are followed by qo- words twice as often as
chance, and how often depends on the family of the -y word, not only on its
last signs. Here the rhythm is first measured in more detail on all B
sheets, then two rules are added to the generator of exps. 60-61:

  family link    the start of a word is drawn given the previous word's
                 family (qo-, ch/sh-, o-, other) and its last sign, a table
                 of 4 x ~20 cells, small enough to keep on a card
  line setting   each line gets its own weights for each family of starts
                 and for each ending, exp(N(0, line_sigma)), optionally
                 drifting from the line before (line_drift)
  echo from above  the repeats and one-sign edits of recent words reach
                 back `window` words (5 = this line, 15-25 = the lines
                 above) and prefer words whose start fits the link

The parameters are chosen on B's even sheets and everything is scored on
the odd sheets (same protocol as exps. 60, 61, 63), with three rhythm
measures besides the scorecard:

  rhythm         P(qo | previous is ch/sh-...-y) over P(qo)
  lag 2          P(qo | qo two words back) over P(qo | no qo two back),
                 divided by the same with words shuffled inside lines
  line spread    variance of the qo share of lines (6+ words) over the
                 binomial variance expected from the sheet's qo share
  neighbours     correlation between adjacent lines (6+ words) of their
                 qo-, -y and -n shares, sheet mean removed, averaged
"""
import importlib.util
import pathlib
import random
import statistics
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich.assemble import Assembler, family, signs  # noqa: E402

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("scorecard", HERE.parent / "60_scorecard" / "run.py")
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)


def end(w):
    s = signs(w)[-1]
    return s if s in ("y", "l", "r", "n") else "other"


def rhythm(sheets):
    n = o = q = t = 0
    for s in sheets:
        for l in s:
            for a, b in zip(l, l[1:]):
                t += 1
                q += b.startswith("q")
                if family(a) == "c" and a.endswith("y"):
                    n += 1
                    o += b.startswith("q")
    return (o / n) / (q / t)


def lag(sheets, k=2):
    a = b = c = d = 0
    for s in sheets:
        for l in s:
            for x, y in zip(l, l[k:]):
                if family(x) == "q":
                    a += 1
                    b += family(y) == "q"
                else:
                    c += 1
                    d += family(y) == "q"
    return (b / a) / (d / c)


def lag2(sheets, rng, reps=5):
    shuffled = [lag([[rng.sample(l, len(l)) for l in s] for s in sheets]) for _ in range(reps)]
    return lag(sheets) / statistics.mean(shuffled)


def spread(sheets):
    r, e = [], []
    for s in sheets:
        ws = [w for l in s for w in l]
        p = sum(family(w) == "q" for w in ws) / len(ws)
        for l in s:
            if len(l) >= 6:
                r.append(sum(family(w) == "q" for w in l) / len(l))
                e.append(p * (1 - p) / len(l))
    return statistics.pvariance(r) / statistics.mean(e)


def feats(l):
    return (sum(family(w) == "q" for w in l) / len(l), sum(w.endswith("y") for w in l) / len(l),
            sum(w.endswith("n") for w in l) / len(l))


def neighbours(units, gap=1, rng=None):
    """units: lists of lines (sheets or pages). With rng, lines are shuffled
    inside each unit first (the baseline: removing the mean makes r < 0)."""
    rs = []
    for j in range(3):
        xs, ys = [], []
        for u in units:
            lines = [l for l in u if len(l) >= 6]
            if len(lines) < gap + 2:
                continue
            if rng:
                lines = rng.sample(lines, len(lines))
            m = statistics.mean(feats(l)[j] for l in lines)
            for a, b in zip(lines, lines[gap:]):
                xs.append(feats(a)[j] - m)
                ys.append(feats(b)[j] - m)
        rs.append(statistics.correlation(xs, ys))
    return statistics.mean(rs)


def b_pages():
    from voynich import Voynich
    pages = {}
    for l in Voynich("ZL").lines:
        if l.language == "B" and not l.unit.startswith("L"):
            ws = [w for w in l.words if "?" not in w]
            if ws:
                pages.setdefault(l.page, []).append(ws)
    return list(pages.values())


def table_of(sheets):
    """Next word's family by previous word's family and ending, over base rate."""
    pairs, base = Counter(), Counter()
    for s in sheets:
        for l in s:
            for a, b in zip(l, l[1:]):
                pairs[(family(a), end(a), family(b))] += 1
                base[family(b)] += 1
    total = sum(base.values())
    rows = []
    for f in "qcox":
        for e in ("y", "l", "r", "n", "other"):
            n = sum(pairs[(f, e, g)] for g in "qcox")
            if n >= 100:
                rows.append({"previous": f"{dict(q='qo', c='ch/sh', o='o', x='other')[f]}-...-{e}", "n": n,
                             **{f"next {g}": pairs[(f, e, g)] / n / (base[g] / total) for g in "qcox"}})
    return rows


def lags(sheets, rng):
    out = {}
    for k in (1, 2, 3, 4):
        real = lag(sheets, k)
        line = statistics.mean(lag([[rng.sample(l, len(l)) for l in s] for s in sheets], k) for _ in range(5))
        sheet = []
        for _ in range(5):
            o = []
            for s in sheets:
                ws = [w for l in s for w in l]
                rng.shuffle(ws)
                it = iter(ws)
                o.append([[next(it) for _ in l] for l in s])
            sheet.append(lag(o, k))
        out[k] = {"lag": k, "real": real, "shuffled in line": line, "shuffled in sheet": statistics.mean(sheet)}
    return list(out.values())


def averaged(make, seeds, rng, measure_rhythm=True):
    """Mean of every statistic over several generator seeds."""
    acc = []
    for sd in seeds:
        sheets = make(sd)
        r = dict(sc.measure(sheets, rng))
        if measure_rhythm:
            r.update({"rhythm": rhythm(sheets), "lag 2": lag2(sheets, rng), "line spread": spread(sheets),
                      "neighbours": neighbours(sheets)})
        acc.append(r)
    return {k: statistics.mean(a[k] for a in acc) for k in acc[0]}, sheets


def gen(seed, link_by, line_sigma=0.0, fits=False, follow_p=0.05, shapes=None, drift=0.0, window=5,
        recall_p=0.01, edit_p=0.10):
    m = Assembler(order=2, recall_p=recall_p, edit_p=edit_p, window=window, sheet_sigma=0.3, hold=1.0,
                  follow_p=follow_p, link_by=link_by, line_sigma=line_sigma, echo_fits=fits,
                  line_drift=drift).fit(
        [w for s in sc.train for w, _ in s], [k for k, (_, p) in enumerate([x for s in sc.train for x in s]) if p])
    return [m.fill_sheet([(len(w), p) for w, p in s], seed=seed * 1000 + i)
            for i, s in enumerate(shapes or sc.test)]


if __name__ == "__main__":
    rng = random.Random(0)
    all_b = [[w for w, _ in s] for s in sc.r50.SHEETS]
    anatomy = table_of(all_b)
    lag_rows = lags(all_b, rng)
    b_spread = spread(all_b)
    print(table(lag_rows, ["lag", "real", "shuffled in line", "shuffled in sheet"]), "spread", b_spread, flush=True)

    pages = b_pages()
    near = [{"lines apart": g, "sheet mean removed": neighbours(all_b, g),
             "page mean removed": neighbours(pages, g),
             "page, lines shuffled": statistics.mean(neighbours(pages, g, rng) for _ in range(5))}
            for g in (1, 2, 3, 5, 8)]
    print(table(near, ["lines apart", "sheet mean removed", "page mean removed", "page, lines shuffled"]))

    train_text = [[w for w, _ in s] for s in sc.train]
    t = sc.measure(train_text, rng)
    tr = {"rhythm": rhythm(train_text), "lag 2": lag2(train_text, rng), "line spread": spread(train_text),
          "neighbours": neighbours(train_text)}
    rkeys = list(tr)

    def score(r):
        n = sum(1 for k in t if t[k] and 0.8 <= r[k] / t[k] <= 1.25)
        n4 = sum(1 for k in rkeys if 0.8 <= r[k] / tr[k] <= 1.25 or abs(r[k] - tr[k]) < 0.02)
        return n, n4

    grid = []
    configs = [("last sign", dict(link_by="last")), ("family", dict(link_by="family"))]
    configs += [(f"family, line setting {sg} drift {d}", dict(link_by="family", line_sigma=sg, drift=d))
                for sg, d in ((0.3, 0.0), (0.4, 0.9), (0.6, 0.9))]
    configs += [(f"family, echo window {wd} edit {ep}{' fits' if f else ''}",
                 dict(link_by="family", window=wd, edit_p=ep, recall_p=ep / 10, fits=f))
                for wd, ep, f in ((15, 0.10, False), (15, 0.20, False), (15, 0.20, True), (25, 0.20, True),
                                  (25, 0.30, True))]
    for name, kw in configs:
        r, _ = averaged(lambda sd: gen(sd, shapes=sc.train, **kw), (5, 6, 7), rng)
        n, n4 = score(r)
        grid.append({"model": name, "kw": kw, "within (of 11)": n, "rhythm measures within (of 4)": n4,
                     **{k: r[k] for k in rkeys}})
        print({k: (round(x, 3) if isinstance(x, float) else x) for k, x in grid[-1].items() if k != "kw"},
              flush=True)
    best = max(grid[1:], key=lambda g: (g["within (of 11)"] + g["rhythm measures within (of 4)"],
                                        g["model"] == "family"))
    chosen = f"chosen on even sheets: {best['model']}"
    makers = {"exp. 61 (last sign)": dict(link_by="last"), "family link": dict(link_by="family"),
              "family link, echo from above (window 25, edit 0.2, fits)":
                  dict(link_by="family", window=25, edit_p=0.2, recall_p=0.02, fits=True)}
    if best["kw"] not in makers.values():
        makers[chosen] = best["kw"]
    models = {}
    b = dict(sc.measure(sc.test_text, rng))
    b.update({"rhythm": rhythm(sc.test_text), "lag 2": lag2(sc.test_text, rng), "line spread": spread(sc.test_text),
              "neighbours": neighbours(sc.test_text)})
    rows = [{"model": "Currier B, odd sheets", **b}]
    for name, kw in makers.items():
        r, models[name] = averaged(lambda sd: gen(sd, **kw), range(1, 6), rng)
        rows.append({"model": name + (" (chosen)" if kw == best["kw"] else ""), **r})
        print({k: (round(x, 3) if isinstance(x, float) else x) for k, x in rows[-1].items()}, flush=True)
    target = rows[0]
    base = [k for k in target if k not in ["model"] + rkeys]
    for r in rows[1:]:
        r["within (of 11)"] = sum(1 for k in base if target[k] and 0.8 <= r[k] / target[k] <= 1.25)
        r["rhythm within (of 4)"] = sum(1 for k in rkeys if 0.8 <= r[k] / target[k] <= 1.25
                                        or abs(r[k] - target[k]) < 0.02)
    gen_anatomy = table_of(models["family link"])
    for g in grid:
        g.pop("kw")
    save(HERE, "family_link", {"anatomy": anatomy, "lags": lag_rows, "spread": b_spread, "near": near,
                               "train_target": tr, "grid": grid, "rows": rows, "generator_anatomy": gen_anatomy})
    f = {f"next {g}": ".2f" for g in "qcox"}
    md = "# 65 family link\n\n## The rhythm in all B sheets (next family over base rate)\n\n"
    md += table(anatomy, ["previous", "n", "next q", "next c", "next o", "next x"], f)
    md += "\n## qo k words back, against shuffles\n\n" + table(lag_rows, ["lag", "real", "shuffled in line",
                                                                         "shuffled in sheet"])
    md += f"\nLine spread of qo share (variance over binomial): {b_spread:.2f}\n"
    md += "\n## Neighbouring lines (qo-, -y, -n shares)\n\n" + table(
        near, ["lines apart", "sheet mean removed", "page mean removed", "page, lines shuffled"])
    md += "\n## Choice on the even sheets (mean of 3 seeds)\n\n" + table(
        [{"model": "B even sheets", **tr}] + grid,
        ["model", "within (of 11)", "rhythm measures within (of 4)"] + rkeys)
    md += "\n## Odd sheets (mean of 5 seeds): words\n\n" + table(rows, [
        "model", "distinct per 1000", "hapax share", "new words vs training half", "lexicon gain (bits)",
        "mean signs per word", "qo- words"])
    md += "\n## Odd sheets: pages, lines, sequence\n\n" + table(rows, [
        "model", "sheet identity", "gallows same line / other", "beyond the boundary (bits)",
        "recurring pairs excess", "class sequence (bits)", "within (of 11)"])
    md += "\n## Odd sheets: the rhythm\n\n" + table(rows, ["model"] + rkeys + ["rhythm within (of 4)"])
    md += "\n## The family table from the family-link generator\n\n" + table(
        gen_anatomy, ["previous", "n", "next q", "next c", "next o", "next x"], f)
    write_md(HERE, "family_link", md)
    print(md)
