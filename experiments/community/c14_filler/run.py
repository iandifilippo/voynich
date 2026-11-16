"""Meaningful text hidden among filler (Mark Knowles, voynich.ninja thread 4057).

His proposal: perhaps a fifth of the text is real and the rest is
meaningless padding, and the real part should be the least repetitive.
Strip the repetitive lines and analyse what is left.

What is left can be tested with exp. 34's lexicon test, the one measure that
separates language from the manuscript sharply: does remembering whole words
help predict held-out words, beyond what the words' letter pairs predict?
Every real text says yes; the manuscript as a whole says no. If Knowles is
right, the least repetitive lines should say yes.

Repetitiveness of a line: share of its words that occur, exactly or with one
glyph changed, in the five lines before it on the same page. Lines are ranked
and the least repetitive quarter kept. The same selection is applied to a
Latin and an Italian text cut into lines of the manuscript's length, so the
selection itself can be seen not to destroy a real vocabulary. Every sample
is cut to the same number of words.
"""
import math
import pathlib
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import _path  # noqa: F401
from _common import save, table, write_md
from voynich import Voynich
from voynich.corpus import historical

HERE = pathlib.Path(__file__).parent
UNIT = re.compile(r"c[tkpf]h|ch|sh|eee|ee|iii|ii|.")
SIZE = 2400


def lexicon_gain(words, split, rng, folds=5, order=2):
    seqs = [tuple(split(w)) + ("$",) for w in words]
    idx = list(range(len(seqs)))
    rng.shuffle(idx)
    alphabet = len({s for q in seqs for s in q})
    a = b = 0.0
    for f in range(folds):
        tabs = [defaultdict(Counter) for _ in range(order + 1)]
        lex = Counter()
        for k, i in enumerate(idx):
            if k % folds == f:
                continue
            lex[seqs[i]] += 1
            q = ("^",) * order + seqs[i]
            for j in range(order, len(q)):
                for o in range(order + 1):
                    tabs[o][q[j - o:j]][q[j]] += 1
        n, t = sum(lex.values()), len(lex)
        for i in idx[f::folds]:
            q = ("^",) * order + seqs[i]
            lp = 0.0
            for j in range(order, len(q)):
                c0 = tabs[0][()]
                p = (c0[q[j]] + 0.5) / (sum(c0.values()) + 0.5 * alphabet)
                for o in range(1, order + 1):
                    c = tabs[o].get(q[j - o:j])
                    if c:
                        p = (c[q[j]] + len(c) * p) / (sum(c.values()) + len(c))
                lp += math.log2(p)
            a -= lp
            b -= math.log2((lex[seqs[i]] + t * 2 ** lp) / (n + t))
    return (a - b) / len(seqs)


def near(w, seen):
    if w in seen:
        return True
    for i in range(len(w)):
        for v in (w[:i] + w[i + 1:],):
            if v in seen:
                return True
    return any(w[:i] + w[i + 1:] == s[:i] + s[i + 1:] for s in seen if len(s) == len(w) for i in range(len(w)))


def rank(pages):
    """pages: list of lists of lines. Returns (score, line) for every line."""
    out = []
    for lines in pages:
        for k, l in enumerate(lines):
            seen = {w for m in lines[max(0, k - 5):k] for w in m}
            if not l:
                continue
            out.append((sum(near(w, seen) for w in l) / len(l), l))
    return out


def plain(words):
    out = []
    for w in words:
        w = unicodedata.normalize("NFD", w.lower())
        w = re.sub(r"[^a-z]", "", "".join(c for c in w if not unicodedata.combining(c)))
        if w:
            out.append(w)
    return out


def as_pages(words, line_len=8, page_lines=25):
    lines = [words[i:i + line_len] for i in range(0, len(words), line_len)]
    return [lines[i:i + page_lines] for i in range(0, len(lines), page_lines)]


v = Voynich("ZL")
sources = {}
for lang in ("A", "B"):
    pages = defaultdict(list)
    for l in v.lines:
        if l.unit == "P" and l.meta.get("L") == lang:
            pages[l.page].append([w for w in l.words if "?" not in w and "'" not in w])
    sources[f"VMS, Currier {lang}"] = (list(pages.values()), UNIT.findall)
sources["Latin (Secreta secretorum)"] = (as_pages(plain(historical("Secreta_Secretorum_LAT"))[:40000]), list)
sources["Italian (Rettorica)"] = (as_pages(plain(historical("Rettorica"))[:40000]), list)

rng = random.Random(0)
rows = []
for name, (pages, split) in sources.items():
    ranked = rank(pages)
    ranked.sort(key=lambda x: (x[0], rng.random()))
    q = len(ranked) // 4
    groups = {"least repetitive quarter": ranked[:q], "most repetitive quarter": ranked[-q:],
              "all lines": ranked[:]}
    row = {"text": name, "lines": len(ranked), "repeated words, least / most quarter":
           f"{sum(s for s, _ in ranked[:q]) / q:.2f} / {sum(s for s, _ in ranked[-q:]) / q:.2f}"}
    for g, sel in groups.items():
        sel = sel[:]
        rng.shuffle(sel)
        words = [w for _, l in sel for w in l][:SIZE]
        row[g] = sum(lexicon_gain(words, split, random.Random(s)) for s in range(5)) / 5
        row[g + ", words"] = len(words)
    rows.append(row)
    print(row, flush=True)

save(HERE, "filler", rows)
md = f"# c14 meaningful text among filler\n\nLexicon gain, bits per held-out word, {SIZE} words per sample (mean of 5 splits).\n\n"
md += table(rows, ["text", "lines", "repeated words, least / most quarter", "least repetitive quarter",
                   "most repetitive quarter", "all lines"])
write_md(HERE, "filler", md)
print(md)
