"""Do similar words sit under each other?

Timm & Schinner's central claim is positional: a word is copied from the lines
just above, usually from about the same horizontal position. Lines sharing
vocabulary (exp. 15, 22) doesn't show that; position does. Their evidence is
worked examples. This is the test with a null.

For every pair of lines k apart on the same page (paragraph text), every word
in the lower line is matched with the words in the upper line that are the same
or one edit away. Statistic: how far apart horizontally the two are, in glyphs
from the left margin (word centres, one glyph per space). Null: the words of
the upper line in random order, which keeps what the line contains and forgets
where. 300 shuffles.

Line-first and line-last words are left out of the main test: they resemble
each other for their own reasons (exp. 10, 20) and would fake an alignment at
both margins.
"""
import json
import pathlib
import random
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, historical, chunk_lines
from voynich.autocopy import AutoCopy
from voynich.corpus import DATA

HERE = pathlib.Path(__file__).parent
REPS = 300
LAGS = [1, 2, 3, 5, 8]
chart = {k: set(v) for k, v in json.loads(
    (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}


def edit1(a, b):
    if abs(len(a) - len(b)) > 1:
        return False
    if a == b:
        return True
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))


def centres(words):
    out, x = [], 0
    for w in words:
        out.append(x + len(w) / 2)
        x += len(w) + 1
    return out


def pairs_at(pages, lag):
    """(upper, lower) word lists, same page, `lag` lines apart"""
    out = []
    for lines in pages:
        for i in range(lag, len(lines)):
            if len(lines[i]) >= 5 and len(lines[i - lag]) >= 5:
                out.append((lines[i - lag], lines[i]))
    return out


def matches(up, low, interior):
    """for each match: index in upper, centre in lower, same word?"""
    cl = centres(low)
    rng_low = range(1, len(low) - 1) if interior else range(len(low))
    rng_up = range(1, len(up) - 1) if interior else range(len(up))
    return [(i, cl[j], up[i] == low[j]) for j in rng_low for i in rng_up
            if len(low[j]) >= 3 and edit1(up[i], low[j])]


def test(pairs, interior=True, seed=0):
    rng = random.Random(seed)
    prepared = []
    for up, low in pairs:
        m = matches(up, low, interior)
        if m:
            prepared.append((up, m))
    n = sum(len(m) for _, m in prepared)
    if n < 30:
        return None

    def stat(order_fn):
        d, close, d_exact, d_near, ne, nn = 0.0, 0, 0.0, 0.0, 0, 0
        for up, m in prepared:
            order = order_fn(up)
            cu = centres([up[k] for k in order])
            where = {orig: cu[pos] for pos, orig in enumerate(order)}
            for i, x, same in m:
                dx = abs(where[i] - x)
                d += dx
                close += dx <= 4
                if same:
                    d_exact += dx
                    ne += 1
                else:
                    d_near += dx
                    nn += 1
        return d / n, close / n, (d_exact / ne if ne else 0), (d_near / nn if nn else 0)

    obs = stat(lambda up: list(range(len(up))))

    def shuffled(up):
        if interior:
            mid = list(range(1, len(up) - 1))
            rng.shuffle(mid)
            return [0] + mid + [len(up) - 1]
        o = list(range(len(up)))
        rng.shuffle(o)
        return o

    null = [stat(shuffled) for _ in range(REPS)]
    mu = [statistics.mean(x[k] for x in null) for k in range(4)]
    sd = statistics.pstdev(x[0] for x in null)
    return {"matches": n, "distance": obs[0], "null": mu[0], "z": (obs[0] - mu[0]) / sd if sd else 0,
            "p": (1 + sum(x[0] <= obs[0] for x in null)) / (REPS + 1),
            "within_4_glyphs": obs[1], "within_4_null": mu[1],
            "exact_distance": obs[2], "exact_null": mu[2], "near_distance": obs[3], "near_null": mu[3]}


def vms_pages(**kw):
    v = Voynich("ZL")
    pages = {}
    for l in v.select(unit="P", **kw):
        if l.words:
            pages.setdefault(l.page, []).append(l.words)
    return list(pages.values())


def as_pages(lines, per_page=30):
    return [lines[i:i + per_page] for i in range(0, len(lines), per_page)]


texts = {
    "VMS all": vms_pages(),
    "VMS Currier A": vms_pages(language="A"),
    "VMS Currier B": vms_pages(language="B"),
    "copying model (positional copying built in)": as_pages(
        AutoCopy(seed=1, currier="B", boundary=chart, boundary_p=0.65, line_end_p=0.5, common_p=0.5).run(4000), 29),
    "Latin (Aix), 9 words a line": as_pages(chunk_lines(historical("Latin_Aix", 40000))),
    "Italian (Rettorica), 9 words a line": as_pages(chunk_lines(historical("Rettorica", 40000))),
}
src = DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt"
if src.exists():
    texts["Naibbe (Pliny)"] = as_pages([l.split() for l in open(src, encoding="utf-8-sig") if l.split()])

rows = []
for name, pages in texts.items():
    for lag in LAGS:
        r = test(pairs_at(pages, lag))
        if r:
            rows.append({"text": name, "lines apart": lag, **r})
            print(name, lag, {k: round(x, 3) if isinstance(x, float) else x for k, x in r.items()})

# VMS extras: with the margins left in, by section, by hand
extra = []
r = test(pairs_at(texts["VMS all"], 1), interior=False)
extra.append({"subset": "all, margins included", **r})
v = Voynich("ZL")
for sec in sorted({l.section for l in v.lines if l.unit == "P" and l.section}):
    r = test(pairs_at(vms_pages(section=sec), 1))
    if r:
        extra.append({"subset": f"section {sec}", **r})
for hand in sorted({l.hand for l in v.lines if l.unit == "P" and l.hand}):
    r = test(pairs_at(vms_pages(hand=hand), 1))
    if r:
        extra.append({"subset": f"hand {hand}", **r})

save(HERE, "vertical", {"lags": rows, "vms_lag1": extra})
cols = ["text", "lines apart", "matches", "distance", "null", "z", "p", "within_4_glyphs", "within_4_null"]
md = "# 24 vertical alignment\n\nMean horizontal distance (glyphs) between a word and the same-or-similar words k lines above it; null = upper line's interior words in random order.\n\n"
md += table(rows, cols)
md += "\n## exact and near matches separately, one line apart\n\n" + table(
    [r for r in rows if r["lines apart"] == 1], ["text", "exact_distance", "exact_null", "near_distance", "near_null"])
md += "\n## VMS, one line apart, subsets\n\n" + table(
    extra, ["subset", "matches", "distance", "null", "z", "p", "within_4_glyphs", "within_4_null"])
write_md(HERE, "vertical", md)
print(md)
