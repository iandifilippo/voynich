"""Page identity in real texts, for comparison.

run.py found that each Voynich page has fork habits of its own, and that they
survive when the words the two halves share are removed. Is that what a
text about changing subjects looks like? In a language a page's subject
shows mostly in its content words, which recur on the page; take those away
and what is left (word beginnings and endings in general) should carry much
less of the page's identity.

Same test on texts whose subject changes from entry to entry: a medical
casebook, a book of tales, a surgery, a book of secrets, Picatrix, and the
Rettorica, cut into "pages" of about the size of a herbal page (14 lines of 8
words). The profile is generic so that every text gets the same treatment:
the share of words starting with each of the 15 commonest two-letter
beginnings and ending with each of the 15 commonest two-letter endings in
that text. The manuscript sections are run through the same generic profile.
"""
import pathlib
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402
from voynich.corpus import historical  # noqa: E402

HERE = pathlib.Path(__file__).parent
N_PAGES, LINES, PER_LINE = 50, 14, 8


def generic(words_all):
    st = [s for s, _ in Counter(w[:2] for w in words_all).most_common(15)]
    en = [e for e, _ in Counter(w[-2:] for w in words_all).most_common(15)]

    def prof(words):
        n = max(len(words), 1)
        c1 = Counter(w[:2] for w in words)
        c2 = Counter(w[-2:] for w in words)
        return np.array([c1[s] / n for s in st] + [1 - sum(c1[s] for s in st) / n] +
                        [c2[e] / n for e in en] + [1 - sum(c2[e] for e in en) / n])
    return prof


def halves(lines):
    return [w for l in lines[0::2] for w in l], [w for l in lines[1::2] for w in l]


def identity(pages, prof, unshared):
    H = [halves(p) for p in pages]
    n = len(H)
    sets = [(set(a), set(b)) for a, b in H]
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a, b = H[i][0], H[j][1]
            if unshared:
                a = [w for w in a if w not in sets[j][1]]
                b = [w for w in b if w not in sets[i][0]]
            D[i, j] = ((prof(a) - prof(b)) ** 2).sum()
    top = 0
    for M in (D, D.T):
        for i in range(n):
            top += int(np.argmin(M[i])) == i
    return top / (2 * n)


def plain(ws):
    out = []
    for w in ws:
        w = unicodedata.normalize("NFD", w.lower())
        w = "".join(c for c in w if not unicodedata.combining(c) and c.isalpha())
        if len(w) > 0:
            out.append(w)
    return out


texts = {"Casebook (English medical cases)": "Casebook_norm", "Alphabet of Tales (English)": "AlphabetOfTales",
         "Cirurgie (English surgery)": "Cirurgie", "Secreta secretorum (Latin)": "Secreta_Secretorum_LAT",
         "Picatrix (Latin)": "Picatrix", "Rettorica (Italian)": "Rettorica"}
rows = []
for label, name in texts.items():
    ws = plain(historical(name))
    lines = [ws[i:i + PER_LINE] for i in range(0, len(ws), PER_LINE)]
    pages = [lines[i:i + LINES] for i in range(0, len(lines), LINES)][:N_PAGES]
    prof = generic([w for p in pages for l in p for w in l])
    a, b = identity(pages, prof, False), identity(pages, prof, True)
    rows.append({"text": label, "pages": len(pages), "own half closest": a, "shared words removed": b,
                 "kept": b / a if a else float("nan")})
    print(rows[-1], flush=True)

v = Voynich("ZL")
book, meta = defaultdict(list), {}
for l in v.lines:
    if l.unit == "P":
        ws = [w for w in l.words if "?" not in w and "'" not in w]
        if ws:
            book[l.page].append(ws)
            meta[l.page] = (l.meta.get("H"), l.meta.get("I"))
for label, key in [("VMS hand 1 herbal", ("1", "H")), ("VMS hand 2 herbal", ("2", "H")),
                   ("VMS hand 2 bathing", ("2", "B")), ("VMS hand 3 stars", ("3", "S"))]:
    pages = [book[p] for p in book if meta[p] == key and sum(map(len, book[p])) >= 80]
    prof = generic([w for p in pages for l in p for w in l])
    a, b = identity(pages, prof, False), identity(pages, prof, True)
    rows.append({"text": label, "pages": len(pages), "own half closest": a, "shared words removed": b,
                 "kept": b / a if a else float("nan")})
    print(rows[-1], flush=True)

save(HERE, "languages", rows)
write_md(HERE, "languages", "# 40 page identity with a generic profile, real texts and the manuscript\n\n" + table(
    rows, ["text", "pages", "own half closest", "shared words removed", "kept"]))
print(table(rows, ["text", "pages", "own half closest", "shared words removed", "kept"]))
