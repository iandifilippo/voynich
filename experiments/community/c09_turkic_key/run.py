"""The Turkic reading (Ata Team / Ardic, 2018), as listed on voynich.ninja.

A forum member collected the sound values shown in the team's video:
  o = o   y = u   a = e/a   e = c   ch = ç   sh = çye, çyedi   k = t or l
  t = b   d = s   l = p or x   r = r   i = i   n = ng   in = in
  iin = iin or m   m = k   q = d
and noted the oddities: m (line-final) = k, q (word-initial only) = d.

Same test as c07 and c08: read every word that uses only these signs, with
every allowed alternative, and count how often some reading is a word in a
Turkic lexicon (Turkish, Azerbaijani, Turkmen, Uzbek; diacritics stripped on
both sides). Against: the same values dealt to the signs at random, and two
texts with no Turkic in them (the copying model, a Naibbe cipher of Latin).
"""
import itertools
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
from voynich.corpus import DATA, wikipedia

HERE = pathlib.Path(__file__).parent
VAL = {"o": ["o"], "y": ["u"], "a": ["e", "a"], "e": ["c"], "ch": ["c"], "sh": ["cye", "cyedi"], "k": ["t", "l"],
       "t": ["b"], "d": ["s"], "l": ["p", "h"], "r": ["r"], "i": ["i"], "n": ["n", "ng"], "in": ["in"],
       "iin": ["iin", "m"], "m": ["k"], "q": ["d"]}
UNITS = sorted(VAL, key=len, reverse=True)


def plain(words):
    out = []
    for w in words:
        w = w.lower().replace("ı", "i").replace("ə", "e").replace("x", "h")
        w = unicodedata.normalize("NFD", w)
        w = re.sub(r"[^a-z]", "", "".join(c for c in w if not unicodedata.combining(c)))
        if w:
            out.append(w)
    return out


def cut(word):
    out, i = [], 0
    while i < len(word):
        for u in UNITS:
            if word.startswith(u, i):
                out.append(u)
                i += len(u)
                break
        else:
            return None
    return out


lex = {}
for lang in ("Turkish", "Azerbaijani", "Turkmen", "Uzbek"):
    c = Counter(plain(wikipedia(lang, 600000)))
    lex[lang] = {w for w, n in c.items() if n >= 2 and len(w) >= 3}
lex["any of the four"] = set().union(*lex.values())


def rate(words, val, lexicon):
    hits = n = 0
    for w in words:
        c = cut(w)
        if not c or len(w) < 3:
            continue
        n += 1
        opts = [val[u] for u in c]
        k = 1
        for o in opts:
            k *= len(o)
        if k <= 64 and any("".join(x) in lexicon for x in itertools.product(*opts)):
            hits += 1
    return hits / n if n else 0.0, n


chart = {k: set(x) for k, x in json.loads(
    (HERE.parent.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}
v = Voynich("ZL")
sources = {"VMS, all": [w for l in v.lines for w in l.words],
           "copying model": [w for l in AutoCopy(seed=1, boundary=chart, boundary_p=0.65, line_end_p=0.5,
                                                 common_p=0.5).run(4500) for w in l]}
src = DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt"
if src.exists():
    sources["Naibbe cipher of Pliny (Latin)"] = open(src, encoding="utf-8-sig").read().split()

rng = random.Random(0)
rows = []
keys = list(VAL)
for name, words in sources.items():
    types = list(set(words))
    for lang, L in lex.items():
        obs, n = rate(words, VAL, L)
        obs_t, nt = rate(types, VAL, L)
        null, null_t = [], []
        for _ in range(200):
            vals = [VAL[k] for k in keys]
            rng.shuffle(vals)
            val = dict(zip(keys, vals))
            null.append(rate(words, val, L)[0])
            null_t.append(rate(types, val, L)[0])
        rows.append({"text": name, "lexicon": lang, "words tested": n, "read as a word": obs,
                     "values shuffled": sum(null) / 200, "p": (1 + sum(x >= obs for x in null)) / 201,
                     "distinct words tested": nt, "distinct: read as a word": obs_t,
                     "distinct: shuffled": sum(null_t) / 200,
                     "distinct: p": (1 + sum(x >= obs_t for x in null_t)) / 201})
        print(rows[-1])

# his odd assignments, in numbers
allw = [(w, i, len(l.words)) for l in v.lines if l.unit == "P" for i, w in enumerate(l.words)]
m_final = sum(1 for w, i, n in allw if w.endswith("m") and i == n - 1) / max(1, sum(1 for w, i, n in allw if w.endswith("m")))
q_tot = sum(w.count("q") for w, _, _ in allw)
q_init = sum(1 for w, _, _ in allw if w.startswith("q")) / q_tot
odd = {"share of words ending in m that end a line": m_final, "share of q that begin a word": q_init}

save(HERE, "turkic", {"rows": rows, "odd": odd})
md = "# c09 the Turkic sound values\n\n" + table(
    rows, ["text", "lexicon", "words tested", "read as a word", "values shuffled", "p",
           "distinct words tested", "distinct: read as a word", "distinct: shuffled", "distinct: p"])
md += "\n" + table([{"": k, "value": x} for k, x in odd.items()], ["", "value"])
write_md(HERE, "turkic", md)
print(md)
