"""Is there a setting per line, too?

Exp. 48: the gallows a word carries predicts the gallows of the words after it
in the same line about equally at distance 1, 2 and 3 (0.032, 0.024, 0.020
bits in B), which is what a choice made once per line would look like, not a
sequence. Exp. 40-42 found a setting per page and per sheet; this asks whether
the line is a unit too.

For pairs of words on the same page, how often do they agree on a feature
(same gallows; same start; same ending), comparing
  two words of the same line, at a given distance apart,
  two words of different lines of the same page, at the same positions.
The first word of each line is left out (line starts have their own habits).
If lines have their own setting, same-line pairs agree more at every
distance; if it's only sequence, the excess dies out with distance.
Run on Currier A and B, the exp. 36 generator and Latin (first letter,
last letter, a letter class in place of the gallows).
"""
import pathlib
import random
import re
import sys
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402
from voynich.assemble import Assembler, signs  # noqa: E402
from voynich.corpus import historical  # noqa: E402

HERE = pathlib.Path(__file__).parent
GAL = ("t", "k", "p", "f", "cth", "ckh", "cph", "cfh")
VMS_FEATS = {"gallows": lambda w: next((x for x in signs(w) if x in GAL), "-"),
             "start": lambda w: signs(w)[0], "ending": lambda w: signs(w)[-1]}
LAT_FEATS = {"has a stop (b c d g p t)": lambda w: any(c in "bcdgpt" for c in w),
             "start": lambda w: w[0], "ending": lambda w: w[-1]}


def agreement(pages, feats):
    rows = {}
    for name, g in feats.items():
        for d in (1, 2, 3, 4):
            same = diff = n_same = n_diff = 0
            for lines in pages:
                ls = [[g(w) for w in l[1:]] for l in lines if len(l) > d + 1]
                for i, l in enumerate(ls):
                    for k in range(len(l) - d):
                        same += l[k] == l[k + d]
                        n_same += 1
                    for j in range(len(ls)):
                        if j == i:
                            continue
                        m = ls[j]
                        for k in range(min(len(l), len(m)) - d):
                            diff += l[k] == m[k + d]
                            n_diff += 1
            rows[name, d] = (same / n_same, diff / n_diff)
    return rows


v = Voynich("ZL")


def vms_pages(lang):
    by = defaultdict(list)
    for l in v.lines:
        if l.unit == "P" and l.meta.get("L") == lang:
            ws = [w for w in l.words if "?" not in w and "'" not in w]
            if ws:
                by[l.page].append(ws)
    return list(by.values())


def plain(ws):
    import unicodedata
    out = []
    for w in ws:
        w = unicodedata.normalize("NFD", w.lower())
        w = re.sub(r"[^a-z]", "", "".join(c for c in w if not unicodedata.combining(c)))
        if w:
            out.append(w)
    return out


B, A = vms_pages("B"), vms_pages("A")
m = Assembler(order=2, recall_p=0.01, edit_p=0.10, window=5).fit([l for p in B for l in p])
G = [m.fill([(len(l), False) for l in p], seed=i) for i, p in enumerate(B)]
lat = plain(historical("Secreta_Secretorum_LAT"))[:20000]
lat_lines = [lat[i:i + 9] for i in range(0, len(lat), 9)]
L = [lat_lines[i:i + 25] for i in range(0, len(lat_lines), 25)]

rows = []
for name, pages, feats in (("Currier B", B, VMS_FEATS), ("Currier A", A, VMS_FEATS),
                           ("generator (exp. 36)", G, VMS_FEATS), ("Latin", L, LAT_FEATS)):
    res = agreement(pages, feats)
    for f in feats:
        row = {"text": name, "feature": f}
        for d in (1, 2, 3, 4):
            s, o = res[f, d]
            row[f"d={d}: same line / other line"] = f"{s:.3f} / {o:.3f}"
            row[f"d={d} ratio"] = s / o
        rows.append(row)
        print(row, flush=True)
save(HERE, "line_setting", rows)
md = "# 49 a setting per line?\n\nShare of word pairs that agree on a feature: same line vs different lines of the same page, at the same positions.\n\n"
md += table(rows, ["text", "feature"] + [f"d={d} ratio" for d in (1, 2, 3, 4)])
md += "\n## Raw shares\n\n" + table(rows, ["text", "feature"] + [f"d={d}: same line / other line" for d in (1, 2, 3, 4)])
write_md(HERE, "line_setting", md)
print(md)
