"""Is the residual made by doubtful spaces?

The start-to-start transitions that carry most of the residual involve short
pieces (or -> aii, ar -> al, or -> ai, da -> al), which look like words cut in
two at a doubtful space (exp. 16, exp. 46). The transliteration marks
uncertain spaces with commas; exp. 16 read them three ways. Here: the
beyond-the-boundary measure (exp. 48) on Currier B with doubtful spaces read
as spaces (as everywhere so far) and as no space at all, and with words of
one or two signs removed from the pairs.
"""
import pathlib
import random
import re
import sys
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import run  # noqa: E402
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402
from voynich.assemble import signs  # noqa: E402

HERE = pathlib.Path(__file__).parent


def sheets_for(commas):
    v = Voynich("ZL", commas=commas)
    by = defaultdict(list)
    for l in v.lines:
        if l.unit == "P" and l.meta.get("L") == "B" and re.fullmatch(r"f\d+[rv]\d*", l.page):
            ws = [w for w in l.words if "?" not in w and "'" not in w]
            if ws:
                m = v.pages.get(l.page) or {}
                by[(m.get("Q"), m.get("B"))].append(ws)
    return [ls for ls in by.values() if sum(map(len, ls)) >= 100]


rng = random.Random(0)
rows = []
for label, sheets in (("doubtful spaces read as spaces", sheets_for("split")),
                      ("doubtful spaces read as no space", sheets_for("join"))):
    rows.append({"Currier B": label, "words": sum(len(l) for s in sheets for l in s),
                 "beyond the boundary (bits)": run.beyond_boundary(sheets, rng)})
    long_only = [[[w for w in l if len(signs(w)) >= 3] for l in s] for s in sheets]
    rows.append({"Currier B": label + ", words of 3+ signs only",
                 "words": sum(len(l) for s in long_only for l in s),
                 "beyond the boundary (bits)": run.beyond_boundary(long_only, rng)})
    print(rows[-2], rows[-1], sep="\n", flush=True)
g = run.generate(0.9, 2.5, 7)
g3 = [[[w for w in l if len(signs(w)) >= 3] for l in s] for s in g]
rows.append({"Currier B": "generator with settings, words of 3+ signs only",
             "words": sum(len(l) for s in g3 for l in s), "beyond the boundary (bits)": run.beyond_boundary(g3, rng)})
save(HERE, "spacing", rows)
md = "# 50 doubtful spaces and short words\n\n" + table(rows, ["Currier B", "words", "beyond the boundary (bits)"])
write_md(HERE, "spacing", md)
print(md)
