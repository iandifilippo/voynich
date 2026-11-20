"""Attack 5: if a word is a letter, its neighbours give it away.

In any cipher where each word stands for a letter (or a letter with a
neighbour, as in the Naibbe family), words for the same letter behave alike
towards the words around them. Group the words so that the class of one word
predicts the class of the next as well as possible (exchange clustering,
voynich/crack/classes.py), and the classes become the alphabet, with the
letter statistics of the plaintext.

This needs no guess about the language and no segmentation of words, and it
is blind to how the words are spelled, so it is untouched by the slot
grammar. It's measured honestly: classes are fitted on the even pages (or
the first half of a text) and their predictive power, the mutual information
between the classes of adjacent words, is measured on the rest.

Calibration: the Naibbe cipher of Pliny. Against it: Currier A and B, the
copying model, the exp. 36 generator, the words of Latin and Italian (words
as tokens), and the letters of Latin (letters as tokens: what a cipher with
one word per letter would show).
"""
import json
import pathlib
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich
from voynich.assemble import Assembler
from voynich.autocopy import AutoCopy
from voynich.corpus import DATA, historical
from voynich.crack.classes import class_mi, fit

HERE = pathlib.Path(__file__).parent
KS = [2, 4, 8, 16, 24, 32]
N_WORDS = 11000
PER_LINE = 9
chart = {k: set(x) for k, x in json.loads(
    (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}


def plain(ws):
    out = []
    for w in ws:
        w = unicodedata.normalize("NFD", w.lower())
        w = re.sub(r"[^a-z]", "", "".join(c for c in w if not unicodedata.combining(c)))
        if w:
            out.append(w)
    return out


def lines_of(tokens):
    return [tokens[i:i + PER_LINE] for i in range(0, len(tokens), PER_LINE)]


def cap(lines, n):
    out, k = [], 0
    for l in lines:
        if k >= n:
            break
        out.append(l)
        k += len(l)
    return out


def vms(lang):
    v = Voynich("ZL")
    pages = defaultdict(list)
    for l in v.lines:
        if l.unit == "P" and l.meta.get("L") == lang:
            ws = [w for w in l.words if "?" not in w and "'" not in w]
            if ws:
                pages[l.page].append(ws)
    order = list(pages)
    return [l for p in order[0::2] for l in pages[p]], [l for p in order[1::2] for l in pages[p]]


def halves(lines):
    return lines[0::2], lines[1::2]


def assembled():
    tr, te = vms("B")
    m = Assembler(order=2, recall_p=0.01, edit_p=0.10, window=5).fit(tr + te)
    out = m.fill([(len(l), False) for l in tr + te], seed=1)
    return halves(out)


def texts():
    nb = open(DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt",
              encoding="utf-8-sig").read().split()
    lat = plain(historical("Secreta_Secretorum_LAT"))
    ita = plain(historical("Rettorica"))
    cp = AutoCopy(seed=1, boundary=chart, boundary_p=0.65, line_end_p=0.5, common_p=0.5).run(3000)
    return {
        "Naibbe cipher of Pliny": halves(lines_of(nb[:2 * N_WORDS])),
        "VMS Currier B": vms("B"),
        "VMS Currier A": vms("A"),
        "copying model": halves([l for l in cp if l]),
        "assembled words (exp. 36)": assembled(),
        "Latin, words": halves(lines_of(lat[:2 * N_WORDS])),
        "Italian, words": halves(lines_of(ita[:2 * N_WORDS])),
        "Latin, letters as tokens": halves(lines_of(list("".join(lat))[:2 * N_WORDS])),
    }


if __name__ == "__main__":
    rows = []
    for name, (train, test) in texts().items():
        train, test = cap(train, N_WORDS), cap(test, N_WORDS)
        flat = [w for l in train for w in l]
        cover = Counter(w for l in test for w in l)
        seen = sum(c for w, c in cover.items() if w in set(flat)) / sum(cover.values())
        row = {"text": name, "types (train)": len(set(flat)), "test tokens seen in train": seen}
        shuffled = [w for l in train for w in l]
        random.Random(0).shuffle(shuffled)
        it = iter(shuffled)
        shuf = [[next(it) for _ in l] for l in train]
        for K in KS:
            mi, assign = fit(train, K)
            held = class_mi(test, assign, unknown=K)
            _, a0 = fit(shuf, K)
            held0 = class_mi(test, a0, unknown=K)
            row[f"K={K}"] = held - held0
            row[f"K={K} train"] = mi
            row[f"K={K} raw"] = held
        rows.append(row)
        print({k: (round(x, 3) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
    save(HERE, "classes", rows)
    md = ("# 44 word classes from neighbours\n\nHeld-out mutual information (bits) between the classes of adjacent "
          "words, minus the same with classes fitted on the training half with its words shuffled.\n\n")
    md += table(rows, ["text", "types (train)", "test tokens seen in train"] + [f"K={k}" for k in KS])
    md += "\n## Raw held-out MI and training MI\n\n" + table(
        rows, ["text"] + [f"K={k} raw" for k in KS] + [f"K={k} train" for k in (8, 24)])
    write_md(HERE, "classes", md)
    print(md)
