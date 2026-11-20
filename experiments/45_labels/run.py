"""Do labels name what the text on their page talks about?

Many drawings carry a one-word label: a jar or a root in the pharmaceutical
pages, a nymph in the bathing pages, a star, a figure in the zodiac rings. If
the writing means something, a label is a name, and a page's text should
mention what its drawings are labelled with more than other pages' text does.
That is a test that doesn't need to know the language.

For every label word (4+ letters), its occurrences in running text (paragraph
lines and ring/circle text) of
  the same page,
  the other pages of the same sheet,
  all other pages of the same section,
per 1000 words of that text. Exact matches, and near matches (one glyph
different), since a page's setting (exp. 40) makes words on a page look
alike without meaning anything; a near-match excess with no exact-match
excess is what the setting alone would give.

Control: the same counts for "labels" that are not labels: words drawn from
the running text of a page of the same section, matched in length, looked up
in the text of a different page of the same sheet and of other pages.
"""
import pathlib
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich

HERE = pathlib.Path(__file__).parent
MIN_LEN = 4
TEXT_UNITS = {"P", "R", "C"}
SECTIONS = {"P": "pharmaceutical", "B": "bathing", "Z": "zodiac", "C": "cosmological", "A": "astronomical",
            "T": "text", "H": "herbal", "S": "stars"}


def edit1(a, b):
    if abs(len(a) - len(b)) > 1 or a == b:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))


v = Voynich("ZL")
text, labels, section, sheet = defaultdict(list), defaultdict(list), {}, {}
for l in v.lines:
    ws = [w for w in l.words if "?" not in w and "'" not in w]
    section[l.page] = l.meta.get("I")
    m = re.fullmatch(r"f(\d+)[rv]\d*", l.page)
    if m:
        pm = v.pages.get(l.page) or {}
        sheet[l.page] = (pm.get("Q"), pm.get("B"))
    if l.unit in TEXT_UNITS:
        text[l.page] += ws
    elif l.unit.startswith("L"):
        labels[l.page] += [w for w in ws if len(w) >= MIN_LEN]


def rates(probes, rng_pages=None):
    """probes: list of (word, page). Exact and near hits per 1000 text words."""
    out = {k: [0, 0, 0] for k in ("same page", "same sheet, other page", "same section, other sheets")}
    for w, p in probes:
        sec = section[p]
        for q in text:
            if section[q] != sec or not text[q]:
                continue
            if q == p:
                k = "same page"
            elif sheet.get(q) and sheet.get(q) == sheet.get(p):
                k = "same sheet, other page"
            else:
                k = "same section, other sheets"
            out[k][0] += sum(1 for x in text[q] if x == w)
            out[k][1] += sum(1 for x in text[q] if edit1(x, w))
            out[k][2] += len(text[q])
    return {k: (1000 * a / n if n else float("nan"), 1000 * b / n if n else float("nan")) for k, (a, b, n) in out.items()}


rng = random.Random(0)
rows = []
for sec in ("P", "B", "Z", "C", "A", "S", "H", "T"):
    probes = [(w, p) for p, ws in labels.items() if section[p] == sec and text.get(p) for w in ws]
    if len(probes) < 15:
        continue
    r = rates(probes)
    # pseudo-labels: words of matched length from the running text of the same section,
    # attributed to a page of the same section that is not the page they came from
    pages = [p for p in text if section[p] == sec and text[p]]
    pool = [(w, p) for p in pages for w in text[p] if len(w) >= MIN_LEN]
    lens = Counter(len(w) for w, _ in probes)
    fake = []
    for L, n in lens.items():
        cand = [x for x in pool if len(x[0]) == L] or pool
        for _ in range(n * 10):
            w, src = rng.choice(cand)
            others = [p for p in pages if p != src]
            fake.append((w, rng.choice(others)))
    rf = rates(fake)
    for kind, res in (("labels", r), ("words from other pages' text (control)", rf)):
        rows.append({"section": SECTIONS[sec], "probes": kind, "n": len(probes) if kind == "labels" else len(fake),
                     **{f"{k}: exact": res[k][0] for k in res}, **{f"{k}: near": res[k][1] for k in res}})
    print(rows[-2], rows[-1], sep="\n", flush=True)

save(HERE, "labels", rows)
ks = ("same page", "same sheet, other page", "same section, other sheets")
md = "# 45 labels and the text on their page\n\nHits per 1000 words of running text.\n\n## Exact\n\n" + table(
    rows, ["section", "probes", "n"] + [f"{k}: exact" for k in ks]) + "\n## One glyph different\n\n" + table(
    rows, ["section", "probes", "n"] + [f"{k}: near" for k in ks])
write_md(HERE, "labels", md)
print(md)


