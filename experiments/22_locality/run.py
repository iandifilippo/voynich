"""At what distance do words stick together?

Exp. 21 left the copying model with the wrong frequency spectrum: too many
words of middling frequency, too weak a core. Copying is local: a new variant
is copied a few times nearby and then lost. Is that how VMS words behave?

For a word that occurs in line i, how much more likely than its base rate is it
to occur in line i+k? ("lift"; 1 = no memory.) By frequency band (core: 21+
occurrences in the 10 000-word sample, middle: 6-20, low: 2-5) and for
k = 1, 2, 5, 10, 25, 100 lines. Also the same thing within a single line
(a second occurrence in the same line, against chance).

Then variants of the copying model:
  - as published: sources mostly from the last few lines
  - a share g of sources drawn from anywhere in the text written so far
  - "prefer common": when the word about to be copied has been written fewer
    than three times so far, look again with probability c. Rare variants
    become dead ends instead of models for further copies.
"""
import json
import pathlib
import statistics
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, benchmark, historical, chunk_lines
from voynich.autocopy import AutoCopy
from voynich.corpus import DATA

HERE = pathlib.Path(__file__).parent
ref = benchmark.reference()
LAGS = [1, 2, 5, 10, 25, 100]
BANDS = [("core 21+", 21, 10 ** 9), ("middle 6-20", 6, 20), ("low 2-5", 2, 5)]
chart = {k: set(v) for k, v in json.loads(
    (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}


def take(lines, n=10000):
    out, k = [], 0
    for l in lines:
        if k >= n:
            break
        if l:
            out.append(list(l))
            k += len(l)
    return out


def locality(lines):
    lines = take(lines)
    f = Counter(w for l in lines for w in l)
    sets = [set(l) for l in lines]
    n = len(sets)
    n_tok = sum(f.values())
    out = {}
    for band, lo, hi in BANDS:
        types = [w for w, c in f.items() if lo <= c <= hi]
        r = {"types": len(types), "share_of_text": sum(f[w] for w in types) / n_tok}
        present = {w: [w in s for s in sets] for w in types}
        for k in LAGS:
            num = den = 0.0
            for w in types:
                inl = present[w]
                base = sum(inl) / n
                num += sum(a and b for a, b in zip(inl, inl[k:]))
                den += sum(inl[:n - k]) * base
            r[f"lag {k}"] = num / den if den else None
        # second occurrence in the same line vs chance
        obs = sum(l.count(w) - 1 for l in lines for w in set(l) if lo <= f[w] <= hi and l.count(w) > 1)
        exp = sum((len(l) - 1) * f[w] / n_tok for l in lines for w in set(l) if lo <= f[w] <= hi)
        r["same line"] = obs / exp if exp else None
        out[band] = r
    return out


def model(g=0.0, c=0.0, seeds=(1, 2, 3, 4)):
    return [AutoCopy(seed=s, currier="B", boundary=chart, boundary_p=0.65, line_end_p=0.5,
                     global_p=g, common_p=c).run(1400) for s in seeds]


v = Voynich("ZL")
texts = {
    "VMS Currier B": [v.text_lines(unit="P", language="B")],
    "VMS Currier A": [v.text_lines(unit="P", language="A")],
    "copying model": model(),
    "copying model, 60% of sources from anywhere": model(g=0.6),
    "copying model, prefer common c = 0.3": model(c=0.3),
    "copying model, prefer common c = 0.5": model(c=0.5),
    "copying model, prefer common c = 0.7": model(c=0.7),
    "Latin (Aix)": [chunk_lines(historical("Latin_Aix", 12000))],
    "Italian (Rettorica)": [chunk_lines(historical("Rettorica", 12000))],
}
src = DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt"
if src.exists():
    texts["Naibbe (Pliny)"] = [[l.split() for l in open(src, encoding="utf-8-sig") if l.split()]]

rows, bench = [], []
for name, runs in texts.items():
    locs = [locality(r) for r in runs]
    for band, _, _ in BANDS:
        row = {"text": name, "band": band}
        for k in ["types", "share_of_text", "same line"] + [f"lag {x}" for x in LAGS]:
            vals = [l[band][k] for l in locs if l[band][k] is not None]
            row[k] = statistics.mean(vals) if vals else None
        rows.append(row)
    sc = [benchmark.score(r, ref) for r in runs]
    bench.append({"text": name, "distance": statistics.mean(s[0] for s in sc),
                  "distance_sd": statistics.pstdev(s[0] for s in sc) if len(sc) > 1 else None,
                  "h2": statistics.mean(s[2]["h2"] for s in sc),
                  "mattr": statistics.mean(s[2]["mattr500"] for s in sc),
                  "repeat": statistics.mean(s[2]["repeat_rate"] for s in sc),
                  "edge": statistics.mean(s[2]["edge_coupling"] for s in sc),
                  "worst": ", ".join(f"{k} {x:+.1f}" for k, x in sorted(
                      {k: statistics.mean(s[1][k] for s in sc) for k in benchmark.KEYS}.items(),
                      key=lambda kv: -abs(kv[1]))[:3]),
                  "hapax": statistics.mean(s[2]["hapax_ratio"] for s in sc),
                  "cohesion": statistics.mean(s[2]["line_cohesion"] for s in sc),
                  "core_share": statistics.mean(l["core 21+"]["share_of_text"] for l in locs),
                  "middle_lag1": statistics.mean(l["middle 6-20"]["lag 1"] for l in locs),
                  "middle_lag25": statistics.mean(l["middle 6-20"]["lag 25"] for l in locs)})
    print(bench[-1])

save(HERE, "locality", {"lift": rows, "summary": bench})
cols = ["text", "types", "share_of_text", "same line"] + [f"lag {x}" for x in LAGS]
md = "# 22 locality\n\nLift = how much more often than its base rate a word turns up k lines after a line that has it (first 10 000 words of each text).\n"
for band, _, _ in BANDS:
    md += f"\n## {band} occurrences\n\n" + table([r for r in rows if r["band"] == band], cols)
md += "\n## summary\n\n" + table(bench, ["text", "distance", "distance_sd", "hapax", "core_share", "cohesion", "mattr", "h2", "repeat", "edge",
                                           "middle_lag1", "middle_lag25", "worst"])
write_md(HERE, "locality", md)
print(md)
