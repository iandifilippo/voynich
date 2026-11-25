"""Spaces measured letter by letter, from Ryan Allen's glyph map.

Exps. 55 and 57 measured spaces with word boxes and with ink masks, and had
to guess where inside a line each boundary falls (glyphs taken as equally
wide). The glyph map (ryanallen.com/voynich, CC BY 4.0) gives the ink of
every letter, so every gap can be measured directly: between two letters
of a word, at a ZL doubtful space (comma, which the map keeps inside its
words) and at a ZL certain space (dot).

Gap = horizontal distance between the ink of the two units, using only ink
within +-0.6 x-heights of the line's centre (x-height and centre: median box
height and centre of o, a, e, y on that line), divided by the x-height.

Then the link across each kind of boundary: mutual information between the
end of one word (last sign, or -dy -ey -in -ol -al -ar -or) and the start of
the next (first sign, or ch sh qo), minus its mean with the pairs shuffled;
certain spaces split into width terciles and subsampled to the number of
commas so the three are compared at equal n. Finally the qo- rhythm of
exp. 62 in each tercile.

Data: data/external/glyph-map (see data/README.md). Only machine-drafted
words ('auto', 'auto-checked') are used for certain spaces: 31% of the
'auto-placed' ones have overlapping words (negative gaps), most likely
placement errors.
"""
import glob
import pathlib
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich.assemble import family  # noqa: E402

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
G = ROOT / "data" / "external" / "glyph-map"
rng = np.random.default_rng(0)

words = pd.read_csv(G / "words.tsv", sep="\t")
letters = pd.read_csv(G / "letters.tsv", sep="\t")
wi = words.set_index("word_id")
reading = wi.reading.str.split(" ")


def zl_tokens():
    """ZL words per locus, split on '.', with doubtful spaces (',') kept."""
    out = {}
    for line in (ROOT / "data" / "ZL3b-n.txt").read_text(encoding="latin-1").splitlines():
        m = re.match(r"<(f\w+\.\d+),[^>]*>\s+(.*)", line)
        if not m:
            continue
        loc, t = m.groups()
        t = re.sub(r"<[^>]*>", "", t)
        t = re.sub(r"\[([^:\]]*):[^\]]*\]", r"\1", t)
        t = re.sub(r"[{}@0-9;!*'\"%-]", "", t)
        out[loc] = t.split(".")
    return out


def plain(s):
    return s.replace("?", "").replace(",", "")


zl = zl_tokens()
token = {}
for r in words.itertuples():
    toks = zl.get(r.locus, [])
    if r.word - 1 < len(toks) and plain(toks[r.word - 1]) == r.reading.replace(" ", "").replace("+", ""):
        token[r.word_id] = toks[r.word - 1].replace("?", "")

small = letters[letters.eva.isin(["o", "a", "e", "y"])].merge(words[["word_id", "locus"]], on="word_id")
small = small.assign(h=small.y1 - small.y0)
xh = small.groupby("locus").h.median()
centre = small.groupby("locus").cy.median()


def ligature(a, b):
    return (a in "cs" and b in "htkpf") or (a in "tkpf" and b == "h")


between, within = [], []
for f in sorted(glob.glob(str(G / "masks" / "*.npz"))):
    m = np.load(f, allow_pickle=False)
    order = np.argsort(m["word"], kind="stable")
    W, Lt, X, Y, I = (m[k][order] for k in ("word", "letter", "x", "y", "image"))
    starts = np.searchsorted(W, np.arange(len(m["words"]) + 1))
    info = {}
    for k, wid in enumerate(m["words"]):
        a, b = starts[k], starts[k + 1]
        if b <= a or wid not in wi.index or wi.at[wid, "locus"] not in xh.index:
            continue
        loc = wi.at[wid, "locus"]
        sel = np.abs(Y[a:b] - centre[loc]) <= 0.6 * xh[loc]
        if sel.any():
            info[wid] = (loc, xh[loc], X[a:b][sel], Lt[a:b][sel], int(np.bincount(I[a:b]).argmax()))
    for wid, (loc, h, xs, ls, img) in info.items():
        nxt = f"{loc}.w{wi.at[wid, 'word'] + 1}"
        if nxt in info and info[nxt][4] == img:
            between.append((wid, nxt, (info[nxt][2].min() - xs.max()) / h, wi.at[wid, "trust"], wi.at[nxt, "trust"]))
        rd = reading[wid]
        commas, k = set(), 0
        for ch in token.get(wid, ""):
            if ch == ",":
                commas.add(k)
            else:
                k += 1
        ends = np.cumsum([len(t.replace("+", "")) for t in rd])
        for i in range(len(rd) - 1):
            p, q = xs[ls == i], xs[ls == i + 1]
            if len(p) and len(q):
                within.append((wid, i, rd[i], rd[i + 1], (q.min() - p.max()) / h, int(ends[i]) in commas,
                               ligature(rd[i][-1], rd[i + 1][0])))

B = pd.DataFrame(between, columns=["w1", "w2", "gap", "t1", "t2"])
Wn = pd.DataFrame(within, columns=["word", "i", "a", "b", "gap", "comma", "lig"])
letters_gap = Wn[~Wn.lig & ~Wn.comma]
machine = ["auto", "auto-checked"]
rel = B[B.t1.isin(machine) & B.t2.isin(machine) & (B.gap > 0)].copy()


def joined(t):
    return "".join(x.replace("+", "") for x in t)


def first(t):
    s = joined(t)
    return s[:2] if s[:2] in ("ch", "sh", "qo") else s[:1]


def last(t):
    s = joined(t)
    return s[-2:] if s[-2:] in ("dy", "ey", "in", "ol", "al", "ar", "or") else s[-1:]


