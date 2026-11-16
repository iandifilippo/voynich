"""Do pages follow a template?

Exp. 27 left two readings of page vocabulary: a subject, or copying within the
page. They disagree about one thing. An entry in a real herbal is built to a
plan (name and description first, then virtues and uses), so what gets said
depends on how far down the entry you are, the same way on every page. A
writer recycling recent words has no reason to use different words near the
top of a page than near the bottom, apart from the known special cases.

Test: split the lines of every page into top, middle and bottom thirds. Does
word use differ between the thirds, consistently across pages? Statistic: G
(log-likelihood ratio) of the table word x third for the 150 most frequent
words. Null: the same pages with their lines in random order (500 times),
which keeps every page's vocabulary and forgets position.

Two nulls. Lines of each page in random order (500 times) is the obvious one,
but it also destroys runs of similar neighbouring lines, and those alone make
the table lumpier. The stricter null keeps each page's lines in sequence and
only moves the frame: start at a random line, wrap around, and read upwards
half the time.

Known position effects are removed first so they can't produce the result:
paragraph-first lines (gallows words) are dropped, and so are the first and
last word of every line (exp. 10, 20). The last line of each paragraph is
dropped too (short lines). What is left is the body of the text.
"""
import json
import math
import pathlib
import random
import re
import statistics
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich
from voynich.autocopy import AutoCopy
from voynich.corpus import DATA

