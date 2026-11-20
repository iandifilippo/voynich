"""Would a cipher with fixed tables give pages an identity?

Exp. 40: every Voynich page has its own fork weights, and real texts barely
show any such thing in their word shapes. A cipher that turns letters into
Voynich-like words through fixed tables (the Naibbe family) passes the
plaintext's letter statistics through to the forks, so its pages should be
about as recognisable as the plaintext's pages: barely.

Same test as exp. 40 (half a page against all other halves, fork profile,
shared words removed too) on:
  the Naibbe cipher of Pliny, Natural History book 16 (fixed tables)
  the plaintext of that cipher, with the generic profile of exp. 40
and, for comparison, the manuscript's stars and bathing sections.
Pages of 14 lines of 8 words, 50 pages.
"""
import csv
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "40_page_identity"))
from _common import save, table, write_md  # noqa: E402
from voynich.corpus import DATA  # noqa: E402
from voynich.forks import profile  # noqa: E402

HERE = pathlib.Path(__file__).parent
LINES, PER_LINE, N_PAGES = 14, 8, 50
NB = DATA / "external" / "naibbe-cipher"


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
    return sum(int(np.argmin(M[i])) == i for M in (D, D.T) for i in range(n)) / (2 * n)


def pages_of(words):
    lines = [words[i:i + PER_LINE] for i in range(0, len(words), PER_LINE)]
    return [lines[i:i + LINES] for i in range(0, len(lines), LINES)][:N_PAGES]


def decode():
    uni, pre, suf = {}, {}, {}
    for code, g in list(csv.reader(open(NB / "references" / "naibbe_tables.csv", encoding="utf-8-sig")))[1:]:
        kind, _, let = code.split("_")
        {"unigram": uni, "prefix": pre, "suffix": suf}[kind].setdefault(g, let)
    return uni, pre, suf


cipher = open(NB / "encrypted" / "nathist_output_ciphertext.txt", encoding="utf-8-sig").read().split()
uni, pre, suf = decode()
plain = []
for w in cipher:
    if w in uni:
        plain.append(uni[w])
    else:
        for i in range(1, len(w)):
            if w[:i] in pre and w[i:] in suf:
                plain.append(pre[w[:i]] + suf[w[i:]])
                break
plaintext = "".join(plain)

import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location("langs", HERE.parent / "40_page_identity" / "languages.py")
src = (HERE.parent / "40_page_identity" / "languages.py").read_text()
gen_src = src[src.index("def generic("):src.index("def halves(")]
ns = {"np": np, "Counter": __import__("collections").Counter}
exec(gen_src, ns)
generic = ns["generic"]

# plaintext of the cipher, re-cut into words of the original text length is not
# recoverable (spaces are lost), so use the letters in chunks of 5 as "words"
pwords = [plaintext[i:i + 5] for i in range(0, len(plaintext), 5)]
rows = []
for label, pages, prof in [
        ("Naibbe cipher of Pliny (fixed tables)", pages_of(cipher), profile),
        ("its plaintext, letters in 5s", pages_of(pwords), generic(pwords))]:
    rows.append({"text": label, "pages": len(pages), "own half closest": identity(pages, prof, False),
                 "shared words removed": identity(pages, prof, True), "chance": 1 / len(pages)})
    print(rows[-1], flush=True)
prev = __import__("json").loads((HERE.parent / "40_page_identity" / "results" / "page_identity.json").read_text())
for r in prev:
    if r["text"] == "manuscript":
        rows.append({"text": f"manuscript, {r['pages']} (exp. 40)", "pages": r["n pages"],
                     "own half closest": r["own half closest"],
                     "shared words removed": r["own half closest, shared words removed"], "chance": 1 / r["n pages"]})
save(HERE, "cipher_identity", rows)
md = "# 43 page identity in a fixed-table cipher\n\n" + table(
    rows, ["text", "pages", "own half closest", "shared words removed", "chance"])
write_md(HERE, "cipher_identity", md)
print(md)
