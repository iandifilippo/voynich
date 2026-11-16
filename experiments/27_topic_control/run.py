"""Would the page test see a subject if there was one?

Exp. 25 says a herbal A page has no vocabulary of its own: far-apart lines of
the same page share nothing extra, and the end of one plant runs into the
start of the next. That only means something if the same measurement, on a
text that really is organised by subject, finds the subject.

Control: Pliny, Natural History book 16 (trees), 44 chapters, in the edition's
own lines (about nine words each): a Latin text about plants, chapter by
chapter. Then the same book through the Naibbe cipher, chapter structure kept,
to see whether a verbose homophonic cipher would hide a subject from this test.
And the copying model, which has no subject at all.

Same statistic as exp. 25 (shared word types between two lines over the number
expected from overall rates), "page" = chapter for Pliny.
"""
import json
import pathlib
import random
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich
from voynich.autocopy import AutoCopy
from voynich.corpus import DATA
from voynich.naibbe import Naibbe

HERE = pathlib.Path(__file__).parent
BOOT = 500
ROOT = DATA / "external" / "naibbe-cipher"
chart = {k: set(v) for k, v in json.loads(
    (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}


def measure(pages, seed=0, band="all", top=60):
    """pages: list of pages, each a list of lines (lists of words), in order.
    band 'rare' drops the `top` most widespread word types before comparing."""
    pages = [[set(l) for l in p if len(l) >= 3] for p in pages]
    pages = [p for p in pages if len(p) >= 2]
    fl, n = Counter(), 0
    for p in pages:
        for s in p:
            fl.update(s)
            n += 1
    if band == "rare":
        common = {w for w, _ in fl.most_common(top)}
        pages = [[s - common for s in p] for p in pages]
        for w in common:
            del fl[w]
    exp = sum(c * (c - 1) for c in fl.values()) / (n * (n - 1))   # two different lines
    cats = {}

    def add(cat, key, a, b):
        t = cats.setdefault(cat, {}).setdefault(key, [0, 0])
        t[0] += 1
        t[1] += len(a & b)

    for pi, ls in enumerate(pages):
        for i in range(len(ls)):
            for j in range(i + 1, min(len(ls), i + 31)):
                d = j - i
                if d <= 5:
                    add("same page, 1-5 lines apart", pi, ls[i], ls[j])
                elif d >= 10:
                    add("same page, 10-30 lines apart", pi, ls[i], ls[j])
        for gap, cat in [(1, "across the page break, 1-5 lines")] + [(g, "end of page vs start of a page 2-6 on") for g in range(2, 7)]:
            if pi + gap < len(pages):
                ms = pages[pi + gap]
                for i in range(max(0, len(ls) - 5), len(ls)):
                    for j in range(min(5, len(ms))):
                        if (len(ls) - i) + j <= 5:
                            add(cat, pi + gap, ls[i], ms[j])
        for gap, cat in [(1, "next page, any lines"), (3, "3 pages on, any lines"), (8, "8 pages on, any lines")]:
            if pi + gap < len(pages):
                for a in ls[::3]:
                    for b in pages[pi + gap][::3]:
                        add(cat, pi + gap, a, b)

    rng = random.Random(seed)

    def lift(cat, keys=None):
        d = cats.get(cat, {})
        keys = list(d) if keys is None else keys
        npairs = sum(d[k][0] for k in keys if k in d)
        return sum(d[k][1] for k in keys if k in d) / (npairs * exp) if npairs else float("nan")

    def ratio(a, b):
        keys = sorted(set(cats.get(a, {})) | set(cats.get(b, {})))
        obs = lift(a) / lift(b)
        bs = []
        for _ in range(BOOT):
            ks = [rng.choice(keys) for _ in keys]
            x, y = lift(a, ks), lift(b, ks)
            if x == x and y == y and y > 0:
                bs.append(x / y)
        bs.sort()
        return obs, f"{bs[int(.025 * len(bs))]:.2f}-{bs[int(.975 * len(bs))]:.2f}"

    # is the real next page recognisable?
    pct = []
    for i in range(len(pages) - 1):
        def sc(j):
            A, B = pages[i][-5:], pages[j][:5]
            return sum(len(x & y) for x in A for y in B) / (len(A) * len(B))
        true = sc(i + 1)
        others = [sc(j) for j in range(len(pages)) if j not in (i, i + 1)]
        pct.append((sum(o < true for o in others) + 0.5 * sum(o == true for o in others)) / len(others))

    out = {"pages": len(pages), "lines": n}
    for c in ["same page, 1-5 lines apart", "same page, 10-30 lines apart", "across the page break, 1-5 lines",
              "end of page vs start of a page 2-6 on", "next page, any lines", "3 pages on, any lines",
              "8 pages on, any lines"]:
        out[c] = lift(c)
    out["own vocabulary: same page far apart / 3 pages on"], out["ci_own"] = ratio(
        "same page, 10-30 lines apart", "3 pages on, any lines")
    out["break / same page near"], out["ci_break"] = ratio(
        "across the page break, 1-5 lines", "same page, 1-5 lines apart")
    out["break / control"], out["ci_control"] = ratio(
        "across the page break, 1-5 lines", "end of page vs start of a page 2-6 on")
    out["next page percentile"] = sum(pct) / len(pct)
    return out


def own_vocabulary(pages, band="all", top=60, dmin=3, dmax=12, shifts=400, seed=0):
    """At the same distance in lines, do two lines of the same page share more
    than two lines with a page break between them? Null: the same sequence of
    lines with the page breaks slid along by a random amount."""
    pages = [[set(l) for l in p if len(l) >= 3] for p in pages]
    pages = [p for p in pages if len(p) >= 2]
    lines = [s for p in pages for s in p]
    if band == "rare":
        fl = Counter(w for s in lines for w in s)
        common = {w for w, _ in fl.most_common(top)}
        lines = [s - common for s in lines]
    n = len(lines)
    share = {d: [len(lines[i] & lines[i + d]) for i in range(n - d)] for d in range(dmin, dmax + 1)}
    sizes = [len(p) for p in pages]

    def ratio(offset):
        page_of, k = [0] * n, 0
        pos = offset % n
        for pi, size in enumerate(sizes):
            for _ in range(size):
                page_of[pos] = pi
                pos = (pos + 1) % n
        num = den = 0.0
        for d, xs in share.items():
            same = [x for i, x in enumerate(xs) if page_of[i] == page_of[i + d]]
            diff = [x for i, x in enumerate(xs) if page_of[i] != page_of[i + d]]
            if same and diff:
                w = min(len(same), len(diff))
                num += w * sum(same) / len(same)
                den += w * sum(diff) / len(diff)
        return num / den if den else float("nan")

    obs = ratio(0)
    rng = random.Random(seed)
    null = [ratio(rng.randrange(2, n - 2)) for _ in range(shifts)]
    null = [x for x in null if x == x]
    mu = sum(null) / len(null)
    return {"same page / across a break, same distance": obs, "with breaks slid along": mu,
            "p": (1 + sum(x >= obs for x in null)) / (1 + len(null))}


# --- texts -------------------------------------------------------------------
def pliny():
    """chapters of book 16 as (plain lines, respaced unit lines); the two files are line-aligned"""
    raw = open(ROOT / "input" / "examples" / "nathist_book16.txt", encoding="utf-8").read().split("\n")
    units = open(ROOT / "respaced_plaintext" / "nathist_pre_encryption_respaced_plaintext.txt",
                 encoding="utf-8").read().split("\n")
    plain, resp = [], []
    for k, line in enumerate(raw):
        t = line.strip()
        if re.fullmatch(r"[IVXLC]+", t):
            plain.append([])
            resp.append([])
        elif t and not t.isdigit() and plain:
            words = re.findall(r"[a-z]+", t.lower())
            if words:
                plain[-1].append(words)
                resp[-1].append(units[k].split() if k < len(units) else [])
    return plain, resp


def vms(**sel):
    v = Voynich("ZL")
    pages = {}
    for l in v.select(unit="P", **sel):
        pages.setdefault(l.page, []).append(l.words)
    return [pages[p] for p in v.pages if p in pages]


plain, resp = pliny()
aligned = sum(len(p) for p in plain) == sum(1 for ch in resp for l in ch if l)
cipher = []
nb = Naibbe(seed=1)
for ch in resp:
    cipher.append(nb.encrypt(ch))
rng = random.Random(3)
shuffled_lines = [l for ch in plain for l in ch]
rng.shuffle(shuffled_lines)
it = iter(shuffled_lines)
plain_shuffled = [[next(it) for _ in ch] for ch in plain]
model = AutoCopy(seed=1, currier="A", boundary=chart, boundary_p=0.65, line_end_p=0.5, common_p=0.5,
                 page_lines=13).run(1235)
model_pages = [model[i:i + 13] for i in range(0, len(model), 13)]

texts = {
    "VMS herbal A, hand 1": vms(language="A", hand="1", section="H"),
    "VMS balneo B, hand 2": vms(language="B", hand="2", section="B"),
    "VMS stars B, hand 3": vms(language="B", hand="3", section="S"),
    "Pliny 16, chapters": plain,
    "Pliny 16, lines dealt at random into the chapters": plain_shuffled,
    "Naibbe cipher of Pliny 16, chapters": cipher,
    "copying model, 13-line pages": model_pages,
}
rows, rare = [], []
for name, pages in texts.items():
    for band, dest in (("all", rows), ("rare", rare)):
        r = measure(pages, band=band)
        r["text"] = name
        dest.append(r)
        print(band, name, {k: round(x, 3) if isinstance(x, float) else x for k, x in r.items()})

own = []
for name, pages in texts.items():
    for band in ("all", "rare"):
        r = own_vocabulary(pages, band)
        own.append({"text": name, "words": "all" if band == "all" else "without the 60 commonest", **r})
        print(own[-1])

save(HERE, "topic_control", {"own_vocabulary": own, "all_words": rows, "without_60_commonest": rare, "pliny_files_aligned": aligned})
md = "# 27 would the page test see a subject?\n\n"
md += table(rows, ["text", "pages", "lines", "same page, 1-5 lines apart", "same page, 10-30 lines apart",
                   "across the page break, 1-5 lines", "end of page vs start of a page 2-6 on",
                   "next page, any lines", "3 pages on, any lines", "8 pages on, any lines"])
md += "\n## does a page have vocabulary of its own?\n\nLines 3-12 apart: shared word types when both are on the same page, over shared word types when a page break lies between them, at matched distances. Null: the page breaks slid along the text.\n\n"
md += table(own, ["text", "words", "same page / across a break, same distance", "with breaks slid along", "p"])
md += "\n## carry-over at the break\n\n" + table(
    rows, ["text", "break / same page near", "ci_break",
           "break / control", "ci_control", "next page percentile"])
md += "\n## the same without each text's 60 most widespread words\n\n" + table(
    rare, ["text", "same page, 1-5 lines apart", "same page, 10-30 lines apart", "across the page break, 1-5 lines",
           "end of page vs start of a page 2-6 on", "next page, any lines", "3 pages on, any lines", "8 pages on, any lines"])
md += "\n" + table(
    rare, ["text", "break / same page near", "ci_break",
           "break / control", "ci_control", "next page percentile"])
md += "\n`break / same page near` = 1: the page break costs nothing.\n"
write_md(HERE, "topic_control", md)
print(md)
