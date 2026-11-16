"""bi3mw's language-independent affix parser (voynich.ninja, Aug 2025).

His method: take the most frequent beginnings and endings of words (length
2-5) as prefixes and suffixes, strip them greedily (longest first) from both
ends of every word while at least two letters remain, call what is left the
stem. A word that is nothing but affixes (dai/in) has no stem. His heatmap of
prefix x suffix on the manuscript shows a few cells holding most of the text
(dai+in 851, qoka+iin, oka+iin).

The method is language-independent, which makes it a fair comparison. Same
parser, same settings (top 25), on the manuscript, the two content-free
controls and three real texts, 10 000 words each. Questions: how much of the
text is explained by affixes alone, how many stems are left, and how strongly
the prefix chooses the suffix (mutual information, minus what shuffling the
suffixes gives).
"""
import json
import math
import pathlib
import random
import re
import sys
import unicodedata
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import _path  # noqa: F401
from _common import save, table, write_md
from voynich import Voynich
from voynich.autocopy import AutoCopy
from voynich.corpus import DATA, historical

HERE = pathlib.Path(__file__).parent
N, TOP = 10000, 25


def affixes(words, top):
    pre, suf = Counter(), Counter()
    for w in words:
        for i in range(2, min(len(w), 6)):
            pre[w[:i]] += 1
            suf[w[-i:]] += 1
    return [p for p, _ in pre.most_common(top)], [s for s, _ in suf.most_common(top)]


def parse(w, pre, suf):
    ps, ss, stem = [], [], w
    while True:
        m = next((p for p in pre if stem.startswith(p) and len(stem) > len(p) + 1), None)
        if not m:
            break
        ps.append(m)
        stem = stem[len(m):]
    while True:
        m = next((s for s in suf if stem.endswith(s) and len(stem) > len(s) + 1), None)
        if not m:
            break
        ss.insert(0, m)
        stem = stem[:-len(m)]
    return ps, stem, ss


def H(c):
    n = sum(c.values())
    return -sum(x / n * math.log2(x / n) for x in c.values())


def mi(pairs):
    return H(Counter(a for a, _ in pairs)) + H(Counter(b for _, b in pairs)) - H(Counter(pairs))


def plain(words):
    out = []
    for w in words:
        w = unicodedata.normalize("NFD", w.lower())
        w = re.sub(r"[^a-z]", "", "".join(c for c in w if not unicodedata.combining(c)))
        if w:
            out.append(w)
    return out


chart = {k: set(x) for k, x in json.loads(
    (HERE.parent.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}
v = Voynich("ZL")
body = [l for l in v.lines if l.unit == "P"]
texts = {"VMS, Currier A": [w for l in body if l.meta.get("L") == "A" for w in l.words],
         "VMS, Currier B": [w for l in body if l.meta.get("L") == "B" for w in l.words],
         "copying model": [w for l in AutoCopy(seed=1, boundary=chart, boundary_p=0.65, line_end_p=0.5,
                                               common_p=0.5).run(4500) for w in l],
         "Naibbe cipher of Pliny": open(DATA / "external" / "naibbe-cipher" / "encrypted" /
                                        "nathist_output_ciphertext.txt", encoding="utf-8-sig").read().split(),
         "Latin (Secreta secretorum)": plain(historical("Secreta_Secretorum_LAT")),
         "Italian (Rettorica)": plain(historical("Rettorica")),
         "English (Alphabet of Tales)": plain(historical("AlphabetOfTales"))}
rng = random.Random(0)
rows, cells = [], {}
for name, words in texts.items():
    words = [w for w in words if w and "?" not in w and "'" not in w][:N]
    pre, suf = affixes(words, TOP)
    parsed = [parse(w, pre, suf) for w in words]
    nostem = [p for p in parsed if not p[1] or (p[0] or p[2]) and len(p[1]) < 2]
    pairs = [(p[0][0] if p[0] else "-", p[2][-1] if p[2] else "-") for p in parsed]
    a = [x for x, _ in pairs]
    b = [y for _, y in pairs]
    null = []
    for _ in range(50):
        rng.shuffle(b)
        null.append(mi(list(zip(a, b))))
    cell = Counter((x, y) for x, y in pairs if x != "-" and y != "-")
    stems = Counter(p[1] for p in parsed)
    rows.append({"text": name, "words": len(words), "distinct words": len(set(words)),
                 "with a prefix": sum(1 for p in parsed if p[0]) / len(words),
                 "with a suffix": sum(1 for p in parsed if p[2]) / len(words),
                 "prefix and suffix": sum(1 for p in parsed if p[0] and p[2]) / len(words),
                 "distinct stems": len(stems), "stems / distinct words": len(stems) / len(set(words)),
                 "top 10 cells hold": sum(c for _, c in cell.most_common(10)) / len(words),
                 "prefix -> suffix (bits)": mi(pairs) - sum(null) / len(null)})
    cells[name] = [(f"{x}/{y}", c) for (x, y), c in cell.most_common(6)]
    print(rows[-1], flush=True)

save(HERE, "affix_parser", {"rows": rows, "top cells": cells})
md = "# c12 bi3mw's affix parser on the manuscript, controls and real texts\n\n" + table(
    rows, ["text", "distinct words", "with a prefix", "with a suffix", "prefix and suffix", "distinct stems",
           "stems / distinct words", "top 10 cells hold", "prefix -> suffix (bits)"])
md += "\n## Commonest prefix/suffix cells\n\n" + table(
    [{"text": k, "cells": ", ".join(f"{a} {c}" for a, c in x)} for k, x in cells.items()], ["text", "cells"])
write_md(HERE, "affix_parser", md)
print(md)