# raw counts behind the exact-match rates, and how labels are built
counts = []
for sec in ("P", "B", "Z"):
    probes = [(w, p) for p, ws in labels.items() if section[p] == sec and text.get(p) for w in ws]
    same = sum(1 for w, p in probes for x in text[p] if x == w)
    other = sum(1 for w, p in probes for q in text if q != p and section[q] == sec for x in text[q] if x == w)
    in_text = sum(1 for w, _ in probes if any(w in text[q] for q in text))
    counts.append({"section": SECTIONS[sec], "label tokens": len(probes), "hits on own page": same,
                   "hits elsewhere in section": other, "labels found anywhere in running text": in_text / len(probes)})
all_text = [w for ws in text.values() for w in ws if len(w) >= MIN_LEN]
all_lab = [w for ws in labels.values() for w in ws]
shape = []
for name, ws in (("labels", all_lab), ("running text (4+ letters)", all_text)):
    c = Counter(w[0] for w in ws)
    shape.append({"words": name, "n": len(ws), "start o": c["o"] / len(ws), "start q": c["q"] / len(ws),
                  "start ch/sh": sum(1 for w in ws if w[:2] in ("ch", "sh")) / len(ws),
                  "start d": c["d"] / len(ws), "end y": sum(w.endswith("y") for w in ws) / len(ws),
                  "end n": sum(w.endswith("n") for w in ws) / len(ws)})
save(HERE, "labels_counts", {"counts": counts, "shape": shape})
md += "\n## Raw counts\n\n" + table(counts, ["section", "label tokens", "hits on own page", "hits elsewhere in section",
                                            "labels found anywhere in running text"])
md += "\n## How labels are built\n\n" + table(shape, ["words", "n", "start o", "start q", "start ch/sh", "start d",
                                                   "end y", "end n"])
write_md(HERE, "labels", md)
print(md[md.index("## Raw"):])


# Labels start with o- three times as often as text words and almost never
# with q-. Two readings of a label o- word: the text word without the o
# (o as a prefix of labels), or the text word with qo- (labels drop the q).
# For each, is the transformed label found on its own page more than elsewhere?
def transformed(fn):
    out = {}
    for sec in ("P", "B", "Z"):
        probes = [(fn(w), p) for p, ws in labels.items() if section[p] == sec and text.get(p) for w in ws
                  if w.startswith("o") and len(w) > MIN_LEN]
        r = rates(probes)
        out[SECTIONS[sec]] = (len(probes), r)
    return out


trans = []
for label, fn in (("as written", lambda w: w), ("o- removed", lambda w: w[1:]), ("o- read as qo-", lambda w: "q" + w)):
    for sec, (n, r) in transformed(fn).items():
        trans.append({"labels starting with o-": label, "section": sec, "n": n,
                      **{f"{k}: exact": r[k][0] for k in r}})
save(HERE, "labels_o", trans)
md += "\n## Labels starting with o-, read three ways (exact hits per 1000 text words)\n\n" + table(
    trans, ["labels starting with o-", "section", "n"] + [f"{k}: exact" for k in ks])
write_md(HERE, "labels", md)
print(md[md.index("## Labels starting"):])


# permutation test: labels reassigned at random to pages of their section that
# have running text; statistic = own-page exact hits summed over P, B, Z
def own_hits(assign, fn):
    return sum(sum(1 for x in text[p] if x == fn(w)) for w, p in assign)


perm_rows = []
prng = random.Random(1)
for label, fn, only_o in (("all labels, as written", lambda w: w, False),
                          ("o- labels, as written", lambda w: w, True),
                          ("o- labels read as qo-", lambda w: "q" + w, True)):
    probes = [(w, p) for p, ws in labels.items() if section[p] in ("P", "B", "Z") and text.get(p) for w in ws
              if (w.startswith("o") and len(w) > MIN_LEN) or not only_o]
    obs = own_hits(probes, fn)
    by_sec = defaultdict(list)
    for p in text:
        if section[p] in ("P", "B", "Z") and text[p]:
            by_sec[section[p]].append(p)
    null = []
    for _ in range(1000):
        null.append(own_hits([(w, prng.choice(by_sec[section[p]])) for w, p in probes], fn))
    perm_rows.append({"probes": label, "n": len(probes), "own-page hits": obs,
                      "if pages were random (mean)": sum(null) / len(null),
                      "p": (1 + sum(x >= obs for x in null)) / (len(null) + 1)})
    print(perm_rows[-1], flush=True)
save(HERE, "labels_perm", perm_rows)
md += "\n## Permutation test (labels moved to random pages of their section; pharmaceutical, bathing, zodiac)\n\n" + table(
    perm_rows, ["probes", "n", "own-page hits", "if pages were random (mean)", "p"])
write_md(HERE, "labels", md)
