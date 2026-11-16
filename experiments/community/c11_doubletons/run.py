"""voynich.ninja, "Hapax and doubletons" (DG97EEB; question by R. Sale).

R. Sale asks: do words that occur exactly twice sit on the same page, in the
same hand, or spread out? If rare words are names of things, their two
occurrences should be close together (the thing is discussed once).

For every word type with exactly two occurrences: are both on the same line,
the same page, the same bifolium, the same section, in the same hand? Expected
rates if the two were placed at random among all tokens of the same Currier
language (so that dialect alone can't produce the result).
"""
import pathlib
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import _path  # noqa: F401
from _common import save, table, write_md
from voynich import Voynich

HERE = pathlib.Path(__file__).parent
v = Voynich("ZL")
tok = []
for l in v.lines:
    for w in l.words:
        tok.append({"w": w, "line": l.locus, "page": l.page, "sheet": (l.meta.get("Q"), l.meta.get("B")),
                    "section": l.section, "hand": l.hand, "lang": l.language})
freq = Counter(t["w"] for t in tok)
where = defaultdict(list)
for t in tok:
    where[t["w"]].append(t)

rows = []
for level in ("line", "page", "sheet", "section", "hand"):
    for n_occ in (2,):
        same = total = 0
        expected = 0.0
        for w, ts in where.items():
            if len(ts) != n_occ or len({t["lang"] for t in ts}) != 1 or ts[0]["lang"] is None:
                continue
            total += 1
            same += len({t[level] for t in ts}) < n_occ
            pool = Counter(t[level] for t in tok if t["lang"] == ts[0]["lang"])
            N = sum(pool.values())
            p2 = sum(c * (c - 1) for c in pool.values()) / (N * (N - 1))
            expected += p2 if n_occ == 2 else min(1.0, 3 * p2)
        rows.append({"both on the same": level, "occurrences": n_occ, "types": total,
                     "observed": same / total, "expected at random": expected / total,
                     "ratio": (same / total) / (expected / total)})
    print(rows[-1])

# how far apart, in pages, when not on the same page
order = {p: i for i, p in enumerate(v.pages)}
gaps = Counter()
for w, ts in where.items():
    if len(ts) == 2:
        d = abs(order[ts[0]["page"]] - order[ts[1]["page"]])
        gaps["same page" if d == 0 else "next page" if d == 1 else "2-5 pages" if d <= 5 else "6-20 pages" if d <= 20 else "further"] += 1
tot = sum(gaps.values())
gap_rows = [{"distance": k, "share of doubletons": gaps[k] / tot}
            for k in ("same page", "next page", "2-5 pages", "6-20 pages", "further")]

save(HERE, "doubletons", {"rows": rows, "gaps": gap_rows})
md = "# c11 doubletons\n\n" + table(rows, ["both on the same", "occurrences", "types", "observed", "expected at random", "ratio"])
md += "\nExpected: two tokens drawn at random from the same Currier language.\n"
md += "\n## distance between the two occurrences\n\n" + table(gap_rows, ["distance", "share of doubletons"])
write_md(HERE, "doubletons", md)
print(md)
