"""voynich.ninja, Geoffrey Caveney: f67r1 line 1 read as Byzantine Greek.

[teeodaiin shey epairody osaiin yteeoey shey epaiin oaiin]
"geiopan tis ipeirous otan skiiois tis epan oan"
"When the whole Earth and all the continents are in the shadows, as they said"

His values: t = k or g; s, sh = t; y = s; r = r; iin = n; p = p; e = e or i;
ai = ei; a = a; o = o; d = u/v, or p after a gallows. He also proposes a test:
merge voiced and voiceless letters in ordinary texts (g>k, d>t, b>p, z>s, and
p, f > v, u = v) and see whether their entropy comes down to the manuscript's.

Checks
 A. his test, as stated: h1 and h2 of Greek, Latin, Italian, French before and
    after the merger, against the manuscript.
 B. how many different strings his values allow for that one line.
 C. the same values on the rest of the text: how often does a word come out
    as a Greek word, against the same key with its values shuffled, and
    against the copying model.
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
from voynich import Voynich, metrics
from voynich.autocopy import AutoCopy
from voynich.corpus import historical, wikipedia

HERE = pathlib.Path(__file__).parent
GREEK = dict(zip("αβγδεζηθικλμνξοπρστυφχψως", "abgdezhqiklmnxoprstufcyws"))


def plain(words):
    out = []
    for w in words:
        w = unicodedata.normalize("NFD", w.lower())
        w = "".join(GREEK.get(c, c) for c in w if not unicodedata.combining(c))
        w = re.sub(r"[^a-z]", "", w)
        if w:
            out.append(w)
    return out


def devoice(w):
    w = w.replace("u", "v")
    return w.translate(str.maketrans("gdbzpf", "ktpsvv"))


# A ---------------------------------------------------------------------
texts = {"Greek (modern, transliterated)": plain(wikipedia("Greek", 60000)),
         "Latin (Aix)": plain(historical("Latin_Aix", 60000)),
         "Italian (Rettorica)": plain(historical("Rettorica", 60000)),
         "French": plain(wikipedia("French", 60000))}
v = Voynich("ZL")
vp = metrics.profile(v.text_lines(unit="P"), 10000)
ent = [{"text": "VMS", "h1": vp["h1"], "h2": vp["h2"], "h1 merged": None, "h2 merged": None, "h2 drop": None}]
for name, ws in texts.items():
    a = metrics.profile([ws[i:i + 9] for i in range(0, len(ws), 9)], 10000)
    m = [devoice(w) for w in ws]
    b = metrics.profile([m[i:i + 9] for i in range(0, len(m), 9)], 10000)
    ent.append({"text": name, "h1": a["h1"], "h2": a["h2"], "h1 merged": b["h1"], "h2 merged": b["h2"],
                "h2 drop": a["h2"] - b["h2"]})

# B ---------------------------------------------------------------------
VAL = {"t": ["k", "g"], "s": ["t"], "sh": ["t"], "y": ["s"], "r": ["r"], "iin": ["n"], "p": ["p"],
       "e": ["e", "i"], "ai": ["ei"], "a": ["a"], "o": ["o"], "d": ["u", "p"], "ee": ["e", "i", "ei", "ii"]}
UNITS = sorted(VAL, key=len, reverse=True)


def cut(word):
    out, i = [], 0
    while i < len(word):
        if word.startswith("aiin", i):      # his rule: iin is one sign, the a before it stands alone
            out += ["a", "iin"]
            i += 4
            continue
        for u in UNITS:
            if word.startswith(u, i):
                out.append(u)
                i += len(u)
                break
        else:
            return None
    return out


line = "teeodaiin shey epairody osaiin yteeoey shey epaiin oaiin".split()
freedom = []
total = 1
for w in line:
    c = cut(w)
    n = 1
    for u in c:
        n *= len(VAL[u])
    total *= n
    freedom.append({"word": w, "units": " ".join(c), "readings allowed": n})

# C ---------------------------------------------------------------------
greek_words = Counter(plain(wikipedia("Greek", 600000)))
lexicon = {w for w, c in greek_words.items() if c >= 2 and len(w) >= 3}


def hit_rate(words, val, rng=None):
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
        if k > 64:
            continue
        if any("".join(x) in lexicon for x in itertools.product(*opts)):
            hits += 1
    return hits / n if n else 0.0, n


chart = {k: set(x) for k, x in json.loads(
    (HERE.parent.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}
sources = {"VMS, all": [w for l in v.lines for w in l.words],
           "copying model": [w for l in AutoCopy(seed=1, boundary=chart, boundary_p=0.65, line_end_p=0.5,
                                                 common_p=0.5).run(4500) for w in l]}
rng = random.Random(0)
keytest = []
for name, words in sources.items():
    obs, n = hit_rate(words, VAL)
    null = []
    keys = list(VAL)
    for _ in range(300):
        vals = [VAL[k] for k in keys]
        rng.shuffle(vals)
        null.append(hit_rate(words, dict(zip(keys, vals)))[0])
    keytest.append({"text": name, "words tested": n, "come out as a Greek word": obs,
                    "same values shuffled": sum(null) / len(null),
                    "p": (1 + sum(x >= obs for x in null)) / 301})

save(HERE, "caveney", {"entropy": ent, "freedom": freedom, "readings_for_line": total, "keytest": keytest})
md = "# c08 Caveney's Greek line\n\n## A. his own test: merge voiced and voiceless letters\n\n" + table(
    ent, ["text", "h1", "h2", "h1 merged", "h2 merged", "h2 drop"])
md += f"\n## B. how much room the values leave\n\n" + table(freedom, ["word", "units", "readings allowed"])
md += f"\nReadings allowed for the whole line: {total}\n"
md += "\n## C. the same values on the rest of the text\n\n" + table(
    keytest, ["text", "words tested", "come out as a Greek word", "same values shuffled", "p"])
write_md(HERE, "caveney", md)
print(md)
