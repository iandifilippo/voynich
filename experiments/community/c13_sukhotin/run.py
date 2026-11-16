"""Sukhotin's vowel algorithm (1962), as described by Guy (Cryptologia 1991).

The algorithm needs nothing but adjacency counts inside words. Make the
symmetric table of how often two letters touch (diagonal zeroed), call every
letter a consonant, then repeatedly take the consonant with the largest row
sum as a vowel and subtract twice its contacts from the sums of the others;
stop when no consonant has a positive sum. It works because in alphabetic
writing vowels and consonants alternate.

Run on the manuscript (EVA characters, and EVA with the usual composite
glyphs as one sign), the controls, and real texts. What matters is not only
which glyphs come out as vowels but how well the split works: the share of
adjacent pairs inside words that cross the split (vowel next to consonant).
For a real alphabet it is high; for random letters it is about half the
pairs that are not on the diagonal.
"""
import json
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
N = 20000
UNIT = re.compile(r"c[tkpf]h|ch|sh|.")


def sukhotin(seqs):
    m = Counter()
    letters = set()
    for s in seqs:
        letters.update(s)
        for a, b in zip(s, s[1:]):
            if a != b:
                m[a, b] += 1
                m[b, a] += 1
    letters = sorted(letters)
    sums = {x: sum(m[x, y] for y in letters) for x in letters}
    vowels = []
    while True:
        cons = [x for x in letters if x not in vowels]
        if not cons:
            break
        best = max(cons, key=lambda x: sums[x])
        if sums[best] <= 0:
            break
        vowels.append(best)
        for x in cons:
            if x != best:
                sums[x] -= 2 * m[x, best]
    pairs = [(a, b) for s in seqs for a, b in zip(s, s[1:]) if a != b]
    cross = sum((a in vowels) != (b in vowels) for a, b in pairs) / len(pairs)
    return vowels, cross, letters


def plain(words):
    out = []
    for w in words:
        w = unicodedata.normalize("NFD", w.lower())
        w = "".join(c for c in w if not unicodedata.combining(c) and c.isalpha())
        if w:
            out.append(w)
    return out


chart = {k: set(x) for k, x in json.loads(
    (HERE.parent.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}
v = Voynich("ZL")
body = [l for l in v.lines if l.unit == "P"]
eva = {"VMS, Currier A": [w for l in body if l.meta.get("L") == "A" for w in l.words],
       "VMS, Currier B": [w for l in body if l.meta.get("L") == "B" for w in l.words],
       "copying model": [w for l in AutoCopy(seed=1, boundary=chart, boundary_p=0.65, line_end_p=0.5,
                                             common_p=0.5).run(4500) for w in l],
       "Naibbe cipher of Pliny": open(DATA / "external" / "naibbe-cipher" / "encrypted" /
                                      "nathist_output_ciphertext.txt", encoding="utf-8-sig").read().split()}
real = {"Latin (Secreta secretorum)": plain(historical("Secreta_Secretorum_LAT")),
        "Italian (Rettorica)": plain(historical("Rettorica")),
        "English (Alphabet of Tales)": plain(historical("AlphabetOfTales")),
        "Hebrew (Mishneh, unvowelled)": plain(historical("Hebrew_Mishneh")),
        "Georgian (Amirandar)": plain(historical("Amirandar"))}
rng = random.Random(0)
rows = []


def add(name, split, seqs):
    seqs = [s for s in seqs if len(s) > 1][:N]
    vw, cross, letters = sukhotin(seqs)
    flat = [c for s in seqs for c in s]
    rng.shuffle(flat)
    it = iter(flat)
    shuf = [[next(it) for _ in s] for s in seqs]
    _, cross0, _ = sukhotin(shuf)
    rows.append({"text": name, "signs": split, "alphabet": len(letters), "vowels": " ".join(vw),
                 "pairs crossing the split": cross, "same, letters shuffled": cross0, "excess": cross - cross0})
    print(rows[-1], flush=True)


for name, words in eva.items():
    words = [w for w in words if w and "?" not in w and "'" not in w]
    add(name, "EVA characters", [list(w) for w in words])
    add(name, "ch sh cth... as one", [UNIT.findall(w) for w in words])
for name, words in real.items():
    add(name, "letters", [list(w) for w in words])

save(HERE, "sukhotin", rows)
md = "# c13 Sukhotin's vowel algorithm\n\n" + table(
    rows, ["text", "signs", "alphabet", "vowels", "pairs crossing the split", "same, letters shuffled", "excess"])
write_md(HERE, "sukhotin", md)
print(md)