HERE = pathlib.Path(__file__).parent
REPS = 500
TOP = 150
ROOT = DATA / "external" / "naibbe-cipher"
chart = {k: set(v) for k, v in json.loads(
    (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}


def g_stat(pages, vocab, parts=3):
    tab = Counter()
    for lines in pages:
        n = len(lines)
        for i, l in enumerate(lines):
            part = min(parts - 1, i * parts // n)
            for w in l:
                if w in vocab:
                    tab[w, part] += 1
    row, col, tot = Counter(), Counter(), 0
    for (w, p), c in tab.items():
        row[w] += c
        col[p] += c
        tot += c
    g = 2 * sum(c * math.log(c * tot / (row[w] * col[p])) for (w, p), c in tab.items())
    return g, tab, row, col, tot


def test(pages, seed=0, parts=3):
    pages = [p for p in pages if len(p) >= 6]
    freq = Counter(w for p in pages for l in p for w in l)
    vocab = {w for w, c in freq.most_common(TOP) if c >= 10}
    obs, tab, row, col, tot = g_stat(pages, vocab, parts)
    rng = random.Random(seed)
    null, null2 = [], []
    for _ in range(REPS):
        sh = [rng.sample(p, len(p)) for p in pages]
        null.append(g_stat(sh, vocab, parts)[0])
        # keeps runs of similar lines together: each page turned upside down or not, and rolled
        rolled = []
        for p in pages:
            k = rng.randrange(len(p))
            q = p[k:] + p[:k]
            rolled.append(q[::-1] if rng.random() < 0.5 else q)
        null2.append(g_stat(rolled, vocab, parts)[0])
    mu, sd = statistics.mean(null), statistics.pstdev(null)
    mu2, sd2 = statistics.mean(null2), statistics.pstdev(null2)
    words = []
    for w in vocab:
        e = [row[w] * col[p] / tot for p in range(parts)]
        o = [tab[w, p] for p in range(parts)]
        gw = 2 * sum(x * math.log(x / y) for x, y in zip(o, e) if x)
        words.append((gw, w, o, [round(x, 1) for x in e]))
    words.sort(reverse=True)
    return {"pages": len(pages), "lines": sum(map(len, pages)), "words tested": len(vocab), "G": obs,
            "G shuffled": mu, "z": (obs - mu) / sd, "p": (1 + sum(x >= obs for x in null)) / (REPS + 1),
            "excess per word": (obs - mu) / len(vocab),
            "G rolled": mu2, "z rolled": (obs - mu2) / sd2,
            "p rolled": (1 + sum(x >= obs for x in null2)) / (REPS + 1)}, words[:12]


def vms_pages(body=True, **sel):
    v = Voynich("ZL")
    pages = {}
    by_page = {}
    for l in v.select(unit="P", **sel):
        by_page.setdefault(l.page, []).append(l)
    for p, ls in by_page.items():
        out = []
        for i, l in enumerate(ls):
            last_of_para = l.para_end or i == len(ls) - 1 or ls[i + 1].para_start
            if body and (l.para_start or last_of_para):
                continue
            w = l.words[1:-1] if body else l.words
            if len(w) >= 2:
                out.append(w)
        pages[p] = out
    return [pages[p] for p in v.pages if p in pages]


def pliny():
    raw = open(ROOT / "input" / "examples" / "nathist_book16.txt", encoding="utf-8").read().split("\n")
    out = []
    for line in raw:
        t = line.strip()
        if re.fullmatch(r"[IVXLC]+", t):
            out.append([])
        elif t and not t.isdigit() and out:
            w = re.findall(r"[a-z]+", t.lower())
            if len(w) >= 4:
                out[-1].append(w[1:-1])
    return out


model = AutoCopy(seed=1, currier="A", boundary=chart, boundary_p=0.65, line_end_p=0.5, common_p=0.5,
                 page_lines=13)
ml = model.run(2400)
starts = set(model.paragraph_starts)
model_pages = []
for i in range(0, len(ml), 13):
    pg = [ml[j][1:-1] for j in range(i, min(i + 13, len(ml)))
          if j not in starts and j + 1 not in starts and len(ml[j]) >= 4]
    model_pages.append(pg)

texts = {
    "VMS herbal A, hand 1 (body text)": vms_pages(language="A", hand="1", section="H"),
    "VMS herbal A, hand 1 (everything left in)": vms_pages(body=False, language="A", hand="1", section="H"),
    "VMS pharma A, hand 1 (body text)": vms_pages(language="A", hand="1", section="P"),
    "VMS balneo B, hand 2 (body text)": vms_pages(language="B", hand="2", section="B"),
    "VMS stars B, hand 3 (body text)": vms_pages(language="B", hand="3", section="S"),
    "VMS herbal B, hand 2 (body text)": vms_pages(language="B", hand="2", section="H"),
    "Pliny 16, chapters": pliny(),
    "copying model, 13-line pages (body text)": model_pages,
}
rows, tops = [], {}
for name, pages in texts.items():
    if sum(len(p) >= 6 for p in pages) < 8:
        continue
    r, words = test(pages)
    r["text"] = name
    rows.append(r)
    tops[name] = [{"word": w, "top / middle / bottom": " / ".join(map(str, o)),
                   "expected": " / ".join(map(str, e)), "G": g} for g, w, o, e in words]
    print(name, {k: round(x, 3) if isinstance(x, float) else x for k, x in r.items()})

save(HERE, "template", {"rows": rows, "words": tops})
md = "# 28 do pages follow a template?\n\n" + table(
    rows, ["text", "pages", "lines", "words tested", "G", "G shuffled", "z", "p", "G rolled", "z rolled", "p rolled"])
md += "\nG: how unevenly the frequent words are spread over the top, middle and bottom third of the page. Shuffled: lines of each page in random order. Rolled: each page's lines kept in sequence but started at a random line and, half the time, read bottom to top; this keeps runs of similar lines, so only a position effect that is the same on every page can beat it.\n"
for name in ("VMS herbal A, hand 1 (body text)", "VMS stars B, hand 3 (body text)", "VMS balneo B, hand 2 (body text)"):
    if name in tops:
        md += f"\n## words that depend most on position: {name}\n\n" + table(
            tops[name], ["word", "top / middle / bottom", "expected", "G"])
write_md(HERE, "template", md)
print(md)