def mi(a, b):
    a = pd.Series(a).astype("category").cat.codes.values
    b = pd.Series(b).astype("category").cat.codes.values
    c = np.zeros((a.max() + 1, b.max() + 1))
    np.add.at(c, (a, b), 1)
    p = c / c.sum()
    e = p.sum(1, keepdims=True) @ p.sum(0, keepdims=True)
    nz = p > 0
    return float((p[nz] * np.log2(p[nz] / e[nz])).sum())


def excess(a, b, reps=50):
    return mi(a, b) - np.mean([mi(a, rng.permutation(b)) for _ in range(reps)])


rel["A"] = [last(reading[w]) for w in rel.w1]
rel["Bf"] = [first(reading[w]) for w in rel.w2]
rel["third"] = pd.qcut(rel.gap, 3, labels=["narrow", "mid", "wide"])
cm = Wn[Wn.comma].copy()
cm["A"] = [last(reading[w][:i + 1]) for w, i in zip(cm.word, cm.i)]
cm["Bf"] = [first(reading[w][i + 1:]) for w, i in zip(cm.word, cm.i)]

q = lambda s: [round(float(x), 2) for x in s.quantile([0.1, 0.25, 0.5, 0.75, 0.9])]  # noqa: E731
dist = [{"gap": "letters inside a word (ligatures left out)", "n": len(letters_gap), "quantiles": q(letters_gap.gap)},
        {"gap": "doubtful space (ZL ',')", "n": len(cm), "quantiles": q(cm.gap)},
        {"gap": "certain space (ZL '.'), all words", "n": len(B), "quantiles": q(B.gap)},
        {"gap": "certain space, machine-drafted words, gap > 0", "n": len(rel), "quantiles": q(rel.gap)}]
negative = B.assign(neg=B.gap < 0).groupby("t1").neg.mean().round(3).to_dict()

link = [{"boundary": "doubtful space", "n": len(cm), "median gap": float(cm.gap.median()),
         "link (bits)": float(np.mean([excess(*cm.sample(len(cm), replace=True, random_state=s)[["A", "Bf"]].values.T)
                                       for s in range(20)]))}]
for t, g in rel.groupby("third", observed=True):
    es = [excess(*g.sample(len(cm), random_state=s)[["A", "Bf"]].values.T) for s in range(20)]
    link.append({"boundary": f"certain space, {t}", "n": len(g), "median gap": float(g.gap.median()),
                 "link (bits)": float(np.mean(es)), "sd": float(np.std(es))})

from voynich import Voynich  # noqa: E402

page_lang = {}
for line in Voynich("ZL").lines:
    page_lang.setdefault(line.page, line.language)
rel["lang"] = [page_lang.get(w.split(".")[0]) for w in rel.w1]
by_lang = []
for lg in ("A", "B"):
    g0 = rel[rel.lang == lg]
    for t, g in g0.groupby(pd.qcut(g0.gap, 3, labels=["narrow", "mid", "wide"]), observed=True):
        by_lang.append({"language": lg, "space": t, "n": len(g), "median gap": float(g.gap.median()),
                        "link (bits)": excess(g.A.values, g.Bf.values)})

rel["s1"] = [joined(reading[w]) for w in rel.w1]
rel["s2"] = [joined(reading[w]) for w in rel.w2]
rhythm = []
for t, g in rel.groupby("third", observed=True):
    base = g.s2.str.startswith("q").mean()
    cy = g[[family(a) == "c" and a.endswith("y") for a in g.s1]]
    nlr = g[[a.endswith(("n", "l", "r")) for a in g.s1]]
    rhythm.append({"space": t, "n": len(g), "P(qo)": base, "after ch/sh-y": cy.s2.str.startswith("q").mean() / base,
                   "after -n/-l/-r": nlr.s2.str.startswith("q").mean() / base})

wide = letters_gap[letters_gap.gap >= 0.6]
pairs = (wide.a.str[-1] + "-" + wide.b.str[0]).value_counts().head(8)
allp = (letters_gap.a.str[-1] + "-" + letters_gap.b.str[0]).value_counts()
wide_rows = [{"letters": k, "wide (>= 0.6)": int(v), "all": int(allp[k]), "share wide": v / allp[k]} for k, v in pairs.items()]

save(HERE, "glyph_gaps", {"distributions": dist, "negative_share_by_trust": negative, "link": link,
                          "rhythm": rhythm, "by_language": by_lang, "wide_inside_words": wide_rows,
                          "wide_share": len(wide) / len(letters_gap), "matched_tokens": len(token)})
md = "# 66 spaces from the glyph map\n\n## Gap widths (x-heights; 10/25/50/75/90th percentiles)\n\n"
md += table(dist, ["gap", "n", "quantiles"])
md += "\nShare of certain spaces with overlapping ink (gap < 0), by trust of the first word: "
md += ", ".join(f"{k} {v}" for k, v in negative.items()) + "\n"
md += "\n## Link across the boundary (excess mutual information, equal n)\n\n"
md += table(link, ["boundary", "n", "median gap", "link (bits)", "sd"])
md += "\n## Same, within each Currier language (each tercile at its own n)\n\n"
md += table(by_lang, ["language", "space", "n", "median gap", "link (bits)"])
md += "\n## The qo- rhythm by space width (over the base rate of qo-)\n\n"
md += table(rhythm, ["space", "n", "P(qo)", "after ch/sh-y", "after -n/-l/-r"])
md += f"\n## Wide gaps inside words ({len(wide)} of {len(letters_gap)}, {len(wide) / len(letters_gap):.3f})\n\n"
md += table(wide_rows, ["letters", "wide (>= 0.6)", "all", "share wide"])
write_md(HERE, "glyph_gaps", md)
print(md)
