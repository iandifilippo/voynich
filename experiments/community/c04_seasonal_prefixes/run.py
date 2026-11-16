"""voynich.ninja thread 5817 (June 2026), "Seasonal prefix clustering in Voynich
zodiac nymph labels": label prefixes shift with the season (ot- in spring,
ok- later). Replies agreed it is visible and asked why.

Check: is the shift bigger than you'd get by dealing the same labels out to the
signs at random? Statistic: chi-square of prefix x sign, and the Spearman
correlation between month order and ot- share. Also: is it the labels, or do
the scribes/pages differ? Compare with the ring text on the same pages.
"""
import math
import pathlib
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import _path  # noqa: F401
from _common import save, table, write_md
from voynich import Voynich

HERE = pathlib.Path(__file__).parent
SIGNS = [(["f70v2"], "Pisces", 3), (["f70v1", "f71r"], "Aries", 4), (["f71v", "f72r1"], "Taurus", 5),
         (["f72r2"], "Gemini", 6), (["f72r3"], "Cancer", 7), (["f72v3"], "Leo", 8), (["f72v2"], "Virgo", 9),
         (["f72v1"], "Libra", 10), (["f73r"], "Scorpio", 11), (["f73v"], "Sagittarius", 12)]
v = Voynich("ZL")


def collect(units):
    out = []
    for pages, sign, m in SIGNS:
        for l in v.select(section=["Z"], pages=pages, unit=units):
            for w in l.words:
                out.append((sign, m, w))
    return out


def prefix(w):
    for p in ("ot", "ok", "oe", "ch", "sh", "y", "d"):
        if w.startswith(p):
            return p
    return "other"


def chi2(items):
    tab = defaultdict(Counter)
    for s, _, w in items:
        tab[s][prefix(w)] += 1
    rows = list(tab)
    cols = sorted({c for r in tab.values() for c in r})
    n = len(items)
    rt = {r: sum(tab[r].values()) for r in rows}
    ct = {c: sum(tab[r][c] for r in rows) for c in cols}
    return sum((tab[r][c] - rt[r] * ct[c] / n) ** 2 / (rt[r] * ct[c] / n) for r in rows for c in cols if ct[c])


def spearman(xs, ys):
    def rank(a):
        o = sorted(range(len(a)), key=lambda i: a[i])
        r = [0] * len(a)
        for k, i in enumerate(o):
            r[i] = k
        return r
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    return 1 - 6 * sum((a - b) ** 2 for a, b in zip(rx, ry)) / (n * (n * n - 1))


def ot_by_month(items):
    c = defaultdict(lambda: [0, 0])
    for _, m, w in items:
        c[m][0] += w.startswith("ot")
        c[m][1] += 1
    ms = sorted(c)
    return ms, [c[m][0] / c[m][1] for m in ms]


rng = random.Random(0)
res = {}
for label, units in (("labels", "L"), ("ring text", "CR")):
    items = collect(units)
    x2 = chi2(items)
    ms, share = ot_by_month(items)
    rho = spearman(ms, share)
    words = [w for _, _, w in items]
    null_x2, null_rho = [], []
    for _ in range(2000):
        rng.shuffle(words)
        sh = [(s, m, w) for (s, m, _), w in zip(items, words)]
        null_x2.append(chi2(sh))
        null_rho.append(spearman(*ot_by_month(sh)))
    res[label] = {"n": len(items), "chi2": x2, "p_chi2": sum(x >= x2 for x in null_x2) / 2000,
                  "spearman_month_ot": rho, "p_rho_two_sided": sum(abs(x) >= abs(rho) for x in null_rho) / 2000,
                  "ot_share_by_month": dict(zip(ms, share))}

save(HERE, "seasonal_prefixes", res)
md = "# c04 seasonal prefixes in zodiac text\n\n"
rows = [{"text": k, **{kk: vv for kk, vv in r.items() if kk != "ot_share_by_month"}} for k, r in res.items()]
md += table(rows, ["text", "n", "chi2", "p_chi2", "spearman_month_ot", "p_rho_two_sided"])
md += "\n## ot- share by month (3 = March ... 12 = December)\n\n"
md += table([{"month": m, "labels": res["labels"]["ot_share_by_month"].get(m), "ring text": res["ring text"]["ot_share_by_month"].get(m)}
             for m in range(3, 13)], ["month", "labels", "ring text"])
write_md(HERE, "seasonal_prefixes", md)
print(md)
